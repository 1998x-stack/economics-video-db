from types import SimpleNamespace

import pytest

from economics_video_db.ingestion import browser_harness


def test_opens_url_without_shell_interpolation(monkeypatch):
    monkeypatch.setattr(browser_harness.shutil, "which", lambda name: "/fake/bin/browser-harness")
    recorded = {}

    def fake_run(argv, **kwargs):
        recorded.update(argv=argv, kwargs=kwargs)
        return SimpleNamespace(
            returncode=0,
            stdout='info\nEVDB_PAGE_JSON:{"url":"https://www.douyin.com/video/7275916556641652027","title":"sample"}\n',
            stderr="",
        )

    monkeypatch.setattr(browser_harness.subprocess, "run", fake_run)
    page = browser_harness.open_douyin_video(
        "https://www.douyin.com/video/7275916556641652027"
    )
    assert page["title"] == "sample"
    assert recorded["argv"] == ["browser-harness"]
    assert "new_tab(" in recorded["kwargs"]["input"]


def test_missing_binary_is_explicit(monkeypatch):
    monkeypatch.setattr(browser_harness.shutil, "which", lambda name: None)
    with pytest.raises(browser_harness.BrowserHarnessError):
        browser_harness.open_douyin_video(
            "https://www.douyin.com/video/7275916556641652027"
        )
