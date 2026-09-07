"""Streamlit wrapper for the Python-generated Electric City scene."""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Electric City · City of Dreams", page_icon="🌃", layout="wide")
st.title("Electric City · Studio")
st.caption(
    "Python generates the renderer, camera system, height classes, and deployment. "
    "ArcGIS streams the public NYC 3-D building meshes in the browser."
)
components.html((ROOT / "docs" / "index.html").read_text(encoding="utf-8"), height=820)
