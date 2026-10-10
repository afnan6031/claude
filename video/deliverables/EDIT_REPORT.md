# Panama earthquake explainer: edit report

**Source:** `AI_Editing_test.mp4`. Portrait, 1080×1920, 30 fps, 44.67 s. Urdu narration, talking head shot on a partial green screen.
**Output:** `renders/panama-quake-final.mp4`. Same aspect ratio, resolution and frame rate (1080×1920, 30 fps, H.264 + AAC). Not upscaled: 4K would add pixels but no real detail.
**Editable project:** `video/index.html` (HyperFrames composition). Open it with `npm run dev`, render it with `npm run render`.

---

## 1. Transcript (Urdu, phrase-level timestamps)

Speech recognition used Whisper large-v3-turbo via sherpa-onnx, run locally. Every phrase was decoded in overlapping windows, then corrected by hand. Full files: `deliverables/transcript_ur.srt`, `deliverables/transcript_en.srt`, `video/transcript.json`.

| # | Time | Urdu | English |
|---|------|------|---------|
| 1 | 0.00–2.31 | پاناما کے قریب سمندر میں زمین ہل گئی۔ | The earth shook in the sea near Panama. |
| 2 | 2.31–5.62 | کتنا خطرناک تھا یہ زلزلہ؟ چار اکتوبر کو مقامی وقت | How dangerous was this quake? On 4 October, local time |
| 3 | 5.62–8.45 | کے مطابق صبح آٹھ بجے بحرالکاہل میں | at 8 a.m., in the Pacific Ocean, |
| 4 | 8.45–10.81 | پانچ اعشاریہ ایک شدت کا زلزلہ آیا۔ | a magnitude 5.1 earthquake struck. |
| 5 | 10.81–14.64 | اس کا مرکز پاناما کوسٹاریکا کی سرحد کے قریب، | Its epicentre was near the Panama–Costa Rica border, |
| 6 | 14.64–18.73 | پونتا بوریکا سے تقریباً دو سو پچانوے کلومیٹر جنوب میں، | about 295 km south of Punta Burica, |
| 7 | 18.73–20.92 | صرف دس کلومیٹر گہرائی پر تھا۔ | only 10 km deep. |
| 8 | 20.92–24.48 | اچھی خبر یہ کہ مرکزی آبادی سے بہت دور سمندر میں تھا، | The good news: it was at sea, far from population centres, |
| 9 | 24.48–27.16 | اس لیے نہ کوئی نقصان ہوا، نہ سونامی، نہ خطرہ۔ | so no damage, no tsunami, no danger. |
| 10 | 27.16–28.84 | یہ علاقہ زلزلوں کا گڑھ ہے۔ | This region is an earthquake hotspot. |
| 11 | 28.84–35.05 | صرف اسی سمندری حصے میں ۲۰۲۶ میں ۴.۵ سے زیادہ شدت کے تیرہ زلزلے آ چکے ہیں۔ | In this sea area alone, 13 quakes above M4.5 have hit in 2026. |
| 12 | 35.05–40.55 | ۱۹۹۱ میں یہاں ۷.۴ کا زلزلہ آیا تھا جس میں تئیس افراد جاں بحق ہوئے تھے۔ | In 1991 a 7.4 quake struck here, killing 23 people. |
| 13 | 40.55–44.66 | کیا آپ نے کبھی زلزلہ محسوس کیا ہے؟ کمنٹ سیکشن میں ضرور بتائیں۔ | Have you ever felt an earthquake? Tell us in the comments. |

**Transcription confidence notes**
- The model heard "بیرال قحل". Context makes it بحرالکاہل (Pacific Ocean).
- "تیرہ" (13) came out as "تیران". I'm confident it is 13, but please confirm.
- "تئیس" (23) was decoded as 23 in three of four passes.

**Fact check (things the speaker states).** A web search found a USGS-reviewed event on 4 Oct 2026 at 14:06 UTC, **295 km S of Burica, Panama, 10 km deep**. That matches the narration, and 14:06 UTC is about 8 a.m. in Costa Rica. USGS lists it as **M5.0**; the speaker says 5.1. I kept the speaker's 5.1 on screen and in the captions. Change one variable in `index.html` if you want M5.0. I could not independently verify the "13 quakes ≥4.5 in 2026" or "1991: 7.4, 23 deaths" figures, because USGS and Hugging Face are blocked from this environment. They appear on screen exactly as spoken.

---

## 2. Timestamped editing breakdown

Layouts: **Hero** = speaker full frame. **Card** = speaker lowered about 470 px, glass card in the top band. **Map** = speaker scaled to 78% at the bottom, map card above. The speaker's face is never covered: cards sit only in the band above the head, and captions sit on the chest or shirt.

| Time | Narration | Visual | Motion | Sound |
|------|-----------|--------|--------|-------|
| 0.00–3.90 | Hook: "the earth shook near Panama" | Hero. **PANAMA** title behind the speaker's head (depth layering). Glass "BREAKING · پاناما · زلزلہ" pill | Slow 4% push-in. Title rises and settles in scale. **Camera tremor 1.3–2.3 s on "زمین ہل گئی"** (decaying, deterministic) | Low impact 0.2 s; earthquake rumble 1.25 s |
| 3.55–10.6 | Date, time, Pacific, M5.1 | Card: three stat tiles (4 اکتوبر · صبح 8 بجے · بحرالکاہل) appear on their spoken words; magnitude panel with **5.1 count-up** and seismograph trace | Card slides in; tiles stagger in with the words; panel wipes in; trace draws | Whoosh; 3 UI clicks on the tiles; soft impact on "5.1" |
| 10.25–24.3 | Epicentre, distance, depth, far from people | Map: **data-accurate map** (Natural Earth 1:10m) of Costa Rica, Panama, Colombia and Nicaragua. Panama, then Costa Rica, highlight on their names. Punta Burica pin. **295 km** dashed line draws south with a count-up. Epicentre M5.1 with expanding seismic rings. Depth inset (10 km cross-section). "آبادی سے بہت دور" pill; Panama City and San José appear with distance lines | Card drops in; fills change colour; pin pops; line extends; rings ripple 3 times | Whoosh, click, ping on the pin, soft whoosh on the line, click on depth, ping on "good news" |
| 23.95–27.0 | "No damage, no tsunami, no danger" | Card: "اچھی خبر / Good news" with **three green checks**, each landing on its spoken phrase | Rows slide in from the right; check icons spring | Whoosh + 3 clicks |
| 26.75–28.8 | "This region is a quake hotspot" | Hero (pattern interrupt). Title **زلزلوں کا گڑھ** with an orange underline | Slow 6% push-in; underline draws | Soft whoosh |
| 28.45–35.0 | 13 quakes ≥4.5 in 2026 | Card: "2026" and "M 4.5+" chips on their words; **13 count-up**; 13 quake dots pop in sequence | Chips rise; number counts; dots stagger | Whoosh, 2 clicks, light impact on "13" |
| 35.0–40.4 | 1991: 7.4, 23 deaths | Card: **1991**; bars comparing the spoken magnitudes 7.4 vs 5.1; muted "In memoriam · 23 افراد جاں بحق" panel | Year slides in; bars grow; casualty panel fades in gently | Soft whoosh, 1 click. No effect on the death toll, out of respect |
| 40.2–44.66 | CTA: "felt an earthquake? comment" | Card: question headline; **comment-box mockup** (avatar, placeholder "اپنا تجربہ کمنٹ میں لکھیں", blinking caret, send button pulse) appears on "کمنٹ" | Card in; input rises; caret blinks; send button pulses | Soft whoosh; notification ping on "کمنٹ" |
| whole video | — | **Urdu Nastaliq captions**, phrase-synced, with keyword colour accents (orange = magnitude and danger, green = good news, blue = CTA) | Each phrase fades in from blur; captions follow the layout (y moves with the speaker) | Music bed throughout at about −20 dB under the voice |

---

## 3. Background replacement, colour and audio

**Background.** I removed the green screen and white wall, and placed the speaker on a graphite studio backdrop with a soft light falloff behind the head.
1. An AI person matte (`hyperframes remove-background`, u2net human-seg) gives the silhouette and handles hair against the white wall.
2. A green-difference key is combined with it (minimum of the two) to remove green spill at the edges.
3. A clean background plate is reconstructed from 61 frames. Motion-blurred hands are **unmixed** against it: the true colour and partial transparency are recovered instead of a green or yellow blur.
4. A wall key (bright, unsaturated pixels above the eyes only) cleans the hair top.
5. Edge colour decontamination, a 1 px erode and a 0.9 px feather.

The result is `assets/footage/subject.webm` (VP9 with alpha).

**Colour grade** (baked into the subject plate):
- Exposure +5%
- Gentle S-curve that keeps shadows open
- Warmth: red +2.5%, blue −3.5%, which removes the green-screen cast from the skin
- Saturation +6%
- Light sharpening (unsharp 0.35)

No skin smoothing.

**Voice:**
- 75 Hz high-pass
- FFT denoise (12 dB)
- −2 dB at 250 Hz (mud)
- +2 dB at 3.2 kHz (presence)
- 3:1 compression
- Loudness normalised to **−15 LUFS** (−1.5 dBTP)

---

## 4. Assets used

| Asset | Source |
|-------|--------|
| Speaker footage | Your upload (keyed, graded) |
| Map geometry | `world-atlas@2.0.2` (Natural Earth 1:10m countries), projected with `d3-geo` (Mercator) |
| Epicentre position | Plotted 295 km due south of Punta Burica (8.03°N, 82.87°W), as stated in the narration and the USGS summary. Approximate, not a surveyed coordinate |
| Fonts | Noto Nastaliq Urdu, Inter (open licences, via @fontsource) |
| Music bed | **Synthesised for this edit** (soft pads, Dm–B♭–F–C, 96 bpm shimmer) |
| SFX (whoosh, click, ping, impact, rumble) | **Synthesised for this edit** (filtered noise and sine designs) |
| Icons and UI (checks, send, comment, seismograph) | Hand-built SVG/CSS |

No stock footage, AI-generated video or AI-generated images were used. See the next section.

---

## 5. What could not be done, and why

| Step | Status |
|------|--------|
| B-roll footage, website screenshots and screen recordings | **Not used.** This sandbox's network policy blocks USGS, Hugging Face, jsDelivr and most websites, so I couldn't capture authentic pages. Instead of inventing footage, the map is built from real geographic data. |
| AI-generated video or images of the earthquake | **Deliberately not used.** This is a news report; generated "earthquake footage" would show something that never happened. The data map is the honest visual. |
| Licensed music and SFX libraries | Not reachable (the HeyGen media CLI needs sign-in; the catalogues are blocked). I synthesised original audio instead. Swap in licensed tracks by replacing files in `assets/audio/`. |
| Word-level timing | Whisper large-v3-turbo via sherpa-onnx gives phrase-level, not word-level, timestamps (the standard Whisper model download was blocked). Captions and graphics are synced per phrase (typically 1.5–3 s), with sub-phrase cues placed by ear and energy envelope. |
| Face tracking | No tracker was needed: the speaker stays centred, and every layout keeps graphics in bands the head never enters. I checked this on rendered frames across the whole video. |
| 4K | Not produced. The source is 1080×1920, and upscaling adds no real detail. |

---

## 6. Re-editing

```bash
cd video
npm run dev       # live preview; click to edit text and timing
npm run check     # lint + layout + contrast
npm run render    # writes renders/*.mp4
```

Card timings, caption text and layout modes are all in the `<script>` block of `index.html` (`CAPS`, `toMode(...)`, and the per-section blocks).
