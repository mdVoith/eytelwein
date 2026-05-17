from math import pi
import math

import pytest
from eytelwein.din_22101.extended.design_layout_of_drive_system import (
    angle_of_inclination_from_horizontal_length_and_lift,
    mechanical_torque_from_belt_force,
    mechanical_power_from_torque_and_belt_speed,
    number_of_revolutions_from_translatory_speed,
    pulley_revolutions_from_belt_speed,
    translatory_speed_from_number_of_revolutions,
    belt_speed_from_pulley_revolutions,
    mechanical_power_from_torque_and_revolutions,
    torque_from_mechanical_power_and_revolutions,
    revolutions_from_mechanical_power_and_torque,
    pulley_diameter_from_belt_speed_and_revolutions,
    radius_from_translatory_speed_and_revolutions,
)
from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def test_mechanical_torque_valid_values():
    result = mechanical_torque_from_belt_force(100 * u.newton, 0.5 * u.meter)
    assert result.magnitude == 25.0
    assert result.units == u.newton * u.meter


def test_mechanical_torque_valid_values_unit():
    result = mechanical_torque_from_belt_force(
        100 * u.newton, 0.5 * u.meter, unit="kilonewton * meter", precision=3
    )
    assert result.magnitude == 25.0 / 1000
    assert result.units == u.kilonewton * u.meter


def test_mechanical_torque_zero_belt_force():
    result = mechanical_torque_from_belt_force(0 * u.newton, 0.5 * u.meter)
    assert result.magnitude == 0.0
    assert result.units == u.newton * u.meter


def test_mechanical_torque_zero_pulley_diameter():
    result = mechanical_torque_from_belt_force(100 * u.newton, 0 * u.meter)
    assert result.magnitude == 0.0
    assert result.units == u.newton * u.meter


def test_mechanical_torque_invalid_unit():
    with pytest.raises(ValueError):
        mechanical_torque_from_belt_force(
            100 * u.newton, 0.5 * u.meter, unit="invalid_unit"
        )


def test_mechanical_torque_invalid_belt_force():
    with pytest.raises(ValueError):
        mechanical_torque_from_belt_force("invalid_value", 0.5 * u.meter)


def test_mechanical_torque_invalid_pulley_diameter():
    with pytest.raises(ValueError):
        mechanical_torque_from_belt_force(100 * u.newton, "invalid_value")


def test_mechanical_torque_precision():
    result = mechanical_torque_from_belt_force(
        100 * u.newton, 0.5 * u.meter, precision=3
    )
    assert result.magnitude == 25.000
    assert result.units == u.newton * u.meter


def test_mechanical_power_valid_values():
    result = mechanical_power_from_torque_and_belt_speed(
        100 * u.newton * u.meter, 5 * u.meter / u.second, 2 * u.meter
    )
    assert result.magnitude == 500.0 / 1000
    assert result.units == u.kilowatt


def test_mechanical_power_zero_torque():
    result = mechanical_power_from_torque_and_belt_speed(
        0 * u.newton * u.meter, 5 * u.meter / u.second, 2 * u.meter
    )
    assert result.magnitude == 0.0
    assert result.units == u.kilowatt


def test_mechanical_power_zero_belt_speed():
    result = mechanical_power_from_torque_and_belt_speed(
        100 * u.newton * u.meter, 0 * u.meter / u.second, 2 * u.meter
    )
    assert result.magnitude == 0.0
    assert result.units == u.kilowatt


def test_mechanical_power_zero_pulley_diameter():
    with pytest.raises(ValueError):
        mechanical_power_from_torque_and_belt_speed(
            100 * u.newton * u.meter, 5 * u.meter / u.second, 0 * u.meter
        )


def test_mechanical_power_invalid_unit():
    with pytest.raises(ValueError):
        mechanical_power_from_torque_and_belt_speed(
            100 * u.newton * u.meter,
            5 * u.meter / u.second,
            2 * u.meter,
            unit="invalid_unit",
        )


def test_mechanical_power_invalid_torque():
    with pytest.raises(ValueError):
        mechanical_power_from_torque_and_belt_speed(
            "invalid_value", 5 * u.meter / u.second, 2 * u.meter
        )


def test_mechanical_power_invalid_belt_speed():
    with pytest.raises(ValueError):
        mechanical_power_from_torque_and_belt_speed(
            100 * u.newton * u.meter, "invalid_value", 2 * u.meter
        )


def test_mechanical_power_invalid_pulley_diameter():
    with pytest.raises(ValueError):
        mechanical_power_from_torque_and_belt_speed(
            100 * u.newton * u.meter, 5 * u.meter / u.second, "invalid_value"
        )


def test_mechanical_power_precision():
    result = mechanical_power_from_torque_and_belt_speed(
        100 * u.newton * u.meter, 5 * u.meter / u.second, 2 * u.meter, precision=3
    )
    assert result.magnitude == 500.000 / 1000
    assert result.units == u.kilowatt


def test_calculates_revolutions_correctly():
    translatory_speed = 10 * u.meter / u.second
    radius = 0.5 * u.meter
    expected_revolutions = round((10 / (2 * pi * 0.5)), 2) * u.revolution / u.second
    assert (
        number_of_revolutions_from_translatory_speed(translatory_speed, radius)
        == expected_revolutions
    )


def test_calculates_revolutions_correctly_with_precision():
    translatory_speed = 10 * u.meter / u.second
    radius = 0.5 * u.meter
    expected_revolutions = round((10 / (2 * pi * 0.5)), 3) * u.revolution / u.second
    assert (
        number_of_revolutions_from_translatory_speed(
            translatory_speed, radius, precision=3
        )
        == expected_revolutions
    )


def test_calculates_revolutions_correctly_with_no_precision():
    translatory_speed = 10 * u.meter / u.second
    radius = 0.5 * u.meter
    expected_revolutions = (10 / (2 * pi * 0.5)) * u.revolution / u.second
    assert (
        number_of_revolutions_from_translatory_speed(
            translatory_speed, radius, precision=None
        )
        == expected_revolutions
    )


def test_calculates_revolutions_correctly_and_converts_to_rpm():
    translatory_speed = 10 * u.meter / u.second
    radius = 0.5 * u.meter
    expected_revolutions = (10 / (2 * pi * 0.5)) * u.revolution / u.second
    assert number_of_revolutions_from_translatory_speed(
        translatory_speed, radius, unit="rpm"
    ) == round(expected_revolutions.to(u.rpm), 2)


def test_handles_zero_translatory_speed():
    translatory_speed = 0 * u.meter / u.second
    radius = 0.5 * u.meter
    expected_revolutions = 0 * u.revolution / u.second
    assert number_of_revolutions_from_translatory_speed(
        translatory_speed, radius
    ) == expected_revolutions.to(u.rpm)


def test_handles_zero_radius():
    translatory_speed = 10 * u.meter / u.second
    radius = 0 * u.meter
    with pytest.raises(ValueError):
        number_of_revolutions_from_translatory_speed(translatory_speed, radius)


def test_handles_negative_translatory_speed():
    translatory_speed = -10 * u.meter / u.second
    radius = 0.5 * u.meter
    expected_revolutions = round((-10 / (2 * pi * 0.5)), 2) * u.revolution / u.second
    assert number_of_revolutions_from_translatory_speed(
        translatory_speed, radius
    ) == expected_revolutions.to(u.rps)


def test_calculates_pulley_revolutions_correctly():
    belt_speed = 5 * u.meter / u.second
    pulley_diameter = 0.5 * u.meter
    expected_revolutions = round((5 / (pi * 0.5)), 2) * u.revolution / u.second
    assert (
        pulley_revolutions_from_belt_speed(belt_speed, pulley_diameter)
        == expected_revolutions
    )


def test_handles_zero_belt_speed():
    belt_speed = 0 * u.meter / u.second
    pulley_diameter = 0.5 * u.meter
    expected_revolutions = 0 * u.revolution / u.second
    assert (
        pulley_revolutions_from_belt_speed(belt_speed, pulley_diameter)
        .to(u.rpm)
        .magnitude
        == expected_revolutions.to(u.rpm).magnitude
    )


def test_handles_zero_pulley_diameter():
    belt_speed = 5 * u.meter / u.second
    pulley_diameter = 0 * u.meter
    with pytest.raises(ValueError):
        pulley_revolutions_from_belt_speed(belt_speed, pulley_diameter)


def test_handles_negative_belt_speed():
    belt_speed = -5 * u.meter / u.second
    pulley_diameter = 0.5 * u.meter
    expected_revolutions = (-5 / (pi * 0.5)) * (u.revolution / u.second)
    assert (
        pulley_revolutions_from_belt_speed(belt_speed, pulley_diameter, precision=None)
        == expected_revolutions
    )


def test_handles_negative_pulley_diameter():
    belt_speed = 5 * u.meter / u.second
    pulley_diameter = -0.5 * u.meter
    with pytest.raises(ValueError):
        pulley_revolutions_from_belt_speed(belt_speed, pulley_diameter)


def test_calculates_translatory_speed_correctly():
    revolutions = 10 * u.revolution / u.second
    radius = 0.5 * u.meter
    expected_speed = round((10 * 2 * pi * 0.5), 2) * u.meter / u.second
    assert (
        translatory_speed_from_number_of_revolutions(revolutions, radius)
        .to(u.meter / u.second)
        .magnitude
        == expected_speed.magnitude
    )


def test_calculates_translatory_speed_and_precision_correctly():
    revolutions = 10 * u.revolution / u.second
    radius = 0.5 * u.meter
    expected_speed = round((10 * 2 * pi * 0.5), 3) * u.meter / u.second
    assert (
        translatory_speed_from_number_of_revolutions(revolutions, radius, precision=3)
        .to(u.meter / u.second)
        .magnitude
        == expected_speed.magnitude
    )


def test_handles_zero_revolutions():
    revolutions = 0 * u.revolution / u.second
    radius = 0.5 * u.meter
    expected_speed = 0 * u.meter / u.second
    assert (
        translatory_speed_from_number_of_revolutions(revolutions, radius)
        .to(u.meter / u.second)
        .magnitude
        == expected_speed.magnitude
    )


def test_handles_zero_radius2():
    revolutions = 10 * u.revolution / u.second
    radius = 0 * u.meter
    with pytest.raises(ValueError):
        translatory_speed_from_number_of_revolutions(revolutions, radius)


def test_handles_negative_revolutions():
    revolutions = -10 * u.revolution / u.second
    radius = 0.5 * u.meter
    expected_speed = round((-10 * 2 * pi * 0.5), 2) * u.meter / u.second
    assert (
        translatory_speed_from_number_of_revolutions(revolutions, radius)
        .to(u.meter / u.second)
        .magnitude
        == expected_speed.magnitude
    )


def test_handles_negative_radius():
    revolutions = 10 * u.revolution / u.second
    radius = -0.5 * u.meter
    with pytest.raises(ValueError):
        translatory_speed_from_number_of_revolutions(revolutions, radius)


def test_calculates_belt_speed_correctly():
    revolutions = 10 * u.revolution / u.second
    pulley_diameter = 0.5 * u.meter
    expected_speed = (10 * pi * 0.5) * u.meter / u.second
    assert belt_speed_from_pulley_revolutions(revolutions, pulley_diameter).to(
        u.meter / u.second
    ).magnitude == round(expected_speed.magnitude, 2)


def test_belt_speed_from_pulley_revolutions_handles_zero_revolutions():
    revolutions = 0 * u.revolution / u.second
    pulley_diameter = 0.5 * u.meter
    expected_speed = 0 * u.meter / u.second
    assert (
        belt_speed_from_pulley_revolutions(revolutions, pulley_diameter)
        .to(u.meter / u.second)
        .magnitude
        == expected_speed.magnitude
    )


def test_belt_speed_from_pulley_revolutions_handles_zero_pulley_diameter():
    revolutions = 10 * u.revolution / u.second
    pulley_diameter = 0 * u.meter
    with pytest.raises(ValueError):
        belt_speed_from_pulley_revolutions(revolutions, pulley_diameter)


def test_belt_speed_from_pulley_revolutions_handles_negative_revolutions():
    revolutions = -10 * u.revolution / u.second
    pulley_diameter = 0.5 * u.meter
    expected_speed = round((-10 * pi * 0.5), 2) * u.meter / u.second
    assert (
        belt_speed_from_pulley_revolutions(revolutions, pulley_diameter)
        .to(u.meter / u.second)
        .magnitude
        == expected_speed.magnitude
    )


def test_belt_speed_from_pulley_revolutions_handles_negative_pulley_diameter():
    revolutions = 10 * u.revolution / u.second
    pulley_diameter = -0.5 * u.meter
    with pytest.raises(ValueError):
        belt_speed_from_pulley_revolutions(revolutions, pulley_diameter)


# Tests for the public function
class TestAngleOfInclinationPublic:
    def test_angle_of_inclination_typical_values(self):
        # 45 degrees when lift == horizontal_length
        result = angle_of_inclination_from_horizontal_length_and_lift(
            4303.0 * u.meter, 18.0 * u.meter
        )
        assert result.magnitude == pytest.approx(0.24, rel=1e-2)
        assert str(result.units) == "degree"

    def test_angle_of_inclination_zero_lift(self):
        # 0 degrees when lift == 0
        result = angle_of_inclination_from_horizontal_length_and_lift(
            10.0 * u.meter, 0.0 * u.meter
        )
        assert result.magnitude == pytest.approx(0.0)
        assert str(result.units) == "degree"

    def test_angle_of_inclination_negative_lift(self):
        # -45 degrees when lift == -horizontal_length
        result = angle_of_inclination_from_horizontal_length_and_lift(
            10.0 * u.meter, -10.0 * u.meter
        )
        assert result.magnitude == pytest.approx(-45.0)
        assert str(result.units) == "degree"

    def test_angle_of_inclination_different_units(self):
        # Test with different units for horizontal_length and lift
        result = angle_of_inclination_from_horizontal_length_and_lift(
            10.0 * u.meter, 10.0 * u.kilometer
        )
        # 10 km rise over 10 m horizontal = very steep angle, almost 90 degrees
        assert result.magnitude > 89.0
        assert str(result.units) == "degree"

    def test_angle_of_inclination_output_unit_radians(self):
        # Test with radians as output unit
        result = angle_of_inclination_from_horizontal_length_and_lift(
            10.0 * u.meter, 10.0 * u.meter, unit="radian"
        )
        assert result.magnitude == pytest.approx(math.pi / 4, rel=1e-4)
        assert str(result.units) == "radian"

    def test_angle_of_inclination_precision(self):
        # Test precision parameter
        result = angle_of_inclination_from_horizontal_length_and_lift(
            10.0 * u.meter, 10.0 * u.meter, precision=2
        )
        assert result.magnitude == pytest.approx(45.0)
        # Check that it's rounded to 2 decimal places
        assert str(result.magnitude).split(".")[-1] in ["0", "00"]

    def test_angle_of_inclination_invalid_units(self):
        # Test with invalid units
        with pytest.raises(ValueError):
            angle_of_inclination_from_horizontal_length_and_lift(
                10.0 * u.meter, 10.0 * u.kilogram
            )

    def test_angle_of_inclination_horizontal_length_zero_raises(self):
        # Should raise ValueError if horizontal_length is zero
        with pytest.raises(ValueError):
            angle_of_inclination_from_horizontal_length_and_lift(
                0.0 * u.meter, 10.0 * u.meter
            )


# Tests for mechanical_power_from_torque_and_revolutions
class TestMechanicalPowerFromTorqueAndRevolutions:
    def test_calculates_mechanical_power_correctly(self):
        torque = 50 * u.newton * u.meter
        revolutions = 20 * u.revolution / u.second
        # P = 2π * T * n, expected is in watts, convert to kilowatt in the default function
        expected_power = round(2 * pi * 50 * 20 / 1000, 2) * u.kilowatt
        result = mechanical_power_from_torque_and_revolutions(torque, revolutions)
        assert result.magnitude == expected_power.magnitude
        assert str(result.units) == "kilowatt"

    def test_precision_parameter(self):
        torque = 50 * u.newton * u.meter
        revolutions = 20 * u.revolution / u.second
        expected_power = round(2 * pi * 50 * 20 / 1000, 3) * u.kilowatt
        result = mechanical_power_from_torque_and_revolutions(
            torque, revolutions, precision=3
        )
        assert result.magnitude == expected_power.magnitude
        assert str(result.units) == "kilowatt"

    def test_different_output_unit(self):
        torque = 50 * u.newton * u.meter
        revolutions = 20 * u.revolution / u.second
        expected_power = round(2 * pi * 50 * 20, 2) * u.watt
        result = mechanical_power_from_torque_and_revolutions(
            torque, revolutions, unit="watt"
        )
        assert result.magnitude == expected_power.magnitude
        assert str(result.units) == "watt"

    def test_zero_torque(self):
        torque = 0 * u.newton * u.meter
        revolutions = 20 * u.revolution / u.second
        expected_power = 0 * u.kilowatt
        result = mechanical_power_from_torque_and_revolutions(torque, revolutions)
        assert result.magnitude == expected_power.magnitude
        assert str(result.units) == "kilowatt"

    def test_zero_revolutions(self):
        torque = 50 * u.newton * u.meter
        revolutions = 0 * u.revolution / u.second
        expected_power = 0 * u.kilowatt
        result = mechanical_power_from_torque_and_revolutions(torque, revolutions)
        assert result.magnitude == expected_power.magnitude
        assert str(result.units) == "kilowatt"

    def test_invalid_unit(self):
        torque = 50 * u.newton * u.meter
        revolutions = 20 * u.revolution / u.second
        with pytest.raises(ValueError):
            mechanical_power_from_torque_and_revolutions(
                torque, revolutions, unit="invalid_unit"
            )

    def test_invalid_torque(self):
        torque = "invalid_value"
        revolutions = 20 * u.revolution / u.second
        with pytest.raises(ValueError):
            mechanical_power_from_torque_and_revolutions(torque, revolutions)

    def test_invalid_revolutions(self):
        torque = 50 * u.newton * u.meter
        revolutions = "invalid_value"
        with pytest.raises(ValueError):
            mechanical_power_from_torque_and_revolutions(torque, revolutions)


# Tests for torque_from_mechanical_power_and_revolutions
class TestTorqueFromMechanicalPowerAndRevolutions:
    def test_calculates_torque_correctly(self):
        power = 6000 * u.watt
        revolutions = 20 * u.revolution / u.second
        # T = P / (2π * n)
        expected_torque = round(6000 / (2 * pi * 20), 2) * u.newton * u.meter
        result = torque_from_mechanical_power_and_revolutions(power, revolutions)
        assert result.magnitude == expected_torque.magnitude
        # Allow both "newton * meter" and "meter * newton" as they're dimensionally equivalent
        assert result.dimensionality == expected_torque.dimensionality

    def test_precision_parameter(self):
        power = 6000 * u.watt
        revolutions = 20 * u.revolution / u.second
        expected_torque = round(6000 / (2 * pi * 20), 3) * u.newton * u.meter
        result = torque_from_mechanical_power_and_revolutions(
            power, revolutions, precision=3
        )
        assert result.magnitude == expected_torque.magnitude
        # Allow for different unit string representations as long as the dimensionality is the same
        assert result.dimensionality == expected_torque.dimensionality

    def test_different_output_unit(self):
        power = 6000 * u.watt
        revolutions = 20 * u.revolution / u.second
        expected_torque = round(6000 / (2 * pi * 20) / 1000, 2) * u.kilonewton * u.meter
        result = torque_from_mechanical_power_and_revolutions(
            power, revolutions, unit="kilonewton * meter"
        )
        assert result.magnitude == expected_torque.magnitude
        assert str(result.units) == "kilonewton * meter"

    def test_zero_power(self):
        power = 0 * u.watt
        revolutions = 20 * u.revolution / u.second
        expected_torque = 0 * u.newton * u.meter
        result = torque_from_mechanical_power_and_revolutions(power, revolutions)
        assert result.magnitude == expected_torque.magnitude
        # Allow for different unit string representations as long as the dimensionality is the same
        assert result.dimensionality == expected_torque.dimensionality

    def test_zero_revolutions(self):
        power = 6000 * u.watt
        revolutions = 0 * u.revolution / u.second
        with pytest.raises(ValueError):
            torque_from_mechanical_power_and_revolutions(power, revolutions)

    def test_invalid_unit(self):
        power = 6000 * u.watt
        revolutions = 20 * u.revolution / u.second
        with pytest.raises(ValueError):
            torque_from_mechanical_power_and_revolutions(
                power, revolutions, unit="invalid_unit"
            )

    def test_invalid_power(self):
        power = "invalid_value"
        revolutions = 20 * u.revolution / u.second
        with pytest.raises(ValueError):
            torque_from_mechanical_power_and_revolutions(power, revolutions)

    def test_invalid_revolutions(self):
        power = 6000 * u.watt
        revolutions = "invalid_value"
        with pytest.raises(ValueError):
            torque_from_mechanical_power_and_revolutions(power, revolutions)


# Tests for revolutions_from_mechanical_power_and_torque
class TestRevolutionsFromMechanicalPowerAndTorque:
    def test_calculates_revolutions_correctly(self):
        power = 6000 * u.watt
        torque = 50 * u.newton * u.meter
        # n = P / (2π * T)
        expected_revolutions = round(6000 / (2 * pi * 50), 2) * u.revolution / u.second
        result = revolutions_from_mechanical_power_and_torque(power, torque)
        assert result.magnitude == expected_revolutions.magnitude
        # Compare dimensionality instead of exact unit string to handle unit formatting differences
        assert result.dimensionality == expected_revolutions.dimensionality

    def test_precision_parameter(self):
        power = 6000 * u.watt
        torque = 50 * u.newton * u.meter
        expected_revolutions = round(6000 / (2 * pi * 50), 3) * u.revolution / u.second
        result = revolutions_from_mechanical_power_and_torque(
            power, torque, precision=3
        )
        assert result.magnitude == expected_revolutions.magnitude
        # Compare dimensionality instead of exact unit string
        assert result.dimensionality == expected_revolutions.dimensionality

    def test_different_output_unit(self):
        power = 6000 * u.watt
        torque = 50 * u.newton * u.meter
        expected_revolutions = round(60 * 6000 / (2 * pi * 50), 2) * u.rpm
        result = revolutions_from_mechanical_power_and_torque(power, torque, unit="rpm")
        assert result.magnitude == expected_revolutions.magnitude
        # Compare dimensionality instead of exact unit string
        assert result.dimensionality == expected_revolutions.dimensionality

    def test_zero_power(self):
        power = 0 * u.watt
        torque = 50 * u.newton * u.meter
        expected_revolutions = 0 * u.revolution / u.second
        result = revolutions_from_mechanical_power_and_torque(power, torque)
        assert result.magnitude == expected_revolutions.magnitude
        # Compare dimensionality instead of exact unit string
        assert result.dimensionality == expected_revolutions.dimensionality

    def test_zero_torque(self):
        power = 6000 * u.watt
        torque = 0 * u.newton * u.meter
        with pytest.raises(ValueError):
            revolutions_from_mechanical_power_and_torque(power, torque)

    def test_invalid_unit(self):
        power = 6000 * u.watt
        torque = 50 * u.newton * u.meter
        with pytest.raises(ValueError):
            revolutions_from_mechanical_power_and_torque(
                power, torque, unit="invalid_unit"
            )

    def test_invalid_power(self):
        power = "invalid_value"
        torque = 50 * u.newton * u.meter
        with pytest.raises(ValueError):
            revolutions_from_mechanical_power_and_torque(power, torque)

    def test_invalid_torque(self):
        power = 6000 * u.watt
        torque = "invalid_value"
        with pytest.raises(ValueError):
            revolutions_from_mechanical_power_and_torque(power, torque)


# Tests for pulley_diameter_from_belt_speed_and_revolutions
class TestPulleyDiameterFromBeltSpeedAndRevolutions:
    def test_calculates_pulley_diameter_correctly(self):
        belt_speed = 6.7 * u.meter / u.second
        revolutions = 121.867 * u.revolution / u.minute
        # D = v / (π * n)
        expected_diameter = 1.05 * u.meter
        result = pulley_diameter_from_belt_speed_and_revolutions(
            belt_speed, revolutions
        )
        assert result.magnitude == expected_diameter.magnitude
        assert str(result.units) == "meter"

    def test_precision_parameter(self):
        belt_speed = 5 * u.meter / u.second
        revolutions = 10 * u.revolution / u.second
        # D = v / (π * n)
        expected_diameter = round((5) / (pi * 10), 3) * u.meter
        result = pulley_diameter_from_belt_speed_and_revolutions(
            belt_speed, revolutions, precision=3
        )
        assert result.magnitude == expected_diameter.magnitude
        assert str(result.units) == "meter"

    def test_different_output_unit(self):
        belt_speed = 5 * u.meter / u.second
        revolutions = 10 * u.revolution / u.second
        # D = v / (π * n)
        expected_diameter = round((5) / (pi * 10) * 1000, 2) * u.millimeter
        result = pulley_diameter_from_belt_speed_and_revolutions(
            belt_speed, revolutions, unit="millimeter"
        )
        assert result.magnitude == expected_diameter.magnitude
        assert str(result.units) == "millimeter"

    def test_zero_belt_speed(self):
        belt_speed = 0 * u.meter / u.second
        revolutions = 10 * u.revolution / u.second
        with pytest.raises(
            ValueError, match="Pulley diameter must be greater than zero."
        ):
            pulley_diameter_from_belt_speed_and_revolutions(belt_speed, revolutions)

    def test_zero_revolutions(self):
        belt_speed = 5 * u.meter / u.second
        revolutions = 0 * u.revolution / u.second
        with pytest.raises(ValueError):
            pulley_diameter_from_belt_speed_and_revolutions(belt_speed, revolutions)

    def test_invalid_unit(self):
        belt_speed = 5 * u.meter / u.second
        revolutions = 10 * u.revolution / u.second
        with pytest.raises(ValueError):
            pulley_diameter_from_belt_speed_and_revolutions(
                belt_speed, revolutions, unit="invalid_unit"
            )

    def test_invalid_belt_speed(self):
        belt_speed = "invalid_value"
        revolutions = 10 * u.revolution / u.second
        with pytest.raises(ValueError):
            pulley_diameter_from_belt_speed_and_revolutions(belt_speed, revolutions)

    def test_invalid_revolutions(self):
        belt_speed = 5 * u.meter / u.second
        revolutions = "invalid_value"
        with pytest.raises(ValueError):
            pulley_diameter_from_belt_speed_and_revolutions(belt_speed, revolutions)


# Tests for radius_from_translatory_speed_and_revolutions
class TestRadiusFromTranslatorySpeedAndRevolutions:
    def test_calculates_radius_correctly(self):
        translatory_speed = 5 * u.meter / u.second
        revolutions = 10 * u.revolution / u.second
        # r = v / (2π * n)
        expected_radius = round(5 / (2 * pi * 10), 2) * u.meter
        result = radius_from_translatory_speed_and_revolutions(
            translatory_speed, revolutions
        )
        assert result.magnitude == expected_radius.magnitude
        assert str(result.units) == "meter"

    def test_different_units(self):
        translatory_speed = 18 * u.kilometer / u.hour  # 5 m/s
        revolutions = 600 * u.revolution / u.minute  # 10 rev/s
        # r = v / (2π * n)
        expected_radius = round(5 / (2 * pi * 10), 2) * u.meter
        result = radius_from_translatory_speed_and_revolutions(
            translatory_speed, revolutions
        )
        assert result.magnitude == expected_radius.magnitude
        assert str(result.units) == "meter"

    def test_custom_output_unit(self):
        translatory_speed = 5 * u.meter / u.second
        revolutions = 10 * u.revolution / u.second
        # r = v / (2π * n)
        expected_radius = round(5 / (2 * pi * 10) * 100, 2) * u.centimeter
        result = radius_from_translatory_speed_and_revolutions(
            translatory_speed, revolutions, unit="centimeter"
        )
        assert result.magnitude == expected_radius.magnitude
        assert str(result.units) == "centimeter"

    def test_zero_translatory_speed(self):
        translatory_speed = 0 * u.meter / u.second
        revolutions = 10 * u.revolution / u.second
        result = radius_from_translatory_speed_and_revolutions(
            translatory_speed, revolutions
        )
        assert result.magnitude == 0
        assert str(result.units) == "meter"

    def test_zero_revolutions(self):
        translatory_speed = 5 * u.meter / u.second
        revolutions = 0 * u.revolution / u.second
        with pytest.raises(
            ValueError, match="The number of revolutions cannot be zero."
        ):
            radius_from_translatory_speed_and_revolutions(
                translatory_speed, revolutions
            )

    def test_negative_translatory_speed(self):
        translatory_speed = -5 * u.meter / u.second
        revolutions = 10 * u.revolution / u.second
        expected_radius = round(-5 / (2 * pi * 10), 2) * u.meter
        result = radius_from_translatory_speed_and_revolutions(
            translatory_speed, revolutions
        )
        assert result.magnitude == expected_radius.magnitude
        assert str(result.units) == "meter"

    def test_negative_revolutions(self):
        translatory_speed = 5 * u.meter / u.second
        revolutions = -10 * u.revolution / u.second
        with pytest.raises(ValueError, match="revolutions must be positive"):
            radius_from_translatory_speed_and_revolutions(
                translatory_speed, revolutions
            )

    def test_invalid_unit(self):
        translatory_speed = 5 * u.meter / u.second
        revolutions = 10 * u.revolution / u.second
        with pytest.raises(ValueError, match="Invalid unit"):
            radius_from_translatory_speed_and_revolutions(
                translatory_speed, revolutions, unit="invalid_unit"
            )
