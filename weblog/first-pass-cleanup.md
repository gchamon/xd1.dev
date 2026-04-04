---
Date: 2026-04-04 10:37
Tags: ai, agents, python, tech
---

# The first pass cleanup

One thing I am starting to believe about agentic coding is that the first cleanup pass matters more than it looks.

It is not glamorous work. It does not add features. It does not close a milestone by itself. But it sets the stage for every change that comes after it, because with agents each incremental change builds on the state left behind by the previous one. The surrounding code, the instructions in the repository, the tests, the names, the structure, the comments, all of that becomes part of the prompt whether you write it down that way or not.

Garbage in, garbage out.

LLMs reflect the environment they are placed in. They are mimics. Not malicious, just imitative. If the repository is vague, inconsistent and loosely stitched together, the agent will tend to continue in that style. If the repository is documented, the code has some shape to it, and there are meaningful checks around it, the odds of getting useful work out of the machine go up immediately.

## A small example

I ran into this again while working on what started as `~/Projects/rebuild-thoracic-atlas/`, now renamed to `~/Projects/thoracic-atlas-viewer/`.

The goal was straightforward enough: preserve and rebuild a ZIP file for a thoracic atlas that had gone offline, using a saved HAR capture and a couple of helper scripts. That first pass produced working Python, but very much in the "it does the job" category. Then I added an `AGENTS.md` with more explicit Python expectations: follow PEP 8, keep the code simple, add docstrings, use type hints, prefer readability.

Only after that did I ask the agent to refactor the Python scripts.

The interesting part is not that the refactor happened. Of course it did. The interesting part is that the instructions changed what kind of refactor was likely to happen.

## Changing the stage

That cleanup pass did not invent a new architecture. It mostly tightened the space the agent was operating in.

In the atlas repository, that meant turning two rough utility scripts into code with clearer names, docstrings, simpler typing aliases, fewer stray imports and less line-wrapping chaos. One practical improvement I liked was moving the Playwright import inside the HAR capture helper, which meant `--help` could run even if the browser dependency was not installed yet. Small change, but exactly the sort of thing a cleanup-minded pass is more likely to produce than a speed-run implementation.

More importantly, the repository itself had started to explain what "good" looked like. Once that happened, later prompts stopped having to fight the local entropy quite so much.

## Why I think this matters

I do not think agents are best used as magic feature dispensers dropped into a random folder tree.

They behave more like the crystal dimension from Adventure Time than like an independent engineer with strong opinions. They pick up local shape. They echo the tone, the habits and the assumptions around them. If the project has decent documentation, coherent code, useful tests and some automated checks, you are giving the model rails to slide on. If not, you are mostly asking a pattern-matcher to imitate confusion.

So I am starting to think the first pass cleanup is not optional overhead. It is how you prepare the ground.

Not because clean repositories are morally superior, but because every later agent run will be downstream from that decision.
