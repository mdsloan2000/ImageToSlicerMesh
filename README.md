# Image to Slicer Ready Mesh

Converts PNG artwork into clean, slicer-ready multicolor `.3mf` mesh files for
OrcaSlicer and Chitubox. Designed for organic/illustrated artwork like the
Veggie Garden Stake series.

---

## Pipeline Overview

| # | Stage | Tool | Status |
|---|-------|------|--------|
| 1 | PNG → Clean SVG | vtracer / OpenCV / Inkscape | **Active** |
| 2 | SVG → Plasticity curves | Plasticity 4.x | In progress |
| 3 | Extrude, fillet, organize by color | Plasticity 4.x | In progress |
| 4 | Export → OrcaSlicer multicolor `.3mf` | OrcaSlicer 2.3.2 | Pending |
| 5 | Slicer prep: filament, infill, orientation | OrcaSlicer 2.3.2 | Pending |

---

## Requirements

### Python packages

```
pip install -r requirements.txt
```

### vtracer CLI (recommended — best quality for organic art)

```
# Option 1: cargo (requires Rust — https://rustup.rs)
cargo install vtracer

# Option 2: download prebuilt binary
# https://github.com/visioncortex/vtracer/releases
```

> The `vtracer` Python wheel crashes on Python 3.12+. Use the CLI binary.

### Other tools (optional)

| Tool | Purpose |
|------|---------|
| Inkscape 1.4+ | Fallback tracer, flatten SVG transforms before Plasticity import |
| Plasticity 4.x | Curve editing, extrude, fillet |
| OrcaSlicer 2.3.2 (vanilla) | Multicolor `.3mf` assembly and slicing |

---

## Quick Start

```bash
# Check tool availability and pipeline status
python get_started.py

# Convert a PNG to SVG (drops result in output/svg/)
python scripts/convert_png.py input/bell_pepper.png

# Skip binarization preprocessing (for already clean PNGs)
python scripts/convert_png.py input/bell_pepper.png --no-preprocess

# Specify output directory
python scripts/convert_png.py input/bell_pepper.png --output output/svg
```

---

## Directory Structure

```
ImageToSlicerMesh/
├── input/                  # Source PNG artwork
├── output/
│   ├── svg/                # Stage 1 output — traced SVGs
│   ├── plasticity/         # Stage 2/3 checkpoints (manual)
│   ├── step/               # Stage 4 intermediate STEP exports
│   └── 3mf/                # Stage 4/5 final slicer-ready files
├── pipeline/
│   ├── stage1_png_to_svg.py        # Tracer logic (vtracer / OpenCV / Inkscape)
│   ├── stage2_svg_to_plasticity.py # SVG prep for Plasticity import
│   ├── stage3_plasticity_export.py # Post-Plasticity STEP/STL helpers
│   ├── stage4_assemble_3mf.py      # OrcaSlicer .3mf assembly
│   └── stage5_slicer_prep.py       # Slicer profile helpers
├── scripts/
│   └── convert_png.py      # CLI wrapper for Stage 1
├── docs/
│   └── pipeline_notes.md   # Stage-by-stage technique notes
├── get_started.py           # Session launcher and tool checker
├── requirements.txt
├── CLAUDE.md
└── .gitignore
```

---

## Active Projects

| Project | Plasticity File |
|---------|----------------|
| Bell Pepper Garden Stake | `D:\Repos\VeggieProject\PlasticityWork\plasticity\bell_pepper_master_curve.plasticity` |
| Tomato Garden Stake | `D:\Repos\VeggieProject\PlasticityWork\plasticity\tomato_master_curve.plasticity` |

---

## Stage 1 Tracer Priority

The pipeline tries tracers in this order and uses the first one that succeeds:

1. **vtracer CLI** — best for organic/cursive art; spline output, minimal nodes
2. **OpenCV contours** — built-in fallback; polygon paths, no extra install
3. **Inkscape CLI** — last resort; slower, more verbose SVG

See `docs/pipeline_notes.md` for per-stage technique details and parameter tuning.
