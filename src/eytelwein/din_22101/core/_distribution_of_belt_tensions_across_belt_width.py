import math


def _mean_belt_tension_related_to_belt_width(
    local_belt_force: float, belt_width: float
) -> float:
    """
    Calculate the mean belt tension related to the belt width.

    Parameters
    ----------
    local_belt_tension : float
        The local belt tension value.
    belt_width : float
        The width of the belt.

    Returns
    -------
    float
        The mean belt tension related to the belt width.

    Raises
    ------
    ValueError
        If belt_width is zero or negative.
    """
    if belt_width <= 0:
        raise ValueError("belt_width must be positive")
    belt_tension = local_belt_force / belt_width
    return belt_tension


def _local_belt_force_related_to_belt_width(
    mean_belt_tension: float, belt_width: float
) -> float:
    """
    Calculate the local belt force related to the belt width.

    Parameters
    ----------
    mean_belt_tension : float
        The mean belt tension value.
    belt_width : float
        The width of the belt.

    Returns
    -------
    float
        The local belt force related to the belt width.

    """
    belt_force = mean_belt_tension * belt_width
    return belt_force


def _local_center_belt_force(
    mean_belt_tension_related_to_belt_width: float,
    part_of_belt_lying_on_side_idler: float,
    belt_width: float,
    difference_edge_and_center_belt_tensions: float,
) -> float:
    """
    Calculate the center belt tension based on the mean belt tension,
    the portion of the belt lying on the side idler, the belt width,
    and the difference between edge and center belt tensions.
    Args:
        mean_belt_tension_related_to_belt_width (float): The mean belt tension
            normalized to the belt width.
        part_of_belt_lying_on_side_idler (float): The portion of the belt
            that lies on the side idler.
        belt_width (float): The total width of the belt.
        difference_edge_and_center_belt_tensions (float): The difference
            between the edge and center belt tensions.
    Returns:
        float: The calculated center belt tension.
    Raises:
        ValueError: If belt_width is zero or negative (division safety).
        ValueError: If the calculated center belt tension is negative.
    """
    # Division safety validation
    if belt_width <= 0:
        raise ValueError(f"belt_width must be positive, got {belt_width}")

    center_belt_tension = (
        mean_belt_tension_related_to_belt_width
        - part_of_belt_lying_on_side_idler
        / belt_width
        * difference_edge_and_center_belt_tensions
    )
    # Check if the local center belt force is negative and raise error
    if center_belt_tension < 0:
        raise ValueError(
            f"The local center belt force shall not be negative. Value: {center_belt_tension}"
        )
    return center_belt_tension


def _part_of_belt_lying_on_side_idler(
    belt_width: float, length_center_roller: float
) -> float:
    """
    Calculate the part of the belt lying on the side idler.

    Simple geometric calculation: (belt_width - length_center_roller) / 2

    Args:
        belt_width (float): The total width of the belt [m].
        length_center_roller (float): The length of the center roller [m].

    Returns:
        float: The calculated part of the belt lying on one side idler [m].

    Notes:
        This is a pure mathematical calculation. Application logic (e.g., flat trough
        configuration detection) is handled in the public function.
    """
    return (belt_width - length_center_roller) / 2


def _local_edge_belt_force(
    local_center_belt_force: float, difference_edge_and_center_belt_tensions: float
) -> float:
    """
    Calculate the local edge belt force based on the local center belt
    force and the difference between edge and center belt tensions.
    Args:
        local_center_belt_force (float): The local center belt force.
        difference_edge_and_center_belt_tensions (float): The difference
            between edge and center belt tensions.
    Returns:
        float: The calculated local edge belt force.
    """
    local_edge_belt_force = (
        local_center_belt_force + difference_edge_and_center_belt_tensions
    )

    # Return the local edge belt force
    return local_edge_belt_force


def _minimal_transition_length(
    coefficient_minimum_transition_length: float,
    distance_belt_edge_pulley_surface_level: float,
) -> float:
    """
    Calculate the minimal transition length based on the coefficient and
    the distance from the belt edge to the pulley surface level.
    Args:
        coefficient_minimum_transition_length (float): The coefficient for minimum
            transition length.
        distance_belt_edge_pulley_surface_level (float): The distance from
            the belt edge to the pulley surface level.
    Returns:
        float: The calculated minimal transition length.
    """
    return (
        coefficient_minimum_transition_length * distance_belt_edge_pulley_surface_level
    )


def _distance_belt_edge_to_pulley_surface_level(
    distance_belt_edge_to_deepest_level_of_trough: float, pulley_lift: float
) -> float:
    """
    Calculate the distance from the belt edge to the pulley surface level.
    Args:
        distance_belt_edge_to_deepest_level_of_trough (float): The distance from the
            belt edge to the deepest level of the trough.
        pulley_lift (float): The lift of the pulley.
    Returns:
        float: The calculated distance from the belt edge to the pulley surface level.
    """
    return distance_belt_edge_to_deepest_level_of_trough - pulley_lift


def _reference_length_of_transition_zone_for_steel_cord_belts(
    minimal_transition_length: float, compensation_length: float
) -> float:
    """
    Calculate the reference length of the transition zone for steel cord belts.
    Args:
        minimal_transition_length (float): The minimal transition length.
        compensation_length (float): The compensation length.
    Returns:
        float: The calculated reference length of the transition zone.
    """
    return minimal_transition_length + compensation_length


def _compensation_length_at_transition_zone(
    distance_belt_edge_to_deepest_level_of_trough: float,
    pulley_lift: float,
    maximal_allowed_pulley_lift: float,
) -> float:
    """
    Calculate the compensation length at the transition zone of a steel cord conveyor belt.

    This function computes the compensation length based on the distance from the belt edge
    to the deepest level of the trough, the pulley lift, and the maximal allowed pulley lift.

    Args:
        distance_belt_edge_to_deepest_level_of_trough (float): The distance from the belt edge
            to the deepest level of the trough.
        pulley_lift (float): The current lift of the pulley.
        maximal_allowed_pulley_lift (float): The maximum allowable lift of the pulley.

    Returns:
        float: The calculated compensation length at the transition zone.
    """
    compensation = (
        90
        * (distance_belt_edge_to_deepest_level_of_trough - pulley_lift)
        * (1 - pulley_lift / (3 * maximal_allowed_pulley_lift))
    )
    return compensation


def _length_of_belt_edge_in_transition_zone(
    minimal_transition_length: float,
    pulley_lift: float,
    part_of_belt_lying_on_side_idler: float,
    troughing_angle: float,
) -> float:
    """
    Calculate the length of the belt edge in the transition zone.

    This function computes the length of the belt edge in the transition zone
    of a conveyor belt system, taking into account the minimal transition length,
    pulley lift, the part of the belt lying on the side idler, and the troughing angle.

    Args:
        minimal_transition_length (float): The minimal transition length of the belt (in meters).
        pulley_lift (float): The vertical lift of the pulley (in meters).
        part_of_belt_lying_on_side_idler (float): The length of the belt lying on the side idler (in meters).
        troughing_angle (float): The troughing angle of the belt (in radians).

    Returns:
        float: The calculated length of the belt edge in the transition zone (in meters).
    """
    squares = (
        minimal_transition_length**2
        + pulley_lift**2
        + 2 * part_of_belt_lying_on_side_idler**2
    )
    parantheses = (
        2
        * part_of_belt_lying_on_side_idler
        * (
            pulley_lift * math.sin(troughing_angle)
            + part_of_belt_lying_on_side_idler * math.cos(troughing_angle)
        )
    )
    length_of_belt_edge = math.sqrt(squares - parantheses)
    return length_of_belt_edge


def _difference_edge_and_center_belt_tensions_steel_cord_belts(
    length_of_belt_edge_in_transition_zone: float,
    minimal_transition_length: float,
    reference_length_of_transition_zone_for_steel_cord_belts: float,
    elastic_modulus: float,
) -> float:
    """
    Calculate the difference between the edge and center belt tensions for steel cord belts.

    This function computes the tension difference based on the length of the belt edge
    in the transition zone, the minimal transition length, the reference length of the
    transition zone for steel cord belts, and the elastic modulus of the belt material.

    Args:
        length_of_belt_edge_in_transition_zone (float): The length of the belt edge in the transition zone.
        minimal_transition_length (float): The minimal transition length of the belt.
        reference_length_of_transition_zone_for_steel_cord_belts (float): The reference length of the transition zone for steel cord belts.
        elastic_modulus (float): The elastic modulus of the belt material.

    Returns:
        float: The calculated difference between the edge and center belt tensions.

    Raises:
        ValueError: If reference_length_of_transition_zone_for_steel_cord_belts is zero.
    """
    if reference_length_of_transition_zone_for_steel_cord_belts == 0:
        raise ValueError(
            "reference_length_of_transition_zone_for_steel_cord_belts cannot be zero"
        )
    difference = (
        (length_of_belt_edge_in_transition_zone - minimal_transition_length)
        * elastic_modulus
        / reference_length_of_transition_zone_for_steel_cord_belts
    )
    return difference


def _difference_edge_and_center_belt_tensions_textile_belts(
    length_of_belt_edge_in_transition_zone: float,
    minimal_transition_length: float,
    elastic_modulus: float,
) -> float:
    """
    Calculate the difference between the edge and center belt tensions for steel cord belts.

    This function computes the tension difference based on the length of the belt edge
    in the transition zone, the minimal transition length, and the elastic modulus of the belt material.

    Args:
        length_of_belt_edge_in_transition_zone (float): The length of the belt edge in the transition zone.
        minimal_transition_length (float): The minimal transition length of the belt.
        elastic_modulus (float): The elastic modulus of the belt material.

    Returns:
        float: The calculated difference between the edge and center belt tensions.

    Raises:
        ValueError: If minimal_transition_length is zero.
    """
    if minimal_transition_length == 0:
        raise ValueError("minimal_transition_length cannot be zero")
    difference = (
        (length_of_belt_edge_in_transition_zone - minimal_transition_length)
        * elastic_modulus
        / minimal_transition_length
    )
    return difference


def _maximal_allowable_pulley_lift(
    distance_from_edge_to_deepest_trough_level: float,
) -> float:
    """
    Calculate the maximal allowable pulley lift based on the distance from the edge to the deepest trough level.

    Parameters
    ----------
    distance_from_edge_to_deepest_trough_level : float
        The distance from the edge of the belt to the deepest level of the trough.

    Returns
    -------
    float
        The maximal allowable pulley lift.

    Raises
    ------
    ValueError
        If the distance is less than or equal to zero.
    """
    if distance_from_edge_to_deepest_trough_level <= 0:
        raise ValueError("distance_from_edge_to_deepest_trough_level must be positive")
    return 1 / 3 * distance_from_edge_to_deepest_trough_level
