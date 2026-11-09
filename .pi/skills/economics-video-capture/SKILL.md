---
name: economics-video-capture
description: Prepare and eventually run one-at-a-time browser-harness navigation and authorized audio capture from an economics creator homepage on Douyin or Xigua Video.
---

# Economics video capture (Pi skill)

Read docs/AGENT_WORKFLOW.md, docs/AUDIO_CAPTURE.md and docs/ROADMAP.md before attempting this workflow.

STATUS: Design and operator-assisted pilot only. The current evdb capture-one command requires a human to press Enter for recording start and stop. Do not run it unattended or pretend a fully automatic capture pipeline exists.

## Operating guidelines

1. Obtain a user-confirmed account homepage (Douyin or Xigua). Do not identify the creator from display name alone; verify platform account ID / source links.
2. Enumerate visible source video URLs and IDs with browser-harness, checkpoint discovery and deduplicate.
3. Only act on content the operator is permitted to record and process. Stop on login, CAPTCHA, DRM or unclear rights, without bypass.
4. Use a single browser tab/controller and one active local audio recorder per video. Avoid autoplay of recommendations and other app sounds.
5. Record one authorized video, verify audio, checksum and manifest, then move to the next. Mark failures; never conflate them with successes.
6. Keep media, transcripts and credentials out of the public repository.

## Current operator-assisted demonstration

Run evdb doctor, verify FFmpeg loopback device routing and browser connection. For a single authorized video use evdb capture-one with url, backend, device and --rights-ok; manually start/stop playback as prompted. Verify the WAV file.

## Future fully agent-driven implementation

Build tested evdb recorder start/status/stop and persistent jobs discover/next/complete/fail/resume commands as described in docs/AGENT_WORKFLOW.md before letting Pi run unattended. Browser-harness start_recording/stop_recording are screenshot/trace controls, NOT audio.

Pi may use its bash tool to run browser-harness CLI (preferred initial integration). pi-browser-harness is a separate third-party Pi extension; review before install and do not mix two browser controllers in one session.
