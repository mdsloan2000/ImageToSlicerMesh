"""
Stage 3: Plasticity Export Helpers

Stage 3 itself (extruding, filleting, organizing color bodies) is done
manually inside Plasticity 4.x. This module provides helpers for the
export step that follows.

Manual workflow in Plasticity:
1. Extrude each closed region to desired height (2–4 mm for garden stakes)
2. Apply fillets to top edges (0.3–0.5 mm radius)
3. Organize bodies by color in the scene tree
4. Export each color body as a separate STEP or STL file

Status: TODO — export automation planned once manual workflow is stable.
"""

from pathlib import Path


def split_step_by_body(step_path: Path, output_dir: Path) -> list[Path]:
    """
    Split a multi-body STEP file into one file per body.
    Useful if Plasticity exports all bodies in a single STEP.
    """
    raise NotImplementedError("Stage 3 export helpers not yet implemented.")


def validate_mesh(mesh_path: Path) -> dict:
    """
    Run basic mesh checks (watertight, manifold, no degenerate faces).
    Returns a dict with keys: watertight, manifold, face_count, warnings.
    """
    raise NotImplementedError("Stage 3 mesh validation not yet implemented.")
