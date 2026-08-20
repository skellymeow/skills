# Composition and rendering

Use this when building the final edit.

## Default: HyperFrames

HyperFrames is preferred for agent-authored motion design because the composition is ordinary HTML/CSS/JavaScript and renders deterministically to MP4.

From the video's `composition/` directory:

```bash
npx hyperframes init .
```

Author the composition around the actual storyboard and assets. Do not blindly assemble catalog blocks. Reuse engine mechanics, not a frozen visual identity.

Useful visual building blocks:

- full-bleed video/image scenes
- masked browser captures
- kinetic typography
- device/browser frames
- callout lines and labels
- animated counters/stat cards
- charts/diagrams
- gradients/noise/lighting layers
- SVG iconography
- subtle parallax/scale/camera moves
- captions driven by word timing JSON

Preview during iteration:

```bash
npx hyperframes preview
```

Render when ready:

```bash
npx hyperframes render
```

Then normalize the final deliverable with FFmpeg if needed:

### 9:16

```bash
ffmpeg -y -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart final.mp4
```

### 16:9

```bash
ffmpeg -y -i input.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart final.mp4
```

Do not use padding as a substitute for designing the composition natively for the chosen aspect ratio. These commands are delivery normalization, not art direction.

## Captions

Create timing data from narration/source audio:

```bash
python "${HERMES_SKILL_DIR}/scripts/transcribe.py" audio/narration.wav --srt captions/captions.srt --json captions/words.json
```

Use word/phrase timing from `words.json` to animate designed captions in the composition. Plain burned SRT is an acceptable fallback for utilitarian videos, not the preferred path for polished marketing/social work.

## Direct FFmpeg path

Skip HyperFrames when the task is fundamentally editorial rather than motion-design-heavy: trim, crop, concatenate, picture-in-picture, simple overlays, audio mixing, or format conversion.

## Audio mix

Keep speech intelligible. A practical starting point is to place music clearly below narration, then adjust by ear rather than trusting one fixed dB value for every track. Use fades/ducking around speech and scene transitions. Avoid hard starts/stops unless intentional.

## Final encoding

Prefer broadly compatible MP4 output (`H.264 + AAC`, `yuv420p`, `faststart`) unless the destination/user requires something else.
