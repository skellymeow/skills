# Video onboarding

Use this only when the user's request is missing important production choices. Never ask for information already provided.

## `/video` with no useful arguments

Ask one compact onboarding question, not a long interview:

```text
What are we making?

Format: 1) 9:16 short/reel  2) 16:9 landscape
Type: A) SaaS/product promo  B) explainer  C) stock montage  D) reference-inspired
      E) talking-head edit  F) long video -> shorts  G) cinematic/trailer  H) custom
Input: send the topic, URL, repo/site, or local media you want me to use.

I can run this entirely free/local where possible. After you choose, I'll check your machine and ask before installing anything missing.
```

If the platform supports interactive choices, present the same choices interactively. Otherwise plain text is enough.

## Defaults

When the user says "you choose" or does not care:

- social/short-form -> 9:16, 1080x1920 final
- YouTube/site/demo/desktop -> 16:9, 1920x1080 final
- short social duration -> 20-45 seconds unless content needs more
- narration -> Kokoro local
- rendering -> HyperFrames + FFmpeg
- captions -> designed captions from local timing
- external cost -> $0

## First-run setup behavior

After format/type are known:

1. Run `scripts/doctor.py`.
2. Decide which missing components are actually needed for this workflow.
3. If none are missing, say so briefly and proceed.
4. If dependencies are missing, explain them in one compact message and ask:

```text
I need to install: <smallest dependency list>. All are free/local. Okay to install them now?
```

5. Do not install before approval.
6. Do not ask the user to install things manually if Hermes has terminal access and can do it after approval.
7. Never auto-download multi-GB AI image/video weights. Offer those only as an optional upgrade after inspecting hardware.

## Inputs by workflow

- SaaS/product promo: URL/repo/app + key feature or CTA
- explainer: topic + audience
- stock montage: topic/mood + optional narration
- reference-inspired: reference URL/file + new topic/product
- talking-head: source video + desired output length/platform
- clip repurpose: long source + number/type of clips
- cinematic/trailer: subject/product + intended mood

If a source URL/file already implies the workflow, infer it and avoid redundant questions.
