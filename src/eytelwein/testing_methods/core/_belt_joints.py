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
    Formula: T_breaking = b * T_nominal_tension / 1000
    where:
        T_breaking = breaking strength (kN)
        b = belt width (mm)
        T_nominal_tension = tension coefficient (N/mm)
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
    Inverse formula: b = 1000 * T_breaking / T_nominal_tension
    where:
        b = specimen width (mm)
        T_breaking = breaking strength (kN)
        T_nominal_tension = tension coefficient (N/mm)
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
    Inverse formula: T_nominal_tension = 1000 * T_breaking / b
    where:
        T_nominal_tension = tension coefficient (N/mm)
        T_breaking = breaking strength (kN)
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


def _relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
    reference_upper_load_kn: float,
    nominal_breaking_strength_of_specimen_kn: float,
) -> float:
    """
    Calculate relative reference splice efficiency from reference upper load and nominal breaking strength.

    Parameters
    ----------
    reference_upper_load_kn : float
        The reference upper load in kilonewtons (kN).
    nominal_breaking_strength_of_specimen_kn : float
        The nominal breaking strength of the specimen in kilonewtons (kN).

    Returns
    -------
    float
        The relative reference splice efficiency in percent.

    Raises
    ------
    ValueError
        If nominal_breaking_strength_of_specimen_kn is zero or negative,
        preventing division by zero or physically invalid results.

    Notes
    -----
    Formula: T_rel_fatigue = T_upper / T_breaking * 100
    where:
        T_rel_fatigue = relative reference splice efficiency (%)
        T_upper = reference upper load (kN)
        T_breaking = nominal breaking strength of specimen (kN)
    """
    # Guard against division by zero and invalid denominator
    if nominal_breaking_strength_of_specimen_kn <= 0:
        raise ValueError(
            f"nominal_breaking_strength_of_specimen_kn must be positive, "
            f"got {nominal_breaking_strength_of_specimen_kn}."
        )

    relative_reference_splice_efficiency_percent = (
        reference_upper_load_kn / nominal_breaking_strength_of_specimen_kn * 100.0
    )
    return relative_reference_splice_efficiency_percent


def _reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
    relative_reference_splice_efficiency_percent: float,
    nominal_breaking_strength_of_specimen_kn: float,
) -> float:
    """
    Calculate reference upper load from relative reference splice efficiency and nominal breaking strength.

    Parameters
    ----------
    relative_reference_splice_efficiency_percent : float
        The relative reference splice efficiency in percent.
    nominal_breaking_strength_of_specimen_kn : float
        The nominal breaking strength of the specimen in kilonewtons (kN).

    Returns
    -------
    float
        The reference upper load in kilonewtons (kN).

    Notes
    -----
    Inverse formula: T_upper = T_rel_fatigue / 100 * T_breaking
    where:
        T_upper = reference upper load (kN)
        T_rel_fatigue = relative reference splice efficiency (%)
        T_breaking = nominal breaking strength of specimen (kN)
    """
    reference_upper_load_kn = (
        relative_reference_splice_efficiency_percent
        / 100.0
        * nominal_breaking_strength_of_specimen_kn
    )
    return reference_upper_load_kn


def _nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
    reference_upper_load_kn: float,
    relative_reference_splice_efficiency_percent: float,
) -> float:
    """
    Calculate nominal breaking strength from reference upper load and relative reference splice efficiency.

    Parameters
    ----------
    reference_upper_load_kn : float
        The reference upper load in kilonewtons (kN).
    relative_reference_splice_efficiency_percent : float
        The relative reference splice efficiency in percent.

    Returns
    -------
    float
        The nominal breaking strength of the specimen in kilonewtons (kN).

    Raises
    ------
    ValueError
        If relative_reference_splice_efficiency_percent is zero or negative,
        preventing division by zero or physically invalid results.

    Notes
    -----
    Inverse formula: T_breaking = T_upper / (T_rel_fatigue / 100)
    where:
        T_breaking = nominal breaking strength of specimen (kN)
        T_upper = reference upper load (kN)
        T_rel_fatigue = relative reference splice efficiency (%)
    """
    # Guard against division by zero and invalid denominator
    if relative_reference_splice_efficiency_percent <= 0:
        raise ValueError(
            f"relative_reference_splice_efficiency_percent must be positive, "
            f"got {relative_reference_splice_efficiency_percent}."
        )

    nominal_breaking_strength_of_specimen_kn = reference_upper_load_kn / (
        relative_reference_splice_efficiency_percent / 100.0
    )
    return nominal_breaking_strength_of_specimen_kn


def _lower_load_from_nominal_breaking_strength_of_specimen(
    nominal_breaking_strength_of_specimen_kn: float,
    *,
    lower_load_factor: float = 0.0667,
) -> float:
    """
    Calculate lower load from nominal breaking strength of specimen.

    Parameters
    ----------
    nominal_breaking_strength_of_specimen_kn : float
        The nominal breaking strength of the specimen in kilonewtons (kN).
    lower_load_factor : float, optional
        Dimensionless lower-load factor. Default is 0.0667.

    Returns
    -------
    float
        The lower load in kilonewtons (kN).

    Raises
    ------
    ValueError
        If lower_load_factor is zero or negative, preventing physically invalid
        results.

    Notes
    -----
    Formula: T_lower = c_lower * T_breaking
    where:
        T_lower = lower load (kN)
        c_lower = lower-load factor (-)
        T_breaking = nominal breaking strength of specimen (kN)
    """
    if lower_load_factor <= 0:
        raise ValueError(
            f"lower_load_factor must be positive, got {lower_load_factor}."
        )

    lower_load_kn = lower_load_factor * nominal_breaking_strength_of_specimen_kn
    return lower_load_kn


def _nominal_breaking_strength_of_specimen_from_lower_load(
    lower_load_kn: float,
    *,
    lower_load_factor: float = 0.0667,
) -> float:
    """
    Calculate nominal breaking strength of specimen from lower load.

    Parameters
    ----------
    lower_load_kn : float
        The lower load in kilonewtons (kN).
    lower_load_factor : float, optional
        Dimensionless lower-load factor. Default is 0.0667.

    Returns
    -------
    float
        The nominal breaking strength of the specimen in kilonewtons (kN).

    Raises
    ------
    ValueError
        If lower_load_factor is zero or negative, preventing division by zero
        or physically invalid results.

    Notes
    -----
    Inverse formula: T_breaking = T_lower / c_lower
    where:
        T_breaking = nominal breaking strength of specimen (kN)
        T_lower = lower load (kN)
        c_lower = lower-load factor (-)
    """
    if lower_load_factor <= 0:
        raise ValueError(
            f"lower_load_factor must be positive, got {lower_load_factor}."
        )

    nominal_breaking_strength_of_specimen_kn = lower_load_kn / lower_load_factor
    return nominal_breaking_strength_of_specimen_kn
