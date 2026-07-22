from __future__ import annotations

import json
from typing import Any


class DeploymentError(RuntimeError):
    """Raised when a Make API deployment operation fails."""

    def __init__(
        self,
        message: str,
        *,
        method: str | None = None,
        path: str | None = None,
        status_code: int | None = None,
        body: str | None = None,
    ) -> None:
        super().__init__(message)
        self.method = method
        self.path = path
        self.status_code = status_code
        self.body = body or ""

    @property
    def api_code(self) -> str | None:
        try:
            payload: Any = json.loads(self.body)
        except (json.JSONDecodeError, TypeError):
            return None
        if isinstance(payload, dict):
            code = payload.get("code")
            return str(code) if code else None
        return None

    def has_text(self, needle: str) -> bool:
        return needle.casefold() in self.body.casefold() or needle.casefold() in str(self).casefold()
