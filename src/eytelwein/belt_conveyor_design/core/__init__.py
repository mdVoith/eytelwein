# Public functions from resistance_and_power_for_steady_operations
from eytelwein.belt_conveyor_design.core.resistance_and_power_for_steady_operations import (
    friction_resistance_of_skirting_board_from_material_flow,
    gradient_resistance,
    gradient_resistance_sections,
    total_power_at_drive_pulley_due_to_motion_resistances,
)

# Public functions from design_layout_of_drive_system
from eytelwein.belt_conveyor_design.core.design_layout_of_drive_system import (
    height_difference_from_section_length_and_inclination_angle,
)

# Public functions from volume_flow_mass_flow
from eytelwein.belt_conveyor_design.core.volume_flow_mass_flow import (
    usable_belt_width,
    partial_cross_section_above_water_fill,
    partial_cross_section_at_water_fill,
    cross_section_of_fill,
    volume_flow_from_cross_section_speed,
    mass_flow_from_volume_flow_density,
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
    reduction_factor_inclined_fill,
    effective_filling_ratio,
)

# Public functions from distribution_of_belt_tensions_across_belt_width
from eytelwein.belt_conveyor_design.core.distribution_of_belt_tensions_across_belt_width import (
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

# Public functions from minimum_pulley_diameter
from eytelwein.belt_conveyor_design.core.minimum_pulley_diameter import (
    minimum_diameter_of_group_A_pulleys,
    pulley_load_factor,
    minimum_diameter_of_group_A_B_C_pulleys,
    get_max_width_related_tension_at_group_A_pulleys,
)

# Public functions from belt_tensions_and_takeup_forces
from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
    minimum_belt_tension_from_sag_carry,
)

# Private functions from _volume_flow_mass_flow
from eytelwein.belt_conveyor_design.core._volume_flow_mass_flow import (
    _usable_belt_width,
    _partial_cross_section_at_water_fill,
    _partial_cross_section_above_water_fill,
    _cross_section_of_fill,
    _volume_flow_from_cross_section_speed,
    _mass_flow_from_volume_flow_density,
    _mass_flow_from_cross_section_speed_density,
    _cross_section_from_volume_flow_speed,
    _cross_section_from_mass_flow_speed_density,
    _nominal_volume_flow,
    _nominal_mass_flow,
    _line_load_from_nominal_load,
    _line_load_from_nominal_mass_flow_speed,
    _solve_for_used_belt_width_from_cross_section,
    _belt_edge_distance,
    _length_of_material_on_side_roll,
    _reduction_factor_inclined_fill_1,
    _reduction_factor_inclined_fill,
    _effective_filling_ratio,
)

# Private functions from _resistance_and_power_for_steady_operations
from eytelwein.belt_conveyor_design.core._resistance_and_power_for_steady_operations import (
    _total_power_at_drive_pulley_due_to_motion_resistances,
    _gradient_resistance,
)

# Private functions from _distribution_of_belt_tensions_across_belt_width
from eytelwein.belt_conveyor_design.core._distribution_of_belt_tensions_across_belt_width import (
    _mean_belt_tension_related_to_belt_width,
    _local_belt_force_related_to_belt_width,
    _local_center_belt_force,
    _part_of_belt_lying_on_side_idler,
    _local_edge_belt_force,
    _minimal_transition_length,
    _distance_belt_edge_to_pulley_surface_level,
    _reference_length_of_transition_zone_for_steel_cord_belts,
    _compensation_length_at_transition_zone,
    _length_of_belt_edge_in_transition_zone,
    _difference_edge_and_center_belt_tensions_steel_cord_belts,
    _difference_edge_and_center_belt_tensions_textile_belts,
    _maximal_allowable_pulley_lift,
)

# Private functions from _minimum_pulley_diameter
from eytelwein.belt_conveyor_design.core._minimum_pulley_diameter import (
    _minimum_diameter_of_group_A_pulleys,
    _pulley_load_factor,
    _minimum_diameter_of_group_A_B_C_pulleys,
    _get_max_width_related_tension_at_group_A_pulleys,
)

# Private functions from _belt_tensions_and_takeup_forces
from eytelwein.belt_conveyor_design.core._belt_tensions_and_takeup_forces import (
    _minimum_belt_tension_from_sag_carry,
)

__all__ = [
    # Public resistance_and_power_for_steady_operations
    "friction_resistance_of_skirting_board_from_material_flow",
    "gradient_resistance",
    "gradient_resistance_sections",
    "total_power_at_drive_pulley_due_to_motion_resistances",
    # Public design_layout_of_drive_system
    "height_difference_from_section_length_and_inclination_angle",
    "angle_of_inclination_from_height_difference_and_section_length",
    "section_length_from_height_difference_and_inclination_angle",
    # Public volume_flow_mass_flow
    "usable_belt_width",
    "partial_cross_section_above_water_fill",
    "partial_cross_section_at_water_fill",
    "cross_section_of_fill",
    "volume_flow_from_cross_section_speed",
    "mass_flow_from_volume_flow_density",
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
    # Public distribution_of_belt_tensions_across_belt_width
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
    "maximal_allowable_pulley_lift",
    # Public minimum_pulley_diameter
    "minimum_diameter_of_group_A_pulleys",
    "pulley_load_factor",
    "minimum_diameter_of_group_A_B_C_pulleys",
    "get_max_width_related_tension_at_group_A_pulleys",
    # Public belt_tensions_and_takeup_forces
    "minimum_belt_tension_from_sag_carry",
    # Private _volume_flow_mass_flow
    "_usable_belt_width",
    "_partial_cross_section_at_water_fill",
    "_partial_cross_section_above_water_fill",
    "_cross_section_of_fill",
    "_volume_flow_from_cross_section_speed",
    "_mass_flow_from_volume_flow_density",
    "_mass_flow_from_cross_section_speed_density",
    "_cross_section_from_volume_flow_speed",
    "_cross_section_from_mass_flow_speed_density",
    "_nominal_volume_flow",
    "_nominal_mass_flow",
    "_line_load_from_nominal_load",
    "_line_load_from_nominal_mass_flow_speed",
    "_solve_for_used_belt_width_from_cross_section",
    "_belt_edge_distance",
    "_length_of_material_on_side_roll",
    "_reduction_factor_inclined_fill_1",
    "_reduction_factor_inclined_fill",
    "_effective_filling_ratio",
    # Private _resistance_and_power_for_steady_operations
    "_friction_resistance_of_skirting_board_from_material_flow",
    "_total_power_at_drive_pulley_due_to_motion_resistances",
    "_gradient_resistance",
    # Private _distribution_of_belt_tensions_across_belt_width
    "_mean_belt_tension_related_to_belt_width",
    "_local_belt_force_related_to_belt_width",
    "_local_center_belt_force",
    "_part_of_belt_lying_on_side_idler",
    "_local_edge_belt_force",
    "_minimal_transition_length",
    "_distance_belt_edge_to_pulley_surface_level",
    "_reference_length_of_transition_zone_for_steel_cord_belts",
    "_compensation_length_at_transition_zone",
    "_length_of_belt_edge_in_transition_zone",
    "_difference_edge_and_center_belt_tensions_steel_cord_belts",
    "_difference_edge_and_center_belt_tensions_textile_belts",
    "_maximal_allowable_pulley_lift",
    # Private _minimum_pulley_diameter
    "_minimum_diameter_of_group_A_pulleys",
    "_pulley_load_factor",
    "_minimum_diameter_of_group_A_B_C_pulleys",
    "_get_max_width_related_tension_at_group_A_pulleys",
    # Private _belt_tensions_and_takeup_forces
    "_minimum_belt_tension_from_sag_carry",
]
