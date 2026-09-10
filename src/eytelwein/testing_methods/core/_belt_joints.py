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
