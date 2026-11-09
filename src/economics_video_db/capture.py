"""One-video, operator-assisted capture pipeline."""

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from .audio.ffmpeg_recorder import FFmpegRecorder, sha256_file
from .ingestion.browser_harness import open_douyin_video
from .ingestion.douyin import infer_video_id, validate_url, validate_video_id
from .storage import write_manifest


def capture_one(
    url: str,
    video_id: str | None,
    backend: str,
    device: str,
    data_dir: Path,
    rights_confirmed: bool,
) -> Path:
    if not rights_confirmed:
        raise ValueError("Pass --rights-ok only if recording and reuse are permitted")
    validate_url(url)
    print("Opening video via browser-harness (tab may remain in background)...")
    page = open_douyin_video(url)
    final_url = str(page.get("url") or url)
    resolved_id = video_id or infer_video_id(url)
    if resolved_id is None:
        try:
            resolved_id = infer_video_id(final_url)
        except ValueError:
            pass
    if resolved_id is None:
        raise ValueError("Could not infer video ID; retry with --video-id")
    resolved_id = validate_video_id(resolved_id)

    capture_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid4().hex[:8]
    audio_path = data_dir / "audio" / resolved_id / (capture_id + ".wav")
    manifest_path = data_dir / "catalog" / resolved_id / (capture_id + ".json")
    print("Browser page:", page.get("title", "(unknown)"))
    print("Bring that Chrome tab to the foreground; pause and seek to the start.")
    input("Press Enter when ready to ARM the audio recorder (NOT playback)... ")
    recorder = FFmpegRecorder(audio_path, backend, device)
    started_at = datetime.now(timezone.utc).isoformat()
    recorder.start()
    print("Audio recording active. Play the video in Chrome now.")
    try:
        input("Press Enter when playback finishes to STOP recording... ")
    except BaseException:
        recorder.abort()
        raise
    seconds = recorder.stop()
    payload = {
        "schema_version": 1,
        "capture_id": capture_id,
        "platform": "douyin",
        "video_id": resolved_id,
        "source_url": url,
        "browser_final_url": final_url,
        "browser_title": page.get("title"),
        "captured_at": started_at,
        "audio_path": str(audio_path),
        "audio_sha256": sha256_file(audio_path),
        "duration_seconds": round(seconds, 3),
        "format": "wav_pcm_s16le_mono_16khz",
        "capture_backend": backend,
        "capture_device": device,
        "rights_confirmed_by_operator": True,
        "transcription_status": "pending",
        "analysis_status": "pending",
    }
    write_manifest(manifest_path, payload)
    print("Saved audio:", audio_path)
    print("Saved manifest:", manifest_path)
    print("Verify the WAV contains the intended video's audio before ingestion.")
    return manifest_path
