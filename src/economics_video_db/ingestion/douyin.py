"""Validate known Douyin video links; no private endpoints or bypasses."""

import re
from urllib.parse import parse_qs, urlsplit

ALLOWED_HOSTS = frozenset(
    {"douyin.com", "www.douyin.com", "v.douyin.com", "jingxuan.douyin.com"}
)
_VIDEO_RE = re.compile(r"/video/([0-9]{12,25})(?:/|$)")
_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{3,64}$")


def validate_url(url: str) -> str:
    """Only permit user-specified HTTPS Douyin video pages."""
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.hostname not in ALLOWED_HOSTS
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port not in (None, 443)
    ):
        raise ValueError("Expected an HTTPS URL on a known douyin.com host")
    return url


def infer_video_id(url: str) -> str | None:
    parsed = urlsplit(validate_url(url))
    found = _VIDEO_RE.search(parsed.path)
    if found:
        return found.group(1)
    possible = parse_qs(parsed.query).get("modal_id", [])
    if possible and possible[0].isdigit() and len(possible[0]) <= 25:
        return possible[0]
    return None


def validate_video_id(video_id: str) -> str:
    if not _SAFE_ID_RE.fullmatch(video_id):
        raise ValueError("Invalid video ID; use 3-64 letters, digits, _ or -")
    return video_id
