from math import pi
import math

import pytest
from eytelwein.din_22101.extended._design_layout_of_drive_system import (
    _angle_of_inclination_from_horizontal_length_and_lift,
    _mechanical_torque_from_belt_force,
    _mechanical_power_from_torque_and_belt_speed,
    _number_of_revolutions_from_translatory_speed,
    _pulley_diameter_from_belt_speed_and_revolutions,
    _pulley_revolutions_from_belt_speed,
    _radius_from_translatory_speed_and_revolutions,
    _translatory_speed_from_number_of_revolutions,
    _belt_speed_from_pulley_revolutions,
    _mechanical_power_from_torque_and_revolutions,
    _torque_from_mechanical_power_and_revolutions,
    _revolutions_from_mechanical_power_and_torque,
)


def test_mechanical_torque_valid_values():
    result = _mechanical_torque_from_belt_force(100.0, 50.0)
    assert result == 2500.0


def test_mechanical_torque_zero_belt_force():
    result = _mechanical_torque_from_belt_force(0.0, 50.0)
    assert result == 0.0


def test_mechanical_torque_zero_pulley_diameter():
    result = _mechanical_torque_from_belt_force(100.0, 0.0)
    assert result == 0.0


def test_mechanical_torque_negative_belt_force():
    result = _mechanical_torque_from_belt_force(-100.0, 50.0)
    assert result == -2500.0


def test_mechanical_torque_negative_pulley_diameter():
    result = _mechanical_torque_from_belt_force(100.0, -50.0)
    assert result == -2500.0


def test_mechanical_torque_negative_values():
    result = _mechanical_torque_from_belt_force(-100.0, -50.0)
    assert result == 2500.0


def test_mechanical_power_valid_values():
    result = _mechanical_power_from_torque_and_belt_speed(100.0, 5.0, 2.0)
    assert result == 500.0


def test_mechanical_power_zero_torque():
    result = _mechanical_power_from_torque_and_belt_speed(0.0, 5.0, 2.0)
    assert result == 0.0


def test_mechanical_power_zero_belt_speed():
    result = _mechanical_power_from_torque_and_belt_speed(100.0, 0.0, 2.0)
    assert result == 0.0


def test_mechanical_power_zero_pulley_diameter():
    with pytest.raises(ValueError, match="pulley_diameter must be positive"):
        _mechanical_power_from_torque_and_belt_speed(100.0, 5.0, 0.0)


def test_mechanical_power_negative_torque():
    result = _mechanical_power_from_torque_and_belt_speed(-100.0, 5.0, 2.0)
    assert result == -500.0


def test_mechanical_power_negative_belt_speed():
    result = _mechanical_power_from_torque_and_belt_speed(100.0, -5.0, 2.0)
    assert result == -500.0


def test_mechanical_power_negative_pulley_diameter():
    with pytest.raises(ValueError, match="pulley_diameter must be positive"):
        _mechanical_power_from_torque_and_belt_speed(100.0, 5.0, -2.0)


def test_mechanical_power_negative_values():
    with pytest.raises(ValueError, match="pulley_diameter must be positive"):
        _mechanical_power_from_torque_and_belt_speed(-100.0, -5.0, -2.0)


def test_calculates_revolutions_correctly():
    translatory_speed = 1.0
    radius = 1.0
    expected_revolutions = translatory_speed / (2 * pi * radius)
    assert (
        _number_of_revolutions_from_translatory_speed(translatory_speed, radius)
        == expected_revolutions
    )


def test_handles_zero_translatory_speed():
    translatory_speed = 0.0
    radius = 2.0
    expected_revolutions = 0.0
    assert (
        _number_of_revolutions_from_translatory_speed(translatory_speed, radius)
        == expected_revolutions
    )


def test_number_of_revolutions_zero_radius():
    """Test that zero radius raises ValueError."""
    with pytest.raises(ValueError, match="radius"):
        _number_of_revolutions_from_translatory_speed(1.0, 0.0)


def test_handles_zero_radius():
    translatory_speed = 10.0
    radius = 0.0
    with pytest.raises(ValueError):
        _number_of_revolutions_from_translatory_speed(translatory_speed, radius)


def test_handles_negative_translatory_speed():
    translatory_speed = -10.0
    radius = 2.0
    expected_revolutions = -10.0 / (2 * pi * 2.0)
    assert (
        _number_of_revolutions_from_translatory_speed(translatory_speed, radius)
        == expected_revolutions
    )


def test_handles_negative_radius():
    translatory_speed = 10.0
    radius = -2.0
    expected_revolutions = 10.0 / (2 * pi * -2.0)
    assert (
        _number_of_revolutions_from_translatory_speed(translatory_speed, radius)
        == expected_revolutions
    )


def test_calculates_pulley_revolutions_correctly():
    belt_speed = 1.0
    pulley_diameter = 2.0
    expected_revolutions = belt_speed / (pi * pulley_diameter)
    assert (
        _pulley_revolutions_from_belt_speed(belt_speed, pulley_diameter)
        == expected_revolutions
    )


def test_handles_zero_belt_speed():
    belt_speed = 0.0
    pulley_diameter = 2.0
    expected_revolutions = 0.0
    assert (
        _pulley_revolutions_from_belt_speed(belt_speed, pulley_diameter)
        == expected_revolutions
    )


def test_handles_zero_pulley_diameter():
    belt_speed = 10.0
    pulley_diameter = 0.0
    with pytest.raises(ValueError):
        _pulley_revolutions_from_belt_speed(belt_speed, pulley_diameter)


def test_handles_negative_belt_speed():
    belt_speed = -10.0
    pulley_diameter = 2.0
    expected_revolutions = -10.0 / (pi * 2.0)
    assert (
        _pulley_revolutions_from_belt_speed(belt_speed, pulley_diameter)
        == expected_revolutions
    )


def test_handles_negative_pulley_diameter():
    belt_speed = 10.0
    pulley_diameter = -2.0
    expected_revolutions = 10.0 / (pi * -2.0)
    assert (
        _pulley_revolutions_from_belt_speed(belt_speed, pulley_diameter)
        == expected_revolutions
    )


def test_calculates_translatory_speed_correctly():
    revolutions = 10.0
    radius = 2.0
    expected_speed = 2 * pi * 2.0 * 10.0
    assert (
        _translatory_speed_from_number_of_revolutions(revolutions, radius)
        == expected_speed
    )


def test_handles_zero_revolutions():
    revolutions = 0.0
    radius = 2.0
    expected_speed = 0.0
    assert (
        _translatory_speed_from_number_of_revolutions(revolutions, radius)
        == expected_speed
    )


def test_calculates_translatory_speed_handles_zero_radius():
    revolutions = 10.0
    radius = 0.0
    expected_speed = 0.0
    assert (
        _translatory_speed_from_number_of_revolutions(revolutions, radius)
        == expected_speed
    )


def test_handles_negative_revolutions():
    revolutions = -10.0
    radius = 2.0
    expected_speed = 2 * pi * 2.0 * -10.0
    assert (
        _translatory_speed_from_number_of_revolutions(revolutions, radius)
        == expected_speed
    )


def test_calculates_translatory_speed_handles_negative_radius():
    revolutions = 10.0
    radius = -2.0
    expected_speed = 2 * pi * -2.0 * 10.0
    assert (
        _translatory_speed_from_number_of_revolutions(revolutions, radius)
        == expected_speed
    )


def test_calculates_belt_speed_correctly():
    pulley_revolutions = 10.0
    pulley_diameter = 2.0
    expected_speed = 2 * pi * (2.0 / 2) * 10.0
    assert (
        _belt_speed_from_pulley_revolutions(pulley_revolutions, pulley_diameter)
        == expected_speed
    )


def test_handles_zero_pulley_revolutions():
    pulley_revolutions = 0.0
    pulley_diameter = 2.0
    expected_speed = 0.0
    assert (
        _belt_speed_from_pulley_revolutions(pulley_revolutions, pulley_diameter)
        == expected_speed
    )


def test_calculates_translatory_speed_handles_zero_pulley_diameter():
    pulley_revolutions = 10.0
    pulley_diameter = 0.0
    expected_speed = 0.0
    assert (
        _belt_speed_from_pulley_revolutions(pulley_revolutions, pulley_diameter)
        == expected_speed
    )


def test_handles_negative_pulley_revolutions():
    pulley_revolutions = -10.0
    pulley_diameter = 2.0
    expected_speed = 2 * pi * (2.0 / 2) * -10.0
    assert (
        _belt_speed_from_pulley_revolutions(pulley_revolutions, pulley_diameter)
        == expected_speed
    )


def test_calculates_translatory_speed_handles_negative_pulley_diameter():
    pulley_revolutions = 10.0
    pulley_diameter = -2.0
    expected_speed = 2 * pi * (-2.0 / 2) * 10.0
    assert (
        _belt_speed_from_pulley_revolutions(pulley_revolutions, pulley_diameter)
        == expected_speed
    )


def test_mechanical_power_with_positive_values():
    torque = 10.0
    revolutions = 5.0
    expected_power = 2 * pi * torque * revolutions
    assert (
        _mechanical_power_from_torque_and_revolutions(torque, revolutions)
        == expected_power
    )


def test_mechanical_power_with_zero_torque():
    torque = 0.0
    revolutions = 5.0
    expected_power = 0.0
    assert (
        _mechanical_power_from_torque_and_revolutions(torque, revolutions)
        == expected_power
    )


def test_mechanical_power_with_zero_revolutions():
    torque = 10.0
    revolutions = 0.0
    expected_power = 0.0
    assert (
        _mechanical_power_from_torque_and_revolutions(torque, revolutions)
        == expected_power
    )


def test_mechanical_power_with_negative_torque():
    torque = -10.0
    revolutions = 5.0
    expected_power = 2 * pi * torque * revolutions
    assert (
        _mechanical_power_from_torque_and_revolutions(torque, revolutions)
        == expected_power
    )


def test_mechanical_power_with_negative_revolutions():
    torque = 10.0
    revolutions = -5.0
    expected_power = 2 * pi * torque * revolutions
    assert (
        _mechanical_power_from_torque_and_revolutions(torque, revolutions)
        == expected_power
    )


def test_torque_with_positive_values():
    power = 100.0
    revolutions = 10.0
    expected_torque = power / (2 * pi * revolutions)
    assert (
        _torque_from_mechanical_power_and_revolutions(power, revolutions)
        == expected_torque
    )


def test_torque_with_zero_revolutions():
    power = 100.0
    revolutions = 0.0
    with pytest.raises(ValueError, match="revolutions must be positive"):
        _torque_from_mechanical_power_and_revolutions(power, revolutions)


def test_torque_with_negative_power():
    power = -100.0
    revolutions = 10.0
    expected_torque = power / (2 * pi * revolutions)
    assert (
        _torque_from_mechanical_power_and_revolutions(power, revolutions)
        == expected_torque
    )


def test_torque_with_negative_revolutions():
    power = 100.0
    revolutions = -10.0
    with pytest.raises(ValueError, match="revolutions must be positive"):
        _torque_from_mechanical_power_and_revolutions(power, revolutions)


def test_revolutions_with_positive_values():
    power = 100.0
    torque = 10.0
    expected_revolutions = power / (2 * pi * torque)
    assert (
        _revolutions_from_mechanical_power_and_torque(power, torque)
        == expected_revolutions
    )


def test_revolutions_with_zero_torque():
    power = 100.0
    torque = 0.0
    with pytest.raises(ValueError, match="torque must be positive"):
        _revolutions_from_mechanical_power_and_torque(power, torque)


def test_revolutions_with_negative_power():
    power = -100.0
    torque = 10.0
    expected_revolutions = power / (2 * pi * torque)
    assert (
        _revolutions_from_mechanical_power_and_torque(power, torque)
        == expected_revolutions
    )


def test_revolutions_with_negative_torque():
    power = 100.0
    torque = -10.0
    with pytest.raises(ValueError, match="torque must be positive"):
        _revolutions_from_mechanical_power_and_torque(power, torque)


def test_angle_of_inclination_typical_values():
    # 45 degrees (pi/4 radians) when lift == horizontal_length
    assert _angle_of_inclination_from_horizontal_length_and_lift(
        4303, 18.0
    ) == pytest.approx(0.00418, rel=1e-2)  # about 0.24 degrees in radians


def test_angle_of_inclination_zero_lift():
    # 0 radians when lift == 0
    assert _angle_of_inclination_from_horizontal_length_and_lift(
        2.0, 0.0
    ) == pytest.approx(0.0)


def test_angle_of_inclination_negative_lift():
    # -45 degrees (-pi/4 radians) when lift == -horizontal_length
    assert _angle_of_inclination_from_horizontal_length_and_lift(
        1.0, -1.0
    ) == pytest.approx(-pi / 4)  # Expect radians, not degrees


def test_angle_of_inclination_horizontal_length_zero_raises():
    # Should raise ValueError if horizontal_length is zero
    with pytest.raises(ValueError):
        _angle_of_inclination_from_horizontal_length_and_lift(0.0, 1.0)


def test_angle_of_inclination_negative_horizontal_length():
    # Should work for negative horizontal_length
    result = _angle_of_inclination_from_horizontal_length_and_lift(-1.0, 1.0)
    expected = math.atan2(1.0, -1.0)  # Expect radians
    assert result == pytest.approx(expected)


def test_angle_of_inclination_both_negative():
    # Should work for both negative values
    result = _angle_of_inclination_from_horizontal_length_and_lift(-2.0, -2.0)
    expected = math.atan2(-2.0, -2.0)  # Expect radians
    assert result == pytest.approx(expected)


def test_angle_of_inclination_large_values():
    # Should work for large values
    result = _angle_of_inclination_from_horizontal_length_and_lift(1e6, 1e6)
    expected = math.atan2(1e6, 1e6)  # Expect radians
    assert result == pytest.approx(expected)


def test_angle_of_inclination_large_values_in_degrees():
    # This test was expecting degrees, but the function returns radians.
    # Updated to correctly compare the result in radians.
    result = _angle_of_inclination_from_horizontal_length_and_lift(1e6, 1e6)
    expected = math.atan2(1e6, 1e6)  # Expect radians
    assert result == pytest.approx(expected)


def test_radius_from_translatory_speed_and_revolutions_typical():
    translatory_speed = 6.7  # m/s
    revolutions = 121.867 / 60  # /rps
    expected_radius = 1.05 / 2  # m
    assert _radius_from_translatory_speed_and_revolutions(
        translatory_speed, revolutions
    ) == pytest.approx(expected_radius, rel=1e-2)


def test_radius_from_translatory_speed_and_revolutions_zero_translatory_speed():
    translatory_speed = 0.0
    revolutions = 2.0
    expected_radius = 0.0
    assert (
        _radius_from_translatory_speed_and_revolutions(translatory_speed, revolutions)
        == expected_radius
    )


def test_radius_from_translatory_speed_and_revolutions_zero_revolutions():
    translatory_speed = 10.0
    revolutions = 0.0
    with pytest.raises(ValueError, match="revolutions must be positive"):
        _radius_from_translatory_speed_and_revolutions(translatory_speed, revolutions)


def test_radius_from_translatory_speed_and_revolutions_negative_translatory_speed():
    translatory_speed = -10.0
    revolutions = 2.0
    expected_radius = -10.0 / (2 * pi * 2.0)
    assert (
        _radius_from_translatory_speed_and_revolutions(translatory_speed, revolutions)
        == expected_radius
    )


def test_radius_from_translatory_speed_and_revolutions_negative_revolutions():
    translatory_speed = 10.0
    revolutions = -2.0
    with pytest.raises(ValueError, match="revolutions must be positive"):
        _radius_from_translatory_speed_and_revolutions(translatory_speed, revolutions)


def test_pulley_diameter_typical_values():
    belt_speed = 6.7  # m/s
    revolutions = 121.867 / 60  # rps
    expected_diameter = 1.05  # m
    assert _pulley_diameter_from_belt_speed_and_revolutions(
        belt_speed, revolutions
    ) == pytest.approx(expected_diameter, rel=1e-2)


def test_pulley_diameter_zero_belt_speed():
    belt_speed = 0.0
    revolutions = 10.0
    with pytest.raises(ValueError):
        _pulley_diameter_from_belt_speed_and_revolutions(belt_speed, revolutions)


def test_pulley_diameter_zero_revolutions():
    belt_speed = 10.0
    revolutions = 0.0
    with pytest.raises(ValueError):
        _pulley_diameter_from_belt_speed_and_revolutions(belt_speed, revolutions)


def test_pulley_diameter_negative_belt_speed():
    belt_speed = -10.0
    revolutions = 2.0
    with pytest.raises(ValueError):
        _pulley_diameter_from_belt_speed_and_revolutions(belt_speed, revolutions)


def test_pulley_diameter_negative_revolutions():
    belt_speed = 10.0
    revolutions = -2.0
    with pytest.raises(ValueError):
        _pulley_diameter_from_belt_speed_and_revolutions(belt_speed, revolutions)


def test_pulley_diameter_both_negative():
    belt_speed = -10.0
    revolutions = -2.0
    with pytest.raises(ValueError, match="revolutions must be positive"):
        _pulley_diameter_from_belt_speed_and_revolutions(belt_speed, revolutions)
