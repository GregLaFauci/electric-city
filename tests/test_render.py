from nyc_skyline.render import (
    HEIGHT_CLASSES,
    SCENE_URL,
    STATUE_SCENE_URL,
    TORCH_ELEVATION_METERS,
    build_html,
    scene_renderer,
)


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


def test_html_adds_liberty_mesh_torch_and_camera():
    html = build_html()
    assert STATUE_SCENE_URL in html
    assert f"z:{TORCH_ELEVATION_METERS}" in html
    assert 'data-view="liberty"' in html
    assert "Statue of Liberty" in html


def test_height_legend_exposes_ranges_on_hover_and_focus():
    html = build_html()
    for low, high, label, _ in HEIGHT_CLASSES:
        assert f'data-range="{low:,}–{high:,} ft"' in html
        assert f"{label}: {low:,} to {high:,} feet" in html
    assert ".legend-item:hover::after" in html
    assert ".legend-item:focus::after" in html
