from __future__ import annotations

import unittest

from learningsuite_make_deployer.services.apps import apply_app_visibility
from learningsuite_make_deployer.services.modules import apply_module_visibility
from learningsuite_make_deployer.settings import Settings


class RecordingClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.calls: list[tuple[str, str]] = []

    def call(self, method: str, path: str, **_: object) -> object:
        self.calls.append((method, path))
        return {}


class VisibilityIdempotencyTests(unittest.TestCase):
    def test_default_preserves_app_visibility(self) -> None:
        client = RecordingClient(Settings(api_token="x"))
        apply_app_visibility(client, "app", 1)
        self.assertEqual(client.calls, [])

    def test_default_preserves_module_visibility(self) -> None:
        client = RecordingClient(Settings(api_token="x"))
        apply_module_visibility(client, "/sdk/apps/app/1/modules/test")
        self.assertEqual(client.calls, [])

    def test_explicit_public_visibility_is_applied(self) -> None:
        client = RecordingClient(Settings(api_token="x", visibility="public"))
        apply_app_visibility(client, "app", 1)
        self.assertEqual(client.calls, [("POST", "/sdk/apps/app/1/public")])


if __name__ == "__main__":
    unittest.main()
