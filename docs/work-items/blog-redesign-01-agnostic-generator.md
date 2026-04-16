# Work Item: Agnostic Static Generator

## Status

done

## Outcome

A script or tool that converts `weblog/*.md` into `dist/*.html` using Jinja2 or similar templating, focusing on being provider-agnostic.

## Decision Changes

- **Content source**: Posts live in `entries/`, `ops/`, `hal/` at repo root — not `weblog/`. Additional categories are auto-discovered from any root directory containing `.md` files.
- **Host-agnostic URLs**: Implemented via `--base-url` CLI flag (env: `BASE_URL`, default `/`). The generator normalises the prefix and splices it into every internal `href`/`src`. Deployers supply the value; the generator has no notion of GitHub or GitLab.
- **Markdown library**: Python-Markdown with `meta`, `fenced_code`, and `tables` extensions.
- **Template engine**: Jinja2 via `PackageLoader`; templates live in `generator/templates/`.

## Main Quests

1. Research/Select minimal markdown processing library.
2. Implement template-based HTML generation.
3. Handle metadata (front-matter) extraction from existing files.
4. Ensure the output structure is host-agnostic (relative paths).

## Acceptance Criteria

- Running the generator produces a valid static site in `dist/`.
- No hardcoded provider URLs in generated files.
- Front-matter tags and dates are correctly preserved.

## Metadata

### id

blog-redesign-01

### type

Issue
