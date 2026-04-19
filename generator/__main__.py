"""CLI entry point: python -m generator"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

import yaml

from generator.build import build


def _load_config(source_root: Path) -> dict:
    """Load configuration from xd1.conf.yml if it exists."""
    config_path = source_root / "xd1.conf.yml"
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Failed to load config from {config_path}: {e}")
    return {}


def _normalize_base_url(raw: str) -> str:
    """Return *raw* with a single leading and trailing slash.

    Empty/``"/"`` stays ``"/"``. Any repeated slashes collapse. This lets
    callers pass ``"xd1.dev"``, ``"/xd1.dev"``, or ``"/xd1.dev/"`` and get the
    same canonical ``"/xd1.dev/"`` the templates splice in.
    """
    if not raw:
        return "/"
    if not raw.startswith("/"):
        raw = "/" + raw
    if not raw.endswith("/"):
        raw = raw + "/"
    return re.sub(r"/+", "/", raw)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="xd1 static site generator",
    )
    parser.add_argument(
        "--output", "-o",
        default="dist",
        help="output directory (default: dist)",
    )
    parser.add_argument(
        "--source", "-s",
        default=".",
        help="source root directory (default: current directory)",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("BASE_URL", "/"),
        help=(
            "URL prefix for all internal links, e.g. '/xd1.dev/' for a "
            "project-page deployment (default: '/' or $BASE_URL)"
        ),
    )
    parser.add_argument(
        "--theme", "-t",
        default=os.environ.get("THEME", "dracula"),
        help="active theme name (default: dracula or $THEME)",
    )
    args = parser.parse_args()

    source_root = Path(args.source).resolve()
    output_dir = Path(args.output).resolve()

    # Load file config and merge with CLI/Env (CLI/Env takes precedence)
    file_config = _load_config(source_root)

    base_url_raw = args.base_url
    if base_url_raw == "/" and "base_url" in file_config:
        base_url_raw = file_config["base_url"]
    base_url = _normalize_base_url(base_url_raw)

    theme = args.theme
    if theme == "dracula" and os.environ.get("THEME") is None and "theme" in file_config:
        theme = file_config["theme"]

    build(source_root, output_dir, base_url, theme)


if __name__ == "__main__":
    main()
