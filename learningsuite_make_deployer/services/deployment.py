from __future__ import annotations

from typing import Any

from ..client import MakeClient
from ..errors import DeploymentError
from ..settings import Settings
from ..specs import app_base, groups, module_definitions
from .apps import apply_app_visibility, ensure_app
from .connections import ensure_connection
from .modules import ensure_module, list_modules, set_groups


def set_base(client: MakeClient, app_name: str, version: int) -> None:
    path = f"/sdk/apps/{app_name}/{version}/base"
    payload = app_base()
    try:
        client.call("POST", path, payload=payload, content_type="application/jsonc")
    except DeploymentError as post_error:
        if post_error.status_code not in {404, 405}:
            raise
        print("  POST Base nicht unterstützt; versuche PATCH …")
        client.call("PATCH", path, payload=payload, content_type="application/jsonc")


def commit_changes(client: MakeClient, app_name: str, version: int) -> None:
    if not client.settings.commit:
        print("ℹ Kein Commit (--no-commit)")
        return
    if not client.settings.commit_all and not client.change_ids:
        print("= Keine Change-IDs erkannt; Commit wird übersprungen")
        return

    body: dict[str, Any] = {
        "message": "Deploy LearningSuite GraphQL Custom App",
        "notify": False,
    }
    if not client.settings.commit_all:
        body["changeIds"] = sorted(set(client.change_ids))

    try:
        client.call("POST", f"/sdk/apps/{app_name}/{version}/commit", payload=body)
    except DeploymentError as exc:
        if exc.status_code == 400 and (
            exc.has_text("nothing to commit") or exc.has_text("no changes")
        ):
            print("= Keine Änderungen zu committen")
            return
        raise
    print(f"✓ Commit durchgeführt ({len(client.change_ids)} erkannte Change-IDs)")


def deploy(settings: Settings) -> None:
    settings.validate()
    client = MakeClient(settings)
    app_name, version = ensure_app(client)
    connection = ensure_connection(client, app_name)
    set_base(client, app_name, version)

    existing = list_modules(client, app_name, version)
    definitions = module_definitions(connection)
    for spec in definitions:
        ensure_module(client, app_name, version, existing, spec)

    set_groups(client, app_name, version, groups())
    apply_app_visibility(client, app_name, version)
    commit_changes(client, app_name, version)

    print(f"\nFertig: {app_name} v{version} in {settings.zone}.make.com")
    print(f"Angelegte/aktualisierte Module: {len(definitions)}")
    print("Lege anschließend in einem Make-Szenario die LearningSuite-Connection an.")
