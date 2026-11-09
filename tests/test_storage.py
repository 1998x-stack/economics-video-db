import json

from economics_video_db.storage import write_manifest


def test_atomic_manifest(tmp_path):
    path = tmp_path / "catalog" / "id.json"
    write_manifest(path, {"hello": "财经"})
    assert json.loads(path.read_text(encoding="utf-8")) == {"hello": "财经"}
    assert not path.with_suffix(".json.tmp").exists()
