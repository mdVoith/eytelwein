"""Private raw-float helpers for translating-mass and inertia calculations.

These functions intentionally operate on plain floats only. Unit conversion and
unit validation are handled by the public wrappers.
"""


def _translating_mass_from_line_load_and_segment_length(
    line_load_kg_per_m: float, segment_length_m: float
) -> float:
    """Calculate translating mass from line load and segment length.

    Parameters
    ----------
    line_load_kg_per_m : float
        Translating line load in kilogram per meter.
    segment_length_m : float
        Segment length in meters.

    Returns
    -------
    float
        Translating mass in kilograms.
    """
    return line_load_kg_per_m * segment_length_m


def _translating_mass_idler_carry(
    idler_carry_line_load_kg_per_m: float, segment_length_m: float
) -> float:
    """Calculate carry-idler translating mass.

    Parameters
    ----------
    idler_carry_line_load_kg_per_m : float
        Carry-idler translating line load in kilogram per meter.
    segment_length_m : float
        Conveyor segment length in meters.

    Returns
    -------
    float
        Carry-idler translating mass in kilograms.
    """
    return _translating_mass_from_line_load_and_segment_length(
        idler_carry_line_load_kg_per_m, segment_length_m
    )


def _translating_mass_idler_return(
    idler_return_line_load_kg_per_m: float, segment_length_m: float
) -> float:
    """Calculate return-idler translating mass.

    Parameters
    ----------
    idler_return_line_load_kg_per_m : float
        Return-idler translating line load in kilogram per meter.
    segment_length_m : float
        Conveyor segment length in meters.

    Returns
    -------
    float
        Return-idler translating mass in kilograms.
    """
    return _translating_mass_from_line_load_and_segment_length(
        idler_return_line_load_kg_per_m, segment_length_m
    )


def _translating_mass_belt(
    belt_line_load_kg_per_m: float, segment_length_m: float
) -> float:
    """Calculate belt translating mass for a given segment, which can be one or more strands, the entire belt or one single segment.

    Parameters
    ----------
    belt_line_load_kg_per_m : float
        Belt translating line load in kilogram per meter.
    segment_length_m : float
        Conveyor segment length in meters.

    Returns
    -------
    float
        Translating belt mass for the given segment in kilograms.
    """
    return _translating_mass_from_line_load_and_segment_length(
        belt_line_load_kg_per_m, segment_length_m
    )


def _translating_mass_material(
    material_line_load_kg_per_m: float, segment_length_m: float
) -> float:
    """Calculate material translating mass for a given segment or the entire conveyor.

    Parameters
    ----------
    material_line_load_kg_per_m : float
        Material translating line load in kilogram per meter.
    segment_length_m : float
        Conveyor segment length in meters.

    Returns
    -------
    float
        Translating material mass for the given segment in kilograms.
    """
    return _translating_mass_from_line_load_and_segment_length(
        material_line_load_kg_per_m, segment_length_m
    )


def _total_translating_mass_empty(
    translating_mass_idler_carry_kg: float,
    translating_mass_idler_return_kg: float,
    translating_mass_belt_carry_strand_kg: float,
    translating_mass_belt_return_strand_kg: float,
) -> float:
    """Calculate total translating mass for empty conveyor.

    Parameters
    ----------
    translating_mass_idler_carry_kg : float
        Carry-idler translating mass in kilograms.
    translating_mass_idler_return_kg : float
        Return-idler translating mass in kilograms.
    translating_mass_belt_carry_strand_kg : float
        Translating belt mass for the carry strand in kilograms.
    translating_mass_belt_return_strand_kg : float
        Translating belt mass for the return strand in kilograms.

    Returns
    -------
    float
        Empty-conveyor total translating mass in kilograms.

    Equation
    --------
    .. math::
        m_{total, empty} = m_{idler, carry} + m_{idler, return} + m_{belt, carry} + m_{belt, return}
    """
    return _total_translating_mass(
        translating_mass_idler_carry_kg=translating_mass_idler_carry_kg,
        translating_mass_idler_return_kg=translating_mass_idler_return_kg,
        translating_mass_belt_carry_strand_kg=translating_mass_belt_carry_strand_kg,
        translating_mass_belt_return_strand_kg=translating_mass_belt_return_strand_kg,
        translating_mass_material_kg=0.0,
    )


def _total_translating_mass(
    translating_mass_idler_carry_kg: float,
    translating_mass_idler_return_kg: float,
    translating_mass_belt_carry_strand_kg: float,
    translating_mass_belt_return_strand_kg: float,
    translating_mass_material_kg: float = 0.0,
) -> float:
    """Calculate total translating mass for a conveyor segment.

    Parameters
    ----------
    translating_mass_idler_carry_kg : float
        Carry-idler translating mass in kilograms.
    translating_mass_idler_return_kg : float
        Return-idler translating mass in kilograms.
    translating_mass_belt_carry_strand_kg : float
        Translating belt mass for the carry strand in kilograms.
    translating_mass_belt_return_strand_kg : float
        Translating belt mass for the return strand in kilograms.
    translating_mass_material_kg : float
        Translating material mass in kilograms, by default 0.0.

    Returns
    -------
    float
        Total translating mass in kilograms.

    Raises
    ------
    ValueError
        If any mass contribution is negative.
    """
    if translating_mass_idler_carry_kg < 0:
        raise ValueError("translating_mass_idler_carry_kg must be non-negative")
    if translating_mass_idler_return_kg < 0:
        raise ValueError("translating_mass_idler_return_kg must be non-negative")
    if translating_mass_belt_carry_strand_kg < 0:
        raise ValueError("translating_mass_belt_carry_strand_kg must be non-negative")
    if translating_mass_belt_return_strand_kg < 0:
        raise ValueError("translating_mass_belt_return_strand_kg must be non-negative")
    if translating_mass_material_kg < 0:
        raise ValueError("translating_mass_material_kg must be non-negative")
    return (
        translating_mass_idler_carry_kg
        + translating_mass_idler_return_kg
        + translating_mass_belt_carry_strand_kg
        + translating_mass_belt_return_strand_kg
        + translating_mass_material_kg
    )


def _total_translating_mass_loaded(
    translating_mass_idler_carry_kg: float,
    translating_mass_idler_return_kg: float,
    translating_mass_belt_carry_strand_kg: float,
    translating_mass_belt_return_strand_kg: float,
    translating_mass_material_kg: float,
) -> float:
    """Calculate total translating mass for loaded conveyor.

    This is a thin wrapper around :func:`_total_translating_mass` with
    explicit material contribution.
    """
    return _total_translating_mass(
        translating_mass_idler_carry_kg=translating_mass_idler_carry_kg,
        translating_mass_idler_return_kg=translating_mass_idler_return_kg,
        translating_mass_belt_carry_strand_kg=translating_mass_belt_carry_strand_kg,
        translating_mass_belt_return_strand_kg=translating_mass_belt_return_strand_kg,
        translating_mass_material_kg=translating_mass_material_kg,
    )


def _drive_pulley_radius_from_drive_pulley_diameter(
    drive_pulley_diameter_m: float,
) -> float:
    """Calculate drive pulley radius from drive pulley diameter.

    Parameters
    ----------
    drive_pulley_diameter_m : float
        Drive pulley diameter in meters.

    Returns
    -------
    float
        Drive pulley radius in meters.

    Raises
    ------
    ValueError
        If ``drive_pulley_diameter_m`` is not positive.
    """
    if drive_pulley_diameter_m <= 0:
        raise ValueError("drive_pulley_diameter_m must be positive")
    return drive_pulley_diameter_m / 2.0


def _translating_mass_inertia_at_pulley_circumference(
    translating_mass_kg: float, drive_pulley_radius_m: float
) -> float:
    """Calculate translating-mass inertia contribution at pulley circumference.

    Parameters
    ----------
    translating_mass_kg : float
        Total translating mass in kilograms.
    drive_pulley_radius_m : float
        Drive pulley radius in meters.

    Returns
    -------
    float
        Translating-mass inertia contribution at pulley circumference (low-speed side)
        in kilogram meter squared.

    Raises
    ------
    ValueError
        If mass is negative or radius is not positive.
    """
    if translating_mass_kg < 0:
        raise ValueError("translating_mass_kg must be non-negative")
    if drive_pulley_radius_m <= 0:
        raise ValueError("drive_pulley_radius_m must be positive")
    return translating_mass_kg * drive_pulley_radius_m * drive_pulley_radius_m


def _mass_inertia_at_pulley_shaft(
    translating_mass_kg: float,
    drive_pulley_radius_m: float,
    pulley_inertia_native_kg_m2: float = 0.0,
) -> float:
    """Calculate total inertia at pulley shaft from translating mass and native pulley inertia.

    Parameters
    ----------
    translating_mass_kg : float
        Total translating mass in kilograms.
    drive_pulley_radius_m : float
        Drive pulley radius in meters.
    pulley_inertia_native_kg_m2 : float, optional
        Native (inherent) pulley inertia in kilogram meter squared, by default 0.0.

    Returns
    -------
    float
        Total inertia at pulley shaft in kilogram meter squared.

    Raises
    ------
    ValueError
        If mass is negative, radius is not positive, or native pulley inertia is negative.
    """
    if pulley_inertia_native_kg_m2 < 0:
        raise ValueError("pulley_inertia_native_kg_m2 must be non-negative")

    translating_inertia = _translating_mass_inertia_at_pulley_circumference(
        translating_mass_kg, drive_pulley_radius_m
    )
    return translating_inertia + pulley_inertia_native_kg_m2


def _component_inertia_referred_to_motor_shaft(
    component_inertia_kg_m2: float, gear_ratio_motor_to_component: float
) -> float:
    """Convert native component inertia to motor-shaft-equivalent inertia.

    Parameters
    ----------
    component_inertia_kg_m2 : float
        Native component inertia in kilogram meter squared.
    gear_ratio_motor_to_component : float
        Gear ratio ``omega_motor / omega_component``.

    Returns
    -------
    float
        Component inertia referred to motor shaft in kilogram meter squared.

    Raises
    ------
    ValueError
        If inertia is negative or gear ratio is not positive.
    """
    if component_inertia_kg_m2 < 0:
        raise ValueError("component_inertia_kg_m2 must be non-negative")
    if gear_ratio_motor_to_component <= 0:
        raise ValueError("gear_ratio_motor_to_component must be positive")
    return component_inertia_kg_m2 / (
        gear_ratio_motor_to_component * gear_ratio_motor_to_component
    )


def _total_low_speed_inertia(
    mass_inertia_at_pulley_shaft_kg_m2: float,
    low_speed_coupling_inertia_kg_m2: float = 0.0,
    low_speed_brake_inertia_kg_m2: float = 0.0,
) -> float:
    """Calculate total low-speed-side inertia at pulley shaft.

    Sums mass inertia at pulley shaft plus optional low-speed coupling and
    brake inertias.

    Parameters
    ----------
    mass_inertia_at_pulley_shaft_kg_m2 : float
        Total inertia at pulley shaft in kilogram meter squared.
    low_speed_coupling_inertia_kg_m2 : float, optional
        Low-speed coupling inertia in kilogram meter squared, by default 0.0.
    low_speed_brake_inertia_kg_m2 : float, optional
        Low-speed brake inertia in kilogram meter squared, by default 0.0.

    Returns
    -------
    float
        Total low-speed-side inertia in kilogram meter squared.

    Raises
    ------
    ValueError
        If any inertia contribution is negative.
    """
    if mass_inertia_at_pulley_shaft_kg_m2 < 0:
        raise ValueError("mass_inertia_at_pulley_shaft_kg_m2 must be non-negative")
    if low_speed_coupling_inertia_kg_m2 < 0:
        raise ValueError("low_speed_coupling_inertia_kg_m2 must be non-negative")
    if low_speed_brake_inertia_kg_m2 < 0:
        raise ValueError("low_speed_brake_inertia_kg_m2 must be non-negative")
    return (
        mass_inertia_at_pulley_shaft_kg_m2
        + low_speed_coupling_inertia_kg_m2
        + low_speed_brake_inertia_kg_m2
    )


def _fluid_coupling_design_inertia(
    total_low_speed_inertia_kg_m2: float,
    gearbox_ratio_motor_to_low_speed_side: float,
    high_speed_coupling_inertia_kg_m2: float = 0.0,
    high_speed_brake_inertia_kg_m2: float = 0.0,
    gearbox_inertia_kg_m2: float = 0.0,
    flywheel_inertia_kg_m2: float = 0.0,
) -> float:
    """Calculate fluid-coupling design inertia from low-speed total and gearbox ratio.

    Reflects total low-speed inertia to motor shaft via gearbox ratio, then sums
    with high-speed components (coupling, brake, gearbox, flywheel).

    Parameters
    ----------
    total_low_speed_inertia_kg_m2 : float
        Total low-speed-side inertia in kilogram meter squared.
    gearbox_ratio_motor_to_low_speed_side : float
        Gearbox ratio ``omega_motor / omega_low_speed_side``.
    high_speed_coupling_inertia_kg_m2 : float, optional
        High-speed coupling inertia in kilogram meter squared, by default 0.0.
    high_speed_brake_inertia_kg_m2 : float, optional
        High-speed brake inertia in kilogram meter squared, by default 0.0.
    gearbox_inertia_kg_m2 : float, optional
        Gearbox inertia (high-speed side) in kilogram meter squared, by default 0.0.
    flywheel_inertia_kg_m2 : float, optional
        Flywheel inertia in kilogram meter squared, by default 0.0.

    Returns
    -------
    float
        Fluid-coupling design inertia in kilogram meter squared.

    Raises
    ------
    ValueError
        If any inertia is negative or gearbox ratio is not positive.
    """
    # Delegate to canonical single-drive helper with quantity=1 and motor-side terms zeroed
    return _total_inertia_for_single_drive(
        total_low_speed_inertia_kg_m2=total_low_speed_inertia_kg_m2,
        quantity_of_drives=1,
        gearbox_ratio_motor_to_low_speed_side=gearbox_ratio_motor_to_low_speed_side,
        high_speed_coupling_inertia_kg_m2=high_speed_coupling_inertia_kg_m2,
        high_speed_brake_inertia_kg_m2=high_speed_brake_inertia_kg_m2,
        gearbox_inertia_kg_m2=gearbox_inertia_kg_m2,
        flywheel_inertia_kg_m2=flywheel_inertia_kg_m2,
        fluid_coupling_inertia_kg_m2=0.0,
        motor_coupling_inertia_kg_m2=0.0,
        motor_inertia_kg_m2=0.0,
    )


def _total_inertia_for_single_drive(
    total_low_speed_inertia_kg_m2: float,
    quantity_of_drives: int,
    gearbox_ratio_motor_to_low_speed_side: float,
    high_speed_coupling_inertia_kg_m2: float = 0.0,
    high_speed_brake_inertia_kg_m2: float = 0.0,
    gearbox_inertia_kg_m2: float = 0.0,
    flywheel_inertia_kg_m2: float = 0.0,
    fluid_coupling_inertia_kg_m2: float = 0.0,
    motor_coupling_inertia_kg_m2: float = 0.0,
    motor_inertia_kg_m2: float = 0.0,
) -> float:
    """Calculate per-drive total inertia from shared low-speed and single-drive motor-side components.

    Reflects total low-speed inertia to motor shaft via gearbox ratio, divides by quantity_of_drives
    (to apportion the shared inertia across parallel drives), then adds optional single-drive
    high-speed and motor-side inertias.

    Parameters
    ----------
    total_low_speed_inertia_kg_m2 : float
        Total low-speed-side inertia in kilogram meter squared.
    quantity_of_drives : int
        Number of drives sharing the low-speed inertia. Must be >= 1.
    gearbox_ratio_motor_to_low_speed_side : float
        Gearbox ratio ``omega_motor / omega_low_speed_side``.
    high_speed_coupling_inertia_kg_m2 : float, optional
        High-speed coupling inertia (single drive) in kilogram meter squared, by default 0.0.
    high_speed_brake_inertia_kg_m2 : float, optional
        High-speed brake inertia (single drive) in kilogram meter squared, by default 0.0.
    gearbox_inertia_kg_m2 : float, optional
        Gearbox inertia on high-speed side (single drive) in kilogram meter squared, by default 0.0.
    flywheel_inertia_kg_m2 : float, optional
        Flywheel inertia (single drive) in kilogram meter squared, by default 0.0.
    fluid_coupling_inertia_kg_m2 : float, optional
        Fluid-coupling inertia (single drive) in kilogram meter squared, by default 0.0.
    motor_coupling_inertia_kg_m2 : float, optional
        Motor coupling inertia (single drive) in kilogram meter squared, by default 0.0.
    motor_inertia_kg_m2 : float, optional
        Motor inertia (single drive) in kilogram meter squared, by default 0.0.

    Returns
    -------
    float
        Per-drive total inertia in kilogram meter squared.

    Raises
    ------
    ValueError
        If any inertia is negative, quantity_of_drives is < 1, or gearbox ratio is not positive.
    """
    # Validate inputs
    if isinstance(quantity_of_drives, bool):
        raise ValueError("quantity_of_drives must be int, not bool")
    if not isinstance(quantity_of_drives, int):
        raise ValueError("quantity_of_drives must be int")
    if total_low_speed_inertia_kg_m2 < 0:
        raise ValueError("total_low_speed_inertia_kg_m2 must be non-negative")
    if quantity_of_drives < 1:
        raise ValueError("quantity_of_drives must be >= 1")
    if gearbox_ratio_motor_to_low_speed_side <= 0:
        raise ValueError("gearbox_ratio_motor_to_low_speed_side must be positive")
    if high_speed_coupling_inertia_kg_m2 < 0:
        raise ValueError("high_speed_coupling_inertia_kg_m2 must be non-negative")
    if high_speed_brake_inertia_kg_m2 < 0:
        raise ValueError("high_speed_brake_inertia_kg_m2 must be non-negative")
    if gearbox_inertia_kg_m2 < 0:
        raise ValueError("gearbox_inertia_kg_m2 must be non-negative")
    if flywheel_inertia_kg_m2 < 0:
        raise ValueError("flywheel_inertia_kg_m2 must be non-negative")
    if fluid_coupling_inertia_kg_m2 < 0:
        raise ValueError("fluid_coupling_inertia_kg_m2 must be non-negative")
    if motor_coupling_inertia_kg_m2 < 0:
        raise ValueError("motor_coupling_inertia_kg_m2 must be non-negative")
    if motor_inertia_kg_m2 < 0:
        raise ValueError("motor_inertia_kg_m2 must be non-negative")

    # Reflect low-speed inertia to motor shaft
    reflected = _component_inertia_referred_to_motor_shaft(
        total_low_speed_inertia_kg_m2, gearbox_ratio_motor_to_low_speed_side
    )

    # Divide reflected shared inertia by quantity of drives
    reflected_per_drive = reflected / quantity_of_drives

    # Sum all components: shared reflected (divided) + single-drive high-speed + single-drive motor-side
    return (
        reflected_per_drive
        + high_speed_coupling_inertia_kg_m2
        + high_speed_brake_inertia_kg_m2
        + gearbox_inertia_kg_m2
        + flywheel_inertia_kg_m2
        + fluid_coupling_inertia_kg_m2
        + motor_coupling_inertia_kg_m2
        + motor_inertia_kg_m2
    )
