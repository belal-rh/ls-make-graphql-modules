#!/usr/bin/env python3
"""Compatibility entrypoint for deploying the LearningSuite Make Custom App.

Make's SDK API currently behaves slightly differently across zones/API versions:

- Some zones accept app fields at the top level, while the public docs show an
  ``app`` wrapper.
- Some create responses omit the numeric app version and generate an internal
  app name with a suffix.
- Base configuration may be writable through POST, PATCH, or the generic PUT
  section endpoint.

This entrypoint resolves the actual app name/version from Make after creation
and provides conservative fallbacks without changing the core deployer.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping

import deploy_learningsuite_make_app as core


def _version(value: Any, default: int) -> int:
    """Convert a Make version value to int without trusting response shape."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _list_apps(client: core.MakeClient) -> list[Mapping[str, Any]]:
    result = client.call("GET", "/sdk/apps?opensource=false")
    if not isinstance(result, Mapping):
        return []
    apps = result.get("apps", [])
    if not isinstance(apps, list):
        return []
    return [app for app in apps if isinstance(app, Mapping)]


def _matching_apps(
    client: core.MakeClient,
    apps: Iterable[Mapping[str, Any]],
    preferred_name: str | None = None,
) -> list[Mapping[str, Any]]:
    """Return likely matches, ordered from strongest to weakest."""
    requested_name = client.settings.app_name
    requested_label = client.settings.app_label
    requested_version = client.settings.version

    candidates: list[tuple[int, Mapping[str, Any]]] = []
    for app in apps:
        name = str(app.get("name", ""))
        label = str(app.get("label", ""))
        version = _version(app.get("version"), requested_version)

        score = 0
        if preferred_name and name == preferred_name:
            score += 100
        if name == requested_name:
            score += 80
        elif name.startswith(f"{requested_name}-"):
            # Some Make zones generate a unique suffix even when a name is sent.
            score += 50
        if label == requested_label:
            score += 40
        if version == requested_version:
            score += 10

        if score >= 40:
            candidates.append((score, app))

    candidates.sort(key=lambda item: item[0], reverse=True)
    return [app for _, app in candidates]


def _probe_app(
    client: core.MakeClient, app: Mapping[str, Any]
) -> tuple[str, int] | None:
    """Verify the name/version pair through Make's Get App endpoint."""
    name = str(app.get("name", ""))
    version = _version(app.get("version"), client.settings.version)
    if not name:
        return None

    try:
        result = client.call("GET", f"/sdk/apps/{name}/{version}")
    except core.DeploymentError:
        return None

    if isinstance(result, Mapping):
        response_app = result.get("app")
        resolved = response_app if isinstance(response_app, Mapping) else result
        resolved_name = str(resolved.get("name", name))
        resolved_version = _version(resolved.get("version"), version)
        return resolved_name, resolved_version

    return name, version


def _resolve_existing_app(
    client: core.MakeClient, preferred_name: str | None = None
) -> tuple[str, int] | None:
    apps = _list_apps(client)
    matches = _matching_apps(client, apps, preferred_name=preferred_name)

    for candidate in matches:
        resolved = _probe_app(client, candidate)
        if resolved is not None:
            if len(matches) > 1:
                print(
                    f"ℹ Mehrere passende Apps gefunden; verwende "
                    f"{resolved[0]} v{resolved[1]}"
                )
            return resolved
    return None


def _patch_app_metadata(
    client: core.MakeClient, app_name: str, version: int
) -> None:
    client.call(
        "PATCH",
        f"/sdk/apps/{app_name}/{version}",
        payload={
            "label": client.settings.app_label,
            "description": (
                "Private Custom App für die inoffizielle "
                "LearningSuite GraphQL API."
            ),
            "theme": "#EA5B0C",
            "language": "de",
        },
    )


def ensure_app_compatible(client: core.MakeClient) -> tuple[str, int]:
    """Find or create the app and resolve its actual Make name and version."""
    existing = _resolve_existing_app(client)
    if existing is not None:
        app_name, version = existing
        print(f"✓ App vorhanden: {app_name} v{version}")
        _patch_app_metadata(client, app_name, version)
        return app_name, version

    print(f"+ Erstelle App: {client.settings.app_name}")
    app_payload: dict[str, Any] = {
        "name": client.settings.app_name,
        "label": client.settings.app_label,
        "description": (
            "Private Custom App für die inoffizielle LearningSuite GraphQL API."
        ),
        "version": client.settings.version,
        "beta": True,
        "theme": "#EA5B0C",
        "language": "de",
        "manifestVersion": 2,
    }

    first_error: core.DeploymentError | None = None
    try:
        # Required by the Make zone observed during the first real deployment.
        created = client.call("POST", "/sdk/apps", payload=app_payload)
    except core.DeploymentError as exc:
        first_error = exc
        print("  Top-Level-Payload abgelehnt; versuche dokumentierten app-Wrapper …")
        try:
            # Format shown in Make's public SDK Apps API documentation.
            created = client.call("POST", "/sdk/apps", payload={"app": app_payload})
        except core.DeploymentError as fallback_error:
            raise core.DeploymentError(
                "App konnte mit keinem der bekannten Make-Payload-Formate "
                f"erstellt werden. Top-Level: {first_error}; "
                f"app-Wrapper: {fallback_error}"
            ) from fallback_error

    if not isinstance(created, Mapping):
        raise core.DeploymentError(
            "Make hat beim Erstellen der App keine JSON-Antwort geliefert."
        )

    response_app = created.get("app")
    created_app = response_app if isinstance(response_app, Mapping) else created
    preferred_name = str(created_app.get("name", "")) or None

    # Do not trust the create response alone. Some zones omit the version and
    # generate a suffixed internal name. Re-list and probe the actual app.
    resolved = _resolve_existing_app(client, preferred_name=preferred_name)
    if resolved is None:
        response_name = preferred_name or client.settings.app_name
        response_version = _version(
            created_app.get("version"), client.settings.version
        )
        raise core.DeploymentError(
            "Make hat die App-Erstellung bestätigt, aber die angelegte "
            f"App konnte nicht über GET /sdk/apps/{response_name}/"
            f"{response_version} verifiziert werden."
        )

    app_name, version = resolved
    print(f"✓ App aufgelöst: {app_name} v{version}")
    return app_name, version


_original_call = core.MakeClient.call


def call_compatible(
    self: core.MakeClient,
    method: str,
    path: str,
    *,
    payload: Any | None = None,
    text: str | None = None,
    content_type: str = "application/json",
    expected: Iterable[int] = (200,),
) -> Any:
    """Fallback for Base writes across Make SDK API variants."""
    try:
        return _original_call(
            self,
            method,
            path,
            payload=payload,
            text=text,
            content_type=content_type,
            expected=expected,
        )
    except core.DeploymentError as first_error:
        if method.upper() != "POST" or not path.endswith("/base"):
            raise

        fallback_errors = [f"POST: {first_error}"]
        for fallback_method in ("PATCH", "PUT"):
            print(
                f"  POST Base abgelehnt; versuche {fallback_method} "
                "für denselben App-Pfad …"
            )
            try:
                return _original_call(
                    self,
                    fallback_method,
                    path,
                    payload=payload,
                    text=text,
                    content_type=content_type,
                    expected=expected,
                )
            except core.DeploymentError as fallback_error:
                fallback_errors.append(f"{fallback_method}: {fallback_error}")

        raise core.DeploymentError(
            "Base-Konfiguration konnte mit POST, PATCH und PUT nicht "
            "geschrieben werden. " + " | ".join(fallback_errors)
        ) from first_error


core.MakeClient.call = call_compatible
core.ensure_app = ensure_app_compatible


if __name__ == "__main__":
    raise SystemExit(core.main())
