#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "skills" / "skill" / "scripts" / "scaffold.py"
VALIDATE = ROOT / "skills" / "skill" / "scripts" / "validate.py"


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "skills"
        proc = subprocess.run(
            [
                sys.executable,
                str(SCAFFOLD),
                "--name", "test-capability",
                "--description", "A test capability pack",
                "--author", "ci",
                "--root", str(root),
            ],
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, proc.stderr
        skill = root / "test-capability"
        assert (skill / "SKILL.md").is_file()
        assert (skill / "references" / "onboarding.md").is_file()
        assert (skill / "references" / "workflows.md").is_file()
        assert (skill / "references" / "setup.md").is_file()
        assert (skill / "references" / "quality.md").is_file()

        valid = subprocess.run(
            [sys.executable, str(VALIDATE), str(skill)],
            capture_output=True,
            text=True,
        )
        assert valid.returncode == 0, valid.stdout + valid.stderr
        assert "[PASS] static validation passed" in valid.stdout

        # Prove broken references are caught.
        (skill / "references" / "quality.md").unlink()
        invalid = subprocess.run(
            [sys.executable, str(VALIDATE), str(skill)],
            capture_output=True,
            text=True,
        )
        assert invalid.returncode != 0
        assert "referenced path does not exist: references/quality.md" in invalid.stdout

    print("/skill scaffolder + validator functional test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
