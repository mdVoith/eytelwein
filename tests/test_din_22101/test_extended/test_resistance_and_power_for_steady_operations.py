import pytest
from eytelwein.din_22101.extended.resistance_and_power_for_steady_operations import (
    motion_resistance_from_torque,
)

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def test_calculates_motion_resistance_correctly():
    torque = 100 * u.newton * u.meter
    pulley_diameter = 0.5 * u.meter
    expected_resistance = 400 * u.newton
    assert (
        motion_resistance_from_torque(torque, pulley_diameter).to(u.newton).magnitude
        == expected_resistance.magnitude
    )


def test_handles_zero_torque():
    torque = 0 * u.newton * u.meter
    pulley_diameter = 0.5 * u.meter
    expected_resistance = 0 * u.newton
    assert (
        motion_resistance_from_torque(torque, pulley_diameter).to(u.newton).magnitude
        == expected_resistance.magnitude
    )


def test_handles_zero_pulley_diameter():
    torque = 100 * u.newton * u.meter
    pulley_diameter = 0 * u.meter
    with pytest.raises(ValueError):
        motion_resistance_from_torque(torque, pulley_diameter)


def test_handles_invalid_unit():
    torque = 100 * u.newton * u.meter
    pulley_diameter = 0.5 * u.meter
    with pytest.raises(ValueError, match="Invalid unit: invalid_unit. Error: "):
        motion_resistance_from_torque(torque, pulley_diameter, unit="invalid_unit")


def test_handles_unit_conversion_error():
    torque = 100 * u.newton
    pulley_diameter = 0.5 * u.meter
    with pytest.raises(ValueError, match="Error in converting units: "):
        motion_resistance_from_torque(torque, pulley_diameter)
