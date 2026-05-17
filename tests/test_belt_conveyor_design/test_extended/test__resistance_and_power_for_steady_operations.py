import pytest

from eytelwein.belt_conveyor_design.extended._resistance_and_power_for_steady_operations import (
    _motion_resistance_from_torque,
)


def test_calculates_motion_resistance_correctly():
    torque = 100.0
    pulley_diameter = 0.5
    expected_resistance = 2 * torque / pulley_diameter
    assert (
        _motion_resistance_from_torque(torque, pulley_diameter) == expected_resistance
    )


def test_handles_zero_torque():
    torque = 0.0
    pulley_diameter = 0.5
    expected_resistance = 0.0
    assert (
        _motion_resistance_from_torque(torque, pulley_diameter) == expected_resistance
    )


def test_handles_zero_pulley_diameter():
    torque = 100.0
    pulley_diameter = 0.0
    with pytest.raises(ValueError, match="pulley_diameter must be positive"):
        _motion_resistance_from_torque(torque, pulley_diameter)


def test_handles_negative_torque():
    torque = -100.0
    pulley_diameter = 0.5
    expected_resistance = 2 * torque / pulley_diameter
    assert (
        _motion_resistance_from_torque(torque, pulley_diameter) == expected_resistance
    )


def test_handles_negative_pulley_diameter():
    torque = 100.0
    pulley_diameter = -0.5
    with pytest.raises(ValueError, match="pulley_diameter must be positive"):
        _motion_resistance_from_torque(torque, pulley_diameter)
