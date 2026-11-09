# Xigua Video adapter (planned)

Status: design placeholder. No verified Xigua author homepage traversal or player adapter has been implemented.

Start from a user-confirmed 温义飞 creator profile URL on 西瓜视频 and collect visible public works with platform-specific IDs, title, publication date if available, video URL and creator account ID. Do not assume Douyin video IDs, URL patterns or HTML selectors are reusable on Xigua.

Proposed adapter interface:
- inspect_creator_profile(page) -> stable account identity and verification status
- enumerate_visible_videos(page) -> source-linked candidates
- open_video(url) -> player page
- inspect_player() -> currentTime, duration, paused, ended, error
- start_playback() and bounded wait_until_ended()

The platform adapter must share the recorder and persistent job ledger with Douyin. On inaccessible/private videos, login walls, CAPTCHA, DRM or unclear recording rights, stop and mark blocked/unverified; never circumvent controls.

See docs/AGENT_WORKFLOW.md.
