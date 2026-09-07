from nyc_skyline.render import HEIGHT_CLASSES, SCENE_URL, build_html, scene_renderer


def test_renderer_covers_full_height_range():
    renderer = scene_renderer()
    assert renderer["field"] == "HEIGHTROOF"
    assert renderer["classBreakInfos"][0]["minValue"] == 0
    assert renderer["classBreakInfos"][-1]["maxValue"] == 2000
    assert len(renderer["classBreakInfos"]) == len(HEIGHT_CLASSES)


def test_html_streams_real_scene_without_synthetic_geometry():
    html = build_html()
    assert SCENE_URL in html
    assert "SceneLayer" in html
    assert "ColumnLayer" not in html
    assert "PathLayer" not in html
    assert "one-wtc-spire" not in html
