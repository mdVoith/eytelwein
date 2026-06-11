"""Public Pint wrappers for minimum pulley diameter calculations."""

from pint import Quantity

from eytelwein.belt_conveyor_design.extended._minimum_pulley_diameter import (
    _resulting_force_from_belt_tensions_and_wrap_angle,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


def resulting_force_from_belt_tensions_and_wrap_angle(
    belt_tension_upper: Quantity,
    belt_tension_lower: Quantity,
    wrap_angle: Quantity,
    unit: str = "kilonewton",
    precision: int | None = 2,
) -> Quantity:
    """Calculate resulting force from belt tensions and wrap angle.

    Converts force quantities to newtons and angle to radians, validates
    physical constraints, then computes the resulting force magnitude.

    Parameters
    ----------
    belt_tension_upper : Quantity
        Upper (tight side) belt tension quantity.
    belt_tension_lower : Quantity
        Lower (slack side) belt tension quantity.
    wrap_angle : Quantity
        Wrap angle quantity (angle dimension).
    unit : str, optional
        Output unit, by default ``"kilonewton"``.
    precision : int | None, optional
        Decimal rounding precision, by default ``2``. Use ``None`` to skip
        rounding.

    Returns
    -------
    Quantity
        Resulting force in requested unit.

    Raises
    ------
    ValueError
        If unit conversion fails or physical constraints are violated
        (negative tensions).
    """
    try:
        belt_tension_upper_n = belt_tension_upper.to(u.newton)
        belt_tension_lower_n = belt_tension_lower.to(u.newton)
        wrap_angle_rad = wrap_angle.to(u.radian)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}") from e

    # Validate physical constraints
    if belt_tension_upper_n.magnitude < 0:
        raise ValueError(
            f"belt_tension_upper cannot be negative, got {belt_tension_upper_n.magnitude}"
        )
    if belt_tension_lower_n.magnitude < 0:
        raise ValueError(
            f"belt_tension_lower cannot be negative, got {belt_tension_lower_n.magnitude}"
        )

    # Ensure the unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as exc:
        raise ValueError(f"Invalid unit: {unit}. Error: {exc}") from exc

    # Calculate the resulting force
    force = (
        _resulting_force_from_belt_tensions_and_wrap_angle(
            belt_tension_upper_n.magnitude,
            belt_tension_lower_n.magnitude,
            wrap_angle_rad.magnitude,
        )
        * u.newton
    )

    # First convert to the requested output unit
    result = force.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
