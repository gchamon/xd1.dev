# First-pass cleanup evidence timeline

This file records the recoverable session-history evidence for the thoracic
atlas example used by `weblog/first-pass-cleanup.md`.

## Verified session prompts

Source: `~/.codex/history.jsonl`

### 1. Initial implementation pass

Session: `019d5884-ce31-7da1-9652-2aae1653110e`

```text
we are going to create a project to rebuild the zip file of the thoracic atlas,
which used to be available at
https://www.openanatomy.org/atlases/macbioidi/mauritania/thorax-2020-11-15.zip
but it's since 2024 been offline.

Fortunately the viewer is up at
https://www.openanatomy.org/atlases/macbioidi/mauritania/thorax-2020-11-15/viewer/

I have extracted a har file which I placed in this repository for preservation,
but we should be able to create a pipeline to reproduce the file. Thats for
later.

I can analyse the har and download the necessary URL's with:

jq -r '
  .log.entries[]
  | .request.url
  | select(startswith("https://www.openanatomy.org/atlases/macbioidi/mauritania/thorax-2020-11-15/Data/"))
' /tmp/www.openanatomy.org_Archive\ \[26-04-04\ 09-31-17\].har |
  while read -r url; do
    wget $url
  done

I'd like to properly document this in this repo and create a download.sh file in
the project's root to download and produce the .zip
```

Interpretation:

- The first pass started from a direct shell pipeline and a concrete utility goal.
- The request focused on making the workflow work and documenting it.

### 2. Refactor after adding repo guidance

Session: `019d589a-b913-76e0-8bba-f6a88b2166e1`

```text
in the last session we structured this repository. You should be able to
rebuild context from this repo's readme and files, if not, consult the last
session logs and propose what could be better.
```

```text
ignore previous plan. using the new definition for the python style present in
AGENTS.md, lets refactor the python scripts in this repository
```

Interpretation:

- This is the recoverable pivot point for the article.
- The refactor was explicitly requested after the repository gained
  `AGENTS.md` guidance for Python.

## Evidence limits

- The exact pre-refactor Python files were not recoverable from committed
  history.
- The local SQLite Codex log database is malformed, so only `history.jsonl`
  session prompts were used as durable evidence.
- Any "before" code example in the article must therefore be labeled as a
  reconstruction, not as an exact recovered file.
