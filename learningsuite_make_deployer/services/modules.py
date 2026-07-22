from __future__ import annotations

from typing import Any, Mapping

from ..client import MakeClient
from ..errors import DeploymentError


def list_modules(
    client: MakeClient,
    app_name: str,
    version: int,
) -> dict[str, Mapping[str, Any]]:
    result = client.call("GET", f"/sdk/apps/{app_name}/{version}/modules")
    items = result.get("appModules", []) if isinstance(result, Mapping) else []
    return {
        str(item["name"]): item
        for item in items
        if isinstance(item, Mapping) and item.get("name")
    }


def ensure_module(
    client: MakeClient,
    app_name: str,
    version: int,
    existing: Mapping[str, Mapping[str, Any]],
    spec: Mapping[str, Any],
) -> None:
    name = str(spec["name"])
    old = existing.get(name)
    expected_type = int(spec["typeId"])

    if old and int(old.get("typeId", expected_type)) != expected_type:
        raise DeploymentError(
            f"Modul {name!r} existiert mit einem anderen Modultyp. Der Deployer "
            "löscht veröffentlichte oder bestehende Module aus Sicherheitsgründen nicht. "
            "Verwende einen neuen Modulnamen oder eine neue App-Version."
        )

    metadata = {
        "label": spec["label"],
        "description": spec["description"],
        "connection": spec["connection"],
    }
    if old:
        print(f"✓ Aktualisiere Modul: {spec['label']}")
        client.call(
            "PATCH",
            f"/sdk/apps/{app_name}/{version}/modules/{name}",
            payload=metadata,
        )
    else:
        print(f"+ Erstelle Modul: {spec['label']}")
        client.call(
            "POST",
            f"/sdk/apps/{app_name}/{version}/modules",
            payload={
                "name": name,
                "typeId": expected_type,
                **metadata,
                "moduleInitMode": "blank",
                "webhook": None,
                "crud": None,
            },
        )

    root = f"/sdk/apps/{app_name}/{version}/modules/{name}"
    client.call("PUT", f"{root}/parameters", payload=spec.get("parameters", []))
    client.call("PUT", f"{root}/api", payload=spec["api"])
    client.call("PUT", f"{root}/interface", payload=spec.get("interface", []))
    apply_module_visibility(client, root)


def apply_module_visibility(client: MakeClient, module_root: str) -> None:
    target = client.settings.module_visibility
    if target == "preserve":
        return
    client.call("POST", f"{module_root}/{target}", payload={})


def set_groups(
    client: MakeClient,
    app_name: str,
    version: int,
    groups: list[dict[str, Any]],
) -> None:
    client.call("PUT", f"/sdk/apps/{app_name}/{version}/groups", payload=groups)
