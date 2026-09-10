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


def test_testing_methods_import_chain():
    """Test that the public function is accessible from eytelwein.testing_methods."""
    from eytelwein.testing_methods import (
        nominal_breaking_strength_of_textile_belt_specimen as imported_func,
    )

    assert imported_func is nominal_breaking_strength_of_textile_belt_specimen


def test_root_package_exposes_testing_methods():
    """Test that root eytelwein exports the testing_methods package surface."""
    import eytelwein
    from eytelwein import testing_methods as imported_package
    from eytelwein.testing_methods import (
        nominal_breaking_strength_of_textile_belt_specimen as imported_func,
    )

    assert eytelwein.testing_methods is imported_package
    assert (
        imported_package.nominal_breaking_strength_of_textile_belt_specimen
        is imported_func
    )


# Tests for specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension


def test_specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension_valid_values():
    """Test with valid inputs for width inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    )

    # b = 1000 * F_B / k_N
    # F_B = 1.0 kN, k_N = 10 N/mm
    # Result: 1000 * 1.0 / 10 = 100 mm
    result = specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
        nominal_breaking_strength=1.0 * u.kilonewton,
        width_related_nominal_breaking_tension=10 * u.N / u.mm,
    )
    assert result.magnitude == 100.0
    assert result.units == u.millimeter


def test_specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension_input_unit_conversion():
    """Test that input units are converted correctly for width inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    )

    # 1000 N = 1 kN, 10 N/mm should work the same
    result = specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
        nominal_breaking_strength=1000 * u.newton,
        width_related_nominal_breaking_tension=10 * u.N / u.mm,
    )
    assert result.magnitude == 100.0
    assert result.units == u.millimeter


def test_specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension_invalid_output_unit():
    """Test that invalid output unit raises ValueError for width inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    )

    with pytest.raises(ValueError):
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
            nominal_breaking_strength=1.0 * u.kilonewton,
            width_related_nominal_breaking_tension=10 * u.N / u.mm,
            unit="invalid_unit",
        )


def test_specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension_incompatible_output_unit():
    """Test that parseable but incompatible output unit raises ValueError for width inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    )

    with pytest.raises(ValueError):
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
            nominal_breaking_strength=1.0 * u.kilonewton,
            width_related_nominal_breaking_tension=10 * u.N / u.mm,
            unit="newton",
        )


def test_specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension_conversion_error():
    """Test that invalid input object raises ValueError for width inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    )

    with pytest.raises(ValueError):
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
            nominal_breaking_strength="not_a_quantity",
            width_related_nominal_breaking_tension=10 * u.N / u.mm,
        )


def test_specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension_non_positive_denominator():
    """Test that zero or negative denominator raises ValueError for width inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    )

    with pytest.raises(ValueError):
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
            nominal_breaking_strength=1.0 * u.kilonewton,
            width_related_nominal_breaking_tension=0 * u.N / u.mm,
        )

    with pytest.raises(ValueError):
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
            nominal_breaking_strength=1.0 * u.kilonewton,
            width_related_nominal_breaking_tension=-10 * u.N / u.mm,
        )


def test_specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension_precision():
    """Test that precision parameter works correctly for width inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    )

    result = specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
        nominal_breaking_strength=1.012 * u.kilonewton,
        width_related_nominal_breaking_tension=10 * u.N / u.mm,
        precision=1,
    )
    assert result.magnitude == 101.2
    assert result.units == u.millimeter


def test_specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension_output_unit_conversion():
    """Test that output can be converted to different units for width inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    )

    result = specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
        nominal_breaking_strength=1.0 * u.kilonewton,
        width_related_nominal_breaking_tension=10 * u.N / u.mm,
        unit="centimeter",
    )
    assert result.magnitude == 10.0
    assert result.units == u.centimeter


def test_specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension_equivalent_input_unit():
    """Test input conversion using equivalent unit for width inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    )

    # 10 kN/m = 10 * 1000 N / 1000 mm = 10 N/mm
    result = specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
        nominal_breaking_strength=1.0 * u.kilonewton,
        width_related_nominal_breaking_tension=10 * u.kN / u.m,
    )
    assert result.magnitude == 100.0
    assert result.units == u.millimeter


# Tests for width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width


def test_width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width_valid_values():
    """Test with valid inputs for tension inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
    )

    # k_N = 1000 * F_B / b
    # F_B = 1.0 kN, b = 100 mm
    # Result: 1000 * 1.0 / 100 = 10 N/mm
    result = width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength=1.0 * u.kilonewton,
        specimen_width=100 * u.mm,
    )
    assert result.magnitude == 10.0
    assert result.units == u.N / u.mm


def test_width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width_input_unit_conversion():
    """Test that input units are converted correctly for tension inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
    )

    # 1000 N = 1 kN, 100 mm = 10 cm
    result = width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength=1000 * u.newton,
        specimen_width=10 * u.cm,
    )
    assert result.magnitude == 10.0
    assert result.units == u.N / u.mm


def test_width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width_invalid_output_unit():
    """Test that invalid output unit raises ValueError for tension inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
    )

    with pytest.raises(ValueError):
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
            nominal_breaking_strength=1.0 * u.kilonewton,
            specimen_width=100 * u.mm,
            unit="invalid_unit",
        )


def test_width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width_incompatible_output_unit():
    """Test that parseable but incompatible output unit raises ValueError for tension inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
    )

    with pytest.raises(ValueError):
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
            nominal_breaking_strength=1.0 * u.kilonewton,
            specimen_width=100 * u.mm,
            unit="meter",
        )


def test_width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width_conversion_error():
    """Test that invalid input object raises ValueError for tension inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
    )

    with pytest.raises(ValueError):
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
            nominal_breaking_strength="not_a_quantity",
            specimen_width=100 * u.mm,
        )


def test_width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width_non_positive_denominator():
    """Test that zero or negative denominator raises ValueError for tension inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
    )

    with pytest.raises(ValueError):
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
            nominal_breaking_strength=1.0 * u.kilonewton,
            specimen_width=0 * u.mm,
        )

    with pytest.raises(ValueError):
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
            nominal_breaking_strength=1.0 * u.kilonewton,
            specimen_width=-100 * u.mm,
        )


def test_width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width_precision():
    """Test that precision parameter works correctly for tension inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
    )

    result = width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength=1.012 * u.kilonewton,
        specimen_width=100 * u.mm,
        precision=2,
    )
    assert result.magnitude == 10.12
    assert result.units == u.N / u.mm


def test_width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width_output_unit_conversion():
    """Test that output can be converted to different units for tension inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
    )

    # 10 N/mm = 10 * 1000 N / 1000 mm = 10 kN/m
    result = width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength=1.0 * u.kilonewton,
        specimen_width=100 * u.mm,
        unit="kN/m",
    )
    assert result.magnitude == 10.0
    assert result.units == u.kN / u.m


def test_width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width_equivalent_input_unit():
    """Test input conversion using equivalent unit for tension inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
    )

    # 1000 N = 1 kN, 100 mm = 0.1 m
    result = width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength=1000 * u.newton,
        specimen_width=0.1 * u.m,
    )
    assert result.magnitude == 10.0
    assert result.units == u.N / u.mm
