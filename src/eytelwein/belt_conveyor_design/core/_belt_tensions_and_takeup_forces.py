"""Private calculations for belt tensions and takeup forces.

This module groups magnitude-only helper functions for belt-tension and
takeup-force calculations. Each private function implements one specific
formula while leaving unit handling, public validation, and output
formatting to the corresponding public module.
"""

from eytelwein.main.constants import STANDARD_GRAVITY_VALUE


def _minimum_belt_tension_from_sag_carry(
    line_load_belt_kg_per_m: float,
    line_load_material_kg_per_m: float,
    idler_spacing_m: float,
    allowable_sag: float,
) -> float:
    """
    Calculate minimum belt tension from sag during carry run (private implementation).

    Parameters
    ----------
    line_load_belt_kg_per_m : float
        Belt line load (mass per unit length) in kg/m.
    line_load_material_kg_per_m : float
        Material line load (mass per unit length) in kg/m.
    idler_spacing_m : float
        Distance between consecutive idlers in meters.
    allowable_sag : float
        Allowable sag as a dimensionless fraction of idler spacing
        (e.g., 0.01 for 1%).

    Returns
    -------
    float
        Minimum belt tension in Newtons.

    Raises
    ------
    ValueError
        If allowable_sag <= 0, preventing division by zero or
        physically meaningless results.

    Notes
    -----
    The private function only prevents mathematical division errors,
    allowing zero or negative loads (which may be pre-validated elsewhere).
    """
    # Guard against division by zero and physically invalid sag
    if allowable_sag <= 0:
        raise ValueError(f"allowable_sag must be positive, got {allowable_sag}.")

    # Combined line load
    combined_load = line_load_belt_kg_per_m + line_load_material_kg_per_m

    # Calculate minimum tension: T = (q_B + q_G) * g * l_o / (8 * f_sag)
    tension = (combined_load * STANDARD_GRAVITY_VALUE * idler_spacing_m) / (
        8 * allowable_sag
    )

    return tension


def _takeup_weight_force_from_takeup_weight(takeup_weight_kg: float) -> float:
    """
    Calculate takeup weight force from takeup weight (private implementation).

    Parameters
    ----------
    takeup_weight_kg : float
        Takeup weight in kilograms.

    Returns
    -------
    float
        Takeup weight force in Newtons.

    Notes
    -----
    Converts mass to force using the formula:
    F [N] = m [kg] * g [m/s²]

    where g is STANDARD_GRAVITY_VALUE (9.80665 m/s²).

    Pure gravity conversion without reeving.
    """
    force = takeup_weight_kg * STANDARD_GRAVITY_VALUE
    return force


def _takeup_weight_from_takeup_weight_force(takeup_weight_force_n: float) -> float:
    """
    Calculate takeup weight from takeup weight force (private implementation).

    Parameters
    ----------
    takeup_weight_force_n : float
        Takeup weight force in Newtons.

    Returns
    -------
    float
        Takeup weight in kilograms.

    Notes
    -----
    Converts force to mass using the formula:
    m [kg] = F [N] / g [m/s²]

    where g is STANDARD_GRAVITY_VALUE (9.80665 m/s²).

    Pure gravity conversion without reeving.
    """
    weight = takeup_weight_force_n / STANDARD_GRAVITY_VALUE
    return weight


def _effort_force_from_load_force(load_force_n: float, strand_count: int = 1) -> float:
    """
    Calculate effort force from load force using ideal reeving (private implementation).

    Parameters
    ----------
    load_force_n : float
        Load force in Newtons.
    strand_count : int, optional
        Number of strands in ideal reeving system (default: 1).
        Must be a positive integer >= 1.

    Returns
    -------
    float
        Effort force in Newtons.

    Raises
    ------
    ValueError
        If strand_count <= 0, preventing division by zero
        and enforcing physically valid reeving configurations.

    Notes
    -----
    Converts load force to effort force using the formula:
    F_effort [N] = F_load [N] / strand_count

    For ideal reeving, the force is distributed equally across
    all strands, so strand_count > 1 reduces the required effort force.
    """
    # Guard against division by zero and invalid strand count
    if strand_count <= 0:
        raise ValueError(
            f"strand_count must be a positive integer >= 1, got {strand_count}."
        )

    effort = load_force_n / strand_count
    return effort


def _load_force_from_effort_force(
    effort_force_n: float, strand_count: int = 1
) -> float:
    """
    Calculate load force from effort force using ideal reeving (private implementation).

    Parameters
    ----------
    effort_force_n : float
        Effort force in Newtons.
    strand_count : int, optional
        Number of strands in ideal reeving system (default: 1).
        Must be a positive integer >= 1.

    Returns
    -------
    float
        Load force in Newtons.

    Raises
    ------
    ValueError
        If strand_count <= 0, preventing division by zero
        and enforcing physically valid reeving configurations.

    Notes
    -----
    Converts effort force to load force using the formula:
    F_load [N] = F_effort [N] * strand_count

    For ideal reeving, the effort force is multiplied by the strand count
    to calculate the total load force.
    """
    # Guard against division by zero and invalid strand count
    if strand_count <= 0:
        raise ValueError(
            f"strand_count must be a positive integer >= 1, got {strand_count}."
        )

    load = effort_force_n * strand_count
    return load


def _rope_travel_from_takeup_travel(
    takeup_travel_m: float, strand_count: int = 1
) -> float:
    """
    Calculate rope travel from takeup travel (private implementation).

    Parameters
    ----------
    takeup_travel_m : float
        Takeup travel distance in meters.
    strand_count : int, optional
        Number of strands in ideal reeving system (default: 1).
        Must be a positive integer >= 1.

    Returns
    -------
    float
        Rope travel distance in meters.

    Raises
    ------
    ValueError
        If strand_count <= 0, preventing division by zero
        and enforcing physically valid reeving configurations.

    Notes
    -----
    Converts takeup travel to rope travel using the formula:
    rope_travel [m] = takeup_travel [m] * strand_count

    For ideal reeving, the rope travels a distance equal to the takeup
    travel multiplied by the strand count.
    """
    # Guard against division by zero and invalid strand count
    if strand_count <= 0:
        raise ValueError(
            f"strand_count must be a positive integer >= 1, got {strand_count}."
        )

    travel = takeup_travel_m * strand_count
    return travel


def _takeup_travel_from_rope_travel(
    rope_travel_m: float, strand_count: int = 1
) -> float:
    """
    Calculate takeup travel from rope travel (private implementation).

    Parameters
    ----------
    rope_travel_m : float
        Rope travel distance in meters.
    strand_count : int, optional
        Number of strands in ideal reeving system (default: 1).
        Must be a positive integer >= 1.

    Returns
    -------
    float
        Takeup travel distance in meters.

    Raises
    ------
    ValueError
        If strand_count <= 0, preventing division by zero
        and enforcing physically valid reeving configurations.

    Notes
    -----
    Converts rope travel to takeup travel using the formula:
    takeup_travel [m] = rope_travel [m] / strand_count

    For ideal reeving, the takeup travel is the rope travel divided
    by the strand count.
    """
    # Guard against division by zero and invalid strand count
    if strand_count <= 0:
        raise ValueError(
            f"strand_count must be a positive integer >= 1, got {strand_count}."
        )

    travel = rope_travel_m / strand_count
    return travel
