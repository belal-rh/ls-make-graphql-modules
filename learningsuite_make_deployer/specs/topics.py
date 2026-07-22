from __future__ import annotations

from typing import Any

from .common import action, parameter


def topic_modules(connection: str) -> list[dict[str, Any]]:
    return [
        action(
            "getTopicTree",
            "Modulstruktur abrufen",
            "Lädt Sektionen und Lektionen eines Moduls.",
            connection,
            [
                parameter("topicId", "Topic Node ID", required=True),
                parameter("courseSid", "Course SID", required=True),
            ],
            "TopicQuery",
            "b44496383040234ea01b5031834480ab3aa50435f4aa2f5ef8fa6f63ee7d285c",
            {
                "topicId": "{{parameters.topicId}}",
                "courseSid": "{{parameters.courseSid}}",
            },
            "topic",
        ),
        action(
            "createStandaloneTopic",
            "Modul in Bibliothek erstellen",
            "Erstellt ein eigenständiges Modul inklusive erster Sektion.",
            connection,
            [
                parameter("name", "Modulname", required=True),
                parameter("description", "Beschreibung"),
                parameter(
                    "folderId",
                    "Folder Node ID",
                    advanced=True,
                    help_text="Leer lassen, damit null gesendet wird.",
                ),
                parameter("sectionName", "Name der ersten Sektion", required=True),
            ],
            "CreateTopic",
            "cc092ff870aa21654e2a2cb7c790c0d9e8fdc9ac64ab1aaaedfa0cc19ab33cdf",
            {
                "name": "{{parameters.name}}",
                "description": "{{ifempty(parameters.description, '')}}",
                "folderId": "{{ifempty(parameters.folderId, null)}}",
                "sectionName": "{{parameters.sectionName}}",
            },
            "createTopic",
            [
                parameter("__typename", "Typ"),
                parameter("id", "Topic Node ID"),
                parameter("name", "Modulname"),
            ],
        ),
        action(
            "addTopicToCourse",
            "Modul zu Kurs hinzufügen",
            "Erstellt ein Modul direkt in einem Kurs.",
            connection,
            [
                parameter("courseId", "Course Node ID", required=True),
                parameter("name", "Modulname", required=True),
                parameter("description", "Beschreibung"),
                parameter("sectionName", "Name der ersten Sektion", required=True),
            ],
            "AddTopicToCourse",
            "4f527eaf6c524c2319bc1607a67ab52667028bd7f00d231e77dbd3ea4554b573",
            {
                "courseId": "{{parameters.courseId}}",
                "name": "{{parameters.name}}",
                "description": "{{ifempty(parameters.description, '')}}",
                "sectionName": "{{parameters.sectionName}}",
            },
            "addTopicToCourse",
            [
                parameter("__typename", "Typ"),
                parameter("id", "Topic Node ID"),
                parameter("sid", "Topic SID"),
            ],
        ),
        action(
            "editTopic",
            "Modulbeschreibung aktualisieren",
            "Aktualisiert die Beschreibung eines Moduls.",
            connection,
            [
                parameter("topicId", "Topic Node ID", required=True),
                parameter("description", "Neue Beschreibung", required=True),
            ],
            "EditTopic",
            "5a49c91efbc2c8581ba26dda9f4768acbf47f0e83bc6d7a58c465dd3403c4dfd",
            {
                "editTopic": {
                    "id": "{{parameters.topicId}}",
                    "description": "{{parameters.description}}",
                }
            },
            "editTopic",
        ),
        action(
            "setModuleThumbnail",
            "Modul-Thumbnail setzen",
            "Setzt ein generiertes Thumbnail für ein Modul.",
            connection,
            [
                parameter("moduleId", "Topic Node ID", required=True),
                parameter("thumbnailId", "Thumbnail-Preset Node ID", required=True),
                parameter("overline", "Overline", required=True),
                parameter("textBefore", "Text davor"),
                parameter("highlightedText", "Hervorgehobener Text", required=True),
            ],
            "SetModuleThumbnail",
            "fa2764b86629193cd84f19da0a4777f22011e2db9bdeb3e0263643fd738575a1",
            {
                "moduleId": "{{parameters.moduleId}}",
                "thumbnailId": "{{parameters.thumbnailId}}",
                "content": {
                    "text": [
                        {"text": "{{ifempty(parameters.textBefore, '')}}", "highlight": False},
                        {"text": "{{parameters.highlightedText}}", "highlight": True},
                    ],
                    "overline": "{{parameters.overline}}",
                },
            },
            "setModuleThumbnail",
        ),
    ]
