#!/usr/bin/env python3
"""Deploy a private Make Custom App for LearningSuite persisted GraphQL queries."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

import requests

AUTH_URL = "https://auth.learningsuite.io/auth/token"
CONNECTION_LABEL = "LearningSuite Login"
DEFAULT_APP_NAME = "learningsuite-graphql"
DEFAULT_APP_LABEL = "LearningSuite GraphQL"
DEFAULT_VERSION = 1
DEFAULT_ZONE = "eu1"
ALLOWED_ZONES = {"eu1", "eu2", "us1", "us2"}


class DeploymentError(RuntimeError):
    pass


@dataclass(frozen=True)
class Settings:
    api_token: str
    zone: str
    app_name: str
    app_label: str
    version: int
    dry_run: bool
    commit: bool
    commit_all: bool

    @property
    def api_base(self) -> str:
        return f"https://{self.zone}.make.com/api/v2"


class MakeClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {settings.api_token}",
            "Accept": "application/json",
            "User-Agent": "RH-LearningSuite-Make-Deployer/1.0",
        })
        self.change_ids: list[int] = []

    def call(
        self,
        method: str,
        path: str,
        *,
        payload: Any | None = None,
        text: str | None = None,
        content_type: str = "application/json",
        expected: Iterable[int] = (200,),
    ) -> Any:
        url = f"{self.settings.api_base}{path}"
        if self.settings.dry_run:
            print(f"[DRY-RUN] {method.upper()} {url}")
            if payload is not None:
                print(json.dumps(payload, indent=2, ensure_ascii=False))
            elif text is not None:
                print(text)
            return {}

        for attempt in range(5):
            response = self.session.request(
                method.upper(),
                url,
                json=payload if text is None else None,
                data=text.encode("utf-8") if text is not None else None,
                headers={"Content-Type": content_type},
                timeout=60,
            )
            if response.status_code in set(expected):
                result = self._decode(response)
                self._collect_change(result)
                return result
            if response.status_code in {429, 500, 502, 503, 504} and attempt < 4:
                wait = float(response.headers.get("Retry-After", min(2 ** attempt, 15)))
                print(f"  Make API {response.status_code}; Wiederholung in {wait:.1f}s")
                time.sleep(wait)
                continue
            raise DeploymentError(
                f"{method.upper()} {path} fehlgeschlagen ({response.status_code}): "
                f"{response.text[:4000]}"
            )
        raise DeploymentError(f"{method.upper()} {path} endgültig fehlgeschlagen")

    @staticmethod
    def _decode(response: requests.Response) -> Any:
        if not response.content:
            return None
        if "json" in response.headers.get("Content-Type", ""):
            return response.json()
        value = response.text.strip()
        if value == "true":
            return True
        if value == "false":
            return False
        return value

    def _collect_change(self, result: Any) -> None:
        if isinstance(result, Mapping):
            change = result.get("change")
            if isinstance(change, Mapping) and isinstance(change.get("id"), int):
                change_id = int(change["id"])
                if change_id not in self.change_ids:
                    self.change_ids.append(change_id)


def p(name: str, label: str, kind: str = "text", required: bool = False,
      advanced: bool = False, help_text: str | None = None,
      default: Any | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "name": name,
        "type": kind,
        "label": label,
        "required": required,
    }
    if advanced:
        value["advanced"] = True
    if help_text:
        value["help"] = help_text
    if default is not None:
        value["default"] = default
    return value


def auth_request() -> dict[str, Any]:
    return {
        "url": AUTH_URL,
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "x-tenant-id": "{{connection.tenantId}}",
        },
        "type": "json",
        "body": {
            "email": "{{connection.email}}",
            "password": "{{connection.password}}",
        },
        "response": {
            "valid": {"condition": "{{body.access_token}}"},
            "temp": {"accessToken": "{{body.access_token}}"},
            "error": {
                "message": "[{{statusCode}}] LearningSuite-Anmeldung fehlgeschlagen: {{body}}"
            },
        },
        "log": {
            "sanitize": ["request.body.password", "response.body.access_token"]
        },
    }


def gql_request(operation: str, sha256_hash: str, variables: Any,
                output: Any, iterate: str | None = None) -> dict[str, Any]:
    response: dict[str, Any] = {
        "valid": {"condition": "{{empty(body.errors)}}"},
        "error": {
            "200": {"message": "LearningSuite GraphQL-Fehler: {{body.errors}}"},
            "message": "[{{statusCode}}] LearningSuite-Anfrage fehlgeschlagen: {{body}}",
        },
        "output": output,
    }
    if iterate:
        response["iterate"] = iterate
    return {
        "url": "/graphql",
        "method": "POST",
        "headers": {"Authorization": "Bearer {{temp.accessToken}}"},
        "type": "json",
        "body": {
            "operationName": operation,
            "variables": variables,
            "extensions": {
                "persistedQuery": {"version": 1, "sha256Hash": sha256_hash}
            },
        },
        "response": response,
        "log": {"sanitize": ["request.headers.authorization"]},
    }


def module_api(operation: str, sha256_hash: str, variables: Any,
               output: Any, iterate: str | None = None) -> list[dict[str, Any]]:
    return [auth_request(), gql_request(operation, sha256_hash, variables, output, iterate)]


def action(name: str, label: str, description: str, connection: str,
           parameters: list[dict[str, Any]], operation: str, sha256_hash: str,
           variables: Any, response_path: str,
           interface: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "name": name,
        "typeId": 4,
        "label": label,
        "description": description,
        "connection": connection,
        "parameters": parameters,
        "api": module_api(operation, sha256_hash, variables,
                          f"{{{{body.data.{response_path}}}}}"),
        "interface": interface or [],
    }


def module_definitions(connection: str) -> list[dict[str, Any]]:
    modules: list[dict[str, Any]] = [
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
                p("id", "Course Node ID"), p("sid", "Course SID"),
                p("name", "Kursname"), p("isPublished", "Veröffentlicht", "boolean"),
            ],
        },
        action(
            "getCourseInfo", "Kursdetails abrufen",
            "Lädt Summary und Rich-Text-Beschreibung eines Kurses.", connection,
            [p("courseSid", "Course SID", required=True)],
            "CourseInfoQuery",
            "a7d1b550276e5621430a8a9fe646ed7d91178232bce12b72923265d89ace0240",
            {"courseSid": "{{parameters.courseSid}}"}, "course",
        ),
        {
            "name": "listCourseTopics",
            "typeId": 9,
            "label": "Module eines Kurses auflisten",
            "description": "Lädt alle Topics/Module eines Kurses.",
            "connection": connection,
            "parameters": [p("courseSid", "Course SID", required=True)],
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
                p("id", "Topic Node ID"), p("sid", "Topic SID"),
                p("name", "Modulname"), p("description", "Beschreibung"),
            ],
        },
        action(
            "getTopicTree", "Modulstruktur abrufen",
            "Lädt Sektionen und Lektionen eines Moduls.", connection,
            [p("topicId", "Topic Node ID", required=True),
             p("courseSid", "Course SID", required=True)],
            "TopicQuery",
            "b44496383040234ea01b5031834480ab3aa50435f4aa2f5ef8fa6f63ee7d285c",
            {"topicId": "{{parameters.topicId}}", "courseSid": "{{parameters.courseSid}}"},
            "topic",
        ),
        action(
            "createCourse", "Kurs erstellen", "Erstellt einen neuen Kurs.", connection,
            [p("name", "Kursname", required=True), p("summary", "Kurzbeschreibung"),
             p("descriptionText", "Ausführliche Beschreibung")],
            "AddCourse",
            "cc30311057ac58b722e109432dd275e82c7d26b2d217c6231d5825876525a990",
            {"courseCreationInput": {
                "name": "{{parameters.name}}",
                "descriptionRichText": [{"type": "paragraph", "children": [
                    {"text": "{{ifempty(parameters.descriptionText, '')}}"}
                ]}],
                "summary": "{{ifempty(parameters.summary, '')}}",
            }},
            "createCourse",
            [p("__typename", "Typ"), p("id", "Course Node ID"), p("sid", "Course SID")],
        ),
        action(
            "updateCourseDescription", "Kursbeschreibung aktualisieren",
            "Aktualisiert Summary und Rich-Text-Beschreibung.", connection,
            [p("courseId", "Course Node ID", required=True),
             p("summary", "Kurzbeschreibung"), p("descriptionText", "Beschreibung")],
            "UpdateCourse",
            "4149001c35a4454bc69fbc0231a22003d2692ca74d083567b69029fd5a4961e5",
            {"data": {
                "id": "{{parameters.courseId}}",
                "summary": "{{ifempty(parameters.summary, '')}}",
                "descriptionRichText": [{"type": "paragraph", "children": [
                    {"text": "{{ifempty(parameters.descriptionText, '')}}"}
                ]}],
            }},
            "updateCourse",
        ),
        action(
            "createStandaloneTopic", "Modul in Bibliothek erstellen",
            "Erstellt ein eigenständiges Modul inklusive erster Sektion.", connection,
            [p("name", "Modulname", required=True), p("description", "Beschreibung"),
             p("folderId", "Folder Node ID", advanced=True,
               help_text="Leer lassen, damit null gesendet wird."),
             p("sectionName", "Name der ersten Sektion", required=True)],
            "CreateTopic",
            "cc092ff870aa21654e2a2cb7c790c0d9e8fdc9ac64ab1aaaedfa0cc19ab33cdf",
            {
                "name": "{{parameters.name}}",
                "description": "{{ifempty(parameters.description, '')}}",
                "folderId": "{{ifempty(parameters.folderId, null)}}",
                "sectionName": "{{parameters.sectionName}}",
            },
            "createTopic",
            [p("__typename", "Typ"), p("id", "Topic Node ID"), p("name", "Modulname")],
        ),
        action(
            "addTopicToCourse", "Modul zu Kurs hinzufügen",
            "Erstellt ein Modul direkt in einem Kurs.", connection,
            [p("courseId", "Course Node ID", required=True),
             p("name", "Modulname", required=True), p("description", "Beschreibung"),
             p("sectionName", "Name der ersten Sektion", required=True)],
            "AddTopicToCourse",
            "4f527eaf6c524c2319bc1607a67ab52667028bd7f00d231e77dbd3ea4554b573",
            {
                "courseId": "{{parameters.courseId}}", "name": "{{parameters.name}}",
                "description": "{{ifempty(parameters.description, '')}}",
                "sectionName": "{{parameters.sectionName}}",
            },
            "addTopicToCourse",
            [p("__typename", "Typ"), p("id", "Topic Node ID"), p("sid", "Topic SID")],
        ),
        action(
            "editTopic", "Modulbeschreibung aktualisieren",
            "Aktualisiert die Beschreibung eines Moduls.", connection,
            [p("topicId", "Topic Node ID", required=True),
             p("description", "Neue Beschreibung", required=True)],
            "EditTopic",
            "5a49c91efbc2c8581ba26dda9f4768acbf47f0e83bc6d7a58c465dd3403c4dfd",
            {"editTopic": {"id": "{{parameters.topicId}}",
                            "description": "{{parameters.description}}"}},
            "editTopic",
        ),
        action(
            "addSection", "Sektion erstellen", "Erstellt eine Sektion in einem Modul.", connection,
            [p("topicId", "Topic Node ID", required=True), p("name", "Sektionsname", required=True),
             p("description", "Beschreibung"),
             p("lessonsDoneOneByOne", "Lektionen nacheinander abschließen", "boolean", default=False)],
            "AddSection",
            "729bbd9af3894f4950dd0823350975645c2834fe4303c92c25350f0316a7f2ac",
            {"topicId": "{{parameters.topicId}}", "data": {
                "name": "{{parameters.name}}",
                "description": "{{ifempty(parameters.description, '')}}",
                "lessonsDoneOneByOne": "{{parameters.lessonsDoneOneByOne}}",
            }},
            "createSection",
        ),
        action(
            "editSection", "Sektion bearbeiten", "Aktualisiert eine Sektion.", connection,
            [p("sectionId", "Section Node ID", required=True),
             p("name", "Sektionsname", required=True), p("description", "Beschreibung"),
             p("lessonsDoneOneByOne", "Lektionen nacheinander abschließen", "boolean", default=False)],
            "EditSection",
            "b875f283e6678a486f47aec32cda3eada719c2f8cfd12614fc2af6fe06f0d6f0",
            {"editSection": {
                "id": "{{parameters.sectionId}}", "name": "{{parameters.name}}",
                "description": "{{ifempty(parameters.description, '')}}",
                "lessonsDoneOneByOne": "{{parameters.lessonsDoneOneByOne}}",
            }},
            "editSection",
        ),
        action(
            "addLesson", "Lektion erstellen", "Erstellt eine Lektion in einer Sektion.", connection,
            [p("sectionId", "Section Node ID", required=True), p("name", "Lektionsname", required=True)],
            "AddLesson",
            "644f5a8990fdb54d69e769c2921ce742119075e7d67e80bb5d141738296aa7e7",
            {"sectionId": "{{parameters.sectionId}}", "name": "{{parameters.name}}"},
            "createLesson",
            [p("__typename", "Typ"), p("id", "Lesson Node ID"), p("name", "Lektionsname")],
        ),
        action(
            "setCourseThumbnail", "Kurs-Thumbnail setzen",
            "Setzt ein generiertes Thumbnail anhand eines Presets.", connection,
            [p("courseId", "Course Node ID", required=True),
             p("thumbnailId", "Thumbnail-Preset Node ID", required=True),
             p("overline", "Overline", required=True), p("textBefore", "Text davor"),
             p("highlightedText", "Hervorgehobener Text", required=True)],
            "SetCourseThumbnail",
            "9547b4268d57319d17a265dbc15e994b2efe11e6a6e08e07ad7669874b04576e",
            {"courseId": "{{parameters.courseId}}", "thumbnailId": "{{parameters.thumbnailId}}",
             "content": {"text": [
                 {"text": "{{ifempty(parameters.textBefore, '')}}", "highlight": False},
                 {"text": "{{parameters.highlightedText}}", "highlight": True},
             ], "overline": "{{parameters.overline}}"}},
            "setCourseThumbnail",
        ),
        action(
            "setModuleThumbnail", "Modul-Thumbnail setzen",
            "Setzt ein generiertes Thumbnail für ein Modul.", connection,
            [p("moduleId", "Topic Node ID", required=True),
             p("thumbnailId", "Thumbnail-Preset Node ID", required=True),
             p("overline", "Overline", required=True), p("textBefore", "Text davor"),
             p("highlightedText", "Hervorgehobener Text", required=True)],
            "SetModuleThumbnail",
            "fa2764b86629193cd84f19da0a4777f22011e2db9bdeb3e0263643fd738575a1",
            {"moduleId": "{{parameters.moduleId}}", "thumbnailId": "{{parameters.thumbnailId}}",
             "content": {"text": [
                 {"text": "{{ifempty(parameters.textBefore, '')}}", "highlight": False},
                 {"text": "{{parameters.highlightedText}}", "highlight": True},
             ], "overline": "{{parameters.overline}}"}},
            "setModuleThumbnail",
        ),
        {
            "name": "executePersistedGraphql",
            "typeId": 12,
            "label": "Persisted GraphQL Query ausführen",
            "description": "Universelles Fallback für weitere LearningSuite-Persisted-Queries.",
            "connection": connection,
            "parameters": [
                p("operationName", "Operation Name", required=True),
                p("sha256Hash", "SHA-256 Hash", required=True),
                p("variables", "Variables", "json", required=True,
                  help_text="Gültiges JSON-Objekt."),
            ],
            "api": module_api(
                "{{parameters.operationName}}", "{{parameters.sha256Hash}}",
                "{{parameters.variables}}", "{{body}}"
            ),
            "interface": [],
        },
    ]
    return modules


def connection_parameters() -> list[dict[str, Any]]:
    return [
        {**p("tenantId", "LearningSuite Tenant-ID", required=True), "editable": True},
        {**p("email", "LearningSuite E-Mail", "email", required=True), "editable": True},
        {**p("password", "LearningSuite Passwort", "password", required=True), "editable": True},
    ]


def connection_api() -> dict[str, Any]:
    return {
        "url": AUTH_URL,
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "x-tenant-id": "{{parameters.tenantId}}",
        },
        "type": "json",
        "body": {"email": "{{parameters.email}}", "password": "{{parameters.password}}"},
        "response": {
            "valid": {"condition": "{{body.access_token}}"},
            "data": {
                "tenantId": "{{parameters.tenantId}}",
                "email": "{{parameters.email}}",
                "password": "{{parameters.password}}",
            },
            "metadata": {"type": "email", "value": "{{parameters.email}}"},
            "error": {
                "message": "[{{statusCode}}] LearningSuite-Anmeldung fehlgeschlagen: {{body}}"
            },
        },
        "log": {"sanitize": ["request.body.password", "response.body.access_token"]},
    }


def app_base() -> dict[str, Any]:
    return {
        "baseUrl": "https://api-p.learningsuite.io/{{connection.tenantId}}",
        "headers": {"Content-Type": "application/json", "Accept": "application/json"},
        "log": {"sanitize": [
            "request.headers.authorization", "request.body.password", "response.body.access_token"
        ]},
    }


def groups() -> list[dict[str, Any]]:
    return [
        {"label": "Abfragen", "modules": ["listCourses", "getCourseInfo", "listCourseTopics", "getTopicTree"]},
        {"label": "Kurse", "modules": ["createCourse", "updateCourseDescription"]},
        {"label": "Module", "modules": ["createStandaloneTopic", "addTopicToCourse", "editTopic"]},
        {"label": "Sektionen & Lektionen", "modules": ["addSection", "editSection", "addLesson"]},
        {"label": "Thumbnails", "modules": ["setCourseThumbnail", "setModuleThumbnail"]},
        {"label": "Erweitert", "modules": ["executePersistedGraphql"]},
    ]


def ensure_app(client: MakeClient) -> tuple[str, int]:
    result = client.call("GET", "/sdk/apps?opensource=false")
    apps = result.get("apps", []) if isinstance(result, Mapping) else []
    for app in apps:
        if app.get("name") == client.settings.app_name and int(app.get("version", 1)) == client.settings.version:
            print(f"✓ App vorhanden: {client.settings.app_name} v{client.settings.version}")
            client.call("PATCH", f"/sdk/apps/{client.settings.app_name}/{client.settings.version}", payload={
                "label": client.settings.app_label,
                "description": "Private Custom App für die inoffizielle LearningSuite GraphQL API.",
                "theme": "#EA5B0C", "language": "de",
            })
            return client.settings.app_name, client.settings.version

    print(f"+ Erstelle App: {client.settings.app_name}")
    created = client.call("POST", "/sdk/apps", payload={"app": {
        "name": client.settings.app_name,
        "label": client.settings.app_label,
        "description": "Private Custom App für die inoffizielle LearningSuite GraphQL API.",
        "version": client.settings.version,
        "beta": True,
        "theme": "#EA5B0C",
        "language": "de",
        "manifestVersion": 2,
    }})
    app = created.get("app", {}) if isinstance(created, Mapping) else {}
    return str(app.get("name", client.settings.app_name)), int(app.get("version", client.settings.version))


def ensure_connection(client: MakeClient, app_name: str) -> str:
    result = client.call("GET", f"/sdk/apps/{app_name}/connections")
    items = result.get("appConnections", []) if isinstance(result, Mapping) else []
    current = next((x for x in items if x.get("label") == CONNECTION_LABEL and x.get("type") == "basic"), None)
    if current:
        name = str(current["name"])
        print(f"✓ Connection-Komponente vorhanden: {name}")
        client.call("PATCH", f"/sdk/apps/connections/{name}", payload={"label": CONNECTION_LABEL})
    else:
        print("+ Erstelle Connection-Komponente")
        created = client.call("POST", f"/sdk/apps/{app_name}/connections", payload={
            "type": "basic", "label": CONNECTION_LABEL
        })
        data = created.get("appConnection", {}) if isinstance(created, Mapping) else {}
        name = str(data.get("name", ""))
        if client.settings.dry_run:
            name = "__MAKE_CONNECTION_NAME__"
        if not name:
            raise DeploymentError("Make hat keinen Connection-Namen zurückgegeben")

    client.call("PUT", f"/sdk/apps/connections/{name}/parameters", payload=connection_parameters())
    client.call("PUT", f"/sdk/apps/connections/{name}/api", payload=connection_api())
    return name


def ensure_module(client: MakeClient, app_name: str, version: int,
                  existing: dict[str, Mapping[str, Any]], spec: Mapping[str, Any]) -> None:
    name = str(spec["name"])
    old = existing.get(name)
    if old and int(old.get("typeId", spec["typeId"])) != int(spec["typeId"]):
        print(f"~ Modultyp geändert; erstelle neu: {name}")
        client.call("DELETE", f"/sdk/apps/{app_name}/{version}/modules/{name}")
        old = None

    if old:
        print(f"✓ Aktualisiere Modul: {spec['label']}")
        client.call("PATCH", f"/sdk/apps/{app_name}/{version}/modules/{name}", payload={
            "label": spec["label"], "description": spec["description"],
            "connection": spec["connection"],
        })
    else:
        print(f"+ Erstelle Modul: {spec['label']}")
        client.call("POST", f"/sdk/apps/{app_name}/{version}/modules", payload={
            "name": name, "typeId": spec["typeId"], "label": spec["label"],
            "description": spec["description"], "moduleInitMode": "blank",
            "connection": spec["connection"], "webhook": None, "crud": None,
        })

    root = f"/sdk/apps/{app_name}/{version}/modules/{name}"
    client.call("PUT", f"{root}/parameters", payload=spec.get("parameters", []))
    client.call("PUT", f"{root}/api", payload=spec["api"])
    client.call("PUT", f"{root}/interface", payload=spec.get("interface", []))
    client.call("POST", f"{root}/private", payload={})


def deploy(settings: Settings) -> None:
    client = MakeClient(settings)
    app_name, version = ensure_app(client)
    connection = ensure_connection(client, app_name)
    client.call("POST", f"/sdk/apps/{app_name}/{version}/base",
                payload=app_base(), content_type="application/jsonc")

    listed = client.call("GET", f"/sdk/apps/{app_name}/{version}/modules")
    old_modules = listed.get("appModules", []) if isinstance(listed, Mapping) else []
    existing = {str(x["name"]): x for x in old_modules if isinstance(x, Mapping) and x.get("name")}

    definitions = module_definitions(connection)
    for spec in definitions:
        ensure_module(client, app_name, version, existing, spec)

    client.call("PUT", f"/sdk/apps/{app_name}/{version}/groups", payload=groups())
    client.call("POST", f"/sdk/apps/{app_name}/{version}/private", payload={})

    if settings.commit:
        body: dict[str, Any] = {
            "message": "Deploy LearningSuite GraphQL Custom App",
            "notify": False,
        }
        if not settings.commit_all and client.change_ids:
            body["changeIds"] = sorted(set(client.change_ids))
        client.call("POST", f"/sdk/apps/{app_name}/{version}/commit", payload=body)
        print(f"✓ Commit durchgeführt ({len(client.change_ids)} erkannte Change-IDs)")
    else:
        print("ℹ Kein Commit (--no-commit)")

    print(f"\nFertig: {app_name} v{version} in {settings.zone}.make.com")
    print(f"Angelegte/aktualisierte Module: {len(definitions)}")
    print("Lege anschließend in einem Make-Szenario die LearningSuite-Connection an.")


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LearningSuite Make Custom App deployen")
    parser.add_argument("--zone", default=os.getenv("MAKE_ZONE", DEFAULT_ZONE))
    parser.add_argument("--app-name", default=os.getenv("MAKE_APP_NAME", DEFAULT_APP_NAME))
    parser.add_argument("--app-label", default=os.getenv("MAKE_APP_LABEL", DEFAULT_APP_LABEL))
    parser.add_argument("--version", type=int, default=int(os.getenv("MAKE_APP_VERSION", str(DEFAULT_VERSION))))
    parser.add_argument("--api-token", default=os.getenv("MAKE_API_TOKEN", ""))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-commit", action="store_true")
    parser.add_argument("--commit-all", action="store_true")
    return parser.parse_args()


def main() -> int:
    try:
        args = arguments()
        if args.zone not in ALLOWED_ZONES:
            raise DeploymentError(f"Ungültige Zone: {args.zone}")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.app_name):
            raise DeploymentError("App-Name: nur Kleinbuchstaben, Zahlen und Bindestriche")
        if not args.api_token and not args.dry_run:
            raise DeploymentError("MAKE_API_TOKEN fehlt (Scopes: sdk-apps:read, sdk-apps:write)")
        deploy(Settings(
            api_token=args.api_token or "DRY_RUN",
            zone=args.zone,
            app_name=args.app_name,
            app_label=args.app_label,
            version=args.version,
            dry_run=args.dry_run,
            commit=not args.no_commit,
            commit_all=args.commit_all,
        ))
        return 0
    except (DeploymentError, requests.RequestException) as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
