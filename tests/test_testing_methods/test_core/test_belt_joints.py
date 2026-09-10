import pytest

from eytelwein.main.units import get_unit_registry
from eytelwein.testing_methods.core.belt_joints import (
    nominal_breaking_strength_of_textile_belt_specimen,
)

# Get the unit registry
u = get_unit_registry()


def test_nominal_breaking_strength_of_textile_belt_specimen_valid_values():
    """Test with valid specimen width and width-related nominal breaking tension."""
    # F_B = b * k_N
    # b = 100 mm, k_N = 10 N/mm
    # Result: 100 * 10 = 1000 N = 1.0 kN
    result = nominal_breaking_strength_of_textile_belt_specimen(
        specimen_width=100 * u.mm,
        width_related_nominal_breaking_tension=10 * u.N / u.mm,
    )
    assert result.magnitude == 1.0
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_textile_belt_specimen_input_unit_conversion():
    """Test that input units are converted correctly."""
    # 1 cm = 10 mm, so width 10 cm = 100 mm
    # Result should be the same as 100 mm input
    result = nominal_breaking_strength_of_textile_belt_specimen(
        specimen_width=10 * u.cm, width_related_nominal_breaking_tension=10 * u.N / u.mm
    )
    assert result.magnitude == 1.0
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_textile_belt_specimen_invalid_output_unit():
    """Test that invalid output unit raises ValueError."""
    with pytest.raises(ValueError):
        nominal_breaking_strength_of_textile_belt_specimen(
            specimen_width=100 * u.mm,
            width_related_nominal_breaking_tension=10 * u.N / u.mm,
            unit="invalid_unit",
        )


def test_nominal_breaking_strength_of_textile_belt_specimen_conversion_error():
    """Test that invalid input object raises ValueError."""
    with pytest.raises(ValueError):
        nominal_breaking_strength_of_textile_belt_specimen(
            specimen_width="not_a_quantity",
            width_related_nominal_breaking_tension=10 * u.N / u.mm,
        )


def test_nominal_breaking_strength_of_textile_belt_specimen_non_positive_width():
    """Test that non-positive specimen width raises ValueError."""
    with pytest.raises(ValueError):
        nominal_breaking_strength_of_textile_belt_specimen(
            specimen_width=0 * u.mm,
            width_related_nominal_breaking_tension=10 * u.N / u.mm,
        )

    with pytest.raises(ValueError):
        nominal_breaking_strength_of_textile_belt_specimen(
            specimen_width=-10 * u.mm,
            width_related_nominal_breaking_tension=10 * u.N / u.mm,
        )


def test_nominal_breaking_strength_of_textile_belt_specimen_negative_width_related_tension():
    """Test that negative width-related nominal breaking tension raises ValueError."""
    with pytest.raises(ValueError):
        nominal_breaking_strength_of_textile_belt_specimen(
            specimen_width=100 * u.mm,
            width_related_nominal_breaking_tension=-10 * u.N / u.mm,
        )


def test_nominal_breaking_strength_of_textile_belt_specimen_precision():
    """Test that precision parameter works correctly."""
    result = nominal_breaking_strength_of_textile_belt_specimen(
        specimen_width=100 * u.mm,
        width_related_nominal_breaking_tension=10.123 * u.N / u.mm,
        precision=2,
    )
    assert result.magnitude == 1.01
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_textile_belt_specimen_output_unit_conversion():
    """Test that output can be converted to different units."""
    result = nominal_breaking_strength_of_textile_belt_specimen(
        specimen_width=100 * u.mm,
        width_related_nominal_breaking_tension=10 * u.N / u.mm,
        unit="newton",
    )
    assert result.magnitude == 1000.0
    assert result.units == u.newton


def test_nominal_breaking_strength_of_textile_belt_specimen_width_related_tension_equivalent_unit():
    """Test input conversion using equivalent unit (kN/m converted to N/mm)."""
    # 1 kN/m = 1000 N / 1000 mm = 1 N/mm
    # So 10 kN/m = 10 N/mm
    # With 100 mm width and 10 kN/m, result should be same as 100 mm width and 10 N/mm
    result = nominal_breaking_strength_of_textile_belt_specimen(
        specimen_width=100 * u.mm,
        width_related_nominal_breaking_tension=10 * u.kN / u.m,
    )
    assert result.magnitude == 1.0
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_textile_belt_specimen_incompatible_output_unit():
    """Test that parseable but incompatible output unit raises ValueError."""
    with pytest.raises(ValueError):
        nominal_breaking_strength_of_textile_belt_specimen(
            specimen_width=100 * u.mm,
            width_related_nominal_breaking_tension=10 * u.N / u.mm,
            unit="meter",
        )
