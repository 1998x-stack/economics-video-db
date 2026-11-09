import wave

import pytest

from economics_video_db.audio.ffmpeg_recorder import (
    ffmpeg_input_args, sha256_file, wav_duration_seconds,
)


def test_ffmpeg_input_args():
    assert ffmpeg_input_args("pulse", "@DEFAULT_MONITOR@") == [
        "-f", "pulse", "-i", "@DEFAULT_MONITOR@"
    ]


def test_dshow_needs_audio_prefix():
    with pytest.raises(ValueError):
        ffmpeg_input_args("dshow", "Microphone")


def test_recording_helpers(tmp_path):
    file = tmp_path / "test.wav"
    with wave.open(str(file), "wb") as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(16000)
        output.writeframes(b"\0\0" * 16000)
    assert wav_duration_seconds(file) == 1
    assert len(sha256_file(file)) == 64
