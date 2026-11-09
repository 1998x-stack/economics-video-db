from economics_video_db.cli import make_parser


def test_capture_requires_explicit_source():
    p = make_parser()
    args = p.parse_args([
        "capture-one", "--url", "https://www.douyin.com/video/7275916556641652027",
        "--backend", "pulse", "--device", "@DEFAULT_MONITOR@", "--rights-ok"
    ])
    assert args.rights_ok is True
    assert args.backend == "pulse"
