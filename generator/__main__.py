"""CLI entry point: python -m generator"""

from __future__ import annotations

import argparse
from pathlib import Path

from generator.build import build


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
    args = parser.parse_args()

    source_root = Path(args.source).resolve()
    output_dir = Path(args.output).resolve()

    build(source_root, output_dir)


if __name__ == "__main__":
    main()
