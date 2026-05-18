"""
CLI: Convert a PNG to SVG using the Stage 1 pipeline.

Usage:
    python scripts/convert_png.py input/myfile.png
    python scripts/convert_png.py input/myfile.png --output output/svg --no-preprocess
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pipeline.stage1_png_to_svg import png_to_svg


def main():
    parser = argparse.ArgumentParser(description="Convert PNG artwork to clean SVG.")
    parser.add_argument("input", help="Path to source PNG file")
    parser.add_argument("--output", "-o", default=None,
                        help="Output directory (default: output/svg/)")
    parser.add_argument("--no-preprocess", action="store_true",
                        help="Skip binarization preprocessing step")
    args = parser.parse_args()

    png_path = Path(args.input)
    out_dir = Path(args.output) if args.output else Path(__file__).parent.parent / "output" / "svg"

    print(f"\nConverting: {png_path.name}")
    print(f"Output dir: {out_dir}\n")

    result = png_to_svg(png_path, out_dir, preprocess=not args.no_preprocess)

    if result:
        print(f"\n✓ Done: {result}")
    else:
        print("\n✗ Conversion failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
