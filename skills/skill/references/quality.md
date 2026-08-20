# Skill quality gate

A skill is not ready because its Markdown looks polished or an evaluator gives it a high score. It is ready when an agent can trigger it correctly, execute the baseline path, recover from realistic failures, and prove the promised result.

## Critical checks

Fail the skill if any are true:

- `SKILL.md` is missing valid frontmatter with `name` and `description`.
- The description does not make the intended trigger clear enough to distinguish nearby skills.
- The command represents several unrelated domains that should not share one router.
- A referenced file does not exist.
- A required dependency has no detection/setup path.
- An imaginary or unverified package, API, model, CLI, pricing claim, licensing claim, or capability is presented as fact.
- Secrets, API keys, tokens, passwords, private session contents, or machine-specific credentials are hardcoded.
- The skill can install software, spend money, publish, send, deploy, delete, overwrite, or make another consequential side effect without a permission gate.
- A required operation can fail while the skill still declares success.
- The skill says work is complete without observable proof.
- The only output is instructions when the skill promises a finished artifact and execution tools are available.

## Architecture checks

Pass when:

- one memorable slash command owns one coherent domain
- internal workflows are routed instead of exposed as needless micro-skills
- `SKILL.md` behaves like a concise control plane
- deep or niche details live in `references/`
- scripts are used only where determinism adds real value
- every helper has a documented invocation and failure path
- MCP/native integration is justified by a real system boundary rather than fashion
- optional providers remain optional
- free/local baseline is used when practical without lowering required quality
- the skill composes with existing skills instead of pretending to replace unrelated capabilities

## UX checks

Pass when:

- specific requests bypass unnecessary onboarding
- vague requests get a compact choice set, not an interrogation
- the agent recommends a default when presenting choices
- the machine is inspected automatically when possible
- users are not expected to know implementation jargon
- missing dependencies produce exact recovery instructions
- no question is asked twice
- the deliverable is surfaced directly rather than buried in a workspace

## Reliability checks

For every helper script:

- usage and arguments are documented or discoverable via `--help`
- paths are cross-platform or intentionally documented
- inputs and outputs are deterministic enough for downstream steps
- invalid inputs and failures return useful non-zero errors
- destructive behavior is opt-in
- partial/intermediate outputs are preserved when useful for recovery
- no secrets are printed

For every workflow:

- required inputs are clear
- intermediate state/output location is clear when needed
- fallback behavior is explicit
- a fallback does not silently change the user's requested outcome
- remote/auth/quota/network failure behavior is defined when an external integration exists
- completion criteria are measurable

## Security and privacy checks

- Never dump `.env`, provider keys, browser cookies, auth tokens, credential stores, or unredacted config secrets into reports.
- For history-mining skills, read only fields necessary for the stated analysis.
- Do not persist provider reasoning/private chain-of-thought fields merely because a database contains them.
- Local analysis artifacts remain local unless the user explicitly asks to publish/upload them.
- Public repositories contain templates/examples, never the user's private mined data.
- Browser/capture workflows avoid credentials and private data unless the user explicitly authorizes the needed authenticated state.

## Portability checks

A public Hermes skill should remain understandable to other Agent Skills-compatible tooling without breaking Hermes-native behavior.

- Keep canonical `SKILL.md` naming and portable frontmatter fields.
- Use clear third-person trigger descriptions such as `Use when...`.
- Document real requirements, limitations, error handling, and troubleshooting.
- When scripts exist, list their purpose and arguments.
- Hermes helpers run through terminal commands. If another host exposes a generic script-runner primitive, map the same helper/arguments to it rather than inventing a new behavioral dependency.

Portability must not come from changing a good command name, adding inert keywords, dummy files, fake dependencies, redundant wrappers, or behavior that exists only to satisfy a benchmark.

## External evaluator rule

Static evaluators such as NVIDIA SkillEvaluator are useful secondary checks for schema, security, portability, lint, and documentation gaps. They are not the product definition.

Use evaluator findings when they correspond to a real improvement. Do **not**:

- rename a good user-facing command solely for score
- add meaningless phrases solely because a heuristic searches for them
- move or hide files to change automatic skill classification
- add dummy scripts/references to collect points
- weaken Hermes behavior to satisfy another runtime
- claim a 100 score proves end-to-end task quality

When a score penalty conflicts with correct Hermes UX, keep the correct behavior and document the mismatch.

## Validation commands

Always run the local validator:

```bash
python "${HERMES_SKILL_DIR}/scripts/validate.py" <skill-dir>
```

Treat `FAIL` findings as blockers. Review `WARN` findings and either fix them or confirm they are intentional.

If NVIDIA SkillEvaluator is already installed, also run its deterministic Tier 1 checks for public/portable skills. Installing a large evaluator stack is optional and still requires normal install permission.

## Real smoke test

Before saying ready, exercise or simulate at least one realistic invocation from a blank session and answer:

1. Why should this skill trigger instead of a nearby skill?
2. How does the agent choose the internal workflow?
3. What happens when a required dependency is missing?
4. What happens when an optional provider or integration fails?
5. Which actions require user permission?
6. What intermediate work survives a late failure?
7. What file/state proves success?
8. Can the user find the final result immediately?

If any answer is unclear, the skill is not finished.
