from pint.registry import Quantity

from eytelwein.main.units import get_unit_registry
from eytelwein.testing_methods.core._belt_joints import (
    _nominal_breaking_strength_of_textile_belt_specimen,
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
