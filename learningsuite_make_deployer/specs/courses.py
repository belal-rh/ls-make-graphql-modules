from __future__ import annotations

from typing import Any

from .common import action, module_api, parameter


def course_modules(connection: str) -> list[dict[str, Any]]:
    return [
        {
            "name": "listCourses",
            "typeId": 9,
            "label": "Kurse auflisten",
            "description": "Lädt alle erstellten Kurse.",
            "connection": connection,
            "parameters": [],
            "api": module_api(
                "AuthoredCourses",
                "a70e28d2b8370d93ce039c75abe29c0ed646259d799d1522bf31e0c22b813c0b",
                {},
                {
                    "id": "{{item.id}}",
                    "sid": "{{item.sid}}",
                    "name": "{{item.name}}",
                    "isPublished": "{{item.isPublished}}",
                },
                "{{body.data.authoredCourses}}",
            ),
            "interface": [
                parameter("id", "Course Node ID"),
                parameter("sid", "Course SID"),
                parameter("name", "Kursname"),
                parameter("isPublished", "Veröffentlicht", "boolean"),
            ],
        },
        action(
            "getCourseInfo",
            "Kursdetails abrufen",
            "Lädt Summary und Rich-Text-Beschreibung eines Kurses.",
            connection,
            [parameter("courseSid", "Course SID", required=True)],
            "CourseInfoQuery",
            "a7d1b550276e5621430a8a9fe646ed7d91178232bce12b72923265d89ace0240",
            {"courseSid": "{{parameters.courseSid}}"},
            "course",
        ),
        {
            "name": "listCourseTopics",
            "typeId": 9,
            "label": "Module eines Kurses auflisten",
            "description": "Lädt alle Topics/Module eines Kurses.",
            "connection": connection,
            "parameters": [parameter("courseSid", "Course SID", required=True)],
            "api": module_api(
                "CoursePaths",
                "dcb1132ae4701875b7ce74fc38afd5ae97ea08df83c06959bff99f3ebe28227b",
                {"courseSid": "{{parameters.courseSid}}"},
                {
                    "id": "{{item.module.id}}",
                    "sid": "{{item.module.sid}}",
                    "name": "{{item.module.name}}",
                    "description": "{{item.module.description}}",
                },
                "{{body.data.course.modules}}",
            ),
            "interface": [
                parameter("id", "Topic Node ID"),
                parameter("sid", "Topic SID"),
                parameter("name", "Modulname"),
                parameter("description", "Beschreibung"),
            ],
        },
        action(
            "createCourse",
            "Kurs erstellen",
            "Erstellt einen neuen Kurs.",
            connection,
            [
                parameter("name", "Kursname", required=True),
                parameter("summary", "Kurzbeschreibung"),
                parameter("descriptionText", "Ausführliche Beschreibung"),
            ],
            "AddCourse",
            "cc30311057ac58b722e109432dd275e82c7d26b2d217c6231d5825876525a990",
            {
                "courseCreationInput": {
                    "name": "{{parameters.name}}",
                    "descriptionRichText": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"text": "{{ifempty(parameters.descriptionText, '')}}"}
                            ],
                        }
                    ],
                    "summary": "{{ifempty(parameters.summary, '')}}",
                }
            },
            "createCourse",
            [
                parameter("__typename", "Typ"),
                parameter("id", "Course Node ID"),
                parameter("sid", "Course SID"),
            ],
        ),
        action(
            "updateCourseDescription",
            "Kursbeschreibung aktualisieren",
            "Aktualisiert Summary und Rich-Text-Beschreibung.",
            connection,
            [
                parameter("courseId", "Course Node ID", required=True),
                parameter("summary", "Kurzbeschreibung"),
                parameter("descriptionText", "Beschreibung"),
            ],
            "UpdateCourse",
            "4149001c35a4454bc69fbc0231a22003d2692ca74d083567b69029fd5a4961e5",
            {
                "data": {
                    "id": "{{parameters.courseId}}",
                    "summary": "{{ifempty(parameters.summary, '')}}",
                    "descriptionRichText": [
                        {
                            "type": "paragraph",
                            "children": [
                                {"text": "{{ifempty(parameters.descriptionText, '')}}"}
                            ],
                        }
                    ],
                }
            },
            "updateCourse",
        ),
        action(
            "setCourseThumbnail",
            "Kurs-Thumbnail setzen",
            "Setzt ein generiertes Thumbnail anhand eines Presets.",
            connection,
            [
                parameter("courseId", "Course Node ID", required=True),
                parameter("thumbnailId", "Thumbnail-Preset Node ID", required=True),
                parameter("overline", "Overline", required=True),
                parameter("textBefore", "Text davor"),
                parameter("highlightedText", "Hervorgehobener Text", required=True),
            ],
            "SetCourseThumbnail",
            "9547b4268d57319d17a265dbc15e994b2efe11e6a6e08e07ad7669874b04576e",
            {
                "courseId": "{{parameters.courseId}}",
                "thumbnailId": "{{parameters.thumbnailId}}",
                "content": {
                    "text": [
                        {"text": "{{ifempty(parameters.textBefore, '')}}", "highlight": False},
                        {"text": "{{parameters.highlightedText}}", "highlight": True},
                    ],
                    "overline": "{{parameters.overline}}",
                },
            },
            "setCourseThumbnail",
        ),
    ]
