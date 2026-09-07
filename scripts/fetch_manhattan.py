#!/usr/bin/env python3
"""Download the complete Manhattan building-footprint subset."""

import argparse
from pathlib import Path

from nyc_skyline.data import fetch_manhattan_all, save_geojson


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--page-size", type=int, default=1000)
    parser.add_argument("--max-pages", type=int, default=60)
    parser.add_argument(
        "--output", type=Path, default=Path("data/manhattan_buildings.geojson")
    )
    args = parser.parse_args()
    collection = fetch_manhattan_all(args.page_size, args.max_pages)
    save_geojson(collection, args.output)
    print(f"Saved {len(collection['features']):,} Manhattan buildings to {args.output}")


if __name__ == "__main__":
    main()
