#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDITOR = ROOT / "skills" / "init" / "scripts" / "audit_hermes.py"


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        home = Path(td) / ".hermes"
        home.mkdir()
        (home / "MEMORY.md").write_text(
            "Reusable preference. token=abc12345678901234567890", encoding="utf-8"
        )

        conn = sqlite3.connect(home / "state.db")
        conn.executescript(
            """
            CREATE TABLE sessions (
              id TEXT PRIMARY KEY, source TEXT NOT NULL, title TEXT,
              started_at REAL NOT NULL, ended_at REAL, model TEXT,
              message_count INTEGER, tool_call_count INTEGER,
              cwd TEXT, git_branch TEXT, git_repo_root TEXT
            );
            CREATE TABLE messages (
              id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT,
              role TEXT, content TEXT, timestamp REAL, tool_name TEXT,
              reasoning TEXT, api_content TEXT, tool_calls TEXT
            );
            """
        )
        conn.execute(
            "INSERT INTO sessions VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            ("s1", "cli", "Video workflow", 1700000000, 1700000100, "test/model", 3, 1, str(home), "main", str(home)),
        )
        conn.execute(
            "INSERT INTO messages(session_id,role,content,timestamp,reasoning,api_content,tool_calls) VALUES (?,?,?,?,?,?,?)",
            (
                "s1", "user", "Make a promo. API_KEY=supersecret123456789", 1700000001,
                "PRIVATE_REASONING_MUST_NOT_EXPORT", "PRIVATE_WIRE_PAYLOAD",
                '[{"arguments":{"password":"PRIVATE_TOOL_ARG"}}]',
            ),
        )
        conn.execute(
            "INSERT INTO messages(session_id,role,content,timestamp) VALUES (?,?,?,?)",
            ("s1", "assistant", "Finished artifact delivered.", 1700000002),
        )
        conn.execute(
            "INSERT INTO messages(session_id,role,content,timestamp,tool_name) VALUES (?,?,?,?,?)",
            ("s1", "tool", "PRIVATE_TOOL_OUTPUT", 1700000003, "terminal"),
        )
        conn.commit()
        conn.close()

        out = home / "init-audit" / "test"
        proc = subprocess.run(
            [sys.executable, str(AUDITOR), "--home", str(home), "--out", str(out)],
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, proc.stderr

        manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["sessions"] == 1
        assert manifest["messages"] == 3
        assert manifest["visible_messages_exported"] == 2
        assert manifest["tool_rows"] == 1
        assert len(manifest["chunks"]) == 1

        history = (out / manifest["chunks"][0]).read_text(encoding="utf-8")
        profile = (out / "profile.md").read_text(encoding="utf-8")
        combined = history + profile

        assert "Make a promo" in history
        assert "Finished artifact delivered" in history
        assert "supersecret123456789" not in combined
        assert "abc12345678901234567890" not in combined
        assert "PRIVATE_REASONING_MUST_NOT_EXPORT" not in combined
        assert "PRIVATE_WIRE_PAYLOAD" not in combined
        assert "PRIVATE_TOOL_ARG" not in combined
        assert "PRIVATE_TOOL_OUTPUT" not in history
        assert "[REDACTED]" in combined

    print("/init auditor functional test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
