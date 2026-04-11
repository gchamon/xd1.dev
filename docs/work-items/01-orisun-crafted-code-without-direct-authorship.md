## Status

<!--
Use a short prose status for the current state of the work item.
Supported values are `backlog`, `planned`, `doing`, `done`, `cancelled`, and `abandoned`.
`killed` is reserved for GitLab graveyard history when a managed work item is removed from the repository.
-->

Backlog

## Outcome

Define an Orisun methodology note for a style of software craft where the
operator shapes the code to match their standards without directly typing the
resulting lines. The work item should explain how this can still count as
deliberate craft when the operator is responsible for the standards, the
constraints, the review, and the refinement loop that produces the code.

## Decision Changes

This work item treats authorship by keystrokes as a weak definition for
agent-assisted development. The stronger definition is whether the operator
intentionally shaped the result and accepted responsibility for it. It also
locks in the idea that early throughput may need to be sacrificed so the
operator can learn how to steer the agent precisely and refine the output until
it matches their standards.

The note should treat repository shape, local standards, and iterative review
as the practical conditions that make this form of craft possible. It should
not drift into a general blog draft or into philosophical treatment of
existentialist authorship, which belongs elsewhere.

## Main Quests

- Define what it means to have "crafted" code when the operator did not type
  the final lines directly.
- Describe the operator responsibilities that replace direct line-by-line
  authorship, including setting constraints, reviewing output, demanding
  revisions, and accepting the result as their own standard.
- Explain how repository cleanliness, conventions, tests, and guidance narrow
  the agent's search space and make deliberate shaping more realistic.
- Identify examples or future case studies that can ground this note in real
  practice instead of leaving it as an abstract claim.

## Acceptance Criteria

The work item is complete when it yields a methodology note outline that can be
used directly in Orisun documentation or expanded into a later essay without
changing the core claims. The note must clearly distinguish craft from mere
prompting, and it must make the operator's responsibilities concrete enough to
be actionable.

## Metadata

### id

orisun-crafted-code-01

### type

Issue
