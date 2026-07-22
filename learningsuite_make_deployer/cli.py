from __future__ import annotations

import argparse
import os
import sys

import requests

from .errors import DeploymentError
from .services.deployment import deploy
from .settings import Settings


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="LearningSuite Make Custom App idempotent deployen"
    )
    parser.add_argument("--zone", default=os.getenv("MAKE_ZONE", "eu1"))
    parser.add_argument(
        "--app-name", default=os.getenv("MAKE_APP_NAME", "learningsuite-graphql")
    )
    parser.add_argument(
        "--app-label", default=os.getenv("MAKE_APP_LABEL", "LearningSuite GraphQL")
    )
    parser.add_argument(
        "--version", type=int, default=int(os.getenv("MAKE_APP_VERSION", "1"))
    )
    parser.add_argument("--api-token", default=os.getenv("MAKE_API_TOKEN", ""))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-commit", action="store_true")
    parser.add_argument("--commit-all", action="store_true")
    parser.add_argument(
        "--visibility",
        choices=("preserve", "private", "public"),
        default=os.getenv("MAKE_APP_VISIBILITY", "preserve"),
        help="Standard preserve: bestehende App-Sichtbarkeit nicht verändern.",
    )
    parser.add_argument(
        "--module-visibility",
        choices=("preserve", "private", "public"),
        default=os.getenv("MAKE_MODULE_VISIBILITY", "preserve"),
        help="Standard preserve: bestehende Modul-Sichtbarkeit nicht verändern.",
    )
    return parser.parse_args()


def main() -> int:
    try:
        args = arguments()
        deploy(
            Settings(
                api_token=args.api_token or "DRY_RUN",
                zone=args.zone,
                app_name=args.app_name,
                app_label=args.app_label,
                version=args.version,
                dry_run=args.dry_run,
                commit=not args.no_commit,
                commit_all=args.commit_all,
                visibility=args.visibility,
                module_visibility=args.module_visibility,
            )
        )
        return 0
    except (DeploymentError, requests.RequestException) as exc:
        print(f"FEHLER: {exc}", file=sys.stderr)
        return 1
