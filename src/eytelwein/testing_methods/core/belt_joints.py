from pint.registry import Quantity

from eytelwein.main.units import get_unit_registry
from eytelwein.testing_methods.core._belt_joints import (
    _nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    _nominal_breaking_strength_of_textile_belt_specimen,
    _reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    _relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    _specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
)

# Get the unit registry
u = get_unit_registry()


def nominal_breaking_strength_of_textile_belt_specimen(
    specimen_width: Quantity,
    width_related_nominal_breaking_tension: Quantity,
    unit: str = "kilonewton",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate the nominal breaking strength of a textile belt specimen.

    Parameters
    ----------
    specimen_width : Quantity
        The width of the textile belt specimen in millimeters.
    width_related_nominal_breaking_tension : Quantity
        The width-related nominal breaking tension (breaking strength per unit width) in Newtons per millimeter.
    unit : str, optional
        The unit for the result, default is "kilonewton".
    precision : int | None, optional
        The precision for rounding the result. Default is None. Use None to skip
        rounding and retain maximum available precision.

    Returns
    -------
    Quantity
        The nominal breaking strength of the textile belt specimen.

    Raises
    ------
    ValueError
        If there is an error in converting inputs, if physical constraints are violated, or if the unit is invalid.

    Notes
    -----
    Formula: F_B = b * k_N
    where:
        F_B = breaking strength (kN)
        b = belt width (mm)
        k_N = width-related nominal breaking tension (N/mm)
    """
    try:
        specimen_width_mm = specimen_width.to("mm")
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting specimen_width: {e}")

    try:
        width_related_nominal_breaking_tension_n_per_mm = (
            width_related_nominal_breaking_tension.to("N/mm")
        )
    except Exception as e:  # noqa: BLE001
        raise ValueError(
            f"Error in converting width_related_nominal_breaking_tension: {e}"
        )

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Validate physical constraints
    if specimen_width_mm.magnitude <= 0:
        raise ValueError(
            f"specimen_width must be positive, got {specimen_width_mm.magnitude}"
        )

    if width_related_nominal_breaking_tension_n_per_mm.magnitude < 0:
        raise ValueError(
            f"width_related_nominal_breaking_tension must be non-negative, got {width_related_nominal_breaking_tension_n_per_mm.magnitude}"
        )

    # Calculate the nominal breaking strength
    breaking_strength_kn = (
        _nominal_breaking_strength_of_textile_belt_specimen(
            specimen_width_mm.magnitude,
            width_related_nominal_breaking_tension_n_per_mm.magnitude,
        )
        * u.kilonewton
    )

    # First convert to the requested output unit
    try:
        result = breaking_strength_kn.to(pint_unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting to output unit: {e}")

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
    nominal_breaking_strength: Quantity,
    width_related_nominal_breaking_tension: Quantity,
    unit: str = "millimeter",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate specimen width from nominal breaking strength and width-related nominal breaking tension.

    Parameters
    ----------
    nominal_breaking_strength : Quantity
        The nominal breaking strength of the specimen.
    width_related_nominal_breaking_tension : Quantity
        The width-related nominal breaking tension (breaking strength per unit width).
    unit : str, optional
        The unit for the result, default is "millimeter".
    precision : int | None, optional
        The precision for rounding the result. Default is None. Use None to skip
        rounding and retain maximum available precision.

    Returns
    -------
    Quantity
        The specimen width.

    Raises
    ------
    ValueError
        If there is an error in converting inputs, if physical constraints are violated, or if the unit is invalid.

    Notes
    -----
    Inverse formula: b = 1000 * F_B / k_N
    where:
        b = specimen width (mm)
        F_B = breaking strength (kN)
        k_N = width-related nominal breaking tension (N/mm)
    """
    try:
        nominal_breaking_strength_kn = nominal_breaking_strength.to("kN")
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting nominal_breaking_strength: {e}")

    try:
        width_related_nominal_breaking_tension_n_per_mm = (
            width_related_nominal_breaking_tension.to("N/mm")
        )
    except Exception as e:  # noqa: BLE001
        raise ValueError(
            f"Error in converting width_related_nominal_breaking_tension: {e}"
        )

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call the private inverse helper (it validates denominator)
    specimen_width_mm = (
        _specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
            nominal_breaking_strength_kn.magnitude,
            width_related_nominal_breaking_tension_n_per_mm.magnitude,
        )
        * u.millimeter
    )

    # First convert to the requested output unit
    try:
        result = specimen_width_mm.to(pint_unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting to output unit: {e}")

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
    nominal_breaking_strength: Quantity,
    specimen_width: Quantity,
    unit: str = "N/mm",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate width-related nominal breaking tension from nominal breaking strength and specimen width.

    Parameters
    ----------
    nominal_breaking_strength : Quantity
        The nominal breaking strength of the specimen.
    specimen_width : Quantity
        The width of the specimen.
    unit : str, optional
        The unit for the result, default is "N/mm".
    precision : int | None, optional
        The precision for rounding the result. Default is None. Use None to skip
        rounding and retain maximum available precision.

    Returns
    -------
    Quantity
        The width-related nominal breaking tension (breaking strength per unit width).

    Raises
    ------
    ValueError
        If there is an error in converting inputs, if physical constraints are violated, or if the unit is invalid.

    Notes
    -----
    Inverse formula: k_N = 1000 * F_B / b
    where:
        k_N = tension coefficient (N/mm)
        F_B = breaking strength (kN)
        b = specimen width (mm)
    """
    try:
        nominal_breaking_strength_kn = nominal_breaking_strength.to("kN")
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting nominal_breaking_strength: {e}")

    try:
        specimen_width_mm = specimen_width.to("mm")
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting specimen_width: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call the private inverse helper (it validates denominator)
    tension_coefficient_n_per_mm = (
        _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
            nominal_breaking_strength_kn.magnitude,
            specimen_width_mm.magnitude,
        )
        * u.N
        / u.mm
    )

    # First convert to the requested output unit
    try:
        result = tension_coefficient_n_per_mm.to(pint_unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting to output unit: {e}")

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
    reference_upper_load: Quantity,
    nominal_breaking_strength_of_specimen: Quantity,
    unit: str = "percent",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate relative reference splice efficiency from reference upper load and nominal breaking strength.

    Parameters
    ----------
    reference_upper_load : Quantity
        The reference upper load in kilonewtons (kN).
    nominal_breaking_strength_of_specimen : Quantity
        The nominal breaking strength of the specimen in kilonewtons (kN).
    unit : str, optional
        The unit for the result, default is "percent".
    precision : int | None, optional
        The precision for rounding the result. Default is None. Use None to skip
        rounding and retain maximum available precision.

    Returns
    -------
    Quantity
        The relative reference splice efficiency.

    Raises
    ------
    ValueError
        If there is an error in converting inputs, if physical constraints are violated, or if the unit is invalid.

    Notes
    -----
    Formula: k_t,rel = F_o,ref / F_B * 100
    where:
        k_t,rel = relative reference splice efficiency (%)
        F_o,ref = reference upper load (kN)
        F_B = nominal breaking strength of specimen (kN)
    """
    try:
        reference_upper_load_kn = reference_upper_load.to("kN")
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting reference_upper_load: {e}")

    try:
        nominal_breaking_strength_of_specimen_kn = (
            nominal_breaking_strength_of_specimen.to("kN")
        )
    except Exception as e:  # noqa: BLE001
        raise ValueError(
            f"Error in converting nominal_breaking_strength_of_specimen: {e}"
        )

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call the private forward helper (it validates denominator)
    efficiency_percent = (
        _relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
            reference_upper_load_kn.magnitude,
            nominal_breaking_strength_of_specimen_kn.magnitude,
        )
        * u.percent
    )

    # First convert to the requested output unit
    try:
        result = efficiency_percent.to(pint_unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting to output unit: {e}")

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
    relative_reference_splice_efficiency: Quantity,
    nominal_breaking_strength_of_specimen: Quantity,
    unit: str = "kilonewton",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate reference upper load from relative reference splice efficiency and nominal breaking strength.

    Parameters
    ----------
    relative_reference_splice_efficiency : Quantity
        The relative reference splice efficiency.
    nominal_breaking_strength_of_specimen : Quantity
        The nominal breaking strength of the specimen in kilonewtons (kN).
    unit : str, optional
        The unit for the result, default is "kilonewton".
    precision : int | None, optional
        The precision for rounding the result. Default is None. Use None to skip
        rounding and retain maximum available precision.

    Returns
    -------
    Quantity
        The reference upper load in kilonewtons (kN).

    Raises
    ------
    ValueError
        If there is an error in converting inputs or if the unit is invalid.

    Notes
    -----
    Inverse formula: F_o,ref = k_t,rel / 100 * F_B
    where:
        F_o,ref = reference upper load (kN)
        k_t,rel = relative reference splice efficiency (%)
        F_B = nominal breaking strength of specimen (kN)
    """
    try:
        relative_reference_splice_efficiency_percent = (
            relative_reference_splice_efficiency.to("percent")
        )
    except Exception as e:  # noqa: BLE001
        raise ValueError(
            f"Error in converting relative_reference_splice_efficiency: {e}"
        )

    try:
        nominal_breaking_strength_of_specimen_kn = (
            nominal_breaking_strength_of_specimen.to("kN")
        )
    except Exception as e:  # noqa: BLE001
        raise ValueError(
            f"Error in converting nominal_breaking_strength_of_specimen: {e}"
        )

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call the private inverse helper
    reference_upper_load_kn = (
        _reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
            relative_reference_splice_efficiency_percent.magnitude,
            nominal_breaking_strength_of_specimen_kn.magnitude,
        )
        * u.kilonewton
    )

    # First convert to the requested output unit
    try:
        result = reference_upper_load_kn.to(pint_unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting to output unit: {e}")

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
    reference_upper_load: Quantity,
    relative_reference_splice_efficiency: Quantity,
    unit: str = "kilonewton",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate nominal breaking strength of specimen from reference upper load and relative reference splice efficiency.

    Parameters
    ----------
    reference_upper_load : Quantity
        The reference upper load in kilonewtons (kN).
    relative_reference_splice_efficiency : Quantity
        The relative reference splice efficiency.
    unit : str, optional
        The unit for the result, default is "kilonewton".
    precision : int | None, optional
        The precision for rounding the result. Default is None. Use None to skip
        rounding and retain maximum available precision.

    Returns
    -------
    Quantity
        The nominal breaking strength of the specimen in kilonewtons (kN).

    Raises
    ------
    ValueError
        If there is an error in converting inputs, if physical constraints are violated, or if the unit is invalid.

    Notes
    -----
    Inverse formula: F_B = F_o,ref / (k_t,rel / 100)
    where:
        F_B = nominal breaking strength of specimen (kN)
        F_o,ref = reference upper load (kN)
        k_t,rel = relative reference splice efficiency (%)
    """
    try:
        reference_upper_load_kn = reference_upper_load.to("kN")
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting reference_upper_load: {e}")

    try:
        relative_reference_splice_efficiency_percent = (
            relative_reference_splice_efficiency.to("percent")
        )
    except Exception as e:  # noqa: BLE001
        raise ValueError(
            f"Error in converting relative_reference_splice_efficiency: {e}"
        )

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call the private inverse helper (it validates denominator)
    nominal_breaking_strength_kn = (
        _nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
            reference_upper_load_kn.magnitude,
            relative_reference_splice_efficiency_percent.magnitude,
        )
        * u.kilonewton
    )

    # First convert to the requested output unit
    try:
        result = nominal_breaking_strength_kn.to(pint_unit)
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Error in converting to output unit: {e}")

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
