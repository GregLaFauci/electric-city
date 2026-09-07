#!/usr/bin/env python3
"""Refresh the reproducible five-borough sample from NYC Open Data."""

import argparse
from pathlib import Path

from nyc_skyline.data import fetch_city, save_geojson


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-borough", type=int, default=100)
    parser.add_argument(
        "--output", type=Path, default=Path("data/skyline_sample.geojson")
    )
    args = parser.parse_args()
    collection = fetch_city(args.per_borough)
    save_geojson(collection, args.output)
    print(f"Saved {len(collection['features']):,} buildings to {args.output}")


if __name__ == "__main__":
    main()
