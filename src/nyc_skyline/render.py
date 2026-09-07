"""PyDeck scene composition for Electric Boroughs."""

from __future__ import annotations

from typing import Any

import pydeck as pdk

from .data import BOROUGHS

CITY_VIEW = pdk.ViewState(
    latitude=40.706,
    longitude=-73.94,
    zoom=10.45,
    pitch=44,
    bearing=-19,
)


def connection_arcs() -> list[dict[str, Any]]:
    """Create a five-borough ring plus links to Manhattan."""
    manhattan = BOROUGHS[0]
    arcs = []
    for index, borough in enumerate(BOROUGHS):
        next_borough = BOROUGHS[(index + 1) % len(BOROUGHS)]
        arcs.append(
            {
                "source": borough.center,
                "target": next_borough.center,
                "source_color": [*borough.color, 185],
                "target_color": [*next_borough.color, 185],
            }
        )
        if borough.code != 1:
            arcs.append(
                {
                    "source": borough.center,
                    "target": manhattan.center,
                    "source_color": [*borough.color, 120],
                    "target_color": [*manhattan.color, 120],
                }
            )
    return arcs


def build_deck(
    buildings: dict[str, Any],
    *,
    boundaries: dict[str, Any] | None = None,
    show_connections: bool = True,
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
                opacity=0.22,
                get_fill_color="properties.fill_color",
                get_line_color="properties.line_color",
                line_width_min_pixels=1.3,
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
            opacity=0.92,
            get_elevation="properties.render_height",
            get_fill_color="properties.fill_color",
            get_line_color="properties.line_color",
            line_width_min_pixels=0.45,
        )
    )
    if show_connections:
        layers.append(
            pdk.Layer(
                "LineLayer",
                connection_arcs(),
                id="borough-connections",
                get_source_position="source",
                get_target_position="target",
                get_source_color="source_color",
                get_target_color="target_color",
                get_width=1.5,
                width_min_pixels=0.8,
                opacity=0.55,
            )
        )

    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state or CITY_VIEW,
        map_provider="carto",
        map_style=pdk.map_styles.DARK,
        tooltip={
            "html": (
                "<b>{borough}</b><br/>"
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
