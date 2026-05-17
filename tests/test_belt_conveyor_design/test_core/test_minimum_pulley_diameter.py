import pytest
from eytelwein.belt_conveyor_design.constants import MinimumPulleyDiameterCoefficient

from eytelwein.belt_conveyor_design.core.minimum_pulley_diameter import (
    minimum_diameter_of_group_A_pulleys,
    pulley_load_factor,
    minimum_diameter_of_group_A_B_C_pulleys,
    get_max_width_related_tension_at_group_A_pulleys,
)

from eytelwein.belt_conveyor_design.constants import PulleyLoadFactor

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def test_minimum_diameter_of_group_A_pulleys_valid_input():
    coefficient = MinimumPulleyDiameterCoefficient.B
    thickness = 5 * u.mm
    result = minimum_diameter_of_group_A_pulleys(coefficient, thickness)
    assert result.magnitude == 400
    assert result.units == u.mm


def test_minimum_diameter_of_group_A_pulleys_invalid_thickness():
    coefficient = MinimumPulleyDiameterCoefficient.B
    thickness = 5 * u.second
    with pytest.raises(ValueError):
        minimum_diameter_of_group_A_pulleys(coefficient, thickness)


def test_minimum_diameter_of_group_A_pulleys_invalid_unit():
    coefficient = MinimumPulleyDiameterCoefficient.B
    thickness = 5 * u.mm
    with pytest.raises(ValueError):
        minimum_diameter_of_group_A_pulleys(coefficient, thickness, unit="invalid")


def test_minimum_diameter_of_group_A_pulleys_with_precision():
    coefficient = MinimumPulleyDiameterCoefficient.B
    thickness = 5 * u.mm
    result = minimum_diameter_of_group_A_pulleys(coefficient, thickness, precision=2)
    assert result.magnitude == 400.00
    assert result.units == u.mm


def test_minimum_diameter_of_group_A_pulleys_with_different_unit():
    coefficient = MinimumPulleyDiameterCoefficient.B
    thickness = 5 * u.mm
    result = minimum_diameter_of_group_A_pulleys(coefficient, thickness, unit="meter")
    assert result.magnitude == 0.4
    assert result.units == u.m


def test_pulley_load_factor_valid_input():
    result = pulley_load_factor(200 * u.kilonewton, 1000 * u.kilonewton)
    assert result == 160.0


def test_pulley_load_factor_zero_tension():
    result = pulley_load_factor(0 * u.kilonewton, 1000 * u.kilonewton)
    assert result == 0.0


def test_pulley_load_factor_zero_strength():
    with pytest.raises(ZeroDivisionError):
        pulley_load_factor(200 * u.kilonewton, 0 * u.kilonewton)


def test_pulley_load_factor_negative_tension():
    result = pulley_load_factor(-200 * u.kilonewton, 1000 * u.kilonewton)
    assert result == -160.0


def test_pulley_load_factor_negative_strength():
    result = pulley_load_factor(200 * u.kilonewton, -1000 * u.kilonewton)
    assert result == -160.0


def test_pulley_load_factor_invalid_unit():
    with pytest.raises(ValueError):
        pulley_load_factor(200 * u.meter, 1000 * u.kilonewton)


def test_minimum_diameter_valid_data():
    result = minimum_diameter_of_group_A_B_C_pulleys(
        125 * u.mm, PulleyLoadFactor.above_100
    )
    assert result == {"A": 160 * u.mm, "B": 125 * u.mm, "C": 100 * u.mm}


def test_minimum_diameter_missing_data():
    result = minimum_diameter_of_group_A_B_C_pulleys(
        100 * u.mm, PulleyLoadFactor.above_100
    )
    assert result == {"A": 125 * u.mm, "B": 100 * u.mm, "C": None}


def test_minimum_diameter_no_data():
    result = minimum_diameter_of_group_A_B_C_pulleys(
        80 * u.mm, PulleyLoadFactor.above_100
    )
    assert result == {"A": None, "B": None, "C": None}


def test_get_max_width_related_tension_valid_values():
    result = get_max_width_related_tension_at_group_A_pulleys(
        800 * u.newton / u.millimeter
    )
    assert result.magnitude == 100.00
    assert result.units == u.newton / u.millimeter


def test_get_max_width_related_tension_custom_unit():
    result = get_max_width_related_tension_at_group_A_pulleys(
        800 * u.newton / u.millimeter, unit="kilonewton / millimeter"
    )
    assert result.magnitude == 0.10
    assert result.units == u.kilonewton / u.millimeter


def test_get_max_width_related_tension_custom_precision():
    result = get_max_width_related_tension_at_group_A_pulleys(
        800 * u.newton / u.millimeter, precision=3
    )
    assert result.magnitude == 100.000  # Replace with the expected value
    assert result.units == u.newton / u.millimeter


def test_get_max_width_related_tension_invalid_unit():
    with pytest.raises(ValueError):
        get_max_width_related_tension_at_group_A_pulleys(
            100 * u.newton / u.millimeter, unit="invalid_unit"
        )


def test_get_max_width_related_tension_invalid_nominal_belt_strength():
    with pytest.raises(ValueError):
        get_max_width_related_tension_at_group_A_pulleys("invalid_value")


if __name__ == "__main__":
    test_minimum_diameter_of_group_A_pulleys_valid_input()
    test_minimum_diameter_of_group_A_pulleys_invalid_thickness()
    test_minimum_diameter_of_group_A_pulleys_invalid_unit()
    test_minimum_diameter_of_group_A_pulleys_with_precision()
    test_minimum_diameter_of_group_A_pulleys_with_different_unit()
    test_pulley_load_factor_valid_input()
    test_pulley_load_factor_zero_tension()
    test_pulley_load_factor_zero_strength()
    test_pulley_load_factor_negative_tension()
    test_pulley_load_factor_negative_strength()
    test_pulley_load_factor_invalid_unit()
