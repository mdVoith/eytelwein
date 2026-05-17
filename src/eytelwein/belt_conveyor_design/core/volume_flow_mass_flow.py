from pint import Quantity
import math

from eytelwein.belt_conveyor_design.core._volume_flow_mass_flow import (
    _solve_for_used_belt_width_from_cross_section,
    _usable_belt_width,
    _partial_cross_section_at_water_fill,
    _partial_cross_section_above_water_fill,
    _cross_section_of_fill,
    _volume_flow_from_cross_section_speed,
    _mass_flow_from_volume_flow_density,
    _volume_flow_from_mass_flow_density,
    _mass_flow_from_cross_section_speed_density,
    _cross_section_from_volume_flow_speed,
    _cross_section_from_mass_flow_speed_density,
    _nominal_volume_flow,
    _nominal_mass_flow,
    _line_load_from_nominal_load,
    _line_load_from_nominal_mass_flow_speed,
    _belt_edge_distance,
    _length_of_material_on_side_roll,
    _reduction_factor_inclined_fill_1,
    _effective_filling_ratio_from_areas,
    _reduction_factor_inclined_fill,
    _effective_filling_ratio,
)
from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def usable_belt_width(
    belt_width: Quantity,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the usable belt width based on the given belt width.

    This function serves as a wrapper for the `_usable_belt_width` function, ensuring that the input is a `Quantity`
    with units of millimeters.

    Parameters:
    belt_width (Quantity): The total width of the belt as a `Quantity` with units of millimeters.
    unit (str, optional): The unit for the returned width. Defaults to "millimeter".
    precision (int, optional): The number of decimal places to round the result to. Defaults to 2.

    Returns:
    Quantity: The usable width of the belt as a `Quantity` with the specified unit.
    """
    try:
        # Convert belt_width to millimeters
        belt_width_mm = belt_width.to(u.millimeter)
    except Exception as e:
        raise ValueError(f"Error in converting belt_width: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the usable belt width using the _usable_belt_width function
    b = _usable_belt_width(belt_width_mm.magnitude)

    # Create a Quantity with millimeter units
    result_mm = b * u.millimeter

    # First convert to the requested output unit
    result = result_mm.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def partial_cross_section_above_water_fill(
    center_roll_length: Quantity,
    usable_belt_width: Quantity,
    troughing_angle: Quantity,
    equivalent_slope_angle: Quantity,
    unit: str = "millimeter**2",
    precision: int = 5,
) -> Quantity:
    try:
        # Convert center_roll_length to millimeters
        center_roll_length_mm = center_roll_length.to(u.millimeter)

        # Convert usable_belt_width to millimeters
        usable_belt_width_mm = usable_belt_width.to(u.millimeter)

        # Convert troughing_angle to degrees
        troughing_angle_degree = troughing_angle.to(u.degree)

        # Convert troughing_angle to degrees
        equivalent_slope_angle_degree = equivalent_slope_angle.to(u.degree)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(
            f"Invalid unit: {unit}. Error: {e}"
        )  # Calculate the cross-section area above the water fill using the _partial_cross_section_above_water_fill function,
    # which returns a float and convert it to square millimeters using pint Quantity.

    area_mm2 = (
        _partial_cross_section_above_water_fill(
            center_roll_length_mm.magnitude,
            usable_belt_width_mm.magnitude,
            math.radians(troughing_angle_degree.magnitude),
            math.radians(equivalent_slope_angle_degree.magnitude),
        )
        * u.millimeter**2
    )

    # Check if the result is physically meaningful.
    if area_mm2.magnitude < 0:
        raise ValueError(
            "Calculated cross-section area A_1 is negative, which is physically impossible."
        )

    # First convert to the requested output unit
    result = area_mm2.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def partial_cross_section_at_water_fill(
    center_roll_length: Quantity,
    usable_belt_width: Quantity,
    troughing_angle: Quantity,
    unit: str = "millimeter**2",
    precision: int = 5,
) -> Quantity:
    """
    Calculate the partial cross-sectional area of the belt at water fill.

    This function calculates the area based on the given center roll length, usable belt width, and troughing angle.
    The formula used takes into account the geometry of the belt and the troughing angle to determine the area.

    Parameters:
    center_roll_length (Quantity): The length of the center roll as a `Quantity` with units of millimeters.
    usable_belt_width (Quantity): The usable width of the belt as a `Quantity` with units of millimeters.
    troughing_angle (Quantity): The troughing angle as a `Quantity` with units of degrees.
    unit (str, optional): The unit for the returned area. Defaults to "millimeter**2".
    precision (int, optional): The number of decimal places to round the result to. Defaults to 5.

    Returns:
    Quantity: The calculated partial cross-sectional area as a `Quantity` with the specified unit.

    Raises:
    ValueError: If there is an error in converting units or if the calculated area is negative.
    """
    try:
        # Convert center_roll_length to millimeters
        center_roll_length_mm = center_roll_length.to(u.millimeter)

        # Convert usable_belt_width to millimeters
        usable_belt_width_mm = usable_belt_width.to(u.millimeter)

        # Convert troughing_angle to degrees
        troughing_angle_degree = troughing_angle.to(u.degree)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(
            f"Invalid unit: {unit}. Error: {e}"
        )  # Calculate the cross-section area at the water fill using the _partial_cross_section_at_water_fill function,
    # which returns a float and convert it to square millimeters using pint Quantity.
    area_mm2 = (
        _partial_cross_section_at_water_fill(
            center_roll_length_mm.magnitude,
            usable_belt_width_mm.magnitude,
            math.radians(
                troughing_angle_degree.magnitude
            ),  # Convert to radians for the private function
        )
        * u.millimeter**2
    )

    # Check if the result is physically meaningful.
    if area_mm2.magnitude < 0:
        raise ValueError(
            "Calculated cross-section area A_2 is negative, which is physically impossible."
        )

    # First convert to the requested output unit
    result = area_mm2.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def cross_section_of_fill(
    center_roll_length: Quantity,
    usable_belt_width: Quantity,
    troughing_angle: Quantity,
    equivalent_slope_angle: Quantity,
    unit: str = "millimeter**2",
    precision: int = 5,
) -> Quantity:
    """
    Calculate the total cross-sectional area of the belt fill.

    This function calculates the total cross-sectional area by summing the partial cross-sectional areas
    at water fill and above water fill. The calculations are based on the given center roll length, usable belt width,
    troughing angle, and equivalent slope angle.

    Parameters:
    center_roll_length (Quantity): The length of the center roll as a `Quantity` with units of millimeters.
    usable_belt_width (Quantity): The usable width of the belt as a `Quantity` with units of millimeters.
    troughing_angle (Quantity): The troughing angle as a `Quantity` with units of degrees.
    equivalent_slope_angle (Quantity): The equivalent slope angle as a `Quantity` with units of degrees.
    unit (str, optional): The unit for the returned area. Defaults to "millimeter**2".
    precision (int, optional): The number of decimal places to round the result to. Defaults to 5.

    Returns:
    Quantity: The calculated total cross-sectional area as a `Quantity` with the specified unit.

    Raises:
    ValueError: If there is an error in converting units or if the calculated area is negative.
    """
    try:
        # Convert center_roll_length to millimeters
        center_roll_length_mm = center_roll_length.to(u.millimeter)

        # Convert usable_belt_width to millimeters
        usable_belt_width_mm = usable_belt_width.to(u.millimeter)

        # Convert troughing_angle to degrees
        troughing_angle_degree = troughing_angle.to(u.degree)

        # Convert troughing_angle to degrees
        equivalent_slope_angle_degree = equivalent_slope_angle.to(u.degree)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(
            f"Invalid unit: {unit}. Error: {e}"
        )  # Calculate the cross-section area using the _cross_section_of_fill function,
    # which returns a float and convert it to square millimeters using pint Quantity.
    area_mm2 = (
        _cross_section_of_fill(
            center_roll_length_mm.magnitude,
            usable_belt_width_mm.magnitude,
            math.radians(troughing_angle_degree.magnitude),
            math.radians(equivalent_slope_angle_degree.magnitude),
        )
        * u.millimeter**2
    )

    # Check if the result is physically meaningful.
    if area_mm2.magnitude < 0:
        raise ValueError(
            "Calculated cross-section area A is negative, which is physically impossible."
        )

    # First convert to the requested output unit
    result = area_mm2.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def volume_flow_from_cross_section_speed(
    cross_section_of_fill: Quantity,
    belt_speed: Quantity,
    unit: str = "meter**3/second",
    precision: int = 5,
) -> Quantity:
    try:
        cross_section_of_fill_m2 = cross_section_of_fill.to(u.meter**2)
        belt_speed_mps = belt_speed.to(u.meter / u.second)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    v_flow = (
        _volume_flow_from_cross_section_speed(
            cross_section_of_fill_m2.magnitude, belt_speed_mps.magnitude
        )
        * u.meter**3
        / u.second
    )

    # First convert to the requested output unit
    result = v_flow.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def mass_flow_from_volume_flow_density(
    volume_flow: Quantity,
    bulk_density: Quantity,
    unit: str = "kilogram/second",
    precision: int = 5,
) -> Quantity:
    try:
        volume_flow_m3ps = volume_flow.to(u.meter**3 / u.second)
        bulk_density_kgpm3 = bulk_density.to(u.kilogram / u.meter**3)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    m_flow = (
        _mass_flow_from_volume_flow_density(
            volume_flow_m3ps.magnitude, bulk_density_kgpm3.magnitude
        )
        * u.kilogram
        / u.second
    )

    # First convert to the requested output unit
    result = m_flow.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def volume_flow_from_mass_flow_density(
    m_flow: Quantity,
    bulk_density: Quantity,
    unit: str = "meter**3/second",
    precision: int = 5,
) -> Quantity:
    """
    Calculate the volume flow of material from mass flow and bulk density.

    This function calculates the volume flow rate by dividing the mass flow by the bulk density.
    It is the inverse of `mass_flow_from_volume_flow_density` and is useful when you have the mass
    flow and density and need to find the volumetric flow rate.

    Parameters
    ----------
    m_flow : Quantity
        The mass flow of material in kilograms per second [kg/s]
    bulk_density : Quantity
        The bulk density of the material in kilograms per cubic meter [kg/m³]
    unit : str, optional
        The unit for the returned volume flow. Defaults to "meter**3/second".
    precision : int, optional
        The number of decimal places to round the result to. Defaults to 5.

    Returns
    -------
    Quantity
        The calculated volume flow in the specified unit [m³/s]

    Raises
    ------
    ValueError
        If bulk_density is zero or negative
        If unit conversion fails
        If invalid output unit is specified

    Notes
    -----
    The calculation follows the formula:

    .. math::

        Q = \frac{m}{\rho}

    Where:
    - Q is the volume flow [m³/s]
    - m is the mass flow [kg/s]
    - ρ is the bulk density [kg/m³]

    This function is the inverse of `mass_flow_from_volume_flow_density`.

    Examples
    --------
    >>> import eytelwein.main.units as u
    >>> from eytelwein.belt_conveyor_design import volume_flow_from_mass_flow_density
    >>> m_flow = 1800 * u.kilogram / u.second
    >>> density = 1200 * u.kilogram / u.meter**3
    >>> volume_flow = volume_flow_from_mass_flow_density(m_flow, density)
    >>> print(volume_flow)  # doctest: +SKIP
    1.5 meter ** 3 / second
    """
    try:
        m_flow_kgps = m_flow.to(u.kilogram / u.second)
        bulk_density_kgpm3 = bulk_density.to(u.kilogram / u.meter**3)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    v_flow = (
        _volume_flow_from_mass_flow_density(
            m_flow_kgps.magnitude, bulk_density_kgpm3.magnitude
        )
        * u.meter**3
        / u.second
    )

    # First convert to the requested output unit
    result = v_flow.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def mass_flow_from_cross_section_speed_density(
    cross_section_of_fill: Quantity,
    belt_speed: Quantity,
    bulk_density: Quantity,
    unit: str = "kilogram/second",
    precision: int = 5,
) -> Quantity:
    try:
        cross_section_of_fill_m2 = cross_section_of_fill.to(u.meter**2)
        belt_speed_mps = belt_speed.to(u.meter / u.second)
        bulk_density_kgpm3 = bulk_density.to(u.kilogram / u.meter**3)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    m_flow = (
        _mass_flow_from_cross_section_speed_density(
            cross_section_of_fill_m2.magnitude,
            belt_speed_mps.magnitude,
            bulk_density_kgpm3.magnitude,
        )
        * u.kilogram
        / u.second
    )

    # First convert to the requested output unit
    result = m_flow.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def cross_section_from_volume_flow_speed(
    volume_flow: Quantity,
    belt_speed: Quantity,
    unit: str = "meter**2",
    precision: int = 5,
) -> Quantity:
    try:
        volume_flow_m3ps = volume_flow.to(u.meter**3 / u.second)
        belt_speed_mps = belt_speed.to(u.meter / u.second)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    cross_section = (
        _cross_section_from_volume_flow_speed(
            volume_flow_m3ps.magnitude, belt_speed_mps.magnitude
        )
        * u.meter**2
    )

    # First convert to the requested output unit
    result = cross_section.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def cross_section_from_mass_flow_speed_density(
    mass_flow: Quantity,
    belt_speed: Quantity,
    bulk_density: Quantity,
    unit: str = "meter**2",
    precision: int = 5,
) -> Quantity:
    try:
        mass_flow_kgps = mass_flow.to(u.kilogram / u.second)
        belt_speed_mps = belt_speed.to(u.meter / u.second)
        bulk_density_kgpm3 = bulk_density.to(u.kilogram / u.meter**3)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    cross_section = (
        _cross_section_from_mass_flow_speed_density(
            mass_flow_kgps.magnitude,
            belt_speed_mps.magnitude,
            bulk_density_kgpm3.magnitude,
        )
        * u.meter**2
    )

    # First convert to the requested output unit
    result = cross_section.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def nominal_volume_flow(
    theoretical_volume_flow: Quantity,
    effective_filling_ratio: float,
    unit: str = "meter**3/second",
    precision: int = 5,
) -> Quantity:
    try:
        theoretical_volume_flow_m3ps = theoretical_volume_flow.to(u.meter**3 / u.second)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    nominal_v_flow = (
        _nominal_volume_flow(
            theoretical_volume_flow_m3ps.magnitude, effective_filling_ratio
        )
        * u.meter**3
        / u.second
    )

    # First convert to the requested output unit
    result = nominal_v_flow.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def nominal_mass_flow(
    theoretical_volume_flow: Quantity,
    effective_filling_ratio: float,
    bulk_density: Quantity,
    unit: str = "kilogram/second",
    precision: int = 5,
) -> Quantity:
    try:
        theoretical_volume_flow_m3ps = theoretical_volume_flow.to(u.meter**3 / u.second)
        bulk_density_kgpm3 = bulk_density.to(u.kilogram / u.meter**3)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    nominal_m_flow = (
        _nominal_mass_flow(
            theoretical_volume_flow_m3ps.magnitude,
            effective_filling_ratio,
            bulk_density_kgpm3.magnitude,
        )
        * u.kilogram
        / u.second
    )

    # First convert to the requested output unit
    result = nominal_m_flow.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def line_load_from_nominal_load(
    theoretical_cross_section: Quantity,
    effective_filling_ratio: float,
    bulk_density: Quantity,
    unit: str = "kilogram/meter",
    precision: int = 5,
) -> Quantity:
    try:
        theoretical_cross_section_m2 = theoretical_cross_section.to(u.meter**2)
        bulk_density_kgpm3 = bulk_density.to(u.kilogram / u.meter**3)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    line_load = (
        _line_load_from_nominal_load(
            theoretical_cross_section_m2.magnitude,
            effective_filling_ratio,
            bulk_density_kgpm3.magnitude,
        )
        * u.kilogram
        / u.meter
    )

    # First convert to the requested output unit
    result = line_load.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def line_load_from_nominal_mass_flow_speed(
    nominal_mass_flow: Quantity,
    belt_speed: Quantity,
    unit: str = "kilogram/meter",
    precision: int = 5,
) -> Quantity:
    try:
        nominal_mass_flow_kgps = nominal_mass_flow.to(u.kilogram / u.second)
        belt_speed_mps = belt_speed.to(u.meter / u.second)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    line_load = (
        _line_load_from_nominal_mass_flow_speed(
            nominal_mass_flow_kgps.magnitude, belt_speed_mps.magnitude
        )
        * u.kilogram
        / u.meter
    )

    # First convert to the requested output unit
    result = line_load.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def solve_for_used_belt_width_from_cross_section(
    target_cross_section: Quantity,
    center_roll_length: Quantity,
    troughing_angle: Quantity,
    equivalent_slope_angle: Quantity,
    initial_guess: Quantity | None = None,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the used belt width required to achieve a specific cross-section area.

    This function uses numerical methods to find the used belt width that would result
    in the specified target cross-section area, given the center roll length,
    troughing angle, and equivalent slope angle.

    Parameters:
    target_cross_section (Quantity): The desired cross-section area as a `Quantity`.
    center_roll_length (Quantity): The length of the center roll as a `Quantity`.
    troughing_angle (Quantity): The troughing angle as a `Quantity`.
    equivalent_slope_angle (Quantity): The equivalent slope angle as a `Quantity`.
    initial_guess (Quantity, optional): Initial guess for used belt width.
    unit (str, optional): The unit for the returned width. Defaults to "millimeter".
    precision (int, optional): The number of decimal places to round the result to. Defaults to 2.

    Returns:
    Quantity: The calculated used belt width as a `Quantity` with the specified unit.

    Raises:
    ValueError: If there is an error in converting units or if the solution doesn't converge.
    """
    try:
        # Convert all inputs to required units for calculation
        target_area_mm2 = target_cross_section.to(u.millimeter**2)
        center_roll_length_mm = center_roll_length.to(u.millimeter)
        troughing_angle_degree = troughing_angle.to(u.degree)
        equivalent_slope_angle_degree = equivalent_slope_angle.to(u.degree)

        if initial_guess is not None:
            initial_guess_mm = initial_guess.to(u.millimeter).magnitude
        else:
            initial_guess_mm = None

    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(
            f"Invalid unit: {unit}. Error: {e}"
        )  # Perform the calculation using the private implementation
    try:
        usable_width_mm = (
            _solve_for_used_belt_width_from_cross_section(
                target_area_mm2.magnitude,
                center_roll_length_mm.magnitude,
                math.radians(troughing_angle_degree.magnitude),
                math.radians(equivalent_slope_angle_degree.magnitude),
                initial_guess=initial_guess_mm,
            )
            * u.millimeter
        )

    except ValueError as e:
        raise ValueError(f"Calculation error: {e}")

    # First convert to the requested output unit
    result = usable_width_mm.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def belt_edge_distance(
    belt_width: Quantity,
    used_belt_width: Quantity,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the distance between the edge of the belt and the used belt width on each side.

    This function assumes that the belt is symmetric, so the distance is the same on both sides.
    It calculates half the difference between the total belt width and the used belt width.

    Parameters:
    belt_width (Quantity): The total width of the belt as a `Quantity`.
    used_belt_width (Quantity): The width of the belt that is actually used or the usable belt width.
    unit (str, optional): The unit for the returned distance. Defaults to "millimeter".
    precision (int, optional): The number of decimal places to round the result to. Defaults to 2.

    Returns:
    Quantity: The calculated distance from the belt edge to the used belt width on one side.

    Raises:
    ValueError: If there is an error in converting units.
    """
    try:
        # Convert both widths to a common unit (millimeters)
        belt_width_mm = belt_width.to(u.millimeter)
        used_belt_width_mm = used_belt_width.to(u.millimeter)
    except Exception as e:
        raise ValueError(f"Error in converting width units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the belt edge distance using the private implementation
    edge_distance_mm = (
        _belt_edge_distance(belt_width_mm.magnitude, used_belt_width_mm.magnitude)
        * u.millimeter
    )

    # First convert to the requested output unit
    result = edge_distance_mm.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def length_of_material_on_side_roll(
    part_of_belt_lying_on_side_idler: Quantity,
    belt_edge_distance: Quantity,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the length of material on the side roll of a conveyor belt.

    This function calculates the effective length of material on the side roll by subtracting
    the belt edge distance from the part of belt lying on the side idler.

    Parameters:
    part_of_belt_lying_on_side_idler (Quantity): The length of the belt segment that lies on the side idler.
    belt_edge_distance (Quantity): The distance from the edge of the belt to the point where the material ends.
    unit (str, optional): The unit for the returned length. Defaults to "millimeter".
    precision (int, optional): The number of decimal places to round the result to. Defaults to 2.

    Returns:
    Quantity: The calculated effective length of material on the side roll with the specified unit.

    Raises:
    ValueError: If there is an error in converting units.
    """
    try:
        # Convert both lengths to a common unit (millimeters)
        part_on_side_idler_mm = part_of_belt_lying_on_side_idler.to(u.millimeter)
        belt_edge_distance_mm = belt_edge_distance.to(u.millimeter)
    except Exception as e:
        raise ValueError(f"Error in converting length units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the length of material on side roll using the private implementation
    length_mm = (
        _length_of_material_on_side_roll(
            part_on_side_idler_mm.magnitude, belt_edge_distance_mm.magnitude
        )
        * u.millimeter
    )

    # First convert to the requested output unit
    result = length_mm.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def reduction_factor_inclined_fill_1(
    maximal_inclination_angle: Quantity,
    dynamic_angle_of_slope: Quantity,
    unit: str = "dimensionless",
    precision: int = 5,
) -> Quantity:
    """
    Calculate the reduction factor for inclined fill based on the maximal inclination angle and the dynamic angle of slope.

    This function computes a reduction factor used in material handling or bulk solids transport, where the
    inclination of the fill affects the flow characteristics. The calculation is based on the cosine
    squared of the provided angles.

    The formula used is sqrt((cos²(maximal_inclination_angle) - cos²(dynamic_angle_of_slope)) /
                            (1 - cos²(maximal_inclination_angle)))

    Parameters:
    maximal_inclination_angle (Quantity): The maximal inclination angle of the fill as a `Quantity` with units of degrees.
    dynamic_angle_of_slope (Quantity): The dynamic angle of slope as a `Quantity` with units of degrees.
    unit (str, optional): The unit for the returned factor. Defaults to "dimensionless".
    precision (int, optional): The number of decimal places to round the result to. Defaults to 5.

    Returns:
    Quantity: The calculated reduction factor as a dimensionless `Quantity`.

    Raises:
    ValueError: If the maximal inclination angle is greater than the dynamic angle of slope,
               if there is an error in converting units, or if the calculation results in an invalid value.
    """
    try:
        # Convert angles to degrees
        maximal_inclination_angle_degree = maximal_inclination_angle.to(u.degree)
        dynamic_angle_of_slope_degree = dynamic_angle_of_slope.to(u.degree)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    try:
        # Calculate the reduction factor using the private implementation
        reduction_factor = (
            _reduction_factor_inclined_fill_1(
                maximal_inclination_angle_degree.magnitude,
                dynamic_angle_of_slope_degree.magnitude,
            )
            * u.dimensionless
        )
    except ValueError as e:
        raise ValueError(f"Calculation error: {e}")
    except ZeroDivisionError:
        raise ValueError(
            "Invalid input: results in division by zero. This occurs when maximal_inclination_angle is 0 or corresponds to 90 degrees."
        )

    # First convert to the requested output unit
    result = reduction_factor.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def reduction_factor_inclined_fill(
    theoretical_partial_cross_section_above_water_fill: Quantity,
    theoretical_cross_section_of_fill: Quantity,
    reduction_factor_inclined_fill_1: Quantity,
    unit: str = "dimensionless",
    precision: int = 5,
) -> Quantity:
    """
    Calculate the reduction factor for inclined fill on a conveyor belt.

    This function calculates a reduction factor used to adjust the cross-sectional area
    of material on an inclined conveyor belt. It accounts for the proportion of material
    above the water fill line and applies a reduction factor based on the inclination.

    The formula used is:
    1 - (theoretical_partial_cross_section_above_water_fill / theoretical_cross_section_of_fill)
        * (1 - reduction_factor_inclined_fill_1)

    Parameters:
    theoretical_partial_cross_section_above_water_fill (Quantity): The theoretical partial
        cross-section above water fill as a `Quantity` with area units.
    theoretical_cross_section_of_fill (Quantity): The theoretical total cross-section of
        fill as a `Quantity` with area units.
    reduction_factor_inclined_fill_1 (Quantity): The first reduction factor for inclined fill
        as a dimensionless `Quantity`.
    unit (str, optional): The unit for the returned factor. Defaults to "dimensionless".
    precision (int, optional): The number of decimal places to round the result to. Defaults to 5.

    Returns:
    Quantity: The calculated reduction factor as a dimensionless `Quantity`.

    Raises:
    ValueError: If theoretical_cross_section_of_fill is zero or if there is an error
               in converting units.
    """
    try:
        # Convert inputs to standard units for calculation
        theoretical_partial_cross_section_above_water_fill_mm2 = (
            theoretical_partial_cross_section_above_water_fill.to(u.millimeter**2)
        )
        theoretical_cross_section_of_fill_mm2 = theoretical_cross_section_of_fill.to(
            u.millimeter**2
        )
        reduction_factor_inclined_fill_1_dim = reduction_factor_inclined_fill_1.to(
            u.dimensionless
        )
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Validate inputs
    if theoretical_cross_section_of_fill_mm2.magnitude == 0:
        raise ValueError("Theoretical cross-section of fill cannot be zero")

    try:
        # Perform the calculation using the private implementation
        result_value = _reduction_factor_inclined_fill(
            theoretical_partial_cross_section_above_water_fill_mm2.magnitude,
            theoretical_cross_section_of_fill_mm2.magnitude,
            reduction_factor_inclined_fill_1_dim.magnitude,
        )
        reduction_factor = result_value * u.dimensionless
    except ZeroDivisionError:
        raise ValueError("Theoretical cross-section of fill cannot be zero")
    except Exception as e:
        raise ValueError(f"Calculation error: {e}")

    # Convert to the requested output unit
    result = reduction_factor.to(pint_unit)

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def effective_filling_ratio(
    filling_ratio_operations: float,
    reduction_factor_inclined_fill: Quantity,
    unit: str = "dimensionless",
    precision: int = 5,
) -> Quantity:
    """
    Calculate the effective filling ratio of a conveyor belt.

    The effective filling ratio represents how much of a conveyor belt's theoretical cross-section
    is actually filled with material under operational conditions, considering both the
    operational filling ratio and the reduction due to inclined fill.

    The formula used is:
    effective_filling_ratio = filling_ratio_operations * reduction_factor_inclined_fill

    Parameters:
    filling_ratio_operations (float): The filling ratio under operational conditions,
        a dimensionless value typically between 0 and 1 representing the operational
        filling level compared to the theoretical maximum.
    reduction_factor_inclined_fill (Quantity): The reduction factor for inclined fill,
        a dimensionless quantity that accounts for material distribution on inclined belts.
    unit (str, optional): The unit for the returned value. Must be dimensionless.
        Defaults to "dimensionless".
    precision (int, optional): The number of decimal places to round the result to.
        Defaults to 5.

    Returns:
    Quantity: The calculated effective filling ratio as a dimensionless `Quantity`.

    Raises:
    ValueError: If there is an error in converting units or if the input values are invalid.
    """
    try:
        # Convert reduction_factor_inclined_fill to dimensionless
        reduction_factor_dim = reduction_factor_inclined_fill.to(u.dimensionless)
    except Exception as e:
        raise ValueError(
            f"Error in converting units: {e}"
        )  # Ensure the unit is a valid Pint unit and is dimensionless
    try:
        pint_unit = u.parse_units(unit)
        # Check if the unit is dimensionless
        if pint_unit.dimensionality != u.dimensionless.dimensionality:
            raise ValueError(
                f"Invalid unit: {unit}. Output unit must be dimensionless."
            )
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the effective filling ratio using the private implementation
    result_value = _effective_filling_ratio(
        filling_ratio_operations, reduction_factor_dim.magnitude
    )

    effective_ratio = result_value * u.dimensionless

    # Convert to the requested output unit (will only work with dimensionless units)
    result = effective_ratio.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def effective_filling_ratio_from_areas(
    theoretical_cross_section_of_fill: Quantity,
    actual_cross_section: Quantity,
    unit: str = "dimensionless",
    precision: int = 5,
) -> Quantity:
    """
    Calculate the effective filling ratio based on the areas of the cross-section.

    This function computes the effective filling ratio by dividing the actual cross-section
    by the theoretical cross-section. It is used in material handling or bulk solids transport
    to determine how full the conveyor belt is compared to its theoretical capacity.

    Parameters
    ----------
    theoretical_cross_section_of_fill : Quantity
        The theoretical maximum cross-sectional area of the fill. Can be in any area unit.
    actual_cross_section : Quantity
        The actual cross-sectional area of the fill. Should have the same unit as
        theoretical_cross_section_of_fill.
    unit : str, optional
        The desired output unit, defaults to "dimensionless". Must be a dimensionless unit.
    precision : int, optional
        The precision of the result (number of decimal places). Default is 5.

    Returns
    -------
    Quantity
        The effective filling ratio as a dimensionless value typically between 0 and 1.

    Raises
    ------
    ValueError
        If the theoretical_cross_section_of_fill is zero or negative.
        If the units of theoretical_cross_section_of_fill and actual_cross_section are not compatible.
        If the specified output unit is not dimensionless.
    """
    # Convert inputs to standard units
    theoretical_area = theoretical_cross_section_of_fill.to("meter**2").magnitude
    actual_area = actual_cross_section.to("meter**2").magnitude

    # Validate inputs
    if theoretical_area <= 0:
        raise ValueError("Theoretical cross-section area must be greater than zero.")

    # Call private implementation
    filling_ratio = _effective_filling_ratio_from_areas(theoretical_area, actual_area)

    # Convert to requested output unit
    try:
        pint_unit = u.Unit(unit)
        # Check if the unit is dimensionless
        if not pint_unit.dimensionless:
            raise ValueError(f"The output unit '{unit}' must be dimensionless.")
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    result = (filling_ratio * u.dimensionless).to(pint_unit)

    # Apply precision
    result = round(result, precision)

    return result


if __name__ == "__main__":
    print(usable_belt_width(55.55 * u.millimeter))
    # print(usable_belt_width(Quantity(50, u.millimeter)))
