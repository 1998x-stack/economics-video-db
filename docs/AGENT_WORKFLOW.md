# Agent-driven homepage discovery and serial capture

Status: DESIGN ONLY. The existing evdb capture-one command still prompts a human for Play and Stop. Do NOT use it as an unattended Pi-agent command.

## Goal

A Pi agent opens the confirmed creator homepage of 温义飞的急救财经 on Douyin or Xigua Video, collects each public video reference from the visible Works list, and processes them ONE AT A TIME. The result is one WAV and one provenance manifest per authorized video. Never claim full historical completeness without a discovered/missing-item ledger.

## Component responsibilities

1. Pi Agent: orchestration, page inspection and per-video recovery through browser-harness.
2. Douyin/Xigua site adapters: creator identity verification, visible homepage enumeration, video URL/ID, player state (currentTime, duration, paused, ended).
3. Independent FFmpeg loopback recorder: audio start, health, stop, WAV finalization. Browser-harness built-in recording only saves screenshots and action traces, NOT audio.
4. Durable job ledger: idempotency by (platform, platform_video_id), state, attempts, source page, capture ID, errors, WAV path, hash and timestamps.
5. ASR and LLM stages: post-QC only, preserving time-coded provenance.

## Process one publication atomically

- Discover videos from a user-confirmed account homepage (check stable creator ID, not display name alone).
- Collect visible metadata; paginate/scroll within site limits and checkpoint progress.
- De-duplicate by source platform + video ID. Cross-platform duplicate detection comes later; titles alone are insufficient.
- Lease exactly one queued video; use a single browser-controller and a single active audio recorder.
- Open exact video page; verify it belongs to the intended creator; check accessible HTML5 player state or accessibility controls.
- Seek/pause at beginning if supported. Start FFmpeg first and check recorder health. Then play; verify currentTime advances.
- Poll bounded player state and detect real ended signal. Buffering, recommended-video autoplay, unrelated navigation, timeouts or login walls are failures requiring review, not successful completion.
- Stop recorder, finalize WAV, verify duration/audio signal and SHA-256, write manifest atomically. Only then visit next video.
- Save cursor and results. On crash, resume with failed/interrupted jobs, never silently overwrite a successful capture.

## Proposed job states

discovered -> queued -> opening -> ready -> recording -> captured -> qc_passed -> transcribed -> analyzed

Other states: blocked, unavailable, skipped, interrupted, qc_failed. All transitions require timestamps and error context.

## Agent-facing local commands (PROPOSED, NOT IMPLEMENTED)

- evdb jobs discover --platform douyin|xigua ... : add or update source candidates
- evdb jobs next : acquire one pending job
- evdb recorder start --job-id ID --backend INPUT --device DEVICE : start real FFmpeg capture
- evdb recorder status --capture-id ID : check process health
- evdb recorder stop --capture-id ID : finalize WAV and return hash/duration
- evdb jobs complete --job-id ID : commit verified capture
- evdb jobs fail --job-id ID : document failure
- evdb jobs resume : recover crash and interrupted jobs

Implement with a single-session lock, persistent process supervision, retry limits and orphan cleanup. No remote unauthenticated control endpoint.

## Pi integration

Option A: Pi bash tool calls the existing browser-harness CLI for navigation and, when implemented, the evdb local recorder commands. This requires no new Pi extension and is best for the first pilot.

Option B: third-party Pi package pi-browser-harness provides native browser tools for a Pi agent (https://pi.dev/packages/pi-browser-harness). Review code/permissions before installing; do not use two competing browser controllers on one tab.

Important: third-party Pi browser integration is not the upstream browser-use/browser-harness package itself.

## Pilot and acceptance

First capture three short, accessible and appropriately authorized videos on ONE platform, not the entire account.

Checks: three distinct WAV/manifest pairs; correct source identity; no duplicates on rerun; audible audio of expected duration; bounded timeout and retry behavior; simulated interruption is recoverable; login/CAPTCHA/access-denial leads to stop without bypass.

Then implement a separate Xigua adapter using the same core capture/ledger infrastructure.

## Rights, privacy and operational boundaries

Only record, retain and process content where appropriate permission or an applicable right exists. A public URL is not blanket permission for a private corpus or re-distribution. Do not bypass paywalls, login controls, CAPTCHAs or DRM. Use isolated Chrome profile and loopback audio route: other app sound, notifications and unrelated private information must not be recorded. Keep source audio, transcripts, logs, cookies and browser data out of this public repository.
