def _belt_weight_per_square_meter(
    tension_member_weight: float,
    top_cover_thickness: float,
    bottom_cover_thickness: float,
    rubber_density: float,
) -> float:
    """
    Calculates the total weight per square meter of a conveyor belt.
    This function computes the total weight per square meter by summing the weight of the tension member and the combined weight of the top and bottom rubber covers.
    Args:
        tension_member_weight (float): Weight per square meter of the tension member (e.g., fabric or steel cords) in kg/m².
        top_cover_thickness (float): Thickness of the top rubber cover in meters.
        bottom_cover_thickness (float): Thickness of the bottom rubber cover in meters.
        rubber_density (float): Density of the rubber material in kg/m³.
    Returns:
        float: Total weight per square meter of the conveyor belt in kg/m².
    """

    cover_weight = (top_cover_thickness + bottom_cover_thickness) * rubber_density
    total_weight_per_square_meter = tension_member_weight + cover_weight

    return total_weight_per_square_meter


def _line_load_belt(
    tension_member_weight: float,
    belt_width: float,
    top_cover_thickness: float,
    bottom_cover_thickness: float,
    rubber_density: float,
) -> float:
    """
    Calculate the line load of a conveyor belt.

    Args:
        tension_member_weight: Weight of the tension member in kg/m²
        belt_width: Width of the belt in meters
        top_cover_thickness: Thickness of the top cover in m
        bottom_cover_thickness: Thickness of the bottom cover in m
        rubber_density: Density of the rubber in kg/m³

    Returns:
        Line load in kg/m
    """

    # Calculate total weight per square meter
    total_weight_per_square_meter = _belt_weight_per_square_meter(
        tension_member_weight,
        top_cover_thickness,
        bottom_cover_thickness,
        rubber_density,
    )
    # Calculate line load by multiplying weight per square meter by belt width
    total_weight_per_meter = total_weight_per_square_meter * belt_width

    return total_weight_per_meter


def _line_load_belt_from_belt_weight_per_square_meter(
    belt_weight_per_square_meter: float, belt_width: float
) -> float:
    """
    Calculate the line load of a conveyor belt from its weight per square meter.

    Args:
        belt_weight_per_square_meter: Weight of the belt per square meter in kg/m²
        belt_width: Width of the belt in meters

    Returns:
        Line load in kg/m
    """
    # Calculate line load by multiplying weight per square meter by belt width
    total_weight_per_meter = belt_weight_per_square_meter * belt_width

    return total_weight_per_meter
