from typing import Optional

from pint import Quantity
from eytelwein.din_22101.extended._volume_flow_mass_flow import (
    _maximal_cross_section_skirt_board_known_geometry,
    _required_skirtboard_height_from_cross_section,
    _get_usable_belt_width_from_skirt_board_width,
    _convert_equivalent_angle_of_slope_to_surcharge_angle,
    _convert_surcharge_angle_to_equivalent_angle_of_slope,
    _convert_surcharge_angles,
    _get_material_bed_depth,
    _material_bed_width,
)

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def maximal_cross_section_skirt_board_known_geometry(
    center_roll_length: Quantity,
    skirt_board_width: Quantity,
    skirt_board_height: Quantity,
    troughing_angle: Quantity,
    equivalent_slope_angle: Quantity,
    unit: str = "millimeter**2",
    precision: int = 5,
) -> Quantity:
    try:
        # Convert quantities to millimeters and angles to radians
        center_roll_length_mm = center_roll_length.to(u.millimeter)
        skirt_board_width_mm = skirt_board_width.to(u.millimeter)
        skirt_board_height_mm = skirt_board_height.to(u.millimeter)
        troughing_angle_rad = troughing_angle.to(u.radian)
        equivalent_slope_angle_rad = equivalent_slope_angle.to(u.radian)
    except Exception as e:
        raise ValueError(f"Error in converting: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the maximal cross-sectional area of a skirt board with known geometry.
    maximal_cross_section_mm = (
        _maximal_cross_section_skirt_board_known_geometry(
            center_roll_length_mm.magnitude,
            skirt_board_width_mm.magnitude,
            skirt_board_height_mm.magnitude,
            troughing_angle_rad.magnitude,
            equivalent_slope_angle_rad.magnitude,
        )
        * u.millimeter**2
    )

    # Check if the result is physically meaningful.
    if maximal_cross_section_mm.magnitude < 0:
        raise ValueError(
            "Calculated cross-section area is negative, which is physically impossible."
        )

    # First convert to the requested output unit
    result = maximal_cross_section_mm.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


############################
def required_skirtboard_height_from_cross_section(
    center_roll_length: Quantity,
    skirt_board_width: Quantity,
    troughing_angle: Quantity,
    equivalent_slope_angle: Quantity,
    cross_section: Quantity,
    unit: str = "millimeter",
    precision: int = 5,
) -> Quantity:
    try:
        # Convert quantities to millimeters and angles to radians
        center_roll_length_mm = center_roll_length.to(u.millimeter)
        skirt_board_width_mm = skirt_board_width.to(u.millimeter)
        troughing_angle_rad = troughing_angle.to(u.radian)
        equivalent_slope_angle_rad = equivalent_slope_angle.to(u.radian)
        cross_section_mm2 = cross_section.to(u.millimeter**2)
    except Exception as e:
        raise ValueError(f"Error in converting: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    skirtboard_height_mm = (
        _required_skirtboard_height_from_cross_section(
            center_roll_length_mm.magnitude,
            skirt_board_width_mm.magnitude,
            troughing_angle_rad.magnitude,
            equivalent_slope_angle_rad.magnitude,
            cross_section_mm2.magnitude,
        )
        * u.millimeter
    )

    # Check if the result is physically meaningful.
    if skirtboard_height_mm.magnitude < 0:
        raise ValueError(
            "Calculated skirt board height is negative, which is physically impossible."
        )

    # First convert to the requested output unit
    result = skirtboard_height_mm.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def get_usable_belt_width_from_skirt_board_width(
    skirt_board_width: Quantity,
    center_roll_length: Quantity,
    troughing_angle: Quantity,
    unit: str = "millimeter",
    precision: int = 5,
) -> Quantity:
    try:
        # Convert quantities to millimeters and angles to radians
        skirt_board_width_mm = skirt_board_width.to(u.millimeter)
        center_roll_length_mm = center_roll_length.to(u.millimeter)
        troughing_angle_rad = troughing_angle.to(u.radian)
    except Exception as e:
        raise ValueError(f"Error in converting: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    usable_belt_width_mm = (
        _get_usable_belt_width_from_skirt_board_width(
            skirt_board_width_mm.magnitude,
            center_roll_length_mm.magnitude,
            troughing_angle_rad.magnitude,
        )
        * u.millimeter
    )
    # Check if the result is physically meaningful.
    if usable_belt_width_mm.magnitude < 0:
        raise ValueError(
            "Calculated skirt board height is negative, which is physically impossible."
        )

    # First convert to the requested output unit
    result = usable_belt_width_mm.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def convert_equivalent_angle_of_slope_to_surcharge_angle(
    equivalent_slope_angle: Quantity,
    unit: str = "degree",
    precision: int = 5,
) -> Quantity:
    try:
        # Convert angle to radians for internal calculations
        equivalent_slope_angle_rad = equivalent_slope_angle.to(u.radian)
    except Exception as e:
        raise ValueError(f"Error in converting: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the surcharge angle in radians
    surcharge_angle_rad = (
        _convert_equivalent_angle_of_slope_to_surcharge_angle(
            equivalent_slope_angle_rad.magnitude
        )
        * u.radian
    )
    # Check if the result is physically meaningful.
    if surcharge_angle_rad.magnitude < 0:
        raise ValueError(
            "Calculated surcharge angle is negative, which is physically impossible."
        )  # First convert to the requested output unit
    result = surcharge_angle_rad.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def convert_surcharge_angle_to_equivalent_angle_of_slope(
    surcharge_angle: Quantity,
    unit: str = "degree",
    precision: int = 5,
) -> Quantity:
    try:
        # Convert angle to radians for internal calculations
        surcharge_angle_rad = surcharge_angle.to(u.radian)
    except Exception as e:
        raise ValueError(f"Error in converting: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the equivalent slope angle in radians
    equivalent_slope_angle_rad = (
        _convert_surcharge_angle_to_equivalent_angle_of_slope(
            surcharge_angle_rad.magnitude
        )
        * u.radian
    )
    # Check if the result is physically meaningful.
    if equivalent_slope_angle_rad.magnitude < 0:
        raise ValueError(
            "Calculated equivalent slope angle is negative, which is physically impossible."
        )

    # First convert to the requested output unit
    result = equivalent_slope_angle_rad.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def convert_surcharge_angles(
    equivalent_slope_angle_DIN22101: Optional[Quantity] = None,
    surcharge_angle_ISO5048: Optional[Quantity] = None,
    unit: str = "degree",
    precision: int = 5,
) -> dict:
    try:
        # Convert angles to radians for internal calculations
        if equivalent_slope_angle_DIN22101:
            equivalent_slope_angle_DIN22101_rad = equivalent_slope_angle_DIN22101.to(
                u.radian
            )
        else:
            equivalent_slope_angle_DIN22101_rad = None
        if surcharge_angle_ISO5048:
            surcharge_angle_ISO5048_rad = surcharge_angle_ISO5048.to(u.radian)
        else:
            surcharge_angle_ISO5048_rad = None
    except Exception as e:
        raise ValueError(f"Error in converting: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    angles_rad = _convert_surcharge_angles(
        equivalent_slope_angle_DIN22101_rad.magnitude
        if equivalent_slope_angle_DIN22101_rad
        else None,
        surcharge_angle_ISO5048_rad.magnitude if surcharge_angle_ISO5048_rad else None,
    )

    # Convert each value in the dictionary to radians
    angles_rad = {k: v * u.radian for k, v in angles_rad.items()}

    # First convert to the requested output unit
    angles_converted = {k: v.to(pint_unit) for k, v in angles_rad.items()}

    # Then apply precision if specified
    if precision is not None:
        angles_converted = {k: round(v, precision) for k, v in angles_converted.items()}

    return {
        k: {"value": v.magnitude, "unit": str(v.units)}
        for k, v in angles_converted.items()
    }


def get_material_bed_depth(
    length_of_material_on_side_roll: Quantity,
    troughing_angle: Quantity,
    center_roll_length: Quantity,
    slope_angle: Quantity,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the material bed depth on a conveyor belt based on the geometry of the belt and material.

    This function calculates the material bed depth using the formula:

    material_bed_depth = length_of_material_on_side_roll * sin(troughing_angle) +
                        (center_roll_length/2 + length_of_material_on_side_roll * cos(troughing_angle)) *
                        tan(slope_angle)

    Parameters:
    length_of_material_on_side_roll (Quantity): The length of material on the side roll.
    troughing_angle (Quantity): The troughing angle of the conveyor belt.
    center_roll_length (Quantity): The length of the center roll.
    slope_angle (Quantity): The slope angle of the material.
    unit (str, optional): The unit for the returned depth. Defaults to "millimeter".
    precision (int, optional): The number of decimal places to round the result to. Defaults to 2.

    Returns:
    Quantity: The calculated material bed depth with the specified unit.

    Raises:
    ValueError: If there is an error in converting units.
    """
    try:
        # Convert inputs to standard units for calculation
        length_mm = length_of_material_on_side_roll.to(u.millimeter)
        troughing_angle_rad = troughing_angle.to(u.radian)
        center_roll_length_mm = center_roll_length.to(u.millimeter)
        slope_angle_rad = slope_angle.to(u.radian)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the material bed depth using the private implementation
    depth_mm = (
        _get_material_bed_depth(
            length_mm.magnitude,
            troughing_angle_rad.magnitude,
            center_roll_length_mm.magnitude,
            slope_angle_rad.magnitude,
        )
        * u.millimeter
    )

    # First convert to the requested output unit
    result = depth_mm.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def material_bed_width(
    center_roll_length: Quantity,
    length_of_material_cover_on_wing_roll: Quantity,
    troughing_angle: Quantity,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    r"""
    Calculate the material bed width at the wing rollers.

    This is the effective width of material covering the belt at the wing idler level,
    accounting for the troughing angle and the material coverage on wing rolls. This value
    is used for visualization and analysis of the conveyor belt cross-section.

    Parameters
    ----------
    center_roll_length : Quantity
        The length of the center idler roll [length unit]
    length_of_material_cover_on_wing_roll : Quantity
        The length of material covering the wing rolls [length unit]
    troughing_angle : Quantity
        The troughing angle [angle unit]
    unit : str, optional
        The output unit for the result (default: "millimeter")
    precision : int, optional
        The number of decimal places for rounding (default: 2)

    Returns
    -------
    Quantity
        The material bed width at wing rollers with the specified unit

    Raises
    ------
    ValueError
        If there is an error in converting units or if unit is invalid

    Notes
    -----
    The calculation follows the formula:

    .. math::

        b_{material} = l_m + 2 \cos(\lambda) \cdot L_{cover}

    Where:
    - b_material is the material bed width at wing rollers
    - l_m is the center roll length
    - λ is the troughing angle
    - L_cover is the length of material cover on wing roll

    This is a simplified form of: l_m + 2*cos(λ)*GBjeSeite - 2*Gurtrand_Real
    which simplifies to l_m + 2*cos(λ)*(GBjeSeite - Gurtrand_Real)
    since GBjeSeite - Gurtrand_Real = length_of_material_cover_on_wing_roll.
    """
    try:
        # Convert quantities to millimeters and angles to radians
        center_roll_length_mm = center_roll_length.to(u.millimeter)
        length_of_material_cover_mm = length_of_material_cover_on_wing_roll.to(
            u.millimeter
        )
        troughing_angle_rad = troughing_angle.to(u.radian)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the material bed width using the private implementation
    width_mm = (
        _material_bed_width(
            center_roll_length_mm.magnitude,
            length_of_material_cover_mm.magnitude,
            troughing_angle_rad.magnitude,
        )
        * u.millimeter
    )

    # Check if the result is physically meaningful
    if width_mm.magnitude <= 0:
        raise ValueError(
            "Calculated material bed width is non-positive, which is physically impossible."
        )

    # First convert to the requested output unit
    result = width_mm.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
