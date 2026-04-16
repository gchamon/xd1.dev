# xd1.dev

This is the repository that is the source of truth for my blog hosted at <https://xd1.dev>.

The automation is based on the upstream repo, but is heavily modified to make it easy for me to upload images to github and have them reflected in the blog, as well as
fixing some quirks in the way that weblog handles markdown, so that it plays well with prism.js for displaying code with syntax highlight.

## mkweblog.sh

This script makes it easier to create weblog posts. It expects three arguments,
the filename (without .md), the title and optionally some tags. Example:

```bash
./mkweblog.sh not-buying-american "Not buying american anymore" "rant, opinion"
```

## Force a full weblog resync

The deploy workflow normally syncs only files changed in the latest commit. If the
remote weblog state gets out of sync or a bad template/config needs to be replaced
everywhere, commit a change to [`configuration/reset`](/home/gchamon/Projects/xd1.dev/configuration/reset).
When [`weblog-import.php`](/home/gchamon/Projects/xd1.dev/weblog-import.php) sees that file in the pushed diff,
it calls the omg.lol reset endpoint and re-uploads every tracked file in the repo.

Update the reset marker with a fresh timestamp, then commit and push:

```bash
printf 'reset %s\n' "$(date +%Y-%m-%dT%H-%M)" > configuration/reset
```

Rerunning an old GitHub Actions job is not enough by itself; the reset file must be
part of a new commit so the importer enters its full rebuild path.


## Static site generator

The repository includes a static site generator that converts Markdown files
into a self-contained HTML site under `dist/`. It replaces the older
weblog.lol sync pipeline for local and CI-driven builds.

### Prerequisites

Python 3.14+ and [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

### Building the site

```bash
.venv/bin/python -m generator
```

This reads every content category directory at the repo root (`entries/`,
`hal/`, `ops/`, or any other directory containing `.md` files), converts them
to HTML, and writes the result to `dist/`.

### Options

```bash
# Custom output directory
.venv/bin/python -m generator --output build

# Different source root
.venv/bin/python -m generator --source /path/to/content
```

### Creating a new post

```bash
./mkweblog.sh my-new-post "My new post" "tag1, tag2"
```

This creates `entries/my-new-post.md` with front-matter and a title stub.
Run the generator again to see it in `dist/`.

### Content organization

Top-level directories with `.md` files are auto-discovered as site categories.
Each category becomes a navigation entry and gets its own section in the
generated site:

| Directory   | Purpose                     | URL            |
|-------------|-----------------------------|----------------|
| `entries/`  | Blog posts (ship's log)     | `/entries/`    |
| `ops/`      | Projects and operations     | `/ops/`        |
| `hal/`      | About (HAL's self-portrait) | `/hal/`        |

A category with a single `.md` file renders as a standalone page.
A category with multiple files gets a listing page plus individual pages.

See [`generator/README.md`](generator/README.md) for architecture details.