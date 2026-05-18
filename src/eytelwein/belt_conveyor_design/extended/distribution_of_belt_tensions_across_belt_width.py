from pint import Quantity
from eytelwein.belt_conveyor_design.extended._distribution_of_belt_tensions_across_belt_width import (
    _distance_belt_edge_deepest_level_of_trough,
)

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def distance_belt_edge_deepest_level_of_trough(
    part_of_belt_lying_on_side_idler: Quantity,
    troughing_angle: Quantity,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculates the distance from the belt edge to the deepest level of the trough.
    This function computes the distance based on the part of the belt lying on the
    side idler and the troughing angle. The result is returned in the specified unit
    with the desired precision.
    Args:
        part_of_belt_lying_on_side_idler (Quantity): The portion of the belt lying
            on the side idler, provided as a Pint Quantity.
        troughing_angle (Quantity): The troughing angle, provided as a Pint Quantity.
        unit (str, optional): The desired unit for the result. Defaults to "millimeter".
        precision (int, optional): The number of decimal places to round the result to.
            If None, no rounding is applied. Defaults to 2.
    Returns:
        Quantity: The calculated distance from the belt edge to the deepest level
        of the trough, in the specified unit.
    Raises:
        ValueError: If there is an error in converting the input values or if the
            specified unit is invalid.
    """
    try:
        part_of_belt_lying_on_side_idler_mm = part_of_belt_lying_on_side_idler.to(
            "millimeter"
        )
        troughing_angle_rad = troughing_angle.to("radians")

    except Exception as e:
        raise ValueError(f"Error in converting values: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    result = (
        _distance_belt_edge_deepest_level_of_trough(
            part_of_belt_lying_on_side_idler_mm.magnitude,
            troughing_angle_rad.magnitude,
        )
    ) * (u.millimeter)

    result = result.to(pint_unit)

    if precision is not None:
        result = round(result, precision)

    return result
