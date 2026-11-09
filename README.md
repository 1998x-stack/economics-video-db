# Economics Video DB

A source-grounded economics video research database. Initial creator: 温义飞 (温义飞的急救财经).

**Status:** Phase 0 scaffold + an operator-assisted single-video audio capture MVP. Agent-driven homepage discovery on Douyin and Xigua Video, automatic playback detection, transcription, and LLM extraction are planned, not implemented.

## Architecture

1. browser-harness opens a Douyin video in your approved, locally connected Chrome.
2. An explicit operator starts FFmpeg **system-loopback** audio capture; the operator plays the video and stops capture at the end.
3. A WAV file and JSON manifest are saved to local data/ (ignored by Git).
4. Later stages add timed transcripts, evidence-backed claims, forecasts, and verification.

**Important:** browser-harness start_recording/stop_recording only capture screenshot/action traces; they do not produce video audio. FFmpeg is a separate recorder. The recorder captures an audio input device, which may include sounds from other apps. Use a dedicated output route and disable notifications.

## Quick start (macOS example)

Requirements: Python 3.11+, FFmpeg, Chrome, browser-harness, and a configured system audio loopback device such as BlackHole.

~~~bash
brew install ffmpeg
uv tool install --python 3.12 --upgrade --force browser-harness
# In Chrome: chrome://inspect/#remote-debugging -> enable remote debugging
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
evdb doctor
ffmpeg -f avfoundation -list_devices true -i ""
~~~

Route the desired Chrome/system audio to BlackHole, and confirm device index/name from the command above. Example (replace device with the actual audio input):

~~~bash
evdb capture-one \
  --url https://www.douyin.com/video/7275916556641652027 \
  --backend avfoundation \
  --device ":BlackHole 2ch" \
  --rights-ok
~~~

This is an **operator-assisted** flow: browser-harness opens a tab (it may remain in the background); you activate the tab, pause/rewind, then press Enter to arm recording. Start playback yourself, then press Enter when it finishes. The tool does not automatically control the Douyin play button yet.

For Linux use --backend pulse and an authorized monitor source, e.g. --device @DEFAULT_MONITOR@. Windows dshow is available experimentally using --device audio=DEVICE.

All example URLs are demonstration inputs, not proof of current access. Do not use this tool to bypass authentication, DRM, paywalls, or platform access controls; confirm rights for every recording and subsequent transcription/reuse.

## Documentation

- [Development roadmap](docs/ROADMAP.md)
- [Audio capture setup and limitations](docs/AUDIO_CAPTURE.md)
- [Architecture and data contracts](docs/ARCHITECTURE.md)
- [Douyin browser adapter notes](docs/DOUYIN.md)
- [Pi agent homepage-driven serial workflow](docs/AGENT_WORKFLOW.md)
- [Xigua Video adapter design](docs/XIGUA.md)
- [Pi agent skill](.pi/skills/economics-video-capture/SKILL.md)

## Future Pi-agent collection flow

Pi will start from a user-confirmed creator homepage on Douyin or Xigua Video, discover visible video IDs, and record one permitted video at a time using browser-harness and a separate local FFmpeg recorder. Persistent job states prevent duplicates, resume after interruptions and preserve source provenance. The site-specific adapters are **not yet implemented**; evdb capture-one remains a manual single-video pilot.

See docs/AGENT_WORKFLOW.md. Pi users may load the local .pi/skills/economics-video-capture/SKILL.md specification. Do not treat it as a working unattended automation.

## Tests

~~~bash
pytest -q
~~~

## Media hygiene

Git tracks source code, docs, schemas and tiny placeholder files only. Audio, video, transcripts, extracts, cookies and local browser artifacts are excluded through .gitignore. Do not commit downloaded media or complete copyrighted transcripts to this public repository without permission.
