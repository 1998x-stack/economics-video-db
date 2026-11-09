"""Operator-controlled FFmpeg WAV recording of an explicitly selected input.

This records the OS input device, NOT a CDP browser-harness recording.
Call start before playback and stop after playback. Do not record microphone
or other apps unless specifically intended and authorized.
"""

from pathlib import Path
import hashlib
import shutil
import subprocess
import time
import wave


def ffmpeg_input_args(backend: str, device: str) -> list[str]:
    if not device:
        raise ValueError("Audio device/source must not be empty")
    if backend not in {"avfoundation", "pulse", "dshow"}:
        raise ValueError("Unsupported backend: " + backend)
    if backend == "dshow" and not device.startswith("audio="):
        raise ValueError("dshow device must use audio=DEVICE syntax")
    return ["-f", backend, "-i", device]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def wav_duration_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as source:
        return source.getnframes() / source.getframerate()


class FFmpegRecorder:
    def __init__(self, output: Path, backend: str, device: str):
        self.output = Path(output)
        self.partial = self.output.with_suffix(".partial.wav")
        self.log_path = self.output.with_suffix(".ffmpeg.log")
        self.backend = backend
        self.device = device
        self.process: subprocess.Popen | None = None
        self._log = None

    def start(self) -> None:
        if self.process is not None:
            raise RuntimeError("Recorder already started")
        if not shutil.which("ffmpeg"):
            raise RuntimeError("ffmpeg is not on PATH")
        self.output.parent.mkdir(parents=True, exist_ok=True)
        self._log = self.log_path.open("wb")
        args = [
            "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
            *ffmpeg_input_args(self.backend, self.device),
            "-vn", "-ac", "1", "-ar", "16000",
            "-c:a", "pcm_s16le", str(self.partial),
        ]
        try:
            self.process = subprocess.Popen(
                args, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                stderr=self._log,
            )
            time.sleep(0.7)
            if self.process.poll() is not None:
                raise RuntimeError(
                    "ffmpeg exited immediately; check " + str(self.log_path)
                )
        except Exception:
            self.abort()
            raise

    def stop(self) -> float:
        if self.process is None:
            raise RuntimeError("Recorder has not started")
        process = self.process
        try:
            if process.stdin:
                process.stdin.write(b"q\n")
                process.stdin.flush()
                process.stdin.close()
            try:
                code = process.wait(timeout=20)
            except subprocess.TimeoutExpired:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
                raise RuntimeError("ffmpeg did not stop cleanly")
        finally:
            self.process = None
            self._close_log()
        if code != 0 or not self.partial.exists():
            raise RuntimeError("Recording failed; inspect " + str(self.log_path))
        try:
            seconds = wav_duration_seconds(self.partial)
        except (wave.Error, EOFError) as exc:
            raise RuntimeError("Invalid WAV file") from exc
        if seconds < 0.5:
            raise RuntimeError("Recording is shorter than 0.5 seconds")
        self.partial.replace(self.output)
        return seconds

    def abort(self) -> None:
        if self.process is not None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)
            self.process = None
        self._close_log()
        self.partial.unlink(missing_ok=True)

    def _close_log(self) -> None:
        if self._log is not None:
            self._log.close()
            self._log = None
