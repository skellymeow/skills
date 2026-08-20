# Video workflows

Use the closest workflow, then adapt it. These are production grammars, not rigid templates.

## Shared production loop

```text
intent -> preflight -> brief -> research/reference analysis -> script/beats -> storyboard
-> capture/source/generate assets -> narration/audio -> composition -> captions -> render -> QA -> deliver
```

Keep the loop resumable by writing artifacts into the workspace defined in `SKILL.md`.

## A. SaaS / product promo

Best for apps, websites, launches, features, redesigns, dev tools.

1. Inspect the actual product/site/repo before scripting claims.
2. Pick one promise, not ten features.
3. Script around: **hook -> proof -> 2-4 feature beats -> result -> CTA**.
4. Capture real product interactions with Playwright. Prefer several short purposeful takes over one endless scroll.
5. Add bespoke motion graphics around the footage: title cards, callouts, cursor emphasis, zooms, masks, stat/result cards.
6. Mix in stock/generated media only when it explains a concept that the interface cannot.
7. Narration should describe value while visuals prove it; avoid reading UI text verbatim.
8. For 9:16, redesign the interface framing for vertical. Crop/zoom to the active UI region instead of shrinking a whole desktop page into unreadable postage stamp size.

Suggested short structure:

```text
0-2s   result/tension hook
2-7s   product reveal + first proof
7-18s  2-3 fast feature demonstrations
18-27s transformation/result/social proof
27-32s CTA / brand close
```

## B. Explainer / educational

1. Research current claims if factual/current information matters.
2. Distill one clear thesis.
3. Build 4-8 visual beats, each with a specific visual explanation.
4. Prefer diagrams, text animation, charts, relevant real footage, and concrete visual metaphors.
5. Use narration to connect scenes, not overload them.
6. Cite factual sources in `sources.json` and optionally in end-card/description material.

Avoid generic AI imagery for every sentence. If a real diagram or motion graphic communicates the idea better, build it.

## C. Stock-footage montage

1. Define mood, subject, temporal arc, and shot vocabulary before searching.
2. Search by scene intent, not only broad topic keywords.
3. Build a candidate pool larger than needed.
4. Verify rights before download/use.
5. Cut for visual continuity: direction of motion, color/lighting, scale, subject placement, and beat.
6. Use text/narration sparingly unless it improves the story.
7. Never use watermarked preview media in final production.

## D. Reference-inspired recreation

Treat the reference as a structure/style study, not reusable source footage.

Analyze:

- first-frame promise and hook mechanism
- total duration
- shot count and average shot length
- pacing curve
- narration density
- caption style
- camera/subject movement
- transition vocabulary
- use of music/SFX
- emotional arc
- CTA placement

Then write a **DNA brief** containing what to preserve abstractly and what must change. Produce an original concept for the user's topic/product.

If downloading a reference is lawful and technically available, use `yt-dlp`/local tools only for analysis. Do not include the downloaded reference footage in the final render unless the user owns/has rights to it.

## E. Talking-head edit

1. Transcribe locally.
2. Identify strongest hook and remove dead air/repetition.
3. Build a clean narrative cut before adding effects.
4. Add punch-ins/crops sparingly, timed to emphasis.
5. Use b-roll, diagrams, screenshots, and kinetic captions only where they clarify or maintain attention.
6. Preserve natural speech rhythm; do not jump-cut every breath.
7. Normalize voice, duck music under speech, and keep captions inside safe zones.

## F. Long-form -> shorts / clip repurpose

1. Transcribe and segment the full source.
2. Rank candidate clips by standalone clarity, hook strength, novelty, emotion, and payoff.
3. Each short must make sense without the original context.
4. Reframe to 9:16 with speaker/subject tracking where possible.
5. Add a title/hook only when the source does not naturally provide one.
6. Produce genuinely different clips, not slightly shifted timestamps of the same moment.

## G. Cinematic / trailer

1. Write the emotional beat sheet first.
2. Build recurring visual motifs and intentional contrast.
3. Prefer fewer stronger shots over a pile of unrelated generated clips.
4. Sound design is structural: impacts, risers, ambience, silence, and music transitions should reinforce cuts.
5. Generated video is optional. Real footage + designed typography + excellent sound can outperform mediocre generation.
6. Maintain continuity in subject, palette, lens language, lighting, and movement.

## H. Custom

Map the request onto the shared production loop. Choose the minimum tools required and preserve all quality/license gates.

# Composition selection

Prefer **HyperFrames** when the video benefits from bespoke motion design, website-to-video, typography, data, product/UI presentation, or other HTML-native visuals.

Prefer direct **FFmpeg** composition for simple trims, crops, concatenation, overlays, audio mixing, or when no browser renderer is necessary.

Use **Remotion** when it is already part of the user's project or its React ecosystem materially helps. Do not force a framework migration for a single video.

# Pace guidance

These are heuristics, not hard limits:

- high-energy social/ad: visual change roughly every 0.7-2.5s
- polished SaaS demo: roughly 1.5-4s per visual beat
- explainer: roughly 2-6s per explanatory beat
- cinematic: let strong shots breathe; pacing follows music/emotion

A visual change can be a shot cut, meaningful camera move, UI interaction, layout transition, chart progression, or strong kinetic-type beat. Random zooms do not count as storytelling.
