from pint import Quantity

from eytelwein.belt_conveyor_design.extended._design_of_conveyor_belt import (
    _belt_weight_per_square_meter,
    _line_load_belt,
    _line_load_belt_from_belt_weight_per_square_meter,
)
from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def belt_weight_per_square_meter(
    tension_member_weight: Quantity,
    top_cover_thickness: Quantity,
    bottom_cover_thickness: Quantity,
    rubber_density: Quantity,
    unit: str = "kilogram/meter**2",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate the total weight per square meter of a conveyor belt.

    This function computes the total weight per square meter by summing the weight of
    the tension member and the combined weight of the top and bottom rubber covers.

    Parameters:
        tension_member_weight: Weight per square meter of the tension member (e.g.,
            fabric or steel cords) as a `Quantity` with units of kg/m².
        top_cover_thickness: Thickness of the top rubber cover as a `Quantity` with
            units of length (e.g., millimeters or meters).
        bottom_cover_thickness: Thickness of the bottom rubber cover as a `Quantity`
            with units of length (e.g., millimeters or meters).
        rubber_density: Density of the rubber material as a `Quantity` with units
            of kg/m³.
        unit: The unit for the returned weight. Defaults to "kilogram/meter**2".
        precision: The number of decimal places to round the result to. Defaults to None. Use None to skip rounding and retain maximum available precision.

    Returns:
        The calculated total weight per square meter of the conveyor belt as a
        `Quantity` with the specified unit.

    Raises:
        ValueError: If there is an error in converting units or if the input values
        are not physically meaningful.
    """
    try:
        # Convert inputs to standard units for calculation
        tension_member_weight_kgpm2 = tension_member_weight.to(u.kilogram / u.meter**2)
        top_cover_thickness_m = top_cover_thickness.to(u.meter)
        bottom_cover_thickness_m = bottom_cover_thickness.to(u.meter)
        rubber_density_kgpm3 = rubber_density.to(u.kilogram / u.meter**3)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Validate inputs for physical meaningfulness
    if tension_member_weight_kgpm2.magnitude < 0:
        raise ValueError("Tension member weight cannot be negative")
    if top_cover_thickness_m.magnitude < 0:
        raise ValueError("Top cover thickness cannot be negative")
    if bottom_cover_thickness_m.magnitude < 0:
        raise ValueError("Bottom cover thickness cannot be negative")
    if rubber_density_kgpm3.magnitude <= 0:
        raise ValueError("Rubber density must be positive")

    # Calculate the belt weight using the private implementation
    weight_kgpm2 = _belt_weight_per_square_meter(
        tension_member_weight_kgpm2.magnitude,
        top_cover_thickness_m.magnitude,
        bottom_cover_thickness_m.magnitude,
        rubber_density_kgpm3.magnitude,
    ) * (u.kilogram / u.meter**2)

    # First convert to the requested output unit
    result = weight_kgpm2.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def line_load_belt(
    tension_member_weight: Quantity,
    belt_width: Quantity,
    top_cover_thickness: Quantity,
    bottom_cover_thickness: Quantity,
    rubber_density: Quantity,
    unit: str = "kilogram/meter",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate the line load of a conveyor belt.

    This function computes the total line load (weight per unit length) of a conveyor belt
    by calculating the weight per square meter and multiplying by the belt width.

    Parameters:
        tension_member_weight: Weight per square meter of the tension member (e.g.,
            fabric or steel cords) as a `Quantity` with units of kg/m².
        belt_width: Width of the belt as a `Quantity` with units of length (e.g., meters).
        top_cover_thickness: Thickness of the top rubber cover as a `Quantity` with
            units of length (e.g., millimeters or meters).
        bottom_cover_thickness: Thickness of the bottom rubber cover as a `Quantity`
            with units of length (e.g., millimeters or meters).
        rubber_density: Density of the rubber material as a `Quantity` with units
            of kg/m³.
        unit: The unit for the returned line load. Defaults to "kilogram/meter".
        precision: The number of decimal places to round the result to. Defaults to None. Use None to skip rounding and retain maximum available precision.

    Returns:
        The calculated line load of the conveyor belt as a `Quantity` with the
        specified unit.

    Raises:
        ValueError: If there is an error in converting units or if the input values
        are not physically meaningful.
    """
    try:
        # Convert inputs to standard units for calculation
        tension_member_weight_kgpm2 = tension_member_weight.to(u.kilogram / u.meter**2)
        belt_width_m = belt_width.to(u.meter)
        top_cover_thickness_m = top_cover_thickness.to(u.meter)
        bottom_cover_thickness_m = bottom_cover_thickness.to(u.meter)
        rubber_density_kgpm3 = rubber_density.to(u.kilogram / u.meter**3)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Validate inputs for physical meaningfulness
    if tension_member_weight_kgpm2.magnitude < 0:
        raise ValueError("Tension member weight cannot be negative")
    if belt_width_m.magnitude <= 0:
        raise ValueError("Belt width must be positive")
    if top_cover_thickness_m.magnitude < 0:
        raise ValueError("Top cover thickness cannot be negative")
    if bottom_cover_thickness_m.magnitude < 0:
        raise ValueError("Bottom cover thickness cannot be negative")
    if rubber_density_kgpm3.magnitude <= 0:
        raise ValueError("Rubber density must be positive")

    # Calculate the line load using the private implementation
    line_load_kgpm = _line_load_belt(
        tension_member_weight_kgpm2.magnitude,
        belt_width_m.magnitude,
        top_cover_thickness_m.magnitude,
        bottom_cover_thickness_m.magnitude,
        rubber_density_kgpm3.magnitude,
    ) * (u.kilogram / u.meter)

    # First convert to the requested output unit
    result = line_load_kgpm.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result


def line_load_belt_from_belt_weight_per_square_meter(
    belt_weight_per_square_meter: Quantity,
    belt_width: Quantity,
    unit: str = "kilogram/meter",
    precision: int | None = None,
) -> Quantity:
    """
    Calculate the line load of a conveyor belt from its weight per square meter.

    This function computes the total line load (weight per unit length) of a conveyor belt
    by multiplying the belt weight per square meter by the belt width.

    Parameters:
        belt_weight_per_square_meter: Weight of the belt per square meter as a `Quantity`
            with units of kg/m².
        belt_width: Width of the belt as a `Quantity` with units of length (e.g., meters).
        unit: The unit for the returned line load. Defaults to "kilogram/meter".
        precision: The number of decimal places to round the result to. Defaults to None. Use None to skip rounding and retain maximum available precision.

    Returns:
        The calculated line load of the conveyor belt as a `Quantity` with the
        specified unit.

    Raises:
        ValueError: If there is an error in converting units or if the input values
        are not physically meaningful.
    """
    try:
        # Convert inputs to standard units for calculation
        belt_weight_kgpm2 = belt_weight_per_square_meter.to(u.kilogram / u.meter**2)
        belt_width_m = belt_width.to(u.meter)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Validate inputs for physical meaningfulness
    if belt_weight_kgpm2.magnitude < 0:
        raise ValueError("Belt weight per square meter cannot be negative")
    if belt_width_m.magnitude <= 0:
        raise ValueError("Belt width must be positive")

    # Calculate the line load using the private implementation
    line_load_kgpm = _line_load_belt_from_belt_weight_per_square_meter(
        belt_weight_kgpm2.magnitude,
        belt_width_m.magnitude,
    ) * (u.kilogram / u.meter)

    # First convert to the requested output unit
    result = line_load_kgpm.to(pint_unit)

    # Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
