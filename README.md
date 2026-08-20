# skellymeow/skills

High-leverage capability packs for Hermes Agent. Each pack is one clean slash command backed by focused workflows, references, and deterministic helper scripts.

## Install `/video`

One command:

```bash
hermes skills install skellymeow/skills/skills/video
```

Start a new Hermes session, then run:

```text
/video
```

### Optional: subscribe to the whole skill repo

```bash
hermes skills tap add skellymeow/skills
hermes skills install skellymeow/skills/video
```

## Skills

### `/video`

Agent-native video production for vertical and landscape content. It can onboard a new user, audit/install a free local production stack with permission, plan the video, capture websites, source license-safe media, generate local Kokoro narration, create captions, compose motion graphics, render, and self-review the final MP4.

Core free path: **FFmpeg + HyperFrames + Playwright + Kokoro + faster-whisper + open/CC0 media**. Paid image/video APIs are optional, never required.

See [`skills/video/SKILL.md`](skills/video/SKILL.md).

## Philosophy

- One command should expose a full capability domain, not dozens of tiny slash commands.
- Free/local paths work first; paid providers are optional upgrades.
- Deterministic scripts handle fragile operations; Markdown skills handle creative judgment.
- Never silently install software, spend money, or use media with unclear commercial rights.
- Deliver finished artifacts, not merely instructions.

## License

MIT
