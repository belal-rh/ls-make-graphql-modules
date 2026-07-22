#!/usr/bin/env python3
"""Backward-compatible entrypoint. Use deploy_learningsuite_make_app.py."""

from learningsuite_make_deployer.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
