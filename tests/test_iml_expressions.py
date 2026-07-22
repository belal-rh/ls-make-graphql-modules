from __future__ import annotations

import json
import unittest

from learningsuite_make_deployer.specs import module_definitions
from learningsuite_make_deployer.specs.common import gql_request


class ImlExpressionTests(unittest.TestCase):
    def test_graphql_valid_condition_uses_supported_negation(self) -> None:
        request = gql_request(
            operation="ExampleQuery",
            sha256_hash="0" * 64,
            variables={},
            output="{{body.data}}",
        )

        self.assertEqual(
            request["response"]["valid"]["condition"],
            "{{!body.errors}}",
        )

    def test_generated_modules_do_not_use_empty_function(self) -> None:
        serialized = json.dumps(module_definitions("testConnection"))
        self.assertNotIn("empty(", serialized)


if __name__ == "__main__":
    unittest.main()
