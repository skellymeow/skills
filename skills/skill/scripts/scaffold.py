#!/usr/bin/env python3
"""Create a compact, production-oriented Hermes domain skill scaffold using stdlib only."""
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

SKILL_TMPL = """---
name: {name}
description: {description}
version: 0.1.0
author: {author}
license: MIT
platforms: [windows, macos, linux]
metadata:
  author: "{author} <user@example.com>"
  tags: [{tags}]
  hermes:
    tags: [{tags}]
---

# /{name}

## Purpose

Deliver the finished {name} outcome, not merely instructions. Replace this generic sentence with the exact domain promise before publishing the skill.

## Requirements

- List only dependencies actually required by the baseline path.
- State when no API key, network access, paid provider, or install is required.
- Put platform/provider setup detail in `references/setup.md`.

## Instructions

1. Route the request to the closest workflow in `references/workflows.md`.
2. If a consequential choice is genuinely missing, use `references/onboarding.md`; otherwise do not re-ask supplied information.
3. Inspect available tools/dependencies before asking technical questions.
4. Use the simplest reliable path. Prefer existing/native capabilities before adding dependencies.
5. Ask permission before installs, spending, publishing/sending/deploying, destructive changes, credential use, or other consequential side effects.
6. Preserve intermediate work when a late step fails so the run can recover instead of restarting.
7. Before delivery, read `references/quality.md` and verify the promised artifact/state exists and is correct.

## Examples

```text
/{name} complete the requested {name} task and return the finished result
```

Before publishing, replace this generic example with at least one realistic domain request that demonstrates routing and the finished output.

## Error Handling

- Report the exact failed operation and preserve useful intermediate state.
- Never silently substitute a materially different provider/workflow.
- If an optional dependency is unavailable, use the documented fallback when it still satisfies the request.
- Never claim completion when the promised artifact/state is missing or validation failed.

## Troubleshooting

| Problem | Likely cause | Response |
| --- | --- | --- |
| Required dependency is missing | Baseline/setup mismatch | Use an existing fallback or show the smallest required install and ask permission. |
| External service fails | Auth, quota, outage, network, or provider error | Avoid printing secrets, retry only safe transient failures, then use the documented fallback or report the blocker. |
| Final validation fails | Output does not meet the domain quality contract | Repair the failed criterion and rerun validation before delivery. |

## Limitations

- State real boundaries of the domain, environment, providers, and validation.
- Do not promise capabilities that the installed tools cannot prove.

## Completion Contract

The skill is complete only when the requested artifact/state exists, required validation passes, consequential side effects were authorized, and the final result is delivered clearly.
"""

ONBOARDING_TMPL = """# Onboarding

Use this reference only when the request lacks choices that materially affect execution.

- Ask at most 1-3 consequential questions.
- Offer concrete options and a recommended default.
- Inspect the environment instead of asking whether tools are installed.
- Do not re-ask information already supplied.
- Stop asking once enough information exists and execute.
"""

WORKFLOWS_TMPL = """# Workflows

Define the few internal routes owned by this domain. For each route specify:

1. trigger / user intent
2. required inputs
3. execution steps
4. intermediate artifacts/state when useful
5. failure and fallback behavior
6. finished deliverable
7. objective completion proof

Do not create another slash command for every route.
"""

SETUP_TMPL = """# Setup

Document only real required or optional dependencies.

For each dependency include:
- why it is needed
- how to detect it
- exact minimum version only when verified and necessary
- free/local fallback when practical
- install command only after user approval
- credentials, network, and cost notes when relevant
- failure/recovery behavior

Never hardcode secrets or assert pricing/licensing/availability without current verification when those facts can change.
"""

QUALITY_TMPL = """# Quality gate

Replace this file with objective checks for the domain's promised deliverable.

A successful command ends with observable proof, not merely a successful process exit.

Check at least:
- required artifact/state exists
- critical inputs were respected
- required external side effects were authorized
- known failure conditions are absent
- output-specific correctness checks pass
- a human-facing result is actually delivered
"""


def default_root() -> Path:
    hermes_home = os.environ.get("HERMES_HOME")
    return (Path(hermes_home).expanduser() if hermes_home else Path.home() / ".hermes") / "skills"


def normalize_tags(raw: str) -> str:
    tags = []
    for item in raw.split(","):
        tag = item.strip().lower().replace(" ", "-")
        if tag and NAME_RE.fullmatch(tag) and tag not in tags:
            tags.append(tag)
    if not tags:
        tags = ["automation", "hermes"]
    return ", ".join(tags[:5])


def write_new(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description="Scaffold one Hermes domain capability-pack skill.")
    p.add_argument("--name", required=True, help="lowercase kebab-case command name, e.g. blog")
    p.add_argument("--description", required=True, help="concise trigger description, ideally beginning with 'Use when...'")
    p.add_argument("--author", default="unknown")
    p.add_argument("--tags", default="automation,hermes", help="comma-separated portable metadata tags")
    p.add_argument("--root", type=Path, default=None, help="skills root; defaults to $HERMES_HOME/skills or ~/.hermes/skills")
    p.add_argument("--force", action="store_true", help="allow replacing scaffold files")
    args = p.parse_args()

    name = args.name.strip()
    if not NAME_RE.fullmatch(name):
        p.error("--name must be lowercase kebab-case: letters, numbers, single hyphens")

    description = args.description.strip()
    if len(description) < 20:
        p.error("--description should clearly say when the skill is used (minimum 20 characters)")

    root = (args.root.expanduser() if args.root else default_root()).resolve()
    skill_dir = root / name
    if skill_dir.exists() and not args.force:
        p.error(f"skill already exists: {skill_dir} (use --force only if overwrite is intended)")

    template_values = {
        "name": name,
        "description": description,
        "author": args.author.strip() or "unknown",
        "tags": normalize_tags(args.tags),
    }
    files = {
        skill_dir / "SKILL.md": SKILL_TMPL.format(**template_values),
        skill_dir / "references" / "onboarding.md": ONBOARDING_TMPL,
        skill_dir / "references" / "workflows.md": WORKFLOWS_TMPL,
        skill_dir / "references" / "setup.md": SETUP_TMPL,
        skill_dir / "references" / "quality.md": QUALITY_TMPL,
    }
    for path, content in files.items():
        write_new(path, content, args.force)

    print(skill_dir)
    for path in files:
        print(f"  + {path.relative_to(skill_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
