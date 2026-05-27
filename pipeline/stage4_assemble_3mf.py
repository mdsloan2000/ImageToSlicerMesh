"""
Stage 4: Assemble Multicolor .3mf for OrcaSlicer

Takes per-color STEP/STL files from Stage 3 and assembles them into a
single multicolor .3mf project file for OrcaSlicer 2.3.2 (vanilla).

Target slicer: OrcaSlicer 2.3.2 vanilla (NOT the Flashforge fork).

Manual workflow (until automation is implemented):
1. Open OrcaSlicer → New Project
2. Import each color body as a separate mesh part
3. Assign filament colors in the Objects panel
4. Position / orient the model
5. Export as .3mf project file

Status: TODO — .3mf assembly automation planned after Stage 3 stabilizes.
"""

from pathlib import Path


def assemble_3mf(mesh_paths: list[Path], output_path: Path,
                 filament_colors: list[str] | None = None) -> Path:
    """
    Combine multiple mesh files into a single multicolor .3mf project.

    mesh_paths:      ordered list of per-color STL/STEP files
    output_path:     destination .3mf file
    filament_colors: optional list of hex color strings (e.g. ["#FF0000", "#FFFFFF"])
    """
    raise NotImplementedError("Stage 4 .3mf assembly not yet implemented.")
