# Media sourcing and licensing

The agent must know the rights status of every external asset used in a final render.

## Default source order

### 1. User-owned/local media

Best option. Use files, screen recordings, logos, product screenshots, footage, music, and brand assets supplied by the user when appropriate.

Record provenance as `user_supplied`.

### 2. Public-domain / CC0 media

Prefer these for zero-friction commercial-safe work when the source explicitly marks the individual asset accordingly.

Useful discovery locations:

- Wikimedia Commons - images, audio, video; licenses vary per file, verify each file page.
- Internet Archive - large archive; rights vary per item, verify item metadata/rights.
- NASA media - much is usable under NASA media guidelines, but logos, third-party material, identifiable people, and endorsements require care. Verify the specific asset and intended use.
- Openverse - search layer for openly licensed images/audio; filter by license and still verify the source record.
- `btahir/open-lofi` - repository publishes 150+ lo-fi tracks under CC0 1.0; useful free background-music fallback.

Never infer `public domain` merely from being hosted on an open archive.

### 3. Creative Commons assets

Use only when the license is compatible with the final use.

At minimum record:

```json
{
  "asset": "assets/example.mp4",
  "source_url": "https://...",
  "creator": "...",
  "license": "CC BY 4.0",
  "license_url": "https://creativecommons.org/licenses/by/4.0/",
  "attribution_required": true,
  "notes": "used in scene 3"
}
```

If attribution is required, create a credits file and include attribution in the delivery package or final content/description as appropriate.

Avoid NC assets for commercial/marketing work. Avoid ND assets when editing/cropping/remixing would create a derivative.

### 4. Free developer-key stock providers

Pexels/Pixabay/Unsplash can be useful, but API access and license terms are separate questions. A free API key does not itself prove unrestricted rights.

If configured, log the canonical asset page and current license/source terms.

### 5. Discovery MCPs

#### Stockflow MCP

`NmediaCloud/stockflow-mcp` can search the public Stockflow catalog without an API key and exposes watermarked previews. Those previews are for drafts; its own README states full-resolution production assets are licensed separately, with paid licenses available from the asset page.

Therefore:

- okay: discovery, storyboards, watermarked internal preview
- not okay: silently shipping preview assets in a final commercial video
- final use: acquire/verify the required license first

#### Tunetank MCP

`https://mcp.tunetank.com` is a no-auth discovery endpoint for music/SFX. Its README states music is free for personal/non-commercial use and directs commercial users to Tunetank licensing terms.

Therefore use it for discovery, not as blanket proof of free commercial rights.

#### Freesound MCP

Common Freesound MCP implementations require a Freesound API key. Individual sounds have different licenses. Always inspect the returned license before use.

## Reference-video rules

A YouTube/TikTok/Reel/reference URL may be analyzed for abstract production characteristics such as pacing, hook structure, shot length, transitions, caption behavior, framing, and sound-design patterns.

Do not:

- copy the reference footage into the deliverable without rights
- clone a creator's distinctive protected expression shot-for-shot
- remove watermarks
- present downloaded reference media as stock

Create a new visual plan with original assets.

## sources.json

Every final run using external media must write `sources.json` with one object per asset. Include source URL and license status even when attribution is not required.

If licensing cannot be verified, do not use the asset in the final render. Substitute a verified asset, create an original graphic, capture user-owned material, or ask the user.
