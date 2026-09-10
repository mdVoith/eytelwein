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
testing_methods
    Testing methods for belt conveyor systems
main
    Core utilities including units and constants
"""

# Import key functions for easy access
from . import (
    belt_conveyor_design,
    horizontal_curves,
    idler_design,
    main,
    testing_methods,
)

__version__ = "0.1.7"

__all__ = [
    "belt_conveyor_design",
    "horizontal_curves",
    "idler_design",
    "main",
    "testing_methods",
]
