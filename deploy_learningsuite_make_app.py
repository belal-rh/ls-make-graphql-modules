#!/usr/bin/env python3
"""Thin CLI entrypoint for the modular LearningSuite Make deployer."""

from learningsuite_make_deployer.cli import main


from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    raise SystemExit(main())
