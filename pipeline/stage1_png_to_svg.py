"""
Stage 1: PNG → Clean SVG

Converts high-contrast PNG artwork to clean SVG using:
  1. vtracer CLI (best quality, needs: cargo install vtracer)
  2. OpenCV contours (built-in fallback, works with just opencv-python)
  3. Inkscape CLI (last resort)
"""

import subprocess
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def convert_with_vtracer(png_path: Path, svg_path: Path, color_mode: str = "bw") -> bool:
    """Trace PNG with vtracer CLI. Best quality for organic/cursive art."""
    # vtracer Python wheel segfaults on Python 3.14 — CLI only.
    if not shutil.which("vtracer"):
        return False

    cmd = [
        "vtracer",
        "--input", str(png_path),
        "--output", str(svg_path),
        "--colormode", color_mode,
        "--mode", "spline",
        "--corner_threshold", "60",
        "--segment_length", "4.0",
        "--splice_threshold", "45",
        "--filter_speckle", "4",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  [✓] vtracer → {svg_path.name}")
        return True
    print(f"  [✗] vtracer failed: {result.stderr.strip()}")
    return False


def convert_with_contours(png_path: Path, svg_path: Path,
                          min_area: int = 20, epsilon_factor: float = 0.002) -> bool:
    """
    Trace PNG using OpenCV contour detection.

    Finds all dark regions, approximates their outlines as polygons,
    and writes them as separate SVG <path> elements. Each disconnected
    shape (letter, outline, etc.) becomes its own path — no blobs.

    min_area:       ignore contours smaller than this many pixels (noise filter)
    epsilon_factor: contour approximation tolerance (higher = fewer nodes)
    """
    try:
        import cv2
        import numpy as np
    except ImportError:
        return False

    img = cv2.imread(str(png_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return False

    h, w = img.shape

    # Invert so dark artwork → white foreground for findContours
    inv = cv2.bitwise_not(img)

    # RETR_CCOMP: two-level hierarchy — outer contours + their holes (letters with counters)
    contours, hierarchy = cv2.findContours(inv, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)

    if not contours:
        print("  [!] No contours found.")
        return False

    paths = []
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue

        # Approximate the contour to reduce node count
        eps = epsilon_factor * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, eps, True)

        if len(approx) < 3:
            continue

        # Build SVG path data from the approximated polygon points
        pts = approx.reshape(-1, 2)
        d = f"M {pts[0][0]},{pts[0][1]}"
        for x, y in pts[1:]:
            d += f" L {x},{y}"
        d += " Z"
        paths.append(d)

    if not paths:
        print("  [!] No usable contours after filtering.")
        return False

    # Write a clean SVG with white background + black paths
    path_elements = "\n  ".join(
        f'<path d="{d}" fill="#000000" fill-rule="evenodd"/>'
        for d in paths
    )
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" fill="white"/>
  {path_elements}
</svg>
"""
    svg_path.write_text(svg, encoding="utf-8")
    print(f"  [✓] OpenCV contours ({len(paths)} paths) → {svg_path.name}")
    return True


INKSCAPE_PATHS = [
    r"C:\Program Files\Inkscape\bin\inkscape.exe",
    "inkscape",
]

def _inkscape_exe() -> str | None:
    for candidate in INKSCAPE_PATHS:
        if shutil.which(candidate) or Path(candidate).exists():
            return candidate
    return None


def convert_with_inkscape(png_path: Path, svg_path: Path) -> bool:
    """Last-resort Inkscape trace (centerline, single scan)."""
    exe = _inkscape_exe()
    if not exe:
        return False

    # Invert so Inkscape traces the bright (artwork) region
    try:
        import cv2
        inv_path = png_path.parent / f"{png_path.stem}_inv.png"
        img = cv2.imread(str(png_path), cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(str(inv_path), cv2.bitwise_not(img))
        trace_src = inv_path
    except ImportError:
        trace_src = png_path

    cmd = [
        exe,
        str(trace_src),
        "--export-type=svg",
        f"--export-filename={svg_path}",
        "--actions=select-all;object-trace:1,true,false,false,2,1.0,0.2;",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode == 0:
        print(f"  [✓] Inkscape → {svg_path.name}")
        return True
    print(f"  [✗] Inkscape trace failed: {result.stderr.strip()}")
    return False


def preprocess_png(png_path: Path, out_path: Path, threshold: int = 128) -> Path:
    """
    Binarize and clean a PNG before tracing.
    Converts RGBA/color sources to clean black-on-white binary.
    """
    try:
        import cv2
        import numpy as np

        img = cv2.imread(str(png_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Could not read {png_path}")

        blurred = cv2.GaussianBlur(img, (3, 3), 0)
        _, binary = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)

        # Close small gaps in letterforms
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
    Main entry point. Priority: vtracer CLI → OpenCV contours → Inkscape.
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
    if convert_with_contours(work_png, svg_path):
        return svg_path
    if convert_with_inkscape(work_png, svg_path):
        return svg_path

    print("  [✗] All tracers failed. Check tool installation.")
    return None
