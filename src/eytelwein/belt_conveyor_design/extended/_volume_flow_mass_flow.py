import math

from eytelwein.belt_conveyor_design.core._volume_flow_mass_flow import (
    _partial_cross_section_at_water_fill,
    _partial_cross_section_above_water_fill,
)


def _maximal_cross_section_skirt_board_known_geometry(
    center_roll_length: float,
    skirt_board_width: float,
    skirt_board_height: float,
    troughing_angle: float,
    equivalent_slope_angle: float,
) -> float:
    """
    Calculate the maximal cross-sectional area of a skirt board with known geometry.

    Parameters:
    center_roll_length (float): The length of the center roll.
    skirt_board_width (float): The width of the skirt board.
    skirt_board_height (float): The height of the skirt board.
    troughing_angle (float): The troughing angle in degrees.
    equivalent_slope_angle (float): The equivalent slope angle in degrees.

    Returns:
    float: The maximal cross-sectional area of the skirt board.
    """
    # Calculate the usable belt width from the skirt board width
    usabel_belt_with_from_skirts = _get_usable_belt_width_from_skirt_board_width(
        skirt_board_width, center_roll_length, troughing_angle
    )

    # Calculate the area below the skirt boards
    area_below_skirt_boards = _partial_cross_section_at_water_fill(
        center_roll_length, usabel_belt_with_from_skirts, troughing_angle
    )

    # Calculate the area between the skirt boards
    area_between_skirt_boards = skirt_board_width * skirt_board_height

    # Calculate the area above the skirt boards
    area_above_skirt_boards = _partial_cross_section_above_water_fill(
        center_roll_length,
        usabel_belt_with_from_skirts,
        troughing_angle,
        equivalent_slope_angle,
    )

    # Return the total cross-sectional area
    return area_below_skirt_boards + area_between_skirt_boards + area_above_skirt_boards


def _required_skirtboard_height_from_cross_section(
    center_roll_length: float,
    skirt_board_width: float,
    troughing_angle: float,
    equivalent_slope_angle: float,
    cross_section: float,
) -> float:
    """
    Calculate the required skirt board height from the given cross-sectional area.

    Parameters:
    center_roll_length (float): The length of the center roll.
    skirt_board_width (float): The width of the skirt board.
    troughing_angle (float): The troughing angle in degrees.
    equivalent_slope_angle (float): The equivalent slope angle in degrees.
    cross_section (float): The cross-sectional area.

    Returns:
    float: The required skirt board height.
    """
    # Calculate the usable belt width from the skirt board width
    usabel_belt_with_from_skirts = _get_usable_belt_width_from_skirt_board_width(
        skirt_board_width, center_roll_length, troughing_angle
    )

    # Calculate the area below the skirt boards
    area_below_skirt_boards = _partial_cross_section_at_water_fill(
        center_roll_length, usabel_belt_with_from_skirts, troughing_angle
    )

    # Calculate the area above the skirt boards
    area_above_skirt_boards = _partial_cross_section_above_water_fill(
        center_roll_length,
        usabel_belt_with_from_skirts,
        troughing_angle,
        equivalent_slope_angle,
    )

    # Determine the required skirt board height based on the cross-sectional area
    if cross_section <= area_below_skirt_boards + area_above_skirt_boards:
        required_skirt_board_height = 0.0
    else:
        required_skirt_board_height = (
            cross_section - area_below_skirt_boards - area_above_skirt_boards
        ) / skirt_board_width

    return required_skirt_board_height


def _get_usable_belt_width_from_skirt_board_width(
    skirt_board_width: float, center_roll_length: float, troughing_angle_rad: float
) -> float:
    """
    Calculate the usable belt width from the skirt board width.

    Parameters:
    skirt_board_width (float): The width of the skirt board.
    center_roll_length (float): The length of the center roll.
    troughing_angle_rad (float): The troughing angle in radians.

    Returns:
    float: The usable belt width.
    """
    return (skirt_board_width - center_roll_length) / math.cos(
        troughing_angle_rad
    ) + center_roll_length


def _convert_surcharge_angles(
    slope_angle_rad: float | None = None,
    surcharge_angle_rad: float | None = None,
) -> dict:
    """
    Convert between equivalent slope angle and surcharge angle.

    Parameters:
    slope_angle_rad (Optional[float]): The equivalent slope angle in radians.
    surcharge_angle_rad (Optional[float]): The surcharge angle in radians.

    Returns:
    dict: A dictionary containing both angles with keys 'slope_angle' and 'surcharge_angle' in radians.

    Raises:
    ValueError: If neither or both angles are provided.
    """
    # Initialize an empty dictionary to store the converted angles
    converted_angles = {}

    # Check if only the equivalent slope angle is provided
    if slope_angle_rad is not None and surcharge_angle_rad is None:
        # Store the provided equivalent slope angle
        converted_angles["slope_angle"] = slope_angle_rad
        # Convert the equivalent slope angle to the surcharge angle and store it
        converted_angles["surcharge_angle"] = (
            _convert_equivalent_angle_of_slope_to_surcharge_angle(slope_angle_rad)
        )
    # Check if only the surcharge angle is provided
    elif surcharge_angle_rad is not None and slope_angle_rad is None:
        # Convert the surcharge angle to the equivalent slope angle and store it
        converted_angles["slope_angle"] = (
            _convert_surcharge_angle_to_equivalent_angle_of_slope(surcharge_angle_rad)
        )
        # Store the provided surcharge angle
        converted_angles["surcharge_angle"] = surcharge_angle_rad
    # Raise an error if neither or both angles are provided
    else:
        raise ValueError(
            "Either equivalent_slope_angle or surcharge_angle must be set."
        )

    # Return the dictionary containing the converted angles
    return converted_angles


def _convert_equivalent_angle_of_slope_to_surcharge_angle(
    equivalent_slope_angle_rad: float,
) -> float:
    """
    Convert the equivalent slope angle to the surcharge angle.

    Parameters:
    equivalent_slope_angle_rad (float): The equivalent slope angle in radians.

    Returns:
    float: The surcharge angle in radians.
    """
    # Calculate the tangent of the angle in radians
    tan_value = math.tan(equivalent_slope_angle_rad)

    # Convert the tangent value to the surcharge angle in radians
    surcharge_angle_radians = math.atan(3 / 2 * tan_value)

    # Return the surcharge angle in radians
    return surcharge_angle_radians


def _convert_surcharge_angle_to_equivalent_angle_of_slope(
    surcharge_angle_rad: float,
) -> float:
    """
    Convert the surcharge angle to the equivalent slope angle.

    Parameters:
    surcharge_angle_rad (float): The surcharge angle in radians.

    Returns:
    float: The equivalent slope angle in radians.
    """
    # Calculate the tangent of the angle in radians
    tan_value = math.tan(surcharge_angle_rad)

    # Convert the tangent value to the equivalent slope angle in radians
    equivalent_slope_angle_radians = math.atan(2 / 3 * tan_value)

    # Return the equivalent slope angle in radians
    return equivalent_slope_angle_radians


def _get_material_bed_depth(
    length_of_material_on_side_roll: float,
    troughing_angle_rad: float,
    center_roll_length: float,
    slope_angle_rad: float,
) -> float:
    """
    Calculates the material bed depth on a conveyor belt based on the geometry of the belt and material.
    Args:
        length_of_material_on_side_roll (float): The length of the material on the side roll (in meters).
        troughing_angle_rad (float): The troughing angle of the conveyor belt (in radians).
        center_roll_length (float): The length of the center roll (in meters).
        slope_angle_rad (float): The slope angle of the conveyor belt (in radians).
    Returns:
        float: The calculated material bed depth (in meters).
    """
    # Calculate the material bed depth using the provided formula
    material_bed_depth = length_of_material_on_side_roll * math.sin(
        troughing_angle_rad
    ) + (
        center_roll_length / 2
        + length_of_material_on_side_roll * math.cos(troughing_angle_rad)
    ) * math.tan(slope_angle_rad)

    return material_bed_depth


def _material_bed_width(
    center_roll_length: float,
    length_of_material_cover_on_wing_roll: float,
    troughing_angle_rad: float,
) -> float:
    r"""
    Calculate the material bed width at the wing rollers.

    This is the effective width of material covering the belt at the wing idler level,
    accounting for the troughing angle and the material coverage on wing rolls.

    Parameters
    ----------
    center_roll_length : float
        The length of the center idler roll [mm]
    length_of_material_cover_on_wing_roll : float
        The length of material covering the wing rolls [mm]
    troughing_angle_rad : float
        The troughing angle in radians [rad]

    Returns
    -------
    float
        The material bed width at wing rollers [mm]

    Notes
    -----
    The calculation follows the formula:

    .. math::

        b_{material} = l_m + 2 \cos(\lambda) \cdot L_{cover}

    Where:
    - b_material is the material bed width at wing rollers [mm]
    - l_m is the center roll length [mm]
    - λ is the troughing angle [rad]
    - L_cover is the length of material cover on wing roll [mm]
    """
    return (
        center_roll_length
        + 2 * math.cos(troughing_angle_rad) * length_of_material_cover_on_wing_roll
    )
