---
name: init
description: Use when a Hermes user wants repeated workflows mined from local history into tailored, reusable skills.
version: 0.2.0
author: skellymeow
license: MIT
platforms: [windows, macos, linux]
metadata:
  author: "skellymeow <user@example.com>"
  tags: [onboarding, personalization, skill-mining, automation]
  hermes:
    tags: [onboarding, personalization, skill-mining, skill-creator, history, state-db]
    requires_toolsets: [terminal]
---

# /init

## Purpose

`/init` learns how this Hermes installation is actually used, finds repeated work worth turning into reusable capabilities, and returns evidence-backed skill opportunities. It should save the user from re-explaining months of workflows.

The default result is a private local audit plus the top 3-5 capability opportunities. `/init auto` may also create or improve the top three non-overlapping local skills after the audit.

## Requirements

- Python 3 with the standard library, including `sqlite3`.
- Read access to `$HERMES_HOME` or `~/.hermes`.
- `state.db` is useful but optional. If it is absent, continue with available profile and installed-skill evidence.
- No API key, network access, paid provider, or software install is required for the baseline audit.

Before mining, read `references/privacy.md`.

## Instructions

### 1. Establish the permission boundary

Invoking `/init` authorizes a **read-only local audit** of Hermes history and non-secret profile/capability metadata only for recommending reusable skills.

It does **not** authorize:

- uploading or publishing history
- printing credentials or secret-bearing configuration
- installing software
- changing global Hermes configuration
- deleting or rewriting user data
- spending money

`/init auto` additionally authorizes creating or updating local skill files. It still does not authorize installs, spending, destructive actions, publishing, credential changes, or other external side effects.

### 2. Produce the sanitized audit

Run the audit helper from the installed skill directory:

```bash
python "${HERMES_SKILL_DIR}/scripts/audit_hermes.py"
```

Hermes should execute helper scripts through its terminal tool. On another compatible agent host that exposes a `run_script` execution primitive, the same script and arguments may be passed to that runner instead. Do not make `run_script` a Hermes requirement.

The helper resolves `$HERMES_HOME` or `~/.hermes`, opens `state.db` in SQLite read-only mode, and writes a private audit under:

```text
$HERMES_HOME/init-audit/<timestamp>/
```

The export intentionally keeps visible conversation content and useful workflow metadata while excluding provider reasoning/private chain-of-thought fields, API wire payloads, tool-call arguments, system prompts, model configuration blobs, and secret-bearing config contents.

If the helper fails, follow **Troubleshooting** below. Never replace missing evidence with guesses.

### 3. Read the complete audit

Start with:

- `inventory.md`
- `manifest.json`
- `profile.md` when present
- `installed-skills.json`

Then process **every file listed in `manifest.json` under `chunks`**. Do not silently sample only recent sessions.

For histories too large for one context window, process chunks sequentially and persist compact evidence notes inside the private audit directory. Each note should preserve the candidate workflow, session count, representative sanitized evidence, and unresolved questions.

Extract only workflow evidence that can improve reusable capabilities:

- repeated deliverables
- repeated multi-step workflows
- recurring setup/configuration work
- tools/services repeatedly combined together
- repeated corrections or dissatisfaction
- preferences/processes the user repeatedly has to restate
- jobs that take several prompts but could become one command
- fragile deterministic operations that deserve helper scripts
- existing skills that should be improved instead of duplicated

Do not mine intimate/private facts merely because they exist. The target is workflow automation.

Read `references/mining.md` before scoring candidates.

### 4. Cluster into capability domains

Prefer one coherent domain command with internal routes instead of many micro-skills.

Examples:

```text
short-form production requests -> /video
research + cited article + images + publish -> /blog
repo audit + screenshots + release copy -> /release
prospecting + verification + outreach state -> /outreach
```

Compare each candidate with `installed-skills.json` and prefer, in order:

1. improve an existing domain skill
2. add an internal workflow to that skill
3. create a new skill only when the capability is genuinely distinct

### 5. Rank opportunities with evidence

Create `skill-opportunities.md` in the private audit directory. For each candidate record:

- proposed `/command`
- finished outcome in one sentence
- number of distinct supporting sessions
- representative sanitized examples
- current friction
- internal workflows
- deterministic helpers likely needed
- overlap with existing capabilities
- score /100 using `references/mining.md`
- expected payoff in plain language

Present only the top 3-5. Distinguish strong evidence from inference.

### 6. Build only when authorized

Default `/init` stops after the audit and recommendations, then asks which skills to build.

`/init auto` builds the top three non-overlapping candidates after ranking them.

When building, use the `/skill` formula when available:

```text
$HERMES_HOME/skills/skill/references/formula.md
```

and validate with:

```text
$HERMES_HOME/skills/skill/scripts/validate.py
```

If `/skill` is missing, do not install it silently. Use these core rules:

- one coherent domain slash command
- small control-plane `SKILL.md`
- detailed knowledge in references
- deterministic scripts only where they improve reliability
- free/local baseline where practical
- reuse existing tools before new dependencies
- permission before installs, spending, destructive actions, or external side effects
- observable QA and a finished artifact/state
- no hardcoded secrets

Default local destination:

```text
$HERMES_HOME/skills/<command>/
```

Never copy mined private conversation content into a reusable public skill.

### 7. Validate and deliver proof

Every created or modified skill must pass the available local validator before it is called ready. If NVIDIA SkillEvaluator is already installed, its deterministic Tier 1 checks may be run as an additional portability/security check; do not install it solely for this run without permission.

Return:

1. sessions/messages/time span scanned
2. top capability opportunities with evidence strength
3. skills created or updated, if authorized
4. validation result for each
5. exact slash commands to test

Do not dump raw history into chat.

## Available Scripts

| Script | Purpose | Arguments |
| --- | --- | --- |
| `scripts/audit_hermes.py` | Create a sanitized, read-only local Hermes audit and chunk visible history for mining. | `--home PATH` optional Hermes home, `--out PATH` optional output directory, `--days N` optional recent-day limit (`0` = all), `--chunk-chars N` approximate chunk size. |

The normal `/init` run uses no arguments so the script discovers Hermes home automatically and audits all available history.

## Examples

**Normal discovery**

```text
/init
```

Expected behavior: produce the private audit, process all manifest chunks, rank the strongest 3-5 skill opportunities, then stop for the user's choice.

**Automatic local build**

```text
/init auto
```

Expected behavior: perform the same evidence pass, then create/update only the top three non-overlapping local skills and validate them.

**Restricted local audit for debugging**

```bash
python "${HERMES_SKILL_DIR}/scripts/audit_hermes.py" --days 30 --out ./init-audit-test
```

Use this only when a limited time window or explicit output path is actually desired.

## Error Handling

- Treat missing files, unreadable rows, unsupported database shapes, and redaction warnings as explicit evidence gaps, not permission to infer content.
- Preserve read-only behavior on the source Hermes state. Never open the database for writes.
- If one audit source is unavailable, continue with the remaining safe sources and label the reduced confidence.
- If a build step fails validation, keep the failed skill local, report the exact failure, and do not claim completion.
- Never expose secrets while diagnosing a failure. Report filenames/field types rather than secret values.

## Troubleshooting

| Problem | Likely cause | Response |
| --- | --- | --- |
| `state.db` is missing | Hermes stores no local DB there or home resolution is wrong | Confirm `$HERMES_HOME`; continue with profile/installed-skill evidence and report that history was unavailable. |
| SQLite cannot be opened | Permission, corruption, or incompatible filesystem state | Do not copy/modify the DB automatically. Report the error and continue with other safe evidence. |
| Audit output directory already exists | An explicit `--out` path was reused | Choose a new output path; never delete the old audit automatically. |
| No history chunks are produced | No visible user/assistant rows matched the safe export | Report zero exported messages and do not fabricate opportunities from absent history. |
| Candidate evidence conflicts | User behavior changed over time or workflows differ by project | Preserve both signals, favor repeated/recent evidence only when justified, and lower confidence rather than forcing one conclusion. |
| `/skill` validator is unavailable | `/skill` is not installed | Perform the core checks manually and offer the install/use path separately. |

## Limitations

- `/init` can only learn from evidence available to the local Hermes installation; deleted, remote-only, encrypted, or inaccessible history cannot be reconstructed.
- Redaction and safe-field filtering intentionally discard some context, so the audit is optimized for workflow discovery rather than exact transcript reproduction.
- Frequency alone does not prove a workflow deserves automation. Ranking must also consider friction, repeatability, value, and existing overlap.
- The skill does not publish, sync, or distribute generated skills unless the user explicitly asks for that separate action.

## Completion Contract

`/init` is complete only when the audit location exists, all listed chunks were accounted for, recommendations cite sanitized evidence counts, overlap with installed skills was checked, confidence/limitations were stated, and every authorized generated skill has an observable validation result.