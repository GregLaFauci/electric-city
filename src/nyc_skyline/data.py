"""Download and transform NYC building footprints for 3D rendering."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import requests

DATASET_ID = "5zhs-2jue"
DATASET_PAGE = "https://data.cityofnewyork.us/d/3g6p-4u5s"
API_URL = f"https://data.cityofnewyork.us/resource/{DATASET_ID}.geojson"
FEET_TO_METERS = 0.3048


@dataclass(frozen=True)
class Borough:
    code: int
    name: str
    short_name: str
    color: tuple[int, int, int]
    center: tuple[float, float]


BOROUGHS = (
    Borough(1, "Manhattan", "MN", (0, 229, 255), (-73.9712, 40.7831)),
    Borough(2, "The Bronx", "BX", (255, 76, 133), (-73.8648, 40.8448)),
    Borough(3, "Brooklyn", "BK", (255, 179, 71), (-73.9442, 40.6782)),
    Borough(4, "Queens", "QN", (174, 255, 80), (-73.7949, 40.7282)),
    Borough(5, "Staten Island", "SI", (180, 113, 255), (-74.1534, 40.5795)),
)
BOROUGH_BY_CODE = {borough.code: borough for borough in BOROUGHS}


def borough_code_from_bin(value: Any) -> int | None:
    """Return NYC borough code encoded in the first digit of a BIN."""
    try:
        code = int(str(int(float(value)))[0])
    except (TypeError, ValueError, IndexError):
        return None
    return code if code in BOROUGH_BY_CODE else None


def query_params(borough: Borough, limit: int) -> dict[str, str | int]:
    """Build a deterministic Socrata query for a borough's tallest buildings."""
    floor = borough.code * 1_000_000
    ceiling = (borough.code + 1) * 1_000_000
    return {
        "$select": (
            "the_geom,name,bin,height_roof,ground_elevation,"
            "construction_year,geom_source"
        ),
        "$where": (
            f"bin >= {floor} AND bin < {ceiling} "
            "AND height_roof IS NOT NULL AND height_roof > 8"
        ),
        "$order": "height_roof DESC, bin ASC",
        "$limit": limit,
    }


def fetch_city(limit_per_borough: int = 100, timeout: int = 60) -> dict[str, Any]:
    """Fetch an equal, deterministic skyline sample from all five boroughs."""
    features: list[dict[str, Any]] = []
    with requests.Session() as session:
        session.headers["User-Agent"] = "electric-boroughs/1.0"
        for borough in BOROUGHS:
            response = session.get(
                API_URL,
                params=query_params(borough, limit_per_borough),
                timeout=timeout,
            )
            response.raise_for_status()
            payload = response.json()
            features.extend(payload.get("features", []))
    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "source": DATASET_PAGE,
            "api": API_URL,
            "sampling": "Tallest buildings per borough, ordered by height then BIN",
            "limit_per_borough": limit_per_borough,
        },
    }


def enrich_features(
    collection: dict[str, Any], vertical_exaggeration: float = 1.0
) -> dict[str, Any]:
    """Add typed rendering properties while preserving source attributes."""
    enriched = {**collection, "features": []}
    for feature in collection.get("features", []):
        props = dict(feature.get("properties") or {})
        code = borough_code_from_bin(props.get("bin"))
        if not code:
            continue
        borough = BOROUGH_BY_CODE[code]
        try:
            height_feet = max(float(props.get("height_roof") or 0), 8.0)
        except (TypeError, ValueError):
            height_feet = 8.0
        alpha = min(235, 145 + int(height_feet / 10))
        props.update(
            borough=borough.name,
            borough_code=code,
            height_feet=round(height_feet, 1),
            render_height=round(
                height_feet * FEET_TO_METERS * vertical_exaggeration, 2
            ),
            fill_color=[*borough.color, alpha],
            line_color=[*borough.color, 255],
        )
        enriched["features"].append({**feature, "properties": props})
    return enriched


def filter_boroughs(
    collection: dict[str, Any], names: Iterable[str]
) -> dict[str, Any]:
    """Return a copy containing only selected borough names."""
    selected = set(names)
    return {
        **collection,
        "features": [
            feature
            for feature in collection.get("features", [])
            if feature.get("properties", {}).get("borough") in selected
        ],
    }


def enrich_boundaries(collection: dict[str, Any]) -> dict[str, Any]:
    """Style official borough boundaries with the Electric Boroughs palette."""
    enriched = {**collection, "features": []}
    for feature in collection.get("features", []):
        props = dict(feature.get("properties") or {})
        try:
            borough = BOROUGH_BY_CODE[int(props.get("borocode"))]
        except (KeyError, TypeError, ValueError):
            continue
        props.update(
            borough=borough.name,
            fill_color=[*borough.color, 22],
            line_color=[*borough.color, 145],
        )
        enriched["features"].append({**feature, "properties": props})
    return enriched


def save_geojson(collection: dict[str, Any], path: str | Path) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(collection, separators=(",", ":")), encoding="utf-8")


def load_geojson(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
