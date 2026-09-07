# Electric City

**City of Dreams — every Manhattan building rendered as a 1990s night drive.**

Electric City turns 45,059 public building footprints and recorded roof heights
into an explorable synthwave Manhattan. Low-rise blocks glow cyan, mid-rise
buildings shift through violet, towers burn magenta, and the tallest landmarks
catch the orange horizon.

![Electric City overview](readme-resources/img/overview.png)

## The idea

The inspiration is the feeling of a 1990s arcade racer at midnight: an endless
city ahead, neon lanes pulling toward the horizon, and Manhattan rising out of
the dark. The spectacle is data-driven. Every visible building is a real NYC
footprint, and every extrusion uses its public `height_roof` value.

The official [NYC 3-D Building Model][3d-model] represents every building in
the 2014 aerial survey as CityGML. Its 894 MB archive expands to many gigabytes,
so Electric City uses NYC OTI's actively maintained [Building Footprints][footprints]
API for a lighter, browser-ready rendering of the complete Manhattan subset.
The island silhouette comes from NYC Planning's current [Borough Boundaries][boundaries]
release.

## Run the interactive studio

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
streamlit run app.py
```

Drag to orbit, scroll to travel through the island, hover to inspect a building,
and adjust the skyline boost.

## Rebuild from NYC Open Data

```bash
python scripts/fetch_manhattan.py
python scripts/build_demo.py
pytest
```

The downloader works in 1,000-record pages with bounded concurrency because a
single 45,000-feature request overwhelms the public Socrata endpoint. The build
step validates heights, converts feet to meters, assigns the height-driven neon
palette, and writes a serverless PyDeck experience to `docs/` for GitHub Pages.

## Honest data notes

- Scope: 45,059 Manhattan footprints returned during the current refresh
- Geometry: WGS84 GeoJSON polygons from NYC OTI
- Height: `height_roof` in feet, converted to meters for Deck.gl
- Validation: records above 2,000 feet are excluded as impossible source anomalies
- Color: an artistic height classification, not a statistical category
- Original 3D capture: 2014 aerial survey, hybrid CityGML LOD 1/2
- Footprints: maintained public basemap, updated separately from the historical model

Public data remains subject to the [NYC Open Data Terms of Use][terms].

## Stack

Python · Streamlit · PyDeck / Deck.gl · Socrata API · GeoJSON · pytest

[3d-model]: https://data.cityofnewyork.us/City-Government/3-D-Building-Model/tnru-abg2
[footprints]: https://data.cityofnewyork.us/d/3g6p-4u5s
[boundaries]: https://data.cityofnewyork.us/d/gthc-hcne
[terms]: https://opendata.cityofnewyork.us/overview/#termsofuse
