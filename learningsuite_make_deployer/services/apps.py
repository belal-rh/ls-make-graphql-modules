from __future__ import annotations

from typing import Any, Mapping

from ..client import MakeClient
from ..errors import DeploymentError

APP_DESCRIPTION = "Private Custom App für die inoffizielle LearningSuite GraphQL API."


def _version(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _list_apps(client: MakeClient) -> list[Mapping[str, Any]]:
    result = client.call("GET", "/sdk/apps?opensource=false")
    apps = result.get("apps", []) if isinstance(result, Mapping) else []
    return [item for item in apps if isinstance(item, Mapping)]


def _candidate_score(
    client: MakeClient,
    app: Mapping[str, Any],
    preferred_name: str | None,
) -> tuple[int, str]:
    name = str(app.get("name", ""))
    label = str(app.get("label", ""))
    version = _version(app.get("version"), client.settings.version)
    score = 0
    if preferred_name and name == preferred_name:
        score += 100
    if name == client.settings.app_name:
        score += 80
    if name.startswith(client.settings.app_name + "-"):
        score += 60
    if label == client.settings.app_label:
        score += 40
    if version == client.settings.version:
        score += 20
    if app.get("beta") is True:
        score += 5
    return score, name


def _resolve_existing_app(
    client: MakeClient,
    *,
    preferred_name: str | None = None,
) -> tuple[str, int] | None:
    ranked: list[tuple[int, str, int]] = []
    for app in _list_apps(client):
        score, name = _candidate_score(client, app, preferred_name)
        if score <= 0 or not name:
            continue
        ranked.append((score, name, _version(app.get("version"), client.settings.version)))

    for _, name, version in sorted(ranked, reverse=True):
        found = client.optional("GET", f"/sdk/apps/{name}/{version}")
        if found is not None:
            return name, version
    return None


def _metadata_payload(client: MakeClient) -> dict[str, Any]:
    return {
        "label": client.settings.app_label,
        "description": APP_DESCRIPTION,
        "theme": "#EA5B0C",
        "language": "de",
    }


def _create_payload(client: MakeClient) -> dict[str, Any]:
    return {
        "name": client.settings.app_name,
        **_metadata_payload(client),
        "version": client.settings.version,
        "beta": True,
        "manifestVersion": 2,
    }


def ensure_app(client: MakeClient) -> tuple[str, int]:
    existing = _resolve_existing_app(client)
    if existing is not None:
        app_name, version = existing
        print(f"✓ App vorhanden: {app_name} v{version}")
        client.call(
            "PATCH",
            f"/sdk/apps/{app_name}/{version}",
            payload=_metadata_payload(client),
        )
        return app_name, version

    print(f"+ Erstelle App: {client.settings.app_name}")
    payload = _create_payload(client)
    try:
        created = client.call("POST", "/sdk/apps", payload=payload)
    except DeploymentError as top_level_error:
        print("  Top-Level-Payload abgelehnt; versuche app-Wrapper …")
        try:
            created = client.call("POST", "/sdk/apps", payload={"app": payload})
        except DeploymentError as wrapper_error:
            raise DeploymentError(
                "App konnte mit keinem bekannten Make-Payload-Format erstellt werden. "
                f"Top-Level: {top_level_error}; app-Wrapper: {wrapper_error}"
            ) from wrapper_error

    preferred_name: str | None = None
    if isinstance(created, Mapping):
        nested = created.get("app")
        app = nested if isinstance(nested, Mapping) else created
        if app.get("name"):
            preferred_name = str(app["name"])

    resolved = _resolve_existing_app(client, preferred_name=preferred_name)
    if resolved is None:
        raise DeploymentError(
            "Make hat die App-Erstellung bestätigt, die App konnte danach aber nicht "
            "über GET /sdk/apps verifiziert werden."
        )
    app_name, version = resolved
    print(f"✓ App aufgelöst: {app_name} v{version}")
    return app_name, version


def apply_app_visibility(client: MakeClient, app_name: str, version: int) -> None:
    target = client.settings.visibility
    if target == "preserve":
        print("= App-Sichtbarkeit bleibt unverändert")
        return

    try:
        client.call("POST", f"/sdk/apps/{app_name}/{version}/{target}", payload={})
        print(f"✓ App-Sichtbarkeit gesetzt: {target}")
    except DeploymentError as exc:
        if target == "private" and (
            exc.api_code == "IM005" or exc.has_text("can't make published app private")
        ):
            raise DeploymentError(
                "Die App ist bereits veröffentlicht und kann laut Make nicht wieder privat "
                "gemacht werden. Verwende --visibility preserve (Standard) oder public."
            ) from exc
        raise
