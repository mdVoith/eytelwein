"""
Eytelwein library for belt conveyor calculations.

This library provides comprehensive calculations for belt conveyor systems
based on established engineering methodologies, as well
as research-based methodologies for specialized applications.

Modules
-------
belt_conveyor_design
    Belt conveyor design calculations
idler_design
    Idler roll load calculations
horizontal_curves
    Research-based horizontal curve force calculations
main
    Core utilities including units and constants
"""

# Import key functions for easy access
from . import belt_conveyor_design, idler_design, horizontal_curves
from . import main

__version__ = "0.1.1"

__all__ = [
    "belt_conveyor_design",
    "idler_design",
    "horizontal_curves",
    "main",
]
