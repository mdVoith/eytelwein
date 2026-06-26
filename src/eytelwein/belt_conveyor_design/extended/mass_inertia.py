"""Public Pint wrappers for translating-mass and motor-shaft inertia functions."""

from pint import Quantity

from eytelwein.belt_conveyor_design.extended._mass_inertia import (
    _translating_mass_from_line_load_and_segment_length,
    _translating_mass_idler_carry,
    _translating_mass_idler_return,
    _translating_mass_belt,
    _translating_mass_material,
    _total_translating_mass_empty,
    _total_translating_mass,
    _drive_pulley_radius_from_drive_pulley_diameter,
    _translating_mass_inertia_at_pulley_circumference,
    _mass_inertia_at_pulley_shaft,
    _component_inertia_referred_to_motor_shaft,
    _total_low_speed_inertia,
    _total_inertia_for_single_drive,
    _fluid_coupling_design_inertia,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


def _parse_unit(unit: str):
    """Parse a user-provided output unit string.

    Parameters
    ----------
    unit : str
        Output unit string expected by Pint.

    Returns
    -------
    pint.Unit
        Parsed Pint unit object.

    Raises
    ------
    ValueError
        If the requested output unit string is invalid.
    """
    try:
        return u.parse_units(unit)
    except Exception as exc:
        raise ValueError(f"Invalid unit: {unit}. Error: {exc}") from exc


def translating_mass_from_line_load_and_segment_length(
    line_load: Quantity,
    segment_length: Quantity,
    unit: str = "kilogram",
    precision: int | None = None,
) -> Quantity:
    """Calculate translating mass from line load and segment length.

    Parameters
    ----------
    line_load : Quantity
        Translating line load quantity.
    segment_length : Quantity
        Conveyor segment length quantity.
    unit : str, optional
        Output unit, by default ``"kilogram"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Translating mass in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        line_load_kg_per_m = line_load.to(u.kilogram / u.meter)
        segment_length_m = segment_length.to(u.meter)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if line_load_kg_per_m.magnitude < 0:
        raise ValueError("line_load must be non-negative")
    if segment_length_m.magnitude <= 0:
        raise ValueError("segment_length must be positive")

    result = (
        _translating_mass_from_line_load_and_segment_length(
            line_load_kg_per_m.magnitude, segment_length_m.magnitude
        )
        * u.kilogram
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def translating_mass_idler_carry(
    idler_carry_line_load: Quantity,
    segment_length: Quantity,
    unit: str = "kilogram",
    precision: int | None = None,
) -> Quantity:
    """Calculate carry-idler translating mass.

    Parameters
    ----------
    idler_carry_line_load : Quantity
        Carry-idler line load quantity.
    segment_length : Quantity
        Conveyor segment length quantity.
    unit : str, optional
        Output unit, by default ``"kilogram"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Carry-idler translating mass in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        line_load_kg_per_m = idler_carry_line_load.to(u.kilogram / u.meter)
        segment_length_m = segment_length.to(u.meter)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if line_load_kg_per_m.magnitude < 0:
        raise ValueError("idler_carry_line_load must be non-negative")
    if segment_length_m.magnitude <= 0:
        raise ValueError("segment_length must be positive")

    result = (
        _translating_mass_idler_carry(
            line_load_kg_per_m.magnitude, segment_length_m.magnitude
        )
        * u.kilogram
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def translating_mass_idler_return(
    idler_return_line_load: Quantity,
    segment_length: Quantity,
    unit: str = "kilogram",
    precision: int | None = None,
) -> Quantity:
    """Calculate return-idler translating mass.

    Parameters
    ----------
    idler_return_line_load : Quantity
        Return-idler line load quantity.
    segment_length : Quantity
        Conveyor segment length quantity.
    unit : str, optional
        Output unit, by default ``"kilogram"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Return-idler translating mass in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        line_load_kg_per_m = idler_return_line_load.to(u.kilogram / u.meter)
        segment_length_m = segment_length.to(u.meter)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if line_load_kg_per_m.magnitude < 0:
        raise ValueError("idler_return_line_load must be non-negative")
    if segment_length_m.magnitude <= 0:
        raise ValueError("segment_length must be positive")

    result = (
        _translating_mass_idler_return(
            line_load_kg_per_m.magnitude, segment_length_m.magnitude
        )
        * u.kilogram
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def translating_mass_belt(
    belt_line_load: Quantity,
    segment_length: Quantity,
    unit: str = "kilogram",
    precision: int | None = None,
) -> Quantity:
    """Calculate belt translating mass for one strand.

    Parameters
    ----------
    belt_line_load : Quantity
        Belt line load quantity for one strand.
    segment_length : Quantity
        Conveyor segment length quantity.
    unit : str, optional
        Output unit, by default ``"kilogram"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Belt translating mass for one strand in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        line_load_kg_per_m = belt_line_load.to(u.kilogram / u.meter)
        segment_length_m = segment_length.to(u.meter)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if line_load_kg_per_m.magnitude <= 0:
        raise ValueError("belt_line_load must be positive")
    if segment_length_m.magnitude <= 0:
        raise ValueError("segment_length must be positive")

    result = (
        _translating_mass_belt(line_load_kg_per_m.magnitude, segment_length_m.magnitude)
        * u.kilogram
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def translating_mass_material(
    material_line_load: Quantity,
    segment_length: Quantity,
    unit: str = "kilogram",
    precision: int | None = None,
) -> Quantity:
    """Calculate material translating mass.

    Parameters
    ----------
    material_line_load : Quantity
        Material line load quantity.
    segment_length : Quantity
        Conveyor segment length quantity.
    unit : str, optional
        Output unit, by default ``"kilogram"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Material translating mass in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        line_load_kg_per_m = material_line_load.to(u.kilogram / u.meter)
        segment_length_m = segment_length.to(u.meter)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if line_load_kg_per_m.magnitude < 0:
        raise ValueError("material_line_load must be non-negative")
    if segment_length_m.magnitude <= 0:
        raise ValueError("segment_length must be positive")

    result = (
        _translating_mass_material(
            line_load_kg_per_m.magnitude, segment_length_m.magnitude
        )
        * u.kilogram
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def total_translating_mass_empty(
    translating_mass_idler_carry_value: Quantity,
    translating_mass_idler_return_value: Quantity,
    translating_mass_belt_per_strand_value: Quantity,
    unit: str = "kilogram",
    precision: int | None = None,
) -> Quantity:
    """Calculate total translating mass for empty conveyor.

    Parameters
    ----------
    translating_mass_idler_carry_value : Quantity
        Carry-idler translating mass quantity.
    translating_mass_idler_return_value : Quantity
        Return-idler translating mass quantity.
    translating_mass_belt_per_strand_value : Quantity
        Belt translating mass quantity for one strand.
    unit : str, optional
        Output unit, by default ``"kilogram"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Empty-conveyor total translating mass in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        idler_carry = translating_mass_idler_carry_value.to(u.kilogram)
        idler_return = translating_mass_idler_return_value.to(u.kilogram)
        belt = translating_mass_belt_per_strand_value.to(u.kilogram)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if idler_carry.magnitude < 0:
        raise ValueError("translating_mass_idler_carry_value must be non-negative")
    if idler_return.magnitude < 0:
        raise ValueError("translating_mass_idler_return_value must be non-negative")
    if belt.magnitude < 0:
        raise ValueError("translating_mass_belt_per_strand_value must be non-negative")

    result = (
        _total_translating_mass_empty(
            idler_carry.magnitude,
            idler_return.magnitude,
            belt.magnitude,
        )
        * u.kilogram
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def total_translating_mass(
    total_translating_mass_empty_value: Quantity,
    translating_mass_material_value: Quantity,
    unit: str = "kilogram",
    precision: int | None = None,
) -> Quantity:
    """Calculate total translating mass for loaded conveyor.

    Parameters
    ----------
    total_translating_mass_empty_value : Quantity
        Empty-conveyor total translating mass quantity.
    translating_mass_material_value : Quantity
        Material translating mass quantity.
    unit : str, optional
        Output unit, by default ``"kilogram"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Loaded-conveyor total translating mass in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        empty_mass = total_translating_mass_empty_value.to(u.kilogram)
        material_mass = translating_mass_material_value.to(u.kilogram)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if empty_mass.magnitude < 0:
        raise ValueError("total_translating_mass_empty_value must be non-negative")
    if material_mass.magnitude < 0:
        raise ValueError("translating_mass_material_value must be non-negative")

    result = (
        _total_translating_mass(empty_mass.magnitude, material_mass.magnitude)
        * u.kilogram
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def drive_pulley_radius_from_drive_pulley_diameter(
    drive_pulley_diameter: Quantity,
    unit: str = "meter",
    precision: int | None = None,
) -> Quantity:
    """Calculate drive pulley radius from drive pulley diameter.

    Parameters
    ----------
    drive_pulley_diameter : Quantity
        Drive pulley diameter quantity.
    unit : str, optional
        Output unit, by default ``"meter"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Drive pulley radius in the requested output unit.

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

    result = (
        _drive_pulley_radius_from_drive_pulley_diameter(diameter.magnitude) * u.meter
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def translating_mass_inertia_at_pulley_circumference(
    translating_mass: Quantity,
    drive_pulley_radius: Quantity,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Calculate translating-mass inertia contribution at pulley circumference.

    Parameters
    ----------
    translating_mass : Quantity
        Total translating mass quantity.
    drive_pulley_radius : Quantity
        Drive pulley radius quantity.
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Translating-mass inertia contribution at pulley circumference (low-speed side)
        in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        mass = translating_mass.to(u.kilogram)
        radius = drive_pulley_radius.to(u.meter)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if mass.magnitude < 0:
        raise ValueError("translating_mass must be non-negative")
    if radius.magnitude <= 0:
        raise ValueError("drive_pulley_radius must be positive")

    result = (
        _translating_mass_inertia_at_pulley_circumference(
            mass.magnitude, radius.magnitude
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def mass_inertia_at_pulley_shaft(
    translating_mass: Quantity,
    drive_pulley_radius: Quantity,
    pulley_inertia_native: Quantity | None = None,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Calculate total inertia at pulley shaft from translating mass and native pulley inertia.

    Parameters
    ----------
    translating_mass : Quantity
        Total translating mass quantity.
    drive_pulley_radius : Quantity
        Drive pulley radius quantity.
    pulley_inertia_native : Quantity | None, optional
        Native (inherent) pulley inertia quantity, by default None (treated as zero).
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Total inertia at pulley shaft in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        mass = translating_mass.to(u.kilogram)
        radius = drive_pulley_radius.to(u.meter)
        native_inertia_kg_m2 = (
            pulley_inertia_native.to(u.kilogram * u.meter**2).magnitude
            if pulley_inertia_native is not None
            else 0.0
        )
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if mass.magnitude < 0:
        raise ValueError("translating_mass must be non-negative")
    if radius.magnitude <= 0:
        raise ValueError("drive_pulley_radius must be positive")
    if native_inertia_kg_m2 < 0:
        raise ValueError("pulley_inertia_native must be non-negative")

    result = (
        _mass_inertia_at_pulley_shaft(
            mass.magnitude, radius.magnitude, native_inertia_kg_m2
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def component_inertia_referred_to_motor_shaft(
    component_inertia: Quantity,
    gear_ratio_motor_to_component: Quantity,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Convert native component inertia to motor-shaft-equivalent inertia.

    Parameters
    ----------
    component_inertia : Quantity
        Native component inertia quantity.
    gear_ratio_motor_to_component : Quantity
        Dimensionless gear ratio ``omega_motor / omega_component``.
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Component inertia referred to the motor shaft in the requested output
        unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        inertia = component_inertia.to(u.kilogram * u.meter**2)
        gear_ratio = gear_ratio_motor_to_component.to(u.dimensionless)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if inertia.magnitude < 0:
        raise ValueError("component_inertia must be non-negative")
    if gear_ratio.magnitude <= 0:
        raise ValueError("gear_ratio_motor_to_component must be positive")

    result = (
        _component_inertia_referred_to_motor_shaft(
            inertia.magnitude, gear_ratio.magnitude
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def total_low_speed_inertia(
    mass_inertia_at_pulley_shaft: Quantity,
    low_speed_coupling_inertia: Quantity | None = None,
    low_speed_brake_inertia: Quantity | None = None,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Calculate total low-speed-side inertia at pulley shaft.

    Sums mass inertia at pulley shaft plus optional low-speed coupling and
    brake inertias.

    Parameters
    ----------
    mass_inertia_at_pulley_shaft : Quantity
        Total inertia at pulley shaft quantity.
    low_speed_coupling_inertia : Quantity | None, optional
        Low-speed coupling inertia quantity, by default None (treated as zero).
    low_speed_brake_inertia : Quantity | None, optional
        Low-speed brake inertia quantity, by default None (treated as zero).
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Total low-speed-side inertia in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        mass_inertia = mass_inertia_at_pulley_shaft.to(u.kilogram * u.meter**2)
        ls_coupling = (
            0.0
            if low_speed_coupling_inertia is None
            else low_speed_coupling_inertia.to(u.kilogram * u.meter**2).magnitude
        )
        ls_brake = (
            0.0
            if low_speed_brake_inertia is None
            else low_speed_brake_inertia.to(u.kilogram * u.meter**2).magnitude
        )
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if mass_inertia.magnitude < 0:
        raise ValueError("mass_inertia_at_pulley_shaft must be non-negative")
    if ls_coupling < 0:
        raise ValueError("low_speed_coupling_inertia must be non-negative")
    if ls_brake < 0:
        raise ValueError("low_speed_brake_inertia must be non-negative")

    result = (
        _total_low_speed_inertia(
            mass_inertia.magnitude,
            ls_coupling,
            ls_brake,
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def fluid_coupling_design_inertia(
    total_low_speed_inertia: Quantity,
    gearbox_ratio_motor_to_low_speed_side: Quantity,
    high_speed_coupling_inertia: Quantity | None = None,
    high_speed_brake_inertia: Quantity | None = None,
    gearbox_inertia: Quantity | None = None,
    flywheel_inertia: Quantity | None = None,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Calculate fluid-coupling design inertia from low-speed total and gearbox ratio.

    Reflects total low-speed inertia to motor shaft via gearbox ratio, then sums
    with high-speed components (coupling, brake, gearbox, flywheel).

    Parameters
    ----------
    total_low_speed_inertia : Quantity
        Total low-speed-side inertia quantity.
    gearbox_ratio_motor_to_low_speed_side : Quantity
        Gearbox ratio ``omega_motor / omega_low_speed_side`` quantity.
    high_speed_coupling_inertia : Quantity | None, optional
        High-speed coupling inertia quantity, by default None (treated as zero).
    high_speed_brake_inertia : Quantity | None, optional
        High-speed brake inertia quantity, by default None (treated as zero).
    gearbox_inertia : Quantity | None, optional
        Gearbox inertia (high-speed side) quantity, by default None (treated as zero).
    flywheel_inertia : Quantity | None, optional
        Flywheel inertia quantity, by default None (treated as zero).
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Fluid-coupling design inertia in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        ls_total = total_low_speed_inertia.to(u.kilogram * u.meter**2)
        ratio = gearbox_ratio_motor_to_low_speed_side.to(u.dimensionless)
        hs_coupling = (
            0.0
            if high_speed_coupling_inertia is None
            else high_speed_coupling_inertia.to(u.kilogram * u.meter**2).magnitude
        )
        hs_brake = (
            0.0
            if high_speed_brake_inertia is None
            else high_speed_brake_inertia.to(u.kilogram * u.meter**2).magnitude
        )
        gearbox = (
            0.0
            if gearbox_inertia is None
            else gearbox_inertia.to(u.kilogram * u.meter**2).magnitude
        )
        flywheel = (
            0.0
            if flywheel_inertia is None
            else flywheel_inertia.to(u.kilogram * u.meter**2).magnitude
        )
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if ls_total.magnitude < 0:
        raise ValueError("total_low_speed_inertia must be non-negative")
    if ratio.magnitude <= 0:
        raise ValueError("gearbox_ratio_motor_to_low_speed_side must be positive")

    result = (
        _fluid_coupling_design_inertia(
            total_low_speed_inertia_kg_m2=ls_total.magnitude,
            gearbox_ratio_motor_to_low_speed_side=ratio.magnitude,
            high_speed_coupling_inertia_kg_m2=hs_coupling,
            high_speed_brake_inertia_kg_m2=hs_brake,
            gearbox_inertia_kg_m2=gearbox,
            flywheel_inertia_kg_m2=flywheel,
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def total_inertia_for_single_drive(
    total_low_speed_inertia: Quantity,
    quantity_of_drives: int,
    gearbox_ratio_motor_to_low_speed_side: Quantity,
    high_speed_coupling_inertia: Quantity | None = None,
    high_speed_brake_inertia: Quantity | None = None,
    gearbox_inertia: Quantity | None = None,
    flywheel_inertia: Quantity | None = None,
    fluid_coupling_inertia: Quantity | None = None,
    motor_coupling_inertia: Quantity | None = None,
    motor_inertia: Quantity | None = None,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Calculate per-drive total inertia from shared low-speed and single-drive motor-side components.

    Reflects total low-speed inertia to motor shaft via gearbox ratio, divides by quantity_of_drives
    (to apportion the shared inertia across parallel drives), then adds optional single-drive
    high-speed and motor-side inertias.

    Parameters
    ----------
    total_low_speed_inertia : Quantity
        Total low-speed-side inertia quantity.
    quantity_of_drives : int
        Number of drives sharing the low-speed inertia. Must be >= 1.
    gearbox_ratio_motor_to_low_speed_side : Quantity
        Gearbox ratio ``omega_motor / omega_low_speed_side`` quantity.
    high_speed_coupling_inertia : Quantity | None, optional
        High-speed coupling inertia (single drive) quantity, by default None (treated as zero).
    high_speed_brake_inertia : Quantity | None, optional
        High-speed brake inertia (single drive) quantity, by default None (treated as zero).
    gearbox_inertia : Quantity | None, optional
        Gearbox inertia on high-speed side (single drive) quantity, by default None (treated as zero).
    flywheel_inertia : Quantity | None, optional
        Flywheel inertia (single drive) quantity, by default None (treated as zero).
    fluid_coupling_inertia : Quantity | None, optional
        Fluid-coupling inertia (single drive) quantity, by default None (treated as zero).
    motor_coupling_inertia : Quantity | None, optional
        Motor coupling inertia (single drive) quantity, by default None (treated as zero).
    motor_inertia : Quantity | None, optional
        Motor inertia (single drive) quantity, by default None (treated as zero).
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Per-drive total inertia in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        ls_total = total_low_speed_inertia.to(u.kilogram * u.meter**2)
        ratio = gearbox_ratio_motor_to_low_speed_side.to(u.dimensionless)
        hs_coupling = (
            0.0
            if high_speed_coupling_inertia is None
            else high_speed_coupling_inertia.to(u.kilogram * u.meter**2).magnitude
        )
        hs_brake = (
            0.0
            if high_speed_brake_inertia is None
            else high_speed_brake_inertia.to(u.kilogram * u.meter**2).magnitude
        )
        gearbox = (
            0.0
            if gearbox_inertia is None
            else gearbox_inertia.to(u.kilogram * u.meter**2).magnitude
        )
        flywheel = (
            0.0
            if flywheel_inertia is None
            else flywheel_inertia.to(u.kilogram * u.meter**2).magnitude
        )
        fluid_coupling = (
            0.0
            if fluid_coupling_inertia is None
            else fluid_coupling_inertia.to(u.kilogram * u.meter**2).magnitude
        )
        motor_coupling = (
            0.0
            if motor_coupling_inertia is None
            else motor_coupling_inertia.to(u.kilogram * u.meter**2).magnitude
        )
        motor = (
            0.0
            if motor_inertia is None
            else motor_inertia.to(u.kilogram * u.meter**2).magnitude
        )
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if ls_total.magnitude < 0:
        raise ValueError("total_low_speed_inertia must be non-negative")
    if isinstance(quantity_of_drives, bool):
        raise ValueError("quantity_of_drives must be int, not bool")
    if not isinstance(quantity_of_drives, int):
        raise ValueError("quantity_of_drives must be int")
    if quantity_of_drives < 1:
        raise ValueError("quantity_of_drives must be >= 1")
    if ratio.magnitude <= 0:
        raise ValueError("gearbox_ratio_motor_to_low_speed_side must be positive")

    result = (
        _total_inertia_for_single_drive(
            total_low_speed_inertia_kg_m2=ls_total.magnitude,
            quantity_of_drives=quantity_of_drives,
            gearbox_ratio_motor_to_low_speed_side=ratio.magnitude,
            high_speed_coupling_inertia_kg_m2=hs_coupling,
            high_speed_brake_inertia_kg_m2=hs_brake,
            gearbox_inertia_kg_m2=gearbox,
            flywheel_inertia_kg_m2=flywheel,
            fluid_coupling_inertia_kg_m2=fluid_coupling,
            motor_coupling_inertia_kg_m2=motor_coupling,
            motor_inertia_kg_m2=motor,
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted
