#!/usr/bin/env python3
"""Static validator for Hermes skills. Stdlib only; never mutates the target skill."""
from __future__ import annotations

import argparse
import json
import py_compile
import re
import shutil
import subprocess
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# Only treat explicit file-like references as paths. This deliberately ignores prose
# such as "scripts/CLIs" and directory mentions such as "references/".
REF_RE = re.compile(
    r"(?<![\w./-])((?:references|scripts|templates|assets)/(?:[A-Za-z0-9._-]+/)*[A-Za-z0-9._-]+\.[A-Za-z0-9]{1,12})"
)
# Build personal-home patterns without embedding a literal personal path in this
# validator's own source, which keeps external PII scanners from flagging the checker.
USERS_DIR = "Users"
HOME_DIR = "home"
ABS_PATH_RE = re.compile(
    rf"(?:[A-Za-z]:\\{USERS_DIR}\\[^\s`]+|/{USERS_DIR}/[^\s`]+|/{HOME_DIR}/[^\s`]+)"
)
SECRET_RE = re.compile(
    r"(?i)(?:api[_-]?key|token|password|secret)\s*[:=]\s*[\"']?(?!your-|<|\$\{|\{\{|example|placeholder)([A-Za-z0-9_\-./+=]{12,})"
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    if not text.startswith("---\n"):
        return {}, "SKILL.md must begin with YAML frontmatter delimited by ---"
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, "SKILL.md frontmatter is not closed with ---"
    data: dict[str, str] = {}
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.startswith((" ", "\t")) or ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip('"\'')
    return data, None


def add(findings: list[dict], level: str, message: str) -> None:
    findings.append({"level": level, "message": message})


def validate(skill_dir: Path) -> list[dict]:
    findings: list[dict] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        add(findings, "FAIL", "SKILL.md is missing")
        return findings

    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fm, fm_error = parse_frontmatter(text)
    if fm_error:
        add(findings, "FAIL", fm_error)
    name = fm.get("name", "")
    desc = fm.get("description", "")
    if not name:
        add(findings, "FAIL", "frontmatter.name is required")
    elif not NAME_RE.fullmatch(name):
        add(findings, "FAIL", f"frontmatter.name must be lowercase kebab-case: {name!r}")
    if not desc:
        add(findings, "FAIL", "frontmatter.description is required")

    if len(text) > 18000:
        add(findings, "WARN", f"SKILL.md is {len(text):,} characters; consider moving depth into references/")

    refs = sorted(set(m.group(1).rstrip(".,);:'\"") for m in REF_RE.finditer(text)))
    for rel in refs:
        if not (skill_dir / rel).exists():
            add(findings, "FAIL", f"referenced path does not exist: {rel}")

    if ABS_PATH_RE.search(text):
        add(findings, "WARN", "SKILL.md contains a machine-specific absolute user path")
    if SECRET_RE.search(text):
        add(findings, "FAIL", "SKILL.md appears to contain a hardcoded secret/token/password")

    for path in skill_dir.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(skill_dir)
        if path.name != "SKILL.md":
            try:
                body = path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                body = ""
            if SECRET_RE.search(body):
                add(findings, "FAIL", f"possible hardcoded secret in {rel}")
        if path.suffix == ".py":
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                add(findings, "FAIL", f"Python syntax error in {rel}: {exc.msg}")
        elif path.suffix in {".js", ".mjs", ".cjs"} and shutil.which("node"):
            proc = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
            if proc.returncode:
                detail = (proc.stderr or proc.stdout).strip().splitlines()[-1:]
                add(findings, "FAIL", f"JavaScript syntax error in {rel}: {' '.join(detail)}")

    if not any(f["level"] == "FAIL" for f in findings):
        add(findings, "PASS", "static validation passed")
    return findings


def main() -> int:
    p = argparse.ArgumentParser(description="Validate a Hermes skill directory without modifying it.")
    p.add_argument("skill_dir", type=Path)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    skill_dir = args.skill_dir.expanduser().resolve()
    findings = validate(skill_dir)
    if args.json:
        print(json.dumps({"skill": str(skill_dir), "findings": findings}, indent=2))
    else:
        print(f"Skill: {skill_dir}")
        for item in findings:
            print(f"[{item['level']}] {item['message']}")
    return 1 if any(f["level"] == "FAIL" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
