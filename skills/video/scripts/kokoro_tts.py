#!/usr/bin/env python3
"""Generate local narration with Kokoro and save a WAV file."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    source = p.add_mutually_exclusive_group(required=True)
    source.add_argument("--text")
    source.add_argument("--text-file")
    p.add_argument("--out", required=True)
    p.add_argument("--voice", default="af_heart")
    p.add_argument("--lang", default="a", help="Kokoro language code; 'a' is American English")
    p.add_argument("--speed", type=float, default=1.0)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        import numpy as np
        import soundfile as sf
        from kokoro import KPipeline
    except ImportError as exc:
        raise SystemExit(
            "Missing local TTS dependencies. After user approval run: "
            "python -m pip install kokoro soundfile"
        ) from exc

    text = args.text if args.text is not None else Path(args.text_file).read_text(encoding="utf-8")
    text = text.strip()
    if not text:
        raise SystemExit("Narration text is empty")
    if args.speed <= 0:
        raise SystemExit("--speed must be greater than zero")

    pipeline = KPipeline(lang_code=args.lang)
    pieces = []
    for _graphemes, _phonemes, audio in pipeline(text, voice=args.voice, speed=args.speed):
        if hasattr(audio, "detach"):
            audio = audio.detach().cpu().numpy()
        pieces.append(np.asarray(audio, dtype=np.float32).reshape(-1))

    if not pieces:
        raise SystemExit("Kokoro produced no audio")

    waveform = np.concatenate(pieces)
    peak = float(np.max(np.abs(waveform))) if waveform.size else 0.0
    if peak > 1.0:
        waveform = waveform / peak * 0.98

    out = Path(args.out).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(out, waveform, 24000, subtype="PCM_16")

    seconds = len(waveform) / 24000.0
    print(f"Wrote {out} ({seconds:.2f}s, voice={args.voice}, speed={args.speed})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
