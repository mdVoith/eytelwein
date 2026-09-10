import pytest

from eytelwein.testing_methods.core._belt_joints import (
    _nominal_breaking_strength_of_textile_belt_specimen,
    _specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
)


def test_nominal_breaking_strength_of_textile_belt_specimen_positive_values():
    """Test calculation with positive width and tension coefficient."""
    # F_B = b * k_N, where b=100 mm, k_N=10 N/mm
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


# Tests for width inverse: b = 1000 * F_B / k_N
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


# Tests for tension inverse: k_N = 1000 * F_B / b
def test_width_related_tension_inverse_positive_values():
    """Test tension inverse calculation with positive inputs."""
    # k_N = 1000 * 1.0 / 100.0 = 10.0 N/mm
    result = _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength_kn=1.0, specimen_width_mm=100.0
    )
    assert result == 10.0


def test_width_related_tension_inverse_zero_breaking_strength():
    """Test tension inverse with zero breaking strength."""
    # k_N = 1000 * 0.0 / 100.0 = 0.0 N/mm
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
    # k_N = 1000 * (-1.0) / 100.0 = -10.0 N/mm
    result = _width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength_kn=-1.0, specimen_width_mm=100.0
    )
    assert result == -10.0
