# Hermes skill formula

Use this to turn a capability idea into the smallest reliable system that still feels powerful.

## 1. Start from the finished outcome

Write one sentence:

> After this skill runs successfully, the user has ______.

Examples:
- `/video` -> a verified MP4 plus editable production files.
- `/blog` -> a publish-ready article with citations, sourced media, metadata, and provenance.
- `/outreach` -> vetted prospects, evidence, approved copy, and a tracked outreach state.

If the outcome is vague, the skill will become vague.

## 2. One domain, many internal routes

Prefer one memorable command for a coherent domain. Route internally based on intent.

Good:

```text
/video
  -> product promo
  -> explainer
  -> reference-inspired
  -> clip repurpose
```

Avoid exposing every internal workflow as another slash command unless it is genuinely a separate domain.

## 3. Put intelligence in Markdown, determinism in code

### Skill / reference Markdown
Use for:
- deciding what the user means
- workflow selection
- creative direction
- tool/provider choice
- research strategy
- quality judgment
- recovery/fallback policy
- onboarding

### Script / CLI
Use for:
- machine inspection
- database parsing
- file transforms
- media encoding
- browser capture
- schema validation
- link checks
- deterministic export/import
- repetitive operations where an LLM could make avoidable mistakes

A script should have clear inputs, clear outputs, useful errors, and no hidden side effects.

## 4. MCP is not the default

Use an MCP/API boundary only when the capability needs a real external callable service, such as:
- remote database/search service
- CMS/project-management service
- authenticated API surface
- structured external resources shared across agents
- persistent service process that provides tools

Do not wrap a simple local script in MCP merely because MCP exists.

## 5. Native Hermes code is the last layer

Use native Hermes changes for things such as deep runtime behavior, gateway internals, streaming primitives, scheduler/runtime capabilities, or functionality that cannot be expressed cleanly through a skill plus existing tools.

## 6. Progressive disclosure

Keep `SKILL.md` compact enough to act as a router. Detailed knowledge belongs in references.

A useful split:

```text
SKILL.md
  identity
  routing
  preflight
  hard rules
  completion contract

references/onboarding.md
  first-run choices

references/workflows.md
  domain playbooks

references/setup.md
  dependencies/providers

references/quality.md
  objective review gate
```

Add more references only when the domain actually needs them.

## 7. Onboarding is conditional

Onboarding exists to resolve choices that materially affect the result. It is not a questionnaire.

Rules:
- Never ask for information already present in the user's request.
- Inspect the environment instead of asking whether tools are installed.
- Give a recommended default.
- Ask permission before installing software or changing configuration.
- Ask permission before spending money or using paid APIs.
- A user with a fully specified request should be able to bypass onboarding entirely.

## 8. Free-first, provider-agnostic

When practical:
1. user-owned/local resources
2. free/local/open-source path
3. free-tier external provider
4. paid provider only as an optional upgrade

Never state that a service, asset, model, or API is free/commercially reusable without evidence.

The skill should use capabilities already available to the agent before demanding another dependency.

## 9. Side effects require explicit gates

Ask before:
- installing packages/software
- modifying global config
- deleting/overwriting data
- spending money
- publishing content
- sending messages/emails
- deploying externally
- creating paid generation jobs

Read-only discovery can normally run automatically.

## 10. Workspace contract

For artifact-producing skills, use an explicit output directory and predictable structure. Keep inputs, intermediate artifacts, provenance, and final deliverables separate.

Example:

```text
output/<slug>/
  brief.md
  sources.json
  work/
  final/
  qa.json
```

This makes runs resumable and auditable.

## 11. Completion gates

A skill must define observable proof.

Weak:
> Generate the video.

Strong:
> `final.mp4` exists, ffprobe validates it, dimensions match the requested aspect, audio/captions pass checks, representative frames were inspected, and media provenance is recorded.

The gate should match the actual product promise.

## 12. Graceful degradation

Optional providers must never silently become mandatory.

If a preferred path is unavailable:
1. state what is missing
2. distinguish required vs optional
3. select the documented free/local fallback when equivalent enough
4. ask before any materially different or paid substitute

## 13. Evidence over invention

Before depending on a package, CLI, API, model, repository, or licensing claim:
- verify it exists
- verify the current install/use contract
- verify auth/cost/license claims that matter
- pin important behavior in the skill reference when it is likely to drift

## 14. Test the user experience

Before shipping, simulate:
- vague first run: `/video`
- specific run: `/video make a 30s 9:16 promo for this app`
- missing dependency
- optional paid provider unavailable
- malformed input
- interrupted run / partial output when relevant

The best skill makes the happy path almost invisible while giving failures explicit recovery.