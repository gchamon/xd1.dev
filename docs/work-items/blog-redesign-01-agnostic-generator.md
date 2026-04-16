# Work Item: Agnostic Static Generator

## Status

planned

## Outcome

A script or tool that converts `weblog/*.md` into `dist/*.html` using Jinja2 or similar templating, focusing on being provider-agnostic.

## Decision Changes

- None.

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
