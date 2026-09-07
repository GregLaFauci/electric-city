"""Streamlit entry point for the Electric City explorer."""

from pathlib import Path

import streamlit as st

from nyc_skyline.data import enrich_boundaries, enrich_features, filter_boroughs, load_geojson
from nyc_skyline.render import build_deck

DATA_PATH = Path(__file__).parent / "docs" / "data" / "manhattan_buildings.geojson"
BOUNDARIES_PATH = Path(__file__).parent / "data" / "borough_boundaries.geojson"

st.set_page_config(
    page_title="Electric City · City of Dreams",
    page_icon="🗽",
    layout="wide",
)
st.markdown(
    """
    <style>
      .stApp { background: #030814; color: #f6fbff; }
      [data-testid="stSidebar"] { background: #07111f; }
      h1 { letter-spacing: -.055em; }
      .eyebrow { color:#00e5ff; font-weight:700; letter-spacing:.16em; text-transform:uppercase; }
      .metric { color:#8fa7bd; margin-top:-.7rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def sample() -> dict:
    return load_geojson(DATA_PATH)


st.markdown('<p class="eyebrow">Manhattan after midnight · Python × public data</p>', unsafe_allow_html=True)
st.title("Electric City")
st.markdown(
    "**City of Dreams.** Every Manhattan building with a recorded roof height, "
    "extruded into a synthwave night drive. Drag to orbit, scroll to zoom, and hover to inspect."
)

with st.sidebar:
    st.header("Tune the dream")
    exaggeration = st.slider("Skyline boost", 0.5, 2.5, 1.0, 0.05)
    st.caption(
        "Building geometry and roof heights come from NYC OTI's public Building "
        "Footprints dataset. The view includes the complete Manhattan subset with "
        "plausible recorded roof heights."
    )

city = enrich_features(sample(), exaggeration)
boundaries = enrich_boundaries(load_geojson(BOUNDARIES_PATH))
visible = city
visible_boundaries = filter_boroughs(boundaries, ["Manhattan"])
st.pydeck_chart(
    build_deck(
        visible,
        boundaries=visible_boundaries,
    ),
    use_container_width=True,
)
st.markdown(
    f'<p class="metric">{len(visible["features"]):,} real building footprints · '
    f'Manhattan complete · heights × {exaggeration:.2f}</p>',
    unsafe_allow_html=True,
)
