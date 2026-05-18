"""
Stage 1: PNG → Clean SVG

Converts high-contrast PNG artwork to clean SVG using vtracer (preferred)
or falls back to Inkscape CLI trace. Potrace is available as a last resort
but produces inferior results on organic/cursive shapes.
"""

import subprocess
import shutil
from pathlib import Path


def convert_with_vtracer(png_path: Path, svg_path: Path, color_mode: str = "bw") -> bool:
    """
    Trace PNG with vtracer. Best choice for organic/cursive art.

    color_mode: "bw" for black-and-white source, "color" for multi-color
    Returns True on success.
    """
    if not shutil.which("vtracer"):
        print("  [!] vtracer not found in PATH.")
        print("      Install: cargo install vtracer")
        print("      Or grab binary: https://github.com/visioncortex/vtracer/releases")
        return False

    cmd = [
        "vtracer",
        "--input", str(png_path),
        "--output", str(svg_path),
        "--colormode", color_mode,
        "--mode", "spline",         # spline paths — smoother than polygon
        "--corner_threshold", "60", # higher = fewer corners on organic shapes
        "--length_threshold", "4.0",# minimum path segment length
        "--splice_threshold", "45",
        "--filter_speckle", "4",    # remove small noise pixels
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  [✓] vtracer → {svg_path.name}")
        return True
    else:
        print(f"  [✗] vtracer failed: {result.stderr.strip()}")
        return False


def convert_with_inkscape(png_path: Path, svg_path: Path) -> bool:
    """Trace PNG using Inkscape CLI (centerline or brightness-cutoff trace)."""
    if not shutil.which("inkscape"):
        print("  [!] Inkscape not found in PATH.")
        return False

    cmd = [
        "inkscape",
        str(png_path),
        "--export-type=svg",
        f"--export-filename={svg_path}",
        "--actions=select-all;object-trace;",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode == 0:
        print(f"  [✓] Inkscape → {svg_path.name}")
        return True
    else:
        print(f"  [✗] Inkscape trace failed: {result.stderr.strip()}")
        return False


def preprocess_png(png_path: Path, out_path: Path, threshold: int = 128) -> Path:
    """
    Optional preprocessing: binarize and clean up a PNG before tracing.
    Helps when source has gray fringing or antialiasing artifacts.
    """
    try:
        import cv2
        import numpy as np

        img = cv2.imread(str(png_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Could not read {png_path}")

        # Gaussian blur to reduce noise, then hard threshold
        blurred = cv2.GaussianBlur(img, (3, 3), 0)
        _, binary = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)

        # Morphological close to fill small gaps in letters
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        cv2.imwrite(str(out_path), cleaned)
        print(f"  [✓] Preprocessed → {out_path.name}")
        return out_path
    except ImportError:
        print("  [!] opencv-python not installed — skipping preprocessing.")
        return png_path


def png_to_svg(png_path: str | Path, output_dir: str | Path = None,
               preprocess: bool = True) -> Path | None:
    """
    Main entry point. Tries vtracer first, falls back to Inkscape.

    Returns the output SVG path or None on failure.
    """
    png_path = Path(png_path)
    if not png_path.exists():
        print(f"  [✗] Input not found: {png_path}")
        return None

    if output_dir is None:
        output_dir = png_path.parent
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    work_png = png_path
    if preprocess:
        preprocessed = output_dir / f"{png_path.stem}_prep.png"
        work_png = preprocess_png(png_path, preprocessed)

    svg_path = output_dir / f"{png_path.stem}.svg"

    if convert_with_vtracer(work_png, svg_path):
        return svg_path
    if convert_with_inkscape(work_png, svg_path):
        return svg_path

    print("  [✗] All tracers failed. Check tool installation.")
    return None
