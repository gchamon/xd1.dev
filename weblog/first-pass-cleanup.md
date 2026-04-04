---
Date: 2026-04-04 10:37
Tags: ai, agents, python, tech
---

# The first pass cleanup

<!--
Assistant notes:

- Opening thesis:
  - The first cleanup pass matters more than it looks.
  - It does not add features directly, but it shapes every later agent run.
  - With agents, each incremental change accumulates because later behavior depends on the local repository state.
- Phrase to preserve:
  - Garbage in, garbage out.
- Analogy to consider:
  - LLMs as mimics, not malicious, but strongly imitative.
  - "Like demons but without the intent to hurt" if you want a harsher line.
  - "Crystal plane / crystal dimension from Adventure Time" as the image for reflective behavior.
- Angle:
  - The repository itself becomes part of the prompt.
  - Code quality, naming, docs, tests, comments, and automation all constrain what the agent is likely to do next.
- Evidence bundle:
  - `weblog/assets/first-pass-cleanup/timeline.md`
  - `weblog/assets/first-pass-cleanup/agents-python-guidance.md`
-->

## Context

<!--
Assistant notes:

- Use the thoracic atlas repo as the concrete story:
  - Started as `~/Projects/rebuild-thoracic-atlas/`
  - Renamed to `~/Projects/thoracic-atlas-viewer/`
- Problem setup:
  - A thoracic atlas ZIP had gone offline.
  - The viewer was still up.
  - The repo preserved a HAR capture and used scripts to reconstruct the ZIP.
- Grounded sequence from session history:
  - First session prompt: create the project, document the approach, and add `download.sh`.
  - Later session prompt: "using the new definition for the python style present in AGENTS.md, lets refactor the python scripts"
- Framing:
  - The first pass got the job done.
  - The later pass was about cleaning the stage the agent would work on.
- Supporting asset:
  - `weblog/assets/first-pass-cleanup/timeline.md`

Suggested inline evidence block:

```text
Session: 019d5884-ce31-7da1-9652-2aae1653110e

we are going to create a project to rebuild the zip file of the thoracic atlas
...
I'd like to properly document this in this repo and create a download.sh file
in the project's root to download and produce the .zip
```
-->

## A small example

<!--
Assistant notes:

- Mention the two Python scripts as the example:
  - `scripts/rebuild_zip.py`
  - `scripts/capture_har.py`
- What is concrete in the current cleaned-up version:
  - module docstrings
  - function docstrings
  - type hints
  - clearer function boundaries
  - explicit validation and error messages
  - small focused helpers like `contains_atlas_requests`, `atlas_relative_path`, `collect_assets`
- Mention `AGENTS.md` as the pivot:
  - It introduced explicit Python expectations: PEP 8, type hints, docstrings, readable imports, simplicity over unnecessary "production ready" complexity.
- Suggested point:
  - The interesting part is not merely that a refactor happened.
  - The interesting part is that the agent was refactored after being given a better local standard to imitate.
- Supporting assets:
  - `weblog/assets/first-pass-cleanup/before-reconstructed.py`
  - `weblog/assets/first-pass-cleanup/after-capture_har.py`
  - `weblog/assets/first-pass-cleanup/after-rebuild_zip.py`

Suggested inline before/after pair:

```python
# Reconstructed approximation, not the exact original file.
def main():
    har = json.loads(Path(sys.argv[1]).read_text())
    assets = {}
    for entry in har["log"]["entries"]:
        req = entry["request"]
        res = entry["response"]
        if req["method"] != "GET":
            continue
        if not req["url"].startswith(ATLAS_PREFIX):
            continue
```

```python
def load_har(path: Path) -> HarData:
    """Load a captured HAR file from disk."""
    return json.loads(path.read_text(encoding="utf-8"))


def contains_atlas_requests(har: HarData) -> bool:
    """Return True when the HAR contains successful atlas asset requests."""
    for entry in har.get("log", {}).get("entries", []):
        request = entry.get("request", {})
        response = entry.get("response", {})
```
-->

## Changing the stage

<!--
Assistant notes:

- Good place to make the broader argument:
  - The cleanup pass tightens the space the agent is operating in.
  - It does not need to invent a new architecture to matter.
- Concrete details you can safely cite from the repo:
  - Playwright import moved inside `capture_raw_har`, which keeps CLI help lighter and avoids importing browser tooling until needed.
  - ZIP rebuild flow validates required atlas files and rejects bad HARs explicitly.
  - README now explains rebuild vs capture responsibilities separately.
- Inference to label as inference if you use it:
  - The pre-refactor scripts were likely more "just make it work" and less explicit in structure.
  - We do not have a committed pre-refactor snapshot, only the surviving session sequence plus the current files.
- Suggested transition:
  - Once the repo started to explain what "good" looked like, later prompts no longer had to fight local entropy as much.
- Supporting asset:
  - `weblog/assets/first-pass-cleanup/agents-python-guidance.md`

Suggested inline guidance block:

```markdown
## 3. Use Type Hinting

While Python is dynamically typed, introducing type hints drastically improves
code clarity.

## 5. Document Effectively

* Docstrings: Write descriptive docstrings for all public modules, functions,
  classes, and methods.
```
-->

## Garbage in, garbage out

<!--
Assistant notes:

- This section can expand the philosophy:
  - Agents reflect the environment.
  - If the repo is vague, inconsistent, and loosely stitched together, the agent will continue that style.
  - If the repo is documented, coherent, and validated, the chance of useful output goes up.
- Possible wording seeds:
  - "The repository is not just context, it is training wheels for the next prompt."
  - "The model picks up local shape."
  - "You are not prompting in a vacuum; you are prompting into a habitat."
- Tie this to tests and automation:
  - meaningful tests
  - automated test pipeline
  - documented commands
  - clear instructions for contributors and agents
-->

## Arriving at the point

<!--
Assistant notes:

- Mirror the reflective turn from `backups-and-bitrot.md`.
- Main conclusion:
  - The first pass cleanup is not optional overhead.
  - It is how you prepare the ground for every later agent-assisted change.
- Suggested emphasis:
  - Not because clean repos are morally superior.
  - Because every later run is downstream from the state you leave behind.
- Candidate closing line:
  - "The first pass cleanup sets the stage; after that, the agent mostly keeps acting in the play you have already built."
-->
