"""Content discovery, front-matter parsing, and markdown conversion."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import markdown

# Directories at repo root that are never content categories.
EXCLUDED_DIRS = frozenset({
    "weblog", "docs", "configuration", "css", "js", "images",
    "generator", ".git", ".github", ".venv", ".codex", "dist",
})


@dataclass
class Page:
    slug: str
    title: str
    date: datetime | None
    tags: list[str]
    html_body: str
    source_path: Path
    category: str


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Split ``---``-delimited front-matter from the markdown body.

    Returns (metadata dict, body markdown).  Metadata values are plain
    strings (not lists).
    """
    md = markdown.Markdown(extensions=["meta"])
    html = md.convert(text)
    meta: dict[str, str] = {}
    for key, values in getattr(md, "Meta", {}).items():
        # The meta extension returns each value as a list; we join.
        meta[key] = " ".join(values)
    return meta, html


def extract_title(body_markdown: str) -> str:
    """Return the text of the first ``# …`` ATX heading, or ``'Untitled'``."""
    match = re.search(r"^#\s+(.+)$", body_markdown, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled"


def _parse_date(raw: str) -> datetime | None:
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def _parse_tags(raw: str) -> list[str]:
    if not raw:
        return []
    return [t.strip() for t in raw.split(",") if t.strip()]


def load_page(path: Path, category: str) -> Page | None:
    """Parse a single markdown file into a Page, or None if it should be skipped."""
    text = path.read_text(encoding="utf-8")

    # Check for Type: Page (weblog.lol artifact) before full parse.
    meta, html_body = parse_frontmatter(text)
    if meta.get("type", "").lower() == "page":
        return None

    title = meta.get("title") or extract_title(text)
    date = _parse_date(meta.get("date", ""))
    tags = _parse_tags(meta.get("tags", ""))
    slug = path.stem  # filename without .md

    return Page(
        slug=slug,
        title=title,
        date=date,
        tags=tags,
        html_body=html_body,
        source_path=path,
        category=category,
    )


def discover_categories(root: Path) -> list[str]:
    """Return sorted list of category directory names under *root*."""
    categories = []
    for child in sorted(root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if child.name in EXCLUDED_DIRS:
            continue
        # Must contain at least one .md file.
        if any(child.glob("*.md")):
            categories.append(child.name)
    return categories


def load_content(root: Path) -> dict[str, list[Page]]:
    """Discover categories and load all pages, sorted newest-first per category."""
    content: dict[str, list[Page]] = {}
    for category in discover_categories(root):
        pages: list[Page] = []
        for md_file in sorted((root / category).glob("*.md")):
            page = load_page(md_file, category)
            if page is not None:
                pages.append(page)
        # Sort by date descending; dateless pages go last.
        pages.sort(key=lambda p: p.date or datetime.min, reverse=True)
        content[category] = pages
    return content
