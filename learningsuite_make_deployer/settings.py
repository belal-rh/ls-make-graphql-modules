from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from .errors import DeploymentError

Visibility = Literal["preserve", "private", "public"]
ALLOWED_ZONES = {"eu1", "eu2", "us1", "us2"}


@dataclass(frozen=True)
class Settings:
    api_token: str
    zone: str = "eu1"
    app_name: str = "learningsuite-graphql"
    app_label: str = "LearningSuite GraphQL"
    version: int = 1
    dry_run: bool = False
    commit: bool = True
    commit_all: bool = False
    visibility: Visibility = "preserve"
    module_visibility: Visibility = "preserve"

    @property
    def api_base(self) -> str:
        return f"https://{self.zone}.make.com/api/v2"

    def validate(self) -> None:
        if self.zone not in ALLOWED_ZONES:
            raise DeploymentError(f"Ungültige Make-Zone: {self.zone}")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", self.app_name):
            raise DeploymentError(
                "App-Name darf nur Kleinbuchstaben, Zahlen und Bindestriche enthalten."
            )
        if self.version < 1:
            raise DeploymentError("App-Version muss mindestens 1 sein.")
        if not self.api_token and not self.dry_run:
            raise DeploymentError(
                "MAKE_API_TOKEN fehlt (benötigte Scopes: sdk-apps:read, sdk-apps:write)."
            )
