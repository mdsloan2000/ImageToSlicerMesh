"""
get_started.py — Session launcher for the Image to Slicer Ready Mesh pipeline.
Run this at the start of each work session to get a status recap and tool check.
"""

import sys
import subprocess
import importlib.util
from pathlib import Path

# Force UTF-8 output so Unicode arrows/checkmarks render on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).parent

# ── Pipeline stage definitions ────────────────────────────────────────────────
STAGES = [
    ("1", "PNG → Clean SVG",           "ACTIVE — improving tracer quality (vtracer recommended)"),
    ("2", "SVG → Plasticity import",   "In progress"),
    ("3", "Plasticity: extrude/fillet","In progress — Bell Pepper fillets underway"),
    ("4", "Export → OrcaSlicer .3mf",  "Pending"),
    ("5", "Slicer prep & filament",    "Pending"),
]

ACTIVE_PROJECTS = [
    ("Bell Pepper Stake", r"D:\Repos\VeggieProject\PlasticityWork\plasticity\bell_pepper_master_curve.plasticity"),
    ("Tomato Stake",      r"D:\Repos\VeggieProject\PlasticityWork\plasticity\tomato_master_curve.plasticity"),
]

# ── Tool checks ───────────────────────────────────────────────────────────────
def check_python_pkg(name):
    return importlib.util.find_spec(name) is not None

def check_cli(cmd):
    try:
        subprocess.run([cmd, "--version"], capture_output=True, timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def check_vtracer():
    try:
        import vtracer  # noqa: F401
        return True
    except ImportError:
        pass
    try:
        result = subprocess.run(["vtracer", "--help"], capture_output=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

# ── Display helpers ───────────────────────────────────────────────────────────
def header(text):
    bar = "=" * 60
    print(f"\n{bar}")
    print(f"  {text}")
    print(bar)

def row(label, status, ok=True):
    icon = "✓" if ok else "✗"
    print(f"  [{icon}] {label:<30} {status}")

# ── Main recap ────────────────────────────────────────────────────────────────
def main():
    header("IMAGE TO SLICER MESH — SESSION START")

    print("\n[PIPELINE STATUS]")
    print("-" * 60)
    for num, stage, status in STAGES:
        marker = ">>> " if "ACTIVE" in status else "    "
        print(f"  {marker}Stage {num}: {stage}")
        print(f"         {status}")

    print("\n[ACTIVE PROJECTS]")
    print("-" * 60)
    for name, path in ACTIVE_PROJECTS:
        exists = Path(path).exists()
        state = "found" if exists else "NOT FOUND -- check path"
        icon = "OK" if exists else "!!"
        print(f"  [{icon}] {name}")
        print(f"       {path}")
        print(f"       Status: {state}")

    print("\n[TOOL CHECK]")
    print("-" * 60)
    row("vtracer (CLI)",         "available" if check_vtracer()           else "MISSING — install: cargo install vtracer",        check_vtracer())
    row("opencv-python",         "available" if check_python_pkg("cv2")   else "MISSING — pip install opencv-python",              check_python_pkg("cv2"))
    row("Pillow",                "available" if check_python_pkg("PIL")   else "MISSING — pip install Pillow",                     check_python_pkg("PIL"))
    row("numpy",                 "available" if check_python_pkg("numpy") else "MISSING — pip install numpy",                      check_python_pkg("numpy"))
    row("svgpathtools",          "available" if check_python_pkg("svgpathtools") else "MISSING — pip install svgpathtools",        check_python_pkg("svgpathtools"))
    row("cairosvg",              "available" if check_python_pkg("cairosvg")    else "MISSING — pip install cairosvg",             check_python_pkg("cairosvg"))
    row("trimesh",               "available" if check_python_pkg("trimesh")     else "MISSING — pip install trimesh",              check_python_pkg("trimesh"))
    row("cadquery",              "available" if check_python_pkg("cadquery")    else "optional — pip install cadquery (STEP out)", check_python_pkg("cadquery"))
    row("Inkscape (CLI)",        "available" if check_cli("inkscape")     else "not found in PATH",                                check_cli("inkscape"))

    print("\n[PROJECT DIRECTORIES]")
    print("-" * 60)
    for subdir in ["input", "output/svg", "output/step", "output/3mf", "pipeline", "scripts"]:
        p = PROJECT_ROOT / subdir
        row(subdir, "exists" if p.exists() else "missing", p.exists())

    header("RECOMMENDED NEXT STEP")
    print("""
  Stage 1 is the current bottleneck — all tools are now installed.

  To run a conversion:
    1. Drop a source PNG into:  input\\
    2. Run:  python scripts\\convert_png.py input\\your_file.png
    3. Check result in:         output\\svg\\

  vtracer (Python API) is active — produces clean spline paths
  on organic/cursive artwork with minimal node count.
""")

if __name__ == "__main__":
    main()
