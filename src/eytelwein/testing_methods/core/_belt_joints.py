def _nominal_breaking_strength_of_textile_belt_specimen(
    belt_width_mm: float, tension_coefficient_n_per_mm: float
) -> float:
    """
    Calculate the nominal breaking strength of a textile belt specimen.

    Parameters
    ----------
    belt_width_mm : float
        The width of the textile belt specimen in millimeters.
    tension_coefficient_n_per_mm : float
        The tension coefficient in Newtons per millimeter (N/mm).

    Returns
    -------
    float
        The nominal breaking strength in kilonewtons (kN).

    Notes
    -----
    Formula: F_B = b * k_N / 1000
    where:
        F_B = breaking strength (kN)
        b = belt width (mm)
        k_N = tension coefficient (N/mm)
    """
    breaking_strength_n = belt_width_mm * tension_coefficient_n_per_mm
    breaking_strength_kn = breaking_strength_n / 1000.0
    return breaking_strength_kn


def _specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
    nominal_breaking_strength_kn: float,
    width_related_nominal_breaking_tension_n_per_mm: float,
) -> float:
    """
    Calculate specimen width from breaking strength and tension coefficient (private inverse).

    Parameters
    ----------
    nominal_breaking_strength_kn : float
        The nominal breaking strength in kilonewtons (kN).
    width_related_nominal_breaking_tension_n_per_mm : float
        The tension coefficient in Newtons per millimeter (N/mm).

    Returns
    -------
    float
        The specimen width in millimeters.

    Raises
    ------
    ValueError
        If width_related_nominal_breaking_tension_n_per_mm is zero or negative,
        preventing division by zero or physically invalid results.

    Notes
    -----
    Inverse formula: b = 1000 * F_B / k_N
    where:
        b = specimen width (mm)
        F_B = breaking strength (kN)
        k_N = tension coefficient (N/mm)
    """
    # Guard against division by zero and invalid denominator
    if width_related_nominal_breaking_tension_n_per_mm <= 0:
        raise ValueError(
            f"width_related_nominal_breaking_tension_n_per_mm must be positive, "
            f"got {width_related_nominal_breaking_tension_n_per_mm}."
        )

    specimen_width_mm = (
        1000.0
        * nominal_breaking_strength_kn
        / width_related_nominal_breaking_tension_n_per_mm
    )
    return specimen_width_mm


def _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
    nominal_breaking_strength_kn: float, specimen_width_mm: float
) -> float:
    """
    Calculate tension coefficient from breaking strength and specimen width (private inverse).

    Parameters
    ----------
    nominal_breaking_strength_kn : float
        The nominal breaking strength in kilonewtons (kN).
    specimen_width_mm : float
        The width of the textile belt specimen in millimeters.

    Returns
    -------
    float
        The tension coefficient in Newtons per millimeter (N/mm).

    Raises
    ------
    ValueError
        If specimen_width_mm is zero or negative, preventing division by zero
        or physically invalid results.

    Notes
    -----
    Inverse formula: k_N = 1000 * F_B / b
    where:
        k_N = tension coefficient (N/mm)
        F_B = breaking strength (kN)
        b = specimen width (mm)
    """
    # Guard against division by zero and invalid denominator
    if specimen_width_mm <= 0:
        raise ValueError(
            f"specimen_width_mm must be positive, got {specimen_width_mm}."
        )

    tension_coefficient_n_per_mm = (
        1000.0 * nominal_breaking_strength_kn / specimen_width_mm
    )
    return tension_coefficient_n_per_mm
