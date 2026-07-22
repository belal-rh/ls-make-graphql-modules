from __future__ import annotations

from typing import Mapping

from ..client import MakeClient
from ..errors import DeploymentError
from ..specs import connection_api, connection_parameters
from ..specs.common import CONNECTION_LABEL


def ensure_connection(client: MakeClient, app_name: str) -> str:
    result = client.call("GET", f"/sdk/apps/{app_name}/connections")
    items = result.get("appConnections", []) if isinstance(result, Mapping) else []
    current = next(
        (
            item
            for item in items
            if isinstance(item, Mapping)
            and item.get("label") == CONNECTION_LABEL
            and item.get("type") == "basic"
        ),
        None,
    )

    if current:
        name = str(current["name"])
        print(f"✓ Connection-Komponente vorhanden: {name}")
        client.call(
            "PATCH",
            f"/sdk/apps/connections/{name}",
            payload={"label": CONNECTION_LABEL},
        )
    else:
        print("+ Erstelle Connection-Komponente")
        created = client.call(
            "POST",
            f"/sdk/apps/{app_name}/connections",
            payload={"type": "basic", "label": CONNECTION_LABEL},
        )
        data = created.get("appConnection", {}) if isinstance(created, Mapping) else {}
        name = str(data.get("name", ""))
        if client.settings.dry_run:
            name = "__MAKE_CONNECTION_NAME__"
        if not name:
            raise DeploymentError("Make hat keinen Connection-Namen zurückgegeben.")

    client.call(
        "PUT",
        f"/sdk/apps/connections/{name}/parameters",
        payload=connection_parameters(),
    )
    client.call("PUT", f"/sdk/apps/connections/{name}/api", payload=connection_api())
    return name
