"""Private raw-float helpers for translating-mass motor-shaft inertia.

These functions intentionally operate on plain floats only. Unit conversion and
unit validation are handled by the public wrappers.
"""


def belt_mass_per_strand(
    belt_linear_mass_kg_per_m: float, center_distance_m: float
) -> float:
    """Calculate belt mass for one strand.

    Parameters
    ----------
    belt_linear_mass_kg_per_m : float
        Belt linear mass in kilogram per meter.
    center_distance_m : float
        Conveyor center distance in meters.

    Returns
    -------
    float
        Belt mass per strand in kilograms.
    """
    return belt_linear_mass_kg_per_m * center_distance_m


def payload_mass_total(
    payload_mass_per_meter_kg_per_m: float, center_distance_m: float
) -> float:
    """Calculate total payload mass over conveyor center distance.

    Parameters
    ----------
    payload_mass_per_meter_kg_per_m : float
        Payload mass per meter in kilogram per meter.
    center_distance_m : float
        Conveyor center distance in meters.

    Returns
    -------
    float
        Total payload mass in kilograms.
    """
    return payload_mass_per_meter_kg_per_m * center_distance_m


def translating_mass_empty(
    idler_mass_upper_total_kg: float,
    idler_mass_lower_total_kg: float,
    belt_mass_per_strand_kg: float,
) -> float:
    """Calculate translating mass for empty conveyor.

    Parameters
    ----------
    idler_mass_upper_total_kg : float
        Total upper-strand idler mass in kilograms.
    idler_mass_lower_total_kg : float
        Total lower-strand idler mass in kilograms.
    belt_mass_per_strand_kg : float
        Belt mass of one strand in kilograms.

    Returns
    -------
    float
        Empty-conveyor translating mass in kilograms.
    """
    return (
        idler_mass_upper_total_kg
        + idler_mass_lower_total_kg
        + 2.0 * belt_mass_per_strand_kg
    )


def translating_mass_full(
    translating_mass_empty_kg: float, payload_mass_total_kg: float
) -> float:
    """Calculate translating mass for loaded conveyor.

    Parameters
    ----------
    translating_mass_empty_kg : float
        Empty-conveyor translating mass in kilograms.
    payload_mass_total_kg : float
        Total payload mass in kilograms.

    Returns
    -------
    float
        Full-conveyor translating mass in kilograms.
    """
    return translating_mass_empty_kg + payload_mass_total_kg


def pulley_radius(drive_pulley_diameter_m: float) -> float:
    """Calculate pulley radius from pulley diameter.

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


def motor_shaft_inertia_total(
    translating_mass_kg: float,
    drive_pulley_radius_m: float,
    gear_ratio_motor_to_pulley: float,
) -> float:
    """Calculate reflected total inertia at motor shaft.

    Parameters
    ----------
    translating_mass_kg : float
        Translating mass in kilograms.
    drive_pulley_radius_m : float
        Drive pulley radius in meters.
    gear_ratio_motor_to_pulley : float
        Gear ratio defined as ``omega_motor / omega_pulley``.

    Returns
    -------
    float
        Total reflected inertia at motor shaft in kilogram meter squared.

    Raises
    ------
    ValueError
        If radius or gear ratio is not positive, or mass is negative.
    """
    if translating_mass_kg < 0:
        raise ValueError("translating_mass_kg must be non-negative")
    if drive_pulley_radius_m <= 0:
        raise ValueError("drive_pulley_radius_m must be positive")
    if gear_ratio_motor_to_pulley <= 0:
        raise ValueError("gear_ratio_motor_to_pulley must be positive")
    return (
        translating_mass_kg
        * drive_pulley_radius_m
        * drive_pulley_radius_m
        / (gear_ratio_motor_to_pulley * gear_ratio_motor_to_pulley)
    )


def inertia_per_drive(
    inertia_total_motor_shaft_kg_m2: float, motor_count: int
) -> float:
    """Calculate per-drive reflected inertia at motor shaft.

    Parameters
    ----------
    inertia_total_motor_shaft_kg_m2 : float
        Total reflected inertia at motor shaft in kilogram meter squared.
    motor_count : int
        Number of motors sharing the load.

    Returns
    -------
    float
        Per-drive reflected inertia in kilogram meter squared.

    Raises
    ------
    ValueError
        If ``inertia_total_motor_shaft_kg_m2`` is negative or ``motor_count`` is
        less than 1.
    """
    if inertia_total_motor_shaft_kg_m2 < 0:
        raise ValueError("inertia_total_motor_shaft_kg_m2 must be non-negative")
    if motor_count < 1:
        raise ValueError("motor_count must be >= 1")
    return inertia_total_motor_shaft_kg_m2 / motor_count
