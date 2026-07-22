from __future__ import annotations

import json
import time
from typing import Any, Iterable, Mapping

import requests

from .errors import DeploymentError
from .settings import Settings


class MakeClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Token {settings.api_token}",
                "Accept": "application/json",
                "User-Agent": "RH-LearningSuite-Make-Deployer/0.2",
            }
        )
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
        method = method.upper()
        expected_statuses = set(expected)
        url = f"{self.settings.api_base}{path}"

        if self.settings.dry_run:
            print(f"[DRY-RUN] {method} {url}")
            if payload is not None:
                print(json.dumps(payload, indent=2, ensure_ascii=False))
            elif text is not None:
                print(text)
            return {}

        for attempt in range(5):
            response = self.session.request(
                method,
                url,
                json=payload if text is None else None,
                data=text.encode("utf-8") if text is not None else None,
                headers={"Content-Type": content_type},
                timeout=60,
            )
            if response.status_code in expected_statuses:
                result = self._decode(response)
                self._collect_change(result)
                return result

            if response.status_code in {429, 500, 502, 503, 504} and attempt < 4:
                wait = float(response.headers.get("Retry-After", min(2**attempt, 15)))
                print(f"  Make API {response.status_code}; Wiederholung in {wait:.1f}s")
                time.sleep(wait)
                continue

            body = response.text[:4000]
            raise DeploymentError(
                f"{method} {path} fehlgeschlagen ({response.status_code}): {body}",
                method=method,
                path=path,
                status_code=response.status_code,
                body=body,
            )

        raise DeploymentError(
            f"{method} {path} endgültig fehlgeschlagen",
            method=method,
            path=path,
        )

    def optional(
        self,
        method: str,
        path: str,
        *,
        missing_statuses: Iterable[int] = (404,),
        **kwargs: Any,
    ) -> Any | None:
        try:
            return self.call(method, path, **kwargs)
        except DeploymentError as exc:
            if exc.status_code in set(missing_statuses):
                return None
            raise

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
        if not isinstance(result, Mapping):
            return
        change = result.get("change")
        if isinstance(change, Mapping) and isinstance(change.get("id"), int):
            change_id = int(change["id"])
            if change_id not in self.change_ids:
                self.change_ids.append(change_id)
