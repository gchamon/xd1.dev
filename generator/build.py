from __future__ import annotations

import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from generator.content import Page, load_content

# Directories copied verbatim to dist/.
STATIC_DIRS = ("css", "js", "images")

# Match ``src="/...`` or ``href="/...`` but not protocol-relative ``//cdn``
# and not absolute ``https://``. Quote-style is fixed to ``"`` because both
# Python-Markdown and Jinja autoescape emit double-quoted attributes.
_URL_ATTR_RE = re.compile(r'((?:src|href)=")/(?!/)')


def _prefix_urls(html: str, base_url: str) -> str:
    """Prefix every absolute ``/…`` ``src``/``href`` in *html* with *base_url*.

    No-op when *base_url* is ``"/"``. Leaves protocol-relative (``//cdn``) and
    fully-qualified (``https://…``) URLs untouched.
    """
    if base_url == "/":
        return html
    return _URL_ATTR_RE.sub(lambda m: m.group(1) + base_url, html)


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _collect_tags(content: dict[str, list[Page]]) -> dict[str, list[Page]]:
    """Build a tag → pages mapping across all categories."""
    tags: dict[str, list[Page]] = defaultdict(list)
    for pages in content.values():
        for page in pages:
            for tag in page.tags:
                tags[tag].append(page)
    # Sort each tag's pages newest-first.
    for pages in tags.values():
        pages.sort(key=lambda p: p.date or datetime.min, reverse=True)
    return dict(tags)


def build(source_root: Path, output_dir: Path, base_url: str = "/") -> None:
    """Build the static site from *source_root* into *output_dir*.

    *base_url* is spliced in front of every internal link and must already be
    normalised (leading and trailing ``/``). Callers should pass ``"/"`` for
    a root-served deployment and something like ``"/xd1.dev/"`` for a
    project-page deployment.
    """

    # Clean output.
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    # Load content.
    content = load_content(source_root)
    categories = sorted(content.keys())
    tags = _collect_tags(content)

    # Set up Jinja2.
    env = Environment(
        loader=PackageLoader("generator", "templates"),
        autoescape=select_autoescape(["html"]),
    )
    env.filters["prefix_urls"] = _prefix_urls
    shared_ctx = {
        "categories": categories,
        "site_title": "xd1",
        "base_url": base_url,
        "now": datetime.utcnow(),
    }

    # --- Landing page (recent entries) ---
    # Show the most recent entries across all categories, preferring entries/.
    all_pages = []
    for pages in content.values():
        all_pages.extend(pages)
    all_pages.sort(key=lambda p: p.date or datetime.min, reverse=True)
    recent = all_pages[:10]

    tmpl_index = env.get_template("index.html")
    _write(
        output_dir / "index.html",
        tmpl_index.render(**shared_ctx, recent_posts=recent),
    )

    # --- Category pages ---
    tmpl_listing = env.get_template("listing.html")
    tmpl_post = env.get_template("post.html")

    for category, pages in content.items():
        cat_dir = output_dir / category

        if len(pages) == 1:
            # Single-page category: render directly as category index.
            page = pages[0]
            _write(
                cat_dir / "index.html",
                tmpl_post.render(**shared_ctx, page=page, is_category_index=True),
            )
        else:
            # Multi-page: listing + individual pages.
            _write(
                cat_dir / "index.html",
                tmpl_listing.render(**shared_ctx, category=category, pages=pages),
            )
            for page in pages:
                _write(
                    cat_dir / page.slug / "index.html",
                    tmpl_post.render(**shared_ctx, page=page, is_category_index=False),
                )

    # --- Tag pages ---
    if tags:
        tmpl_tags = env.get_template("tags.html")
        _write(
            output_dir / "tags" / "index.html",
            tmpl_tags.render(**shared_ctx, tags=tags),
        )

        tmpl_tag = env.get_template("tag.html")
        for tag_name, tag_pages in tags.items():
            _write(
                output_dir / "tags" / tag_name / "index.html",
                tmpl_tag.render(**shared_ctx, tag=tag_name, pages=tag_pages),
            )

    # --- Static assets ---
    for dirname in STATIC_DIRS:
        src = source_root / dirname
        if src.is_dir():
            shutil.copytree(src, output_dir / dirname)

    # Summary.
    total_pages = sum(len(p) for p in content.values())
    print(f"Built {total_pages} pages across {len(categories)} categories")
    print(f"Generated {len(tags)} tag pages")
    print(f"Output: {output_dir}")
