"""PyDeck scene composition for Electric City."""

from __future__ import annotations

from typing import Any

import pydeck as pdk

CITY_VIEW = pdk.ViewState(
    latitude=40.754,
    longitude=-73.982,
    zoom=11.15,
    pitch=55,
    bearing=29,
)

ONE_WTC = [
    {
        "name": "One World Trade Center",
        "position": [-74.0133, 40.7127],
        "height": 541.3,
        "height_feet": 1776,
        "bin": "1088469",
        "construction_year": "2009",
        "color": [255, 181, 71, 255],
    }
]


def build_deck(
    buildings: Any,
    *,
    boundaries: dict[str, Any] | None = None,
    view_state: pdk.ViewState | None = None,
) -> pdk.Deck:
    """Compose the interactive 3D city scene."""
    layers: list[pdk.Layer] = []
    if boundaries:
        layers.append(
            pdk.Layer(
                "GeoJsonLayer",
                boundaries,
                id="borough-foundation",
                filled=True,
                stroked=True,
                pickable=False,
                opacity=0.16,
                get_fill_color="properties.fill_color",
                get_line_color="properties.line_color",
                line_width_min_pixels=1.8,
            )
        )
    layers.append(
        pdk.Layer(
            "GeoJsonLayer",
            buildings,
            id="nyc-buildings",
            extruded=True,
            wireframe=True,
            pickable=True,
            auto_highlight=True,
            opacity=0.9,
            get_elevation="properties.render_height",
            get_fill_color="properties.fill_color",
            get_line_color="properties.line_color",
            line_width_min_pixels=0.35,
        )
    )
    layers.append(
        pdk.Layer(
            "ColumnLayer",
            ONE_WTC,
            id="one-wtc-spire",
            pickable=True,
            auto_highlight=True,
            disk_resolution=6,
            radius=6,
            extruded=True,
            get_position="position",
            get_elevation="height",
            get_fill_color="color",
            elevation_scale=1,
        )
    )
    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state or CITY_VIEW,
        map_provider="carto",
        map_style=pdk.map_styles.DARK,
        tooltip={
            "html": (
                "<b>Electric City</b><br/>"
                "{height_feet} ft · BIN {bin}<br/>"
                "Built {construction_year}"
            ),
            "style": {
                "backgroundColor": "#07111f",
                "color": "#f6fbff",
                "fontFamily": "Inter, sans-serif",
            },
        },
    )
