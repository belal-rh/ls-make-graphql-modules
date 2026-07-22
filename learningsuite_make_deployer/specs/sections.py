from __future__ import annotations

from typing import Any

from .common import action, parameter


def section_modules(connection: str) -> list[dict[str, Any]]:
    return [
        action(
            "addSection",
            "Sektion erstellen",
            "Erstellt eine Sektion in einem Modul.",
            connection,
            [
                parameter("topicId", "Topic Node ID", required=True),
                parameter("name", "Sektionsname", required=True),
                parameter("description", "Beschreibung"),
                parameter(
                    "lessonsDoneOneByOne",
                    "Lektionen nacheinander abschließen",
                    "boolean",
                    default=False,
                ),
            ],
            "AddSection",
            "729bbd9af3894f4950dd0823350975645c2834fe4303c92c25350f0316a7f2ac",
            {
                "topicId": "{{parameters.topicId}}",
                "data": {
                    "name": "{{parameters.name}}",
                    "description": "{{ifempty(parameters.description, '')}}",
                    "lessonsDoneOneByOne": "{{parameters.lessonsDoneOneByOne}}",
                },
            },
            "createSection",
        ),
        action(
            "editSection",
            "Sektion bearbeiten",
            "Aktualisiert eine Sektion.",
            connection,
            [
                parameter("sectionId", "Section Node ID", required=True),
                parameter("name", "Sektionsname", required=True),
                parameter("description", "Beschreibung"),
                parameter(
                    "lessonsDoneOneByOne",
                    "Lektionen nacheinander abschließen",
                    "boolean",
                    default=False,
                ),
            ],
            "EditSection",
            "b875f283e6678a486f47aec32cda3eada719c2f8cfd12614fc2af6fe06f0d6f0",
            {
                "editSection": {
                    "id": "{{parameters.sectionId}}",
                    "name": "{{parameters.name}}",
                    "description": "{{ifempty(parameters.description, '')}}",
                    "lessonsDoneOneByOne": "{{parameters.lessonsDoneOneByOne}}",
                }
            },
            "editSection",
        ),
    ]
