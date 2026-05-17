import pytest
from eytelwein.din_22101.core._minimum_pulley_diameter import (
    _minimum_diameter_of_group_A_pulleys,
    _pulley_load_factor,
)
from eytelwein.din_22101.core._minimum_pulley_diameter import (
    _minimum_diameter_of_group_A_B_C_pulleys,
    _get_max_width_related_tension_at_group_A_pulleys,
)
from eytelwein.din_22101.constants import PulleyLoadFactor


def test_minimum_diameter_of_group_A_pulleys_valid_input():
    assert _minimum_diameter_of_group_A_pulleys(10, 2.5) == 25.0


def test_minimum_diameter_of_group_A_pulleys_zero_coefficient():
    assert _minimum_diameter_of_group_A_pulleys(0, 2.5) == 0.0


def test_minimum_diameter_of_group_A_pulleys_zero_thickness():
    assert _minimum_diameter_of_group_A_pulleys(10, 0.0) == 0.0


def test_minimum_diameter_of_group_A_pulleys_negative_coefficient():
    assert _minimum_diameter_of_group_A_pulleys(-10, 2.5) == -25.0


def test_minimum_diameter_of_group_A_pulleys_negative_thickness():
    assert _minimum_diameter_of_group_A_pulleys(10, -2.5) == -25.0


def test_minimum_diameter_of_group_A_pulleys_large_values():
    assert _minimum_diameter_of_group_A_pulleys(1000000, 1000000.0) == 1000000000000.0


def test_pulley_load_factor_valid_input():
    result = _pulley_load_factor(200.0, 1000.0)
    assert result == 160.0


def test_pulley_load_factor_valid_input2():
    result = _pulley_load_factor(100.0, 1000.0)
    assert result == 80.0


def test_pulley_load_factor_zero_tension():
    result = _pulley_load_factor(0.0, 1000.0)
    assert result == 0.0


def ptest_ulley_load_factor_zero_strength():
    with pytest.raises(ZeroDivisionError):
        _pulley_load_factor(200.0, 0.0)


def test_pulley_load_factor_negative_tension():
    result = _pulley_load_factor(-200.0, 1000.0)
    assert result == -160.0


def test_pulley_load_factor_negative_strength():
    result = _pulley_load_factor(200.0, -1000.0)
    assert result == -160.0


def test_minimum_diameter_valid_data():
    result = _minimum_diameter_of_group_A_B_C_pulleys(125, PulleyLoadFactor.above_100)
    assert result == {"A": 160, "B": 125, "C": 100}


def test_minimum_diameter_missing_data():
    result = _minimum_diameter_of_group_A_B_C_pulleys(100, PulleyLoadFactor.above_100)
    assert result == {"A": 125, "B": 100, "C": None}


def test_minimum_diameter_no_data():
    result = _minimum_diameter_of_group_A_B_C_pulleys(80, PulleyLoadFactor.above_100)
    assert result == {"A": None, "B": None, "C": None}


def test_get_max_width_related_tension_valid_values():
    result = _get_max_width_related_tension_at_group_A_pulleys(800)
    assert result == 100.0


def test_get_max_width_related_tension_custom_pulley_load_factor():
    result = _get_max_width_related_tension_at_group_A_pulleys(
        800, PulleyLoadFactor.above_30_up_to_60
    )
    assert result == 60.0


def test_get_max_width_related_tension_zero_nominal_belt_strength():
    result = _get_max_width_related_tension_at_group_A_pulleys(0)
    assert result == 0.0


def test_get_max_width_related_tension_invalid_nominal_belt_strength():
    with pytest.raises(TypeError):
        _get_max_width_related_tension_at_group_A_pulleys("invalid_value")


def test_get_max_width_related_tension_invalid_pulley_load_factor():
    with pytest.raises(AttributeError):
        _get_max_width_related_tension_at_group_A_pulleys(800, "invalid_value")


if __name__ == "__main__":
    test_minimum_diameter_of_group_A_pulleys_valid_input()
    test_minimum_diameter_of_group_A_pulleys_zero_coefficient()
    test_minimum_diameter_of_group_A_pulleys_zero_thickness()
    test_minimum_diameter_of_group_A_pulleys_negative_coefficient()
    test_minimum_diameter_of_group_A_pulleys_negative_thickness()
    test_minimum_diameter_of_group_A_pulleys_large_values()
    test_pulley_load_factor_valid_input()
    test_pulley_load_factor_valid_input2
    test_pulley_load_factor_zero_tension()
    test_pulley_load_factor_negative_tension()
    test_pulley_load_factor_negative_strength()
    print("All tests passed!")
