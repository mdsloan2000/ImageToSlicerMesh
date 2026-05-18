# Image to Slicer Ready Mesh Workflow — Project Context

## User
- **Name**: Mike Sloan
- **Background**: Software developer, data scientist, maker, 3D printing reseller
- **Note**: Mike has MCI (vascular type) — always provide a session recap at the start of every response and a "Next Step" summary at the end. Honor all reminders without hesitation.

## Hardware & Environment
- **OS**: Windows 11
- **3D Printers**: Flashforge AD5M Pro, AD5X, Creator 5 Pro
- **Slicer**: OrcaSlicer 2.3.2 (vanilla only — NOT the Flashforge fork)
- **Workstation**: Dual-GPU (RTX 3060 + RTX 5070 build in progress)

## Software Versions (verify against official docs at each session start)
| Tool | Version |
|------|---------|
| Plasticity | 4.26.1.3 (Trial) |
| OrcaSlicer | 2.3.2 (vanilla) |
| Inkscape | 1.4.3 |
| Python | primary scripting language |

## Project Goal
Build a robust, repeatable, Python-friendly pipeline that converts PNG artwork into clean,
slicer-ready multicolor `.3mf` mesh files for OrcaSlicer and Chitubox.

## Pipeline Stages
| # | Stage | Status |
|---|-------|--------|
| 1 | PNG → Clean SVG (vector conversion) | **Active — reworking tracer quality** |
| 2 | SVG → Plasticity (curve import and cleanup) | In progress |
| 3 | Plasticity: extrude, fillet, organize by color | In progress |
| 4 | Export → OrcaSlicer (multicolor `.3mf` assembly) | Pending |
| 5 | Slicer prep: filament assignment, infill, orientation | Pending |

## Current Problem — Stage 1
Existing Potrace/ImageMagick conversion produces SVGs with:
- Too many nodes (over-sampling on curves)
- Jogs and artifacts on cursive/organic letterforms
- Poorly separated closed regions
- Inconsistent quality across different PNG sources

**Preferred fix**: Replace or supplement Potrace with a better tracer.
**Best candidate**: `vtracer` — Rust-based, handles organic shapes far better than Potrace.
Other options: OpenCV-based custom preprocessing → Potrace, Inkscape CLI trace with tuned params.

## Source Artwork
- Cursive lettering inside shaped borders (tomato, pepper, etc.)
- Organic, hand-drawn / illustrated style
- Black-and-white or high-contrast source PNGs

## Active Projects
| Project | Location | Status |
|---------|----------|--------|
| Bell Pepper Garden Stake | `D:\Repos\VeggieProject\PlasticityWork\plasticity\bell_pepper_master_curve.plasticity` | Curves extruded, fillets in progress |
| Tomato Garden Stake | `D:\Repos\VeggieProject\PlasticityWork\plasticity\tomato_master_curve.plasticity` | Curves imported, baseline saved — pipeline rework needed |

## Workflow Preferences
- Python scripts over GUI tools wherever possible
- Airgapped / local processing preferred
- Always check official docs for version-specific behavior at session start
- Save named checkpoints before any destructive edits
- Tool-agnostic — best result wins regardless of tool

## Formatting Preferences
- Use headings, tables, and bullet points for scannable responses
- End each response with a single focused **Next Step**
- Provide session recaps at start and end of each conversation
