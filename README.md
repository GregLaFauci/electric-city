# Electric Boroughs

**A Python-powered 3D portrait of all five New York City boroughs.**

Electric Boroughs turns public building footprints and real roof heights into
an explorable city of light. Manhattan, The Bronx, Brooklyn, Queens, and Staten
Island each receive a distinct color; glowing arcs make the five-borough system
visible as one connected metropolis.

![Electric Boroughs overview](readme-resources/img/overview.png)

## Why this exists

The official [NYC 3-D Building Model][3d-model] represents every building
present in the 2014 aerial survey. It is an extraordinary CityGML source, but
the 894 MB download expands to many gigabytes and is not ideal for a quick web
demo. This project pairs that source with NYC OTI's actively maintained
[Building Footprints][footprints] dataset. The footprint API supplies geometry,
roof height, construction year, and borough-coded BIN values in browser-ready
GeoJSON.

The luminous ground plane is also public data: NYC Planning's current
[Borough Boundaries][boundaries] release. This keeps the city readable when a
basemap tile is unavailable and makes the five-borough premise explicit.

The committed showcase is a deterministic sample of the 100 tallest structures
from each borough—not a claim that those 500 buildings are the entire city.
The equal sampling is intentional: Staten Island and The Bronx deserve visual
weight alongside Manhattan. Re-run the pipeline with any sample size, or adapt
the loader to process all one-million-plus footprints in tiles.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
streamlit run app.py
```

Then orbit, zoom, filter boroughs, and change the vertical exaggeration from
the sidebar.

## Rebuild from public data

```bash
python scripts/fetch_data.py --per-borough 100
python scripts/build_demo.py
pytest
```

The first command issues one transparent Socrata query per borough. Query
construction, height conversion, borough colors, and filtering live in
`src/nyc_skyline/`; the generated, serverless PyDeck experience is written to
`docs/index.html` for GitHub Pages.

## Data notes

- Source agency: NYC Office of Technology and Innovation (OTI)
- Geometry: building footprint polygons, WGS84 GeoJSON from the Socrata API
- Height: `height_roof`, feet above ground, converted to meters for Deck.gl
- Borough: first digit of the seven-digit Building Identification Number (BIN)
- Original 3D capture: 2014 aerial survey, hybrid CityGML LOD 1/2
- Footprints: maintained public basemap, updated independently of the historical model

Public data remains subject to the [NYC Open Data Terms of Use][terms].

## Stack

Python · Streamlit · PyDeck / Deck.gl · Socrata API · GeoJSON · pytest

[3d-model]: https://data.cityofnewyork.us/City-Government/3-D-Building-Model/tnru-abg2
[footprints]: https://data.cityofnewyork.us/d/3g6p-4u5s
[boundaries]: https://data.cityofnewyork.us/d/gthc-hcne
[terms]: https://opendata.cityofnewyork.us/overview/#termsofuse
