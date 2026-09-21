import pytest

from eytelwein.testing_methods.core._belt_joints import (
    _lower_load_from_nominal_breaking_strength_of_specimen,
    _nominal_breaking_strength_of_specimen_from_lower_load,
    _nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    _nominal_breaking_strength_of_textile_belt_specimen,
    _reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    _relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    _specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
)


def test_nominal_breaking_strength_of_textile_belt_specimen_positive_values():
    """Test calculation with positive width and tension coefficient."""
    # T_breaking = b * T_nominal_tension, where b=100 mm, T_nominal_tension=10 N/mm
    # Result: 100 * 10 = 1000 N = 1.0 kN
    result = _nominal_breaking_strength_of_textile_belt_specimen(
        belt_width_mm=100.0, tension_coefficient_n_per_mm=10.0
    )
    assert result == 1.0


def test_nominal_breaking_strength_of_textile_belt_specimen_zero_width():
    """Test calculation with zero belt width."""
    result = _nominal_breaking_strength_of_textile_belt_specimen(
        belt_width_mm=0.0, tension_coefficient_n_per_mm=10.0
    )
    assert result == 0.0


def test_nominal_breaking_strength_of_textile_belt_specimen_zero_tension():
    """Test calculation with zero tension coefficient."""
    result = _nominal_breaking_strength_of_textile_belt_specimen(
        belt_width_mm=100.0, tension_coefficient_n_per_mm=0.0
    )
    assert result == 0.0


def test_nominal_breaking_strength_of_textile_belt_specimen_negative_inputs():
    """Test calculation with negative inputs."""
    # Negative width
    result = _nominal_breaking_strength_of_textile_belt_specimen(
        belt_width_mm=-100.0, tension_coefficient_n_per_mm=10.0
    )
    assert result == -1.0

    # Negative tension coefficient
    result = _nominal_breaking_strength_of_textile_belt_specimen(
        belt_width_mm=100.0, tension_coefficient_n_per_mm=-10.0
    )
    assert result == -1.0

    # Both negative
    result = _nominal_breaking_strength_of_textile_belt_specimen(
        belt_width_mm=-100.0, tension_coefficient_n_per_mm=-10.0
    )
    assert result == 1.0


# Tests for width inverse: b = 1000 * T_breaking / T_nominal_tension
def test_specimen_width_inverse_positive_values():
    """Test width inverse calculation with positive inputs."""
    # b = 1000 * 1.0 / 10.0 = 100.0 mm
    result = _specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
        nominal_breaking_strength_kn=1.0,
        width_related_nominal_breaking_tension_n_per_mm=10.0,
    )
    assert result == 100.0


def test_specimen_width_inverse_zero_breaking_strength():
    """Test width inverse with zero breaking strength."""
    # b = 1000 * 0.0 / 10.0 = 0.0 mm
    result = _specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
        nominal_breaking_strength_kn=0.0,
        width_related_nominal_breaking_tension_n_per_mm=10.0,
    )
    assert result == 0.0


def test_specimen_width_inverse_zero_denominator():
    """Test width inverse raises ValueError when tension coefficient is zero."""
    with pytest.raises(ValueError):
        _specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
            nominal_breaking_strength_kn=1.0,
            width_related_nominal_breaking_tension_n_per_mm=0.0,
        )


def test_specimen_width_inverse_negative_denominator():
    """Test width inverse raises ValueError when tension coefficient is negative."""
    with pytest.raises(ValueError):
        _specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
            nominal_breaking_strength_kn=1.0,
            width_related_nominal_breaking_tension_n_per_mm=-10.0,
        )


def test_specimen_width_inverse_negative_numerator():
    """Test width inverse with negative breaking strength (negative denominator still guards)."""
    # b = 1000 * (-1.0) / 10.0 = -100.0 mm
    result = _specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
        nominal_breaking_strength_kn=-1.0,
        width_related_nominal_breaking_tension_n_per_mm=10.0,
    )
    assert result == -100.0


# Tests for tension inverse: T_nominal_tension = 1000 * T_breaking / b
def test_width_related_tension_inverse_positive_values():
    """Test tension inverse calculation with positive inputs."""
    # T_nominal_tension = 1000 * 1.0 / 100.0 = 10.0 N/mm
    result = _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength_kn=1.0, specimen_width_mm=100.0
    )
    assert result == 10.0


def test_width_related_tension_inverse_zero_breaking_strength():
    """Test tension inverse with zero breaking strength."""
    # T_nominal_tension = 1000 * 0.0 / 100.0 = 0.0 N/mm
    result = _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength_kn=0.0, specimen_width_mm=100.0
    )
    assert result == 0.0


def test_width_related_tension_inverse_zero_denominator():
    """Test tension inverse raises ValueError when specimen width is zero."""
    with pytest.raises(ValueError):
        _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
            nominal_breaking_strength_kn=1.0, specimen_width_mm=0.0
        )


def test_width_related_tension_inverse_negative_denominator():
    """Test tension inverse raises ValueError when specimen width is negative."""
    with pytest.raises(ValueError):
        _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
            nominal_breaking_strength_kn=1.0, specimen_width_mm=-100.0
        )


def test_width_related_tension_inverse_negative_numerator():
    """Test tension inverse with negative breaking strength (negative denominator still guards)."""
    # T_nominal_tension = 1000 * (-1.0) / 100.0 = -10.0 N/mm
    result = _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength_kn=-1.0, specimen_width_mm=100.0
    )
    assert result == -10.0


# Tests for relative reference splice efficiency forward: T_rel_fatigue = T_upper / T_breaking * 100
def test_relative_reference_splice_efficiency_forward_positive_values():
    """Test forward efficiency calculation with positive inputs."""
    # T_rel_fatigue = 10.0 / 100.0 * 100 = 10.0 percent
    result = _relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load_kn=10.0,
        nominal_breaking_strength_of_specimen_kn=100.0,
    )
    assert result == 10.0


def test_relative_reference_splice_efficiency_forward_zero_numerator():
    """Test forward efficiency with zero reference upper load."""
    # T_rel_fatigue = 0.0 / 100.0 * 100 = 0.0 percent
    result = _relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load_kn=0.0,
        nominal_breaking_strength_of_specimen_kn=100.0,
    )
    assert result == 0.0


def test_relative_reference_splice_efficiency_forward_zero_denominator():
    """Test forward efficiency raises ValueError when nominal breaking strength is zero."""
    with pytest.raises(ValueError):
        _relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
            reference_upper_load_kn=10.0,
            nominal_breaking_strength_of_specimen_kn=0.0,
        )


def test_relative_reference_splice_efficiency_forward_negative_denominator():
    """Test forward efficiency raises ValueError when nominal breaking strength is negative."""
    with pytest.raises(ValueError):
        _relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
            reference_upper_load_kn=10.0,
            nominal_breaking_strength_of_specimen_kn=-100.0,
        )


def test_relative_reference_splice_efficiency_forward_negative_numerator():
    """Test forward efficiency with negative reference upper load (negative denominator still guards)."""
    # T_rel_fatigue = (-10.0) / 100.0 * 100 = -10.0 percent
    result = _relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load_kn=-10.0,
        nominal_breaking_strength_of_specimen_kn=100.0,
    )
    assert result == -10.0


# Tests for reference upper load inverse: T_upper = T_rel_fatigue / 100 * T_breaking
def test_reference_upper_load_inverse_positive_values():
    """Test reference upper load inverse with positive inputs."""
    # T_upper = 10.0 / 100 * 100.0 = 10.0 kN
    result = _reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
        relative_reference_splice_efficiency_percent=10.0,
        nominal_breaking_strength_of_specimen_kn=100.0,
    )
    assert result == 10.0


def test_reference_upper_load_inverse_zero_efficiency():
    """Test reference upper load inverse with zero efficiency."""
    # T_upper = 0.0 / 100 * 100.0 = 0.0 kN
    result = _reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
        relative_reference_splice_efficiency_percent=0.0,
        nominal_breaking_strength_of_specimen_kn=100.0,
    )
    assert result == 0.0


def test_reference_upper_load_inverse_zero_efficiency_negative_numerator():
    """Test reference upper load inverse with zero efficiency and negative nominal breaking strength."""
    # T_upper = 0.0 / 100 * (-100.0) = 0.0 kN
    result = _reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
        relative_reference_splice_efficiency_percent=0.0,
        nominal_breaking_strength_of_specimen_kn=-100.0,
    )
    assert result == 0.0


def test_reference_upper_load_inverse_negative_numerator():
    """Test reference upper load inverse with negative nominal breaking strength."""
    # T_upper = 10.0 / 100 * (-100.0) = -10.0 kN
    result = _reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
        relative_reference_splice_efficiency_percent=10.0,
        nominal_breaking_strength_of_specimen_kn=-100.0,
    )
    assert result == -10.0


# Tests for nominal breaking strength inverse: T_breaking = T_upper / (T_rel_fatigue / 100)
def test_nominal_breaking_strength_inverse_positive_values():
    """Test nominal breaking strength inverse with positive inputs."""
    # T_breaking = 10.0 / (10.0 / 100) = 10.0 / 0.1 = 100.0 kN
    result = _nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
        reference_upper_load_kn=10.0,
        relative_reference_splice_efficiency_percent=10.0,
    )
    assert result == 100.0


def test_nominal_breaking_strength_inverse_zero_efficiency():
    """Test nominal breaking strength inverse raises ValueError when efficiency is zero."""
    with pytest.raises(ValueError):
        _nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
            reference_upper_load_kn=10.0,
            relative_reference_splice_efficiency_percent=0.0,
        )


def test_nominal_breaking_strength_inverse_negative_efficiency():
    """Test nominal breaking strength inverse raises ValueError when efficiency is negative."""
    with pytest.raises(ValueError):
        _nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
            reference_upper_load_kn=10.0,
            relative_reference_splice_efficiency_percent=-10.0,
        )


def test_nominal_breaking_strength_inverse_negative_numerator():
    """Test nominal breaking strength inverse with negative reference upper load."""
    # T_breaking = (-10.0) / (10.0 / 100) = (-10.0) / 0.1 = -100.0 kN
    result = _nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
        reference_upper_load_kn=-10.0,
        relative_reference_splice_efficiency_percent=10.0,
    )
    assert result == -100.0


# Dataset tests using approved values:
# b = 172 mm, T_nominal_tension = 630 N/mm, T_rel_fatigue = 30 %
# Derived: T_breaking = 172 * 630 / 1000 = 108.36 kN
# Derived: T_upper = 30 / 100 * 108.36 = 32.508 kN


def test_nominal_breaking_strength_of_textile_belt_specimen_dataset():
    """Test with approved dataset: b=172mm, T_nominal_tension=630N/mm."""
    # T_breaking = 172 * 630 / 1000 = 108.36 kN
    result = _nominal_breaking_strength_of_textile_belt_specimen(
        belt_width_mm=172.0,
        tension_coefficient_n_per_mm=630.0,
    )
    assert result == pytest.approx(108.36, abs=1e-10)


def test_specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension_dataset():
    """Test width inverse with approved dataset: T_breaking=108.36kN, T_nominal_tension=630N/mm."""
    # b = 1000 * 108.36 / 630 = 172.0 mm
    result = _specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
        nominal_breaking_strength_kn=108.36,
        width_related_nominal_breaking_tension_n_per_mm=630.0,
    )
    assert result == pytest.approx(172.0, abs=1e-10)


def test_width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width_dataset():
    """Test tension inverse with approved dataset: T_breaking=108.36kN, b=172mm."""
    # T_nominal_tension = 1000 * 108.36 / 172 = 630.0 N/mm
    result = _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength_kn=108.36,
        specimen_width_mm=172.0,
    )
    assert result == pytest.approx(630.0, abs=1e-10)


def test_relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen_dataset():
    """Test splice efficiency forward with approved dataset: T_upper=32.508kN, T_breaking=108.36kN."""
    # T_rel_fatigue = 32.508 / 108.36 * 100 = 30.0 %
    result = _relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load_kn=32.508,
        nominal_breaking_strength_of_specimen_kn=108.36,
    )
    assert result == pytest.approx(30.0, abs=1e-10)


def test_reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen_dataset():
    """Test reference upper load inverse with approved dataset: T_rel_fatigue=30%, T_breaking=108.36kN."""
    # T_upper = 30 / 100 * 108.36 = 32.508 kN
    result = _reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
        relative_reference_splice_efficiency_percent=30.0,
        nominal_breaking_strength_of_specimen_kn=108.36,
    )
    assert result == pytest.approx(32.508, abs=1e-10)


def test_nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency_dataset():
    """Test nominal breaking strength inverse with approved dataset: T_upper=32.508kN, T_rel_fatigue=30%."""
    # T_breaking = 32.508 / (30 / 100) = 108.36 kN
    result = _nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
        reference_upper_load_kn=32.508,
        relative_reference_splice_efficiency_percent=30.0,
    )
    assert result == pytest.approx(108.36, abs=1e-10)


def test_lower_load_from_nominal_breaking_strength_of_specimen_default_factor():
    """Test lower load forward calculation with default lower-load factor."""
    result = _lower_load_from_nominal_breaking_strength_of_specimen(
        nominal_breaking_strength_of_specimen_kn=100.0
    )
    assert result == pytest.approx(6.67, abs=1e-10)


def test_lower_load_from_nominal_breaking_strength_of_specimen_custom_factor():
    """Test lower load forward calculation with explicit lower-load factor."""
    result = _lower_load_from_nominal_breaking_strength_of_specimen(
        nominal_breaking_strength_of_specimen_kn=108.36,
        lower_load_factor=0.0667,
    )
    assert result == pytest.approx(7.227612, abs=1e-10)


def test_lower_load_from_nominal_breaking_strength_of_specimen_invalid_factor():
    """Test lower load forward calculation rejects non-positive factor."""
    with pytest.raises(ValueError):
        _lower_load_from_nominal_breaking_strength_of_specimen(
            nominal_breaking_strength_of_specimen_kn=100.0,
            lower_load_factor=0.0,
        )

    with pytest.raises(ValueError):
        _lower_load_from_nominal_breaking_strength_of_specimen(
            nominal_breaking_strength_of_specimen_kn=100.0,
            lower_load_factor=-0.067,
        )


def test_nominal_breaking_strength_of_specimen_from_lower_load_default_factor():
    """Test lower load inverse calculation with default lower-load factor."""
    result = _nominal_breaking_strength_of_specimen_from_lower_load(
        lower_load_kn=6.7,
    )
    assert result == pytest.approx(100.44977511244379, abs=1e-10)


def test_nominal_breaking_strength_of_specimen_from_lower_load_custom_factor():
    """Test lower load inverse calculation with explicit lower-load factor."""
    result = _nominal_breaking_strength_of_specimen_from_lower_load(
        lower_load_kn=7.227612,
        lower_load_factor=0.0667,
    )
    assert result == pytest.approx(108.36, abs=1e-10)


def test_nominal_breaking_strength_of_specimen_from_lower_load_invalid_factor():
    """Test lower load inverse calculation rejects non-positive factor."""
    with pytest.raises(ValueError):
        _nominal_breaking_strength_of_specimen_from_lower_load(
            lower_load_kn=6.7,
            lower_load_factor=0.0,
        )

    with pytest.raises(ValueError):
        _nominal_breaking_strength_of_specimen_from_lower_load(
            lower_load_kn=6.7,
            lower_load_factor=-0.067,
        )


def test_lower_load_round_trip_dataset_with_default_factor():
    """Test lower load round trip with dataset breaking strength and default factor."""
    lower_load_kn = _lower_load_from_nominal_breaking_strength_of_specimen(
        nominal_breaking_strength_of_specimen_kn=108.36,
    )
    recovered_breaking_strength_kn = (
        _nominal_breaking_strength_of_specimen_from_lower_load(
            lower_load_kn=lower_load_kn,
        )
    )
    assert lower_load_kn == pytest.approx(7.227612, abs=1e-10)
    assert recovered_breaking_strength_kn == pytest.approx(108.36, abs=1e-10)
