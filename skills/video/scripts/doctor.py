#!/usr/bin/env python3
"""Read-only preflight for the /video Hermes skill."""

from __future__ import annotations

import importlib.util
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from typing import Any


def run(cmd: list[str], timeout: int = 8) -> tuple[bool, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        text = (p.stdout or p.stderr or "").strip()
        return p.returncode == 0, text.splitlines()[0] if text else ""
    except Exception as exc:
        return False, str(exc)


def command(name: str, args: list[str] | None = None) -> dict[str, Any]:
    path = shutil.which(name) or (shutil.which(f"{name}.cmd") if os.name == "nt" else None)
    if not path:
        return {"ok": False, "path": None, "version": None}
    ok, version = run([path, *(args or ["--version"])])
    return {"ok": ok, "path": path, "version": version or None}


def python_module(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except Exception:
        return False


def node_package(bin_name: str) -> dict[str, Any]:
    npx = shutil.which("npx") or (shutil.which("npx.cmd") if os.name == "nt" else None)
    if not npx:
        return {"ok": False, "detail": "npx unavailable"}
    ok, detail = run([npx, "--no-install", bin_name, "--version"], timeout=12)
    if not ok:
        ok2, detail2 = run([npx, "--no-install", bin_name, "--help"], timeout=12)
        ok, detail = ok2, detail2 or detail
    return {"ok": ok, "detail": detail or None}


def gpu_info() -> dict[str, Any] | None:
    smi = shutil.which("nvidia-smi")
    if not smi:
        return None
    ok, text = run(
        [
            smi,
            "--query-gpu=name,memory.total,driver_version",
            "--format=csv,noheader,nounits",
        ]
    )
    if not ok:
        return {"detected": True, "detail": text}
    rows = []
    for line in text.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) >= 3:
            rows.append({"name": parts[0], "vram_mb": parts[1], "driver": parts[2]})
    return {"detected": True, "gpus": rows}


def main() -> int:
    ffmpeg = command("ffmpeg")
    ffprobe = command("ffprobe")
    node = command("node")
    npm = command("npm")
    npx = command("npx")
    git = command("git")
    espeak = command("espeak-ng", ["--version"])

    node_major = None
    if node.get("version"):
        match = re.search(r"v?(\d+)", str(node["version"]))
        if match:
            node_major = int(match.group(1))

    report: dict[str, Any] = {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "python": {
            "ok": sys.version_info >= (3, 10),
            "version": platform.python_version(),
            "executable": sys.executable,
        },
        "commands": {
            "ffmpeg": ffmpeg,
            "ffprobe": ffprobe,
            "node": node,
            "npm": npm,
            "npx": npx,
            "git": git,
            "espeak-ng": espeak,
        },
        "node_22_plus": bool(node_major and node_major >= 22),
        "python_modules": {
            "kokoro": python_module("kokoro"),
            "soundfile": python_module("soundfile"),
            "faster_whisper": python_module("faster_whisper"),
        },
        "node_tools_local": {
            "playwright": node_package("playwright"),
            "hyperframes": node_package("hyperframes"),
        },
        "gpu": gpu_info(),
    }

    core_ok = (
        report["python"]["ok"]
        and bool(ffmpeg["ok"])
        and bool(ffprobe["ok"])
        and bool(node["ok"])
        and bool(npx["ok"])
    )
    report["core_ready"] = core_ok

    missing = []
    if not report["python"]["ok"]:
        missing.append("Python 3.10+")
    if not ffmpeg["ok"] or not ffprobe["ok"]:
        missing.append("FFmpeg/ffprobe")
    if not node["ok"] or not npx["ok"]:
        missing.append("Node.js/npx")
    if node["ok"] and not report["node_22_plus"]:
        missing.append("Node.js 22+ recommended for HyperFrames")
    if not report["node_tools_local"]["playwright"]["ok"]:
        missing.append("Playwright (workspace package)")
    if not report["node_tools_local"]["hyperframes"]["ok"]:
        missing.append("HyperFrames (workspace package or npx download)")
    if not report["python_modules"]["kokoro"]:
        missing.append("kokoro Python package")
    if not report["python_modules"]["soundfile"]:
        missing.append("soundfile Python package")
    if not report["python_modules"]["faster_whisper"]:
        missing.append("faster-whisper Python package")
    if not espeak["ok"]:
        missing.append("espeak-ng (needed by common Kokoro setups)")
    report["missing_or_optional"] = missing

    print(json.dumps(report, indent=2))
    return 0 if core_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
