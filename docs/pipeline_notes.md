# Pipeline Notes

## Stage 1 — PNG to SVG

### Why vtracer over Potrace
- vtracer uses spline fitting natively; Potrace outputs polygons then approximates curves
- vtracer handles organic/cursive letter shapes with far fewer spurious nodes
- vtracer respects corner thresholds better on flowing strokes

### vtracer Install
```
# Requires Rust — install from https://rustup.rs if needed
cargo install vtracer

# Or download binary from:
# https://github.com/visioncortex/vtracer/releases
```

### Key vtracer Parameters for Organic Art
| Parameter | Value | Reason |
|-----------|-------|--------|
| `--mode` | `spline` | Smooth curves instead of polyline |
| `--corner_threshold` | `60` | Higher = fewer sharp corners on curves |
| `--length_threshold` | `4.0` | Ignore very short segments (noise) |
| `--filter_speckle` | `4` | Remove small noise dots |

### Preprocessing Tips
- Source PNGs should be high-contrast (black art on white background)
- If there is gray fringing/antialiasing, run `preprocess_png()` first
- For very low-res sources: upscale 2–4× with Lanczos before tracing

---

## Stage 2 — SVG to Plasticity

- Plasticity 4.x imports SVG curves directly (File → Import → SVG)
- Flatten transforms in SVG before import (Inkscape: Edit → XML editor or `Object → Flatten Transforms`)
- Each color region should be a separate closed path for clean extrusion
- Save checkpoint: File → Save As → `*_baseline.plasticity` before any edits

---

## Stage 3 — Plasticity Extrude & Fillet

- Extrude each closed region to desired height (typically 2–4 mm for garden stakes)
- Apply fillets to top edges for print-friendly geometry (0.3–0.5 mm radius)
- Organize bodies by color in the scene tree before export

---

## Stage 4 — OrcaSlicer Assembly

- Export from Plasticity as STEP or STL per color body
- Import into OrcaSlicer as multi-part / multi-filament object
- Assign filament colors per body in the Objects panel
- Target: OrcaSlicer 2.3.2 vanilla (not Flashforge fork)

---

## Active Project Files
| Project | File |
|---------|------|
| Bell Pepper | `D:\Repos\VeggieProject\PlasticityWork\plasticity\bell_pepper_master_curve.plasticity` |
| Tomato | `D:\Repos\VeggieProject\PlasticityWork\plasticity\tomato_master_curve.plasticity` |
