# Epic: Blog Redesign & Deployment

## Status
In Progress

## Outcome
A completely redesigned blog (xd1.dev) based on the `buzz` project's terminal-inspired aesthetic, utilizing an agnostic static site generator that consumes existing Markdown files and is host-independent.

## Context
The current blog is hosted on omg.lol. We want to move away from provider-locked platforms to a self-managed static generation flow. The new design should replicate the terminal/monochrome aesthetic of the `buzz` torrent manager.

## Main Quests
1. **Tooling**: Implement an agnostic static site generator.
2. **Design**: Port the `buzz` aesthetic (CSS/Layout) to the blog generator.
3. **Content**: Reuse existing Markdown files from `weblog/`.
4. **Deployment**: Establish CI/CD for GitHub Pages (initial) and GitLab Pages (validation).

## Success Criteria
- Blog is successfully generated as static HTML.
- Design matches `buzz` terminal aesthetic.
- Deployment works on both GitHub and GitLab Pages with minimal configuration changes.
