"""Streamlit entry point for the Electric Boroughs explorer."""

from pathlib import Path

import streamlit as st

from nyc_skyline.data import (
    BOROUGHS,
    enrich_boundaries,
    enrich_features,
    filter_boroughs,
    load_geojson,
)
from nyc_skyline.render import build_deck

DATA_PATH = Path(__file__).parent / "data" / "skyline_sample.geojson"
BOUNDARIES_PATH = Path(__file__).parent / "data" / "borough_boundaries.geojson"

st.set_page_config(
    page_title="Electric Boroughs · NYC in 3D",
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


st.markdown('<p class="eyebrow">Python × NYC Open Data</p>', unsafe_allow_html=True)
st.title("Electric Boroughs")
st.markdown(
    "A living 3D portrait of New York: five boroughs, one skyline, and public data "
    "extruded into light. Drag to orbit, scroll to zoom, and hover over a building."
)

with st.sidebar:
    st.header("Shape the city")
    selected = st.multiselect(
        "Boroughs",
        [borough.name for borough in BOROUGHS],
        default=[borough.name for borough in BOROUGHS],
    )
    exaggeration = st.slider("Vertical energy", 0.5, 3.0, 1.35, 0.05)
    connections = st.toggle("Borough pulse lines", value=True)
    st.caption(
        "Building geometry and roof heights come from NYC OTI's public Building "
        "Footprints dataset. The bundled view samples the tallest structures equally "
        "from every borough."
    )

city = enrich_features(sample(), exaggeration)
visible = filter_boroughs(city, selected)
boundaries = enrich_boundaries(load_geojson(BOUNDARIES_PATH))
visible_boundaries = filter_boroughs(boundaries, selected)
st.pydeck_chart(
    build_deck(
        visible,
        boundaries=visible_boundaries,
        show_connections=connections,
    ),
    use_container_width=True,
)
st.markdown(
    f'<p class="metric">{len(visible["features"]):,} real building footprints · '
    f'{len(selected)} boroughs visible · heights × {exaggeration:.2f}</p>',
    unsafe_allow_html=True,
)
