#!/usr/bin/env python3
"""Technical QA for a rendered video using ffprobe/ffmpeg."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


def run(cmd: list[str], timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)


def probe(path: Path) -> dict[str, Any]:
    p = run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format",
        "-of", "json", str(path),
    ])
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "ffprobe failed")
    return json.loads(p.stdout)


def detect_black(path: Path) -> list[float]:
    p = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-vf", "blackdetect=d=0.75:pix_th=0.98", "-an", "-f", "null", "-",
    ], timeout=120)
    text = (p.stderr or "") + "\n" + (p.stdout or "")
    return [float(x) for x in re.findall(r"black_duration:([0-9.]+)", text)]


def detect_volume(path: Path) -> dict[str, float | None]:
    p = run([
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-vn", "-af", "volumedetect", "-f", "null", "-",
    ], timeout=120)
    text = (p.stderr or "") + "\n" + (p.stdout or "")
    mean = re.search(r"mean_volume:\s*(-?[0-9.]+) dB", text)
    maximum = re.search(r"max_volume:\s*(-?[0-9.]+) dB", text)
    return {
        "mean_db": float(mean.group(1)) if mean else None,
        "max_db": float(maximum.group(1)) if maximum else None,
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--aspect", choices=["9:16", "16:9"])
    p.add_argument("--require-audio", action="store_true")
    p.add_argument("--json", dest="json_out")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    video = Path(args.video).expanduser().resolve()
    if not video.exists() or not video.is_file():
        raise SystemExit(f"Video not found: {video}")
    if video.stat().st_size < 100_000:
        size_warning = "file is unusually small"
    else:
        size_warning = None

    for cmd in ("ffprobe", "ffmpeg"):
        if not shutil.which(cmd):
            raise SystemExit(f"{cmd} is required for QA")

    data = probe(video)
    streams = data.get("streams", [])
    vstreams = [s for s in streams if s.get("codec_type") == "video"]
    astreams = [s for s in streams if s.get("codec_type") == "audio"]
    fmt = data.get("format", {})

    failures: list[str] = []
    warnings: list[str] = []
    if size_warning:
        warnings.append(size_warning)
    if not vstreams:
        failures.append("no video stream")
        width = height = 0
        codec = None
    else:
        v = vstreams[0]
        width = int(v.get("width") or 0)
        height = int(v.get("height") or 0)
        codec = v.get("codec_name")

    duration = float(fmt.get("duration") or 0.0)
    if duration <= 0.5:
        failures.append("invalid/very short duration")

    if args.aspect and width and height:
        actual = width / height
        expected = 9 / 16 if args.aspect == "9:16" else 16 / 9
        if abs(actual - expected) > 0.015:
            failures.append(f"aspect mismatch: {width}x{height} is not {args.aspect}")

        if args.aspect == "9:16":
            if height < 1280:
                failures.append("portrait output is below 720x1280 class resolution")
            elif (width, height) != (1080, 1920):
                warnings.append(f"final target is usually 1080x1920; got {width}x{height}")
        else:
            if width < 1280:
                failures.append("landscape output is below 1280x720 class resolution")
            elif (width, height) != (1920, 1080):
                warnings.append(f"final target is usually 1920x1080; got {width}x{height}")

    if args.require_audio and not astreams:
        failures.append("audio was required but no audio stream exists")

    black_durations = detect_black(video) if vstreams else []
    long_black = [d for d in black_durations if d >= 1.0]
    if long_black:
        warnings.append(f"detected {len(long_black)} black segment(s) >= 1.0s")

    volume = detect_volume(video) if astreams else {"mean_db": None, "max_db": None}
    if astreams and volume["mean_db"] is not None and volume["mean_db"] < -45:
        warnings.append("audio is extremely quiet / possibly unintended silence")
    if astreams and volume["max_db"] is not None and volume["max_db"] >= 0:
        warnings.append("audio peaks at 0 dB; inspect for clipping")

    report = {
        "ok": not failures,
        "file": str(video),
        "size_bytes": video.stat().st_size,
        "duration_seconds": round(duration, 3),
        "video": {
            "width": width,
            "height": height,
            "codec": codec,
            "stream_count": len(vstreams),
        },
        "audio": {
            "present": bool(astreams),
            "stream_count": len(astreams),
            **volume,
        },
        "black_segments_seconds": black_durations,
        "failures": failures,
        "warnings": warnings,
    }

    rendered = json.dumps(report, indent=2)
    print(rendered)
    if args.json_out:
        out = Path(args.json_out).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered + "\n", encoding="utf-8")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
