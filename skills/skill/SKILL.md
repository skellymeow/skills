---
name: skill
description: Use when creating, improving, packaging, or testing a Hermes skill that must be simple, installable, and verifiable.
version: 0.2.0
author: skellymeow
license: MIT
platforms: [windows, macos, linux]
metadata:
  author: "skellymeow <user@example.com>"
  tags: [skills, skill-creator, automation, developer-tools]
  hermes:
    tags: [skills, skill-creator, developer-tools, hermes, agents]
    requires_toolsets: [terminal]
---

# /skill

## Purpose

`/skill` turns a capability idea or existing workflow into a production-ready Hermes skill with the least complexity needed to deliver the outcome reliably. It also audits and improves existing skills without erasing useful behavior.

The default unit is a **domain capability pack**: one memorable slash command such as `/video`, `/blog`, `/research`, or `/outreach` with a few internal routes. Do not create dozens of tiny commands when one coherent domain skill is easier to use and maintain.

## Requirements

- Hermes access to the target skill files and terminal/file tools.
- Python 3 for the included scaffolder and local validator.
- No API key, MCP server, package install, or network access is required to create a normal instruction-based skill.
- External services are requirements only when the capability itself genuinely needs them. Document and permission-gate those dependencies instead of assuming them.

## Instructions

### 1. Choose the right mode

Route the request into one mode:

1. **Create** - turn an idea into a complete new skill.
2. **Improve** - read an existing skill, preserve useful behavior, and repair concrete weaknesses.
3. **Package** - make an existing workflow installable and documented.
4. **Test** - validate a skill and report exact failures with proof.
5. **Ideate** - propose the highest-value capability packs for a stated job or agent.

If the user already supplied enough information, do not interview them again. Infer safe defaults and proceed.

### 2. Check `/learn` before rebuilding it

Hermes `/learn` is appropriate when the job is mainly turning source material or a completed workflow into reusable knowledge.

Use `/skill` when the job needs capability engineering: routing, onboarding, environment checks, deterministic helpers, external integrations, permission gates, fallbacks, artifact delivery, and objective QA.

A capability may use both. `/learn` can distill deep knowledge while `/skill` packages the executable workflow around it.

### 3. Read the architecture formula

Before designing or materially rewriting a skill, read `references/formula.md`.

Choose the least-complex layer that reliably delivers the promised result:

- **Skill instructions** for judgment, routing, process knowledge, onboarding, and tool choice.
- **Small deterministic scripts/CLIs** for fragile repeatable operations, parsing, rendering, validation, or transforms.
- **MCP/API integration** only when the capability needs a real external service boundary, structured remote resource, auth surface, or callable interface.
- **Native Hermes code** only when the capability cannot reasonably live as a skill/tool wrapper.

Do not invent dependencies just to make a skill look sophisticated.

### 4. Define the contract before writing files

Write down four things internally before implementation:

- **Trigger:** when this skill should be used, including obvious non-use cases when ambiguity exists.
- **Deliverable:** the artifact or state that must exist when the command succeeds.
- **Inputs:** only the choices/data that materially affect execution.
- **Proof:** objective checks that demonstrate success.

Then choose one short domain command and map the few distinct user intents it needs to handle.

### 5. Build with progressive disclosure

A production skill normally looks like:

```text
skills/<name>/
  SKILL.md
  references/
    onboarding.md      # only when missing choices matter
    workflows.md       # domain routes and execution playbooks
    setup.md           # real dependencies/providers/fallbacks
    quality.md         # objective completion gate
  scripts/             # only deterministic helpers that earn their keep
  templates/           # optional reusable structures
  assets/              # optional static resources
```

Do not create empty folders or boilerplate files merely to match the tree.

Keep `SKILL.md` as the control plane:

- purpose and trigger
- routing
- required preflight
- permission/safety rules
- references to load
- helper invocation
- completion contract

Move detailed provider instructions, examples, platform-specific setup, long workflows, style systems, and niche knowledge into `references/`.

### 6. Add dependencies only when they improve the real outcome

Before adding any package, CLI, API, MCP server, model, or service:

1. check whether Hermes/native tools already solve the operation
2. check whether a small local helper is enough
3. document detection and fallback behavior
4. ask permission before installs, paid calls, publishing, sending, deployment, destructive changes, credential use, or other consequential side effects

Free/local options are good defaults when they are practical, not dogma. Never call an unverified provider free, installed, licensed, or available.

### 7. Make onboarding small

When onboarding is necessary:

- ask only 1-3 choices that materially change execution
- offer concrete options and a recommended default
- inspect the machine automatically instead of asking whether tools are installed
- never re-ask information already supplied
- stop asking once enough information exists and execute

### 8. Implement the skill

For a new skill, `scripts/scaffold.py` can create a minimal starting structure. Replace its placeholders with real domain behavior instead of shipping the scaffold unchanged.

For an existing skill:

- read all files that affect its behavior before rewriting
- preserve user-authored rules that still matter
- prefer targeted structural improvements over wholesale replacement
- make a backup when a local destructive rewrite is necessary

Helper scripts must have a documented invocation path, deterministic inputs/outputs where practical, useful exit codes/errors, and no embedded secrets.

Hermes should execute helpers through terminal commands exactly as documented. On another compatible agent host that exposes a `run_script` execution primitive, the same helper and arguments may be passed to that runner. Do not make `run_script` a Hermes requirement.

### 9. Validate behavior, not just formatting

Read `references/quality.md` before finalizing.

At minimum verify:

- command and description clearly match one domain
- every referenced file exists
- helper syntax passes where tooling exists
- dependencies have detection, setup, and fallback behavior
- secrets are never hardcoded or printed
- consequential side effects require permission
- error paths do not silently claim success
- the skill can degrade gracefully when optional providers are missing
- completion is observable
- at least one realistic invocation has been exercised mentally or with available tools

Run the local validator:

```bash
python "${HERMES_SKILL_DIR}/scripts/validate.py" <path-to-skill>
```

If NVIDIA SkillEvaluator is already installed, its deterministic Tier 1 checks can be used as an additional portability/security check. Do not change useful Hermes behavior merely to satisfy an external heuristic.

### 10. Deliver the actual capability

When filesystem/repo tools are available and the user asked to create or improve a skill, produce the files. Do not stop at a design document unless planning was explicitly requested.

When invoked from `/init`, treat its evidence as the product brief. Build only approved or `auto`-authorized candidates, preserve evidence-backed workflow behavior, and do not add unrelated features.

A skill is complete only when it is **installable, understandable, executable with its documented baseline, and passes its real validation contract**.

## Available Scripts

| Script | Purpose | Arguments |
| --- | --- | --- |
| `scripts/scaffold.py` | Create a minimal domain-skill directory and starter references. | Required `--name`, `--description`; optional `--author`, `--root`; `--force` only for an intentional overwrite. |
| `scripts/validate.py` | Run read-only static checks for frontmatter, referenced paths, obvious secrets, and Python/JavaScript syntax. | Positional `<skill_dir>`; optional `--json`. |

Typical scaffold:

```bash
python "${HERMES_SKILL_DIR}/scripts/scaffold.py" --name blog --description "Use when producing a sourced article and publish-ready package." --author skellymeow
```

Typical validation:

```bash
python "${HERMES_SKILL_DIR}/scripts/validate.py" "$HERMES_HOME/skills/blog"
```

## Examples

**Create a capability**

```text
/skill make me a /blog skill that researches, writes, sources licensed stock images, validates links, and returns a publish-ready folder
```

Expected behavior: choose the minimal architecture, inspect existing tools before adding dependencies, create the actual files, and validate the result.

**Improve without replacement**

```text
/skill improve ~/.hermes/skills/video - keep its existing workflows but make failure handling and QA reliable
```

Expected behavior: read the current files first, identify concrete gaps, preserve useful behavior, patch the skill, and prove validation.

**Test only**

```text
/skill test ~/.hermes/skills/outreach
```

Expected behavior: make no behavioral rewrite unless requested; report exact validation or dead-path failures with remediation.

## Error Handling

- Never claim a dependency, integration, or command works without available proof.
- If scaffolding would overwrite an existing skill, stop unless overwrite was explicitly authorized.
- If validation fails, report the failing path/check and repair it when the user asked for improvement. Do not hide failures behind a successful process exit elsewhere.
- If an external API/MCP integration is optional and unavailable, use the documented local/native fallback when one exists.
- If the required external integration is unavailable, keep the partial artifact reproducible and identify the single missing dependency instead of silently substituting an unrelated service.

## Troubleshooting

| Problem | Likely cause | Response |
| --- | --- | --- |
| Scaffold says the skill already exists | Safe overwrite guard | Read and improve the existing skill, or use `--force` only after explicit overwrite intent. |
| Local validator reports a missing reference | `SKILL.md` names a file that was moved/never created | Fix the path or create the genuinely required file; do not add dummy files. |
| Helper syntax check fails | Broken Python/JavaScript helper | Repair the helper before delivery and rerun validation. |
| A CLI/package is missing | Setup assumed rather than detected | Use native/local fallback or show the smallest required install and ask permission. |
| MCP connection fails | Server not running, endpoint/auth mismatch, timeout, or transient disconnect | Verify configured endpoint/auth without printing secrets, confirm the server is reachable/running, retry only safe transient failures, then use the documented fallback or report the blocker. |
| API authentication fails | Missing/expired key or wrong provider configuration | Do not print the key. Identify the provider/config field, ask the user to repair credentials, and avoid repeated paid/erroring calls. |
| External evaluator disagrees with Hermes behavior | Cross-runtime heuristic mismatch | Preserve correct Hermes behavior, document the portability difference, and only change behavior when it improves the real skill. |

## Limitations

- `/skill` can validate structure and deterministic helpers, but it cannot prove domain output quality without a realistic task or domain-specific QA.
- A generic scaffold is only a starting point. It does not become production-grade until its routes, setup, fallbacks, and quality gate are made domain-specific.
- Optional external evaluators can find portability/security issues but should not replace real end-to-end testing.
- MCP/API integrations can fail outside the skill because of remote outages, permissions, billing, or credential state; the skill must surface those boundaries clearly.

## Completion Contract

A `/skill` job is done only when the promised files exist, the command has a clear trigger and deliverable, dependencies/fallbacks are documented, helper scripts have real invocation paths, consequential actions are permission-gated, failure modes are explicit, and available validation returns observable proof.