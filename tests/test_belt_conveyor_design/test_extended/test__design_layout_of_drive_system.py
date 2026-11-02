from math import pi
import math

import pytest
from eytelwein.belt_conveyor_design.extended._design_layout_of_drive_system import (
    _angle_of_inclination_from_horizontal_length_and_lift,
    _belt_speed_from_motor_revolutions_gear_ratio_and_pulley_diameter,
    _belt_speed_from_pulley_revolutions,
    _effective_pulley_diameter_from_shell_diameter_and_lagging_thickness,
    _gear_ratio_from_belt_speed_motor_revolutions_and_pulley_diameter,
    _gear_ratio_from_motor_revolutions_and_pulley_revolutions,
    _lagging_thickness_from_effective_and_shell_diameter,
    _mechanical_power_from_torque_and_belt_speed,
    _mechanical_power_from_torque_and_revolutions,
    _mechanical_torque_from_belt_force,
    _motor_revolutions_from_belt_speed_gear_ratio_and_pulley_diameter,
    _motor_revolutions_from_pulley_revolutions_and_gear_ratio,
    _motor_revolutions_from_synchronous_revolutions_and_slip,
    _number_of_revolutions_from_translatory_speed,
    _pulley_diameter_from_belt_speed_and_revolutions,
    _pulley_diameter_from_belt_speed_motor_revolutions_and_gear_ratio,
    _pulley_revolutions_from_belt_speed,
    _pulley_revolutions_from_motor_revolutions_and_gear_ratio,
    _radius_from_translatory_speed_and_revolutions,
    _revolutions_from_mechanical_power_and_torque,
    _shell_diameter_from_effective_pulley_diameter_and_lagging_thickness,
    _slip_from_synchronous_revolutions_and_motor_revolutions,
    _synchronous_revolutions_from_supply_frequency_and_pole_pairs,
    _torque_from_mechanical_power_and_revolutions,
    _translatory_speed_from_number_of_revolutions,
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


# Reference case (SI units): D_shell = 1.05 m, t = 0.015 m -> D_eff = 1.08 m;
# f = 50 Hz, p = 2 -> n_sync = 25 rps (1500 rpm); n_m = 1442 rpm;
# v = 6.7 m/s -> n_p = v / (pi * D_eff) ~ 118.48 rpm; i = n_m / n_p ~ 12.17.
D_EFF = 1.08
N_SYNC = 25.0
N_MOTOR = 1442.0 / 60
SLIP = (1500.0 - 1442.0) / 1500.0
BELT_SPEED = 6.7
N_PULLEY = BELT_SPEED / (pi * D_EFF)
GEAR_RATIO = 12.17


class TestDriveTrainKinematicsPrivate:
    """Private drive-train kinematics helpers (raw floats, SI units)."""

    def test_effective_pulley_diameter_from_shell_and_lagging(self):
        """Test D_eff = D_shell + 2 * t_lagging."""
        result = _effective_pulley_diameter_from_shell_diameter_and_lagging_thickness(
            1.05, 0.015
        )
        assert result == pytest.approx(1.08)

    def test_effective_pulley_diameter_zero_lagging(self):
        """Test zero lagging returns the shell diameter."""
        result = _effective_pulley_diameter_from_shell_diameter_and_lagging_thickness(
            1.05, 0.0
        )
        assert result == pytest.approx(1.05)

    def test_shell_diameter_from_effective_and_lagging(self):
        """Test D_shell = D_eff - 2 * t_lagging."""
        result = _shell_diameter_from_effective_pulley_diameter_and_lagging_thickness(
            1.08, 0.015
        )
        assert result == pytest.approx(1.05)

    def test_shell_diameter_lagging_too_thick(self):
        """Test lagging consuming the whole diameter is rejected."""
        with pytest.raises(
            ValueError, match="must exceed twice the lagging_thickness, got"
        ):
            _shell_diameter_from_effective_pulley_diameter_and_lagging_thickness(
                0.03, 0.015
            )

    def test_lagging_thickness_from_effective_and_shell_diameter(self):
        """Test t_lagging = (D_eff - D_shell) / 2."""
        result = _lagging_thickness_from_effective_and_shell_diameter(1.08, 1.05)
        assert result == pytest.approx(0.015)

    def test_lagging_thickness_equal_diameters(self):
        """Test equal diameters give zero lagging."""
        result = _lagging_thickness_from_effective_and_shell_diameter(1.05, 1.05)
        assert result == pytest.approx(0.0)

    def test_lagging_thickness_effective_smaller_than_shell(self):
        """Test effective diameter below shell diameter is rejected."""
        with pytest.raises(
            ValueError, match="greater than or equal to shell_diameter, got"
        ):
            _lagging_thickness_from_effective_and_shell_diameter(1.0, 1.05)

    def test_pulley_revolutions_from_motor_revolutions_and_gear_ratio(self):
        """Test n_pulley = n_motor / i."""
        result = _pulley_revolutions_from_motor_revolutions_and_gear_ratio(
            N_MOTOR, GEAR_RATIO
        )
        assert result == pytest.approx(N_MOTOR / GEAR_RATIO)
        assert result == pytest.approx(N_PULLEY, rel=1e-3)

    def test_pulley_revolutions_zero_gear_ratio(self):
        """Test zero gear ratio denominator is rejected."""
        with pytest.raises(ValueError, match="gear_ratio must be positive, got 0.0"):
            _pulley_revolutions_from_motor_revolutions_and_gear_ratio(24.0, 0.0)

    def test_motor_revolutions_from_pulley_revolutions_and_gear_ratio(self):
        """Test n_motor = n_pulley * i."""
        result = _motor_revolutions_from_pulley_revolutions_and_gear_ratio(
            N_PULLEY, GEAR_RATIO
        )
        assert result == pytest.approx(N_PULLEY * GEAR_RATIO)
        assert result == pytest.approx(N_MOTOR, rel=1e-3)

    def test_gear_ratio_from_motor_and_pulley_revolutions(self):
        """Test i = n_motor / n_pulley."""
        result = _gear_ratio_from_motor_revolutions_and_pulley_revolutions(
            N_MOTOR, N_PULLEY
        )
        assert result == pytest.approx(12.1706237, rel=1e-6)
        assert round(result, 2) == GEAR_RATIO

    def test_gear_ratio_zero_pulley_revolutions(self):
        """Test zero pulley revolutions denominator is rejected."""
        with pytest.raises(
            ValueError, match="pulley_revolutions must be positive, got 0.0"
        ):
            _gear_ratio_from_motor_revolutions_and_pulley_revolutions(1442.0, 0.0)

    def test_synchronous_revolutions_from_supply_frequency_and_pole_pairs(self):
        """Test n_sync = f / p."""
        result = _synchronous_revolutions_from_supply_frequency_and_pole_pairs(50.0, 2)
        assert result == pytest.approx(25.0)

    def test_synchronous_revolutions_zero_pole_pairs(self):
        """Test zero pole pairs denominator is rejected."""
        with pytest.raises(ValueError, match="pole_pairs must be positive, got 0"):
            _synchronous_revolutions_from_supply_frequency_and_pole_pairs(50.0, 0)

    def test_motor_revolutions_from_sync_and_slip(self):
        """Test n_motor = n_sync * (1 - s)."""
        result = _motor_revolutions_from_synchronous_revolutions_and_slip(N_SYNC, SLIP)
        assert result == pytest.approx(N_MOTOR)

    def test_slip_from_sync_and_motor_revolutions(self):
        """Test s = (n_sync - n_motor) / n_sync."""
        result = _slip_from_synchronous_revolutions_and_motor_revolutions(
            N_SYNC, N_MOTOR
        )
        assert result == pytest.approx(0.0386667, rel=1e-5)

    def test_slip_zero_synchronous_revolutions(self):
        """Test zero synchronous speed denominator is rejected."""
        with pytest.raises(
            ValueError, match="synchronous_revolutions must be positive, got 0.0"
        ):
            _slip_from_synchronous_revolutions_and_motor_revolutions(0.0, 0.0)

    def test_slip_motor_above_synchronous(self):
        """Test motor speed above synchronous speed is rejected."""
        with pytest.raises(
            ValueError, match="must not exceed synchronous_revolutions, got"
        ):
            _slip_from_synchronous_revolutions_and_motor_revolutions(25.0, 26.0)

    def test_belt_speed_from_motor_revolutions_gear_ratio_and_pulley_diameter(self):
        """Test v = pi * D_eff * n_motor / i."""
        result = _belt_speed_from_motor_revolutions_gear_ratio_and_pulley_diameter(
            N_MOTOR, GEAR_RATIO, D_EFF
        )
        assert result == pytest.approx(pi * D_EFF * N_MOTOR / GEAR_RATIO)
        assert result == pytest.approx(BELT_SPEED, rel=1e-3)

    def test_belt_speed_zero_gear_ratio(self):
        """Test zero gear ratio denominator is rejected."""
        with pytest.raises(ValueError, match="gear_ratio must be positive, got 0.0"):
            _belt_speed_from_motor_revolutions_gear_ratio_and_pulley_diameter(
                24.0, 0.0, 1.08
            )

    def test_gear_ratio_from_belt_speed_motor_revolutions_and_pulley_diameter(self):
        """Test i = pi * D_eff * n_motor / v."""
        result = _gear_ratio_from_belt_speed_motor_revolutions_and_pulley_diameter(
            BELT_SPEED, N_MOTOR, D_EFF
        )
        assert result == pytest.approx(pi * D_EFF * N_MOTOR / BELT_SPEED)
        assert result == pytest.approx(GEAR_RATIO, rel=1e-3)

    def test_gear_ratio_zero_belt_speed(self):
        """Test zero belt speed denominator is rejected."""
        with pytest.raises(ValueError, match="belt_speed must be positive, got 0.0"):
            _gear_ratio_from_belt_speed_motor_revolutions_and_pulley_diameter(
                0.0, 24.0, 1.08
            )

    def test_pulley_diameter_from_belt_speed_motor_revolutions_and_gear_ratio(self):
        """Test D_eff = v * i / (pi * n_motor)."""
        result = _pulley_diameter_from_belt_speed_motor_revolutions_and_gear_ratio(
            BELT_SPEED, N_MOTOR, GEAR_RATIO
        )
        assert result == pytest.approx(BELT_SPEED * GEAR_RATIO / (pi * N_MOTOR))
        assert result == pytest.approx(D_EFF, rel=1e-3)

    def test_pulley_diameter_zero_motor_revolutions(self):
        """Test zero motor revolutions denominator is rejected."""
        with pytest.raises(
            ValueError, match="motor_revolutions must be positive, got 0.0"
        ):
            _pulley_diameter_from_belt_speed_motor_revolutions_and_gear_ratio(
                6.7, 0.0, 12.17
            )

    def test_motor_revolutions_from_belt_speed_gear_ratio_and_pulley_diameter(self):
        """Test n_motor = v * i / (pi * D_eff)."""
        result = _motor_revolutions_from_belt_speed_gear_ratio_and_pulley_diameter(
            BELT_SPEED, GEAR_RATIO, D_EFF
        )
        assert result == pytest.approx(BELT_SPEED * GEAR_RATIO / (pi * D_EFF))
        assert result == pytest.approx(N_MOTOR, rel=1e-3)

    def test_motor_revolutions_zero_pulley_diameter(self):
        """Test zero pulley diameter denominator is rejected."""
        with pytest.raises(
            ValueError, match="pulley_diameter must be positive, got 0.0"
        ):
            _motor_revolutions_from_belt_speed_gear_ratio_and_pulley_diameter(
                6.7, 12.17, 0.0
            )
