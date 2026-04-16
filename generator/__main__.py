"""CLI entry point: python -m generator"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

from generator.build import build


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
    args = parser.parse_args()

    source_root = Path(args.source).resolve()
    output_dir = Path(args.output).resolve()
    base_url = _normalize_base_url(args.base_url)

    build(source_root, output_dir, base_url)


if __name__ == "__main__":
    main()
