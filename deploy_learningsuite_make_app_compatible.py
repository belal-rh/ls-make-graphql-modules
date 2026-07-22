#!/usr/bin/env python3
"""Compatibility entrypoint for deploying the LearningSuite Make Custom App.

Some Make zones currently validate POST /sdk/apps fields at the top level, while
Make's public API documentation shows the same fields wrapped in an ``app``
object. This entrypoint supports both formats without changing the core deployer.
"""

from __future__ import annotations

from typing import Any, Mapping

import deploy_learningsuite_make_app as core


def ensure_app_compatible(client: core.MakeClient) -> tuple[str, int]:
    """Find or create the app and support both known request-body formats."""
    result = client.call("GET", "/sdk/apps?opensource=false")
    apps = result.get("apps", []) if isinstance(result, Mapping) else []

    for app in apps:
        if (
            app.get("name") == client.settings.app_name
            and int(app.get("version", 1)) == client.settings.version
        ):
            print(f"✓ App vorhanden: {client.settings.app_name} v{client.settings.version}")
            client.call(
                "PATCH",
                f"/sdk/apps/{client.settings.app_name}/{client.settings.version}",
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
            return client.settings.app_name, client.settings.version

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
        # Required by some Make zones / API versions.
        created = client.call("POST", "/sdk/apps", payload=app_payload)
    except core.DeploymentError as exc:
        first_error = exc
        print("  Top-Level-Payload abgelehnt; versuche dokumentierten app-Wrapper …")
        try:
            # Format currently shown in Make's public API documentation.
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
    app = response_app if isinstance(response_app, Mapping) else created
    return (
        str(app.get("name", client.settings.app_name)),
        int(app.get("version", client.settings.version)),
    )


core.ensure_app = ensure_app_compatible


if __name__ == "__main__":
    raise SystemExit(core.main())
