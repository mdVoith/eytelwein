"""
Core horizontal curve calculations module.

This module contains the fundamental calculations for horizontal curve forces
in belt conveyor systems, based on research methodologies.
"""

from .horizontal_curve_calculations import (
    force_component_towards_inside_curve_from_belt_tension,
    force_component_towards_inside_curve_from_belt_tension_sections,
    weight_force_belt_inside,
    weight_force_belt_outside,
    weight_force_belt_center,
    weight_force_of_belt,
    weight_force_material_inside,
    weight_force_material_outside,
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
    "weight_force_material_inside",
    "weight_force_material_outside",
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
