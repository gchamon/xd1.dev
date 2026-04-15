# Athletes Against Bicycles

## Status

planned

## Outcome

Prepare the scaffold for a future blog article, "Athletes Against Bicycles",
without forcing the writing pass to rediscover the thesis, section order, or
the role of the project anecdotes. The article should argue against the idea
that AI makes software developers obsolete by opening with an absurd allegory:
athletes unionize against bicycles, fear that walking will become obsolete, and
smash every bicycle in the country.

The article should not stay trapped inside the allegory. It should explicitly
break the metaphor early, acknowledge that bicycles never represented a real
threat to human work in the way AI can, and then pivot into a practical stance:
AI is better understood as a bicycle or an exoskeleton for the mind. It still
requires effort, judgment, and direction, but it can multiply what a person can
do with modest time and money, including when using less capable models.

This artifact is planning plus scaffold support. It should drive a paired
`weblog/athletes-against-bicycles.md` draft that contains only front matter,
headings, and HTML comments with writing prompts.

## Decision Changes

- create both a work-item and a matching `weblog/` scaffold in the same pass
- keep the article aimed at practitioners already using AI rather than general
  readers or pure skeptics
- use a balanced weave between allegory and concrete project anecdotes instead
  of a strict "story first" or "projects first" structure
- reserve three named project slots so the writing pass can decide which
  examples best support the argument without changing the shape of the article
- end on a practical posture about using AI well rather than on a manifesto or
  a purely reflective conclusion
- keep the `weblog/` draft compliant with `AGENTS.md`: no authored article
  prose, only comments and headers

## Main Quests

- Fix the article thesis in advance: AI does pose a genuine labor risk, but the
  most useful immediate response for practitioners is not sabotage or denial,
  but learning how to extract leverage from it responsibly.
- Open with the athlete-versus-bicycle fiction strongly enough that the reader
  understands the absurdity before the article punctures its own metaphor.
- Add an explicit "where the allegory breaks" section so the article does not
  pretend the comparison is airtight.
- Use the middle of the article to reframe AI as cognitive leverage:
  bicycle, tool, and exoskeleton all in service of the same point that effort
  still matters.
- Recount three projects or experiments that show concrete leverage from AI,
  especially cases where modest models were enough because the human supplied
  the structure, taste, or debugging.
- End with practical guidance that is grounded in lived experience:
  what AI is good for, what still requires human work, and how to avoid being
  turned into a passive operator.

## Section Blueprint

### 1. Opening fiction

Purpose:
Introduce the athlete union and the anti-bicycle campaign in an exaggerated but
internally serious tone.

Must establish:

- athletes fear walking will be devalued
- bicycles are framed as unfair mechanical amplification
- the movement escalates into breaking bicycles across the country
- the reader should feel the comparison is silly, but not yet know exactly why
  it is being used

### 2. Where the allegory breaks

Purpose:
Break the metaphor on purpose and regain intellectual honesty.

Must establish:

- bicycles were never a credible threat to eliminate the need for human motion
- AI can plausibly destroy, compress, or deskill parts of software work
- the point of the allegory is not "there is no threat"
- the real target is the instinct to answer new leverage with sabotage,
  purity-testing, or denial

### 3. AI as a bicycle for the mind

Purpose:
Propose the replacement frame for the rest of the article.

Must establish:

- AI works best as leverage, not autonomy
- using it well still costs effort and skill
- the return on that effort can be absurdly high compared to the investment
- good outcomes do not require the strongest or most expensive model if the
  workflow is designed well

### 4. Project evidence

Purpose:
Support the thesis with concrete work.

For each project section, the later writing pass should answer:

- what problem existed before AI entered the picture
- what part AI accelerated or unlocked
- what the human still had to decide, verify, or repair
- where a cheaper or weaker model was sufficient
- what this says about augmentation rather than replacement
- what went wrong, or what stayed difficult, so the section remains credible

### 5. Practical ending

Purpose:
Close with actionable posture rather than abstraction.

Must establish:

- practitioners should learn to ride the bicycle instead of pretending it will
  disappear
- human judgment, verification, and responsibility remain the scarce part
- workflow design matters more than model mystique
- modest models become much more useful when paired with discipline and
  structure

## Project Slots

### Project 1: [name]

Intended role:
Use this slot for the clearest example where AI multiplied throughput on a
bounded engineering task.

Collect during writing:

- repo or project name
- one-sentence problem statement
- one concrete output delivered faster because of AI
- one place where you had to step in and correct direction
- whether a smaller or cheaper model was good enough

### Project 2: [name]

Intended role:
Use this slot for a more ambiguous or exploratory project, where the value came
from iteration, reframing, or research assistance rather than direct code
generation alone.

Collect during writing:

- what AI helped you see or test earlier
- what remained stubbornly human
- one failure mode that proves the tool was not self-sufficient
- how the final result was still worth the overhead

### Project 3: [name]

Intended role:
Use this slot for a project that best supports the claim about good results from
modest models, disciplined prompting, or a well-designed workflow.

Collect during writing:

- what constraints forced pragmatism
- how you adapted the process to the model instead of expecting magic
- what quality bar you still enforced manually
- what this implies for cost-effective AI use

## Exit Criteria

- the paired blog draft exists in `weblog/` with matching headings and comments
- the article shape is fixed enough that the writing pass does not need to
  decide how the allegory, break, project evidence, and ending relate
- the scaffold explicitly preserves the nuance that AI risk is real even though
  the bicycle allegory is absurd
- each project slot includes prompts for both leverage and limitations
- the ending is clearly practical and argues for intentional augmentation with
  modest models where appropriate

## Metadata

### id

athletes-against-bicycles
