import pytest

from eytelwein.main.units import get_unit_registry
from eytelwein.testing_methods.core.belt_joints import (
    lower_load_from_nominal_breaking_strength_of_specimen,
    nominal_breaking_strength_of_specimen_from_lower_load,
    nominal_breaking_strength_of_textile_belt_specimen,
    specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
)

# Get the unit registry
u = get_unit_registry()


def test_nominal_breaking_strength_of_textile_belt_specimen_valid_values():
    """Test with valid specimen width and width-related nominal breaking tension."""
    # T_breaking = b * T_nominal_tension
    # b = 100 mm, T_nominal_tension = 10 N/mm
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


# Phase 3: Round-trip coverage and import-surface checks


def test_forward_to_width_inverse_round_trip():
    """Test forward->width_inverse round trip consistency."""
    # Start with specimen width and tension
    original_width = 100 * u.mm
    tension = 10 * u.N / u.mm

    # Forward: calculate breaking strength
    breaking_strength = nominal_breaking_strength_of_textile_belt_specimen(
        specimen_width=original_width,
        width_related_nominal_breaking_tension=tension,
    )

    # Inverse: recover specimen width
    recovered_width = specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
        nominal_breaking_strength=breaking_strength,
        width_related_nominal_breaking_tension=tension,
    )

    # Round-trip should recover original width (within tolerance)
    assert recovered_width.units == original_width.units
    assert abs(recovered_width.magnitude - original_width.magnitude) < 1e-9


def test_forward_to_tension_inverse_round_trip():
    """Test forward->tension_inverse round trip consistency."""
    # Start with specimen width and tension
    width = 100 * u.mm
    original_tension = 10 * u.N / u.mm

    # Forward: calculate breaking strength
    breaking_strength = nominal_breaking_strength_of_textile_belt_specimen(
        specimen_width=width,
        width_related_nominal_breaking_tension=original_tension,
    )

    # Inverse: recover tension
    recovered_tension = width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength=breaking_strength,
        specimen_width=width,
    )

    # Round-trip should recover original tension (within tolerance)
    assert recovered_tension.units == original_tension.units
    assert abs(recovered_tension.magnitude - original_tension.magnitude) < 1e-9


def test_inverse_width_import_surface():
    """Test that width inverse public name is accessible from testing_methods package."""
    import eytelwein.testing_methods

    assert hasattr(
        eytelwein.testing_methods,
        "specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension",
    )
    func = eytelwein.testing_methods.specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension
    assert callable(func)


def test_inverse_tension_import_surface():
    """Test that tension inverse public name is accessible from testing_methods package."""
    import eytelwein.testing_methods

    assert hasattr(
        eytelwein.testing_methods,
        "width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width",
    )
    func = eytelwein.testing_methods.width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width
    assert callable(func)


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
        lower_load_from_nominal_breaking_strength_of_specimen as imported_lower_load,
    )
    from eytelwein.testing_methods import (
        nominal_breaking_strength_of_specimen_from_lower_load as imported_lower_load_inverse,
    )
    from eytelwein.testing_methods import (
        nominal_breaking_strength_of_textile_belt_specimen as imported_func,
    )
    from eytelwein.testing_methods import (
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension as imported_width_inverse,
    )
    from eytelwein.testing_methods import (
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width as imported_tension_inverse,
    )

    assert eytelwein.testing_methods is imported_package
    assert (
        imported_package.nominal_breaking_strength_of_textile_belt_specimen
        is imported_func
    )
    assert (
        imported_package.lower_load_from_nominal_breaking_strength_of_specimen
        is imported_lower_load
    )
    assert (
        imported_package.nominal_breaking_strength_of_specimen_from_lower_load
        is imported_lower_load_inverse
    )
    assert (
        imported_package.specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension
        is imported_width_inverse
    )
    assert (
        imported_package.width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width
        is imported_tension_inverse
    )


# Tests for specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension


def test_specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension_valid_values():
    """Test with valid inputs for width inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension,
    )

    # b = 1000 * T_breaking / T_nominal_tension
    # T_breaking = 1.0 kN, T_nominal_tension = 10 N/mm
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


def test_lower_load_from_nominal_breaking_strength_of_specimen_valid_values():
    """Test lower load forward calculation with default factor."""
    result = lower_load_from_nominal_breaking_strength_of_specimen(
        nominal_breaking_strength_of_specimen=100 * u.kilonewton,
    )
    assert result.magnitude == 6.67
    assert result.units == u.kilonewton


def test_lower_load_from_nominal_breaking_strength_of_specimen_custom_factor_dataset():
    """Test lower load forward calculation with dataset breaking strength and explicit factor."""
    result = lower_load_from_nominal_breaking_strength_of_specimen(
        nominal_breaking_strength_of_specimen=108.36 * u.kilonewton,
        lower_load_factor=0.0667,
    )
    assert result.magnitude == pytest.approx(7.227612, abs=1e-10)
    assert result.units == u.kilonewton


def test_lower_load_from_nominal_breaking_strength_of_specimen_input_unit_conversion():
    """Test lower load forward conversion from equivalent force unit."""
    result = lower_load_from_nominal_breaking_strength_of_specimen(
        nominal_breaking_strength_of_specimen=108360 * u.newton,
        lower_load_factor=0.0667,
    )
    assert result.magnitude == pytest.approx(7.227612, abs=1e-10)
    assert result.units == u.kilonewton


def test_lower_load_from_nominal_breaking_strength_of_specimen_invalid_output_unit():
    """Test lower load forward rejects invalid output unit."""
    with pytest.raises(ValueError):
        lower_load_from_nominal_breaking_strength_of_specimen(
            nominal_breaking_strength_of_specimen=100 * u.kilonewton,
            unit="invalid_unit",
        )


def test_lower_load_from_nominal_breaking_strength_of_specimen_incompatible_output_unit():
    """Test lower load forward rejects incompatible output unit."""
    with pytest.raises(ValueError):
        lower_load_from_nominal_breaking_strength_of_specimen(
            nominal_breaking_strength_of_specimen=100 * u.kilonewton,
            unit="meter",
        )


def test_lower_load_from_nominal_breaking_strength_of_specimen_conversion_error():
    """Test lower load forward rejects invalid breaking-strength input."""
    with pytest.raises(ValueError):
        lower_load_from_nominal_breaking_strength_of_specimen(
            nominal_breaking_strength_of_specimen="not_a_quantity",
        )


def test_lower_load_from_nominal_breaking_strength_of_specimen_invalid_factor():
    """Test lower load forward rejects non-positive factor."""
    with pytest.raises(ValueError):
        lower_load_from_nominal_breaking_strength_of_specimen(
            nominal_breaking_strength_of_specimen=100 * u.kilonewton,
            lower_load_factor=0.0,
        )

    with pytest.raises(ValueError):
        lower_load_from_nominal_breaking_strength_of_specimen(
            nominal_breaking_strength_of_specimen=100 * u.kilonewton,
            lower_load_factor=-0.067,
        )


def test_lower_load_from_nominal_breaking_strength_of_specimen_precision():
    """Test lower load forward precision handling."""
    result = lower_load_from_nominal_breaking_strength_of_specimen(
        nominal_breaking_strength_of_specimen=108.36 * u.kilonewton,
        lower_load_factor=0.0667,
        precision=3,
    )
    assert result.magnitude == pytest.approx(7.228, abs=1e-10)
    assert result.units == u.kilonewton


def test_lower_load_from_nominal_breaking_strength_of_specimen_output_unit_conversion():
    """Test lower load forward output conversion to newton."""
    result = lower_load_from_nominal_breaking_strength_of_specimen(
        nominal_breaking_strength_of_specimen=100 * u.kilonewton,
        unit="newton",
    )
    assert result.magnitude == 6670.0
    assert result.units == u.newton


def test_nominal_breaking_strength_of_specimen_from_lower_load_valid_values():
    """Test lower load inverse calculation with default factor."""
    result = nominal_breaking_strength_of_specimen_from_lower_load(
        lower_load=6.7 * u.kilonewton,
    )
    assert result.magnitude == pytest.approx(100.44977511244379, abs=1e-10)
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_specimen_from_lower_load_custom_factor_dataset():
    """Test lower load inverse calculation with dataset lower load and explicit factor."""
    result = nominal_breaking_strength_of_specimen_from_lower_load(
        lower_load=7.227612 * u.kilonewton,
        lower_load_factor=0.0667,
    )
    assert result.magnitude == pytest.approx(108.36, abs=1e-10)
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_specimen_from_lower_load_input_unit_conversion():
    """Test lower load inverse converts force units correctly."""
    result = nominal_breaking_strength_of_specimen_from_lower_load(
        lower_load=7227.612 * u.newton,
        lower_load_factor=0.0667,
    )
    assert result.magnitude == pytest.approx(108.36, abs=1e-10)
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_specimen_from_lower_load_invalid_output_unit():
    """Test lower load inverse rejects invalid output unit."""
    with pytest.raises(ValueError):
        nominal_breaking_strength_of_specimen_from_lower_load(
            lower_load=6.7 * u.kilonewton,
            unit="invalid_unit",
        )


def test_nominal_breaking_strength_of_specimen_from_lower_load_incompatible_output_unit():
    """Test lower load inverse rejects incompatible output unit."""
    with pytest.raises(ValueError):
        nominal_breaking_strength_of_specimen_from_lower_load(
            lower_load=6.7 * u.kilonewton,
            unit="meter",
        )


def test_nominal_breaking_strength_of_specimen_from_lower_load_conversion_error():
    """Test lower load inverse rejects invalid lower-load input."""
    with pytest.raises(ValueError):
        nominal_breaking_strength_of_specimen_from_lower_load(
            lower_load="not_a_quantity",
        )


def test_nominal_breaking_strength_of_specimen_from_lower_load_invalid_factor():
    """Test lower load inverse rejects non-positive factor."""
    with pytest.raises(ValueError):
        nominal_breaking_strength_of_specimen_from_lower_load(
            lower_load=6.7 * u.kilonewton,
            lower_load_factor=0.0,
        )

    with pytest.raises(ValueError):
        nominal_breaking_strength_of_specimen_from_lower_load(
            lower_load=6.7 * u.kilonewton,
            lower_load_factor=-0.067,
        )


def test_nominal_breaking_strength_of_specimen_from_lower_load_precision():
    """Test lower load inverse precision handling."""
    result = nominal_breaking_strength_of_specimen_from_lower_load(
        lower_load=7.227612 * u.kilonewton,
        lower_load_factor=0.0667,
        precision=2,
    )
    assert result.magnitude == pytest.approx(108.36, abs=1e-10)
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_specimen_from_lower_load_output_unit_conversion():
    """Test lower load inverse output conversion to newton."""
    result = nominal_breaking_strength_of_specimen_from_lower_load(
        lower_load=6.7 * u.kilonewton,
        unit="newton",
    )
    assert result.magnitude == pytest.approx(100449.7751124438, abs=1e-10)
    assert result.units == u.newton


def test_lower_load_round_trip_public_dataset_with_default_factor():
    """Test lower load public round trip with dataset breaking strength and default factor."""
    lower_load = lower_load_from_nominal_breaking_strength_of_specimen(
        nominal_breaking_strength_of_specimen=108.36 * u.kilonewton,
    )
    recovered_breaking_strength = nominal_breaking_strength_of_specimen_from_lower_load(
        lower_load=lower_load,
    )
    assert lower_load.magnitude == pytest.approx(7.227612, abs=1e-10)
    assert lower_load.units == u.kilonewton
    assert recovered_breaking_strength.magnitude == pytest.approx(108.36, abs=1e-10)
    assert recovered_breaking_strength.units == u.kilonewton


def test_lower_load_import_surface():
    """Test that lower load public name is accessible from testing_methods package."""
    import eytelwein.testing_methods

    assert hasattr(
        eytelwein.testing_methods,
        "lower_load_from_nominal_breaking_strength_of_specimen",
    )
    func = eytelwein.testing_methods.lower_load_from_nominal_breaking_strength_of_specimen
    assert callable(func)


def test_lower_load_inverse_import_surface():
    """Test that lower load inverse public name is accessible from testing_methods package."""
    import eytelwein.testing_methods

    assert hasattr(
        eytelwein.testing_methods,
        "nominal_breaking_strength_of_specimen_from_lower_load",
    )
    func = eytelwein.testing_methods.nominal_breaking_strength_of_specimen_from_lower_load
    assert callable(func)


# Tests for width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width


def test_width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width_valid_values():
    """Test with valid inputs for tension inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width,
    )

    # k_N = 1000 * T_breaking / b
    # T_breaking = 1.0 kN, b = 100 mm
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


# Tests for relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen


def test_relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen_valid_values():
    """Test forward relative reference splice efficiency with valid values."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    # T_rel_fatigue = T_upper / T_breaking * 100
    # T_upper = 5 kN, T_breaking = 10 kN
    # Result: 5 / 10 * 100 = 50 percent
    result = relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load=5 * u.kilonewton,
        nominal_breaking_strength_of_specimen=10 * u.kilonewton,
    )
    assert result.magnitude == 50.0
    assert result.units == u.percent


def test_relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen_input_unit_conversion():
    """Test that input units are converted correctly for forward function."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    # 5000 N = 5 kN, 10000 N = 10 kN
    result = relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load=5000 * u.newton,
        nominal_breaking_strength_of_specimen=10000 * u.newton,
    )
    assert result.magnitude == 50.0
    assert result.units == u.percent


def test_relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen_invalid_output_unit():
    """Test that invalid output unit raises ValueError for forward function."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    with pytest.raises(ValueError):
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
            reference_upper_load=5 * u.kilonewton,
            nominal_breaking_strength_of_specimen=10 * u.kilonewton,
            unit="invalid_unit",
        )


def test_relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen_incompatible_output_unit():
    """Test that incompatible output unit raises ValueError for forward function."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    with pytest.raises(ValueError):
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
            reference_upper_load=5 * u.kilonewton,
            nominal_breaking_strength_of_specimen=10 * u.kilonewton,
            unit="meter",
        )


def test_relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen_conversion_error():
    """Test that invalid input raises ValueError for forward function."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    with pytest.raises(ValueError):
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
            reference_upper_load="not_a_quantity",
            nominal_breaking_strength_of_specimen=10 * u.kilonewton,
        )


def test_relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen_nominal_breaking_strength_conversion_error():
    """Test that invalid nominal_breaking_strength_of_specimen input raises ValueError for forward function."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    with pytest.raises(ValueError):
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
            reference_upper_load=5 * u.kilonewton,
            nominal_breaking_strength_of_specimen="not_a_quantity",
        )


def test_relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen_positive_denominator_validation():
    """Test that non-positive nominal breaking strength raises ValueError for forward function."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    with pytest.raises(ValueError):
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
            reference_upper_load=5 * u.kilonewton,
            nominal_breaking_strength_of_specimen=0 * u.kilonewton,
        )

    with pytest.raises(ValueError):
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
            reference_upper_load=5 * u.kilonewton,
            nominal_breaking_strength_of_specimen=-10 * u.kilonewton,
        )


def test_relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen_percent_output_behavior():
    """Test that default output unit is percent for forward function."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    result = relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load=5 * u.kilonewton,
        nominal_breaking_strength_of_specimen=10 * u.kilonewton,
    )
    assert str(result.units) == "percent"


def test_relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen_dimensionless_output_conversion():
    """Test output conversion to dimensionless for forward function."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    result = relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load=5 * u.kilonewton,
        nominal_breaking_strength_of_specimen=10 * u.kilonewton,
        unit="dimensionless",
    )
    assert result.magnitude == 0.5
    assert result.units == u.dimensionless


def test_relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen_precision():
    """Test that precision parameter works correctly for forward function."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    result = relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load=5.123 * u.kilonewton,
        nominal_breaking_strength_of_specimen=10 * u.kilonewton,
        precision=1,
    )
    assert result.magnitude == 51.2
    assert result.units == u.percent


# Tests for reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen


def test_reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen_valid_values():
    """Test inverse reference upper load with valid values."""
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    )

    # T_upper = T_rel_fatigue / 100 * T_breaking
    # T_rel_fatigue = 50 percent, T_breaking = 10 kN
    # Result: 50 / 100 * 10 = 5 kN
    result = reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
        relative_reference_splice_efficiency=50 * u.percent,
        nominal_breaking_strength_of_specimen=10 * u.kilonewton,
    )
    assert result.magnitude == 5.0
    assert result.units == u.kilonewton


def test_reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen_unit_conversion():
    """Test that input units are converted correctly for reference upper load inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    )

    # 0.5 dimensionless = 50 percent, 10000 N = 10 kN
    result = reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
        relative_reference_splice_efficiency=0.5 * u.dimensionless,
        nominal_breaking_strength_of_specimen=10000 * u.newton,
    )
    assert result.magnitude == 5.0
    assert result.units == u.kilonewton


def test_reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen_invalid_output_unit():
    """Test that invalid output unit raises ValueError for reference upper load inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    )

    with pytest.raises(ValueError):
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
            relative_reference_splice_efficiency=50 * u.percent,
            nominal_breaking_strength_of_specimen=10 * u.kilonewton,
            unit="invalid_unit",
        )


def test_reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen_incompatible_output_unit():
    """Test that incompatible output unit raises ValueError for reference upper load inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    )

    with pytest.raises(ValueError):
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
            relative_reference_splice_efficiency=50 * u.percent,
            nominal_breaking_strength_of_specimen=10 * u.kilonewton,
            unit="meter",
        )


def test_reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen_precision():
    """Test that precision parameter works correctly for reference upper load inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    )

    result = reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
        relative_reference_splice_efficiency=50.123 * u.percent,
        nominal_breaking_strength_of_specimen=10 * u.kilonewton,
        precision=2,
    )
    assert result.magnitude == 5.01
    assert result.units == u.kilonewton


def test_reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen_conversion_error_bad_efficiency():
    """Test that invalid efficiency input raises ValueError for reference upper load inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    )

    with pytest.raises(ValueError):
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
            relative_reference_splice_efficiency="not_a_quantity",
            nominal_breaking_strength_of_specimen=10 * u.kilonewton,
        )


def test_reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen_conversion_error_bad_nominal_breaking_strength():
    """Test that invalid nominal breaking strength input raises ValueError for reference upper load inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    )

    with pytest.raises(ValueError):
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
            relative_reference_splice_efficiency=50 * u.percent,
            nominal_breaking_strength_of_specimen="not_a_quantity",
        )


def test_reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen_output_unit_conversion():
    """Test that output can be converted to different units for reference upper load inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    )

    # 5 kN = 5000 N
    result = reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
        relative_reference_splice_efficiency=50 * u.percent,
        nominal_breaking_strength_of_specimen=10 * u.kilonewton,
        unit="newton",
    )
    assert result.magnitude == 5000.0
    assert result.units == u.newton


# Tests for nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency


def test_nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency_valid_values():
    """Test inverse nominal breaking strength with valid values."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    # T_breaking = T_upper / (T_rel_fatigue / 100)
    # T_upper = 5 kN, T_rel_fatigue = 50 percent
    # Result: 5 / (50 / 100) = 5 / 0.5 = 10 kN
    result = nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
        reference_upper_load=5 * u.kilonewton,
        relative_reference_splice_efficiency=50 * u.percent,
    )
    assert result.magnitude == 10.0
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency_unit_conversion():
    """Test that input units are converted correctly for nominal breaking strength inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    # 5000 N = 5 kN, 0.5 dimensionless = 50 percent
    result = nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
        reference_upper_load=5000 * u.newton,
        relative_reference_splice_efficiency=0.5 * u.dimensionless,
    )
    assert result.magnitude == 10.0
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency_invalid_output_unit():
    """Test that invalid output unit raises ValueError for nominal breaking strength inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    with pytest.raises(ValueError):
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
            reference_upper_load=5 * u.kilonewton,
            relative_reference_splice_efficiency=50 * u.percent,
            unit="invalid_unit",
        )


def test_nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency_incompatible_output_unit():
    """Test that incompatible output unit raises ValueError for nominal breaking strength inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    with pytest.raises(ValueError):
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
            reference_upper_load=5 * u.kilonewton,
            relative_reference_splice_efficiency=50 * u.percent,
            unit="meter",
        )


def test_nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency_positive_denominator_validation():
    """Test that non-positive relative reference splice efficiency raises ValueError."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    with pytest.raises(ValueError):
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
            reference_upper_load=5 * u.kilonewton,
            relative_reference_splice_efficiency=0 * u.percent,
        )

    with pytest.raises(ValueError):
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
            reference_upper_load=5 * u.kilonewton,
            relative_reference_splice_efficiency=-50 * u.percent,
        )


def test_nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency_precision():
    """Test that precision parameter works correctly for nominal breaking strength inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    result = nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
        reference_upper_load=5 * u.kilonewton,
        relative_reference_splice_efficiency=50.123 * u.percent,
        precision=2,
    )
    assert result.magnitude == 9.98
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency_conversion_error_bad_reference_upper_load():
    """Test that invalid reference upper load input raises ValueError for nominal breaking strength inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    with pytest.raises(ValueError):
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
            reference_upper_load="not_a_quantity",
            relative_reference_splice_efficiency=50 * u.percent,
        )


def test_nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency_conversion_error_bad_efficiency():
    """Test that invalid efficiency input raises ValueError for nominal breaking strength inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    with pytest.raises(ValueError):
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
            reference_upper_load=5 * u.kilonewton,
            relative_reference_splice_efficiency="not_a_quantity",
        )


def test_nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency_output_unit_conversion():
    """Test that output can be converted to different units for nominal breaking strength inverse."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    # 10 kN = 10000 N
    result = nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
        reference_upper_load=5 * u.kilonewton,
        relative_reference_splice_efficiency=50 * u.percent,
        unit="newton",
    )
    assert result.magnitude == 10000.0
    assert result.units == u.newton


# Import surface tests for relative reference splice efficiency functions


def test_relative_reference_splice_efficiency_import_from_core():
    """Test that relative reference splice efficiency forward is accessible from core.belt_joints."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    assert callable(
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen
    )


def test_reference_upper_load_import_from_core():
    """Test that reference upper load inverse is accessible from core.belt_joints."""
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    )

    assert callable(
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen
    )


def test_nominal_breaking_strength_of_specimen_import_from_core():
    """Test that nominal breaking strength of specimen inverse is accessible from core.belt_joints."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    assert callable(
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency
    )


def test_relative_reference_splice_efficiency_import_from_testing_methods():
    """Test that relative reference splice efficiency forward is accessible from eytelwein.testing_methods."""
    from eytelwein.testing_methods import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    assert callable(
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen
    )


def test_reference_upper_load_import_from_testing_methods():
    """Test that reference upper load inverse is accessible from eytelwein.testing_methods."""
    from eytelwein.testing_methods import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    )

    assert callable(
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen
    )


def test_nominal_breaking_strength_of_specimen_import_from_testing_methods():
    """Test that nominal breaking strength of specimen inverse is accessible from eytelwein.testing_methods."""
    from eytelwein.testing_methods import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    assert callable(
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency
    )


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


# Phase 3: Round-trip coverage and import-surface checks for splice efficiency


def test_forward_to_reference_upper_load_inverse_round_trip():
    """Test forward->reference_upper_load_inverse round trip consistency."""
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    # Start with reference upper load and breaking strength
    original_reference_upper_load = 5 * u.kilonewton
    breaking_strength = 10 * u.kilonewton

    # Forward: calculate relative reference splice efficiency
    efficiency = relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load=original_reference_upper_load,
        nominal_breaking_strength_of_specimen=breaking_strength,
    )

    # Inverse: recover reference upper load
    recovered_reference_upper_load = reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
        relative_reference_splice_efficiency=efficiency,
        nominal_breaking_strength_of_specimen=breaking_strength,
    )

    # Round-trip should recover original reference upper load (within tolerance)
    assert recovered_reference_upper_load.units == original_reference_upper_load.units
    assert (
        abs(
            recovered_reference_upper_load.magnitude
            - original_reference_upper_load.magnitude
        )
        < 1e-9
    )


def test_forward_to_nominal_breaking_strength_inverse_round_trip():
    """Test forward->nominal_breaking_strength_inverse round trip consistency."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    # Start with reference upper load and breaking strength
    reference_upper_load = 5 * u.kilonewton
    original_breaking_strength = 10 * u.kilonewton

    # Forward: calculate relative reference splice efficiency
    efficiency = relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load=reference_upper_load,
        nominal_breaking_strength_of_specimen=original_breaking_strength,
    )

    # Inverse: recover breaking strength
    recovered_breaking_strength = nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
        reference_upper_load=reference_upper_load,
        relative_reference_splice_efficiency=efficiency,
    )

    # Round-trip should recover original breaking strength (within tolerance)
    assert recovered_breaking_strength.units == original_breaking_strength.units
    assert (
        abs(
            recovered_breaking_strength.magnitude - original_breaking_strength.magnitude
        )
        < 1e-9
    )


def test_splice_efficiency_functions_import_from_testing_methods_identity():
    """Test that splice efficiency functions are accessible from eytelwein.testing_methods with identity checks."""
    import eytelwein.testing_methods
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency as core_breaking,
    )
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen as core_ref_upper,
    )
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen as core_forward,
    )

    # Import from package and check identity
    assert (
        eytelwein.testing_methods.relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen
        is core_forward
    )
    assert (
        eytelwein.testing_methods.reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen
        is core_ref_upper
    )
    assert (
        eytelwein.testing_methods.nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency
        is core_breaking
    )


# Phase 2: Dataset correctness tests for nominal breaking strength triad
# Approved dataset: b = 172 mm, T_nominal_tension = 630 N/mm, T_breaking = 172 * 630 / 1000 = 108.36 kN


def test_nominal_breaking_strength_dataset_forward():
    """Test nominal breaking strength forward with approved dataset."""
    # T_breaking = b * T_nominal_tension = 172 mm * 630 N/mm = 108360 N = 108.36 kN
    result = nominal_breaking_strength_of_textile_belt_specimen(
        specimen_width=172 * u.mm,
        width_related_nominal_breaking_tension=630 * u.N / u.mm,
    )
    assert result.magnitude == 108.36
    assert result.units == u.kilonewton


def test_specimen_width_dataset_inverse():
    """Test specimen width inverse with approved dataset."""
    # b = 1000 * T_breaking / T_nominal_tension = 1000 * 108.36 kN / 630 N/mm = 172 mm
    result = specimen_width_from_nominal_breaking_strength_and_width_related_nominal_breaking_tension(
        nominal_breaking_strength=108.36 * u.kilonewton,
        width_related_nominal_breaking_tension=630 * u.N / u.mm,
    )
    assert result.magnitude == 172.0
    assert result.units == u.millimeter


def test_width_related_tension_dataset_inverse():
    """Test width-related nominal breaking tension inverse with approved dataset."""
    # T_nominal_tension = 1000 * T_breaking / b = 1000 * 108.36 kN / 172 mm = 630 N/mm
    result = width_related_nominal_breaking_tension_from_nominal_breaking_strength_and_specimen_width(
        nominal_breaking_strength=108.36 * u.kilonewton,
        specimen_width=172 * u.mm,
    )
    assert result.magnitude == 630.0
    assert result.units == u.N / u.mm


# Phase 3: Dataset correctness tests for splice-efficiency triad
# Approved dataset: T_breaking = 108.36 kN, T_upper = 32.508 kN, T_rel_fatigue = 30 %


def test_relative_reference_splice_efficiency_dataset_forward():
    """Test relative reference splice efficiency forward with approved dataset."""
    from eytelwein.testing_methods.core.belt_joints import (
        relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen,
    )

    # T_rel_fatigue = T_upper / T_breaking * 100 = 32.508 kN / 108.36 kN * 100 = 30 %
    result = relative_reference_splice_efficiency_from_reference_upper_load_and_nominal_breaking_strength_of_specimen(
        reference_upper_load=32.508 * u.kilonewton,
        nominal_breaking_strength_of_specimen=108.36 * u.kilonewton,
    )
    assert result.magnitude == pytest.approx(30.0)
    assert result.units == u.percent


def test_reference_upper_load_dataset_inverse():
    """Test reference upper load inverse with approved dataset."""
    from eytelwein.testing_methods.core.belt_joints import (
        reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen,
    )

    # T_upper = T_rel_fatigue / 100 * T_breaking = 30 % / 100 * 108.36 kN = 32.508 kN
    result = reference_upper_load_from_relative_reference_splice_efficiency_and_nominal_breaking_strength_of_specimen(
        relative_reference_splice_efficiency=30 * u.percent,
        nominal_breaking_strength_of_specimen=108.36 * u.kilonewton,
    )
    assert result.magnitude == pytest.approx(32.508)
    assert result.units == u.kilonewton


def test_nominal_breaking_strength_of_specimen_dataset_inverse():
    """Test nominal breaking strength of specimen inverse with approved dataset."""
    from eytelwein.testing_methods.core.belt_joints import (
        nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency,
    )

    # T_breaking = T_upper / (T_rel_fatigue / 100) = 32.508 kN / (30 % / 100) = 32.508 kN / 0.30 = 108.36 kN
    result = nominal_breaking_strength_of_specimen_from_reference_upper_load_and_relative_reference_splice_efficiency(
        reference_upper_load=32.508 * u.kilonewton,
        relative_reference_splice_efficiency=30 * u.percent,
    )
    assert result.magnitude == pytest.approx(108.36)
    assert result.units == u.kilonewton
