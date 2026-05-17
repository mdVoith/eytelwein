"""
Eytelwein library for belt conveyor calculations.

This library provides comprehensive calculations for belt conveyor systems
based on established standards including DIN 22101 and VDI 2341, as well
as research-based methodologies for specialized applications.

Modules
-------
din_22101
    Belt conveyor calculations according to DIN 22101 standard
vdi_2341
    Idler roll calculations according to VDI 2341 standard
horizontal_curves
    Research-based horizontal curve force calculations
main
    Core utilities including units and constants
"""

# Import key functions for easy access
from . import din_22101, vdi_2341, horizontal_curves
from . import main

__version__ = "0.1.0"

__all__ = [
    "din_22101",
    "vdi_2341",
    "horizontal_curves",
    "main",
]
