# Skill quality gate

A skill is not ready because its Markdown looks good. It is ready when a Hermes agent can understand it, execute its baseline path, recover from missing optional capabilities, and prove completion.

## Critical checks

Fail the skill if any are true:

- `SKILL.md` is missing valid frontmatter with `name` and `description`.
- The command represents several unrelated domains that should not share one router.
- A referenced file does not exist.
- A required dependency has no setup path.
- An imaginary/unverified package, API, model, CLI, pricing claim, or licensing claim is presented as fact.
- Secrets, API keys, tokens, passwords, private session contents, or machine-specific credentials are hardcoded.
- The skill can install software, spend money, publish, send, deploy, delete, overwrite, or make another consequential side effect without an explicit permission gate.
- The skill says work is complete without observable proof.
- The only output is instructions when the skill promises a finished artifact and execution tools are available.

## Architecture checks

Pass when:

- one memorable slash command owns one coherent domain
- internal workflows are routed instead of exposed as needless micro-skills
- `SKILL.md` behaves like a control plane
- deep/niche details live in `references/`
- scripts are used only where determinism adds real value
- MCP/native integration is justified rather than fashionable
- optional providers remain optional
- free/local baseline is used where practical

## UX checks

Pass when:

- specific requests bypass unnecessary onboarding
- vague requests get a compact menu, not an interrogation
- the agent recommends a default when presenting choices
- the machine is inspected automatically when possible
- users are not expected to know implementation jargon
- missing dependencies produce exact recovery instructions
- no question is asked twice

## Reliability checks

For every helper script:

- usage is documented or discoverable via `--help`
- paths are cross-platform or intentionally documented
- outputs are deterministic enough for downstream steps
- errors are non-zero and explain the failure
- destructive behavior is opt-in
- no secrets are printed

For every workflow:

- required inputs are clear
- intermediate state/output location is clear when needed
- fallback behavior is explicit
- completion criteria are measurable

## Security/privacy checks

- Never dump `.env`, provider keys, browser cookies, auth tokens, credential stores, or unredacted config secrets into reports.
- For history-mining skills, read only fields necessary for the stated analysis.
- Do not persist provider reasoning/private chain-of-thought fields just because a database contains them.
- Local analysis artifacts should remain local unless the user explicitly asks to publish/upload them.
- Public repositories must contain templates/examples, never the user's private mined data.

## Validation command

Run:

```bash
python "${HERMES_SKILL_DIR}/scripts/validate.py" <skill-dir>
```

Treat `FAIL` findings as blockers. Review `WARN` findings and either fix them or ensure they are intentional.

## Final smoke test

Before saying ready, simulate one realistic invocation from a blank session and answer:

1. How does the agent know what workflow to choose?
2. What happens when the machine is missing a dependency?
3. What is the cheapest viable path?
4. What requires user permission?
5. What file/state proves success?
6. What happens when an optional provider fails?

If any answer is unclear, the skill is not finished.