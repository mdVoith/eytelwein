# Export commonly used functions from core and extended modules

# Core Module - Volume flow and mass flow functions
from eytelwein.din_22101.core.volume_flow_mass_flow import (
    usable_belt_width,
    partial_cross_section_above_water_fill,
    partial_cross_section_at_water_fill,
    cross_section_of_fill,
    volume_flow_from_cross_section_speed,
    mass_flow_from_volume_flow_density,
    volume_flow_from_mass_flow_density,
    mass_flow_from_cross_section_speed_density,
    cross_section_from_volume_flow_speed,
    cross_section_from_mass_flow_speed_density,
    nominal_volume_flow,
    nominal_mass_flow,
    line_load_from_nominal_load,
    line_load_from_nominal_mass_flow_speed,
    solve_for_used_belt_width_from_cross_section,
    belt_edge_distance,
    length_of_material_on_side_roll,
    reduction_factor_inclined_fill_1,
    effective_filling_ratio_from_areas,
    reduction_factor_inclined_fill,
    effective_filling_ratio,
)

# Core Module - Belt tension distribution functions
from eytelwein.din_22101.core.distribution_of_belt_tensions_across_belt_width import (
    mean_belt_tension_related_to_belt_width,
    local_belt_force_related_to_belt_width,
    local_center_belt_force,
    part_of_belt_lying_on_side_idler,
    local_edge_belt_force,
    minimal_transition_length,
    distance_belt_edge_to_pulley_surface_level,
    reference_length_of_transition_zone_for_steel_cord_belts,
    compensation_length_at_transition_zone,
    length_of_belt_edge_in_transition_zone,
    difference_edge_and_center_belt_tensions_steel_cord_belts,
    difference_edge_and_center_belt_tensions_textile_belts,
    maximal_allowable_pulley_lift,
)

# Core Module - Minimum pulley diameter functions
from eytelwein.din_22101.core.minimum_pulley_diameter import (
    minimum_diameter_of_group_A_pulleys,
    pulley_load_factor,
    minimum_diameter_of_group_A_B_C_pulleys,
    get_max_width_related_tension_at_group_A_pulleys,
)

# Core Module - Resistance and power functions
from eytelwein.din_22101.core.resistance_and_power_for_steady_operations import (
    friction_resistance_of_skirting_board_from_material_flow,
    gradient_resistance,
    gradient_resistance_sections,
    total_power_at_drive_pulley_due_to_motion_resistances,
)

# Core Module - Design layout of drive system
from eytelwein.din_22101.core.design_layout_of_drive_system import (
    height_difference_from_section_length_and_inclination_angle,
    angle_of_inclination_from_height_difference_and_section_length,
    section_length_from_height_difference_and_inclination_angle,
)

# Core Module - Belt tensions and takeup forces
from eytelwein.din_22101.core.belt_tensions_and_takeup_forces import (
    minimum_belt_tension_from_sag_carry,
)

# Extended Module - Volume flow and mass flow functions
from eytelwein.din_22101.extended.volume_flow_mass_flow import (
    maximal_cross_section_skirt_board_known_geometry,
    required_skirtboard_height_from_cross_section,
    get_usable_belt_width_from_skirt_board_width,
    convert_equivalent_angle_of_slope_to_surcharge_angle,
    convert_surcharge_angle_to_equivalent_angle_of_slope,
    convert_surcharge_angles,
    get_material_bed_depth,
)

# Extended Module - Resistance and power for steady operations
from eytelwein.din_22101.extended.resistance_and_power_for_steady_operations import (
    motion_resistance_from_torque,
)

# Extended Module - Belt tension distribution functions
from eytelwein.din_22101.extended.distribution_of_belt_tensions_across_belt_width import (
    distance_belt_edge_deepest_level_of_trough,
)

# Extended Module - Design layout of drive system
from eytelwein.din_22101.extended.design_layout_of_drive_system import (
    mechanical_torque_from_belt_force,
    mechanical_power_from_torque_and_belt_speed,
    number_of_revolutions_from_translatory_speed,
    pulley_revolutions_from_belt_speed,
    translatory_speed_from_number_of_revolutions,
    belt_speed_from_pulley_revolutions,
)

# Extended Module - Mass inertia functions
from eytelwein.din_22101.extended.mass_inertia import (
    belt_mass_per_strand,
    payload_mass_total,
    translating_mass_empty,
    translating_mass_full,
    pulley_radius,
    motor_shaft_inertia_total,
    inertia_per_drive,
)

# Extended Module - Design of conveyor belt functions
from eytelwein.din_22101.extended.design_of_conveyor_belt import (
    belt_weight_per_square_meter,
    line_load_belt,
    line_load_belt_from_belt_weight_per_square_meter,
)

from eytelwein.din_22101.constants import IdlerSets

__all__ = [
    # Core - Volume flow and mass flow functions
    "usable_belt_width",
    "partial_cross_section_above_water_fill",
    "partial_cross_section_at_water_fill",
    "cross_section_of_fill",
    "volume_flow_from_cross_section_speed",
    "mass_flow_from_volume_flow_density",
    "volume_flow_from_mass_flow_density",
    "mass_flow_from_cross_section_speed_density",
    "cross_section_from_volume_flow_speed",
    "cross_section_from_mass_flow_speed_density",
    "nominal_volume_flow",
    "nominal_mass_flow",
    "line_load_from_nominal_load",
    "line_load_from_nominal_mass_flow_speed",
    "solve_for_used_belt_width_from_cross_section",
    "belt_edge_distance",
    "length_of_material_on_side_roll",
    "reduction_factor_inclined_fill_1",
    "reduction_factor_inclined_fill",
    "effective_filling_ratio",
    "effective_filling_ratio_from_areas",
    # Core - Belt tension distribution functions
    "mean_belt_tension_related_to_belt_width",
    "local_belt_force_related_to_belt_width",
    "local_center_belt_force",
    "part_of_belt_lying_on_side_idler",
    "local_edge_belt_force",
    "minimal_transition_length",
    "distance_belt_edge_to_pulley_surface_level",
    "reference_length_of_transition_zone_for_steel_cord_belts",
    "compensation_length_at_transition_zone",
    "length_of_belt_edge_in_transition_zone",
    "difference_edge_and_center_belt_tensions_steel_cord_belts",
    "difference_edge_and_center_belt_tensions_textile_belts",
    "maximal_allowable_pulley_lift",  # Core - Resistance and power functions
    "friction_resistance_of_skirting_board_from_material_flow",
    "gradient_resistance",
    "gradient_resistance_sections",
    "total_power_at_drive_pulley_due_to_motion_resistances",
    # Core - Design layout of drive system
    "height_difference_from_section_length_and_inclination_angle",
    "angle_of_inclination_from_height_difference_and_section_length",
    "section_length_from_height_difference_and_inclination_angle",
    # Core - Minimum pulley diameter functions
    "minimum_diameter_of_group_A_pulleys",
    "pulley_load_factor",
    "minimum_diameter_of_group_A_B_C_pulleys",
    "get_max_width_related_tension_at_group_A_pulleys",
    # Core - Belt tensions and takeup forces
    "minimum_belt_tension_from_sag_carry",
    # Extended - Volume flow and mass flow functions
    "maximal_cross_section_skirt_board_known_geometry",
    "required_skirtboard_height_from_cross_section",
    "get_usable_belt_width_from_skirt_board_width",
    "convert_equivalent_angle_of_slope_to_surcharge_angle",
    "convert_surcharge_angle_to_equivalent_angle_of_slope",
    "convert_surcharge_angles",
    "get_material_bed_depth",
    # Extended - Resistance and power for steady operations
    "motion_resistance_from_torque",
    # Extended - Belt tension distribution functions
    "distance_belt_edge_deepest_level_of_trough",
    # Extended - Design layout of drive system
    "mechanical_torque_from_belt_force",
    "mechanical_power_from_torque_and_belt_speed",
    "number_of_revolutions_from_translatory_speed",
    "pulley_revolutions_from_belt_speed",
    "translatory_speed_from_number_of_revolutions",
    "belt_speed_from_pulley_revolutions",
    # Extended - Mass inertia functions
    "belt_mass_per_strand",
    "payload_mass_total",
    "translating_mass_empty",
    "translating_mass_full",
    "pulley_radius",
    "motor_shaft_inertia_total",
    "inertia_per_drive",
    # Extended - Design of conveyor belt functions
    "belt_weight_per_square_meter",
    "line_load_belt",
    "line_load_belt_from_belt_weight_per_square_meter",
    # Constants
    "IdlerSets",
]
