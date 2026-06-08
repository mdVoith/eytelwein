from pint.registry import Quantity

from eytelwein.belt_conveyor_design.constants import (
    MinimumPulleyDiameterCoefficient,
    PulleyLoadFactor,
)
from eytelwein.belt_conveyor_design.core._minimum_pulley_diameter import (
    _minimum_diameter_of_group_A_pulleys,
    _pulley_load_factor,
    _minimum_diameter_of_group_A_B_C_pulleys,
    _get_max_width_related_tension_at_group_A_pulleys,
)

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def minimum_diameter_of_group_A_pulleys(
    minimum_pulley_diameter_coefficient: MinimumPulleyDiameterCoefficient,
    tension_member_thickness: Quantity,
    unit: str = "millimeter",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate the minimum diameter of a group A pulley.

    Parameters
    ----------
    minimum_pulley_diameter_coefficient : MinimumPulleyDiameterCoefficient
        The minimum pulley diameter coefficient, dimensionless.
    tension_member_thickness : Quantity
        The thickness of the tension member inmillimeters.
    unit : str, optional
        The unit for the result, default is "millimeter" and "meter" is a useful alternative.
    precision : int | None, optional
        The precision for rounding the result. Default is None. Use None to skip
        rounding and retain maximum available precision.

    Returns
    -------
    Quantity
        The minimum diameter of a group A pulley usually in millimeters.

    Raises
    ------
    ValueError
        If there is an error in converting tension_member_thickness or if the unit is invalid.
    """
    try:
        tension_member_thickness_mm = tension_member_thickness.to("mm")
    except Exception as e:
        raise ValueError(f"Error in converting tension_member_thickness: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the minimum diameter of a group A pulley.
    pulley_diameter = (
        _minimum_diameter_of_group_A_pulleys(
            minimum_pulley_diameter_coefficient.to_int(),
            tension_member_thickness_mm.magnitude,
        )
        * u.mm
    )

    # First convert to the requested output unit
    result = pulley_diameter.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def pulley_load_factor(
    max_width_related_belt_tension_at_pulleys: Quantity,
    nominal_belt_breaking_strength: Quantity,
) -> float:
    """
    Calculate the pulley load factor.

    Parameters
    ----------
    max_width_related_belt_tension_at_pulleys : Quantity
        The mean width-related tension at the point of maximum belt tension in the zone of Group A pulleys in the steady operating condition in kilonewton.
    nominal_belt_breaking_strength : Quantity
        The nominal belt breaking strength in kilonewton.

    Returns
    -------
    float
        The pulley load factor as a percentage.
    """
    try:
        max_width_related_belt_tension_at_pulleys_kN = (
            max_width_related_belt_tension_at_pulleys.to("kilonewton")
        )
        nominal_belt_breaking_strength_kN = nominal_belt_breaking_strength.to(
            "kilonewton"
        )
    except Exception as e:
        raise ValueError(f"Error in converting tension_member_thickness: {e}")

    load_factor = _pulley_load_factor(
        max_width_related_belt_tension_at_pulleys_kN.magnitude,
        nominal_belt_breaking_strength_kN.magnitude,
    )
    return load_factor


def minimum_diameter_of_group_A_B_C_pulleys(
    minimum_diameter_of_group_A_pulleys: Quantity,
    pulley_load_factor: PulleyLoadFactor,
    unit: str = "millimeter",
    precision: int | None = None,
) -> dict[str, Quantity | None]:
    """
    Calculate the minimum diameters of group A, B, and C pulleys.

    Parameters
    ----------
    minimum_diameter_of_group_A_pulleys : Quantity
        The minimum diameter of group A pulleys.
    pulley_load_factor : PulleyLoadFactor
        The pulley load factor.
    unit : str, optional
        The unit for the result, default is "millimeter".
    precision : int | None, optional
        The precision for rounding the result. Default is None. Use None to skip
        rounding and retain maximum available precision.

    Returns
    -------
    Dict[str, Quantity[int, None]]
        A dictionary with the minimum diameters of group A, B, and C pulleys.

    Raises
    ------
    ValueError
        If there is an error in converting the minimum diameter or if the unit is invalid.
    """
    try:
        minimum_diameter_of_group_A_pulleys_mm = minimum_diameter_of_group_A_pulleys.to(
            "mm"
        )
    except Exception as e:
        raise ValueError(f"Error in converting pulley diameter: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    A_B_C = _minimum_diameter_of_group_A_B_C_pulleys(
        minimum_diameter_of_group_A_pulleys_mm.magnitude, pulley_load_factor
    )

    # Create dictionary with mm units
    A_B_C_mm = {k: (v * u.mm if v is not None else None) for k, v in A_B_C.items()}

    # First convert to the requested output unit
    A_B_C_unit = {
        k: (v.to(pint_unit) if v is not None else None) for k, v in A_B_C_mm.items()
    }

    # Then apply precision if specified
    if precision is not None:
        A_B_C_unit = {
            k: (round(v, precision) if v is not None else None)
            for k, v in A_B_C_unit.items()
        }

    return A_B_C_unit


def get_max_width_related_tension_at_group_A_pulleys(
    nominal_belt_strength: Quantity,
    pulley_load_factor: PulleyLoadFactor = PulleyLoadFactor.above_60_up_to_100,
    unit: str = "newton / millimeter",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate the maximum width-related tension at the point of maximum belt tension in the zone of Group A pulleys in the steady operating condition.

    Parameters
    ----------
    nominal_belt_strength : Quantity
        The nominal belt strength in newton per millimeter.
    pulley_load_factor : PulleyLoadFactor, optional
        The pulley load factor, default is PulleyLoadFactor.above_60_up_to_100.
    unit : str, optional
        The unit for the result, default is "kilonewton".
    precision : int | None, optional
        The precision for rounding the result. Default is None. Use None to skip
        rounding and retain maximum available precision.

    Returns
    -------
    Quantity
        The maximum width-related tension at the point of maximum belt tension in the zone of Group A pulleys in the steady operating condition.

    Raises
    ------
    ValueError
        If there is an error in converting nominal_belt_strength or if the unit is invalid.
    """
    try:
        nominal_belt_strength_Npmm = nominal_belt_strength.to("newton / millimeter")
    except Exception as e:
        raise ValueError(f"Error in converting nominal_belt_strength: {e}")

    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    max_width_related_tension = (
        (
            _get_max_width_related_tension_at_group_A_pulleys(
                nominal_belt_strength_Npmm.magnitude, pulley_load_factor
            )
        )
        * u.newton
        / u.millimeter
    )

    # First convert to the requested output unit
    result = max_width_related_tension.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
