#!/usr/bin/env python3
"""Create a sanitized, read-only audit of a Hermes installation for /init."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

PROFILE_NAMES = ("SOUL.md", "USER.md", "MEMORY.md", "MACHINE.md", "AGENTS.md")
SAFE_TOPLEVEL_NAMES = {
    "config.yaml", "config.yml", "settings.json", "team.yaml", "agents-models.yaml",
    "state.db", "state.db-wal", "state.db-shm",
}
MAX_PROFILE_BYTES = 500_000

SECRET_PATTERNS = [
    re.compile(r"(?i)(authorization\s*:\s*bearer\s+)[^\s\"']+"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"(?i)\b([A-Z][A-Z0-9_]*(?:API_?KEY|TOKEN|SECRET|PASSWORD|PASS|CREDENTIAL)[A-Z0-9_]*)\s*([=:])\s*([^\s,;]+)"),
    re.compile(r"(?i)([?&](?:api_?key|token|secret|auth|access_token)=)[^&#\s]+"),
]


def hermes_home_from_env() -> Path:
    raw = os.environ.get("HERMES_HOME")
    return Path(raw).expanduser().resolve() if raw else (Path.home() / ".hermes").resolve()


def redact(text: str) -> str:
    out = text
    for i, pattern in enumerate(SECRET_PATTERNS):
        if i == 0:
            out = pattern.sub(r"\1[REDACTED]", out)
        elif i in {1, 2, 3}:
            out = pattern.sub("[REDACTED_TOKEN]", out)
        elif i == 4:
            out = pattern.sub(r"\1\2[REDACTED]", out)
        else:
            out = pattern.sub(r"\1[REDACTED]", out)
    return out


def safe_path(value: str | None) -> str | None:
    if not value:
        return value
    text = str(value)
    home = str(Path.home())
    if text.startswith(home):
        text = "~" + text[len(home):]
    return redact(text)


def iso_ts(value: float | int | None) -> str | None:
    if value is None:
        return None
    try:
        return dt.datetime.fromtimestamp(float(value), tz=dt.timezone.utc).isoformat()
    except (ValueError, OSError, TypeError):
        return None


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type IN ('table','view') AND name=? LIMIT 1", (name,)
    ).fetchone()
    return bool(row)


def columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})")}


def open_readonly(db_path: Path) -> sqlite3.Connection:
    uri = f"{db_path.as_uri()}?mode=ro"
    conn = sqlite3.connect(uri, uri=True, timeout=2.0)
    conn.row_factory = sqlite3.Row
    return conn


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def read_profile(home: Path) -> tuple[str, list[dict]]:
    sections: list[str] = []
    metadata: list[dict] = []
    candidates = []
    for name in PROFILE_NAMES:
        candidates.extend([home / name, home / "profile" / name])
    seen: set[Path] = set()
    for path in candidates:
        path = path.resolve()
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        stat = path.stat()
        metadata.append({"path": safe_path(str(path)), "size": stat.st_size})
        if stat.st_size > MAX_PROFILE_BYTES:
            sections.append(f"\n## {safe_path(str(path))}\n\n[Skipped: file larger than {MAX_PROFILE_BYTES:,} bytes]\n")
            continue
        try:
            content = redact(path.read_text(encoding="utf-8", errors="replace"))
        except OSError as exc:
            sections.append(f"\n## {safe_path(str(path))}\n\n[Unreadable: {exc}]\n")
            continue
        sections.append(f"\n## {safe_path(str(path))}\n\n{content}\n")
    return "".join(sections).strip() + ("\n" if sections else ""), metadata


def installed_skills(home: Path) -> list[dict]:
    roots = [home / "skills"]
    results: list[dict] = []
    for root in roots:
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir(), key=lambda p: p.name.lower()):
            if not child.is_dir():
                continue
            skill_md = child / "SKILL.md"
            item = {"name": child.name, "path": safe_path(str(child)), "description": None}
            if skill_md.is_file():
                try:
                    text = skill_md.read_text(encoding="utf-8", errors="replace")
                    m_name = re.search(r"(?m)^name:\s*(.+?)\s*$", text)
                    m_desc = re.search(r"(?m)^description:\s*(.+?)\s*$", text)
                    if m_name:
                        item["name"] = m_name.group(1).strip().strip("\"'")
                    if m_desc:
                        item["description"] = redact(m_desc.group(1).strip().strip("\"'"))[:1000]
                except OSError:
                    pass
            results.append(item)
    return results


def safe_home_inventory(home: Path) -> list[dict]:
    items: list[dict] = []
    if not home.exists():
        return items
    for child in sorted(home.iterdir(), key=lambda p: p.name.lower()):
        if child.is_file() and child.name in SAFE_TOPLEVEL_NAMES | set(PROFILE_NAMES):
            try:
                size = child.stat().st_size
            except OSError:
                size = None
            items.append({"path": safe_path(str(child)), "type": "file", "size": size})
        elif child.is_dir() and child.name in {"skills", "profile", "cron", "logs", "cache", "plugins"}:
            try:
                count = sum(1 for _ in child.iterdir())
            except OSError:
                count = None
            items.append({"path": safe_path(str(child)), "type": "dir", "children": count})
    return items


def flush_chunk(out_dir: Path, idx: int, entries: list[str]) -> str:
    name = f"chunks/chunk-{idx:04d}.md"
    path = out_dir / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# Sanitized Hermes history chunk\n\n"
        "Visible user/assistant content only. Credential-like strings have been redacted.\n\n"
        + "\n\n".join(entries)
        + "\n",
        encoding="utf-8",
    )
    return name


def export_db(db_path: Path, out_dir: Path, chunk_chars: int, days: int) -> dict:
    result = {
        "database": safe_path(str(db_path)),
        "sessions": 0,
        "messages": 0,
        "visible_messages_exported": 0,
        "tool_rows": 0,
        "sources": {},
        "models": {},
        "roles": {},
        "time_start": None,
        "time_end": None,
        "chunks": [],
        "warnings": [],
    }
    if not db_path.is_file():
        result["warnings"].append("state.db not found")
        return result

    try:
        conn = open_readonly(db_path)
    except sqlite3.Error as exc:
        result["warnings"].append(f"Could not open state.db read-only: {exc}")
        return result

    with conn:
        if not table_exists(conn, "sessions") or not table_exists(conn, "messages"):
            result["warnings"].append("state.db does not contain expected sessions/messages tables")
            return result

        scols = columns(conn, "sessions")
        mcols = columns(conn, "messages")

        since = None
        if days > 0:
            since = dt.datetime.now(tz=dt.timezone.utc).timestamp() - days * 86400

        where_session = " WHERE started_at >= ?" if since is not None and "started_at" in scols else ""
        params = (since,) if where_session else ()
        result["sessions"] = int(conn.execute(f"SELECT COUNT(*) FROM sessions{where_session}", params).fetchone()[0])

        if "source" in scols:
            for row in conn.execute(
                f"SELECT COALESCE(source,'') AS k, COUNT(*) AS n FROM sessions{where_session} GROUP BY source ORDER BY n DESC",
                params,
            ):
                result["sources"][str(row["k"] or "unknown")] = int(row["n"])
        if "model" in scols:
            for row in conn.execute(
                f"SELECT COALESCE(model,'') AS k, COUNT(*) AS n FROM sessions{where_session} GROUP BY model ORDER BY n DESC",
                params,
            ):
                result["models"][str(row["k"] or "unknown")] = int(row["n"])

        if "started_at" in scols:
            row = conn.execute(
                f"SELECT MIN(started_at) AS lo, MAX(started_at) AS hi FROM sessions{where_session}", params
            ).fetchone()
            result["time_start"], result["time_end"] = iso_ts(row["lo"]), iso_ts(row["hi"])

        join_filter = ""
        qparams: tuple = ()
        if since is not None:
            join_filter = " AND s.started_at >= ?"
            qparams = (since,)

        result["messages"] = int(
            conn.execute(
                "SELECT COUNT(*) FROM messages m JOIN sessions s ON s.id=m.session_id WHERE 1=1" + join_filter,
                qparams,
            ).fetchone()[0]
        )

        if "role" in mcols:
            for row in conn.execute(
                "SELECT COALESCE(m.role,'') AS k, COUNT(*) AS n "
                "FROM messages m JOIN sessions s ON s.id=m.session_id WHERE 1=1"
                + join_filter
                + " GROUP BY m.role ORDER BY n DESC",
                qparams,
            ):
                result["roles"][str(row["k"] or "unknown")] = int(row["n"])

        if "tool_name" in mcols:
            result["tool_rows"] = int(
                conn.execute(
                    "SELECT COUNT(*) FROM messages m JOIN sessions s ON s.id=m.session_id "
                    "WHERE m.tool_name IS NOT NULL AND m.tool_name <> ''" + join_filter,
                    qparams,
                ).fetchone()[0]
            )
            tool_counts = [
                {"tool": str(row["tool_name"]), "count": int(row["n"])}
                for row in conn.execute(
                    "SELECT m.tool_name, COUNT(*) AS n "
                    "FROM messages m JOIN sessions s ON s.id=m.session_id "
                    "WHERE m.tool_name IS NOT NULL AND m.tool_name <> ''"
                    + join_filter
                    + " GROUP BY m.tool_name ORDER BY n DESC LIMIT 200",
                    qparams,
                )
            ]
        else:
            tool_counts = []
        write_json(out_dir / "tool-usage.json", tool_counts)

        session_fields = [
            x for x in ("id", "source", "title", "started_at", "ended_at", "model", "message_count",
                        "tool_call_count", "cwd", "git_branch", "git_repo_root")
            if x in scols
        ]
        if session_fields:
            query = "SELECT " + ",".join(session_fields) + " FROM sessions"
            if where_session:
                query += where_session
            query += " ORDER BY started_at ASC" if "started_at" in scols else ""
            def session_rows():
                for row in conn.execute(query, params):
                    item = dict(row)
                    for key in ("cwd", "git_repo_root"):
                        if key in item:
                            item[key] = safe_path(item[key])
                    if "title" in item and item["title"]:
                        item["title"] = redact(str(item["title"]))[:1000]
                    if "started_at" in item:
                        item["started_at_iso"] = iso_ts(item["started_at"])
                    if "ended_at" in item:
                        item["ended_at_iso"] = iso_ts(item["ended_at"])
                    yield item
            write_jsonl(out_dir / "sessions.jsonl", session_rows())

        select_parts = [
            "m.id AS message_id",
            "m.session_id AS session_id",
            "m.role AS role",
            "m.content AS content",
        ]
        if "timestamp" in mcols:
            select_parts.append("m.timestamp AS timestamp")
        else:
            select_parts.append("NULL AS timestamp")
        for col in ("source", "title"):
            if col in scols:
                select_parts.append(f"s.{col} AS session_{col}")
            else:
                select_parts.append(f"NULL AS session_{col}")

        sql = (
            "SELECT " + ", ".join(select_parts)
            + " FROM messages m JOIN sessions s ON s.id=m.session_id "
            + "WHERE m.role IN ('user','assistant') AND m.content IS NOT NULL"
            + join_filter
            + " ORDER BY m.timestamp ASC, m.id ASC"
        )

        chunks: list[str] = []
        entries: list[str] = []
        current_chars = 0
        idx = 1
        exported = 0
        for row in conn.execute(sql, qparams):
            content = redact(str(row["content"] or "")).strip()
            if not content:
                continue
            meta = {
                "session": str(row["session_id"]),
                "source": row["session_source"],
                "title": redact(str(row["session_title"]))[:300] if row["session_title"] else None,
                "role": row["role"],
                "timestamp": iso_ts(row["timestamp"]),
            }
            header = "### " + json.dumps(meta, ensure_ascii=False)
            entry = header + "\n\n" + content
            if entries and current_chars + len(entry) > chunk_chars:
                chunks.append(flush_chunk(out_dir, idx, entries))
                idx += 1
                entries = []
                current_chars = 0
            entries.append(entry)
            current_chars += len(entry)
            exported += 1
        if entries:
            chunks.append(flush_chunk(out_dir, idx, entries))
        result["chunks"] = chunks
        result["visible_messages_exported"] = exported

    return result


def inventory_markdown(home: Path, db: dict, skills: list[dict], profile_meta: list[dict], home_items: list[dict]) -> str:
    lines = [
        "# Hermes /init audit inventory",
        "",
        f"- Hermes home: `{safe_path(str(home))}`",
        f"- Sessions scanned: **{db.get('sessions', 0)}**",
        f"- DB messages scanned: **{db.get('messages', 0)}**",
        f"- Visible user/assistant messages exported: **{db.get('visible_messages_exported', 0)}**",
        f"- Tool rows observed: **{db.get('tool_rows', 0)}**",
        f"- Time span: **{db.get('time_start') or 'unknown'}** to **{db.get('time_end') or 'unknown'}**",
        f"- History chunks: **{len(db.get('chunks', []))}**",
        f"- Installed skills discovered: **{len(skills)}**",
        "",
        "## Session sources",
        "",
    ]
    for key, count in db.get("sources", {}).items():
        lines.append(f"- {key}: {count}")
    lines += ["", "## Models seen"]
    for key, count in list(db.get("models", {}).items())[:30]:
        lines.append(f"- {key}: {count}")
    lines += ["", "## Installed skills"]
    for skill in skills:
        desc = f" - {skill['description']}" if skill.get("description") else ""
        lines.append(f"- `/{skill['name']}`{desc}")
    lines += ["", "## Profile files"]
    if profile_meta:
        for item in profile_meta:
            lines.append(f"- `{item['path']}` ({item['size']} bytes)")
    else:
        lines.append("- none found")
    lines += ["", "## Safe Hermes-home inventory"]
    for item in home_items:
        lines.append(f"- `{item['path']}` - {item['type']}")
    if db.get("warnings"):
        lines += ["", "## Warnings"]
        lines.extend(f"- {w}" for w in db["warnings"])
    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="Sanitized read-only Hermes history audit for the /init skill.")
    p.add_argument("--home", type=Path, default=None, help="Hermes home; defaults to $HERMES_HOME or ~/.hermes")
    p.add_argument("--out", type=Path, default=None, help="output directory; defaults inside HERMES_HOME/init-audit/")
    p.add_argument("--days", type=int, default=0, help="optional recent-day limit; 0 means all history")
    p.add_argument("--chunk-chars", type=int, default=80_000, help="approximate max characters per history chunk")
    args = p.parse_args()

    home = (args.home.expanduser().resolve() if args.home else hermes_home_from_env())
    if args.out:
        out_dir = args.out.expanduser().resolve()
    else:
        stamp = dt.datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
        out_dir = home / "init-audit" / stamp
    out_dir.mkdir(parents=True, exist_ok=False)

    profile_text, profile_meta = read_profile(home)
    if profile_text:
        (out_dir / "profile.md").write_text(
            "# Sanitized Hermes profile context\n\n" + profile_text, encoding="utf-8"
        )

    skills = installed_skills(home)
    write_json(out_dir / "installed-skills.json", skills)
    home_items = safe_home_inventory(home)
    write_json(out_dir / "hermes-home-inventory.json", home_items)

    db = export_db(home / "state.db", out_dir, max(20_000, args.chunk_chars), max(0, args.days))
    manifest = {
        "version": 1,
        "created_at": dt.datetime.now(tz=dt.timezone.utc).isoformat(),
        "hermes_home": safe_path(str(home)),
        "private_local_audit": True,
        "filters": {
            "days": max(0, args.days),
            "roles": ["user", "assistant"],
            "excluded": [
                "reasoning fields", "api_content", "system prompts", "model_config",
                "tool-call arguments", "secret-bearing config contents",
            ],
        },
        **db,
    }
    write_json(out_dir / "manifest.json", manifest)
    (out_dir / "inventory.md").write_text(
        inventory_markdown(home, db, skills, profile_meta, home_items),
        encoding="utf-8",
    )

    print(str(out_dir))
    print(f"sessions={db.get('sessions', 0)} messages={db.get('messages', 0)} exported={db.get('visible_messages_exported', 0)} chunks={len(db.get('chunks', []))}")
    for warning in db.get("warnings", []):
        print(f"warning: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
