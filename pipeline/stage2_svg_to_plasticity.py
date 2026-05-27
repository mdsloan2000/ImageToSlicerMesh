"""
Stage 2: SVG → Plasticity Import Prep

Prepares a traced SVG for clean import into Plasticity 4.x:
- Validates that all paths are closed
- Flattens transforms (Plasticity requires identity transforms)
- Optionally invokes Inkscape CLI to flatten

Plasticity import: File → Import → SVG
Save checkpoint immediately after import:
    File → Save As → <name>_baseline.plasticity

Status: TODO — manual workflow for now; automation planned.
"""

from pathlib import Path


def validate_closed_paths(svg_path: Path) -> list[str]:
    """
    Return a list of warning strings for any open paths found in the SVG.
    Open paths won't extrude cleanly in Plasticity.
    """
    raise NotImplementedError("Stage 2 automation not yet implemented.")


def flatten_transforms(svg_path: Path, out_path: Path) -> Path:
    """
    Use Inkscape CLI to flatten all transforms to absolute coordinates.
    Required before Plasticity import to avoid misaligned geometry.
    """
    raise NotImplementedError("Stage 2 automation not yet implemented.")
