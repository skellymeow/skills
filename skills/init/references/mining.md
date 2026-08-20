# Mining Hermes history for skill opportunities

The goal is not to summarize the user's life. The goal is to identify repeated work that should become a durable capability.

## Evidence unit

A useful evidence item has:

- `session_id`
- timestamp / source
- user intent in one short paraphrase
- finished outcome requested
- tools/workflow involved when visible
- friction/correction signal when present
- candidate capability domain

Prefer paraphrase over copying private text.

## What counts as strong evidence

Strong signals:

- the same deliverable appears in multiple distinct sessions
- the user repeatedly gives the same process instructions
- the user repeatedly corrects the agent for the same failure mode
- a task repeatedly combines 3+ tools/steps
- the user asks for a finished artifact, not just information
- setup is repeated across agents/machines/projects
- a deterministic operation is manually re-explained
- the same workflow appears across different projects

Weak signals:

- one-off trivia questions
- isolated personal conversation
- a single experimental tool mention
- generic preferences that do not define a workflow
- tasks already handled cleanly by an installed skill

## Cluster by finished outcome, not keywords

Do not create separate clusters for superficial wording differences.

These can be one `/video` domain:
- make a SaaS promo
- record a product walkthrough
- turn a reference Short into an original variant
- cut long footage into vertical clips

These are different domains:
- produce a video
- enrich and contact sales leads

## Candidate scoring: 100 points

### Recurrence - 30

Count distinct sessions, not repeated messages inside one session.

- 0: one-off
- 10: 2 distinct sessions
- 20: 3-5 distinct sessions
- 30: 6+ distinct sessions or a clearly recurring operational job

### Friction eliminated - 25

- 0: already easy / one step
- 10: repeated prompt explanation or setup
- 18: repeated corrections/failures
- 25: chronic multi-turn failure that a capability pack can structurally remove

### Deterministic leverage - 20

- 0: mostly conversational judgment
- 8: a few reusable templates/checks
- 14: repeatable scripts/checks materially improve reliability
- 20: substantial fragile work can become deterministic helpers

### Cross-project reuse - 15

- 0: specific to one temporary project
- 7: useful across several related projects
- 15: reusable across many projects/agents

### Setup/time savings - 10

- 0: no meaningful setup reduction
- 5: avoids repeated tool discovery/config explanation
- 10: converts repeated environment/tool orchestration into preflight + one command

## Deductions

Subtract:

- 25 if an installed skill already covers the domain well
- 15 if the candidate should clearly be an internal route of an existing skill
- 20 if it depends on an unverified/fragile third-party service with no fallback
- 20 if the task cannot define an observable finished outcome

Never lower a score because a task is technically ambitious if the evidence and payoff are real.

## Candidate design

For each top candidate define:

```text
command:
outcome:
internal routes:
onboarding choices:
preflight:
existing tools to reuse:
deterministic helpers:
optional providers:
permission gates:
quality proof:
evidence sessions:
score:
```

## Corrections are especially valuable

Repeated user corrections often encode the highest-value skill rules.

Examples:
- "stop asking me again" -> onboarding rule: reuse supplied context
- "deliver the MP4" -> completion contract: artifact first
- "you said it was done but didn't verify" -> mandatory verification gate
- "don't make 20 commands" -> architecture: one domain router

Turn repeated corrections into hard rules, not personality prose.

## Avoid overfitting

A skill should encode the reusable workflow, not private project facts.

Bad:
> Always write videos for Company X using their secret launch plan.

Good:
> For product promos, inspect the supplied product/site, identify the primary transformation, record real product footage, and verify the final MP4.

Project-specific facts belong in the current project, not the public/general skill.

## Final ranking

Recommend 3-5 candidates maximum in normal mode. The top candidate should be the capability that combines highest recurrence, highest friction reduction, and broadest reuse - not simply the most frequently mentioned noun.