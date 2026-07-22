from __future__ import annotations

from typing import Any

from .common import module_api, parameter


def universal_modules(connection: str) -> list[dict[str, Any]]:
    return [
        {
            "name": "executePersistedGraphql",
            "typeId": 12,
            "label": "Persisted GraphQL Query ausführen",
            "description": "Universelles Fallback für weitere LearningSuite-Persisted-Queries.",
            "connection": connection,
            "parameters": [
                parameter("operationName", "Operation Name", required=True),
                parameter("sha256Hash", "SHA-256 Hash", required=True),
                parameter(
                    "variables",
                    "Variables",
                    "json",
                    required=True,
                    help_text="Gültiges JSON-Objekt.",
                ),
            ],
            "api": module_api(
                "{{parameters.operationName}}",
                "{{parameters.sha256Hash}}",
                "{{parameters.variables}}",
                "{{body}}",
            ),
            "interface": [],
        }
    ]
