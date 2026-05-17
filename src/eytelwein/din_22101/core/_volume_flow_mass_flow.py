import math
from typing import Optional


def _usable_belt_width(belt_width: float) -> float:
    """
    Calculate the usable belt width based on the given belt width.

    The function applies different formulas depending on the belt width:
    - If the belt width is less than or equal to 2000 millimeters, the usable belt width is calculated as 90% of the belt width minus 50 millimeters.
    - If the belt width is greater than 2000 millimeters, the usable belt width is calculated as the belt width minus 250 millimeters.

    Parameters:
    belt_width (float): The total width of the belt in millimeters.

    Returns:
    float: The usable width of the belt in millimeters.
    """
    if belt_width <= 2000:
        return 0.9 * belt_width - 50
    else:
        return belt_width - 250


def _partial_cross_section_at_water_fill(
    center_roll_length: float, usable_belt_width: float, troughing_angle_rad: float
) -> float:
    """
    Calculate the partial cross-sectional area of the belt at water fill.

    This function calculates the area based on the given center roll length, usable belt width, and troughing angle.
    The formula used takes into account the geometry of the belt and the troughing angle to determine the area.

    Parameters:
    center_roll_length (float): The length of the center roll in millimeters.
    usable_belt_width (float): The usable width of the belt in millimeters.
    troughing_angle_rad (float): The troughing angle in radians.

    Returns:
    float: The calculated partial cross-sectional area in square millimeters.
    """
    area = (
        (
            center_roll_length
            + (usable_belt_width - center_roll_length)
            / 2
            * math.cos(troughing_angle_rad)
        )
        * (usable_belt_width - center_roll_length)
        / 2
        * math.sin(troughing_angle_rad)
    )

    return area


def _partial_cross_section_above_water_fill(
    center_roll_length: float,
    usable_belt_width: float,
    troughing_angle_rad: float,
    equivalent_slope_angle_rad: float,
) -> float:
    """
    Calculate the partial cross-sectional area of the belt above the water fill.

    This function calculates the area based on the given center roll length, usable belt width, troughing angle, and equivalent slope angle.
    The formula used takes into account the geometry of the belt and the angles to determine the area.

    Parameters:
    center_roll_length (float): The length of the center roll in millimeters.
    usable_belt_width (float): The usable width of the belt in millimeters.
    troughing_angle_rad (float): The troughing angle in radians.
    equivalent_slope_angle_rad (float): The equivalent slope angle in radians.

    Returns:
    float: The calculated partial cross-sectional area above the water fill in square millimeters.
    """
    area = (
        (
            center_roll_length
            + (usable_belt_width - center_roll_length) * math.cos(troughing_angle_rad)
        )
        ** 2
        * math.tan(equivalent_slope_angle_rad)
        / 4
    )

    return area


def _cross_section_of_fill(
    center_roll_length: float,
    usable_belt_width: float,
    troughing_angle_rad: float,
    equivalent_slope_angle_rad: float,
) -> float:
    """
    Calculate the total cross-sectional area of the belt fill.

    This function calculates the total cross-sectional area by summing the partial cross-sectional areas
    at water fill and above water fill. The calculations are based on the given center roll length, usable belt width,
    troughing angle, and equivalent slope angle.

    Parameters:
    center_roll_length (float): The length of the center roll in millimeters.
    usable_belt_width (float): The usable width of the belt in millimeters.
    troughing_angle_rad (float): The troughing angle in radians.
    equivalent_slope_angle_rad (float): The equivalent slope angle in radians.

    Returns:
    float: The calculated total cross-sectional area in square millimeters.
    """
    area = _partial_cross_section_at_water_fill(
        center_roll_length, usable_belt_width, troughing_angle_rad
    ) + _partial_cross_section_above_water_fill(
        center_roll_length,
        usable_belt_width,
        troughing_angle_rad,
        equivalent_slope_angle_rad,
    )
    return area


def _volume_flow_from_cross_section_speed(
    cross_section_of_fill: float, belt_speed: float
) -> float:
    """
    Calculate the volume flow of material on the conveyor belt.

    This function calculates the volume flow based on the cross-sectional area of the fill and the belt speed.

    Parameters:
    cross_section_of_fill (float): The cross-sectional area of the fill in square meters.
    belt_speed (float): The speed of the conveyor belt in meters per second.

    Returns:
    float: The calculated volume flow in cubic meters per second.
    """
    v_flow = cross_section_of_fill * belt_speed
    return v_flow


def _mass_flow_from_volume_flow_density(
    volume_flow: float, bulk_density: float
) -> float:
    """
    Calculate the mass flow of material on the conveyor belt.

    This function calculates the mass flow based on the volume flow and the bulk density of the material.

    Parameters:
    volume_flow (float): The volume flow of material in cubic meters per second.
    bulk_density (float): The bulk density of the material in kilograms per cubic meter.

    Returns:
    float: The calculated mass flow in kilograms per second.
    """
    m_flow = volume_flow * bulk_density
    return m_flow


def _volume_flow_from_mass_flow_density(m_flow: float, bulk_density: float) -> float:
    """
    Calculate the volume flow of material from mass flow and bulk density.

    This function is the inverse of `_mass_flow_from_volume_flow_density`.
    It calculates the volume flow rate by dividing the mass flow by the bulk density.

    Parameters
    ----------
    m_flow : float
        The mass flow of material in kilograms per second [kg/s]
    bulk_density : float
        The bulk density of the material in kilograms per cubic meter [kg/m³]

    Returns
    -------
    float
        The calculated volume flow in cubic meters per second [m³/s]

    Raises
    ------
    ValueError
        If bulk_density is zero or negative

    Notes
    -----
    The calculation follows the rearranged formula:

    .. math::

        Q = \frac{m}{\rho}

    Where:
    - Q is the volume flow [m³/s]
    - m is the mass flow [kg/s]
    - ρ is the bulk density [kg/m³]

    This function is the inverse of `_mass_flow_from_volume_flow_density`.
    To validate: volume_flow = _volume_flow_from_mass_flow_density(_mass_flow_from_volume_flow_density(volume_flow, density), density)
    """
    if bulk_density <= 0:
        raise ValueError("Bulk density must be positive (> 0).")
    volume_flow = m_flow / bulk_density
    return volume_flow


def _bulk_density_from_mass_flow_volume_flow(
    m_flow: float, volume_flow: float
) -> float:
    """
    Calculate the bulk density of material from mass flow and volume flow.

    This function is the inverse of `_mass_flow_from_volume_flow_density`.
    It calculates the bulk density by dividing the mass flow by the volume flow.

    Parameters
    ----------
    m_flow : float
        The mass flow of material in kilograms per second [kg/s]
    volume_flow : float
        The volume flow of material in cubic meters per second [m³/s]

    Returns
    -------
    float
        The calculated bulk density in kilograms per cubic meter [kg/m³]

    Raises
    ------
    ValueError
        If volume_flow is zero or negative

    Notes
    -----
    The calculation follows the rearranged formula:

    .. math::

        \rho = \frac{m}{Q}

    Where:
    - ρ is the bulk density [kg/m³]
    - m is the mass flow [kg/s]
    - Q is the volume flow [m³/s]

    This function is the inverse of `_mass_flow_from_volume_flow_density`.
    To validate: density = _bulk_density_from_mass_flow_volume_flow(_mass_flow_from_volume_flow_density(volume_flow, density), volume_flow)
    """
    if volume_flow <= 0:
        raise ValueError("Volume flow must be positive (> 0).")
    bulk_density = m_flow / volume_flow
    return bulk_density


def _mass_flow_from_cross_section_speed_density(
    cross_section_of_fill: float, belt_speed: float, bulk_density: float
) -> float:
    """
    Calculate the mass flow of material on the conveyor belt.

    This function calculates the mass flow based on the cross-sectional area of the fill, the belt speed, and the bulk density of the material.

    Parameters:
    cross_section_of_fill (float): The cross-sectional area of the fill in square meters.
    belt_speed (float): The speed of the conveyor belt in meters per second.
    bulk_density (float): The bulk density of the material in kilograms per cubic meter.

    Returns:
    float: The calculated mass flow in kilograms per second.
    """
    volume_flow = _volume_flow_from_cross_section_speed(
        cross_section_of_fill, belt_speed
    )
    m_flow = _mass_flow_from_volume_flow_density(volume_flow, bulk_density)
    return m_flow


def _cross_section_from_volume_flow_speed(
    volume_flow: float, belt_speed: float
) -> float:
    """
    Calculate the cross-sectional area of the belt fill.

    This function calculates the cross-sectional area based on the volume flow and the belt speed.

    Parameters:
    volume_flow (float): The volume flow of material in cubic meters per second.
    belt_speed (float): The speed of the conveyor belt in meters per second.

    Returns:
    float: The calculated cross-sectional area of the fill in square meters.
    """
    if belt_speed <= 0:
        raise ValueError("Belt speed must be positive (> 0).")
    cross_section = volume_flow / belt_speed
    return cross_section


def _cross_section_from_mass_flow_speed_density(
    mass_flow: float, belt_speed: float, bulk_density: float
) -> float:
    """
    Calculate the cross-sectional area of the belt fill.

    This function calculates the cross-sectional area based on the mass flow, the belt speed, and the bulk density of the material.

    Parameters:
    mass_flow (float): The mass flow of material in kilograms per second.
    belt_speed (float): The speed of the conveyor belt in meters per second.
    bulk_density (float): The bulk density of the material in kilograms per cubic meter.

    Returns:
    float: The calculated cross-sectional area of the fill in square meters.

    Raises:
        ValueError: If belt_speed is zero or negative, or if bulk_density is zero or negative.
    """
    if bulk_density <= 0:
        raise ValueError("Bulk density must be positive (> 0).")
    cross_section = _cross_section_from_volume_flow_speed(
        mass_flow / bulk_density, belt_speed
    )
    return cross_section


def _nominal_volume_flow(
    theoretical_volume_flow: float, effective_filling_ratio: float
) -> float:
    """
    Calculate the nominal volume flow of material on the conveyor belt.

    This function calculates the nominal volume flow based on the volume flow and the effective filling ratio.

    Parameters:
    volume_flow (float): The volume flow of material in cubic meters per second.
    effective_filling_ratio (float): The effective filling ratio of the belt.

    Returns:
    float: The calculated nominal volume flow in cubic meters per second.
    """
    nominal_v_flow = theoretical_volume_flow * effective_filling_ratio
    return nominal_v_flow


def _nominal_mass_flow(
    theoretical_volume_flow: float, effective_filling_ratio: float, bulk_density: float
) -> float:
    """
    Calculate the theoretical mass flow of material on the conveyor belt.

    This function calculates the theoretical mass flow based on the volume flow, the effective filling ratio, and the bulk density of the material.

    Parameters:
    theoretical_volume_flow (float): The volume flow of material in cubic meters per second.
    effective_filling_ratio (float): The effective filling ratio of the belt.
    bulk_density (float): The bulk density of the material in kilograms per cubic meter.

    Returns:
    float: The calculated theoretical mass flow in kilograms per second.
    """
    theoretical_m_flow = (
        theoretical_volume_flow * effective_filling_ratio * bulk_density
    )
    return theoretical_m_flow


def _line_load_from_nominal_load(
    theoretical_cross_section: float,
    effective_filling_ratio: float,
    bulk_density: float,
) -> float:
    """
    Calculate the line load of material on the conveyor belt.

    This function calculates the line load based on the theoretical cross-sectional area, the effective filling ratio, and the bulk density of the material.

    Parameters:
    theoretical_cross_section (float): The cross-sectional area of the fill in square meters.
    effective_filling_ratio (float): The effective filling ratio of the belt.
    bulk_density (float): The bulk density of the material in kilograms per cubic meter.

    Returns:
    float: The calculated line load in kilograms per meter.
    """
    line_load = theoretical_cross_section * effective_filling_ratio * bulk_density
    return line_load


def _line_load_from_nominal_mass_flow_speed(
    nominal_mass_flow: float, belt_speed: float
) -> float:
    """
    Calculate the line load of material on the conveyor belt.

    This function calculates the line load based on the theoretical mass flow and the belt speed.

    Parameters:
    theoretical_mass_flow (float): The theoretical mass flow of material in kilograms per second.
    belt_speed (float): The speed of the conveyor belt in meters per second.

    Returns:
    float: The calculated line load in kilograms per meter.

    Raises:
    ValueError: If belt_speed is zero or negative.
    """
    if belt_speed <= 0:
        raise ValueError("Belt speed must be positive (> 0).")
    return nominal_mass_flow / belt_speed


def _solve_for_used_belt_width_from_cross_section(
    target_cross_section_area: float,
    center_roll_length: float,
    troughing_angle: float,
    equivalent_slope_angle: float,
    initial_guess: Optional[float] = None,
    tol: float = 1e-6,
    max_iterations: float = 100,
) -> float:
    """
    Calculates the used belt width required to achieve a specified cross-sectional area of material on a conveyor belt, using the Newton-Raphson root-finding method.
    Parameters
    ----------
    target_cross_section_area : float
        The desired cross-sectional area of material on the belt (in m²).
    center_roll_length : float
        The length of the center roll of the conveyor (in meters).
    troughing_angle : float
        The troughing angle of the conveyor belt (in degrees).
    equivalent_slope_angle : float
        The equivalent slope angle of the conveyor belt (in degrees).
    initial_guess : float, optional
        An initial guess for the usable belt width (in meters). If None, defaults to half of the center roll length.
    tol : float, optional
        The tolerance for the root-finding convergence. Default is 1e-6.
    max_iterations : int, optional
        The maximum number of iterations for the root-finding algorithm. Default is 100.
    Returns
    -------
    float
        The calculated usable belt width (in meters) that achieves the target cross-sectional area.
    Raises
    ------
    ValueError
        If the root-finding algorithm fails to converge to a solution.
    """
    from scipy import optimize

    # Special case: if target area is zero, return zero width
    if target_cross_section_area == 0.0:
        return 0.0

    # Default initial guess if not provided
    if initial_guess is None:
        initial_guess = center_roll_length / 2

    # Define objective function
    def objective_function(b):
        # b is usable belt width
        calculated_area = _cross_section_of_fill(
            center_roll_length,
            b[0],
            troughing_angle,
            equivalent_slope_angle,
        )
        return calculated_area - target_cross_section_area

    # Solve using SciPy's root finding
    result = optimize.root(
        objective_function,
        [initial_guess],
        method="hybr",
        tol=tol,
        options={"maxfev": max_iterations},
    )

    if not result.success:
        raise ValueError(f"Failed to converge: {result.message}")

    return result.x[0]  # Return the solution


def _belt_edge_distance(belt_width: float, used_belt_width: float) -> float:
    """
    Calculates the distance between the edge of the belt and the used belt width on each side.
    This function assumes that the belt is symmetric, so the distance is the same on both sides.

    Args:
        belt_width (float): The total width of the belt.
        used_belt_width (float): The width of the belt that is actually used or the usable belt width as described in DIN 22101.
    Returns:
        float: The distance from the edge of the belt to the used belt width on one side.
    """

    return 0.5 * (belt_width - used_belt_width)


def _length_of_material_on_side_roll(
    part_of_belt_lying_on_side_idler: float, belt_edge_distance: float
) -> float:
    """
    Calculates the length of material on the side roll of a conveyor belt.
    Args:
        part_of_belt_lying_on_side_idler (float): The length of the belt segment that lies on the side idler (in meters).
        belt_edge_distance (float): The distance from the edge of the belt to the point where the material ends (in meters).
    Returns:
        float: The effective length of material on the side roll (in meters).
    """
    return part_of_belt_lying_on_side_idler - belt_edge_distance


def _effective_filling_ratio(
    filling_ratio_operations: float, reduction_factor_inclined_fill: float
) -> float:
    """
    Calculate the effective filling ratio of a conveyor belt by multiplying the
    operational filling ratio by the reduction factor for inclined fill.

    This is an internal function that performs the core calculation for the effective filling ratio.
    The public interface for this function is available via `effective_filling_ratio`.

    Parameters:
    filling_ratio_operations (float): The filling ratio under operational conditions,
        a dimensionless value typically between 0 and 1.
    reduction_factor_inclined_fill (float): The reduction factor for inclined fill,
        a dimensionless value that accounts for material distribution on inclined belts.

    Returns:
    float: The effective filling ratio of the conveyor belt.
    """
    return filling_ratio_operations * reduction_factor_inclined_fill


def _reduction_factor_inclined_fill(
    theoretical_partial_cross_section_above_water_fill: float,
    theoretical_cross_section_of_fill: float,
    reduction_factor_inclined_fill_1: float,
) -> float:
    """
    Calculate the reduction factor for inclined fill on a conveyor belt.

    This function calculates a reduction factor used to adjust the cross-sectional area
    of material on an inclined conveyor belt. It accounts for the proportion of material
    above the water fill line and applies a reduction factor based on the inclination.

    Args:
        theoretical_partial_cross_section_above_water_fill (float): The theoretical partial
            cross-section above water fill in square millimeters.
        theoretical_cross_section_of_fill (float): The theoretical total cross-section of
            fill in square millimeters.
        reduction_factor_inclined_fill_1 (float): The first reduction factor for inclined fill,
            a dimensionless value between 0 and 1.

    Returns:
        float: The calculated reduction factor, a dimensionless value between 0 and 1.

    Raises:
        ValueError: If theoretical_cross_section_of_fill is zero.
    """
    if theoretical_cross_section_of_fill == 0:
        raise ValueError("Theoretical cross-section of fill cannot be zero.")
    return (
        1
        - theoretical_partial_cross_section_above_water_fill
        / theoretical_cross_section_of_fill
        * (1 - reduction_factor_inclined_fill_1)
    )


def _reduction_factor_inclined_fill_1(
    maximal_inclination_angle: float, dynamic_angle_of_slope: float
) -> float:
    """
    Calculates the reduction factor for inclined fill based on the maximal inclination angle and the dynamic angle of slope.
    This function computes a reduction factor used in material handling or bulk solids transport, where the inclination of the fill affects the flow characteristics. The calculation is based on the cosine squared of the provided angles.
    Args:
        maximal_inclination_angle (float): The maximal inclination angle of the fill (in degrees).
        dynamic_angle_of_slope (float): The dynamic angle of slope (in degrees).
    Returns:
        float: The calculated reduction factor.
    Raises:
        ValueError: If the maximal inclination angle is greater than the dynamic angle of slope.
    """
    if abs(maximal_inclination_angle) > dynamic_angle_of_slope:
        raise ValueError(
            "The maximal inclination angle must not be greater than the dynamic angle of slope."
        )

    cos2dmax = math.cos(math.radians(maximal_inclination_angle)) ** 2
    cos2bdyn = math.cos(math.radians(dynamic_angle_of_slope)) ** 2

    if cos2dmax == 1:
        raise ValueError("Maximal inclination angle cannot be zero degrees.")

    fraction = (cos2dmax - cos2bdyn) / (1 - cos2dmax)
    sqrt = math.sqrt(fraction)

    return sqrt


def _effective_filling_ratio_from_areas(
    theoretical_cross_section_of_fill: float, actual_cross_section: float
) -> float:
    """
    Calculate the effective filling ratio based on the areas of the cross-section.

    This function computes the effective filling ratio by dividing the actual cross-section
    by the theoretical cross-section. It is used in material handling or bulk solids transport
    to determine how full the conveyor belt is compared to its theoretical capacity.

    Parameters:
        theoretical_cross_section_of_fill (float): The theoretical maximum cross-sectional
            area of the fill (in square meters).
        actual_cross_section (float): The actual cross-sectional area of the fill
            (in square meters).

    Returns:
        float: The effective filling ratio, a dimensionless value typically between 0 and 1.

    Raises:
        ValueError: If theoretical_cross_section_of_fill is zero.
    """
    if theoretical_cross_section_of_fill == 0:
        raise ValueError("Theoretical cross-section of fill cannot be zero.")
    return actual_cross_section / theoretical_cross_section_of_fill


if __name__ == "__main__":
    print(_cross_section_of_fill(750, 1750, 30, 0))
    print(_usable_belt_width(2000))
    print(_usable_belt_width(1200))
