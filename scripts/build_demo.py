#!/usr/bin/env python3
"""Generate the deployable Electric City scene from Python."""

from pathlib import Path

from nyc_skyline.render import build_html

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    output = ROOT / "docs" / "index.html"
    output.write_text(build_html(), encoding="utf-8")
    print(f"Built {output}")


if __name__ == "__main__":
    main()
