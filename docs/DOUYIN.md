# Douyin source adapter

Initial support: validate public HTTPS Douyin hostnames, infer numeric video IDs from /video/ID (including jingxuan /m/video/ID) or modal_id, and call browser-harness new_tab(url) + wait_for_load() + page_info().

**Not implemented:** account video enumeration, playback controls, metadata extraction, player-ended detection, dynamic selectors, rate-limited queues, and media direct-download. Do not assume any undocumented Douyin API is stable.

Future player adapter contract:
- open_video(url) -> page metadata
- inspect_player() -> state {current_time, duration, paused, ended, error}
- start_playback() -> verified state transition, after operator/browser user gesture if required
- wait_until_ended(max_runtime) -> ended or timeout/interrupted, no infinite waits
- stop_playback() -> optional cleanup
- never navigate away while FFmpeg is active
- on login wall, CAPTCHA, access denial, or rights uncertainty: stop and mark inaccessible; no bypass

Use stable video IDs, idempotent capture jobs, source URL and publication provenance. This first version deliberately keeps a human in the loop while we validate Chrome behavior.
