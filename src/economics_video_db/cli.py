"""Small CLI; intentionally separate capture from future ASR/analysis."""

import argparse
from pathlib import Path
import shutil
import sys

from .capture import capture_one


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="evdb", description="Economics video DB")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Check local external executables")
    capture = sub.add_parser("capture-one", help="Operator-assisted Douyin audio capture")
    capture.add_argument("--url", required=True, help="HTTPS Douyin video URL")
    capture.add_argument("--video-id", help="Explicit ID for a short URL")
    capture.add_argument(
        "--backend", choices=["avfoundation", "pulse", "dshow"], required=True,
        help="FFmpeg input backend",
    )
    capture.add_argument(
        "--device", required=True, help="Audio loopback input source, not an output device"
    )
    capture.add_argument("--data-dir", type=Path, default=Path("data"))
    capture.add_argument(
        "--rights-ok", action="store_true",
        help="Confirm you have permission for this recording and intended usage",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = make_parser().parse_args(argv)
    if args.command == "doctor":
        for command in ("ffmpeg", "browser-harness"):
            print(f"{command}: {shutil.which(command) or 'NOT FOUND'}")
        print("Audio source routing and Chrome permission require manual verification.")
        return 0
    if args.command == "capture-one":
        try:
            capture_one(
                url=args.url, video_id=args.video_id, backend=args.backend,
                device=args.device, data_dir=args.data_dir,
                rights_confirmed=args.rights_ok,
            )
            return 0
        except (ValueError, RuntimeError, KeyboardInterrupt) as exc:
            print("Capture not completed:", exc, file=sys.stderr)
            return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
