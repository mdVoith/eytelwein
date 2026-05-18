"""Public Pint wrappers for translating-mass motor-shaft inertia."""

from pint import Quantity

from eytelwein.belt_conveyor_design.extended._mass_inertia import (
    belt_mass_per_strand as _belt_mass_per_strand,
    payload_mass_total as _payload_mass_total,
    translating_mass_empty as _translating_mass_empty,
    translating_mass_full as _translating_mass_full,
    pulley_radius as _pulley_radius,
    motor_shaft_inertia_total as _motor_shaft_inertia_total,
    inertia_per_drive as _inertia_per_drive,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


def _parse_unit(unit: str):
    try:
        return u.parse_units(unit)
    except Exception as exc:
        raise ValueError(f"Invalid unit: {unit}. Error: {exc}") from exc


def belt_mass_per_strand(
    belt_linear_mass: Quantity,
    center_distance: Quantity,
    unit: str = "kilogram",
    precision: int = 2,
) -> Quantity:
    """Calculate belt mass for one strand.

    Parameters
    ----------
    belt_linear_mass : Quantity
        Belt linear mass quantity.
    center_distance : Quantity
        Conveyor center distance quantity.
    unit : str, optional
        Output unit, by default ``"kilogram"``.
    precision : int, optional
        Decimal rounding precision, by default ``2``. Use ``None`` to skip
        rounding.

    Returns
    -------
    Quantity
        Belt mass per strand in requested unit.

    Raises
    ------
    ValueError
        If unit conversion fails, inputs are not physically meaningful, or the
        requested output unit is invalid.
    """
    try:
        linear_mass = belt_linear_mass.to(u.kilogram / u.meter)
        distance = center_distance.to(u.meter)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if linear_mass.magnitude <= 0:
        raise ValueError("belt_linear_mass must be positive")
    if distance.magnitude <= 0:
        raise ValueError("center_distance must be positive")

    result = (
        _belt_mass_per_strand(linear_mass.magnitude, distance.magnitude) * u.kilogram
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def payload_mass_total(
    payload_mass_per_meter: Quantity,
    center_distance: Quantity,
    unit: str = "kilogram",
    precision: int = 2,
) -> Quantity:
    """Calculate total payload mass over conveyor center distance.

    Parameters
    ----------
    payload_mass_per_meter : Quantity
        Payload mass per meter quantity.
    center_distance : Quantity
        Conveyor center distance quantity.
    unit : str, optional
        Output unit, by default ``"kilogram"``.
    precision : int, optional
        Decimal rounding precision, by default ``2``. Use ``None`` to skip
        rounding.

    Returns
    -------
    Quantity
        Total payload mass in requested unit.

    Raises
    ------
    ValueError
        If unit conversion fails, inputs are not physically meaningful, or the
        requested output unit is invalid.
    """
    try:
        load = payload_mass_per_meter.to(u.kilogram / u.meter)
        distance = center_distance.to(u.meter)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if load.magnitude < 0:
        raise ValueError("payload_mass_per_meter must be non-negative")
    if distance.magnitude <= 0:
        raise ValueError("center_distance must be positive")

    result = _payload_mass_total(load.magnitude, distance.magnitude) * u.kilogram
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def translating_mass_empty(
    idler_mass_upper_total: Quantity,
    idler_mass_lower_total: Quantity,
    belt_mass_per_strand_value: Quantity,
    unit: str = "kilogram",
    precision: int = 2,
) -> Quantity:
    """Calculate translating mass for empty conveyor.

    Parameters
    ----------
    idler_mass_upper_total : Quantity
        Upper-strand total idler mass quantity.
    idler_mass_lower_total : Quantity
        Lower-strand total idler mass quantity.
    belt_mass_per_strand_value : Quantity
        Belt mass per strand quantity.
    unit : str, optional
        Output unit, by default ``"kilogram"``.
    precision : int, optional
        Decimal rounding precision, by default ``2``. Use ``None`` to skip
        rounding.

    Returns
    -------
    Quantity
        Empty-conveyor translating mass in requested unit.

    Raises
    ------
    ValueError
        If unit conversion fails, inputs are not physically meaningful, or the
        requested output unit is invalid.
    """
    try:
        idler_upper = idler_mass_upper_total.to(u.kilogram)
        idler_lower = idler_mass_lower_total.to(u.kilogram)
        belt_mass = belt_mass_per_strand_value.to(u.kilogram)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if idler_upper.magnitude < 0:
        raise ValueError("idler_mass_upper_total must be non-negative")
    if idler_lower.magnitude < 0:
        raise ValueError("idler_mass_lower_total must be non-negative")
    if belt_mass.magnitude < 0:
        raise ValueError("belt_mass_per_strand_value must be non-negative")

    result = (
        _translating_mass_empty(
            idler_upper.magnitude,
            idler_lower.magnitude,
            belt_mass.magnitude,
        )
        * u.kilogram
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def translating_mass_full(
    translating_mass_empty_value: Quantity,
    payload_mass_total_value: Quantity,
    unit: str = "kilogram",
    precision: int = 2,
) -> Quantity:
    """Calculate translating mass for loaded conveyor.

    Parameters
    ----------
    translating_mass_empty_value : Quantity
        Empty-conveyor translating mass quantity.
    payload_mass_total_value : Quantity
        Total payload mass quantity.
    unit : str, optional
        Output unit, by default ``"kilogram"``.
    precision : int, optional
        Decimal rounding precision, by default ``2``. Use ``None`` to skip
        rounding.

    Returns
    -------
    Quantity
        Full-conveyor translating mass in requested unit.

    Raises
    ------
    ValueError
        If unit conversion fails, inputs are not physically meaningful, or the
        requested output unit is invalid.
    """
    try:
        empty_mass = translating_mass_empty_value.to(u.kilogram)
        payload_mass = payload_mass_total_value.to(u.kilogram)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if empty_mass.magnitude < 0:
        raise ValueError("translating_mass_empty_value must be non-negative")
    if payload_mass.magnitude < 0:
        raise ValueError("payload_mass_total_value must be non-negative")

    result = (
        _translating_mass_full(empty_mass.magnitude, payload_mass.magnitude)
        * u.kilogram
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def pulley_radius(
    drive_pulley_diameter: Quantity,
    unit: str = "meter",
    precision: int = 2,
) -> Quantity:
    """Calculate drive pulley radius from drive pulley diameter.

    Parameters
    ----------
    drive_pulley_diameter : Quantity
        Drive pulley diameter quantity.
    unit : str, optional
        Output unit, by default ``"meter"``.
    precision : int, optional
        Decimal rounding precision, by default ``2``. Use ``None`` to skip
        rounding.

    Returns
    -------
    Quantity
        Drive pulley radius in requested unit.

    Raises
    ------
    ValueError
        If unit conversion fails, diameter is not positive, or the requested
        output unit is invalid.
    """
    try:
        diameter = drive_pulley_diameter.to(u.meter)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if diameter.magnitude <= 0:
        raise ValueError("drive_pulley_diameter must be positive")

    result = _pulley_radius(diameter.magnitude) * u.meter
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def motor_shaft_inertia_total(
    translating_mass: Quantity,
    drive_pulley_radius: Quantity,
    gear_ratio_motor_to_pulley: Quantity,
    unit: str = "kilogram * meter**2",
    precision: int = 2,
) -> Quantity:
    """Calculate reflected total inertia at motor shaft.

    Parameters
    ----------
    translating_mass : Quantity
        Translating mass quantity.
    drive_pulley_radius : Quantity
        Drive pulley radius quantity.
    gear_ratio_motor_to_pulley : Quantity
        Gear ratio quantity defined as ``omega_motor / omega_pulley``.
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int, optional
        Decimal rounding precision, by default ``2``. Use ``None`` to skip
        rounding.

    Returns
    -------
    Quantity
        Reflected total inertia in requested unit.

    Raises
    ------
    ValueError
        If unit conversion fails, inputs are not physically meaningful, or the
        requested output unit is invalid.
    """
    try:
        mass = translating_mass.to(u.kilogram)
        radius = drive_pulley_radius.to(u.meter)
        ratio = gear_ratio_motor_to_pulley.to(u.dimensionless)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if mass.magnitude < 0:
        raise ValueError("translating_mass must be non-negative")
    if radius.magnitude <= 0:
        raise ValueError("drive_pulley_radius must be positive")
    if ratio.magnitude <= 0:
        raise ValueError("gear_ratio_motor_to_pulley must be positive")

    result = (
        _motor_shaft_inertia_total(mass.magnitude, radius.magnitude, ratio.magnitude)
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def inertia_per_drive(
    inertia_total_motor_shaft: Quantity,
    motor_count: int,
    unit: str = "kilogram * meter**2",
    precision: int = 2,
) -> Quantity:
    """Calculate reflected inertia per drive motor.

    Parameters
    ----------
    inertia_total_motor_shaft : Quantity
        Total reflected motor-shaft inertia quantity.
    motor_count : int
        Number of drives sharing load.
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int, optional
        Decimal rounding precision, by default ``2``. Use ``None`` to skip
        rounding.

    Returns
    -------
    Quantity
        Per-drive reflected inertia in requested unit.

    Raises
    ------
    ValueError
        If unit conversion fails, total inertia is negative, motor count is
        less than 1, or requested output unit is invalid.
    """
    try:
        total_inertia = inertia_total_motor_shaft.to(u.kilogram * u.meter**2)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if total_inertia.magnitude < 0:
        raise ValueError("inertia_total_motor_shaft must be non-negative")
    if motor_count < 1:
        raise ValueError("motor_count must be >= 1")

    result = (
        _inertia_per_drive(total_inertia.magnitude, motor_count)
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted
