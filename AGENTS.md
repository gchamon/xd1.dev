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


## Rules of engagement

This section provides instructions for how to behave when engaging with the
implementation of work item tasks.

These rules are engaged when starting a session with `engage with
{docs/work-items/[work-item-name].md}` or similar, where the `[work-item-name]`
pattern is documented in [the work items readme](./docs/work-items/README.md).

When asked to engage you should always enter plan mode if not already.

### Restrictions

- Never update a work item that is already completed
  - You can only update a decision changes in the output section
  - the output's decision changes should be reserved exclusively for necessary
  changes during the implementation of the work-item that needed to be
  reflected after the work-item went to done
  - these decision changes must be actual design decisions or changes in
  implementation direction, not delivery details, completion summaries, test
  coverage notes, or other descriptions of what was built

### Preparation phase

First always use the start of the session to ground yourself in the context of
the work item. You are free to pull data from ~/.codex/sessions/ whenever
necessary, but always ask when doing so because this can be token-intensive.

When handling epics or work items, always include
`docs/work-items/README.md` and `docs/epics/README.md` in the working context.
You are free to pull data from ~/.codex/sessions/ whenever necessary, but
always ask when doing so because this can be token-intensive.

### Execution phase

The execution phase will go on until the user is satisfied with reviewing the
changes, before then the agent and the user are going to iterate on the
implementation.

It's important to always consider if there is need for a final pass over the
work item's acceptance criteria before exiting the Execution phase to catch
anything that was overlooked.

### Post phase

In the post phase of implementing a work item, propagate changes in the design
and decisions to the next work item in the sequence, if there are any, in which
case these changes have to be added to the last work item under `Decision
changes` section.

Never mark a work item as completed without first checking that all of its main
quests, side-quests that were taken on as part of the implementation, and exit
criteria were actually fulfilled. If any accepted quest or exit criterion is
still open, do not mark the work item as complete; leave it in an appropriate
non-complete status and record the remaining work explicitly.
