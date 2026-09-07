from nyc_skyline.data import (
    BOROUGHS,
    borough_code_from_bin,
    enrich_boundaries,
    enrich_features,
    filter_boroughs,
    query_params,
)


def feature(bin_value="1000001", height="100"):
    return {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": []},
        "properties": {"bin": bin_value, "height_roof": height},
    }


def test_borough_code_comes_from_bin():
    assert borough_code_from_bin("3001234") == 3
    assert borough_code_from_bin(None) is None
    assert borough_code_from_bin("9001234") is None


def test_query_is_scoped_to_one_borough():
    params = query_params(BOROUGHS[2], 25)
    assert "bin >= 3000000" in params["$where"]
    assert "bin < 4000000" in params["$where"]
    assert params["$limit"] == 25


def test_enrichment_converts_feet_and_adds_identity():
    result = enrich_features({"type": "FeatureCollection", "features": [feature()]}, 2)
    props = result["features"][0]["properties"]
    assert props["borough"] == "Manhattan"
    assert props["render_height"] == 60.96
    assert len(props["fill_color"]) == 4


def test_enrichment_drops_impossible_height_outliers():
    result = enrich_features(
        {"type": "FeatureCollection", "features": [feature("2000001", "2130353")]}
    )
    assert result["features"] == []


def test_filter_boroughs():
    result = enrich_features(
        {"type": "FeatureCollection", "features": [feature(), feature("3000001")]}
    )
    filtered = filter_boroughs(result, ["Brooklyn"])
    assert len(filtered["features"]) == 1
    assert filtered["features"][0]["properties"]["borough"] == "Brooklyn"


def test_boundary_palette_uses_official_borough_code():
    result = enrich_boundaries(
        {
            "type": "FeatureCollection",
            "features": [{"type": "Feature", "properties": {"borocode": "5"}}],
        }
    )
    assert result["features"][0]["properties"]["borough"] == "Staten Island"
