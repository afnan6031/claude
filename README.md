# claude

Video editing with [HyperFrames](https://github.com/heygen-com/hyperframes): write HTML, render deterministic MP4s.

## Layout

- `video/` — HyperFrames project (`index.html` is the main composition)
- `video/assets/` — media and scripts used by the composition (GSAP is vendored here so renders work offline)
- `.claude/skills/` — HyperFrames agent skills (`/hyperframes` is the entry point)
- `.claude/hooks/session-start.sh` — installs the headless Chrome renderer in cloud sessions

## Editing with Claude

Ask Claude something like:

> Using /hyperframes, create a 15-second intro about [topic] with a fade-in title and background music.

To edit existing footage, drop the file in `video/assets/` and ask, e.g. "add captions to assets/clip.mp4" or "add lower-thirds to this interview".

## Manual CLI

Requires Node.js 22+ and FFmpeg.

```bash
cd video
npm run dev       # live preview studio in the browser
npm run check     # lint + validate the composition
npm run render    # render to MP4 (renders/)
```

First local render needs Chrome Headless Shell: `npx hyperframes browser ensure`.
