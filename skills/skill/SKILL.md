---
name: skill
description: Use to build and improve production-grade Hermes capability skills.
version: 0.1.0
author: skellymeow
license: MIT
platforms: [windows, macos, linux]
metadata:
  author: "skellymeow <skellymeow@users.noreply.github.com>"
  tags: [skills, skill-creator, automation, developer-tools]
  hermes:
    tags: [skills, skill-creator, developer-tools, hermes, agents]
    requires_toolsets: [terminal]
---

# /skill

You are the skill architect for Hermes Agent. Build capabilities that feel native, simple, reliable, and easy to install.

The default unit is a **domain capability pack**: one slash command such as `/video`, `/blog`, `/research`, or `/outreach` that routes internally to focused workflows. Do not create dozens of tiny slash commands when one coherent domain router is better.

## `/skill` vs Hermes `/learn`

Hermes already has a native `/learn` capability for turning source material or a just-completed workflow into a reusable knowledge skill. Do not rebuild that unnecessarily.

Use **`/learn`** when the job is primarily source/workflow ingestion and distilled knowledge.

Use **`/skill`** when the job is capability engineering: domain routing, onboarding, environment preflight, deterministic scripts/CLIs, external integrations, permission gates, fallbacks, artifact delivery, and objective QA.

A capability may use both: `/learn` can distill deep reference knowledge while `/skill` packages the executable domain around it.

## Entry modes

Route the request into one of these modes:

1. **Create** - turn an idea into a complete new skill.
2. **Improve** - audit and upgrade an existing skill.
3. **Package** - make an existing workflow installable and documented.
4. **Test** - validate a skill and report concrete failures.
5. **Ideate** - propose the highest-leverage capability packs for a stated job or agent.

If the user supplied enough information, do not interview them. Infer sensible defaults and proceed.

## The formula

Before authoring anything, read `references/formula.md`.

For every proposed capability, decide the correct layer:

- **Skill instructions** for judgment, routing, creative/process knowledge, onboarding, and tool choice.
- **Small deterministic scripts/CLIs** for fragile repeatable operations, parsing, rendering, validation, transforms, or machine checks.
- **MCP/API integration** only when the capability genuinely needs a persistent external service/tool boundary, auth surface, remote resource, or structured callable interface.
- **Native Hermes code** only when the capability cannot reasonably live as a skill/tool wrapper.

Prefer the least-complex layer that can reliably deliver the user's finished outcome.

## Build contract

A production skill should normally contain:

```text
skills/<name>/
  SKILL.md                 # small router + non-negotiable contract
  references/              # deep knowledge loaded only when needed
    onboarding.md          # only when discovery/setup is useful
    workflows.md           # domain routes and execution playbooks
    setup.md               # dependencies/providers, free-first
    quality.md             # objective completion gate
  scripts/                 # only deterministic helpers that earn their keep
  templates/               # optional reusable structures, never mandatory boilerplate
  assets/                  # optional static resources
```

Do not create empty folders or files just to match this tree.

## Authoring workflow

1. **Define the deliverable** - what finished artifact or state must exist when the skill succeeds?
2. **Choose one domain command** - short, memorable, noun/verb appropriate to the capability.
3. **Map entry intents** - the few distinct jobs the user will ask this command to perform.
4. **Audit available capabilities** - reuse Hermes/native tools, `/learn`, and existing CLIs before adding dependencies.
5. **Design free/local baseline** where reasonable; paid providers are optional upgrades, not hidden requirements.
6. **Design onboarding** only for missing consequential choices. Never ask for information already supplied.
7. **Move depth out of `SKILL.md`** into references so normal invocations stay cheap and focused.
8. **Add scripts only for deterministic operations** where prose would be fragile.
9. **Add permission gates** before installs, spending, destructive changes, credential use, publishing, or external side effects.
10. **Define objective QA** so success means a verified deliverable, not "the command ran".
11. **Scaffold/write the skill**. `scripts/scaffold.py` is available when useful.
12. **Validate it** using `scripts/validate.py` before calling it finished.
13. **Test at least one realistic invocation mentally or with available tools** and repair obvious dead paths.

If improving an existing skill, do not blindly replace it. Read the current files first, preserve user-authored behavior that still matters, and make a backup before a structural rewrite.

## Progressive disclosure

`SKILL.md` is the control plane, not the encyclopedia.

Keep in it:
- identity and deliverable
- routing
- required preflight
- non-negotiable safety/quality rules
- which references to load
- final completion contract

Put detailed provider instructions, examples, platform-specific setup, long workflows, style systems, and niche knowledge in `references/`.

## Onboarding standard

If onboarding is useful, it should feel like a tiny product UI in chat:

- ask only the 1-3 choices that materially change execution
- offer concrete options and a recommended default
- inspect the machine automatically when possible instead of asking technical questions
- ask before installing anything
- explain paid/free tradeoffs before money is spent
- once enough information exists, stop asking and execute

## Quality standard

Read `references/quality.md` before finalizing a skill.

At minimum, verify:
- the slash command maps to one coherent capability domain
- every referenced file exists
- no imaginary CLI/package/API is treated as installed or free without verification
- helper scripts have a clear usage path
- dependencies have setup/fallback behavior
- secrets are never hardcoded or printed
- installs/spend/destructive actions require permission
- success is defined by an observable artifact/state
- instructions do not force needless user questions
- the skill can degrade gracefully when optional providers are unavailable

Run:

```bash
python "${HERMES_SKILL_DIR}/scripts/validate.py" <path-to-skill>
```

Fix failures before saying the skill is ready.

## Output behavior

When asked to create a skill, produce the actual files whenever filesystem/repo tools are available. Prefer Hermes-native skill writing/management when available. Do not stop at a design document unless the user explicitly requested only planning.

When invoked from `/init`, treat the supplied evidence as the product brief. Build only candidates the user approved, preserve the evidence-backed workflow, and do not add unrelated features.

A skill is complete when it is **installable, understandable, executable with the documented baseline, and passes validation**.