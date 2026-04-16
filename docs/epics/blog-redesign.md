# Epic: Blog Redesign & Deployment

## Status

Planned

## Outcome

A completely redesigned blog (xd1.dev) based on the `buzz` project's terminal-inspired aesthetic, utilizing an agnostic static site generator that consumes existing Markdown files and is host-independent.

## Work items

- [agnostic-generator](/docs/work-items/blog-redesign-01-agnostic-generator.md)
- [buzz-theme-port](/docs/work-items/blog-redesign-02-buzz-theme-port.md)
- [deployment-setup](/docs/work-items/blog-redesign-03-deployment-setup.md)

## Decision Changes

- **Epic Prioritization**: Set to `critical` to drive the core project goal.
- **Provider Strategy**: Decouple from GitHub/GitLab specific features to ensure portability.

## Main Quests

1. **Tooling**: Implement an agnostic static site generator.
2. **Design**: Port the `buzz` aesthetic (CSS/Layout) to the blog generator.
3. **Content**: Reuse existing Markdown files from `weblog/`.
4. **Deployment**: Establish CI/CD for GitHub Pages (initial) and GitLab Pages (validation).

## Acceptance Criteria

- Blog is successfully generated as static HTML.
- Design matches `buzz` terminal aesthetic.
- Deployment works on both GitHub and GitLab Pages with minimal configuration changes.

## Metadata

### id

blog-redesign

### child_ids

- blog-redesign-01
- blog-redesign-02
- blog-redesign-03

### priority

critical
