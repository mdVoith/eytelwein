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
    """Calculate belt translating mass for one strand.

    Parameters
    ----------
    belt_line_load_kg_per_m : float
        Belt translating line load in kilogram per meter.
    segment_length_m : float
        Conveyor segment length in meters.

    Returns
    -------
    float
        Translating belt mass for one strand in kilograms.
    """
    return _translating_mass_from_line_load_and_segment_length(
        belt_line_load_kg_per_m, segment_length_m
    )


def _translating_mass_material(
    material_line_load_kg_per_m: float, segment_length_m: float
) -> float:
    """Calculate material translating mass.

    Parameters
    ----------
    material_line_load_kg_per_m : float
        Material translating line load in kilogram per meter.
    segment_length_m : float
        Conveyor segment length in meters.

    Returns
    -------
    float
        Translating material mass in kilograms.
    """
    return _translating_mass_from_line_load_and_segment_length(
        material_line_load_kg_per_m, segment_length_m
    )


def _total_translating_mass_empty(
    translating_mass_idler_carry_kg: float,
    translating_mass_idler_return_kg: float,
    translating_mass_belt_per_strand_kg: float,
) -> float:
    """Calculate total translating mass for empty conveyor.

    Parameters
    ----------
    translating_mass_idler_carry_kg : float
        Carry-idler translating mass in kilograms.
    translating_mass_idler_return_kg : float
        Return-idler translating mass in kilograms.
    translating_mass_belt_per_strand_kg : float
        Translating belt mass per strand in kilograms.

    Returns
    -------
    float
        Empty-conveyor total translating mass in kilograms.
    """
    return (
        translating_mass_idler_carry_kg
        + translating_mass_idler_return_kg
        + 2.0 * translating_mass_belt_per_strand_kg
    )


def _total_translating_mass(
    total_translating_mass_empty_kg: float, translating_mass_material_kg: float
) -> float:
    """Calculate total translating mass for loaded conveyor.

    Parameters
    ----------
    total_translating_mass_empty_kg : float
        Empty-conveyor total translating mass in kilograms.
    translating_mass_material_kg : float
        Translating material mass in kilograms.

    Returns
    -------
    float
        Loaded-conveyor total translating mass in kilograms.
    """
    return total_translating_mass_empty_kg + translating_mass_material_kg


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


def _translating_mass_inertia_at_pulley_shaft(
    translating_mass_kg: float, drive_pulley_radius_m: float
) -> float:
    """Calculate translating-mass inertia contribution at pulley shaft.

    Parameters
    ----------
    translating_mass_kg : float
        Total translating mass in kilograms.
    drive_pulley_radius_m : float
        Drive pulley radius in meters.

    Returns
    -------
    float
        Translating-mass inertia contribution at pulley shaft (low-speed side)
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


def _reflected_translating_mass_inertia_at_motor_shaft(
    translating_mass_kg: float,
    drive_pulley_radius_m: float,
    gear_ratio_motor_to_pulley: float,
) -> float:
    """Calculate reflected translating-mass inertia contribution at motor shaft.

    This function converts pulley-shaft inertia to motor-shaft-equivalent inertia
    by applying the squared speed ratio. It composes two primitives:
    (1) translating mass → pulley-shaft inertia
    (2) pulley-shaft inertia → motor-shaft inertia via speed reduction

    Parameters
    ----------
    translating_mass_kg : float
        Total translating mass in kilograms.
    drive_pulley_radius_m : float
        Drive pulley radius in meters.
    gear_ratio_motor_to_pulley : float
        Gear ratio ``omega_motor / omega_pulley``.

    Returns
    -------
    float
        Reflected translating-mass inertia contribution at motor shaft in
        kilogram meter squared.

    Raises
    ------
    ValueError
        If mass is negative, radius is not positive, or gear ratio is not
        positive.
    """
    if translating_mass_kg < 0:
        raise ValueError("translating_mass_kg must be non-negative")
    if drive_pulley_radius_m <= 0:
        raise ValueError("drive_pulley_radius_m must be positive")
    if gear_ratio_motor_to_pulley <= 0:
        raise ValueError("gear_ratio_motor_to_pulley must be positive")

    pulley_inertia = _translating_mass_inertia_at_pulley_shaft(
        translating_mass_kg, drive_pulley_radius_m
    )
    return _component_inertia_referred_to_motor_shaft(
        pulley_inertia, gear_ratio_motor_to_pulley
    )


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


def _total_motor_shaft_rotational_inertia_from_equivalent_component_inertias(
    reflected_translating_mass_inertia_kg_m2: float,
    gearbox_inertia_at_motor_shaft_kg_m2: float,
    coupling_inertia_at_motor_shaft_kg_m2: float,
    brake_inertia_at_motor_shaft_kg_m2: float,
) -> float:
    """Sum all motor-shaft-equivalent rotational inertia contributions.

    Parameters
    ----------
    reflected_translating_mass_inertia_kg_m2 : float
        Reflected translating-mass inertia at motor shaft in kilogram meter
        squared.
    gearbox_inertia_at_motor_shaft_kg_m2 : float
        Gearbox inertia already referred to motor shaft in kilogram meter
        squared.
    coupling_inertia_at_motor_shaft_kg_m2 : float
        Coupling inertia already referred to motor shaft in kilogram meter
        squared.
    brake_inertia_at_motor_shaft_kg_m2 : float
        Brake inertia already referred to motor shaft in kilogram meter
        squared.

    Returns
    -------
    float
        Total motor-shaft rotational inertia in kilogram meter squared.

    Raises
    ------
    ValueError
        If any inertia contribution is negative.
    """
    if reflected_translating_mass_inertia_kg_m2 < 0:
        raise ValueError(
            "reflected_translating_mass_inertia_kg_m2 must be non-negative"
        )
    if gearbox_inertia_at_motor_shaft_kg_m2 < 0:
        raise ValueError("gearbox_inertia_at_motor_shaft_kg_m2 must be non-negative")
    if coupling_inertia_at_motor_shaft_kg_m2 < 0:
        raise ValueError("coupling_inertia_at_motor_shaft_kg_m2 must be non-negative")
    if brake_inertia_at_motor_shaft_kg_m2 < 0:
        raise ValueError("brake_inertia_at_motor_shaft_kg_m2 must be non-negative")
    return (
        reflected_translating_mass_inertia_kg_m2
        + gearbox_inertia_at_motor_shaft_kg_m2
        + coupling_inertia_at_motor_shaft_kg_m2
        + brake_inertia_at_motor_shaft_kg_m2
    )


def _total_motor_shaft_rotational_inertia_from_native_component_inertias(
    reflected_translating_mass_inertia_kg_m2: float,
    gearbox_inertia_native_kg_m2: float,
    gearbox_gear_ratio_motor_to_component: float,
    coupling_inertia_native_kg_m2: float,
    coupling_gear_ratio_motor_to_component: float,
    brake_inertia_native_kg_m2: float,
    brake_gear_ratio_motor_to_component: float,
) -> float:
    """Sum translating inertia and native component inertias at motor shaft.

    Parameters
    ----------
    reflected_translating_mass_inertia_kg_m2 : float
        Reflected translating-mass inertia at motor shaft in kilogram meter
        squared.
    gearbox_inertia_native_kg_m2 : float
        Native gearbox inertia in kilogram meter squared.
    gearbox_gear_ratio_motor_to_component : float
        Gear ratio ``omega_motor / omega_gearbox``.
    coupling_inertia_native_kg_m2 : float
        Native coupling inertia in kilogram meter squared.
    coupling_gear_ratio_motor_to_component : float
        Gear ratio ``omega_motor / omega_coupling``.
    brake_inertia_native_kg_m2 : float
        Native brake inertia in kilogram meter squared.
    brake_gear_ratio_motor_to_component : float
        Gear ratio ``omega_motor / omega_brake``.

    Returns
    -------
    float
        Total motor-shaft rotational inertia in kilogram meter squared.
    """
    return _total_motor_shaft_rotational_inertia_from_equivalent_component_inertias(
        reflected_translating_mass_inertia_kg_m2,
        _component_inertia_referred_to_motor_shaft(
            gearbox_inertia_native_kg_m2, gearbox_gear_ratio_motor_to_component
        ),
        _component_inertia_referred_to_motor_shaft(
            coupling_inertia_native_kg_m2, coupling_gear_ratio_motor_to_component
        ),
        _component_inertia_referred_to_motor_shaft(
            brake_inertia_native_kg_m2, brake_gear_ratio_motor_to_component
        ),
    )


def _motor_shaft_rotational_inertia_per_drive(
    total_motor_shaft_rotational_inertia_kg_m2: float, motor_count: int
) -> float:
    """Calculate per-drive motor-shaft rotational inertia.

    Parameters
    ----------
    total_motor_shaft_rotational_inertia_kg_m2 : float
        Total motor-shaft rotational inertia in kilogram meter squared.
    motor_count : int
        Number of motors sharing the rotational inertia.

    Returns
    -------
    float
        Per-drive motor-shaft rotational inertia in kilogram meter squared.

    Raises
    ------
    ValueError
        If total inertia is negative or ``motor_count`` is less than 1.
    """
    if total_motor_shaft_rotational_inertia_kg_m2 < 0:
        raise ValueError(
            "total_motor_shaft_rotational_inertia_kg_m2 must be non-negative"
        )
    if motor_count < 1:
        raise ValueError("motor_count must be >= 1")
    return total_motor_shaft_rotational_inertia_kg_m2 / motor_count
