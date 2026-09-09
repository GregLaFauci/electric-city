from nyc_skyline.render import (
    BQE_ROUTE,
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


def test_bqe_drive_reveals_skyline_then_removes_intro_route():
    html = build_html()
    assert "BQE NIGHT RUN" in html
    assert "CITY OF DREAMS" in html
    assert "BROOKLYN HEIGHTS · SLOW MOTION" in html
    assert 'id="skipDrive"' in html
    assert 'id="replayDrive"' in html
    assert "map.add(introRoad,0)" in html
    assert "map.remove(introRoad)" in html
    assert "driveIntro.classList.add(\"to-map\")" in html
    assert len(BQE_ROUTE) >= 10


def test_bqe_drive_respects_reduced_motion():
    html = build_html()
    assert 'matchMedia("(prefers-reduced-motion: reduce)")' in html
    assert "if(reduceMotion)endDriveImmediately()" in html


def test_idle_mode_cycles_real_sun_without_moving_camera():
    html = build_html()
    assert "setTimeout(startOrbit,18000)" in html
    assert 'view.environment.lighting={type:"sun",date:simulatedTime,directShadowsEnabled:true}' in html
    assert "view.environment.lighting.date=simulatedTime" in html
    assert "setInterval(updateOrbit,200)" in html
    start_orbit = html.split("function startOrbit()", 1)[1].split("function stopOrbit()", 1)[0]
    assert "view.camera=" not in start_orbit


def test_idle_mode_uses_calculated_moon_and_wakes_on_activity():
    html = build_html()
    assert "suncalc@2.0.1/+esm" in html
    assert "getMoonPosition(date,40.758,-73.9855)" in html
    assert "getMoonIllumination(date)" in html
    assert 'id="orbitHud"' in html
    assert '["pointerdown","pointermove","touchstart","wheel","keydown"]' in html
    assert 'view.environment.lighting={type:"virtual"' in html
