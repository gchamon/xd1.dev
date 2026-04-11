# I Wrote None Of This Code

## Status

planned

## Outcome

Prepare a work-item that can drive the future blog article "I wrote none of
this code" without forcing the writing pass to rediscover the shape of the
story. The article should recount the side project where agentic coding was
used to design and implement the `orisun-gitlab` CI component in
`/home/gchamon/Projects/ci-components` and the `orisun-validator` tool in
`/home/gchamon/Projects/orisun`.

The narrative should be chronological. It should start from the motivation for
using the project as an agentic coding experiment, move through the design of
the CI component and validator, cover the testing that made the work durable,
and end on the failed or reverted improvement attempts that produced better
guidelines for Python work and agent instructions.

This artifact is planning only. It is not the blog post itself and it should
not create a `weblog/` draft yet.

## Decision changes

- use an Orisun-style work-item as the planning artifact even though
  `xd1.dev` does not otherwise use the full Orisun planning scaffold
- frame the future article as a chronological build story instead of a pure
  technical deep dive or a reflective essay
- ground the article in selective repo history from
  `/home/gchamon/Projects/ci-components` and
  `/home/gchamon/Projects/orisun`, crossing it with session memory where
  necessary for prompts, dead ends, and rationale that were not fully recorded
- treat the `AGENTS.md` and Python-guidelines discussions in
  `/home/gchamon/Projects/ci-components` as a supporting design thread instead
  of the main storyline
- postpone creation of `weblog/i-wrote-none-of-this-code.md` until the outline,
  evidence map, and anecdotes have been gathered

## Main quests

- Reconstruct the article timeline from repo evidence, focusing on the
  `orisun-gitlab` work-item sequence in
  `/home/gchamon/Projects/ci-components/docs/work-items/`,
  the component implementation under
  `/home/gchamon/Projects/ci-components/templates/orisun-gitlab/`,
  the toolkit code under
  `/home/gchamon/Projects/ci-components/toolbox/orisun-gitlab/`,
  and the validator implementation under
  `/home/gchamon/Projects/orisun/toolbox/validator/`.
- Extract the turning points that matter to the article, including the initial
  markdown contract, ingest and validation work, CI entrypoint behavior,
  branch-driven status updates, warning contract refinements, and the
  cancelled `python-gitlab` adoption direction.
- Build a writing outline that preserves the order of discovery: why this was
  chosen as an agentic coding experiment, how the CI component logic took
  shape, how the validator contract stabilized, how tests and fixtures proved
  the behavior, and which attempted improvements made the code or workflow
  worse before being corrected.
- Capture the testing story with enough specificity to support the article:
  validator fixtures, CLI tests, tool-local CI jobs, and any cases where tests
  exposed parser or sync-contract mistakes.
- Identify which claims can be backed directly by commits, work-items, README
  files, or code, and which claims depend on session-history recollection so
  the later writing pass can separate evidence from memory.
- Summarize how the implementation debates hardened into local guidance for
  Python scripts and agent behavior, especially the normalization-at-boundaries
  and simplicity-first preferences that ended up recorded in
  `/home/gchamon/Projects/ci-components/AGENTS.md`.

## Exit Criteria

- a complete article outline exists with a fixed section order and a clear
  ending focused on lessons learned from failed improvement attempts
- the future writing pass has a source map of the key repos, paths, work-items,
  and commits needed to support the narrative without rereading everything
- the notes explicitly cover both primary implementation threads:
  `orisun-gitlab` and `orisun-validator`
- the notes explicitly cover the testing strategy and at least one reverted or
  cancelled improvement path
- the plan leaves no ambiguity that this phase ends with research and outline
  material, not with a published `weblog/` article draft

## Metadata

### id

i-wrote-none-of-this-code
