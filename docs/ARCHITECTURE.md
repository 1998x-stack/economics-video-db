# Architecture and data contracts

## Modules

- ingestion/douyin.py: URL validation and ID extraction
- ingestion/browser_harness.py: controlled Chrome open, no private browser-harness APIs
- audio/ffmpeg_recorder.py: independent WAV capture and SHA-256
- capture.py: one source video -> one audio WAV + manifest
- storage.py: atomic JSON manifest persistence
- asr/: future timed speech recognition with raw and reviewed versions
- extraction/: future evidence-backed claims and forecasts
- retrieval/: future keyword + vector search
- evaluation/: future economic indicator observations and prediction verification

## Proposed pipeline

catalog_discovered -> accessible -> audio_acquired -> transcribed_raw -> reviewed -> extracted -> evaluated.

A recording can fail without invalidating a catalog entry; retry attempts have distinct capture IDs and audio hashes. Preserve source release date separately from capture date.

Capture manifest v1 is documented in schemas/capture.schema.json. Output paths:
- data/audio/VIDEO_ID/CAPTURE_ID.wav
- data/catalog/VIDEO_ID/CAPTURE_ID.json

All generated data is ignored by Git. Future PostgreSQL records should point to artifact paths, rights policy and checksums, not store video/audio binary blobs.

## Evidence provenance for future claims

Keep video_id, transcript_version, segment IDs, start/end timestamps, verbatim evidence, extracted claim type, model version, prompt version, and review status. Do not infer prediction deadlines or claim authorship without explicit evidence.

## Data security

The browser-harness daemon can access all tabs in the selected Chrome profile; use a dedicated profile where practical and do not store cookies/session information in this repository. System loopback can capture non-target apps. Access controls, audit logs and retention policies are future milestones before multi-user deployment.
