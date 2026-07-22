from __future__ import annotations

from typing import Any

from .common import action, parameter


def lesson_modules(connection: str) -> list[dict[str, Any]]:
    return [
        action(
            "addLesson",
            "Lektion erstellen",
            "Erstellt eine Lektion in einer Sektion.",
            connection,
            [
                parameter("sectionId", "Section Node ID", required=True),
                parameter("name", "Lektionsname", required=True),
            ],
            "AddLesson",
            "644f5a8990fdb54d69e769c2921ce742119075e7d67e80bb5d141738296aa7e7",
            {
                "sectionId": "{{parameters.sectionId}}",
                "name": "{{parameters.name}}",
            },
            "createLesson",
            [
                parameter("__typename", "Typ"),
                parameter("id", "Lesson Node ID"),
                parameter("name", "Lektionsname"),
            ],
        )
    ]
