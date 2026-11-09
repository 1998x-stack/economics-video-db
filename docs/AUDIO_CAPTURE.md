# Audio capture design and setup

## What browser-harness actually records

Upstream browser-harness recorder stores screenshot JPEGs, events.jsonl and metadata; start_recording() is **not an audio recorder**. Use it for UI audit traces only, not speech transcription.

This project uses browser-harness for browser navigation and FFmpeg for system-loopback audio recording. Do **not** modify the upstream library or assume CDP provides decoded PCM tab audio.

## macOS setup

1. Install browser-harness as described in upstream install.md. Connect it to your **own** Chrome using chrome://inspect/#remote-debugging.
2. Install FFmpeg: brew install ffmpeg.
3. Install and configure an authorized system audio loopback device (for example BlackHole 2ch). Configure a Multi-Output Device or route Chrome playback to the loopback so audio actually reaches the input; do not assume the mere presence of BlackHole means sound is routed.
4. Run ffmpeg -f avfoundation -list_devices true -i "" to determine the **input** name or index. An example device argument is :BlackHole 2ch (confirm it locally). Test an ordinary, authorized media sample.
5. Run evdb doctor. Then run evdb capture-one with --backend avfoundation --device ":BlackHole 2ch" --rights-ok and a known video URL.
6. After browser-harness opens the tab, activate it yourself, seek to 0, and pause. Press Enter to arm FFmpeg, press Play in the browser, then press Enter when it ends. Play back the WAV to confirm the content and duration.

## Linux / Windows

Linux: PulseAudio or PipeWire with Pulse compatibility; --backend pulse --device @DEFAULT_MONITOR@. Confirm via pactl list short sources and correct playback routing.

Windows: --backend dshow --device "audio=YOUR_CAPTURE_DEVICE". A usable loopback/virtual input must be configured; configuration is environment-specific and has not yet been tested in this repo.

## Guardrails and known limitations

- This is Phase 1 **operator-assisted** capture, not reliable automatic playback detection. A background Chrome tab may be throttled or autoplay-blocked.
- Audio loopback records anything routed to that input, including other apps. Isolate the audio route, mute notifications, avoid capturing other people, and review the result.
- The two Enter presses are human-controlled start/stop markers. Some silence at the start/end is expected and will need trimming/quality control.
- Short links may not resolve to a numeric video ID, so pass --video-id. Broken links, login challenges, anti-bot pages and inaccessible videos must be skipped or handled by the operator without bypassing controls.
- Capture only media you are allowed to record, retain or process. Recording is not permission to redistribute a creator's audio or transcripts.
- Never commit audio, transcripts, browser cookies, tokens, profiles, or logs. Keep browser-harness connected only to an intended Chrome profile.
- WAV capture is 16kHz mono 16-bit PCM. Result manifests include source URL, capture time, duration and SHA-256 for later provenance.
- For automation, later implement a site-specific player state adapter (currentTime, duration, paused, ended) and document timing drift, interruptions, replay and authentication failure. Do not rely on fixed sleeps for unknown video duration.

## Useful upstream references

- https://github.com/browser-use/browser-harness/blob/main/SKILL.md
- https://github.com/browser-use/browser-harness/blob/main/src/browser_harness/recorder.py
- https://github.com/browser-use/browser-harness/blob/main/docs/MCP.md
