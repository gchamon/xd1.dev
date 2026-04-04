# Repository Guidelines

## Project Structure & Module Organization

This repository is the source of truth for the `xd1.dev` blog. Content lives in [`weblog/`](/home/gchamon/Projects/xd1.dev/weblog), where each Markdown file is a published entry. Shared presentation assets live in [`css/`](/home/gchamon/Projects/xd1.dev/css), [`js/`](/home/gchamon/Projects/xd1.dev/js), and [`images/`](/home/gchamon/Projects/xd1.dev/images). Blog platform configuration is stored in [`configuration/`](/home/gchamon/Projects/xd1.dev/configuration), including the remote template and reset trigger file. Automation is handled by [`mkweblog.sh`](/home/gchamon/Projects/xd1.dev/mkweblog.sh) for new posts and [`weblog-import.php`](/home/gchamon/Projects/xd1.dev/weblog-import.php) for syncing changed files to omg.lol.

## Expected behavior

When editing files in ./weblog, you should only manage headers and write inside
comments. Don't attempt to write the blog article ourself. You only write
inside comments acting as an assistant, with general notes and lists of items
derived from the ideas in my prompt. I am the only one allowed to do edits in
the actual text. Sorry about that, maybe one day I'll create a blog article for
you so that you can write your own text using openclaw or something, let's
see...

## Build, Test, and Development Commands

There is no local build pipeline in this repo; changes are plain file edits plus deployment automation.

- `./mkweblog.sh slug "Post Title" "tag1, tag2"` creates a new post stub in `weblog/`.
- `php -l weblog-import.php` runs a syntax check on the import script before committing PHP changes.
- `bash -n mkweblog.sh` validates shell syntax after editing the helper script.
- `git diff --stat` is the quickest sanity check before pushing content, asset, or template updates.

## Coding Style & Naming Conventions

Use Markdown for posts, PHP for the importer, Bash for the post generator, and keep indentation consistent with the surrounding file: 4 spaces in scripts, simple paragraph-style prose in posts. Name blog entries with lowercase kebab-case slugs such as `weblog/reshade-chrono-trigger.md`. Keep image paths descriptive and grouped by post, for example `images/hyprland-crash-course/...`. Prefer direct, minimal changes over broad rewrites because deployment sync is file-based.

## Testing Guidelines

There is no formal automated test suite or coverage gate. Validate by linting edited scripts, checking Markdown front matter, and reviewing rendered links and image references. For content changes, confirm local paths like `/images/...` are valid because the importer rewrites them to GitHub raw URLs during sync.

## Commit & Pull Request Guidelines

Recent history favors short, imperative commit messages such as `change README`, `fix weird sentence phrasing`, and `add responses and changed wording`. Keep commits focused on one post, asset set, or script change. Pull requests should include a brief summary, note any affected paths, and attach screenshots when changing template, CSS, or image-heavy content.
