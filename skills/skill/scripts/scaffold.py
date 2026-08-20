#!/usr/bin/env python3
"""Create a minimal Hermes domain capability-pack scaffold using only stdlib."""
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
---

# /{name}

You are the user's {name} capability operator. Deliver the finished outcome, not merely instructions.

## Route

If the request is underspecified, read `references/onboarding.md`. Otherwise choose the closest route from `references/workflows.md` and proceed.

## Preflight

Inspect available tools/dependencies before asking technical questions. Read `references/setup.md` only when setup or provider selection is relevant. Ask permission before installing software, spending money, publishing/sending/deploying, destructive changes, or other consequential side effects.

## Execute

Use the simplest reliable path. Prefer capabilities already available to the agent and free/local options when practical. Use deterministic scripts for fragile repeatable operations and Markdown references for judgment/workflow knowledge.

## Quality gate

Before completion, read `references/quality.md` and verify the promised artifact/state exists and is correct.
"""

ONBOARDING_TMPL = """# Onboarding

Use only when the request lacks choices that materially affect execution.

- Ask at most 1-3 consequential questions.
- Offer concrete options and a recommended default.
- Inspect the environment instead of asking whether tools are installed.
- Do not re-ask information the user already supplied.
- Once enough information exists, execute.
"""

WORKFLOWS_TMPL = """# Workflows

Define the few internal routes owned by this domain. For each route specify:

1. trigger / user intent
2. required inputs
3. execution steps
4. fallback behavior
5. finished deliverable

Do not create another slash command for every route.
"""

SETUP_TMPL = """# Setup

Document only real required/optional dependencies.

For each dependency include:
- why it is needed
- how to detect it
- free/local fallback when practical
- exact install only after user approval
- credentials/cost notes when relevant

Never hardcode secrets or assert pricing/licensing without verification.
"""

QUALITY_TMPL = """# Quality gate

Replace this with objective checks for the domain's promised deliverable.

A successful command should end with observable proof, not simply a successful process exit.
"""


def default_root() -> Path:
    hermes_home = os.environ.get("HERMES_HOME")
    return (Path(hermes_home).expanduser() if hermes_home else Path.home() / ".hermes") / "skills"


def write_new(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description="Scaffold one Hermes domain capability-pack skill.")
    p.add_argument("--name", required=True, help="lowercase kebab-case command name, e.g. blog")
    p.add_argument("--description", required=True)
    p.add_argument("--author", default="unknown")
    p.add_argument("--root", type=Path, default=None, help="skills root; defaults to $HERMES_HOME/skills or ~/.hermes/skills")
    p.add_argument("--force", action="store_true", help="allow replacing scaffold files")
    args = p.parse_args()

    name = args.name.strip()
    if not NAME_RE.fullmatch(name):
        p.error("--name must be lowercase kebab-case: letters, numbers, single hyphens")

    root = (args.root.expanduser() if args.root else default_root()).resolve()
    skill_dir = root / name
    if skill_dir.exists() and not args.force:
        p.error(f"skill already exists: {skill_dir} (use --force only if overwrite is intended)")

    files = {
        skill_dir / "SKILL.md": SKILL_TMPL.format(name=name, description=args.description.strip(), author=args.author.strip()),
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
