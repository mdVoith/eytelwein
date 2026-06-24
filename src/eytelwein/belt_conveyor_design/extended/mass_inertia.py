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
    _reflected_translating_mass_inertia_at_motor_shaft,
    _component_inertia_referred_to_motor_shaft,
    _total_motor_shaft_rotational_inertia_from_equivalent_component_inertias,
    _total_motor_shaft_rotational_inertia_from_native_component_inertias,
    _low_speed_native_component_inertia_at_motor_shaft,
    _high_speed_native_component_inertia_at_motor_shaft,
    _fluid_coupling_inertia_referred_to_motor_shaft,
    _total_rotational_inertia_at_motor_shaft,
    _total_rotational_inertia_at_fluid_coupling_shaft,
    _rotational_inertia_breakdown_at_motor_shaft,
    _motor_shaft_rotational_inertia_per_drive,
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


def reflected_translating_mass_inertia_at_motor_shaft(
    translating_mass: Quantity,
    drive_pulley_radius: Quantity,
    gear_ratio_motor_to_pulley: Quantity,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Calculate reflected translating-mass inertia contribution at motor shaft.

    This function converts pulley-shaft inertia to motor-shaft-equivalent inertia
    by applying the squared speed ratio. It composes two primitives:
    (1) translating mass → pulley-shaft inertia
    (2) pulley-shaft inertia → motor-shaft inertia via speed reduction

    Parameters
    ----------
    translating_mass : Quantity
        Total translating mass quantity.
    drive_pulley_radius : Quantity
        Drive pulley radius quantity.
    gear_ratio_motor_to_pulley : Quantity
        Gear ratio quantity defined as ``omega_motor / omega_pulley``.
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Reflected translating-mass inertia contribution at motor shaft in the
        requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
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
        _reflected_translating_mass_inertia_at_motor_shaft(
            mass.magnitude, radius.magnitude, ratio.magnitude
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


def total_motor_shaft_rotational_inertia_from_equivalent_component_inertias(
    reflected_translating_mass_inertia: Quantity,
    gearbox_inertia_at_motor_shaft: Quantity,
    coupling_inertia_at_motor_shaft: Quantity,
    brake_inertia_at_motor_shaft: Quantity,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Sum motor-shaft-equivalent rotational inertia contributions.

    Parameters
    ----------
    reflected_translating_mass_inertia : Quantity
        Reflected translating-mass inertia contribution at motor shaft.
    gearbox_inertia_at_motor_shaft : Quantity
        Gearbox inertia already referred to motor shaft.
    coupling_inertia_at_motor_shaft : Quantity
        Coupling inertia already referred to motor shaft.
    brake_inertia_at_motor_shaft : Quantity
        Brake inertia already referred to motor shaft.
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Total motor-shaft rotational inertia in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails or requested output unit is invalid.
    """
    try:
        translating = reflected_translating_mass_inertia.to(u.kilogram * u.meter**2)
        gearbox = gearbox_inertia_at_motor_shaft.to(u.kilogram * u.meter**2)
        coupling = coupling_inertia_at_motor_shaft.to(u.kilogram * u.meter**2)
        brake = brake_inertia_at_motor_shaft.to(u.kilogram * u.meter**2)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    result = (
        _total_motor_shaft_rotational_inertia_from_equivalent_component_inertias(
            translating.magnitude,
            gearbox.magnitude,
            coupling.magnitude,
            brake.magnitude,
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def total_motor_shaft_rotational_inertia_from_native_component_inertias(
    reflected_translating_mass_inertia: Quantity,
    gearbox_inertia_native: Quantity,
    drive_gear_ratio_motor_to_low_speed_side: Quantity,
    coupling_inertia_native: Quantity,
    brake_inertia_native: Quantity,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Sum translating inertia and native component inertias at motor shaft.

    Parameters
    ----------
    reflected_translating_mass_inertia : Quantity
        Reflected translating-mass inertia contribution at motor shaft.
    gearbox_inertia_native : Quantity
        Native gearbox inertia quantity.
    drive_gear_ratio_motor_to_low_speed_side : Quantity
        Dimensionless drive gear ratio ``omega_motor / omega_low_speed_side``
        used for all low-speed-side native inertias.
    coupling_inertia_native : Quantity
        Native coupling inertia quantity.
    brake_inertia_native : Quantity
        Native brake inertia quantity.
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Total motor-shaft rotational inertia in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails or requested output unit is invalid.
    """
    try:
        translating = reflected_translating_mass_inertia.to(u.kilogram * u.meter**2)
        gearbox_inertia = gearbox_inertia_native.to(u.kilogram * u.meter**2)
        drive_ratio = drive_gear_ratio_motor_to_low_speed_side.to(u.dimensionless)
        coupling_inertia = coupling_inertia_native.to(u.kilogram * u.meter**2)
        brake_inertia = brake_inertia_native.to(u.kilogram * u.meter**2)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    result = (
        _total_motor_shaft_rotational_inertia_from_native_component_inertias(
            translating.magnitude,
            gearbox_inertia.magnitude,
            drive_ratio.magnitude,
            coupling_inertia.magnitude,
            brake_inertia.magnitude,
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def low_speed_native_component_inertia_at_motor_shaft(
    *,
    pulley_inertia_native: Quantity | None = None,
    pulley_gear_ratio_motor_to_component: Quantity | None = None,
    low_speed_coupling_inertia_native: Quantity | None = None,
    low_speed_coupling_gear_ratio_motor_to_component: Quantity | None = None,
    low_speed_brake_inertia_native: Quantity | None = None,
    low_speed_brake_gear_ratio_motor_to_component: Quantity | None = None,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Sum low-speed native component inertias referred to motor shaft.

    All component inputs are optional. When a low-speed inertia input is
    positive, the corresponding gear ratio must be provided.
    """
    try:
        pulley_inertia = (
            0.0
            if pulley_inertia_native is None
            else pulley_inertia_native.to(u.kilogram * u.meter**2).magnitude
        )
        pulley_ratio = (
            None
            if pulley_gear_ratio_motor_to_component is None
            else pulley_gear_ratio_motor_to_component.to(u.dimensionless).magnitude
        )

        coupling_inertia = (
            0.0
            if low_speed_coupling_inertia_native is None
            else low_speed_coupling_inertia_native.to(u.kilogram * u.meter**2).magnitude
        )
        coupling_ratio = (
            None
            if low_speed_coupling_gear_ratio_motor_to_component is None
            else low_speed_coupling_gear_ratio_motor_to_component.to(
                u.dimensionless
            ).magnitude
        )

        brake_inertia = (
            0.0
            if low_speed_brake_inertia_native is None
            else low_speed_brake_inertia_native.to(u.kilogram * u.meter**2).magnitude
        )
        brake_ratio = (
            None
            if low_speed_brake_gear_ratio_motor_to_component is None
            else low_speed_brake_gear_ratio_motor_to_component.to(
                u.dimensionless
            ).magnitude
        )
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    result = (
        _low_speed_native_component_inertia_at_motor_shaft(
            pulley_inertia_native_kg_m2=pulley_inertia,
            pulley_gear_ratio_motor_to_component=pulley_ratio,
            low_speed_coupling_inertia_native_kg_m2=coupling_inertia,
            low_speed_coupling_gear_ratio_motor_to_component=coupling_ratio,
            low_speed_brake_inertia_native_kg_m2=brake_inertia,
            low_speed_brake_gear_ratio_motor_to_component=brake_ratio,
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def high_speed_native_component_inertia_at_motor_shaft(
    *,
    high_speed_coupling_inertia_native: Quantity | None = None,
    high_speed_coupling_gear_ratio_motor_to_component: Quantity | None = None,
    high_speed_brake_inertia_native: Quantity | None = None,
    high_speed_brake_gear_ratio_motor_to_component: Quantity | None = None,
    fluid_coupling_inertia_native: Quantity | None = None,
    fluid_coupling_gear_ratio_motor_to_component: Quantity | None = None,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Sum high-speed native component inertias referred to motor shaft.

    All component inputs are optional. High-speed gear ratios default to
    ``1.0`` when omitted.
    """
    try:
        hs_coupling_inertia = (
            0.0
            if high_speed_coupling_inertia_native is None
            else high_speed_coupling_inertia_native.to(
                u.kilogram * u.meter**2
            ).magnitude
        )
        hs_coupling_ratio = (
            None
            if high_speed_coupling_gear_ratio_motor_to_component is None
            else high_speed_coupling_gear_ratio_motor_to_component.to(
                u.dimensionless
            ).magnitude
        )

        hs_brake_inertia = (
            0.0
            if high_speed_brake_inertia_native is None
            else high_speed_brake_inertia_native.to(u.kilogram * u.meter**2).magnitude
        )
        hs_brake_ratio = (
            None
            if high_speed_brake_gear_ratio_motor_to_component is None
            else high_speed_brake_gear_ratio_motor_to_component.to(
                u.dimensionless
            ).magnitude
        )

        fluid_inertia = (
            0.0
            if fluid_coupling_inertia_native is None
            else fluid_coupling_inertia_native.to(u.kilogram * u.meter**2).magnitude
        )
        fluid_ratio = (
            None
            if fluid_coupling_gear_ratio_motor_to_component is None
            else fluid_coupling_gear_ratio_motor_to_component.to(
                u.dimensionless
            ).magnitude
        )
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    result = (
        _high_speed_native_component_inertia_at_motor_shaft(
            high_speed_coupling_inertia_native_kg_m2=hs_coupling_inertia,
            high_speed_coupling_gear_ratio_motor_to_component=hs_coupling_ratio,
            high_speed_brake_inertia_native_kg_m2=hs_brake_inertia,
            high_speed_brake_gear_ratio_motor_to_component=hs_brake_ratio,
            fluid_coupling_inertia_native_kg_m2=fluid_inertia,
            fluid_coupling_gear_ratio_motor_to_component=fluid_ratio,
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def fluid_coupling_inertia_referred_to_motor_shaft(
    fluid_coupling_inertia_native: Quantity,
    gear_ratio_motor_to_fluid_coupling: Quantity,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Convert native fluid-coupling inertia to motor-shaft-equivalent inertia."""
    try:
        fluid_inertia = fluid_coupling_inertia_native.to(u.kilogram * u.meter**2)
        ratio = gear_ratio_motor_to_fluid_coupling.to(u.dimensionless)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    result = (
        _fluid_coupling_inertia_referred_to_motor_shaft(
            fluid_inertia.magnitude,
            ratio.magnitude,
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def total_rotational_inertia_at_motor_shaft(
    *,
    reflected_translating_mass_inertia: Quantity | None = None,
    gearbox_inertia_at_motor_shaft: Quantity | None = None,
    low_speed_native_component_inertia_at_motor_shaft: Quantity | None = None,
    high_speed_native_component_inertia_at_motor_shaft: Quantity | None = None,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Calculate total rotational inertia at motor shaft from layer totals.

    All layer inputs are optional and default to zero.
    """
    try:
        reflected = (
            0.0
            if reflected_translating_mass_inertia is None
            else reflected_translating_mass_inertia.to(
                u.kilogram * u.meter**2
            ).magnitude
        )
        gearbox = (
            0.0
            if gearbox_inertia_at_motor_shaft is None
            else gearbox_inertia_at_motor_shaft.to(u.kilogram * u.meter**2).magnitude
        )
        low_speed = (
            0.0
            if low_speed_native_component_inertia_at_motor_shaft is None
            else low_speed_native_component_inertia_at_motor_shaft.to(
                u.kilogram * u.meter**2
            ).magnitude
        )
        high_speed = (
            0.0
            if high_speed_native_component_inertia_at_motor_shaft is None
            else high_speed_native_component_inertia_at_motor_shaft.to(
                u.kilogram * u.meter**2
            ).magnitude
        )
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    result = (
        _total_rotational_inertia_at_motor_shaft(
            reflected_translating_mass_inertia_kg_m2=reflected,
            gearbox_inertia_at_motor_shaft_kg_m2=gearbox,
            low_speed_native_component_inertia_at_motor_shaft_kg_m2=low_speed,
            high_speed_native_component_inertia_at_motor_shaft_kg_m2=high_speed,
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def total_rotational_inertia_at_fluid_coupling_shaft(
    total_rotational_inertia_at_motor_shaft_value: Quantity,
    gear_ratio_motor_to_fluid_coupling: Quantity,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Convert total rotational inertia at motor shaft to fluid-coupling shaft."""
    try:
        total_motor = total_rotational_inertia_at_motor_shaft_value.to(
            u.kilogram * u.meter**2
        )
        ratio = gear_ratio_motor_to_fluid_coupling.to(u.dimensionless)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    result = (
        _total_rotational_inertia_at_fluid_coupling_shaft(
            total_motor.magnitude,
            ratio.magnitude,
        )
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted


def rotational_inertia_breakdown_at_motor_shaft(
    *,
    reflected_translating_mass_inertia: Quantity | None = None,
    gearbox_inertia_at_motor_shaft: Quantity | None = None,
    pulley_inertia_native: Quantity | None = None,
    pulley_gear_ratio_motor_to_component: Quantity | None = None,
    low_speed_coupling_inertia_native: Quantity | None = None,
    low_speed_coupling_gear_ratio_motor_to_component: Quantity | None = None,
    low_speed_brake_inertia_native: Quantity | None = None,
    low_speed_brake_gear_ratio_motor_to_component: Quantity | None = None,
    high_speed_coupling_inertia_native: Quantity | None = None,
    high_speed_coupling_gear_ratio_motor_to_component: Quantity | None = None,
    high_speed_brake_inertia_native: Quantity | None = None,
    high_speed_brake_gear_ratio_motor_to_component: Quantity | None = None,
    fluid_coupling_inertia_native: Quantity | None = None,
    fluid_coupling_gear_ratio_motor_to_component: Quantity | None = None,
) -> dict[str, Quantity]:
    """Return layered rotational inertia breakdown at motor shaft."""
    try:
        reflected = (
            0.0
            if reflected_translating_mass_inertia is None
            else reflected_translating_mass_inertia.to(
                u.kilogram * u.meter**2
            ).magnitude
        )
        gearbox = (
            0.0
            if gearbox_inertia_at_motor_shaft is None
            else gearbox_inertia_at_motor_shaft.to(u.kilogram * u.meter**2).magnitude
        )
        pulley = (
            0.0
            if pulley_inertia_native is None
            else pulley_inertia_native.to(u.kilogram * u.meter**2).magnitude
        )
        pulley_ratio = (
            None
            if pulley_gear_ratio_motor_to_component is None
            else pulley_gear_ratio_motor_to_component.to(u.dimensionless).magnitude
        )
        ls_coupling = (
            0.0
            if low_speed_coupling_inertia_native is None
            else low_speed_coupling_inertia_native.to(u.kilogram * u.meter**2).magnitude
        )
        ls_coupling_ratio = (
            None
            if low_speed_coupling_gear_ratio_motor_to_component is None
            else low_speed_coupling_gear_ratio_motor_to_component.to(
                u.dimensionless
            ).magnitude
        )
        ls_brake = (
            0.0
            if low_speed_brake_inertia_native is None
            else low_speed_brake_inertia_native.to(u.kilogram * u.meter**2).magnitude
        )
        ls_brake_ratio = (
            None
            if low_speed_brake_gear_ratio_motor_to_component is None
            else low_speed_brake_gear_ratio_motor_to_component.to(
                u.dimensionless
            ).magnitude
        )
        hs_coupling = (
            0.0
            if high_speed_coupling_inertia_native is None
            else high_speed_coupling_inertia_native.to(
                u.kilogram * u.meter**2
            ).magnitude
        )
        hs_coupling_ratio = (
            None
            if high_speed_coupling_gear_ratio_motor_to_component is None
            else high_speed_coupling_gear_ratio_motor_to_component.to(
                u.dimensionless
            ).magnitude
        )
        hs_brake = (
            0.0
            if high_speed_brake_inertia_native is None
            else high_speed_brake_inertia_native.to(u.kilogram * u.meter**2).magnitude
        )
        hs_brake_ratio = (
            None
            if high_speed_brake_gear_ratio_motor_to_component is None
            else high_speed_brake_gear_ratio_motor_to_component.to(
                u.dimensionless
            ).magnitude
        )
        fluid = (
            0.0
            if fluid_coupling_inertia_native is None
            else fluid_coupling_inertia_native.to(u.kilogram * u.meter**2).magnitude
        )
        fluid_ratio = (
            None
            if fluid_coupling_gear_ratio_motor_to_component is None
            else fluid_coupling_gear_ratio_motor_to_component.to(
                u.dimensionless
            ).magnitude
        )
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    raw = _rotational_inertia_breakdown_at_motor_shaft(
        reflected_translating_mass_inertia_kg_m2=reflected,
        gearbox_inertia_at_motor_shaft_kg_m2=gearbox,
        pulley_inertia_native_kg_m2=pulley,
        pulley_gear_ratio_motor_to_component=pulley_ratio,
        low_speed_coupling_inertia_native_kg_m2=ls_coupling,
        low_speed_coupling_gear_ratio_motor_to_component=ls_coupling_ratio,
        low_speed_brake_inertia_native_kg_m2=ls_brake,
        low_speed_brake_gear_ratio_motor_to_component=ls_brake_ratio,
        high_speed_coupling_inertia_native_kg_m2=hs_coupling,
        high_speed_coupling_gear_ratio_motor_to_component=hs_coupling_ratio,
        high_speed_brake_inertia_native_kg_m2=hs_brake,
        high_speed_brake_gear_ratio_motor_to_component=hs_brake_ratio,
        fluid_coupling_inertia_native_kg_m2=fluid,
        fluid_coupling_gear_ratio_motor_to_component=fluid_ratio,
    )
    return {key: value * u.kilogram * u.meter**2 for key, value in raw.items()}


def motor_shaft_rotational_inertia_per_drive(
    total_motor_shaft_rotational_inertia: Quantity,
    motor_count: int,
    unit: str = "kilogram * meter**2",
    precision: int | None = None,
) -> Quantity:
    """Calculate per-drive motor-shaft rotational inertia.

    Parameters
    ----------
    total_motor_shaft_rotational_inertia : Quantity
        Total motor-shaft rotational inertia quantity.
    motor_count : int
        Number of drives sharing the inertia.
    unit : str, optional
        Output unit, by default ``"kilogram * meter**2"``.
    precision : int | None, optional
        Decimal rounding precision. Use ``None`` to skip rounding.

    Returns
    -------
    Quantity
        Per-drive motor-shaft rotational inertia in the requested output unit.

    Raises
    ------
    ValueError
        If unit conversion fails, physical constraints are violated, or the
        requested output unit is invalid.
    """
    try:
        total_inertia = total_motor_shaft_rotational_inertia.to(u.kilogram * u.meter**2)
    except Exception as exc:
        raise ValueError(f"Error in converting units: {exc}") from exc

    if total_inertia.magnitude < 0:
        raise ValueError("total_motor_shaft_rotational_inertia must be non-negative")
    if motor_count < 1:
        raise ValueError("motor_count must be >= 1")

    result = (
        _motor_shaft_rotational_inertia_per_drive(total_inertia.magnitude, motor_count)
        * u.kilogram
        * u.meter**2
    )
    converted = result.to(_parse_unit(unit))
    if precision is not None:
        converted = round(converted, precision)
    return converted
