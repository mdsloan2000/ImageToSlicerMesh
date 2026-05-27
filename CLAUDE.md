# Image to Slicer Ready Mesh — Agent Context

## User & Behavior Rules

- **Name**: Mike Sloan — software developer, data scientist, maker, 3D printing reseller
- **Cognitive note**: Mike has MCI (vascular type). **Always** provide a session recap at the
  start of every response and a "Next Step" summary at the end. Honor all reminders without
  hesitation.
- **Response format**: Use headings, tables, and bullet points for scannable output. Keep
  explanations direct. End every response with a single focused **Next Step**.

---

## Project Goal

Build a repeatable, Python-scripted pipeline that converts PNG artwork into clean,
slicer-ready multicolor `.3mf` mesh files for OrcaSlicer and Chitubox.

Source artwork: cursive lettering inside organic shaped borders (veggie garden stakes).
Artwork is hand-drawn / illustrated style, high-contrast black-and-white PNGs.

---

## Hardware & Tool Versions

| Tool | Version | Notes |
|------|---------|-------|
| Python | primary language | Windows 11, bash shell in VSCode |
| Plasticity | 4.26.1.3 (Trial) | GUI-only — no Python API |
| OrcaSlicer | 2.3.2 vanilla | **NOT** the Flashforge fork |
| Inkscape | 1.4.3 | Used as tracer fallback and SVG flattener |
| vtracer | CLI binary | See constraints below |
| OS | Windows 11 | RTX 3060 + RTX 5070 workstation |
| Printers | AD5M Pro, AD5X, Creator 5 Pro | All Flashforge |

---

## Pipeline Stages

| # | Stage | Automation | Status |
|---|-------|-----------|--------|
| 1 | PNG → Clean SVG | Python (`pipeline/stage1_png_to_svg.py`) | **Active** |
| 2 | SVG → Plasticity import prep | Python stub — manual for now | In progress |
| 3 | Extrude, fillet, organize by color | Plasticity GUI — no automation planned | In progress |
| 4 | Export → OrcaSlicer `.3mf` assembly | Python stub — not yet implemented | Pending |
| 5 | Slicer prep: filament, infill, orientation | Python stub — not yet implemented | Pending |

Stages 3–5 are blocked on Plasticity/OrcaSlicer being GUI tools. Stubs exist to capture
the planned interface; `raise NotImplementedError` is intentional.

---

## Repo Structure

```
ImageToSlicerMesh/
│
├── CLAUDE.md               ← this file — agent context and coding rules
├── README.md               ← human-facing project overview and quick start
├── get_started.py          ← session launcher: pipeline status + tool checker
├── requirements.txt        ← pip dependencies; vtracer is CLI-only (see constraints)
├── .gitignore
│
├── input/                  ← source PNG artwork (committed; do not gitignore)
│   └── *.png               ← bell_pepper.png, tomato.png, cucumber.png, etc.
│
├── output/                 ← ALL output is gitignored; dirs exist locally only
│   ├── svg/                ← Stage 1 output — traced SVGs
│   ├── plasticity/         ← Stage 2/3 checkpoint files (manual saves)
│   ├── step/               ← Stage 4 intermediate STEP exports
│   └── 3mf/                ← Stage 4/5 final slicer-ready files
│
├── pipeline/               ← importable Python package; one module per stage
│   ├── __init__.py         ← exports: png_to_svg (Stage 1 only so far)
│   ├── stage1_png_to_svg.py        ← IMPLEMENTED — tracer logic
│   ├── stage2_svg_to_plasticity.py ← STUB — NotImplementedError
│   ├── stage3_plasticity_export.py ← STUB — NotImplementedError
│   ├── stage4_assemble_3mf.py      ← STUB — NotImplementedError
│   └── stage5_slicer_prep.py       ← STUB — NotImplementedError
│
├── scripts/                ← CLI entry points; thin wrappers around pipeline/
│   └── convert_png.py      ← CLI for Stage 1: python scripts/convert_png.py input/foo.png
│
└── docs/
    └── pipeline_notes.md   ← Stage-by-stage technique notes, parameter rationale
```

---

## Code Architecture

### `pipeline/` vs `scripts/`

- **`pipeline/`** — importable library. All logic lives here. Each stage module has a primary
  entry-point function (e.g. `png_to_svg()`). No `argparse`, no `print` that the caller
  didn't ask for.
- **`scripts/`** — thin CLI wrappers. They add `sys.path`, call into `pipeline/`, handle
  `argparse`, and print user-facing output. Keep them short.
- **`get_started.py`** — standalone session tool. Not part of the pipeline import chain.

### Stage 1 tracer priority (in `stage1_png_to_svg.py`)

The `png_to_svg()` function tries tracers in order and returns on first success:

1. **vtracer CLI** — best quality; spline output; use when `shutil.which("vtracer")` is truthy
2. **OpenCV contours** — built-in fallback; polygon paths; needs only `opencv-python`
3. **Inkscape CLI** — last resort; slow, verbose SVG output

Do not change this priority order without a documented reason.

### Adding a new stage module

Follow the pattern in `stage2_svg_to_plasticity.py`:
1. Module-level docstring describing the stage, its manual workflow, and status
2. Individual functions with clear signatures and docstrings
3. `raise NotImplementedError("...")` in unimplemented functions — do not use `pass`
4. Export the primary entry-point function from `pipeline/__init__.py`
5. Create a matching CLI script in `scripts/` if it needs to be run standalone

---

## Critical Constraints

### vtracer — use CLI, not pip

The `vtracer` Python wheel segfaults / crashes on Python 3.12+. **Never** import vtracer
as a Python module. Always invoke it via `subprocess` after checking `shutil.which("vtracer")`.

```python
# CORRECT
if shutil.which("vtracer"):
    subprocess.run(["vtracer", "--input", ..., "--output", ...])

# WRONG — crashes on Python 3.12+
import vtracer
```

### Windows paths

- All paths in code must use `pathlib.Path` — never raw string concatenation
- Paths in config/docs use Windows notation (`D:\Repos\...`) since the user sees these
- Shell commands run in bash (Unix syntax) inside VSCode terminal

### UTF-8 terminal output

All pipeline modules and CLI scripts that print Unicode (checkmarks, arrows) must include:

```python
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
```

Place this immediately after imports, before any output.

### `output/` is fully gitignored

The entire `output/` tree is in `.gitignore`. Do not add `.gitkeep` files or try to commit
output artifacts. The directories exist on the local machine. Scripts create them with
`Path(...).mkdir(parents=True, exist_ok=True)` when needed.

### Preprocessing intermediate files

`input/*_prep.png` and `input/*_inv.png` are gitignored (preprocessing artifacts).
Source PNGs in `input/` are committed and should never be deleted by scripts.

### OrcaSlicer target

Always specify **OrcaSlicer 2.3.2 vanilla**. The Flashforge fork has different `.3mf`
structure and filament assignment UI — do not target it.

---

## Active Projects (external to this repo)

| Project | File | Status |
|---------|------|--------|
| Bell Pepper Garden Stake | `D:\Repos\VeggieProject\PlasticityWork\plasticity\bell_pepper_master_curve.plasticity` | Fillets in progress |
| Tomato Garden Stake | `D:\Repos\VeggieProject\PlasticityWork\plasticity\tomato_master_curve.plasticity` | Baseline saved, pipeline rework needed |

These files live outside this repo. `get_started.py` checks whether they exist at startup.

---

## Workflow Preferences

- Python scripts over GUI tools wherever possible
- Local/airgapped processing preferred — avoid cloud dependencies
- Save named checkpoints before any destructive Plasticity edits
- Tool-agnostic — best result wins regardless of tool
- When in doubt, check official docs for the pinned tool versions above
