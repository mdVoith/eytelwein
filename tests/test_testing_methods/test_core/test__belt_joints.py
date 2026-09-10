from eytelwein.testing_methods.core._belt_joints import (
    _nominal_breaking_strength_of_textile_belt_specimen,
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
