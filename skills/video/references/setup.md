# Free/local setup

Only install components required by the chosen workflow, and only after the user approves installation.

## Core stack

| Component | Purpose | Cost |
|---|---|---|
| FFmpeg + ffprobe | encode, mux, crop, mix, inspect | free/local |
| Node.js 22+ / npx | HyperFrames + Playwright runner | free/local |
| HyperFrames | HTML/CSS/JS -> deterministic MP4 | free/open source |
| Playwright Chromium | website/app capture | free/local |
| Python 3.10+ | TTS/captions/helpers | free/local |
| Kokoro | local TTS | free/open weights |
| faster-whisper | transcription/caption timing | free/local |

## Install minimal dependencies

### Node packages

Inside the user's video workspace, initialize only if needed:

```bash
npm init -y
npm install playwright
npx playwright install chromium
```

HyperFrames can be invoked with `npx hyperframes ...`; install it into the workspace when repeated rendering is expected:

```bash
npm install hyperframes
```

### Python packages

Prefer an isolated environment:

```bash
python -m venv .video-venv
```

Activate it using the platform's normal venv command, then:

```bash
python -m pip install -U pip
python -m pip install kokoro soundfile faster-whisper
```

Kokoro's phonemization may require `espeak-ng` on the host. Install it through the user's OS package manager when available. On Windows, use the official eSpeak-NG Windows installer if it is not already present.

### FFmpeg

Use the platform package manager when available:

```text
macOS:        brew install ffmpeg
Ubuntu/Debian:sudo apt-get update && sudo apt-get install -y ffmpeg espeak-ng
Windows:      winget install Gyan.FFmpeg
```

If the package manager is unavailable, use the official FFmpeg download for the platform instead of downloading random binaries.

## Optional media sources

No accounts are required for the baseline open-media route (Wikimedia Commons, Internet Archive, NASA/public-domain sources, Openverse search where applicable).

Optional free developer keys can improve generic stock search:

- Pexels API
- Pixabay API
- Unsplash API for still images

Do not block production while waiting for optional keys.

## Optional MCP discovery sources

These are discovery helpers, not proof that every returned asset is free for commercial use:

- `stockflow-mcp`: no API key for search/previews; full-resolution production assets may require a paid Stockflow license.
- `https://mcp.tunetank.com`: no-auth music/SFX discovery; commercial licensing must be checked on Tunetank.
- Freesound MCP servers: useful for SFX metadata, but common implementations require a Freesound API key and each sound has its own license.

Always follow `media-sources.md` before using a discovered asset.

## Optional local AI generation

Do not install large models automatically.

If the user explicitly wants AI-generated images/video:

1. Inspect available GPU/VRAM.
2. Check whether ComfyUI, local diffusion/video models, or an existing generation service is already configured.
3. Prefer what already exists.
4. If nothing exists, offer a local model path only if the hardware is suitable and tell the user the download/storage cost first.
5. Otherwise offer a cloud provider as an optional paid path and ask before spending.

A high-quality video must remain possible without generative video models by combining real footage, browser capture, typography, graphics, narration, sound design, and intentional editing.
