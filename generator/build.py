"""Build orchestrator: discover → parse → render → write."""

from __future__ import annotations

import shutil
from collections import defaultdict
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

from generator.content import Page, load_content

# Directories copied verbatim to dist/.
STATIC_DIRS = ("css", "js", "images")


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
        from datetime import datetime
        pages.sort(key=lambda p: p.date or datetime.min, reverse=True)
    return dict(tags)


def build(source_root: Path, output_dir: Path) -> None:
    """Build the static site from *source_root* into *output_dir*."""

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
    shared_ctx = {
        "categories": categories,
        "site_title": "xd1",
    }

    # --- Landing page (recent entries) ---
    # Show the most recent entries across all categories, preferring entries/.
    all_pages = []
    for pages in content.values():
        all_pages.extend(pages)
    from datetime import datetime
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
