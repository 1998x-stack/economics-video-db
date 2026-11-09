"""Use browser-harness as a separate CLI; never reach into its private APIs.

See upstream SKILL.md: browser-harness accepts Python snippets on stdin.
The tab is created without foreground activation. We do not automate login.
"""

import json
import shutil
import subprocess

from .douyin import validate_url

MARKER = "EVDB_PAGE_JSON:"


class BrowserHarnessError(RuntimeError):
    pass


def open_douyin_video(url: str, *, timeout_seconds: int = 120) -> dict:
    validate_url(url)
    if not shutil.which("browser-harness"):
        raise BrowserHarnessError(
            "browser-harness is not installed. See docs/AUDIO_CAPTURE.md"
        )
    script = (
        "import json\n"
        + "new_tab(" + json.dumps(url, ensure_ascii=False) + ")\n"
        + "wait_for_load()\n"
        + "print(" + json.dumps(MARKER) + " + json.dumps(page_info(), ensure_ascii=False))\n"
    )
    try:
        result = subprocess.run(
            ["browser-harness"],
            input=script,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise BrowserHarnessError("browser-harness timed out opening the video") from exc

    if result.returncode:
        raise BrowserHarnessError(
            "browser-harness failed (see its local diagnostics): "
            + (result.stderr or result.stdout)[-700:]
        )
    for line in reversed(result.stdout.splitlines()):
        if MARKER in line:
            try:
                return json.loads(line.split(MARKER, 1)[1])
            except json.JSONDecodeError as exc:
                raise BrowserHarnessError("Malformed browser page metadata") from exc
    raise BrowserHarnessError("browser-harness did not return page metadata")
