import pytest

from economics_video_db.ingestion.douyin import (
    infer_video_id, validate_url, validate_video_id,
)


def test_video_id_from_direct_link():
    assert infer_video_id("https://www.douyin.com/video/7275916556641652027") == "7275916556641652027"


def test_video_id_from_jingxuan():
    assert infer_video_id("https://jingxuan.douyin.com/m/video/7572995854828406117") == "7572995854828406117"


def test_short_link_requires_resolution_or_explicit_id():
    assert infer_video_id("https://v.douyin.com/abc123/") is None


@pytest.mark.parametrize("url", [
    "http://www.douyin.com/video/123456789012",
    "https://notdouyin.com/video/123456789012",
    "https://www.douyin.com.evil.test/video/123456789012",
    "https://user:password@www.douyin.com/video/123456789012",
])
def test_rejects_unsafe_urls(url):
    with pytest.raises(ValueError):
        validate_url(url)


def test_video_id_path_safety():
    with pytest.raises(ValueError):
        validate_video_id("../../traversal")
