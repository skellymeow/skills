# skellymeow/skills

High-leverage capability packs for Hermes Agent. The idea is simple: **a few great domain commands, each containing many focused workflows**.

## Recommended first install

```bash
hermes skills tap add skellymeow/skills
hermes skills install skellymeow/skills/init
hermes skills install skellymeow/skills/skill
```

Start a new Hermes session and run:

```text
/init
```

`/init` reads your local Hermes history **read-only**, mines repeated workflows/friction, compares them with installed capabilities, and recommends the highest-leverage tailor-made skills for how you actually use Hermes.

Use:

```text
/init auto
```

to also create/update the top 3 non-overlapping local skill candidates automatically after the audit.

Private history stays under `$HERMES_HOME/init-audit/`. The auditor deliberately excludes provider reasoning/private chain-of-thought fields, API wire payloads, system prompts, model-config blobs, raw tool-call arguments, and secret-bearing config contents.

## Skills

### `/init` - personalized capability bootstrapper

**history → evidence → repeated workflows → ranked capability domains → tailor-made skills**

- reads Hermes `state.db` in SQLite read-only mode
- scans all visible user/assistant history by default
- inventories installed skills and useful profile context
- redacts credential-like strings before writing its private audit corpus
- mines repeated deliverables, setup work, corrections, tool combinations, and failure patterns
- scores candidates by recurrence, friction removed, deterministic leverage, reuse, and setup savings
- avoids duplicating capabilities already covered by an installed domain skill
- can build the approved candidates locally

### `/skill` - high-quality skill creator

Turns an idea or existing workflow into a production-grade Hermes capability pack.

- one coherent domain command instead of micro-skill spam
- progressive-disclosure `SKILL.md` + references
- deterministic helper scripts only where they improve reliability
- decides when something should instead be a CLI/script, MCP/API integration, or native Hermes feature
- free/local baseline when practical
- setup/onboarding and permission gates
- objective completion/QA contract
- built-in scaffolder and static validator

Examples:

```text
/skill make a complete blog publishing capability
/skill improve my existing video skill
/skill audit ~/.hermes/skills/outreach
```

### `/video` - agent-native video production

Install:

```bash
hermes skills install skellymeow/skills/video
```

Then:

```text
/video
```

Handles vertical/landscape production, Playwright product capture, Kokoro narration, faster-whisper captions, HyperFrames composition, FFmpeg rendering, license-aware media sourcing, and final QA.

## Architecture

```text
/init     learns which capabilities you need
   ↓
/skill    knows how to build them properly
   ↓
/video, /blog, /research, /outreach, ...
```

### Formula

- **Skill Markdown** = judgment, routing, workflow knowledge, onboarding, quality rules
- **Script/CLI** = deterministic fragile/repetitive operations
- **MCP/API** = genuine external service/tool boundary
- **Native Hermes** = deep runtime functionality that cannot cleanly live above

## Principles

- One command should expose a capability domain, not dozens of tiny commands.
- Read existing context before asking the user to explain themselves again.
- Free/local paths first; paid providers are optional upgrades.
- Never silently install software, spend money, publish, or perform destructive actions.
- Never hardcode or leak credentials.
- Deliver and verify finished artifacts/state, not merely instructions.

## License

MIT
