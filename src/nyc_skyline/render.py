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


def dream_trails() -> list[dict[str, Any]]:
    """Art-directed light trails that frame Manhattan like a night drive."""
    return [
        {
            "path": [
                [-74.0132, 40.7030], [-74.0150, 40.7165], [-74.0125, 40.7350],
                [-74.0088, 40.7540], [-74.0048, 40.7740], [-73.9955, 40.7975],
                [-73.9348, 40.8725],
            ],
            "color": [0, 229, 255, 210],
        },
        {
            "path": [
                [-74.0090, 40.7065], [-73.9985, 40.7285], [-73.9875, 40.7520],
                [-73.9795, 40.7695], [-73.9690, 40.7915], [-73.9495, 40.8210],
                [-73.9330, 40.8670],
            ],
            "color": [255, 48, 144, 220],
        },
        {
            "path": [
                [-74.0030, 40.7095], [-73.9735, 40.7360], [-73.9680, 40.7610],
                [-73.9525, 40.7880], [-73.9345, 40.8350], [-73.9220, 40.8780],
            ],
            "color": [255, 174, 74, 190],
        },
    ]


def build_deck(
    buildings: Any,
    *,
    boundaries: dict[str, Any] | None = None,
    show_trails: bool = True,
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
    if show_trails:
        layers.append(
            pdk.Layer(
                "PathLayer",
                dream_trails(),
                id="dream-trails",
                get_path="path",
                get_color="color",
                get_width=8,
                width_min_pixels=1.4,
                joint_rounded=True,
                cap_rounded=True,
                opacity=0.8,
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
