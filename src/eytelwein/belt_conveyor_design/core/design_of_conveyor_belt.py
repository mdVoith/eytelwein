from eytelwein.belt_conveyor_design.constants import BeltCoverCharacteristicsAssessments
from pint import Quantity

from eytelwein.belt_conveyor_design.core._design_of_conveyor_belt import (
    _belt_safety_factor_fromsplice_strength_and_belt_tension,
    _splice_strength_from_belt_safety_factor_and_belt_tension,
    _belt_tension_fromsplice_strength_and_belt_safety_factor,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


def addition_to_minimum_cover_thickness(
    feeding_condition: BeltCoverCharacteristicsAssessments,
    cycle_time: BeltCoverCharacteristicsAssessments,
    top_size: BeltCoverCharacteristicsAssessments,
    bulk_density: BeltCoverCharacteristicsAssessments,
    abrasivity: BeltCoverCharacteristicsAssessments,
) -> tuple[int, int]:
    """
    Calculates the recommended addition to the minimum cover thickness for a conveyor belt based on several assessment criteria.
    Parameters:
        feeding_condition (BeltCoverCharacteristicsAssessments): Assessment of the feeding condition.
        cycle_time (BeltCoverCharacteristicsAssessments): Assessment of the cycle time.
        top_size (BeltCoverCharacteristicsAssessments): Assessment of the top size of the material.
        bulk_density (BeltCoverCharacteristicsAssessments): Assessment of the bulk density of the material.
        abrasivity (BeltCoverCharacteristicsAssessments): Assessment of the material's abrasivity.
    Returns:
        tuple[int, int]: A tuple representing the recommended range (in millimeters) to be added to the minimum cover thickness.
    """
    evaluation = 0
    evaluation += feeding_condition.to_int()
    evaluation += cycle_time.to_int()
    evaluation += top_size.to_int()
    evaluation += bulk_density.to_int()
    evaluation += abrasivity.to_int()

    if evaluation < 7:
        return (0, 1)
    elif evaluation < 9:
        return (1, 3)
    elif evaluation < 12:
        return (3, 6)
    elif evaluation < 14:
        return (6, 10)
    else:
        return (11, 15)


def belt_safety_factor_fromsplice_strength_and_belt_tension(
    splice_strength: Quantity,
    belt_tension: Quantity,
    unit: str = "dimensionless",
    precision: int | None = None,
) -> Quantity:
    """Calculate belt safety factor from splice strength and belt tension.

    Formula:
        S = k_N / k
    """
    try:
        splice_strength_n_per_mm = splice_strength.to(u.newton / u.millimeter)
        belt_tension_n_per_mm = belt_tension.to(u.newton / u.millimeter)
    except Exception as e:
        raise ValueError(f"Error in unit conversion: {e}")

    if splice_strength_n_per_mm.magnitude <= 0:
        raise ValueError(
            f"splice_strength must be positive, got {splice_strength_n_per_mm}"
        )
    if belt_tension_n_per_mm.magnitude <= 0:
        raise ValueError(f"belt_tension must be positive, got {belt_tension_n_per_mm}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    safety_factor = _belt_safety_factor_fromsplice_strength_and_belt_tension(
        splice_strength_n_per_mm=splice_strength_n_per_mm.magnitude,
        belt_tension_n_per_mm=belt_tension_n_per_mm.magnitude,
    )

    result = safety_factor * u.dimensionless

    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    if precision is not None:
        result = round(result, precision)

    return result


def splice_strength_from_belt_safety_factor_and_belt_tension(
    belt_safety_factor: Quantity,
    belt_tension: Quantity,
    unit: str = "newton / millimeter",
    precision: int | None = None,
) -> Quantity:
    """Calculate splice strength from belt safety factor and belt tension.

    Formula:
        k_N = S * k
    """
    try:
        belt_safety_factor_dimensionless = belt_safety_factor.to(u.dimensionless)
        belt_tension_n_per_mm = belt_tension.to(u.newton / u.millimeter)
    except Exception as e:
        raise ValueError(f"Error in unit conversion: {e}")

    if belt_safety_factor_dimensionless.magnitude <= 0:
        raise ValueError(
            "belt_safety_factor must be positive, "
            f"got {belt_safety_factor_dimensionless}"
        )
    if belt_tension_n_per_mm.magnitude <= 0:
        raise ValueError(f"belt_tension must be positive, got {belt_tension_n_per_mm}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    splice_strength_n_per_mm = (
        _splice_strength_from_belt_safety_factor_and_belt_tension(
            belt_safety_factor=belt_safety_factor_dimensionless.magnitude,
            belt_tension_n_per_mm=belt_tension_n_per_mm.magnitude,
        )
    )

    result = splice_strength_n_per_mm * (u.newton / u.millimeter)

    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    if precision is not None:
        result = round(result, precision)

    return result


def belt_tension_fromsplice_strength_and_belt_safety_factor(
    splice_strength: Quantity,
    belt_safety_factor: Quantity,
    unit: str = "newton / millimeter",
    precision: int | None = None,
) -> Quantity:
    """Calculate belt tension from splice strength and belt safety factor.

    Formula:
        k = k_N / S
    """
    try:
        splice_strength_n_per_mm = splice_strength.to(u.newton / u.millimeter)
        belt_safety_factor_dimensionless = belt_safety_factor.to(u.dimensionless)
    except Exception as e:
        raise ValueError(f"Error in unit conversion: {e}")

    if splice_strength_n_per_mm.magnitude <= 0:
        raise ValueError(
            f"splice_strength must be positive, got {splice_strength_n_per_mm}"
        )
    if belt_safety_factor_dimensionless.magnitude <= 0:
        raise ValueError(
            "belt_safety_factor must be positive, "
            f"got {belt_safety_factor_dimensionless}"
        )

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    belt_tension_n_per_mm = _belt_tension_fromsplice_strength_and_belt_safety_factor(
        splice_strength_n_per_mm=splice_strength_n_per_mm.magnitude,
        belt_safety_factor=belt_safety_factor_dimensionless.magnitude,
    )

    result = belt_tension_n_per_mm * (u.newton / u.millimeter)

    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    if precision is not None:
        result = round(result, precision)

    return result
