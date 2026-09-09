from nyc_skyline.render import (
    HEIGHT_CLASSES,
    NAMED_BUILDINGS_WHERE,
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


def test_building_clicks_use_explicit_hit_test_and_popup():
    html = build_html()
    assert 'popupEnabled:false' in html
    assert 'view.hitTest(event,{include:[buildings,liberty,torch]})' in html
    assert 'id="inspector"' in html
    assert 'showInspector(attrs.NAME||"Manhattan Building"' in html
    assert "buildingLayerView?.highlight(feature)" in html
    for field in ("OBJECTID", "NAME", "HEIGHTROOF", "NUM_FLOORS", "CNSTRCT_YR", "GROUNDELEV"):
        assert field in html


def test_scene_loading_uses_guarded_one_shot_reactivity():
    html = build_html()
    assert '"esri/core/reactiveUtils"' in html
    assert "reactiveUtils.whenOnce(()=>!layerView.updating)" in html
    assert 'const loading=document.getElementById("loading");if(!loading)return' in html
    assert 'layerView.watch(' not in html


def test_named_building_search_queries_flies_and_inspects():
    html = build_html()
    assert 'id="buildingSearch"' in html
    assert 'id="searchResults"' in html
    assert "bottom:calc(100% + 8px)" in html
    assert "renderSearchResults" in html
    assert "const NAMED_WHERE=" in html
    assert NAMED_BUILDINGS_WHERE in html
    assert "buildings.queryFeatures(query)" in html
    assert "buildings.queryExtent({objectIds:[record.id]})" in html
    assert "jumpToNamedBuilding" in html
    assert "buildingLayerView?.highlight(record.id)" in html


def test_named_only_toggle_filters_scene_layer_view():
    html = build_html()
    assert 'id="namedOnly"' in html
    assert "buildingLayerView.filter=namedOnly.checked?{where:NAMED_WHERE}:null" in html
    assert "Show only named buildings" in html
