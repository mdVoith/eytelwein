from pint import Quantity
from eytelwein.main.units import get_unit_registry
from eytelwein.din_22101.core._design_layout_of_drive_system import (
    _height_difference_from_section_length_and_inclination_angle,
    _angle_of_inclination_from_height_difference_and_section_length,
    _section_length_from_height_difference_and_inclination_angle,
)

# Get the unit registry
u = get_unit_registry()


def height_difference_from_section_length_and_inclination_angle(
    section_length: Quantity,
    inclination_angle: Quantity,
    unit: str = "meter",
    precision: int = 3,
) -> Quantity:
    """
    Calculate the height difference from the section length and inclination angle.

    This function calculates the vertical height difference of a conveyor section
    based on its length and inclination angle using the formula:

    H = L * sin(α)

    Where:
    - H is the height difference
    - L is the section length
    - α is the inclination angle

    Parameters
    ----------
    section_length : Quantity
        The length of the conveyor section (typically in meters).
    inclination_angle : Quantity
        The angle of inclination of the conveyor (typically in degrees).
    unit : str, optional
        The desired unit for the output height difference. Default is "meter".
    precision : int, optional
        The number of decimal places for the result. Default is 3.

    Returns
    -------
    Quantity
        The calculated height difference with the specified unit.

    Raises
    ------
    ValueError
        If there is an error in converting units: {e}
        If the section length is negative.
    """
    try:
        # Convert inputs to standard units
        length_m = section_length.to(u.meter)
        angle_rad = inclination_angle.to(u.radian)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate input values
    if length_m.magnitude < 0:
        raise ValueError(f"Section length must be non-negative, got {section_length}")

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call the private implementation with raw values
    result_value = _height_difference_from_section_length_and_inclination_angle(
        length_m.magnitude, angle_rad.magnitude
    )

    # Attach the appropriate unit and convert to requested unit
    result = (result_value * u.meter).to(pint_unit)

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def angle_of_inclination_from_height_difference_and_section_length(
    height_difference: Quantity,
    section_length: Quantity,
    unit: str = "radian",
    precision: int = 3,
) -> Quantity:
    """
    Calculate the angle of inclination from the height difference and section length.

    This function calculates the angle of inclination of a conveyor section
    based on its height difference and section length using the formula:

    α = arcsin(H / L)

    Where:
    - α is the angle of inclination
    - H is the height difference
    - L is the section length

    Parameters
    ----------
    height_difference : Quantity
        The vertical height difference of the conveyor section (typically in meters).
    section_length : Quantity
        The length of the conveyor section (typically in meters).
    unit : str, optional
        The desired unit for the output angle. Default is "radian". Common alternatives are "degree".
    precision : int, optional
        The number of decimal places for the result. Default is 3.

    Returns
    -------
    Quantity
        The calculated angle of inclination with the specified unit.

    Raises
    ------
    ValueError
        If there is an error in converting units: {e}
        If the section length is negative or zero.
        If the height difference is greater than the section length in magnitude.
    """
    try:
        # Convert inputs to standard units
        height_m = height_difference.to(u.meter)
        length_m = section_length.to(u.meter)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate input values
    if length_m.magnitude <= 0:
        raise ValueError(f"Section length must be positive, got {section_length}")

    if abs(height_m.magnitude) > length_m.magnitude:
        raise ValueError(
            f"Height difference ({height_difference}) cannot exceed section length ({section_length}) in magnitude"
        )  # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
        # Verify it's an angle unit by attempting conversion
        (1.0 * u.radian).to(pint_unit)
    except Exception as e:
        raise ValueError(f"Invalid angle unit: {unit}. Error: {e}")

    # Call the private implementation with raw values
    result_value = _angle_of_inclination_from_height_difference_and_section_length(
        height_m.magnitude, length_m.magnitude
    )

    # Attach the appropriate unit and convert to requested unit
    result = (result_value * u.radian).to(pint_unit)

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def section_length_from_height_difference_and_inclination_angle(
    height_difference: Quantity,
    inclination_angle: Quantity,
    unit: str = "meter",
    precision: int = 3,
) -> Quantity:
    """
    Calculate the section length from the height difference and inclination angle.

    This function calculates the length of a conveyor section based on its
    height difference and inclination angle using the formula:

    L = H / sin(α)

    Where:
    - L is the section length
    - H is the height difference
    - α is the inclination angle

    Parameters
    ----------
    height_difference : Quantity
        The vertical height difference of the conveyor section (typically in meters).
    inclination_angle : Quantity
        The angle of inclination of the conveyor (typically in degrees).
    unit : str, optional
        The desired unit for the output section length. Default is "meter".
    precision : int, optional
        The number of decimal places for the result. Default is 3.

    Returns
    -------
    Quantity
        The calculated section length with the specified unit.

    Raises
    ------
    ValueError
        If there is an error in converting units: {e}
        If the height difference is negative.
        If the inclination angle is zero or very close to zero.
    """
    try:
        # Convert inputs to standard units
        height_m = height_difference.to(u.meter)
        angle_rad = inclination_angle.to(u.radian)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate input values
    if height_m.magnitude < 0:
        raise ValueError(
            f"Height difference must be non-negative, got {height_difference}"
        )

    if abs(angle_rad.magnitude) < 1e-10:
        raise ValueError(
            f"Inclination angle cannot be zero or very close to zero, got {inclination_angle}. "
            "Division by sin(0) would lead to infinity."
        )

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call the private implementation with raw values
    result_value = _section_length_from_height_difference_and_inclination_angle(
        height_m.magnitude, angle_rad.magnitude
    )

    # Attach the appropriate unit and convert to requested unit
    result = (result_value * u.meter).to(pint_unit)

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
