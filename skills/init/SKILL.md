---
name: init
description: Personalized Hermes capability bootstrapper. Mines the user's real local Hermes history and installed environment, finds repeated workflows and friction, then designs and optionally builds the highest-leverage tailor-made domain skills.
version: 0.1.0
author: skellymeow
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [onboarding, personalization, skill-mining, skill-creator, history, state-db]
---

# /init

You are the user's capability architect. Your job is to learn how this Hermes installation is actually used, identify repeated work that deserves first-class slash commands, and turn the best opportunities into tailor-made domain skills.

Do **not** ask the user to explain months of past work if Hermes already has the evidence locally.

## What `/init` means

Invoking `/init` explicitly authorizes a **read-only local audit** of Hermes history and non-secret profile/capability metadata for the purpose of recommending skills. It does not authorize uploading history, printing credentials, installing software, changing global configuration, deleting data, or publishing anything.

Read `references/privacy.md` before mining.

## 1. Audit the real Hermes state

Run:

```bash
python "${HERMES_SKILL_DIR}/scripts/audit_hermes.py"
```

The script resolves `$HERMES_HOME` or `~/.hermes`, reads `state.db` in SQLite read-only mode, and writes a sanitized private audit under:

```text
$HERMES_HOME/init-audit/<timestamp>/
```

It intentionally exports only visible conversation content and useful metadata. It excludes provider reasoning/private chain-of-thought fields, API wire payloads, tool-call arguments, system prompts, model configuration blobs, and secret-bearing config contents.

If `state.db` does not exist, say exactly that and fall back to available profile/installed-skill evidence. Do not invent history.

## 2. Read all audit chunks

Start with:

- `inventory.md`
- `manifest.json`
- `profile.md` when present
- `installed-skills.json`

Then process **every file listed in `manifest.json` under `chunks`**. Do not sample only the newest sessions unless the user explicitly requested a limited scan.

For very large histories, process chunks sequentially and persist compact evidence notes under the private audit directory so context limits do not cause you to forget earlier evidence.

For each chunk extract only evidence relevant to reusable capabilities:

- repeated deliverables the user asks for
- repeated multi-step workflows
- recurring setup/configuration work
- tools/services repeatedly combined together
- repeated corrections or dissatisfaction
- places where the user repeatedly has to explain the same preference/process
- jobs that currently require several prompts but could become one command
- deterministic operations that should become helper scripts
- existing skills that already solve the problem and should be improved instead of duplicated

Never mine intimate/private details merely because they exist. The purpose is workflow automation.

Read `references/mining.md` for the scoring system.

## 3. Turn history into capability domains

Cluster related jobs into **domain-level commands**, not micro-skills.

Examples:

```text
many requests about short-form production -> /video
research + cited article + images + publish -> /blog
repo audit + screenshots + release copy -> /release
prospecting + verification + outreach state -> /outreach
```

One command may contain many internal workflows.

Compare candidate domains against the installed skill inventory. Prefer:

1. improving an existing domain skill
2. extending it with another internal route
3. creating a new domain skill only when the capability is genuinely distinct

## 4. Rank opportunities

Create `skill-opportunities.md` in the private audit directory with evidence-backed candidates.

For each candidate include:

- proposed `/command`
- one-sentence finished outcome
- evidence: number of distinct sessions + representative sanitized examples
- current friction
- workflows it would contain
- deterministic helpers it likely needs
- existing capability overlap
- score /100
- expected payoff in plain language

Present the **top 3-5** to the user. Keep the presentation compact.

### Default behavior

`/init` -> audit + recommend, then ask which recommended skills to build.

`/init auto` -> audit + build the top **3 non-overlapping candidates** automatically after the audit. This explicit `auto` mode is permission to create/update local skill files, but still does not authorize software installs, spending, destructive actions, publishing, or credential changes.

## 5. Build approved skills with the shared formula

Use the `/skill` architecture formula when available at:

```text
$HERMES_HOME/skills/skill/references/formula.md
```

and its validator at:

```text
$HERMES_HOME/skills/skill/scripts/validate.py
```

If `/skill` is not installed, do not silently install it. Use the core rules below and offer the exact install command afterward.

Core rules:

- one coherent domain slash command
- small `SKILL.md` router
- progressive-disclosure references
- deterministic scripts only where they add reliability
- free/local baseline where practical
- provider/tool reuse before new dependencies
- permission before installs/spend/destructive/external side effects
- objective QA and finished deliverable/state
- no hardcoded secrets

When writing a new local skill, default destination is:

```text
$HERMES_HOME/skills/<command>/
```

Do not publish the user's private skill or mined history unless explicitly asked.

## 6. Validate every built skill

If the `/skill` validator exists, run it against every created/modified skill. Otherwise perform the same static checks manually.

A built skill is not ready until:

- all referenced files exist
- syntax checks pass for helper scripts when tooling exists
- setup/fallback paths are coherent
- consequential side effects are permission-gated
- success has observable proof
- no mined private content or credentials were copied into reusable public instructions

## 7. Deliver the result

Return:

1. audit totals: sessions/messages/time span scanned
2. top capability opportunities
3. skills created/updated, if any
4. validation result for each
5. exact commands to test, e.g. `/video`, `/blog`

Do not dump the raw history back into chat. The useful output is the capability system learned from it.