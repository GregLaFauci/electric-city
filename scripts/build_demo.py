#!/usr/bin/env python3
"""Generate the no-server GitHub Pages experience with Python."""

from pathlib import Path

from nyc_skyline.data import enrich_boundaries, enrich_features, load_geojson
from nyc_skyline.render import build_deck

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    buildings = enrich_features(
        load_geojson(ROOT / "data" / "skyline_sample.geojson"), 1.35
    )
    boundaries = enrich_boundaries(
        load_geojson(ROOT / "data" / "borough_boundaries.geojson")
    )
    deck = build_deck(buildings, boundaries=boundaries)
    output = ROOT / "docs" / "index.html"
    deck.to_html(
        str(output),
        open_browser=False,
        css_background_color="#030814",
    )
    html = output.read_text(encoding="utf-8")
    html = html.replace(
        "<body>",
        """<body><header class="project-header">
<p>PYTHON × NYC OPEN DATA</p><h1>Electric Boroughs</h1>
<span>Five boroughs. Real roof heights. One city made of light.</span>
</header><div class="legend"><b>NYC, 2014 → now</b><br>
Drag to orbit · Scroll to zoom · Hover to inspect</div>""",
    ).replace(
        "</style>",
        """
.project-header{position:fixed;z-index:2;top:28px;left:36px;color:#f6fbff;
font:16px/1.25 Inter,system-ui,sans-serif;pointer-events:none;text-shadow:0 2px 18px #030814}
.project-header p{color:#00e5ff;font-size:11px;font-weight:800;letter-spacing:.18em;margin:0 0 5px}
.project-header h1{font-size:42px;letter-spacing:-.055em;margin:0 0 4px}
.project-header span{color:#b9cad8;font-size:13px}
.legend{position:fixed;z-index:2;right:24px;bottom:24px;padding:12px 15px;border:1px solid #26445c;
border-radius:10px;background:#07111fd9;color:#8fa7bd;font:11px/1.6 Inter,system-ui,sans-serif}
.legend b{color:#f6fbff;font-size:12px}
@media(max-width:600px){.project-header{top:18px;left:20px}.project-header h1{font-size:32px}.legend{right:12px;bottom:12px}}
</style>""",
    )
    output.write_text(html, encoding="utf-8")
    print(f"Built {output}")


if __name__ == "__main__":
    main()
