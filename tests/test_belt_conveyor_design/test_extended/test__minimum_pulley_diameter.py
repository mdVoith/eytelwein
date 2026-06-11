import math

from eytelwein.belt_conveyor_design.extended._minimum_pulley_diameter import (
    _resulting_force_from_belt_tensions_and_wrap_angle,
)


def test_resulting_force_from_belt_tensions_and_wrap_angle_general_case():
    """Test with typical belt tensions and a 60-degree wrap angle."""
    belt_tension_upper_n = 5000.0
    belt_tension_lower_n = 2000.0
    wrap_angle_rad = math.pi / 3  # 60 degrees

    result = _resulting_force_from_belt_tensions_and_wrap_angle(
        belt_tension_upper_n, belt_tension_lower_n, wrap_angle_rad
    )

    # F_T = sqrt((T1 - T2*cos(alpha))^2 + (T2*sin(alpha))^2)
    # F_T = sqrt((5000 - 2000*cos(pi/3))^2 + (2000*sin(pi/3))^2)
    # F_T = sqrt((5000 - 2000*0.5)^2 + (2000*sqrt(3)/2)^2)
    # F_T = sqrt(4000^2 + (1000*sqrt(3))^2)
    # F_T = sqrt(16000000 + 3000000)
    # F_T = sqrt(19000000)
    expected = math.sqrt(4000**2 + (1000 * math.sqrt(3))**2)
    assert abs(result - expected) < 1e-9


def test_resulting_force_from_belt_tensions_and_wrap_angle_zero_wrap():
    """Test with zero wrap angle."""
    belt_tension_upper_n = 5000.0
    belt_tension_lower_n = 2000.0
    wrap_angle_rad = 0.0

    result = _resulting_force_from_belt_tensions_and_wrap_angle(
        belt_tension_upper_n, belt_tension_lower_n, wrap_angle_rad
    )

    # F_T = sqrt((T1 - T2*cos(0))^2 + (T2*sin(0))^2)
    # F_T = sqrt((5000 - 2000*1)^2 + (2000*0)^2)
    # F_T = sqrt(3000^2 + 0)
    # F_T = 3000.0
    expected = 3000.0
    assert result == expected


def test_resulting_force_from_belt_tensions_and_wrap_angle_right_angle_wrap():
    """Test with 90-degree wrap angle."""
    belt_tension_upper_n = 5000.0
    belt_tension_lower_n = 2000.0
    wrap_angle_rad = math.pi / 2  # 90 degrees

    result = _resulting_force_from_belt_tensions_and_wrap_angle(
        belt_tension_upper_n, belt_tension_lower_n, wrap_angle_rad
    )

    # F_T = sqrt((T1 - T2*cos(pi/2))^2 + (T2*sin(pi/2))^2)
    # F_T = sqrt((5000 - 2000*0)^2 + (2000*1)^2)
    # F_T = sqrt(5000^2 + 2000^2)
    # F_T = sqrt(25000000 + 4000000)
    # F_T = sqrt(29000000)
    # F_T ≈ 5385.1646...
    expected = math.sqrt(5000**2 + 2000**2)
    assert abs(result - expected) < 1e-9


def test_resulting_force_from_belt_tensions_and_wrap_angle_half_turn_wrap():
    """Test with half-turn (pi radians) wrap angle."""
    belt_tension_upper_n = 3000.0
    belt_tension_lower_n = 1000.0
    wrap_angle_rad = math.pi

    result = _resulting_force_from_belt_tensions_and_wrap_angle(
        belt_tension_upper_n, belt_tension_lower_n, wrap_angle_rad
    )

    # F_T = sqrt((T1 - T2*cos(pi))^2 + (T2*sin(pi))^2)
    # F_T = sqrt((3000 - 1000*(-1))^2 + (1000*0)^2)
    # F_T = sqrt((3000 + 1000)^2 + 0)
    # F_T = sqrt(16000000)
    # F_T = 4000.0
    expected = 4000.0
    assert result == expected


def test_resulting_force_from_equal_belt_tensions_and_half_turn_wrap():
    """Test that equal tensions at 180-degree wrap yield twice the tension."""
    belt_tension_upper_n = 2500.0
    belt_tension_lower_n = 2500.0
    wrap_angle_rad = math.pi

    result = _resulting_force_from_belt_tensions_and_wrap_angle(
        belt_tension_upper_n, belt_tension_lower_n, wrap_angle_rad
    )

    # F_T = sqrt((T1 - T1*cos(pi))^2 + (T1*sin(pi))^2)
    # F_T = sqrt((T1 - T1*(-1))^2 + 0)
    # F_T = sqrt((2*T1)^2)
    # F_T = 2*T1
    expected = 2 * belt_tension_upper_n
    assert result == expected
