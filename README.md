# Economics Video DB

可溯源的财经视频逐字稿、论点与经济预测数据库。

> Status: Phase 0 bootstrap. The implementation is developed incrementally on feature branches. Raw media and transcripts are not committed to Git.

## Goal

Discover and catalog public videos; acquire audio only with suitable access and usage rights; generate timestamped transcripts; extract grounded claims and forecasts; verify forecasts against released economic data.

## First milestone

Use [browser-harness](https://github.com/browser-use/browser-harness) for Chrome navigation and a **separate FFmpeg system-loopback recorder** for audio. Note: browser-harness built-in recordings contain screenshots and action traces, **not playable audio**.

See `docs/ROADMAP.md` and `docs/AUDIO_CAPTURE.md` after the scaffold is merged.
