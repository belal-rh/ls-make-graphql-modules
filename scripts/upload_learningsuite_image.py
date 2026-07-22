#!/usr/bin/env python3
"""Upload images to LearningSuite via GraphQL UploadSpec and signed GCP URL."""

from __future__ import annotations

import argparse
import mimetypes
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

import requests

AUTH_URL = "https://auth.learningsuite.io/auth/token"
REQUEST_TIMEOUT = 60


class UploadError(RuntimeError):
    """Raised when authentication, GraphQL, or binary upload fails."""


@dataclass(frozen=True)
class UploadOperation:
    operation_name: str
    sha256_hash: str
    variable_name: str
    expected_response_path: str


OPERATIONS: dict[str, UploadOperation] = {
    "course-image": UploadOperation(
        operation_name="SetCourseImage",
        sha256_hash="f2cf01baef20d81055fba0c2a6164b9d74973b42fd0eb26f7161fa4bff3e36de",
        variable_name="courseId",
        expected_response_path="setCourseImage",
    ),
    "course-thumbnail-bg": UploadOperation(
        operation_name="SetCourseThumbnailBG",
        sha256_hash="8696c20b2d6f76cf22e9b1cdc5633b662a5e6fdffaccf405c93846474da076e2",
        variable_name="courseId",
        expected_response_path="setCourseThumbnailBGImage",
    ),
    "topic-image": UploadOperation(
        operation_name="TopicEditSetImage",
        sha256_hash="06538877b15a180f42502d24f7ced1a2c0b0fcd86d887683d13c2292b1852451",
        variable_name="topicId",
        expected_response_path="setTopicImage",
    ),
    "module-thumbnail-bg": UploadOperation(
        operation_name="SetModuleThumbnailBG",
        sha256_hash="9ece459af9b322066a99dbc1f392bc8d89763b98788304fefce6455e4d0baba6",
        variable_name="moduleId",
        expected_response_path="setModuleThumbnailBGImage",
    ),
    "lesson-image": UploadOperation(
        operation_name="SetLessonImage",
        sha256_hash="6498cfd61f61564acf8dad163e9a9fb31b7e144e3040ef6959d9b5f2ed968a6e",
        variable_name="lessonId",
        expected_response_path="setLessonImage",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Upload an image to a LearningSuite course, topic, or lesson."
    )
    parser.add_argument("target", choices=sorted(OPERATIONS))
    parser.add_argument("--node-id", required=True, help="LearningSuite Node ID of the target object")
    parser.add_argument("--file", required=True, type=Path, help="Local image file")
    parser.add_argument(
        "--content-type",
        help="MIME type override, for example image/png. Inferred from the filename by default.",
    )
    parser.add_argument(
        "--tenant-id",
        default=os.getenv("LS_TENANT_ID"),
        help="LearningSuite tenant ID; defaults to LS_TENANT_ID",
    )
    parser.add_argument(
        "--email",
        default=os.getenv("LS_EMAIL"),
        help="LearningSuite login email; defaults to LS_EMAIL",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("LS_PASSWORD"),
        help="LearningSuite password; defaults to LS_PASSWORD",
    )
    return parser.parse_args()


def require_credentials(args: argparse.Namespace) -> None:
    missing = [
        name
        for name, value in {
            "tenant ID": args.tenant_id,
            "email": args.email,
            "password": args.password,
        }.items()
        if not value
    ]
    if missing:
        raise UploadError(
            "Missing credentials: " + ", ".join(missing) + ". "
            "Use --tenant-id/--email/--password or LS_TENANT_ID/LS_EMAIL/LS_PASSWORD."
        )


def authenticate(session: requests.Session, tenant_id: str, email: str, password: str) -> str:
    response = session.post(
        AUTH_URL,
        headers={"Content-Type": "application/json", "x-tenant-id": tenant_id},
        json={"email": email, "password": password},
        timeout=REQUEST_TIMEOUT,
    )
    if not response.ok:
        raise UploadError(f"Authentication failed ({response.status_code}): {response.text[:1000]}")

    try:
        payload = response.json()
    except ValueError as exc:
        raise UploadError("Authentication returned invalid JSON.") from exc

    token = payload.get("access_token")
    if not isinstance(token, str) or not token:
        raise UploadError("Authentication response did not contain access_token.")
    return token


def request_upload_spec(
    session: requests.Session,
    tenant_id: str,
    token: str,
    operation: UploadOperation,
    node_id: str,
) -> Mapping[str, Any]:
    url = f"https://api-p.learningsuite.io/{tenant_id}/graphql"
    body = {
        "operationName": operation.operation_name,
        "variables": {operation.variable_name: node_id},
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": operation.sha256_hash,
            }
        },
    }
    response = session.post(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json=body,
        timeout=REQUEST_TIMEOUT,
    )
    if not response.ok:
        raise UploadError(f"GraphQL request failed ({response.status_code}): {response.text[:2000]}")

    try:
        payload = response.json()
    except ValueError as exc:
        raise UploadError("GraphQL response was not valid JSON.") from exc

    errors = payload.get("errors")
    if errors:
        raise UploadError(f"LearningSuite GraphQL errors: {errors}")

    data = payload.get("data")
    if not isinstance(data, Mapping):
        raise UploadError("GraphQL response did not contain a data object.")

    expected = data.get(operation.expected_response_path)
    if isinstance(expected, Mapping) and expected.get("uploadUrl"):
        return expected

    fallback = find_upload_spec(data)
    if fallback is None:
        raise UploadError(
            f"No UploadSpec found. Expected data.{operation.expected_response_path}; "
            f"available keys: {', '.join(map(str, data.keys()))}"
        )
    return fallback


def find_upload_spec(value: Any) -> Mapping[str, Any] | None:
    """Find an UploadSpec defensively if LearningSuite changes only the response root key."""
    if isinstance(value, Mapping):
        if isinstance(value.get("uploadUrl"), str) and isinstance(value.get("requestHeaders", {}), Mapping):
            return value
        for child in value.values():
            found = find_upload_spec(child)
            if found is not None:
                return found
    elif isinstance(value, list):
        for child in value:
            found = find_upload_spec(child)
            if found is not None:
                return found
    return None


def upload_binary(
    session: requests.Session,
    upload_spec: Mapping[str, Any],
    file_path: Path,
    content_type: str,
) -> None:
    upload_url = upload_spec.get("uploadUrl")
    if not isinstance(upload_url, str) or not upload_url:
        raise UploadError("UploadSpec did not contain uploadUrl.")

    raw_headers = upload_spec.get("requestHeaders", {})
    if not isinstance(raw_headers, Mapping):
        raise UploadError("UploadSpec requestHeaders was not an object.")

    headers = {str(key): str(value) for key, value in raw_headers.items()}
    headers.setdefault("Content-Type", content_type)

    with file_path.open("rb") as file_handle:
        response = session.put(
            upload_url,
            headers=headers,
            data=file_handle,
            timeout=REQUEST_TIMEOUT,
        )
    if not response.ok:
        raise UploadError(f"Binary upload failed ({response.status_code}): {response.text[:2000]}")


def main() -> int:
    args = parse_args()
    try:
        require_credentials(args)
        file_path = args.file.expanduser().resolve()
        if not file_path.is_file():
            raise UploadError(f"File not found: {file_path}")

        content_type = args.content_type or mimetypes.guess_type(file_path.name)[0]
        if not content_type or not content_type.startswith("image/"):
            raise UploadError(
                "Could not determine an image MIME type. Use --content-type, for example image/png."
            )

        operation = OPERATIONS[args.target]
        session = requests.Session()
        session.headers.update({"User-Agent": "RH-LearningSuite-Image-Uploader/1.0"})

        token = authenticate(session, args.tenant_id, args.email, args.password)
        upload_spec = request_upload_spec(
            session, args.tenant_id, token, operation, args.node_id
        )
        upload_binary(session, upload_spec, file_path, content_type)

        print(
            f"Upload successful: target={args.target}, file={file_path.name}, "
            f"upload_id={upload_spec.get('id', 'unknown')}"
        )
        return 0
    except (UploadError, requests.RequestException, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
