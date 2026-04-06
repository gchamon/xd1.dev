## Status

Doing

## Outcome

Preserve the recoverable evidence for `weblog/first-pass-cleanup.md` so the
article can continue from repository state alone rather than depending on
memory of this session. The work item should make the evidence bundle durable,
auditable, and easy to use when turning the current scaffold into a finished
post.

The main target is not the final prose itself. The target is a dependable
evidence base for that prose: the session-history timeline, the verified
current-code excerpts, the explicitly reconstructed rough examples, and the
article-side references that bind those materials together.

## Decision Changes

This work item locks in that the current progress is real repository state, not
just conversational intent. The session already produced a scaffolded article
file at `weblog/first-pass-cleanup.md` and a supporting evidence bundle under
`weblog/assets/first-pass-cleanup/`.

It also locks in that evidence provenance must remain explicit. Verified
session-history prompts and verified current-code excerpts are the authority
for the article. Reconstructed "before" examples are allowed because they help
illustrate the claim, but they must stay labeled as reconstructions and must
not be presented as exact recovered pre-refactor source.

The work item should not drift into full article authorship. Its role is to
capture what was recovered, define what is still missing, and make the later
writing pass safe to resume without reopening this session. Because the local
SQLite Codex logs are malformed, the repository should also avoid claiming that
the exact pre-refactor Python files were recovered.

## Main Quests

- Inventory the evidence bundle under `weblog/assets/first-pass-cleanup/` and
  confirm what each file proves.
- Keep the provenance labels stable across the bundle and the article scaffold:
  `Verified`, `Reconstructed`, and `Inference`.
- Ensure `weblog/first-pass-cleanup.md` references the evidence files in a way
  that a later writing pass can follow directly.
- Identify any missing evidence still needed before the scaffold can be turned
  into final prose, especially where the article currently depends on inferred
  transitions.
- Define the handoff from evidence curation into article drafting so the next
  pass knows what can be treated as factual support and what must remain marked
  as interpretation.

## Acceptance Criteria

The work item is complete when it records the current evidence artifacts, the
limits of that evidence, and the remaining curation work clearly enough that a
later session can continue without depending on recollection.

The bundle must be sufficient to support the article scaffold on its own. Each
example used by the article must have unambiguous provenance, and the article
must be able to distinguish verified material from reconstructed approximation
without additional detective work.

The resulting state must support a future writing pass that can safely expand
the post without re-deriving the timeline or re-investigating what was and was
not actually recovered from session history.

## Metadata

### id

first-pass-cleanup-evidence-04

### type

Issue
