"""
Horizontal curve calculations for belt conveyor systems.

This module provides functions for analyzing horizontal curves in belt conveyor
systems, implementing research-based methodologies for force and load calculations.

The module is organized into:
- core: Fundamental calculation functions
- models: Data structures and curve definitions (planned)
- constants: Physical constants and curve parameters (planned)

Key Functions
-------------
force_component_towards_inside_curve_from_belt_tension
    Calculate centripetal force component from belt tension
weight_force_belt_inside
    Calculate weight force on inside belt section considering geometry and inclination
weight_force_belt_outside
    Calculate weight force on outside belt section considering geometry and inclination
weight_force_belt_center
    Calculate weight force on center belt section considering banking and inclination
weight_force_of_belt
    Calculate net lateral weight force from individual belt section forces
"""

from .core import (
    force_component_towards_inside_curve_from_belt_tension,
    force_component_towards_inside_curve_from_belt_tension_sections,
    weight_force_belt_inside,
    weight_force_belt_outside,
    weight_force_belt_center,
    weight_force_of_belt,
    weight_force_material_outside,
    weight_force_material_inside,
    weight_force_material_center,
    weight_force_of_material,
    restraining_force_from_dead_weights,
    tilted_idler_friction_force_inside,
    tilted_idler_friction_force_outside,
    tilted_idler_friction_force_center,
    restraining_force_from_tilted_idlers,
    # Enhanced error handling and constants
    ERROR_MESSAGES,
    DEFAULT_WING_LOAD_FACTOR,
    DEFAULT_CENTER_LOAD_FACTOR,
)

__all__ = [
    "force_component_towards_inside_curve_from_belt_tension",
    "force_component_towards_inside_curve_from_belt_tension_sections",
    "weight_force_belt_inside",
    "weight_force_belt_outside",
    "weight_force_belt_center",
    "weight_force_of_belt",
    "weight_force_material_outside",
    "weight_force_material_inside",
    "weight_force_material_center",
    "weight_force_of_material",
    "restraining_force_from_dead_weights",
    "tilted_idler_friction_force_inside",
    "tilted_idler_friction_force_outside",
    "tilted_idler_friction_force_center",
    "restraining_force_from_tilted_idlers",
    # Enhanced error handling and constants
    "ERROR_MESSAGES",
    "DEFAULT_WING_LOAD_FACTOR",
    "DEFAULT_CENTER_LOAD_FACTOR",
]
