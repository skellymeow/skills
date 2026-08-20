# Video quality gate

The renderer succeeding is not proof the video is good. Review the output as a viewer would.

## Automated checks

Run `scripts/qa_video.py` against the final MP4.

Minimum technical expectations:

- valid video stream
- intended aspect ratio
- 9:16 final target: 1080x1920 unless user requested otherwise
- 16:9 final target: 1920x1080 unless user requested otherwise
- H.264/H.265/AV1 or another broadly playable final codec chosen intentionally
- audio stream present when narration/music/SFX are intended
- no accidental long black frames
- duration roughly matches the brief
- file is non-trivial and playable

## Visual review

Inspect representative frames and, when possible, watch the rendered video.

Reject/fix if any are true:

- unreadable or clipped text
- captions outside safe margins
- desktop UI shrunk too small in a vertical composition
- logos or important UI cropped accidentally
- watermarked stock previews in final output
- stretched/distorted media
- broken image/video placeholders
- inconsistent fonts/layout for no reason
- long dead moments
- random transitions that fight the content
- generic slideshow feel where real motion was promised
- repeated stock shot or visual motif without purpose
- AI-generated continuity errors that dominate the scene

## Story/pacing review

For short-form, ask:

1. Does frame one give the viewer a reason to continue?
2. Is the value/topic understandable without waiting 8 seconds?
3. Does each scene advance the promise?
4. Is there a payoff/result, not just setup?
5. Does the ending tell the viewer what to do/remember when appropriate?

For product promos, every major claim should have visual proof or a clearly labeled conceptual graphic.

## Audio review

Reject/fix if:

- narration clips or distorts
- speech is hard to understand over music
- music abruptly starts/stops accidentally
- dead silence appears where audio was intended
- TTS pronunciation errors change meaning or sound obviously broken
- SFX are spammed on every transition

Default hierarchy: speech first, then intentional SFX, then music underneath.

## Caption review

Captions should:

- be timed to actual speech
- use phrase/word groups that are easy to scan
- remain inside platform-safe margins
- maintain strong contrast
- avoid covering the main subject or UI
- avoid dumping full paragraphs on screen

## Distinctness review

Before delivery, ask:

- Could this exact composition be reused for any random company/topic with only text swapped?
- Is the footage actually about the thing being discussed?
- Did we build any visual moments specific to this product/topic?

If the answer is effectively "generic template," improve it before delivery.

## Final deliverables

At minimum:

```text
renders/final.mp4
qa.json
sources.json     # when external assets are used
```

Keep script/storyboard/composition sources in the project workspace so the video can be revised instead of regenerated from scratch.
