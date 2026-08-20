---
name: video
description: Use when producing a polished 9:16 or 16:9 video from concept through render, QA, and delivery.
version: 0.2.0
author: skellymeow
license: MIT
platforms: [windows, macos, linux]
metadata:
  author: "skellymeow <user@example.com>"
  tags: [video, shorts, marketing, ffmpeg, automation]
  hermes:
    tags: [video, shorts, reels, tiktok, youtube, marketing, ffmpeg, playwright, kokoro, hyperframes]
---

# /video

## Purpose

`/video` is an end-to-end production operator. Its default job is to return a finished, editable, QA-checked MP4, not a pile of suggestions or a slideshow pretending to be a video.

It handles SaaS/product promos, explainers, stock-footage edits, reference-inspired structures, talking-head edits, long-form clipping, cinematic/trailer work, and custom compositions.

## Requirements

The exact dependencies depend on the route. Detect them before production instead of assuming them.

Baseline tooling:

- Python 3.10+
- FFmpeg and ffprobe for media operations and technical QA
- Node.js/npx for browser capture and HTML-native composition workflows

Common optional local tooling:

- Playwright Chromium for browser/app capture
- HyperFrames for deterministic HTML/CSS/JS motion composition
- Kokoro + `soundfile` + `espeak-ng` for local narration
- faster-whisper for local transcription and word timings

No paid provider is required for the baseline workflow. Optional stock APIs, hosted TTS, image generation, or video generation may require credentials or payment and must not be used without approval when they incur cost.

Read `references/setup.md` only when setup or provider choice is relevant.

## Instructions

### 1. Route the request

If the user already supplied the important details, do not ask for them again. Otherwise use the compact onboarding in `references/onboarding.md`.

Choose the closest route from `references/workflows.md`:

- SaaS / product promo
- explainer / educational
- stock-footage montage
- reference-inspired recreation
- talking-head edit
- long-form to shorts / clip repurpose
- cinematic / trailer
- custom

Default to **9:16** for short-form social and **16:9** for normal landscape video unless the request says otherwise.

### 2. Run read-only preflight

Run:

```bash
python "${HERMES_SKILL_DIR}/scripts/doctor.py"
```

Hermes should execute helpers through terminal commands exactly as documented. On another compatible agent host that exposes a `run_script` execution primitive, pass the same script and arguments to that runner. Do not make `run_script` a Hermes requirement.

Use the doctor result to choose the smallest viable production path. If a required dependency is missing:

1. check for an already-installed/native alternative
2. use a documented fallback when quality remains acceptable
3. otherwise show the smallest install needed and ask permission before installing

Never install large local image/video models automatically. Never make a paid API call without approval when it can spend money.

### 3. Lock a production brief

Before generating assets, establish a short brief containing:

- goal and audience
- aspect ratio and target duration
- video type
- hook
- beat/scene outline
- visual grammar
- narration choice
- asset strategy
- composition/render path
- external cost, normally `$0` unless a paid option was approved

If the request already defines these, infer the rest and proceed. Do not force a planning ceremony.

### 4. Follow the production rules

Read only the references needed for the chosen route.

Non-negotiable rules:

1. **Motion first.** Use real footage, browser capture, kinetic type, purposeful graphics, camera movement, or generated motion. Ship a slideshow only when the user asked for one.
2. **Hook immediately.** Short-form should communicate tension, curiosity, result, or transformation in roughly the first 1-2 seconds.
3. **Every shot earns its place.** Stock footage must support the exact idea being communicated, not act as generic filler.
4. **Compose natively for the destination.** Do not build landscape and blindly crop it into 9:16.
5. **Prefer local narration when it is good enough.** Respect user-supplied voice/audio and explicit provider choices.
6. **Design captions.** Keep them readable, timed, and clear of faces, UI controls, and platform safe-area conflicts.
7. **Track asset provenance.** Follow `references/media-sources.md`; record source URL, creator/source, license, and use. Never claim commercial permission without evidence.
8. **Use references as structural inspiration, not source material.** Analyze pacing, hooks, rhythm, typography, and visual grammar; do not copy protected footage or distinctive creative expression.
9. **No silent substitutions.** If a route is blocked, state the blocker and use the closest documented fallback only when it still satisfies the brief.
10. **Finish the artifact.** Continue through render and QA unless the user explicitly asked only for a script, plan, storyboard, or raw assets.

### 5. Build with the simplest viable architecture

#### Browser / SaaS footage

For a public or authorized URL, capture deliberate app motion:

```bash
node "${HERMES_SKILL_DIR}/scripts/capture_browser.mjs" --url "https://example.com" --aspect 9:16 --out captures/product.mp4
```

Use smooth scrolling and meaningful interactions. Never record passwords, private customer data, billing details, destructive actions, or anything the user did not authorize.

#### Narration

Generate local Kokoro narration when suitable:

```bash
python "${HERMES_SKILL_DIR}/scripts/kokoro_tts.py" --text-file script.md --out audio/narration.wav
```

Listen or inspect the result when tools permit. Fix obvious pronunciation, pacing, silence, or clipping problems before composition.

#### Captions

Create local subtitle and word timing data when precise caption timing matters:

```bash
python "${HERMES_SKILL_DIR}/scripts/transcribe.py" audio/narration.wav --srt captions/captions.srt --json captions/words.json
```

A faster-whisper model may download on first use. Treat that as a setup/network dependency and do not pretend it is already cached.

#### Composition

Read `references/composition.md` before building the final composition.

Prefer HyperFrames for bespoke deterministic HTML/CSS/JS motion graphics when available. Use FFmpeg as universal media glue/fallback. If the user's existing project already uses Remotion or another capable renderer, reuse it rather than migrating for no reason.

#### Assets

Read `references/media-sources.md`. Prefer:

1. user-owned/local assets
2. verified public-domain or CC0 assets
3. compatible Creative Commons assets with required attribution
4. free-key stock providers the user has configured
5. paid stock or generation only after approval

Use image/video generation only when it materially improves the brief. It is an optional production technique, not a prerequisite for a good edit.

### 6. Keep the run reproducible

Create one workspace per production:

```text
video-output/<slug>/
  brief.md
  script.md
  storyboard.md
  sources.json
  assets/
  captures/
  audio/
  captions/
  composition/
  renders/
    final.mp4
  qa.json
```

Keep source files editable. Do not overwrite the user's originals.

### 7. Render, inspect, and repair

Read `references/quality.md`, render the final candidate, then run technical QA:

```bash
python "${HERMES_SKILL_DIR}/scripts/qa_video.py" "video-output/<slug>/renders/final.mp4" --aspect <9:16-or-16:9> --json "video-output/<slug>/qa.json"
```

Use `--require-audio` when the brief requires an audio track.

Also visually inspect representative frames or short segments from the beginning, middle, and end when tools allow it. Technical QA cannot detect ugly typography, covered UI, awkward pacing, bad stock choices, or weak storytelling.

Fix obvious failures and rerun the relevant checks. A video is not done because one renderer exited successfully.

### 8. Deliver the artifact first

Return the final MP4 first, then a terse summary plus the relevant source/license or QA artifact when useful. Do not make the user hunt through the workspace for the finished file.

## Available Scripts

| Script | Purpose | Arguments |
| --- | --- | --- |
| `scripts/doctor.py` | Read-only environment check for Python, FFmpeg, Node, Playwright, HyperFrames, Kokoro, faster-whisper, espeak-ng, and basic GPU info. | No arguments. |
| `scripts/capture_browser.mjs` | Record a URL with Playwright and encode a clean browser capture. | Required `--url`, `--out`; optional `--aspect 9:16|16:9`, `--duration N`, `--width N`, `--height N`, `--no-scroll`. |
| `scripts/kokoro_tts.py` | Generate local Kokoro narration as WAV. | Exactly one of `--text` or `--text-file`; required `--out`; optional `--voice`, `--lang`, `--speed`. |
| `scripts/transcribe.py` | Create SRT captions and optional word-level JSON with faster-whisper. | Positional input; required `--srt`; optional `--json`, `--model`, `--language`, `--device`. |
| `scripts/qa_video.py` | Probe the rendered video for streams, duration, aspect/resolution, audio, long black segments, and volume problems. | Positional video; optional `--aspect 9:16|16:9`, `--require-audio`, `--json`. |

## Examples

**SaaS short**

```text
/video make a 25-second 9:16 launch video for this SaaS URL, clean screen capture, concise narration, designed captions, no paid APIs
```

Expected behavior: doctor -> brief -> authorized capture -> local narration/captions if available -> composition -> MP4 -> technical + visual QA -> delivery.

**Reference-inspired edit**

```text
/video use this reference for pacing and visual grammar, but make the actual visuals and copy original for my product
```

Expected behavior: extract structure and rhythm, do not reuse protected source footage, build an original production, track source licenses, render and QA.

**Plan only**

```text
/video storyboard this idea only - do not render yet
```

Expected behavior: stop at the requested planning artifact. Do not install dependencies or generate/render media unnecessarily.

## Error Handling

- Preserve intermediate artifacts when a late render/encode step fails so work can resume instead of starting over.
- Treat missing packages, model downloads, network failures, browser navigation failures, unsupported media, and renderer errors as explicit blockers with the smallest next action.
- Never hide a failed required step behind a fallback that changes the brief materially.
- If an optional narration/caption method fails, use an existing safe alternative only when the result remains acceptable; otherwise report the blocker.
- If QA returns a failure, do not deliver the candidate as final until the failure is fixed or the user explicitly accepts the known defect.
- Warnings require judgment: inspect them and decide whether they affect the brief rather than mechanically failing every warning.

## Troubleshooting

| Problem | Likely cause | Response |
| --- | --- | --- |
| Doctor reports FFmpeg/ffprobe missing | Core media tooling is absent | Ask permission for the smallest platform-appropriate install; do not continue to a fake QA result. |
| Browser capture says Playwright is missing | Workspace lacks Playwright/Chromium | Use existing authorized browser footage or ask before installing Playwright and Chromium. |
| URL capture times out or shows the wrong state | Network/login/app readiness issue | Verify the URL/state, use authorized authenticated capture only when credentials/private data can be protected, or switch to user-supplied footage. |
| Kokoro import/setup fails | Python package, voice dependency, or espeak-ng missing | Use the documented local setup after permission, an already-configured TTS option, or proceed without narration only if the brief permits it. |
| faster-whisper tries to download a model | Model is not cached | Explain the download/network requirement; use existing timing data/manual captions or get permission to proceed. |
| HyperFrames/renderer is unavailable | Node package/runtime mismatch | Reuse an installed capable renderer or use FFmpeg composition for a simpler design; do not install/migrate silently. |
| FFmpeg encode fails after browser capture | Codec/tooling problem | Preserve the raw capture path printed by the helper, repair FFmpeg, then re-encode instead of recording again. |
| QA reports wrong aspect/resolution | Composition/export settings are wrong | Re-render at the native target dimensions and rerun QA. |
| QA warns about black segments or quiet/clipping audio | Timeline gap, fade, or mix issue | Visually/audibly inspect the flagged region, fix unintended defects, and keep intentional creative fades only when justified. |
| Stock license cannot be verified | Source metadata is unclear | Do not use the asset as commercially safe; replace it with a verifiable source or user-owned media. |

## Limitations

- Technical QA cannot judge taste, narrative strength, caption aesthetics, pronunciation quality, or whether an edit feels premium; visual/audio inspection is still required.
- Browser capture can only show states the agent can lawfully and safely access. Private authenticated surfaces require extra care and explicit authorization.
- Free/local tools vary by machine performance. Heavy rendering, transcription, and generation may be slow or unavailable without suitable hardware.
- Stock/provider availability and licenses can change. Provenance must be checked at use time rather than assumed from an old list.
- Generative media may introduce visual artifacts or rights/licensing constraints and should not replace simpler deterministic production when it adds no real value.

## Completion Contract

A `/video` production is complete only when the requested artifact exists, aspect/duration match the brief, required audio is present, technical QA has no unresolved failures, representative visuals were inspected when possible, obvious pacing/caption/media defects were repaired, asset provenance is recorded, and the final MP4 is delivered directly to the user.