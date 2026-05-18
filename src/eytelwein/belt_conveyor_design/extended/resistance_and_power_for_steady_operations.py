from pint import Quantity

from eytelwein.belt_conveyor_design.extended._resistance_and_power_for_steady_operations import (
    _motion_resistance_from_torque,
)

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def motion_resistance_from_torque(
    torque: Quantity, pulley_diameter: Quantity, unit="kilonewton", precision=2
) -> Quantity:
    try:
        torque_Nm = torque.to(u.newton * u.meter)
        pulley_diameter_m = pulley_diameter.to(u.meter)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate the motion resistance
    resistance = (
        _motion_resistance_from_torque(torque_Nm.magnitude, pulley_diameter_m.magnitude)
        * u.newton
    )

    # Apply precision if specified.
    if precision is not None:
        resistance = round(resistance, precision)

    # Return the result with the specified unit
    return resistance.to(pint_unit)
