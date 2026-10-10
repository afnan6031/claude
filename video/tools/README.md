# Processing tools

Scripts used to prepare the Panama earthquake edit. Paths are relative to `video/`.

1. `npx hyperframes remove-background assets/footage/raw.mp4 -o work/matte.mov` — AI person matte.
2. `python3 tools/plate.py assets/footage/raw.mp4 work/matte.mov work/plate.npy` — clean green-screen plate.
3. `python3 tools/key.py assets/footage/raw.mp4 work/matte.mov assets/footage/subject.webm 0 work/plate.npy` — combined key, spill unmix, decontam, grade → VP9 alpha.
4. `python3 tools/synth.py assets/audio` — synthesised SFX + music bed.
5. `node tools/map.mjs assets/map.json` (run where world-atlas/topojson-client/d3-geo are installed) — map geometry.
6. ASR: `seg_asr.py` / `win_asr.py` with sherpa-onnx + Whisper large-v3-turbo (GitHub release `asr-models/sherpa-onnx-whisper-turbo`).

Footage, mattes and renders are git-ignored because this repo is public.
