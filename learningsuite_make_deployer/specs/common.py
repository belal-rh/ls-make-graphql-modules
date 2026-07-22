from __future__ import annotations

from typing import Any

AUTH_URL = "https://auth.learningsuite.io/auth/token"
CONNECTION_LABEL = "LearningSuite Login"


def parameter(
    name: str,
    label: str,
    kind: str = "text",
    required: bool = False,
    advanced: bool = False,
    help_text: str | None = None,
    default: Any | None = None,
) -> dict[str, Any]:
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
        "log": {"sanitize": ["request.body.password", "response.body.access_token"]},
    }


def gql_request(
    operation: str,
    sha256_hash: str,
    variables: Any,
    output: Any,
    iterate: str | None = None,
) -> dict[str, Any]:
    response: dict[str, Any] = {
        # GraphQL omits `errors` on success. Make IML supports logical negation,
        # while an `empty()` helper is not available in this runtime.
        "valid": {"condition": "{{!body.errors}}"},
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


def module_api(
    operation: str,
    sha256_hash: str,
    variables: Any,
    output: Any,
    iterate: str | None = None,
) -> list[dict[str, Any]]:
    return [auth_request(), gql_request(operation, sha256_hash, variables, output, iterate)]


def action(
    name: str,
    label: str,
    description: str,
    connection: str,
    parameters: list[dict[str, Any]],
    operation: str,
    sha256_hash: str,
    variables: Any,
    response_path: str,
    interface: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "name": name,
        "typeId": 4,
        "label": label,
        "description": description,
        "connection": connection,
        "parameters": parameters,
        "api": module_api(
            operation,
            sha256_hash,
            variables,
            f"{{{{body.data.{response_path}}}}}",
        ),
        "interface": interface or [],
    }


def connection_parameters() -> list[dict[str, Any]]:
    return [
        {**parameter("tenantId", "LearningSuite Tenant-ID", required=True), "editable": True},
        {**parameter("email", "LearningSuite E-Mail", "email", required=True), "editable": True},
        {**parameter("password", "LearningSuite Passwort", "password", required=True), "editable": True},
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
        "log": {
            "sanitize": [
                "request.headers.authorization",
                "request.body.password",
                "response.body.access_token",
            ]
        },
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
