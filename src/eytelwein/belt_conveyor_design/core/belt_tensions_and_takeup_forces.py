"""Public API for belt tensions and takeup forces calculations.

This module provides the Quantity-based public interface for calculations
in the belt-tensions-and-takeup-forces domain. Each public function wraps
the corresponding private helper with unit conversion, validation, and
output formatting.
"""

from pint import Quantity
from eytelwein.belt_conveyor_design.core._belt_tensions_and_takeup_forces import (
    _minimum_belt_tension_from_sag_carry,
)
from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def minimum_belt_tension_from_sag_carry(
    line_load_belt: Quantity,
    line_load_material: Quantity,
    idler_spacing: Quantity,
    allowable_sag: Quantity,
    unit: str = "kilonewton",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate minimum belt tension from sag during carry run.

    This function applies the relationship between belt tension,
    belt and material line loads, idler spacing, and allowable sag.
    All inputs must be strict Quantity objects with explicit units.

    Parameters
    ----------
    line_load_belt : Quantity
        Belt line load (mass per unit length) in kg/m or equivalent units.
    line_load_material : Quantity
        Material line load (mass per unit length) in kg/m or equivalent units.
    idler_spacing : Quantity
        Distance between consecutive idlers (e.g., 1.5 meter).
    allowable_sag : Quantity
        Allowable sag as a dimensionless fraction of idler spacing
        (e.g., 0.01 for 1%). Must be a Quantity with dimensionless units.
    unit : str, optional
        Output unit for tension result (default: "kilonewton").
        Common values: "newton", "kilonewton".
        Must be a force unit.
    precision : int or None, optional
        Decimal places to round the result to (default: 5).
        If None, no rounding is applied.

    Returns
    -------
    Quantity
        Minimum belt tension in the specified output unit.

    Raises
    ------
    ValueError
        If unit conversion fails due to incompatible input units.
    ValueError
        If line_load_belt is negative.
    ValueError
        If line_load_material is negative.
    ValueError
        If idler_spacing is negative.
    ValueError
        If allowable_sag is not positive or invalid.

    Examples
    --------
    >>> from pint import Quantity
    >>> from eytelwein.main.units import get_unit_registry
    >>> u = get_unit_registry()
    >>> result = minimum_belt_tension_from_sag_carry(
    ...     line_load_belt=Quantity(5.0, u.kilogram / u.meter),
    ...     line_load_material=Quantity(10.0, u.kilogram / u.meter),
    ...     idler_spacing=Quantity(1.5, u.meter),
    ...     allowable_sag=Quantity(0.01, u.dimensionless),
    ... )
    >>> result  # doctest: +SKIP
    2.75812... kilonewton
    """
    try:
        # Convert inputs to standard working units
        line_load_belt_kg_m = line_load_belt.to(u.kilogram / u.meter)
        line_load_material_kg_m = line_load_material.to(u.kilogram / u.meter)
        idler_spacing_m = idler_spacing.to(u.meter)

        # Convert allowable_sag to dimensionless
        sag_percent_val = allowable_sag.to(u.dimensionless).magnitude
    except Exception as e:
        raise ValueError(f"Error in unit conversion: {e}")

    # Validate physical constraints after unit conversion
    if line_load_belt_kg_m.magnitude < 0:
        raise ValueError(
            f"line_load_belt cannot be negative, got {line_load_belt_kg_m}"
        )

    if line_load_material_kg_m.magnitude < 0:
        raise ValueError(
            f"line_load_material cannot be negative, got {line_load_material_kg_m}"
        )

    if idler_spacing_m.magnitude < 0:
        raise ValueError(f"idler_spacing cannot be negative, got {idler_spacing_m}")

    # Ensure the output unit is valid
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call private implementation with magnitude values
    tension_newtons = _minimum_belt_tension_from_sag_carry(
        line_load_belt_kg_per_m=line_load_belt_kg_m.magnitude,
        line_load_material_kg_per_m=line_load_material_kg_m.magnitude,
        idler_spacing_m=idler_spacing_m.magnitude,
        allowable_sag=sag_percent_val,
    )

    # Attach units to result (newtons)
    result = tension_newtons * u.newton

    # Convert to requested output unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in attaching unit '{unit}': {e}")

    # Apply precision rounding if specified
    if precision is not None:
        result = round(result, precision)

    return result
