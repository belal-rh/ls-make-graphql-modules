from __future__ import annotations

from typing import Any

from .common import app_base, connection_api, connection_parameters, groups
from .courses import course_modules
from .lessons import lesson_modules
from .sections import section_modules
from .topics import topic_modules
from .universal import universal_modules


def module_definitions(connection: str) -> list[dict[str, Any]]:
    return [
        *course_modules(connection),
        *topic_modules(connection),
        *section_modules(connection),
        *lesson_modules(connection),
        *universal_modules(connection),
    ]


__all__ = [
    "app_base",
    "connection_api",
    "connection_parameters",
    "groups",
    "module_definitions",
]
