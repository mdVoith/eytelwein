# Public functions from volume_flow_mass_flow
from eytelwein.belt_conveyor_design.extended.volume_flow_mass_flow import (
    maximal_cross_section_skirt_board_known_geometry,
    required_skirtboard_height_from_cross_section,
    get_usable_belt_width_from_skirt_board_width,
    convert_equivalent_angle_of_slope_to_surcharge_angle,
    convert_surcharge_angle_to_equivalent_angle_of_slope,
    convert_surcharge_angles,
    get_material_bed_depth,
)

# Public functions from resistance_and_power_for_steady_operations
from eytelwein.belt_conveyor_design.extended.resistance_and_power_for_steady_operations import (
    motion_resistance_from_torque,
)

# Public functions from minimum_pulley_diameter
from eytelwein.belt_conveyor_design.extended.minimum_pulley_diameter import (
    resulting_force_from_belt_tensions_and_wrap_angle,
)

# Public functions from distribution_of_belt_tensions_across_belt_width
from eytelwein.belt_conveyor_design.extended.distribution_of_belt_tensions_across_belt_width import (
    distance_belt_edge_deepest_level_of_trough,
)

# Public functions from design_layout_of_drive_system
from eytelwein.belt_conveyor_design.extended.design_layout_of_drive_system import (
    mechanical_torque_from_belt_force,
    mechanical_power_from_torque_and_belt_speed,
    number_of_revolutions_from_translatory_speed,
    pulley_revolutions_from_belt_speed,
    translatory_speed_from_number_of_revolutions,
    belt_speed_from_pulley_revolutions,
    angle_of_inclination_from_horizontal_length_and_lift,
    mechanical_power_from_torque_and_revolutions,
    torque_from_mechanical_power_and_revolutions,
    revolutions_from_mechanical_power_and_torque,
    pulley_diameter_from_belt_speed_and_revolutions,
    radius_from_translatory_speed_and_revolutions,
)

# Private functions from _volume_flow_mass_flow
from eytelwein.belt_conveyor_design.extended._volume_flow_mass_flow import (
    _maximal_cross_section_skirt_board_known_geometry,
    _required_skirtboard_height_from_cross_section,
    _get_usable_belt_width_from_skirt_board_width,
    _convert_surcharge_angles,
    _convert_equivalent_angle_of_slope_to_surcharge_angle,
    _convert_surcharge_angle_to_equivalent_angle_of_slope,
    _get_material_bed_depth,
)

# Private functions from _resistance_and_power_for_steady_operations
from eytelwein.belt_conveyor_design.extended._resistance_and_power_for_steady_operations import (
    _motion_resistance_from_torque,
)

# Private functions from _minimum_pulley_diameter
from eytelwein.belt_conveyor_design.extended._minimum_pulley_diameter import (
    _resulting_force_from_belt_tensions_and_wrap_angle,
)

# Private functions from _distribution_of_belt_tensions_across_belt_width
from eytelwein.belt_conveyor_design.extended._distribution_of_belt_tensions_across_belt_width import (
    _distance_belt_edge_deepest_level_of_trough,
)

# Private functions from _design_layout_of_drive_system
from eytelwein.belt_conveyor_design.extended._design_layout_of_drive_system import (
    _mechanical_torque_from_belt_force,
    _mechanical_power_from_torque_and_belt_speed,
    _number_of_revolutions_from_translatory_speed,
    _pulley_revolutions_from_belt_speed,
    _translatory_speed_from_number_of_revolutions,
    _belt_speed_from_pulley_revolutions,
    _mechanical_power_from_torque_and_revolutions,
    _torque_from_mechanical_power_and_revolutions,
    _revolutions_from_mechanical_power_and_torque,
    _pulley_diameter_from_belt_speed_and_revolutions,
    _radius_from_translatory_speed_and_revolutions,
)

__all__ = [
    # Public volume_flow_mass_flow
    "maximal_cross_section_skirt_board_known_geometry",
    "required_skirtboard_height_from_cross_section",
    "get_usable_belt_width_from_skirt_board_width",
    "convert_equivalent_angle_of_slope_to_surcharge_angle",
    "convert_surcharge_angle_to_equivalent_angle_of_slope",
    "convert_surcharge_angles",
    "get_material_bed_depth",
    # Public resistance_and_power_for_steady_operations
    "motion_resistance_from_torque",
    # Public minimum_pulley_diameter
    "resulting_force_from_belt_tensions_and_wrap_angle",
    # Public distribution_of_belt_tensions_across_belt_width
    "distance_belt_edge_deepest_level_of_trough",  # Public design_layout_of_drive_system
    "mechanical_torque_from_belt_force",
    "mechanical_power_from_torque_and_belt_speed",
    "number_of_revolutions_from_translatory_speed",
    "pulley_revolutions_from_belt_speed",
    "translatory_speed_from_number_of_revolutions",
    "belt_speed_from_pulley_revolutions",
    "angle_of_inclination_from_horizontal_length_and_lift",
    "mechanical_power_from_torque_and_revolutions",
    "torque_from_mechanical_power_and_revolutions",
    "revolutions_from_mechanical_power_and_torque",
    "pulley_diameter_from_belt_speed_and_revolutions",
    "radius_from_translatory_speed_and_revolutions",
    # Private _volume_flow_mass_flow
    "_maximal_cross_section_skirt_board_known_geometry",
    "_required_skirtboard_height_from_cross_section",
    "_get_usable_belt_width_from_skirt_board_width",
    "_convert_surcharge_angles",
    "_convert_equivalent_angle_of_slope_to_surcharge_angle",
    "_convert_surcharge_angle_to_equivalent_angle_of_slope",
    "_get_material_bed_depth",
    # Private _resistance_and_power_for_steady_operations
    "_motion_resistance_from_torque",
    # Private _minimum_pulley_diameter
    "_resulting_force_from_belt_tensions_and_wrap_angle",
    # Private _distribution_of_belt_tensions_across_belt_width
    "_distance_belt_edge_deepest_level_of_trough",
    # Private _design_layout_of_drive_system    "_mechanical_torque_from_belt_force",
    "_mechanical_power_from_torque_and_belt_speed",
    "_number_of_revolutions_from_translatory_speed",
    "_pulley_revolutions_from_belt_speed",
    "_translatory_speed_from_number_of_revolutions",
    "_belt_speed_from_pulley_revolutions",
    "_mechanical_power_from_torque_and_revolutions",
    "_torque_from_mechanical_power_and_revolutions",
    "_revolutions_from_mechanical_power_and_torque",
    "_pulley_diameter_from_belt_speed_and_revolutions",
    "_mechanical_torque_from_belt_force",
    "_radius_from_translatory_speed_and_revolutions",
]
