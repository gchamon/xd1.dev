# Work Item: Buzz-based Theme Port

## Status

done

## Outcome

A Jinja2 template and CSS file that implements the `buzz` terminal aesthetic for the blog.

## Decision Changes

- **Generator location**: Python package at `generator/` with Jinja2 templates under `generator/templates/`.
- **Content directories**: Blog posts now live in `entries/` (not `weblog/`). Additional categories: `ops/` (projects), `hal/` (about). Directory names are auto-discovered as navigation categories.
- **Navigation pattern**: `xd1: entries ◈ ops ◈ hal` — categories auto-populated from discovered content directories.
- **Naming lore**: Discovery XD-1 / 2001: A Space Odyssey theme.
- **Template blocks**: `base.html` defines blocks `title`, `content`, `head_extra`. Theme work targets these blocks and the inline `<style>` in `base.html`.
- **Dependencies**: `pyproject.toml` at repo root, managed via `uv`. Jinja2 3.1+ and Markdown 3.10+.

## Main Quests

1. Extract CSS from `~/Projects/buzz/buzz/static/buzz.css`.
2. Design a blog post layout based on `torrents.html`.
3. Implement a monochrome/terminal theme with the Dracula-inspired palette.
4. Ensure mobile responsiveness.

## Acceptance Criteria

- Blog post rendering matches the `buzz` look and feel.
- Code blocks and typography follow the mono-spaced aesthetic.

## Metadata

### id

blog-redesign-02

### type

Issue
