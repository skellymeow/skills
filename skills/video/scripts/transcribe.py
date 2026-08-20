#!/usr/bin/env python3
"""Create local SRT + word timing JSON with faster-whisper."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def ts(seconds: float) -> str:
    ms = max(0, int(round(seconds * 1000)))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, milli = divmod(rem, 1000)
    return f"{h:02}:{m:02}:{s:02},{milli:03}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--srt", required=True)
    p.add_argument("--json", dest="json_out")
    p.add_argument("--model", default="small", help="faster-whisper model name; downloads on first use")
    p.add_argument("--language")
    p.add_argument("--device", default="auto")
    args = p.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise SystemExit(
            "Missing faster-whisper. After user approval run: python -m pip install faster-whisper"
        ) from exc

    source = Path(args.input).expanduser().resolve()
    if not source.exists():
        raise SystemExit(f"Input not found: {source}")

    if args.device == "auto":
        try:
            model = WhisperModel(args.model, device="cuda", compute_type="float16")
        except Exception:
            model = WhisperModel(args.model, device="cpu", compute_type="int8")
    else:
        compute = "float16" if args.device == "cuda" else "int8"
        model = WhisperModel(args.model, device=args.device, compute_type=compute)

    segments_iter, info = model.transcribe(
        str(source),
        language=args.language,
        word_timestamps=True,
        vad_filter=True,
    )
    segments = list(segments_iter)

    srt_lines: list[str] = []
    words: list[dict] = []
    for idx, seg in enumerate(segments, start=1):
        text = (seg.text or "").strip()
        if text:
            srt_lines.extend([str(idx), f"{ts(seg.start)} --> {ts(seg.end)}", text, ""])
        for w in seg.words or []:
            words.append({
                "word": (w.word or "").strip(),
                "start": round(float(w.start), 3),
                "end": round(float(w.end), 3),
                "probability": round(float(w.probability), 4) if w.probability is not None else None,
            })

    srt = Path(args.srt).expanduser().resolve()
    srt.parent.mkdir(parents=True, exist_ok=True)
    srt.write_text("\n".join(srt_lines), encoding="utf-8")

    payload = {
        "input": str(source),
        "model": args.model,
        "language": getattr(info, "language", args.language),
        "language_probability": getattr(info, "language_probability", None),
        "words": words,
    }
    if args.json_out:
        jout = Path(args.json_out).expanduser().resolve()
        jout.parent.mkdir(parents=True, exist_ok=True)
        jout.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"srt": str(srt), "word_count": len(words), "language": payload["language"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
