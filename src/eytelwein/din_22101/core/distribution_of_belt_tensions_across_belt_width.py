from pint.registry import Quantity
from eytelwein.din_22101.constants import CoefficientMinimumTransitionLength

from eytelwein.din_22101.core._distribution_of_belt_tensions_across_belt_width import (
    _compensation_length_at_transition_zone,
    _difference_edge_and_center_belt_tensions_steel_cord_belts,
    _difference_edge_and_center_belt_tensions_textile_belts,
    _distance_belt_edge_to_pulley_surface_level,
    _length_of_belt_edge_in_transition_zone,
    _local_center_belt_force,
    _local_edge_belt_force,
    _maximal_allowable_pulley_lift,
    _mean_belt_tension_related_to_belt_width,
    _local_belt_force_related_to_belt_width,
    _minimal_transition_length,
    _part_of_belt_lying_on_side_idler,
    _reference_length_of_transition_zone_for_steel_cord_belts,
)

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def mean_belt_tension_related_to_belt_width(
    local_belt_force: Quantity,
    belt_width: Quantity,
    unit: str = "newton / millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the mean belt tension related to the belt width.

    Parameters
    ----------
    local_belt_force : Quantity
        The local belt force value with units.
    belt_width : Quantity
        The width of the belt with units.
    unit : str, optional
        The unit for the output mean belt tension (default is "newton / millimeter").
    precision : int, optional
        The precision for rounding the result (default is 2).

    Returns
    -------
    Quantity
        The mean belt tension related to the belt width in the specified unit.

    Raises
    ------
    ValueError
        If there is an error in converting local belt force or if the unit is invalid.
    """
    try:
        local_belt_force_kN = local_belt_force.to("kilonewton")
        belt_width_mm = belt_width.to("millimeter")
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    # Validate physical meaningfulness after unit conversion
    if belt_width_mm.magnitude <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    belt_tension = (
        _mean_belt_tension_related_to_belt_width(
            local_belt_force_kN.magnitude, belt_width_mm.magnitude
        )
    ) * (u.kilonewton / u.millimeter)  # First convert to the requested output unit
    belt_tension = belt_tension.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        belt_tension = round(belt_tension, precision)

    return belt_tension


def local_belt_force_related_to_belt_width(
    mean_belt_tension: Quantity,
    belt_width: Quantity,
    unit: str = "kilonewton",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the local belt force related to the belt width.

    Parameters
    ----------
    mean_belt_tension : Quantity
        The mean belt tension value with units.
    belt_width : Quantity
        The width of the belt with units.
    unit : str, optional
        The unit for the output local belt force (default is "kilonewton").
    precision : int, optional
        The precision for rounding the result (default is 2).

    Returns
    -------
    Quantity
        The local belt force related to the belt width in the specified unit.

    Raises
    ------
    ValueError
        If there is an error in converting values or if the unit is invalid.
    """
    try:
        mean_belt_tension_Npmm = mean_belt_tension.to("newton / millimeter")
        belt_width_mm = belt_width.to("millimeter")
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    belt_force = (
        _local_belt_force_related_to_belt_width(
            mean_belt_tension_Npmm.magnitude, belt_width_mm.magnitude
        )
    ) * (u.newton)  # First convert to the requested output unit
    belt_force = belt_force.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        belt_force = round(belt_force, precision)

    return belt_force


def local_center_belt_force(
    mean_belt_tension_related_to_belt_width: Quantity,
    part_of_belt_lying_on_side_idler: Quantity,
    belt_width: Quantity,
    difference_edge_and_center_belt_tensions: Quantity,
    unit: str = "newton / millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the center belt force based on various parameters.
    This function computes the center belt force using the mean belt tension
    related to the belt width, the portion of the belt lying on the side idler,
    the belt width, and the difference between edge and center belt tensions.
    The result is returned in the specified unit with optional precision.
    Parameters:
        mean_belt_tension_related_to_belt_width (Quantity):
            The mean belt tension per unit width of the belt, expressed as a
            Pint Quantity.
        part_of_belt_lying_on_side_idler (Quantity):
            The portion of the belt lying on the side idler, expressed as a
            Pint Quantity.
        belt_width (Quantity):
            The total width of the belt, expressed as a Pint Quantity.
        difference_edge_and_center_belt_tensions (Quantity):
            The difference between the edge and center belt tensions, expressed
            as a Pint Quantity.
        unit (str, optional):
            The desired unit for the output force. Defaults to "kilonewton".
        precision (int, optional):
            The number of decimal places to round the result to. If None, no
            rounding is applied. Defaults to 2.
    Returns:
        Quantity:
            The calculated center belt force as a Pint Quantity in the specified
            unit.
    Raises:
        ValueError:
            If there is an error in converting input values to the required units
            or if the specified unit is invalid.
    """
    try:
        mean_belt_tension_related_to_belt_width_Npmm = (
            mean_belt_tension_related_to_belt_width.to("newton / millimeter")
        )
        belt_width_m = belt_width.to("meter")
        part_of_belt_lying_on_side_idler_m = part_of_belt_lying_on_side_idler.to(
            "meter"
        )
        difference_edge_and_center_belt_tensions_Npmm = (
            difference_edge_and_center_belt_tensions.to("newton / millimeter")
        )
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    # Validate physical meaningfulness after unit conversion
    if belt_width_m.magnitude <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")

    if part_of_belt_lying_on_side_idler_m.magnitude < 0:
        raise ValueError(
            f"part_of_belt_lying_on_side_idler must be non-negative, got {part_of_belt_lying_on_side_idler}"
        )

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    try:
        center_belt_force = (
            _local_center_belt_force(
                mean_belt_tension_related_to_belt_width_Npmm.magnitude,
                part_of_belt_lying_on_side_idler_m.magnitude,
                belt_width_m.magnitude,
                difference_edge_and_center_belt_tensions_Npmm.magnitude,
            )
        ) * (u.newton / u.millimeter)
    except ValueError as e:
        raise ValueError(
            f"Calculation error: {e}. Check the input values for physical validity."
        ) from e  # First convert to the requested output unit
    center_belt_force = center_belt_force.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        center_belt_force = round(center_belt_force, precision)

    return center_belt_force


def part_of_belt_lying_on_side_idler(
    belt_width: Quantity,
    length_center_roller: Quantity,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the part of the belt lying on the side idler based on the belt width
    and the length of the center roller.

    For flat trough configurations where the center roller length equals or exceeds
    the belt width, returns 0 as there are no side idlers.

    Args:
        belt_width (Quantity): The width of the belt as a Pint Quantity.
        length_center_roller (Quantity): The length of the center roller as a Pint Quantity.
        unit (str, optional): The desired unit for the result. Defaults to "millimeter".
        precision (int, optional): The number of decimal places to round the result to.
                                   If None, no rounding is applied. Defaults to 2.
    Returns:
        Quantity: The calculated part of the belt lying on the side idler in the specified unit.
                  Returns 0 for flat trough configurations (length_center_roller >= belt_width).
    Raises:
        ValueError: If there is an error in converting the input values to meters.
        ValueError: If belt_width is zero or negative.
        ValueError: If length_center_roller is negative.
        ValueError: If the specified unit is invalid.
    """
    try:
        belt_width_m = belt_width.to("meter")
        length_center_roller_m = length_center_roller.to("meter")
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    # Validate physical meaningfulness after unit conversion
    if belt_width_m.magnitude <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")

    if length_center_roller_m.magnitude < 0:
        raise ValueError(
            f"length_center_roller must be non-negative, got {length_center_roller}"
        )

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Handle flat trough configuration (application logic)
    if length_center_roller_m.magnitude >= belt_width_m.magnitude:
        # Flat trough: center roller covers entire belt width or more, no side idlers
        result = 0.0 * u.meter
    else:
        # Three-trough or V-trough: calculate side idler portion
        result = (
            _part_of_belt_lying_on_side_idler(
                belt_width_m.magnitude,
                length_center_roller_m.magnitude,
            )
            * u.meter
        )

    # Convert to the desired unit
    result = result.to(pint_unit)

    if precision is not None:
        result = round(result, precision)

    return result


def local_edge_belt_force(
    local_center_belt_force: Quantity,
    difference_edge_and_center_belt_tensions: Quantity,
    unit: str = "newton / millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the local edge belt force based on the local center belt force
    and the difference between edge and center belt tensions.
    Args:
        local_center_belt_force (Quantity): The local center belt force,
            expected to be a Pint Quantity with units convertible to "newton / millimeter".
        difference_edge_and_center_belt_tensions (Quantity): The difference between
            edge and center belt tensions, expected to be a Pint Quantity with units
            convertible to "newton / millimeter".
        unit (str, optional): The desired output unit for the result. Defaults to "newton / millimeter".
        precision (int, optional): The number of decimal places to round the result to.
            If None, no rounding is applied. Defaults to 2.
    Returns:
        Quantity: The calculated local edge belt force as a Pint Quantity in the specified unit.
    Raises:
        ValueError: If the input quantities cannot be converted to "newton / millimeter".
        ValueError: If the specified unit is invalid.
    """
    try:
        local_center_belt_force_Npmm = local_center_belt_force.to("newton / millimeter")
        difference_edge_and_center_belt_tensions_Npmm = (
            difference_edge_and_center_belt_tensions.to("newton / millimeter")
        )
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    result = (
        _local_edge_belt_force(
            local_center_belt_force_Npmm.magnitude,
            difference_edge_and_center_belt_tensions_Npmm.magnitude,
        )
    ) * (u.newton / u.millimeter)
    result = result.to(pint_unit)

    if precision is not None:
        result = round(result, precision)

    return result


def minimal_transition_length(
    coefficient_minimum_transition_length: CoefficientMinimumTransitionLength,
    distance_belt_edge_pulley_surface_level: Quantity,
    unit: str = "meter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the minimal transition length for a belt system.
    This function computes the minimal transition length required for a belt
    system based on the coefficient of minimum transition length and the
    distance between the belt edge and the pulley surface level.
    Args:
        coefficient_minimum_transition_length (CoefficientMinimumTransitionLength):
            The coefficient used to calculate the minimal transition length.
        distance_belt_edge_pulley_surface_level (Quantity):
            The distance between the belt edge and the pulley surface level,
            provided as a Pint Quantity.
        unit (str, optional):
            The desired unit for the result. Defaults to "meter".
        precision (int, optional):
            The number of decimal places to round the result to. If None, no
            rounding is applied. Defaults to 2.
    Returns:
        Quantity:
            The minimal transition length as a Pint Quantity in the specified unit.
    Raises:
        ValueError:
            If the input distance cannot be converted to meters or if the
            specified unit is invalid.
    """
    try:
        distance_belt_edge_pulley_surface_level_m = (
            distance_belt_edge_pulley_surface_level.to("meter")
        )
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    result = (
        _minimal_transition_length(
            coefficient_minimum_transition_length.value,
            distance_belt_edge_pulley_surface_level_m.magnitude,
        )
    ) * (u.meter)
    result = result.to(pint_unit)

    if precision is not None:
        result = round(result, precision)

    return result


def distance_belt_edge_to_pulley_surface_level(
    distance_belt_edge_to_deepest_level_of_trough: Quantity,
    pulley_lift: Quantity,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculates the distance from the belt edge to the pulley surface level.
    This function computes the distance from the edge of a belt to the surface
    level of a pulley, taking into account the distance to the deepest level
    of the trough and the pulley lift. The result is returned in the specified
    unit with the desired precision.
    Args:
        distance_belt_edge_to_deepest_level_of_trough (Quantity):
            The distance from the belt edge to the deepest level of the trough,
            expressed as a Pint Quantity.
        pulley_lift (Quantity):
            The lift of the pulley, expressed as a Pint Quantity.
        unit (str, optional):
            The unit in which the result should be returned. Defaults to "millimeter".
        precision (int, optional):
            The number of decimal places to round the result to. If None, no rounding
            is applied. Defaults to 2.
    Returns:
        Quantity:
            The calculated distance from the belt edge to the pulley surface level,
            expressed as a Pint Quantity in the specified unit.
    Raises:
        ValueError:
            If there is an error in converting the input values to the desired unit
            or if the specified unit is invalid.
    """
    try:
        distance_belt_edge_to_deepest_level_of_trough_mm = (
            distance_belt_edge_to_deepest_level_of_trough.to("millimeter")
        )
        pulley_lift_mm = pulley_lift.to("millimeter")
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    result = (
        _distance_belt_edge_to_pulley_surface_level(
            distance_belt_edge_to_deepest_level_of_trough_mm.magnitude,
            pulley_lift_mm.magnitude,
        )
    ) * (u.millimeter)
    result = result.to(pint_unit)

    if precision is not None:
        result = round(result, precision)

    return result


def reference_length_of_transition_zone_for_steel_cord_belts(
    minimal_transition_length: Quantity,
    compensation_length: Quantity,
    unit: str = "meter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the reference length of the transition zone for steel cord belts.
    This function computes the reference length of the transition zone based on
    the minimal transition length and the compensation length. The result is
    returned in the specified unit with an optional precision.
    Args:
        minimal_transition_length (Quantity): The minimal transition length,
            provided as a Pint Quantity object.
        compensation_length (Quantity): The compensation length, provided as
            a Pint Quantity object.
        unit (str, optional): The unit in which the result should be returned.
            Defaults to "meter".
        precision (int, optional): The number of decimal places to round the
            result to. If None, no rounding is applied. Defaults to 2.
    Returns:
        Quantity: The reference length of the transition zone as a Pint
        Quantity object in the specified unit.
    Raises:
        ValueError: If the input values cannot be converted to meters or if
            the specified unit is invalid.
    """
    try:
        minimal_transition_length_m = minimal_transition_length.to("meter")
        compensation_length_m = compensation_length.to("meter")
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    result = (
        _reference_length_of_transition_zone_for_steel_cord_belts(
            minimal_transition_length_m.magnitude,
            compensation_length_m.magnitude,
        )
    ) * (u.meter)

    result = result.to(pint_unit)

    if precision is not None:
        result = round(result, precision)

    return result


def compensation_length_at_transition_zone(
    distance_belt_edge_to_deepest_level_of_trough: Quantity,
    pulley_lift: Quantity,
    maximal_allowed_pulley_lift: Quantity,
    unit: str = "meter",
    precision: int = 2,
) -> Quantity:
    """
    Calculates the compensation length at the transition zone of a conveyor belt.
    This function computes the compensation length based on the distance from the
    belt edge to the deepest level of the trough, the pulley lift, and the maximal
    allowed pulley lift. The result is returned in the specified unit with an
    optional precision.
    Parameters:
        distance_belt_edge_to_deepest_level_of_trough (Quantity):
            The distance from the belt edge to the deepest level of the trough.
        pulley_lift (Quantity):
            The lift of the pulley.
        maximal_allowed_pulley_lift (Quantity):
            The maximum allowed lift of the pulley.
        unit (str, optional):
            The unit in which the result should be returned. Defaults to "meter".
        precision (int, optional):
            The number of decimal places to round the result to. Defaults to 2.
    Returns:
        Quantity: The compensation length at the transition zone in the specified unit.
    Raises:
        ValueError: If there is an error in converting input values or if the unit is invalid.
    """
    try:
        distance_belt_edge_to_deepest_level_of_trough_mm = (
            distance_belt_edge_to_deepest_level_of_trough.to("millimeter")
        )
        pulley_lift_mm = pulley_lift.to("millimeter")
        maximal_allowed_pulley_lift_mm = maximal_allowed_pulley_lift.to("millimeter")
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    result = (
        _compensation_length_at_transition_zone(
            distance_belt_edge_to_deepest_level_of_trough_mm.magnitude,
            pulley_lift_mm.magnitude,
            maximal_allowed_pulley_lift_mm.magnitude,
        )
    ) * (u.millimeter)

    result = result.to(pint_unit)

    if precision is not None:
        result = round(result, precision)

    return result


def length_of_belt_edge_in_transition_zone(
    minimal_transition_length: Quantity,
    pulley_lift: Quantity,
    part_of_belt_lying_on_side_idler: Quantity,
    troughing_angle: Quantity,
    unit: str = "meter",
    precision: int = 6,
) -> Quantity:
    """
    Calculate the length of the belt edge in the transition zone.
    This function computes the length of the belt edge in the transition zone
    based on the minimal transition length, pulley lift, part of the belt lying
    on the side idler, and the troughing angle. The result can be returned in
    a specified unit with a given precision.
    Parameters:
        minimal_transition_length (Quantity): The minimal transition length,
            provided as a Pint Quantity.
        pulley_lift (Quantity): The vertical lift of the pulley, provided as
            a Pint Quantity.
        part_of_belt_lying_on_side_idler (Quantity): The portion of the belt
            lying on the side idler, provided as a Pint Quantity.
        troughing_angle (Quantity): The troughing angle, provided as a Pint
            Quantity.
        unit (str, optional): The desired unit for the result. Defaults to "meter".
        precision (int, optional): The number of decimal places to round the
            result to. If None, no rounding is applied. Defaults to 2.
    Returns:
        Quantity: The length of the belt edge in the transition zone, as a Pint
        Quantity in the specified unit.
    Raises:
        ValueError: If there is an error in converting input values to the
            required units or if the specified unit is invalid.
    """
    try:
        minimal_transition_length_m = minimal_transition_length.to("meter")
        pulley_lift_m = pulley_lift.to("meter")
        part_of_belt_lying_on_side_idler_m = part_of_belt_lying_on_side_idler.to(
            "meter"
        )
        troughing_angle_rad = troughing_angle.to("radian")
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    result = (
        _length_of_belt_edge_in_transition_zone(
            minimal_transition_length_m.magnitude,
            pulley_lift_m.magnitude,
            part_of_belt_lying_on_side_idler_m.magnitude,
            troughing_angle_rad.magnitude,
        )
    ) * (u.meter)

    result = result.to(pint_unit)

    if precision is not None:
        result = round(result, precision)

    return result


def difference_edge_and_center_belt_tensions_steel_cord_belts(
    length_of_belt_edge_in_transition_zone: Quantity,
    minimal_transition_length: Quantity,
    reference_length_of_transition_zone_for_steel_cord_belts: Quantity,
    elastic_modulus: Quantity,
    unit: str = "newton / millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the difference between edge and center belt tensions for steel cord belts.
    This function computes the difference in tensions between the edge and center of a steel cord belt
    based on the provided parameters. The calculation considers the length of the belt edge in the
    transition zone, the minimal transition length, a reference length for steel cord belts, and the
    elastic modulus of the belt material.
    Parameters:
        length_of_belt_edge_in_transition_zone (Quantity): The length of the belt edge in the transition zone,
            specified as a Pint Quantity.
        minimal_transition_length (Quantity): The minimal transition length, specified as a Pint Quantity.
        reference_length_of_transition_zone_for_steel_cord_belts (Quantity): The reference length of the
            transition zone for steel cord belts, specified as a Pint Quantity.
        elastic_modulus (Quantity): The elastic modulus of the belt material, specified as a Pint Quantity.
        unit (str, optional): The desired output unit for the result. Defaults to "newton / milimeter".
        precision (int, optional): The number of decimal places to round the result to. Defaults to 6.
    Returns:
        Quantity: The difference between edge and center belt tensions, expressed as a Pint Quantity
        in the specified unit.
    Raises:
        ValueError: If there is an error in converting input values to the required units or if the
        specified unit is invalid.
    Notes:
        - The function internally uses a helper function `_difference_edge_and_center_belt_tensions_steel_cord_belts`
          to perform the core calculation.
        - The input quantities must be compatible with the expected units for proper conversion and calculation.
    """
    try:
        length_of_belt_edge_in_transition_zone_m = (
            length_of_belt_edge_in_transition_zone.to("meter")
        )
        minimal_transition_length_m = minimal_transition_length.to("meter")
        reference_length_of_transition_zone_for_steel_cord_belts_m = (
            reference_length_of_transition_zone_for_steel_cord_belts.to("meter")
        )
        elastic_modulus_Npmm = elastic_modulus.to("newton / millimeter")
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    result = (
        _difference_edge_and_center_belt_tensions_steel_cord_belts(
            length_of_belt_edge_in_transition_zone_m.magnitude,
            minimal_transition_length_m.magnitude,
            reference_length_of_transition_zone_for_steel_cord_belts_m.magnitude,
            elastic_modulus_Npmm.magnitude,
        )
    ) * (u.newton / u.millimeter)

    result = result.to(pint_unit)

    if precision is not None:
        result = round(result, precision)

    return result


def difference_edge_and_center_belt_tensions_textile_belts(
    length_of_belt_edge_in_transition_zone: Quantity,
    minimal_transition_length: Quantity,
    elastic_modulus: Quantity,
    unit: str = "newton / millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the difference between edge and center belt tensions for steel cord belts.
    This function computes the difference in tensions between the edge and center of a steel cord belt
    based on the provided parameters. The calculation considers the length of the belt edge in the
    transition zone, the minimal transition length, a reference length for steel cord belts, and the
    elastic modulus of the belt material.
    Parameters:
        length_of_belt_edge_in_transition_zone (Quantity): The length of the belt edge in the transition zone,
            specified as a Pint Quantity.
        minimal_transition_length (Quantity): The minimal transition length, specified as a Pint Quantity.
        elastic_modulus (Quantity): The elastic modulus of the belt material, specified as a Pint Quantity.
        unit (str, optional): The desired output unit for the result. Defaults to "newton / milimeter".
        precision (int, optional): The number of decimal places to round the result to. Defaults to 6.
    Returns:
        Quantity: The difference between edge and center belt tensions, expressed as a Pint Quantity
        in the specified unit.
    Raises:
        ValueError: If there is an error in converting input values to the required units or if the
        specified unit is invalid.
    Notes:
        - The function internally uses a helper function `_difference_edge_and_center_belt_tensions_steel_cord_belts`
          to perform the core calculation.
        - The input quantities must be compatible with the expected units for proper conversion and calculation.
    """
    try:
        length_of_belt_edge_in_transition_zone_m = (
            length_of_belt_edge_in_transition_zone.to("meter")
        )
        minimal_transition_length_m = minimal_transition_length.to("meter")
        elastic_modulus_Npmm = elastic_modulus.to("newton / millimeter")
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    result = (
        _difference_edge_and_center_belt_tensions_textile_belts(
            length_of_belt_edge_in_transition_zone_m.magnitude,
            minimal_transition_length_m.magnitude,
            elastic_modulus_Npmm.magnitude,
        )
    ) * (u.newton / u.millimeter)

    result = result.to(pint_unit)

    if precision is not None:
        result = round(result, precision)

    return result


def maximal_allowable_pulley_lift(
    distance_from_edge_to_deepest_trough_level: Quantity,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the maximal allowable pulley lift based on the distance from the edge
    to the deepest trough level.
    Parameters:
        distance_from_edge_to_deepest_trough_level (Quantity):
            The distance from the edge to the deepest trough level, provided as a
            Pint Quantity object.
        unit (str, optional):
            The desired output unit for the result. Defaults to "millimeter".
        precision (int, optional):
            The number of decimal places to round the result to. If None, no rounding
            is applied. Defaults to 2.
    Returns:
        Quantity: The maximal allowable pulley lift as a Pint Quantity object,
        converted to the specified unit.
    Raises:
        ValueError: If the input distance cannot be converted to meters or if the
        specified unit is invalid.
    """
    try:
        distance_from_edge_to_deepest_trough_level_m = (
            distance_from_edge_to_deepest_trough_level.to("meter")
        )
    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    result = (
        _maximal_allowable_pulley_lift(
            distance_from_edge_to_deepest_trough_level_m.magnitude
        )
    ) * (u.meter)

    result = result.to(pint_unit)

    if precision is not None:
        result = round(result, precision)

    return result
