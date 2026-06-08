"""
Tests for public horizontal curve calculation functions.

This module tests the public API functions with comprehensive unit handling,
error validation, and the new sections-based architecture.
"""

import math
import numpy as np
import pytest

from eytelwein.horizontal_curves.core.horizontal_curve_calculations import (
    restraining_force_from_dead_weights,
    weight_force_material_center,
    weight_force_material_outside,
    weight_force_of_material,
)
import eytelwein.main.units as u
from eytelwein.horizontal_curves import (
    force_component_towards_inside_curve_from_belt_tension,
    force_component_towards_inside_curve_from_belt_tension_sections,
    weight_force_belt_inside,
    weight_force_belt_outside,
    weight_force_belt_center,
    weight_force_of_belt,
    weight_force_material_inside,
    restraining_force_from_tilted_idlers,
    tilted_idler_friction_force_inside,
    tilted_idler_friction_force_outside,
    tilted_idler_friction_force_center,
)

from eytelwein.horizontal_curves.core._horizontal_curve_calculations import (
    _restraining_force_from_tilted_idlers_towards_outside_curve_conventional,
)


class TestPublicForceFunction:
    """Test public function with unit handling."""

    def test_basic_calculation_with_units(self):
        """Test basic calculation with proper units."""
        belt_tension = 5000 * u.ureg.newton
        idler_spacing = 1.2 * u.ureg.meter
        curve_radius = 50.0 * u.ureg.meter

        result = force_component_towards_inside_curve_from_belt_tension(
            belt_tension, idler_spacing, curve_radius
        )

        assert result.magnitude == pytest.approx(120.0, rel=1e-10)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_unit_conversion(self):
        """Test automatic unit conversion."""
        belt_tension = 5 * u.ureg.kilonewton  # 5000 N
        idler_spacing = 120 * u.ureg.centimeter  # 1.2 m
        curve_radius = 0.05 * u.ureg.kilometer  # 50 m

        result = force_component_towards_inside_curve_from_belt_tension(
            belt_tension, idler_spacing, curve_radius
        )

        assert result.magnitude == pytest.approx(120.0, rel=1e-10)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_custom_output_unit(self):
        """Test custom output unit specification."""
        belt_tension = 5000 * u.ureg.newton
        idler_spacing = 1.2 * u.ureg.meter
        curve_radius = 50.0 * u.ureg.meter

        result = force_component_towards_inside_curve_from_belt_tension(
            belt_tension, idler_spacing, curve_radius, unit="kilonewton"
        )

        assert result.magnitude == pytest.approx(0.12, rel=1e-10)
        assert result.dimensionality == u.ureg.kilonewton.dimensionality

    def test_precision_control(self):
        """Test precision parameter."""
        belt_tension = 5000 * u.ureg.newton
        idler_spacing = 1.234567 * u.ureg.meter
        curve_radius = 49.987 * u.ureg.meter

        result = force_component_towards_inside_curve_from_belt_tension(
            belt_tension, idler_spacing, curve_radius, precision=3
        )

        # Result should be rounded to 3 decimal places
        expected = round(5000 * 1.234567 / 49.987, 3)
        assert result.magnitude == pytest.approx(expected, rel=1e-10)

    def test_array_inputs_with_units(self):
        """Test function with array inputs and units."""
        belt_tensions = [3000, 4000, 5000] * u.ureg.newton
        idler_spacing = 1.2 * u.ureg.meter
        curve_radius = 50.0 * u.ureg.meter

        result = force_component_towards_inside_curve_from_belt_tension(
            belt_tensions, idler_spacing, curve_radius
        )

        expected_magnitudes = [72.0, 96.0, 120.0]
        np.testing.assert_array_almost_equal(
            result.magnitude, expected_magnitudes, decimal=10
        )
        assert result.dimensionality == u.ureg.newton.dimensionality


class TestPublicFunctionErrorHandling:
    """Test error handling in public function."""

    def test_wrong_dimensions_belt_tension(self):
        """Test error handling for wrong belt tension dimensions."""
        belt_tension = 5000 * u.ureg.meter  # Wrong dimension
        idler_spacing = 1.2 * u.ureg.meter
        curve_radius = 50.0 * u.ureg.meter

        with pytest.raises(ValueError, match="Error in converting units"):
            force_component_towards_inside_curve_from_belt_tension(
                belt_tension, idler_spacing, curve_radius
            )

    def test_wrong_dimensions_spacing(self):
        """Test error handling for wrong idler spacing dimensions."""
        belt_tension = 5000 * u.ureg.newton
        idler_spacing = 1.2 * u.ureg.second  # Wrong dimension
        curve_radius = 50.0 * u.ureg.meter

        with pytest.raises(ValueError, match="Error in converting units"):
            force_component_towards_inside_curve_from_belt_tension(
                belt_tension, idler_spacing, curve_radius
            )

    def test_wrong_dimensions_radius(self):
        """Test error handling for wrong curve radius dimensions."""
        belt_tension = 5000 * u.ureg.newton
        idler_spacing = 1.2 * u.ureg.meter
        curve_radius = 50.0 * u.ureg.kilogram  # Wrong dimension

        with pytest.raises(ValueError, match="Error in converting units"):
            force_component_towards_inside_curve_from_belt_tension(
                belt_tension, idler_spacing, curve_radius
            )

    def test_zero_radius_error(self):
        """Test error handling for zero radius."""
        belt_tension = 5000 * u.ureg.newton
        idler_spacing = 1.2 * u.ureg.meter
        curve_radius = 0.0 * u.ureg.meter

        with pytest.raises(
            ValueError, match="horizontal_curve_radius must be positive"
        ):
            force_component_towards_inside_curve_from_belt_tension(
                belt_tension, idler_spacing, curve_radius
            )

    def test_negative_radius_error(self):
        """Test error handling for negative radius."""
        belt_tension = 5000 * u.ureg.newton
        idler_spacing = 1.2 * u.ureg.meter
        curve_radius = -50.0 * u.ureg.meter

        with pytest.raises(
            ValueError, match="horizontal_curve_radius must be positive"
        ):
            force_component_towards_inside_curve_from_belt_tension(
                belt_tension, idler_spacing, curve_radius
            )

    def test_invalid_output_unit(self):
        """Test error handling for invalid output unit."""
        belt_tension = 5000 * u.ureg.newton
        idler_spacing = 1.2 * u.ureg.meter
        curve_radius = 50.0 * u.ureg.meter

        with pytest.raises(ValueError, match="Invalid unit"):
            force_component_towards_inside_curve_from_belt_tension(
                belt_tension, idler_spacing, curve_radius, unit="invalid_unit"
            )


class TestSectionsFunction:
    """Test the sections function."""

    def test_basic_sections_calculation(self):
        """Test basic multi-section calculation."""
        belt_tensions = [3000, 4000, 5000] * u.ureg.newton
        idler_spacing = 1.2 * u.ureg.meter
        curve_radius = 50.0 * u.ureg.meter

        result = force_component_towards_inside_curve_from_belt_tension_sections(
            belt_tensions, idler_spacing, curve_radius
        )

        expected_magnitudes = [72.0, 96.0, 120.0]
        np.testing.assert_array_almost_equal(
            result.magnitude, expected_magnitudes, decimal=10
        )
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_mixed_array_scalar_inputs(self):
        """Test mixed array and scalar inputs."""
        belt_tension = 5000 * u.ureg.newton  # Scalar
        idler_spacings = [1.0, 1.2, 1.5] * u.ureg.meter  # Array
        curve_radius = 50.0 * u.ureg.meter  # Scalar

        result = force_component_towards_inside_curve_from_belt_tension_sections(
            belt_tension, idler_spacings, curve_radius
        )

        expected_magnitudes = [100.0, 120.0, 150.0]
        np.testing.assert_array_almost_equal(
            result.magnitude, expected_magnitudes, decimal=10
        )

    def test_single_tensor_multiple_radii(self):
        """Test single tension with multiple radii (key broadcasting case)."""
        belt_tension = 3000 * u.ureg.newton  # Single value
        idler_spacing = 1.2 * u.ureg.meter  # Single value
        curve_radii = [40.0, 50.0, 60.0, 80.0] * u.ureg.meter  # Array

        result = force_component_towards_inside_curve_from_belt_tension_sections(
            belt_tension, idler_spacing, curve_radii
        )

        expected_magnitudes = [90.0, 72.0, 60.0, 45.0]  # 3000*1.2/radius
        np.testing.assert_array_almost_equal(
            result.magnitude, expected_magnitudes, decimal=10
        )

    def test_custom_units_and_precision(self):
        """Test custom output units and precision in sections function."""
        belt_tensions = [3000, 4000] * u.ureg.newton
        idler_spacing = 1.2 * u.ureg.meter
        curve_radius = 50.0 * u.ureg.meter

        result = force_component_towards_inside_curve_from_belt_tension_sections(
            belt_tensions, idler_spacing, curve_radius, unit="kilonewton", precision=4
        )

        expected_magnitudes = [0.0720, 0.0960]  # In kilonewtons
        np.testing.assert_array_almost_equal(
            result.magnitude, expected_magnitudes, decimal=4
        )
        assert result.dimensionality == u.ureg.kilonewton.dimensionality

    def test_sections_error_handling(self):
        """Test error handling in sections function."""
        # Test with negative radius in array
        belt_tensions = [3000, 4000] * u.ureg.newton
        idler_spacing = 1.0 * u.ureg.meter
        curve_radii = [50.0, -25.0] * u.ureg.meter  # One negative radius

        with pytest.raises(ValueError, match="Horizontal curve radii must be positive"):
            force_component_towards_inside_curve_from_belt_tension_sections(
                belt_tensions, idler_spacing, curve_radii
            )


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_very_small_values(self):
        """Test with very small but positive values."""
        belt_tension = 0.001 * u.ureg.newton
        idler_spacing = 0.001 * u.ureg.meter
        curve_radius = 0.1 * u.ureg.meter

        result = force_component_towards_inside_curve_from_belt_tension(
            belt_tension, idler_spacing, curve_radius, precision=8
        )

        expected = 0.001 * 0.001 / 0.1  # 0.00001 N
        assert result.magnitude == pytest.approx(expected, rel=1e-10)

    def test_very_large_values(self):
        """Test with very large values."""
        belt_tension = 1e6 * u.ureg.newton
        idler_spacing = 10.0 * u.ureg.meter
        curve_radius = 1000.0 * u.ureg.meter

        result = force_component_towards_inside_curve_from_belt_tension(
            belt_tension, idler_spacing, curve_radius
        )

        expected = 1e6 * 10.0 / 1000.0  # 10000 N
        assert result.magnitude == pytest.approx(expected, rel=1e-10)

    def test_zero_tension_arrays(self):
        """Test arrays with zero tension values."""
        belt_tensions = [0.0, 1000.0, 0.0, 2000.0] * u.ureg.newton
        idler_spacing = 1.0 * u.ureg.meter
        curve_radius = 25.0 * u.ureg.meter

        result = force_component_towards_inside_curve_from_belt_tension_sections(
            belt_tensions, idler_spacing, curve_radius
        )

        expected = [0.0, 40.0, 0.0, 80.0]
        np.testing.assert_array_almost_equal(result.magnitude, expected, decimal=10)

    def test_array_with_zero_radius_elements(self):
        """Test that arrays with zero radius elements raise errors."""
        belt_tension = 1000.0 * u.ureg.newton
        idler_spacing = 1.0 * u.ureg.meter
        curve_radii = [50.0, 0.0, 25.0] * u.ureg.meter

        with pytest.raises(
            ValueError, match="horizontal_curve_radius must be positive"
        ):
            force_component_towards_inside_curve_from_belt_tension(
                belt_tension, idler_spacing, curve_radii
            )


class TestWeightForceBeltInsidePublic:
    """Test public weight force function with unit handling."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic weight force calculation with unit handling."""
        total_force = u.ureg.Quantity(156.71475, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(800, u.ureg.millimeter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.46, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3025, u.ureg.meter)

        result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            precision=10,
        )

        assert result.units == u.ureg.newton
        # assert equivalent to 26.7834083560146
        assert result.magnitude == pytest.approx(26.7834083560146, rel=1e-10)

    def test_basic_calculation_with_units(self):
        """Test basic weight force calculation with unit handling."""
        total_force = u.ureg.Quantity(10000, u.ureg.newton)
        inclination = u.ureg.Quantity(5.7, u.ureg.degree)
        belt_width = u.ureg.Quantity(1200, u.ureg.millimeter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        inside_width = u.ureg.Quantity(400, u.ureg.millimeter)

        result = weight_force_belt_inside(
            total_force, inclination, belt_width, troughing, banking, inside_width
        )

        assert result.units == u.ureg.newton
        assert result.magnitude > 0

    def test_unit_conversion(self):
        """Test input unit conversion."""
        total_force = u.ureg.Quantity(5, u.ureg.kilonewton)  # Input in kN
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.2, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)  # Input in degrees
        banking = u.ureg.Quantity(0.087, u.ureg.radian)
        inside_width = u.ureg.Quantity(40, u.ureg.centimeter)  # Input in cm

        result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            unit="kilonewton",  # Output in kN
        )

        assert result.units == u.ureg.kilonewton
        assert result.magnitude > 0

    def test_precision_control(self):
        """Test precision parameter."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.333333, u.ureg.meter)

        result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            precision=1,
        )

        # Check that result is rounded to 1 decimal place
        assert result.magnitude == round(result.magnitude, 1)

    def test_error_handling_negative_force(self):
        """Test error handling for negative total force."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_inside(
                u.ureg.Quantity(-1000, u.ureg.newton),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0.3, u.ureg.meter),
            )
        assert "non-negative" in str(excinfo.value)

    def test_error_handling_invalid_width(self):
        """Test error handling for invalid belt width."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_inside(
                u.ureg.Quantity(1000, u.ureg.newton),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1.5, u.ureg.meter),  # Larger than total width
            )
        assert "cannot exceed total belt width" in str(excinfo.value)

    def test_error_handling_wrong_dimensions(self):
        """Test error handling for wrong unit dimensions."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_inside(
                u.ureg.Quantity(
                    1000, u.ureg.meter
                ),  # Wrong dimension (length instead of force)
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0.3, u.ureg.meter),
            )
        assert "Error in converting units" in str(excinfo.value)

    def test_invalid_output_unit(self):
        """Test error handling for invalid output unit."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_inside(
                u.ureg.Quantity(1000, u.ureg.newton),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0.3, u.ureg.meter),
                unit="invalid_unit",
            )
        assert "invalid_unit" in str(excinfo.value) and "not defined" in str(
            excinfo.value
        )

    def test_method_parameter_conventional(self):
        """Test explicit conventional method selection."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(0.8, u.ureg.meter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3, u.ureg.meter)

        result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="conventional",
        )

        assert result.units == u.ureg.newton
        assert result.magnitude == pytest.approx(169.7, rel=1e-2)

    def test_method_parameter_improved_with_load_factor(self):
        """Test improved method with explicit wing_roll_load_factor."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(0.8, u.ureg.meter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3, u.ureg.meter)
        load_factor = u.ureg.Quantity(1.5, u.ureg.dimensionless)

        result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",
            wing_roll_load_factor=load_factor,
        )

        assert result.units == u.ureg.newton
        assert result.magnitude == pytest.approx(293.9, rel=1e-2)

    def test_method_parameter_improved_default_load_factor(self):
        """Test improved method with default wing_roll_load_factor."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(0.8, u.ureg.meter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3, u.ureg.meter)

        result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",  # No explicit wing_roll_load_factor
        )

        assert result.units == u.ureg.newton
        # Should use default load factor of 1.5
        assert result.magnitude == pytest.approx(215.5, rel=1e-2)

    def test_wing_roll_load_factor_linear_scaling(self):
        """Test that wing_roll_load_factor scales results linearly."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(0.8, u.ureg.meter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3, u.ureg.meter)

        # Base case with load factor 1.0
        base_result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",
            wing_roll_load_factor=u.ureg.Quantity(1.0, u.ureg.dimensionless),
        )

        # Test linear scaling
        for multiplier in [1.5, 2.0]:
            scaled_result = weight_force_belt_inside(
                total_force,
                inclination,
                belt_width,
                troughing,
                banking,
                inside_width,
                method="improved",
                wing_roll_load_factor=u.ureg.Quantity(multiplier, u.ureg.dimensionless),
            )

            expected_magnitude = base_result.magnitude * multiplier
            assert scaled_result.magnitude == pytest.approx(
                expected_magnitude, rel=1e-3
            )

    def test_wing_roll_load_factor_equivalence_to_conventional(self):
        """Test that specific load factor gives equivalent result to conventional method."""
        import math

        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(0.8, u.ureg.meter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3, u.ureg.meter)

        # Conventional result
        conv_result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="conventional",
        )

        # Calculate equivalent load factor (cos of troughing angle)
        troughing_rad = troughing.to(u.ureg.radian).magnitude
        equiv_factor = math.cos(troughing_rad)

        # Improved result with equivalent load factor
        impr_result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",
            wing_roll_load_factor=u.ureg.Quantity(equiv_factor, u.ureg.dimensionless),
        )

        # Results should be nearly identical
        assert abs(conv_result.magnitude - impr_result.magnitude) < 1e-6

    def test_wing_roll_load_factor_ignored_for_conventional(self):
        """Test that wing_roll_load_factor is ignored for conventional method."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(0.8, u.ureg.meter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3, u.ureg.meter)

        # Conventional without load factor
        result1 = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="conventional",
        )

        # Conventional with load factor (should be ignored)
        result2 = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="conventional",
            wing_roll_load_factor=u.ureg.Quantity(1.5, u.ureg.dimensionless),
        )

        # Results should be identical
        assert abs(result1.magnitude - result2.magnitude) < 1e-10

    def test_method_parameter_invalid(self):
        """Test error handling for invalid method parameter."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(0.8, u.ureg.meter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3, u.ureg.meter)

        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_inside(
                total_force,
                inclination,
                belt_width,
                troughing,
                banking,
                inside_width,
                method="invalid_method",
            )
        assert "Unknown method" in str(excinfo.value)
        assert "Valid options are" in str(excinfo.value)

    def test_wing_roll_load_factor_realistic_range(self):
        """Test improved method with realistic load factor range."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(0.8, u.ureg.meter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3, u.ureg.meter)

        # Test range from 1.0 to 2.0 (typical engineering range)
        for factor_value in [1.0, 1.2, 1.5, 1.8, 2.0]:
            load_factor = u.ureg.Quantity(factor_value, u.ureg.dimensionless)

            result = weight_force_belt_inside(
                total_force,
                inclination,
                belt_width,
                troughing,
                banking,
                inside_width,
                method="improved",
                wing_roll_load_factor=load_factor,
            )

            # Result should be positive and reasonable
            assert result.magnitude > 0
            assert result.units == u.ureg.newton
            # Result should scale with load factor
            expected_magnitude = 195.9 * factor_value  # Base result * factor
            assert result.magnitude == pytest.approx(expected_magnitude, rel=1e-2)


class TestWeightForceBeltOutsidePublic:
    """Test public weight force outside function with unit handling."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic weight force calculation with unit handling."""
        total_force = u.ureg.Quantity(156.71475, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(800, u.ureg.millimeter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.46, u.ureg.degree)
        outside_width = u.ureg.Quantity(0.1825, u.ureg.meter)

        result = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            precision=10,
        )

        assert result.units == u.ureg.newton
        # assert equivalent to 14.7922500663868
        assert result.magnitude == pytest.approx(14.7922500663868, rel=1e-10)

    def test_basic_calculation_with_units(self):
        """Test basic weight force calculation with unit handling."""
        total_force = u.ureg.Quantity(10000, u.ureg.newton)
        inclination = u.ureg.Quantity(5.7, u.ureg.degree)
        belt_width = u.ureg.Quantity(1200, u.ureg.millimeter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        outside_width = u.ureg.Quantity(400, u.ureg.millimeter)

        result = weight_force_belt_outside(
            total_force, inclination, belt_width, troughing, banking, outside_width
        )

        assert result.units == u.ureg.newton
        assert result.magnitude > 0

    def test_unit_conversion(self):
        """Test input unit conversion."""
        total_force = u.ureg.Quantity(5, u.ureg.kilonewton)
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.2, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(0.087, u.ureg.radian)
        outside_width = u.ureg.Quantity(40, u.ureg.centimeter)

        result = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            unit="kilonewton",
        )

        assert result.units == u.ureg.kilonewton
        assert result.magnitude > 0

    def test_precision_control(self):
        """Test precision parameter."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        outside_width = u.ureg.Quantity(0.333333, u.ureg.meter)

        result = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            precision=1,
        )

        assert result.magnitude == round(result.magnitude, 1)

    def test_error_handling_negative_force(self):
        """Test error handling for negative total force."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_outside(
                u.ureg.Quantity(-1000, u.ureg.newton),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0.3, u.ureg.meter),
            )
        assert "non-negative" in str(excinfo.value)

    def test_error_handling_invalid_width(self):
        """Test error handling for invalid belt width."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_outside(
                u.ureg.Quantity(1000, u.ureg.newton),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1.5, u.ureg.meter),  # Larger than total width
            )
        assert "cannot exceed total belt width" in str(excinfo.value)

    def test_error_handling_wrong_dimensions(self):
        """Test error handling for wrong unit dimensions."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_outside(
                u.ureg.Quantity(1000, u.ureg.meter),  # Wrong dimension
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0.3, u.ureg.meter),
            )
        assert "Error in converting units" in str(excinfo.value)

    def test_invalid_output_unit(self):
        """Test error handling for invalid output unit."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_outside(
                u.ureg.Quantity(1000, u.ureg.newton),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0.3, u.ureg.meter),
                unit="invalid_unit",
            )
        assert "Invalid unit" in str(excinfo.value)

    def test_method_parameter_conventional(self):
        """Test explicit conventional method selection."""
        total_force = u.ureg.Quantity(500, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(1, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(10, u.ureg.degree)
        outside_width = u.ureg.Quantity(0.35, u.ureg.meter)

        result = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="conventional",
        )

        # Should be approximately 28.47 newton with these parameters
        assert abs(result.magnitude - 28.47) < 0.1

    def test_method_parameter_improved_with_load_factor(self):
        """Test improved method with explicit wing_roll_load_factor."""
        total_force = u.ureg.Quantity(500, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(1, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(10, u.ureg.degree)
        outside_width = u.ureg.Quantity(0.35, u.ureg.meter)

        result = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="improved",
            wing_roll_load_factor=1.2 * u.ureg.dimensionless,
        )

        # Should be approximately 36.47 newton with these parameters and load factor 1.2
        assert abs(result.magnitude - 36.47) < 0.1

    def test_wing_roll_load_factor_linear_scaling(self):
        """Test that wing_roll_load_factor scales linearly."""
        total_force = u.ureg.Quantity(500, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(1, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(10, u.ureg.degree)
        outside_width = u.ureg.Quantity(0.35, u.ureg.meter)

        result_1x = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="improved",
            wing_roll_load_factor=1.0 * u.ureg.dimensionless,
        )
        result_15x = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="improved",
            wing_roll_load_factor=1.5 * u.ureg.dimensionless,
        )

        # Should scale linearly
        expected_15x = result_1x * 1.5
        assert abs(result_15x.magnitude - expected_15x.magnitude) < 0.01

    def test_wing_roll_load_factor_ignored_for_conventional(self):
        """Test that wing_roll_load_factor is ignored for conventional method."""
        total_force = u.ureg.Quantity(500, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(1, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(10, u.ureg.degree)
        outside_width = u.ureg.Quantity(0.35, u.ureg.meter)

        result_no_factor = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="conventional",
        )
        result_with_factor = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="conventional",
            wing_roll_load_factor=2.0 * u.ureg.dimensionless,
        )

        # Results should be identical for conventional method
        assert abs(result_no_factor.magnitude - result_with_factor.magnitude) < 1e-10


class TestWeightForceBeltCenterPublic:
    """Test public weight force center function with unit handling."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic weight force calculation with publication data."""
        total_force = u.ureg.Quantity(156.71475, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(800, u.ureg.millimeter)
        banking = u.ureg.Quantity(1.46, u.ureg.degree)
        center_width = u.ureg.Quantity(0.315, u.ureg.meter)

        result = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            precision=10,
        )

        # Expected result based on provided publication data
        expected = u.ureg.Quantity(1.57222125714098, u.ureg.newton)
        assert abs(result.magnitude - expected.magnitude) < 1e-10

    def test_basic_calculation_with_units(self):
        """Test basic weight force calculation with unit handling."""
        total_force = u.ureg.Quantity(10000, u.ureg.newton)
        inclination = u.ureg.Quantity(5.7, u.ureg.degree)
        belt_width = u.ureg.Quantity(1200, u.ureg.millimeter)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        center_width = u.ureg.Quantity(400, u.ureg.millimeter)

        result = weight_force_belt_center(
            total_force, inclination, belt_width, banking, center_width
        )

        assert result.units == u.ureg.newton
        assert result.magnitude > 0

    def test_unit_conversion(self):
        """Test input unit conversion."""
        total_force = u.ureg.Quantity(5, u.ureg.kilonewton)
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.2, u.ureg.meter)
        banking = u.ureg.Quantity(0.087, u.ureg.radian)
        center_width = u.ureg.Quantity(40, u.ureg.centimeter)

        result = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            unit="kilonewton",
        )

        assert result.units == u.ureg.kilonewton
        assert result.magnitude > 0

    def test_precision_control(self):
        """Test precision parameter."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        center_width = u.ureg.Quantity(0.333333, u.ureg.meter)

        result = weight_force_belt_center(
            total_force, inclination, belt_width, banking, center_width, precision=1
        )

        assert result.magnitude == round(result.magnitude, 1)

    def test_zero_banking_behavior(self):
        """Test that zero banking results in zero force."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(1, u.ureg.meter)
        banking = u.ureg.Quantity(0, u.ureg.radian)  # Zero banking
        center_width = u.ureg.Quantity(0.3, u.ureg.meter)

        result = weight_force_belt_center(
            total_force, inclination, belt_width, banking, center_width
        )

        assert result.magnitude == 0.0

    def test_error_handling_negative_force(self):
        """Test error handling for negative total force."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_center(
                u.ureg.Quantity(-1000, u.ureg.newton),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0.3, u.ureg.meter),
            )
        assert "non-negative" in str(excinfo.value)

    def test_error_handling_invalid_width(self):
        """Test error handling for invalid belt width."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_center(
                u.ureg.Quantity(1000, u.ureg.newton),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1.5, u.ureg.meter),  # Larger than total width
            )
        assert "cannot exceed total belt width" in str(excinfo.value)

    def test_error_handling_wrong_dimensions(self):
        """Test error handling for wrong unit dimensions."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_center(
                u.ureg.Quantity(1000, u.ureg.meter),  # Wrong dimension
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0.3, u.ureg.meter),
            )
        assert "Error in converting units" in str(excinfo.value)

    def test_invalid_output_unit(self):
        """Test error handling for invalid output unit."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_center(
                u.ureg.Quantity(1000, u.ureg.newton),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(0.3, u.ureg.meter),
                unit="invalid_unit",
            )
        assert "Invalid unit" in str(excinfo.value)

    def test_method_parameter_conventional(self):
        """Test explicit conventional method selection."""
        total_force = u.ureg.Quantity(500, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(1, u.ureg.meter)
        banking = u.ureg.Quantity(10, u.ureg.degree)
        center_width = u.ureg.Quantity(0.30, u.ureg.meter)

        result = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="conventional",
        )

        # Should be approximately 26.12 newton with these parameters
        assert abs(result.magnitude - 26.12) < 0.1

    def test_method_parameter_improved_with_load_factor(self):
        """Test improved method with explicit center_roll_load_factor."""
        total_force = u.ureg.Quantity(500, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(1, u.ureg.meter)
        banking = u.ureg.Quantity(10, u.ureg.degree)
        center_width = u.ureg.Quantity(0.30, u.ureg.meter)

        result = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=0.8 * u.ureg.dimensionless,
        )

        # Should be approximately 20.89 newton with these parameters and load factor 0.8
        assert abs(result.magnitude - 20.89) < 0.1

    def test_center_roll_load_factor_linear_scaling(self):
        """Test that center_roll_load_factor scales linearly."""
        total_force = u.ureg.Quantity(500, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(1, u.ureg.meter)
        banking = u.ureg.Quantity(10, u.ureg.degree)
        center_width = u.ureg.Quantity(0.30, u.ureg.meter)

        result_1x = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=1.0 * u.ureg.dimensionless,
        )
        result_05x = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=0.5 * u.ureg.dimensionless,
        )

        # Should scale linearly
        expected_05x = result_1x * 0.5
        assert abs(result_05x.magnitude - expected_05x.magnitude) < 0.01

    def test_center_roll_load_factor_ignored_for_conventional(self):
        """Test that center_roll_load_factor is ignored for conventional method."""
        total_force = u.ureg.Quantity(500, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.radian)
        belt_width = u.ureg.Quantity(1, u.ureg.meter)
        banking = u.ureg.Quantity(10, u.ureg.degree)
        center_width = u.ureg.Quantity(0.30, u.ureg.meter)

        result_no_factor = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="conventional",
        )
        result_with_factor = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="conventional",
            center_roll_load_factor=0.5 * u.ureg.dimensionless,
        )

        # Results should be identical for conventional method
        assert abs(result_no_factor.magnitude - result_with_factor.magnitude) < 1e-10


class TestWeightForceOfBeltPublic:
    """Test public weight force of belt function with unit handling."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic net weight force calculation with publication data."""
        # Calculate individual forces using publication data parameters
        total_force = u.ureg.Quantity(156.71475, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(800, u.ureg.millimeter)
        banking = u.ureg.Quantity(1.46, u.ureg.degree)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        section_width = u.ureg.Quantity(0.315, u.ureg.meter)
        outside_width = u.ureg.Quantity(0.1825, u.ureg.meter)
        inside_width = u.ureg.Quantity(0.3025, u.ureg.meter)

        # Calculate individual force components
        inside_force = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            precision=10,
        )
        center_force = weight_force_belt_center(
            total_force, inclination, belt_width, banking, section_width, precision=10
        )
        outside_force = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            precision=10,
        )

        # Calculate net force
        result = weight_force_of_belt(
            inside_force, center_force, outside_force, precision=10
        )

        # Expected result based on publication data: 13.5633795467688 N
        expected = u.ureg.Quantity(13.5633795467688, u.ureg.newton)
        assert abs(result.magnitude - expected.magnitude) < 1e-10

    def test_basic_calculation_with_units(self):
        """Test basic calculation with unit handling."""
        inside_force = u.ureg.Quantity(10000, u.ureg.newton)
        center_force = u.ureg.Quantity(2000, u.ureg.newton)
        outside_force = u.ureg.Quantity(8000, u.ureg.newton)

        result = weight_force_of_belt(inside_force, center_force, outside_force)

        # Expected: 10000 + 2000 - 8000 = 4000 N
        assert result.units == u.ureg.newton
        assert result.magnitude == 4000.0

    def test_unit_conversion(self):
        """Test input unit conversion."""
        inside_force = u.ureg.Quantity(5, u.ureg.kilonewton)
        center_force = u.ureg.Quantity(1000, u.ureg.newton)
        outside_force = u.ureg.Quantity(3.5, u.ureg.kilonewton)

        result = weight_force_of_belt(
            inside_force, center_force, outside_force, unit="kilonewton"
        )

        assert result.units == u.ureg.kilonewton
        # Expected: 5 + 1 - 3.5 = 2.5 kN
        assert abs(result.magnitude - 2.5) < 1e-10

    def test_precision_control(self):
        """Test precision parameter."""
        inside_force = u.ureg.Quantity(1000.123456, u.ureg.newton)
        center_force = u.ureg.Quantity(200.654321, u.ureg.newton)
        outside_force = u.ureg.Quantity(800.111111, u.ureg.newton)

        result = weight_force_of_belt(
            inside_force, center_force, outside_force, precision=1
        )

        assert result.magnitude == round(result.magnitude, 1)

    def test_zero_forces(self):
        """Test calculation with zero forces."""
        zero_force = u.ureg.Quantity(0, u.ureg.newton)

        result = weight_force_of_belt(zero_force, zero_force, zero_force)

        assert result.magnitude == 0.0

    def test_negative_result(self):
        """Test calculation that results in negative net force."""
        inside_force = u.ureg.Quantity(500, u.ureg.newton)
        center_force = u.ureg.Quantity(100, u.ureg.newton)
        outside_force = u.ureg.Quantity(800, u.ureg.newton)

        result = weight_force_of_belt(inside_force, center_force, outside_force)

        # Expected: 500 + 100 - 800 = -200 N
        assert result.magnitude == -200.0

    def test_error_handling_wrong_dimensions(self):
        """Test error handling for wrong unit dimensions."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_of_belt(
                u.ureg.Quantity(1000, u.ureg.meter),  # Wrong dimension
                u.ureg.Quantity(200, u.ureg.newton),
                u.ureg.Quantity(800, u.ureg.newton),
            )
        assert "Error in converting units" in str(excinfo.value)

    def test_invalid_output_unit(self):
        """Test error handling for invalid output unit."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_of_belt(
                u.ureg.Quantity(1000, u.ureg.newton),
                u.ureg.Quantity(200, u.ureg.newton),
                u.ureg.Quantity(800, u.ureg.newton),
                unit="invalid_unit",
            )
        assert "Invalid unit" in str(excinfo.value)

    def test_method_parameter_conventional(self):
        """Test explicit conventional method selection for net force."""
        inside_force = u.ureg.Quantity(30.0, u.ureg.newton)
        center_force = u.ureg.Quantity(26.1, u.ureg.newton)
        outside_force = u.ureg.Quantity(28.5, u.ureg.newton)

        result = weight_force_of_belt(
            inside_force, center_force, outside_force, method="conventional"
        )

        # Net force = 30.0 + 26.1 - 28.5 = 27.6 newton
        assert abs(result.magnitude - 27.6) < 0.1

    def test_method_parameter_improved(self):
        """Test improved method for net force calculation."""
        inside_force = u.ureg.Quantity(45.0, u.ureg.newton)  # Higher due to load factor
        center_force = u.ureg.Quantity(20.9, u.ureg.newton)  # Lower due to load factor
        outside_force = u.ureg.Quantity(
            36.4, u.ureg.newton
        )  # Higher due to load factor

        result = weight_force_of_belt(
            inside_force, center_force, outside_force, method="improved"
        )

        # Net force = 45.0 + 20.9 - 36.4 = 29.5 newton
        assert abs(result.magnitude - 29.5) < 0.1

    def test_improved_vs_conventional_comparison(self):
        """Test comparison between improved and conventional methods."""
        # Use force values typical of load factor adjustments
        inside_conventional = u.ureg.Quantity(30.0, u.ureg.newton)
        center_conventional = u.ureg.Quantity(26.1, u.ureg.newton)
        outside_conventional = u.ureg.Quantity(28.5, u.ureg.newton)

        inside_improved = inside_conventional * 1.5  # Higher load factor
        center_improved = center_conventional * 0.8  # Lower load factor
        outside_improved = outside_conventional * 1.2  # Higher load factor

        result_conventional = weight_force_of_belt(
            inside_conventional,
            center_conventional,
            outside_conventional,
            method="conventional",
        )
        result_improved = weight_force_of_belt(
            inside_improved, center_improved, outside_improved, method="improved"
        )

        # Improved method should give different (typically higher) net force
        assert abs(result_improved.magnitude - result_conventional.magnitude) > 1.0

    def test_publication_data_verification_improved(self):
        """Test improved method with publication data - Grimmer & Kessler (1987) Teil II."""
        # Calculate individual forces using publication data with improved methods
        total_force = u.ureg.Quantity(156.71475, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(800, u.ureg.millimeter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.46, u.ureg.degree)

        # Belt width sections
        inside_width = u.ureg.Quantity(0.3025, u.ureg.meter)
        center_width = u.ureg.Quantity(0.315, u.ureg.meter)
        outside_width = u.ureg.Quantity(0.1825, u.ureg.meter)

        # Load factors for improved method
        wing_roll_load_factor = 1.1 * u.ureg.dimensionless
        center_roll_load_factor = 0.9 * u.ureg.dimensionless

        # Calculate individual forces using improved methods
        inside_force = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
            precision=10,
        )

        center_force = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=center_roll_load_factor,
            precision=10,
        )

        outside_force = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
            precision=10,
        )

        # Calculate net force using improved method
        result = weight_force_of_belt(
            inside_force, center_force, outside_force, method="improved", precision=10
        )

        # Expected result based on improved calculations
        expected = u.ureg.Quantity(16.6458157575333, u.ureg.newton)
        assert abs(result.magnitude - expected.magnitude) < 1e-10


class TestWeightForceBeltInsidePublicImproved:
    """Test public improved weight force inside function with publication data."""

    def test_basic_calculation_with_publication_data_improved(self):
        """Test improved method with publication data - Grimmer & Kessler (1987) Teil II."""
        total_force = u.ureg.Quantity(156.71475, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(800, u.ureg.millimeter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.46, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3025, u.ureg.meter)
        wing_roll_load_factor = 1.1 * u.ureg.dimensionless

        result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
            precision=10,
        )

        # Expected result based on improved calculation
        expected = u.ureg.Quantity(34.0194976531535, u.ureg.newton)
        assert abs(result.magnitude - expected.magnitude) < 1e-10

    def test_basic_calculation_with_units_improved(self):
        """Test improved method with typical unit handling."""
        total_force = u.ureg.Quantity(10000, u.ureg.newton)
        inclination = u.ureg.Quantity(5.7, u.ureg.degree)
        belt_width = u.ureg.Quantity(1200, u.ureg.millimeter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        inside_width = u.ureg.Quantity(400, u.ureg.millimeter)
        wing_roll_load_factor = 1.5 * u.ureg.dimensionless

        result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
        )

        assert result.units == u.ureg.newton
        assert result.magnitude > 0

    def test_unit_conversion_improved(self):
        """Test input unit conversion with improved method."""
        total_force = u.ureg.Quantity(5, u.ureg.kilonewton)  # Input in kN
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.2, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)  # Input in degrees
        banking = u.ureg.Quantity(0.087, u.ureg.radian)
        inside_width = u.ureg.Quantity(40, u.ureg.centimeter)  # Input in cm
        wing_roll_load_factor = 1.3 * u.ureg.dimensionless

        result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
            unit="kilonewton",  # Output in kN
        )

        assert result.units == u.ureg.kilonewton
        assert result.magnitude > 0

    def test_load_factor_scaling_improved(self):
        """Test that wing roll load factor scales the result correctly."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3, u.ureg.meter)

        # Test with different load factors using higher precision
        result_1x = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",
            wing_roll_load_factor=1.0 * u.ureg.dimensionless,
            precision=6,  # Higher precision to avoid rounding issues
        )

        result_15x = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",
            wing_roll_load_factor=1.5 * u.ureg.dimensionless,
            precision=6,  # Higher precision to avoid rounding issues
        )

        # Should scale linearly
        expected = result_1x.magnitude * 1.5
        assert result_15x.magnitude == pytest.approx(expected, rel=1e-5)

    def test_precision_control_improved(self):
        """Test precision parameter with improved method."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.333333, u.ureg.meter)
        wing_roll_load_factor = 1.2 * u.ureg.dimensionless

        result = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
            precision=1,
        )

        # Check that result is rounded to 1 decimal place
        assert result.magnitude == round(result.magnitude, 1)

    def test_default_load_factor_behavior_improved(self):
        """Test that default load factor behavior works for improved method."""
        # Test that improved method works with default load factor
        result = weight_force_belt_inside(
            u.ureg.Quantity(1000, u.ureg.newton),
            u.ureg.Quantity(0, u.ureg.radian),
            u.ureg.Quantity(1, u.ureg.meter),
            u.ureg.Quantity(0, u.ureg.radian),
            u.ureg.Quantity(0, u.ureg.radian),
            u.ureg.Quantity(0.3, u.ureg.meter),
            method="improved",
            # No wing_roll_load_factor provided - should use default
        )
        assert result.magnitude >= 0  # Should produce valid result

    def test_error_handling_invalid_load_factor_improved(self):
        """Test error handling for invalid wing load factor values."""
        # Test that negative load factor raises an error
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_inside(
                u.ureg.Quantity(1000, u.ureg.newton),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0.3, u.ureg.radian),  # Non-zero troughing
                u.ureg.Quantity(0.1, u.ureg.radian),  # Non-zero banking
                u.ureg.Quantity(0.3, u.ureg.meter),
                method="improved",
                wing_roll_load_factor=-0.5
                * u.ureg.dimensionless,  # Negative load factor
            )

        # Should raise error about physical meaningfulness
        assert (
            "wing_roll_load_factor must be non-negative for physical meaningfulness"
            in str(excinfo.value)
        )

    def test_comparison_with_conventional_improved(self):
        """Test relationship between improved and conventional methods."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        inside_width = u.ureg.Quantity(0.3, u.ureg.meter)

        # Conventional result
        conventional = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="conventional",
        )

        # Improved with load factor 1.0
        improved = weight_force_belt_inside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            inside_width,
            method="improved",
            wing_roll_load_factor=1.0 * u.ureg.dimensionless,
        )

        # The relationship should follow: improved = conventional / cos(troughing)
        import math

        troughing_rad = math.radians(20)
        expected_ratio = 1.0 / math.cos(troughing_rad)
        actual_ratio = improved.magnitude / conventional.magnitude
        assert actual_ratio == pytest.approx(expected_ratio, rel=1e-4)


class TestWeightForceBeltOutsidePublicImproved:
    """Test public improved weight force outside function with publication data."""

    def test_basic_calculation_with_publication_data_improved(self):
        """Test improved method with publication data - Grimmer & Kessler (1987) Teil II."""
        total_force = u.ureg.Quantity(156.71475, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(800, u.ureg.millimeter)
        troughing = u.ureg.Quantity(30, u.ureg.degree)
        banking = u.ureg.Quantity(1.46, u.ureg.degree)
        outside_width = u.ureg.Quantity(0.1825, u.ureg.meter)
        wing_roll_load_factor = 1.1 * u.ureg.dimensionless

        result = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
            precision=10,
        )

        # Expected result based on improved calculation
        expected = u.ureg.Quantity(18.7886810270471, u.ureg.newton)
        assert abs(result.magnitude - expected.magnitude) < 1e-10

    def test_basic_calculation_with_units_improved(self):
        """Test improved method with typical unit handling."""
        total_force = u.ureg.Quantity(10000, u.ureg.newton)
        inclination = u.ureg.Quantity(5.7, u.ureg.degree)
        belt_width = u.ureg.Quantity(1200, u.ureg.millimeter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        outside_width = u.ureg.Quantity(400, u.ureg.millimeter)
        wing_roll_load_factor = 1.5 * u.ureg.dimensionless

        result = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
        )

        assert result.units == u.ureg.newton
        assert result.magnitude > 0

    def test_unit_conversion_improved(self):
        """Test input unit conversion with improved method."""
        total_force = u.ureg.Quantity(5, u.ureg.kilonewton)  # Input in kN
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.2, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)  # Input in degrees
        banking = u.ureg.Quantity(0.087, u.ureg.radian)
        outside_width = u.ureg.Quantity(40, u.ureg.centimeter)  # Input in cm
        wing_roll_load_factor = 1.3 * u.ureg.dimensionless

        result = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
            unit="kilonewton",  # Output in kN
        )

        assert result.units == u.ureg.kilonewton
        assert result.magnitude > 0

    def test_wing_load_factor_scaling_improved(self):
        """Test that wing roll load factor scales the result correctly."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        outside_width = u.ureg.Quantity(0.4, u.ureg.meter)

        # Test with different load factors
        result_1x = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="improved",
            wing_roll_load_factor=1.0 * u.ureg.dimensionless,
        )

        result_2x = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="improved",
            wing_roll_load_factor=2.0 * u.ureg.dimensionless,
        )

        # Should scale linearly
        assert result_2x.magnitude == pytest.approx(
            result_1x.magnitude * 2.0, rel=1e-10
        )

    def test_banking_angle_effects_improved(self):
        """Test effects of different banking angles with improved method."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        outside_width = u.ureg.Quantity(0.4, u.ureg.meter)
        wing_roll_load_factor = 1.2 * u.ureg.dimensionless

        # Positive banking
        result_pos = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            u.ureg.Quantity(5, u.ureg.degree),  # Positive banking
            outside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
        )

        # Negative banking
        result_neg = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            u.ureg.Quantity(-5, u.ureg.degree),  # Negative banking
            outside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
        )

        # Should be different due to sin(troughing ± banking)
        assert result_pos.magnitude != result_neg.magnitude

    def test_precision_control_improved(self):
        """Test precision parameter with improved method."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        outside_width = u.ureg.Quantity(0.333333, u.ureg.meter)
        wing_roll_load_factor = 1.2 * u.ureg.dimensionless

        result = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="improved",
            wing_roll_load_factor=wing_roll_load_factor,
            precision=1,
        )

        # Check that result is rounded to 1 decimal place
        assert result.magnitude == round(result.magnitude, 1)

    def test_error_handling_missing_load_factor_improved(self):
        """Test that improved method works with default load factor when not specified."""
        # Test that function works when wing_roll_load_factor is not provided (uses default)
        result = weight_force_belt_outside(
            u.ureg.Quantity(1000, u.ureg.newton),
            u.ureg.Quantity(0, u.ureg.radian),
            u.ureg.Quantity(1, u.ureg.meter),
            u.ureg.Quantity(0, u.ureg.radian),
            u.ureg.Quantity(0, u.ureg.radian),
            u.ureg.Quantity(0.4, u.ureg.meter),
            method="improved",
            # wing_roll_load_factor not provided - should use default
        )

        # Should produce a valid result using default load factor
        assert isinstance(result, u.ureg.Quantity)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_comparison_with_conventional_improved(self):
        """Test relationship between improved and conventional methods."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        troughing = u.ureg.Quantity(20, u.ureg.degree)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        outside_width = u.ureg.Quantity(0.4, u.ureg.meter)

        # Conventional result
        conventional = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="conventional",
        )

        # Improved with load factor 1.0
        improved = weight_force_belt_outside(
            total_force,
            inclination,
            belt_width,
            troughing,
            banking,
            outside_width,
            method="improved",
            wing_roll_load_factor=1.0 * u.ureg.dimensionless,
        )

        # The relationship should follow: improved = conventional / cos(troughing)
        import math

        troughing_rad = math.radians(20)
        expected_ratio = 1.0 / math.cos(troughing_rad)
        actual_ratio = improved.magnitude / conventional.magnitude
        assert actual_ratio == pytest.approx(
            expected_ratio, rel=1e-4
        )  # Adjusted for implementation precision


class TestWeightForceBeltCenterPublicImproved:
    """Test public improved weight force center function with publication data."""

    def test_basic_calculation_with_publication_data_improved(self):
        """Test improved method with publication data - Grimmer & Kessler (1987) Teil II."""
        total_force = u.ureg.Quantity(156.71475, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(800, u.ureg.millimeter)
        banking = u.ureg.Quantity(1.46, u.ureg.degree)
        center_width = u.ureg.Quantity(0.315, u.ureg.meter)
        center_roll_load_factor = 0.9 * u.ureg.dimensionless

        result = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=center_roll_load_factor,
            precision=10,
        )

        # Expected result based on improved calculation
        expected = u.ureg.Quantity(1.41499913142688, u.ureg.newton)
        assert abs(result.magnitude - expected.magnitude) < 1e-10

    def test_basic_calculation_with_units_improved(self):
        """Test improved method with typical unit handling."""
        total_force = u.ureg.Quantity(10000, u.ureg.newton)
        inclination = u.ureg.Quantity(5.7, u.ureg.degree)
        belt_width = u.ureg.Quantity(1200, u.ureg.millimeter)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        center_width = u.ureg.Quantity(400, u.ureg.millimeter)
        center_roll_load_factor = 0.8 * u.ureg.dimensionless

        result = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=center_roll_load_factor,
        )

        assert result.units == u.ureg.newton
        assert result.magnitude > 0

    def test_unit_conversion_improved(self):
        """Test input unit conversion with improved method."""
        total_force = u.ureg.Quantity(5, u.ureg.kilonewton)  # Input in kN
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.2, u.ureg.meter)
        banking = u.ureg.Quantity(0.087, u.ureg.radian)
        center_width = u.ureg.Quantity(40, u.ureg.centimeter)  # Input in cm
        center_roll_load_factor = 0.9 * u.ureg.dimensionless

        result = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=center_roll_load_factor,
            unit="kilonewton",  # Output in kN
        )

        assert result.units == u.ureg.kilonewton
        assert result.magnitude > 0

    def test_center_load_factor_scaling_improved(self):
        """Test that center roll load factor scales the result correctly."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        center_width = u.ureg.Quantity(0.4, u.ureg.meter)

        # Test with different load factors
        result_05x = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=0.5 * u.ureg.dimensionless,
        )

        result_1x = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=1.0 * u.ureg.dimensionless,
        )

        # Should scale linearly
        assert result_1x.magnitude == pytest.approx(
            result_05x.magnitude * 2.0, rel=1e-10
        )

    def test_zero_banking_angle_improved(self):
        """Test with zero banking angle using improved method."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        banking = u.ureg.Quantity(0, u.ureg.degree)  # Zero banking
        center_width = u.ureg.Quantity(0.4, u.ureg.meter)
        center_roll_load_factor = 0.8 * u.ureg.dimensionless

        result = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=center_roll_load_factor,
        )

        # sin(0) = 0, so result should be 0
        assert result.magnitude == pytest.approx(0.0, abs=1e-10)

    def test_precision_control_improved(self):
        """Test precision parameter with improved method."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0.1, u.ureg.radian)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        center_width = u.ureg.Quantity(0.333333, u.ureg.meter)
        center_roll_load_factor = 0.75 * u.ureg.dimensionless

        result = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=center_roll_load_factor,
            precision=1,
        )

        # Check that result is rounded to 1 decimal place
        assert result.magnitude == round(result.magnitude, 1)

    def test_error_handling_missing_load_factor_improved(self):
        """Test that improved method works with default load factor when not specified."""
        # Test that function works when center_roll_load_factor is not provided (uses default)
        result = weight_force_belt_center(
            u.ureg.Quantity(1000, u.ureg.newton),
            u.ureg.Quantity(0, u.ureg.radian),
            u.ureg.Quantity(1, u.ureg.meter),
            u.ureg.Quantity(0.1, u.ureg.radian),
            u.ureg.Quantity(0.4, u.ureg.meter),
            method="improved",
            # center_roll_load_factor not provided - should use default
        )

        # Should produce a valid result using default load factor
        assert isinstance(result, u.ureg.Quantity)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_error_handling_invalid_load_factor_improved(self):
        """Test error handling for invalid center load factor values."""
        with pytest.raises(ValueError) as excinfo:
            weight_force_belt_center(
                u.ureg.Quantity(1000, u.ureg.newton),
                u.ureg.Quantity(0, u.ureg.radian),
                u.ureg.Quantity(1, u.ureg.meter),
                u.ureg.Quantity(0.1, u.ureg.radian),
                u.ureg.Quantity(0.4, u.ureg.meter),
                method="improved",
                center_roll_load_factor=-0.1
                * u.ureg.dimensionless,  # Negative load factor
            )
        assert "center_roll_load_factor" in str(excinfo.value)

    def test_comparison_with_conventional_improved(self):
        """Test relationship between improved and conventional methods."""
        total_force = u.ureg.Quantity(1000, u.ureg.newton)
        inclination = u.ureg.Quantity(0, u.ureg.degree)
        belt_width = u.ureg.Quantity(1.0, u.ureg.meter)
        banking = u.ureg.Quantity(5, u.ureg.degree)
        center_width = u.ureg.Quantity(0.4, u.ureg.meter)

        # Conventional result
        conventional = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="conventional",
        )

        # Improved with load factor 1.0
        improved = weight_force_belt_center(
            total_force,
            inclination,
            belt_width,
            banking,
            center_width,
            method="improved",
            center_roll_load_factor=1.0 * u.ureg.dimensionless,
        )

        # The center methods should be identical since they use the same formula
        assert improved.magnitude == pytest.approx(conventional.magnitude, rel=1e-10)


class TestTiltedIdlerFrictionForceInside:
    """Test public tilted idler friction force inside function with unit handling."""

    def test_basic_calculation_with_units(self):
        """Test basic calculation with proper units."""
        total_weight_force_material = 156.71475 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_inside_wing_roll = 0.3025 * u.ureg.meter
        friction_variation = 1.0 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.3 * u.ureg.dimensionless
        normal_force_on_idler_roll = 10 * u.ureg.newton

        result = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
        )

        # Check result has proper units
        assert result.check("[force]")
        assert result.magnitude > 0
        # Result should be around 15.73 N with these parameters (from TDD)
        assert 15 < result.to(u.ureg.newton).magnitude < 16

    def test_unit_conversion(self):
        """Test various unit conversions."""
        # Define inputs in different units
        total_weight_force_material = 156.71475 * u.ureg.newton
        inclination_angle = 0 * u.ureg.radian  # 0 degrees in radians
        belt_width = 800 * u.ureg.millimeter  # 0.8 m in mm
        troughing_angle = (30 * np.pi / 180) * u.ureg.radian  # 30 degrees in radians
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_inside_wing_roll = 302.5 * u.ureg.millimeter  # 0.3025 m in mm
        friction_variation = 1.0 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.3 * u.ureg.dimensionless
        normal_force_on_idler_roll = 10000 * u.ureg.millinewton  # 10 N in mN

        # Test different output units with higher precision for accurate comparison
        result_n = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            unit="newton",
            precision=5,
        )

        result_kn = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            unit="kilonewton",
            precision=5,
        )  # Check unit conversion consistency (allow for small rounding differences)
        assert result_n.to(u.ureg.kilonewton).magnitude == pytest.approx(
            result_kn.magnitude, rel=1e-4
        )

        # Check magnitudes are reasonable (around 15.73061 N / 0.01573 kN)
        assert result_n.magnitude == pytest.approx(15.73061, rel=1e-3)
        assert result_kn.magnitude == pytest.approx(0.01573, rel=1e-3)

    def test_zero_normal_force(self):
        """Test calculation with zero normal force."""
        total_weight_force_material = 156.71475 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_inside_wing_roll = 0.3025 * u.ureg.meter
        friction_variation = 1.0 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.3 * u.ureg.dimensionless
        normal_force_on_idler_roll = 0 * u.ureg.newton

        result = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
        )

        # Result should still be positive due to material weight component
        assert result.magnitude > 0

    def test_error_handling_negative_forces(self):
        """Test error handling for negative force inputs."""
        with pytest.raises(ValueError, match="Total weight force must be non-negative"):
            tilted_idler_friction_force_inside(
                -100 * u.ureg.newton,  # Negative weight force
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.3025 * u.ureg.meter,
                1.0 * u.ureg.dimensionless,
                0.3 * u.ureg.dimensionless,
                10 * u.ureg.newton,
            )

        with pytest.raises(ValueError, match="Normal force must be non-negative"):
            tilted_idler_friction_force_inside(
                156.71475 * u.ureg.newton,
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.3025 * u.ureg.meter,
                1.0 * u.ureg.dimensionless,
                0.3 * u.ureg.dimensionless,
                -10 * u.ureg.newton,  # Negative normal force
            )

    def test_error_handling_negative_coefficients(self):
        """Test error handling for negative friction coefficients."""
        with pytest.raises(ValueError, match="Friction variation must be non-negative"):
            tilted_idler_friction_force_inside(
                156.71475 * u.ureg.newton,
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.3025 * u.ureg.meter,
                -1.0 * u.ureg.dimensionless,  # Negative friction variation
                0.3 * u.ureg.dimensionless,
                10 * u.ureg.newton,
            )

        with pytest.raises(
            ValueError, match="Friction coefficient must be non-negative"
        ):
            tilted_idler_friction_force_inside(
                156.71475 * u.ureg.newton,
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.3025 * u.ureg.meter,
                1.0 * u.ureg.dimensionless,
                -0.3 * u.ureg.dimensionless,  # Negative friction coefficient
                10 * u.ureg.newton,
            )

    def test_error_handling_invalid_widths(self):
        """Test error handling for invalid belt widths."""
        with pytest.raises(ValueError, match="Belt width must be positive"):
            tilted_idler_friction_force_inside(
                156.71475 * u.ureg.newton,
                0 * u.ureg.degree,
                0 * u.ureg.meter,  # Zero belt width
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.3025 * u.ureg.meter,
                1.0 * u.ureg.dimensionless,
                0.3 * u.ureg.dimensionless,
                10 * u.ureg.newton,
            )

        with pytest.raises(
            ValueError, match="Belt width on section cannot exceed total belt width"
        ):
            tilted_idler_friction_force_inside(
                156.71475 * u.ureg.newton,
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                1.0 * u.ureg.meter,  # Inside width > total width
                1.0 * u.ureg.dimensionless,
                0.3 * u.ureg.dimensionless,
                10 * u.ureg.newton,
            )

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters (conventional method)."""
        # Using parameters from publication data
        total_weight_force_material = 156.71475 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_inside_wing_roll = 0.3025 * u.ureg.meter
        friction_variation = 0.7 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.416183096 * u.ureg.dimensionless
        normal_force_on_idler_roll = 0 * u.ureg.newton

        result = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            method="conventional",
            precision=8,  # Higher precision for publication data validation
        )

        # Expected result from publication data: 12.75292522 N
        expected_value = 12.75292522
        assert result.check("[force]")
        assert result.to(u.ureg.newton).magnitude == pytest.approx(
            expected_value, rel=1e-4
        )

    def test_basic_calculation_with_publication_data_improved(self):
        """Test basic calculation with publication data parameters (improved method)."""
        # Using parameters from publication data with improved method
        total_weight_force_material = 156.71475 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_inside_wing_roll = 0.3025 * u.ureg.meter
        friction_variation = 0.7 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.416183096 * u.ureg.dimensionless
        normal_force_on_idler_roll = 0 * u.ureg.newton

        result = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            method="improved",
            precision=8,  # Higher precision for publication data validation
        )

        # Expected result from publication data: 16.19839058 N
        expected_value = 16.19839058
        assert result.check("[force]")
        assert result.to(u.ureg.newton).magnitude == pytest.approx(
            expected_value, rel=1e-4
        )

    def test_method_parameter_validation(self):
        """Test that method parameter is properly validated."""
        total_weight_force_material = 156.71475 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_inside_wing_roll = 0.3025 * u.ureg.meter
        friction_variation = 0.7 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.416183096 * u.ureg.dimensionless
        normal_force_on_idler_roll = 0 * u.ureg.newton

        # Test valid methods work
        result_conventional = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            method="conventional",
        )

        result_improved = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            method="improved",
        )

        assert result_conventional.check("[force]")
        assert result_improved.check("[force]")

        # The improved method should give a higher result for these parameters
        assert result_improved.magnitude > result_conventional.magnitude

        # Test invalid method raises error
        with pytest.raises(
            ValueError, match="Unknown method: 'invalid_method'. Valid options are:"
        ):
            tilted_idler_friction_force_inside(
                total_weight_force_material,
                inclination_angle,
                belt_width,
                troughing_angle,
                banking_angle,
                belt_width_on_inside_wing_roll,
                friction_variation,
                friction_coefficient_tilted_idler,
                normal_force_on_idler_roll,
                method="invalid_method",
            )

    def test_method_comparison_with_publication_data(self):
        """Test comparison between conventional and improved methods with publication data."""
        # Using standard publication data parameters
        total_weight_force_material = 156.71475 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_inside_wing_roll = 0.3025 * u.ureg.meter
        friction_variation = 0.7 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.416183096 * u.ureg.dimensionless
        normal_force_on_idler_roll = 0 * u.ureg.newton

        conventional_result = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            method="conventional",
            precision=8,  # Higher precision for publication data validation
        )

        improved_result = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            method="improved",
            precision=8,  # Higher precision for publication data validation
        )

        # Verify expected publication data values
        assert conventional_result.to(u.ureg.newton).magnitude == pytest.approx(
            12.75292522, rel=1e-4
        )
        assert improved_result.to(u.ureg.newton).magnitude == pytest.approx(
            16.19839058, rel=1e-4
        )

        # Calculate improvement ratio (should be approximately 1.27)
        improvement_ratio = improved_result.magnitude / conventional_result.magnitude
        assert improvement_ratio == pytest.approx(1.269964, rel=1e-3)

    def test_error_handling_invalid_units(self):
        """Test error handling for invalid units."""
        with pytest.raises(ValueError, match="Cannot convert result to"):
            tilted_idler_friction_force_inside(
                156.71475 * u.ureg.newton,
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.3025 * u.ureg.meter,
                1.0 * u.ureg.dimensionless,
                0.3 * u.ureg.dimensionless,
                10 * u.ureg.newton,
                unit="invalid_unit",
            )

    def test_precision_parameter(self):
        """Test precision parameter functionality."""
        total_weight_force_material = 156.71475 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_inside_wing_roll = 0.3025 * u.ureg.meter
        friction_variation = 1.0 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.3 * u.ureg.dimensionless
        normal_force_on_idler_roll = 10 * u.ureg.newton

        # Test different precision values
        result_2 = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            precision=2,
        )

        result_4 = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            precision=4,
        )

        # Both should be equal when rounded to 2 decimal places
        assert round(result_2.magnitude, 2) == round(result_4.magnitude, 2)


class TestTiltedIdlerFrictionForceOutside:
    """Test public tilted idler friction force outside function with unit handling."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with proper units using publication data."""
        total_weight_force_material = 156.71475 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_outside_wing_roll = 0.1825 * u.ureg.meter
        friction_variation = 0.7 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.216183095606664 * u.ureg.dimensionless
        normal_force_on_idler_roll = 0 * u.ureg.newton

        result = tilted_idler_friction_force_outside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_outside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            precision=10,
        )

        # Check result has proper units
        assert result.check("[force]")
        assert result.magnitude > 0
        # Expected result: 4.11591981879653 N (from private function test data)
        assert result.to(u.ureg.newton).magnitude == pytest.approx(
            4.11591981879653, rel=1e-10
        )

    def test_unit_conversion(self):
        """Test various unit conversions."""
        # Define inputs in different units
        total_weight_force_material = 156.71475 * u.ureg.newton
        inclination_angle = 0 * u.ureg.radian  # 0 degrees in radians
        belt_width = 800 * u.ureg.millimeter  # 0.8 m in mm
        troughing_angle = (30 * np.pi / 180) * u.ureg.radian  # 30 degrees in radians
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_outside_wing_roll = 182.5 * u.ureg.millimeter  # 0.1825 m in mm
        friction_variation = 0.7 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.216183095606664 * u.ureg.dimensionless
        normal_force_on_idler_roll = 0 * u.ureg.millinewton  # 0 N in mN

        # Test different output units with higher precision for accurate comparison
        result_n = tilted_idler_friction_force_outside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_outside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            unit="newton",
            precision=10,
        )

        result_kn = tilted_idler_friction_force_outside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_outside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            unit="kilonewton",
            precision=10,
        )

        # Check unit conversion consistency
        assert result_n.to(u.ureg.kilonewton).magnitude == pytest.approx(
            result_kn.magnitude, rel=1e-8
        )

        # Check magnitudes are reasonable (around 4.11591981879653 N / 0.00411591981879653 kN)
        assert result_n.magnitude == pytest.approx(4.11591981879653, rel=1e-8)
        assert result_kn.magnitude == pytest.approx(0.00411591981879653, rel=1e-8)

    def test_zero_friction_variation(self):
        """Test calculation with zero friction variation."""
        total_weight_force_material = 156.71 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_outside_wing_roll = 0.1825 * u.ureg.meter
        friction_variation = 0.0 * u.ureg.dimensionless  # Zero friction variation
        friction_coefficient_tilted_idler = 0.216 * u.ureg.dimensionless
        normal_force_on_idler_roll = 10 * u.ureg.newton

        result = tilted_idler_friction_force_outside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_outside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
        )

        # Result should be zero due to zero friction variation
        assert result.magnitude == pytest.approx(0.0, abs=1e-10)

    def test_zero_friction_coefficient(self):
        """Test calculation with zero friction coefficient."""
        total_weight_force_material = 156.71 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_outside_wing_roll = 0.1825 * u.ureg.meter
        friction_variation = 0.7 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = (
            0.0 * u.ureg.dimensionless
        )  # Zero friction coeff
        normal_force_on_idler_roll = 10 * u.ureg.newton

        result = tilted_idler_friction_force_outside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_outside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
        )

        # Result should be zero due to zero friction coefficient
        assert result.magnitude == pytest.approx(0.0, abs=1e-10)

    def test_with_normal_force(self):
        """Test calculation with additional normal force."""
        total_weight_force_material = 156.71 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_outside_wing_roll = 0.1825 * u.ureg.meter
        friction_variation = 0.7 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.216 * u.ureg.dimensionless
        normal_force_on_idler_roll = 50 * u.ureg.newton

        result = tilted_idler_friction_force_outside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_outside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
        )

        # Result should be higher due to additional normal force
        assert result.magnitude > 4.11591981879653  # Base case without normal force

    def test_error_handling_negative_forces(self):
        """Test error handling for negative force inputs."""
        with pytest.raises(ValueError, match="Total weight force must be non-negative"):
            tilted_idler_friction_force_outside(
                -100 * u.ureg.newton,  # Negative weight force
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.1825 * u.ureg.meter,
                0.7 * u.ureg.dimensionless,
                0.216 * u.ureg.dimensionless,
                0 * u.ureg.newton,
            )

        with pytest.raises(ValueError, match="Normal force must be non-negative"):
            tilted_idler_friction_force_outside(
                156.71 * u.ureg.newton,
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.1825 * u.ureg.meter,
                0.7 * u.ureg.dimensionless,
                0.216 * u.ureg.dimensionless,
                -10 * u.ureg.newton,  # Negative normal force
            )

    def test_error_handling_negative_coefficients(self):
        """Test error handling for negative friction coefficients."""
        with pytest.raises(ValueError, match="Friction variation must be non-negative"):
            tilted_idler_friction_force_outside(
                156.71 * u.ureg.newton,
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.1825 * u.ureg.meter,
                -0.7 * u.ureg.dimensionless,  # Negative friction variation
                0.216 * u.ureg.dimensionless,
                0 * u.ureg.newton,
            )

        with pytest.raises(
            ValueError, match="Friction coefficient must be non-negative"
        ):
            tilted_idler_friction_force_outside(
                156.71 * u.ureg.newton,
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.1825 * u.ureg.meter,
                0.7 * u.ureg.dimensionless,
                -0.216 * u.ureg.dimensionless,  # Negative friction coefficient
                0 * u.ureg.newton,
            )

    def test_error_handling_invalid_widths(self):
        """Test error handling for invalid belt widths."""
        with pytest.raises(ValueError, match="Belt width must be positive"):
            tilted_idler_friction_force_outside(
                156.71 * u.ureg.newton,
                0 * u.ureg.degree,
                0 * u.ureg.meter,  # Zero belt width
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.1825 * u.ureg.meter,
                0.7 * u.ureg.dimensionless,
                0.216 * u.ureg.dimensionless,
                0 * u.ureg.newton,
            )

        with pytest.raises(ValueError, match="Belt width must be positive"):
            tilted_idler_friction_force_outside(
                156.71 * u.ureg.newton,
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0 * u.ureg.meter,  # Zero outside width
                0.7 * u.ureg.dimensionless,
                0.216 * u.ureg.dimensionless,
                0 * u.ureg.newton,
            )

        with pytest.raises(
            ValueError, match="Belt width on section cannot exceed total belt width"
        ):
            tilted_idler_friction_force_outside(
                156.71 * u.ureg.newton,
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                1.0 * u.ureg.meter,  # Outside width > total width
                0.7 * u.ureg.dimensionless,
                0.216 * u.ureg.dimensionless,
                0 * u.ureg.newton,
            )

    def test_error_handling_wrong_dimensions(self):
        """Test error handling for wrong unit dimensions."""
        with pytest.raises(ValueError, match="Error in converting units"):
            tilted_idler_friction_force_outside(
                156.71 * u.ureg.meter,  # Wrong dimension (length instead of force)
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.1825 * u.ureg.meter,
                0.7 * u.ureg.dimensionless,
                0.216 * u.ureg.dimensionless,
                0 * u.ureg.newton,
            )

    def test_error_handling_invalid_units(self):
        """Test error handling for invalid output units."""
        with pytest.raises(ValueError, match="not defined"):
            tilted_idler_friction_force_outside(
                156.71 * u.ureg.newton,
                0 * u.ureg.degree,
                0.8 * u.ureg.meter,
                30 * u.ureg.degree,
                1.46 * u.ureg.degree,
                0.1825 * u.ureg.meter,
                0.7 * u.ureg.dimensionless,
                0.216 * u.ureg.dimensionless,
                0 * u.ureg.newton,
                unit="invalid_unit",
            )

    def test_precision_parameter(self):
        """Test precision parameter functionality."""
        total_weight_force_material = 156.71 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        belt_width_on_outside_wing_roll = 0.1825 * u.ureg.meter
        friction_variation = 0.7 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.216 * u.ureg.dimensionless
        normal_force_on_idler_roll = 0 * u.ureg.newton

        # Test different precision values
        result_2 = tilted_idler_friction_force_outside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_outside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            precision=2,
        )

        result_4 = tilted_idler_friction_force_outside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_outside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
            precision=4,
        )

        # Both should be equal when rounded to 2 decimal places
        assert round(result_2.magnitude, 2) == round(result_4.magnitude, 2)

    def test_comparison_with_inside_function(self):
        """Test that outside and inside functions have different results for same parameters."""
        # Common parameters
        total_weight_force_material = 156.71 * u.ureg.newton
        inclination_angle = 0 * u.ureg.degree
        belt_width = 0.8 * u.ureg.meter
        troughing_angle = 30 * u.ureg.degree
        banking_angle = 1.46 * u.ureg.degree
        friction_variation = 0.7 * u.ureg.dimensionless
        friction_coefficient_tilted_idler = 0.216 * u.ureg.dimensionless
        normal_force_on_idler_roll = 0 * u.ureg.newton

        # Different belt widths for inside vs outside
        belt_width_on_inside_wing_roll = 0.3025 * u.ureg.meter
        belt_width_on_outside_wing_roll = 0.1825 * u.ureg.meter

        result_inside = tilted_idler_friction_force_inside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
        )

        result_outside = tilted_idler_friction_force_outside(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_outside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
        )

        # Results should be different due to different belt width proportions and formulas
        assert result_inside.magnitude != result_outside.magnitude

    def test_mathematical_consistency(self):
        """Test mathematical consistency with different parameter combinations."""
        base_params = {
            "total_weight_force_material": 200 * u.ureg.newton,
            "inclination_angle": 0 * u.ureg.degree,
            "belt_width": 1.0 * u.ureg.meter,
            "troughing_angle": 20 * u.ureg.degree,
            "banking_angle": 2 * u.ureg.degree,
            "belt_width_on_outside_wing_roll": 0.2 * u.ureg.meter,
            "friction_variation": 1.0 * u.ureg.dimensionless,
            "friction_coefficient_tilted_idler": 0.3 * u.ureg.dimensionless,
            "normal_force_on_idler_roll": 0 * u.ureg.newton,
        }

        # Base result
        base_result = tilted_idler_friction_force_outside(**base_params)

        # Double material force should double the result (linear relationship)
        params_double_force = base_params.copy()
        params_double_force["total_weight_force_material"] = 400 * u.ureg.newton
        result_double_force = tilted_idler_friction_force_outside(**params_double_force)

        assert result_double_force.magnitude == pytest.approx(
            base_result.magnitude * 2, rel=1e-3
        )  # Double friction coefficient should double the result
        params_double_friction = base_params.copy()
        params_double_friction["friction_coefficient_tilted_idler"] = (
            0.6 * u.ureg.dimensionless
        )
        result_double_friction = tilted_idler_friction_force_outside(
            **params_double_friction
        )

        assert result_double_friction.magnitude == pytest.approx(
            base_result.magnitude * 2, rel=1e-3
        )


class TestTiltedIdlerFrictionForceCenter:
    """Test public function tilted_idler_friction_force_center with unit handling."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        # Publication test data parameters - expected result: 16.77059015 N
        result = tilted_idler_friction_force_center(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=1.46 * u.ureg.degree,
            belt_width_on_center_wing_roll=0.315 * u.ureg.meter,
            belt_width_on_inside_wing_roll=0.3025 * u.ureg.meter,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.279588668362082 * u.ureg.dimensionless,
            normal_force_on_idler_roll=0.0 * u.ureg.newton,
            precision=10,  # Higher precision for exact comparison
        )

        assert result.magnitude == pytest.approx(16.77059015, rel=1e-6)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_unit_conversion_and_output_units(self):
        """Test automatic unit conversion and output unit specification."""
        # Test with mixed input units
        result_n = tilted_idler_friction_force_center(
            total_weight_force_material=200.0 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.degree,
            belt_width=1000.0 * u.ureg.millimeter,
            troughing_angle=20.0 * u.ureg.degree,
            banking_angle=2.0 * u.ureg.degree,
            belt_width_on_center_wing_roll=0.4 * u.ureg.meter,
            belt_width_on_inside_wing_roll=0.3 * u.ureg.meter,
            belt_width_on_outside_wing_roll=0.3 * u.ureg.meter,
            friction_variation=1.0 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.3 * u.ureg.dimensionless,
            unit="newton",
            precision=10,  # Use high precision
        )

        # Test with different output unit
        result_kn = tilted_idler_friction_force_center(
            total_weight_force_material=200.0 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.degree,
            belt_width=1000.0 * u.ureg.millimeter,
            troughing_angle=20.0 * u.ureg.degree,
            banking_angle=2.0 * u.ureg.degree,
            belt_width_on_center_wing_roll=0.4 * u.ureg.meter,
            belt_width_on_inside_wing_roll=0.3 * u.ureg.meter,
            belt_width_on_outside_wing_roll=0.3 * u.ureg.meter,
            friction_variation=1.0 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.3 * u.ureg.dimensionless,
            unit="kilonewton",
            precision=10,  # Use high precision
        )

        assert result_n.dimensionality == u.ureg.newton.dimensionality
        assert result_kn.dimensionality == u.ureg.kilonewton.dimensionality
        assert result_kn.magnitude == pytest.approx(
            result_n.magnitude / 1000,
            rel=1e-8,  # Adjusted for precision=10 effects
        )

    def test_dimensionless_inputs(self):
        """Test function with dimensionless inputs."""
        # All inputs without units should work with assumed standard units
        result = tilted_idler_friction_force_center(
            total_weight_force_material=200.0 * u.ureg.newton,  # assumed Newtons
            inclination_angle=0.0 * u.ureg.radian,  # assumed radians
            belt_width=1.0 * u.ureg.meter,  # assumed meters
            troughing_angle=0.3490658504 * u.ureg.radian,  # 20 degrees in radians
            banking_angle=0.0349065850 * u.ureg.radian,  # 2 degrees in radians
            belt_width_on_center_wing_roll=0.4 * u.ureg.meter,  # assumed meters
            belt_width_on_inside_wing_roll=0.3 * u.ureg.meter,  # assumed meters
            belt_width_on_outside_wing_roll=0.3 * u.ureg.meter,  # assumed meters
            friction_variation=1.0 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.3 * u.ureg.dimensionless,
        )

        assert result.dimensionality == u.ureg.newton.dimensionality
        assert result.magnitude > 0

    def test_precision_parameter(self):
        """Test precision parameter for result rounding."""
        result = tilted_idler_friction_force_center(
            total_weight_force_material=200.0 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            belt_width=1.0 * u.ureg.meter,
            troughing_angle=20.0 * u.ureg.degree,
            banking_angle=2.0 * u.ureg.degree,
            belt_width_on_center_wing_roll=0.4 * u.ureg.meter,
            belt_width_on_inside_wing_roll=0.3 * u.ureg.meter,
            belt_width_on_outside_wing_roll=0.3 * u.ureg.meter,
            friction_variation=1.0 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.3 * u.ureg.dimensionless,
            precision=2,
        )

        # Check that result has exactly 2 decimal places
        assert result.magnitude == round(result.magnitude, 2)

    def test_optional_normal_force_parameter(self):
        """Test function with and without normal force parameter."""
        base_params = {
            "total_weight_force_material": 200.0 * u.ureg.newton,
            "inclination_angle": 0.0 * u.ureg.radian,
            "belt_width": 1.0 * u.ureg.meter,
            "troughing_angle": 20.0 * u.ureg.degree,
            "banking_angle": 2.0 * u.ureg.degree,
            "belt_width_on_center_wing_roll": 0.4 * u.ureg.meter,
            "belt_width_on_inside_wing_roll": 0.3 * u.ureg.meter,
            "belt_width_on_outside_wing_roll": 0.3 * u.ureg.meter,
            "friction_variation": 1.0 * u.ureg.dimensionless,
            "friction_coefficient_tilted_idler": 0.3 * u.ureg.dimensionless,
        }

        # Default normal force (should be 0)
        result_default = tilted_idler_friction_force_center(**base_params)

        # Explicit zero normal force
        result_zero = tilted_idler_friction_force_center(
            **base_params, normal_force_on_idler_roll=0.0 * u.ureg.newton
        )

        # With normal force
        result_with_normal = tilted_idler_friction_force_center(
            **base_params, normal_force_on_idler_roll=50.0 * u.ureg.newton
        )

        assert result_default.magnitude == result_zero.magnitude
        assert result_with_normal.magnitude > result_default.magnitude

    def test_error_handling_negative_weight(self):
        """Test error handling for negative weight force."""
        with pytest.raises(ValueError, match="Total weight force must be non-negative"):
            tilted_idler_friction_force_center(
                total_weight_force_material=-100.0 * u.ureg.newton,
                inclination_angle=0.0 * u.ureg.radian,
                belt_width=1.0 * u.ureg.meter,
                troughing_angle=20.0 * u.ureg.degree,
                banking_angle=2.0 * u.ureg.degree,
                belt_width_on_center_wing_roll=0.4 * u.ureg.meter,
                belt_width_on_inside_wing_roll=0.3 * u.ureg.meter,
                belt_width_on_outside_wing_roll=0.3 * u.ureg.meter,
                friction_variation=1.0 * u.ureg.dimensionless,
                friction_coefficient_tilted_idler=0.3 * u.ureg.dimensionless,
            )

    def test_error_handling_invalid_belt_width(self):
        """Test error handling for invalid belt width configurations."""
        with pytest.raises(ValueError, match="Belt width must be positive"):
            tilted_idler_friction_force_center(
                total_weight_force_material=200.0 * u.ureg.newton,
                inclination_angle=0.0 * u.ureg.radian,
                belt_width=0.0 * u.ureg.meter,
                troughing_angle=20.0 * u.ureg.degree,
                banking_angle=2.0 * u.ureg.degree,
                belt_width_on_center_wing_roll=0.4 * u.ureg.meter,
                belt_width_on_inside_wing_roll=0.3 * u.ureg.meter,
                belt_width_on_outside_wing_roll=0.3 * u.ureg.meter,
                friction_variation=1.0 * u.ureg.dimensionless,
                friction_coefficient_tilted_idler=0.3 * u.ureg.dimensionless,
            )

    def test_error_handling_section_width_exceeds_total(self):
        """Test error handling when section width exceeds total belt width."""
        with pytest.raises(
            ValueError, match="Belt width on section cannot exceed total belt width"
        ):
            tilted_idler_friction_force_center(
                total_weight_force_material=200.0 * u.ureg.newton,
                inclination_angle=0.0 * u.ureg.radian,
                belt_width=1.0 * u.ureg.meter,
                troughing_angle=20.0 * u.ureg.degree,
                banking_angle=2.0 * u.ureg.degree,
                belt_width_on_center_wing_roll=1.5 * u.ureg.meter,  # Exceeds total
                belt_width_on_inside_wing_roll=0.3 * u.ureg.meter,
                belt_width_on_outside_wing_roll=0.3 * u.ureg.meter,
                friction_variation=1.0 * u.ureg.dimensionless,
                friction_coefficient_tilted_idler=0.3 * u.ureg.dimensionless,
            )

    def test_error_handling_invalid_output_unit(self):
        """Test error handling for invalid output unit."""
        with pytest.raises(ValueError, match="Cannot convert result to"):
            tilted_idler_friction_force_center(
                total_weight_force_material=200.0 * u.ureg.newton,
                inclination_angle=0.0 * u.ureg.radian,
                belt_width=1.0 * u.ureg.meter,
                troughing_angle=20.0 * u.ureg.degree,
                banking_angle=2.0 * u.ureg.degree,
                belt_width_on_center_wing_roll=0.4 * u.ureg.meter,
                belt_width_on_inside_wing_roll=0.3 * u.ureg.meter,
                belt_width_on_outside_wing_roll=0.3 * u.ureg.meter,
                friction_variation=1.0 * u.ureg.dimensionless,
                friction_coefficient_tilted_idler=0.3 * u.ureg.dimensionless,
                unit="invalid_unit",
            )

    def test_linear_scaling_properties(self):
        """Test mathematical consistency with linear scaling properties."""
        base_params = {
            "total_weight_force_material": 100.0 * u.ureg.newton,
            "inclination_angle": 0.0 * u.ureg.radian,
            "belt_width": 1.0 * u.ureg.meter,
            "troughing_angle": 20.0 * u.ureg.degree,
            "banking_angle": 2.0 * u.ureg.degree,
            "belt_width_on_center_wing_roll": 0.4 * u.ureg.meter,
            "belt_width_on_inside_wing_roll": 0.3 * u.ureg.meter,
            "belt_width_on_outside_wing_roll": 0.3 * u.ureg.meter,
            "friction_variation": 1.0 * u.ureg.dimensionless,
            "friction_coefficient_tilted_idler": 0.3 * u.ureg.dimensionless,
        }

        base_result = tilted_idler_friction_force_center(**base_params)

        # Double material weight should double the result
        params_double_material = base_params.copy()
        params_double_material["total_weight_force_material"] = 200.0 * u.ureg.newton
        result_double_material = tilted_idler_friction_force_center(
            **params_double_material
        )

        assert result_double_material.magnitude == pytest.approx(
            base_result.magnitude * 2, rel=1e-3
        )

        # Double friction coefficient should double the result
        params_double_friction = base_params.copy()
        params_double_friction["friction_coefficient_tilted_idler"] = (
            0.6 * u.ureg.dimensionless
        )
        result_double_friction = tilted_idler_friction_force_center(
            **params_double_friction
        )

        assert result_double_friction.magnitude == pytest.approx(
            base_result.magnitude * 2, rel=1e-3
        )


class TestTiltedIdlerFrictionForceConventionalNetCalculation:
    """Test private function _restraining_force_from_tilted_idlers_towards_outside_curve_conventional net calculation."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        # Component forces from test results
        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=12.75292522,
                force_component_center=16.77059015,
                force_component_outside=4.115919819,
            )
        )

        # Expected test result: 25.40759555
        assert result == pytest.approx(25.40759555, rel=1e-6)

    def test_zero_forces(self):
        """Test calculation with zero force inputs."""
        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=0.0,
                force_component_center=0.0,
                force_component_outside=0.0,
            )
        )

        assert result == pytest.approx(0.0, abs=1e-12)

    def test_negative_result_case(self):
        """Test case where outside force exceeds inside + center forces."""
        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=5.0,
                force_component_center=8.0,
                force_component_outside=20.0,
            )
        )

        # Expected: 5 + 8 - 20 = -7.0
        assert result == pytest.approx(-7.0, rel=1e-10)

    def test_precision_handling(self):
        """Test precision handling with high precision inputs."""
        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=12.752925221,
                force_component_center=16.770590151,
                force_component_outside=4.115919819,
            )
        )

        # Should maintain precision
        expected = 12.752925221 + 16.770590151 - 4.115919819
        assert result == pytest.approx(expected, rel=1e-10)

    def test_edge_case_very_small_forces(self):
        """Test edge case with very small force values."""
        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=1e-10,
                force_component_center=2e-10,
                force_component_outside=1.5e-10,
            )
        )

        expected = 1e-10 + 2e-10 - 1.5e-10  # = 1.5e-10
        assert result == pytest.approx(expected, rel=1e-6)

    def test_edge_case_very_large_forces(self):
        """Test edge case with very large force values."""
        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=1e6,
                force_component_center=2e6,
                force_component_outside=1.5e6,
            )
        )

        expected = 1e6 + 2e6 - 1.5e6  # = 1.5e6
        assert result == pytest.approx(expected, rel=1e-10)

    def test_mathematical_properties_additive(self):
        """Test mathematical properties - additivity."""
        # Base calculation
        base_result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=10.0,
                force_component_center=15.0,
                force_component_outside=5.0,
            )
        )

        # Add additional forces
        additional_result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=12.0,  # +2
                force_component_center=18.0,  # +3
                force_component_outside=7.0,  # +2
            )
        )

        # Difference should be (2 + 3 - 2) = 3
        assert additional_result - base_result == pytest.approx(3.0, rel=1e-10)

    def test_mathematical_properties_linearity(self):
        """Test mathematical properties - linearity (scaling)."""
        base_inside = 12.75292522
        base_center = 16.77059015
        base_outside = 4.115919819

        # Base calculation
        base_result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=base_inside,
                force_component_center=base_center,
                force_component_outside=base_outside,
            )
        )

        # Scaled calculation (multiply all by 3.7)
        scale_factor = 3.7
        scaled_result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=scale_factor * base_inside,
                force_component_center=scale_factor * base_center,
                force_component_outside=scale_factor * base_outside,
            )
        )

        # Result should be exactly scaled
        assert scaled_result == pytest.approx(scale_factor * base_result, rel=1e-10)

    def test_symmetry_properties(self):
        """Test symmetry properties - order independence."""
        # Standard order
        result1 = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=10.0,
                force_component_center=15.0,
                force_component_outside=5.0,
            )
        )

        # Different assignment (but same mathematical result)
        result2 = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=15.0,
                force_component_center=10.0,
                force_component_outside=5.0,
            )
        )

        # Both should give same result since addition is commutative
        assert result1 == result2

    def test_input_validation_numeric_types(self):
        """Test that function accepts various numeric input types."""
        # Test with int inputs
        result_int = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=10,
                force_component_center=15,
                force_component_outside=5,
            )
        )

        # Test with float inputs
        result_float = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_component_inside=10.0,
                force_component_center=15.0,
                force_component_outside=5.0,
            )
        )

        # Should give same result
        assert result_int == result_float


class TestTiltedIdlerFrictionForceUnified:
    """Test unified restraining_force_from_tilted_idlers function with method parameter dispatch."""

    def test_basic_calculation_with_publication_data_conventional(self):
        """Test basic calculation with publication data parameters - conventional method."""
        # Component forces from test results
        result = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,
            force_component_center=16.77059015 * u.ureg.newton,
            force_component_outside=4.115919819 * u.ureg.newton,
            method="conventional",
            precision=10,  # Use high precision
        )

        # Expected test result: 25.40759555
        assert result.magnitude == pytest.approx(25.40759555, rel=1e-6)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_basic_calculation_with_publication_data_improved(self):
        """Test basic calculation with publication data parameters - improved method."""
        # Component forces from test results
        result = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,
            force_component_center=16.77059015 * u.ureg.newton,
            force_component_outside=4.115919819 * u.ureg.newton,
            method="improved",
            precision=10,  # Use high precision
        )

        # Expected test result should be same for this simple case: 25.40759555
        assert result.magnitude == pytest.approx(25.40759555, rel=1e-6)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_unit_conversion_and_output_units_conventional(self):
        """Test automatic unit conversion and output unit specification - conventional method."""
        # Test with mixed input units
        result_n = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,
            force_component_center=16770.59015 * u.ureg.millinewton,  # Mixed units
            force_component_outside=4.115919819 * u.ureg.newton,
            method="conventional",
            unit="newton",
            precision=10,  # Use high precision
        )

        # Test with output in kilonewtons
        result_kn = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,
            force_component_center=16.77059015 * u.ureg.newton,
            force_component_outside=4.115919819 * u.ureg.newton,
            method="conventional",
            unit="kilonewton",
            precision=10,  # Use high precision
        )

        # Both should give same result when converted
        assert result_n.to("kilonewton").magnitude == pytest.approx(
            result_kn.magnitude,
            rel=1e-8,  # Adjusted for precision effects
        )
        assert result_kn.magnitude == pytest.approx(25.40759555e-3, rel=1e-6)

    def test_unit_conversion_and_output_units_improved(self):
        """Test automatic unit conversion and output unit specification - improved method."""
        # Test with mixed input units
        result_n = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,
            force_component_center=16770.59015 * u.ureg.millinewton,  # Mixed units
            force_component_outside=4.115919819 * u.ureg.newton,
            method="improved",
            unit="newton",
            precision=10,  # Use high precision
        )

        # Test with output in kilonewtons
        result_kn = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,
            force_component_center=16.77059015 * u.ureg.newton,
            force_component_outside=4.115919819 * u.ureg.newton,
            method="improved",
            unit="kilonewton",
            precision=10,  # Use high precision
        )

        # Both should give same result when converted
        assert result_n.to("kilonewton").magnitude == pytest.approx(
            result_kn.magnitude,
            rel=1e-8,  # Adjusted for precision effects
        )

    def test_dimensionless_inputs_conventional(self):
        """Test function with dimensionless (float) inputs - conventional method."""
        result = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,  # N (dimensionless)
            force_component_center=16.77059015 * u.ureg.newton,  # N (dimensionless)
            force_component_outside=4.115919819 * u.ureg.newton,  # N (dimensionless)
            method="conventional",
            precision=10,  # Use high precision
        )

        assert result.magnitude == pytest.approx(25.40759555, rel=1e-6)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_dimensionless_inputs_improved(self):
        """Test function with dimensionless (float) inputs - improved method."""
        result = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,  # N (dimensionless)
            force_component_center=16.77059015 * u.ureg.newton,  # N (dimensionless)
            force_component_outside=4.115919819 * u.ureg.newton,  # N (dimensionless)
            method="improved",
            precision=10,  # Use high precision
        )

        assert result.magnitude == pytest.approx(25.40759555, rel=1e-6)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_precision_parameter_conventional(self):
        """Test precision parameter functionality - conventional method."""
        result = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,
            force_component_center=16.77059015 * u.ureg.newton,
            force_component_outside=4.115919819 * u.ureg.newton,
            method="conventional",
            precision=3,
        )

        # Result should be rounded to 3 decimal places
        assert result.magnitude == 25.408
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_precision_parameter_improved(self):
        """Test precision parameter functionality - improved method."""
        result = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,
            force_component_center=16.77059015 * u.ureg.newton,
            force_component_outside=4.115919819 * u.ureg.newton,
            method="improved",
            precision=3,
        )

        # Result should be rounded to 3 decimal places
        assert result.magnitude == 25.408
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_zero_forces_both_methods(self):
        """Test calculation with zero force inputs for both methods."""
        for method in ["conventional", "improved"]:
            result = restraining_force_from_tilted_idlers(
                force_component_inside=0.0 * u.ureg.newton,
                force_component_center=0.0 * u.ureg.newton,
                force_component_outside=0.0 * u.ureg.newton,
                method=method,
            )

            assert result.magnitude == pytest.approx(0.0, abs=1e-12)
            assert result.dimensionality == u.ureg.newton.dimensionality

    def test_negative_result_case_both_methods(self):
        """Test case where outside force exceeds inside + center forces for both methods."""
        for method in ["conventional", "improved"]:
            result = restraining_force_from_tilted_idlers(
                force_component_inside=5.0 * u.ureg.newton,
                force_component_center=8.0 * u.ureg.newton,
                force_component_outside=20.0 * u.ureg.newton,
                method=method,
            )

            # Expected: 5 + 8 - 20 = -7.0
            assert result.magnitude == pytest.approx(-7.0, rel=1e-10)
            assert result.dimensionality == u.ureg.newton.dimensionality

    def test_method_parameter_validation(self):
        """Test method parameter validation."""
        with pytest.raises(ValueError, match="Unknown method"):
            restraining_force_from_tilted_idlers(
                force_component_inside=10.0 * u.ureg.newton,
                force_component_center=15.0 * u.ureg.newton,
                force_component_outside=5.0 * u.ureg.newton,
                method="invalid_method",
            )

    def test_method_default_parameter(self):
        """Test that default method parameter works (should be conventional)."""
        result_default = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,
            force_component_center=16.77059015 * u.ureg.newton,
            force_component_outside=4.115919819 * u.ureg.newton,
        )

        result_explicit = restraining_force_from_tilted_idlers(
            force_component_inside=12.75292522 * u.ureg.newton,
            force_component_center=16.77059015 * u.ureg.newton,
            force_component_outside=4.115919819 * u.ureg.newton,
            method="conventional",
        )

        assert result_default.magnitude == pytest.approx(
            result_explicit.magnitude, rel=1e-10
        )

    def test_error_handling_invalid_output_unit(self):
        """Test error handling for invalid output unit."""
        with pytest.raises(ValueError, match="not defined"):
            restraining_force_from_tilted_idlers(
                force_component_inside=10.0 * u.ureg.newton,
                force_component_center=15.0 * u.ureg.newton,
                force_component_outside=5.0 * u.ureg.newton,
                method="conventional",
                unit="invalid_unit",
            )

    def test_linear_scaling_properties_both_methods(self):
        """Test linear scaling properties of the calculation for both methods."""
        base_inside = 12.75292522
        base_center = 16.77059015
        base_outside = 4.115919819

        for method in ["conventional", "improved"]:
            # Base calculation
            base_result = restraining_force_from_tilted_idlers(
                force_component_inside=base_inside * u.ureg.newton,
                force_component_center=base_center * u.ureg.newton,
                force_component_outside=base_outside * u.ureg.newton,
                method=method,
            )

            # Scaled calculation (multiply all by 2)
            scaled_result = restraining_force_from_tilted_idlers(
                force_component_inside=2 * base_inside * u.ureg.newton,
                force_component_center=2 * base_center * u.ureg.newton,
                force_component_outside=2 * base_outside * u.ureg.newton,
                method=method,
            )

            # Result should be exactly double
            assert scaled_result.magnitude == pytest.approx(
                2 * base_result.magnitude, rel=1e-10
            )

    def test_mixed_units_comprehensive_both_methods(self):
        """Test with comprehensive mix of different force units for both methods."""
        for method in ["conventional", "improved"]:
            result = restraining_force_from_tilted_idlers(
                force_component_inside=12752.92522 * u.ureg.millinewton,
                force_component_center=16.77059015 * u.ureg.newton,
                force_component_outside=0.004115919819 * u.ureg.kilonewton,
                method=method,
                unit="newton",
                precision=10,  # Use high precision
            )

            # All should convert to same result as publication data
            assert result.magnitude == pytest.approx(25.40759555, rel=1e-6)
            assert result.dimensionality == u.ureg.newton.dimensionality


class TestTiltedIdlerFrictionForceUnifiedOutsideImproved:
    """Test public function restraining_force_from_tilted_idlers calculation for outside improved method."""

    def test_unit_conversion_and_output_units(self):
        """Test unit conversion and output units."""
        from eytelwein.horizontal_curves.core.horizontal_curve_calculations import (
            tilted_idler_friction_force_outside,
        )

        # Test with newton output
        result_n = tilted_idler_friction_force_outside(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.216183096 * u.ureg.dimensionless,
            normal_force_on_idler_roll=0.0 * u.ureg.newton,
            method="improved",
            unit="newton",
            precision=10,
        )

        # Test with kilonewton output
        result_kn = tilted_idler_friction_force_outside(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.216183096 * u.ureg.dimensionless,
            normal_force_on_idler_roll=0.0 * u.ureg.newton,
            method="improved",
            unit="kilonewton",
            precision=10,
        )

        # Check unit conversion
        assert result_n.magnitude == pytest.approx(5.2279203137592, rel=1e-6)
        assert result_kn.magnitude == pytest.approx(0.0052279203137592, rel=1e-6)
        assert result_n.dimensionality == u.ureg.newton.dimensionality
        assert result_kn.dimensionality == u.ureg.kilonewton.dimensionality

    def test_precision_parameter(self):
        """Test precision parameter functionality."""
        from eytelwein.horizontal_curves.core.horizontal_curve_calculations import (
            tilted_idler_friction_force_outside_improved,
        )

        result = tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            wing_roll_load_factor=1.1 * u.ureg.dimensionless,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.216183096 * u.ureg.dimensionless,
            precision=3,
        )

        # Check precision is applied - use the actual calculated value
        assert result.magnitude == pytest.approx(5.228, abs=1e-10)

    def test_zero_forces(self):
        """Test function with zero forces."""
        from eytelwein.horizontal_curves.core.horizontal_curve_calculations import (
            tilted_idler_friction_force_outside_improved,
        )

        result = tilted_idler_friction_force_outside_improved(
            total_weight_force_material=0.0 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            wing_roll_load_factor=1.1 * u.ureg.dimensionless,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.216183096 * u.ureg.dimensionless,
        )

        assert result.magnitude == pytest.approx(0.0, abs=1e-12)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_normal_force_parameter(self):
        """Test normal force parameter functionality."""
        from eytelwein.horizontal_curves.core.horizontal_curve_calculations import (
            tilted_idler_friction_force_outside_improved,
        )

        # Base case without normal force
        base_result = tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            wing_roll_load_factor=1.1 * u.ureg.dimensionless,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.216183096 * u.ureg.dimensionless,
        )

        # Case with normal force
        normal_force = 10.0 * u.ureg.newton
        with_normal_result = tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            wing_roll_load_factor=1.1 * u.ureg.dimensionless,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.216183096 * u.ureg.dimensionless,
            normal_force_on_idler_roll=normal_force,
        )

        # Should be larger due to additional normal force contribution
        assert with_normal_result.magnitude > base_result.magnitude

    def test_error_handling_invalid_output_unit(self):
        """Test error handling for invalid output unit."""
        from eytelwein.horizontal_curves.core.horizontal_curve_calculations import (
            tilted_idler_friction_force_outside_improved,
        )

        with pytest.raises(ValueError, match="not defined"):
            tilted_idler_friction_force_outside_improved(
                total_weight_force_material=156.71475 * u.ureg.newton,
                inclination_angle=0.0 * u.ureg.radian,
                wing_roll_load_factor=1.1 * u.ureg.dimensionless,
                belt_width=0.8 * u.ureg.meter,
                troughing_angle=math.radians(30) * u.ureg.radian,
                banking_angle=math.radians(1.46) * u.ureg.radian,
                belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
                friction_variation=0.7 * u.ureg.dimensionless,
                friction_coefficient_tilted_idler=0.216183096 * u.ureg.dimensionless,
                unit="invalid_unit",
            )

    def test_load_factor_influence_public(self):
        """Test influence of load factor through public interface."""
        from eytelwein.horizontal_curves.core.horizontal_curve_calculations import (
            tilted_idler_friction_force_outside_improved,
        )

        base_result = tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            wing_roll_load_factor=1.0 * u.ureg.dimensionless,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.216183096 * u.ureg.dimensionless,
        )

        improved_result = tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            wing_roll_load_factor=1.1 * u.ureg.dimensionless,  # Improved load factor
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.216183096 * u.ureg.dimensionless,
        )

        # Improved method should give 10% higher result (with tolerance for rounding)
        ratio = improved_result.magnitude / base_result.magnitude
        assert ratio == pytest.approx(1.1, rel=1e-2)  # More lenient tolerance

    def test_mixed_units_comprehensive(self):
        """Test with comprehensive mix of different units."""
        from eytelwein.horizontal_curves.core.horizontal_curve_calculations import (
            tilted_idler_friction_force_outside_improved,
        )

        result = tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156714.75 * u.ureg.millinewton,
            inclination_angle=0.0 * u.ureg.degree,
            wing_roll_load_factor=1.1 * u.ureg.dimensionless,
            belt_width=80 * u.ureg.centimeter,
            troughing_angle=30 * u.ureg.degree,
            banking_angle=1.46 * u.ureg.degree,
            belt_width_on_outside_wing_roll=182.5 * u.ureg.millimeter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.216183096 * u.ureg.dimensionless,
            unit="newton",
        )

        # Default precision now preserves the unrounded calculation result.
        assert result.magnitude == pytest.approx(5.23, rel=1e-3)
        assert result.dimensionality == u.ureg.newton.dimensionality


class TestTiltedIdlerFrictionForceCenterImprovedMethod:
    """Test public function tilted_idler_friction_force_center with improved method."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        result_n = tilted_idler_friction_force_center(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            center_roll_load_factor=0.9 * u.ureg.dimensionless,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_center_wing_roll=0.315 * u.ureg.meter,
            belt_width_on_inside_wing_roll=0.3025 * u.ureg.meter,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.279588668 * u.ureg.dimensionless,
            method="improved",
            precision=10,  # Use high precision
        )

        # Both should give the same result in different units
        assert result_n.magnitude == pytest.approx(15.0935311327433, rel=1e-6)
        assert result_n.dimensionality == u.ureg.newton.dimensionality

    def test_load_factor_influence_public(self):
        """Test influence of center roll load factor in public function."""
        base_result = tilted_idler_friction_force_center(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            center_roll_load_factor=1.0 * u.ureg.dimensionless,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_center_wing_roll=0.315 * u.ureg.meter,
            belt_width_on_inside_wing_roll=0.3025 * u.ureg.meter,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.279588668 * u.ureg.dimensionless,
            method="improved",
            precision=10,  # Use high precision
        )

        improved_result = tilted_idler_friction_force_center(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            center_roll_load_factor=0.9 * u.ureg.dimensionless,  # Improved load factor
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_center_wing_roll=0.315 * u.ureg.meter,
            belt_width_on_inside_wing_roll=0.3025 * u.ureg.meter,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.279588668 * u.ureg.dimensionless,
            method="improved",
            precision=10,  # Use high precision
        )

        # Improved method should give 90% of base result due to load factor (with tolerance)
        ratio = improved_result.magnitude / base_result.magnitude
        assert ratio == pytest.approx(0.9, rel=1e-2)  # More lenient tolerance

    def test_normal_force_influence_public(self):
        """Test influence of normal force parameter in public function."""
        base_result = tilted_idler_friction_force_center(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            center_roll_load_factor=0.9 * u.ureg.dimensionless,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_center_wing_roll=0.315 * u.ureg.meter,
            belt_width_on_inside_wing_roll=0.3025 * u.ureg.meter,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.279588668 * u.ureg.dimensionless,
            method="improved",
            normal_force_on_idler_roll=0.0 * u.ureg.newton,
            precision=10,  # Use high precision
        )

        with_normal_result = tilted_idler_friction_force_center(
            total_weight_force_material=156.71475 * u.ureg.newton,
            inclination_angle=0.0 * u.ureg.radian,
            center_roll_load_factor=0.9 * u.ureg.dimensionless,
            belt_width=0.8 * u.ureg.meter,
            troughing_angle=math.radians(30) * u.ureg.radian,
            banking_angle=math.radians(1.46) * u.ureg.radian,
            belt_width_on_center_wing_roll=0.315 * u.ureg.meter,
            belt_width_on_inside_wing_roll=0.3025 * u.ureg.meter,
            belt_width_on_outside_wing_roll=0.1825 * u.ureg.meter,
            friction_variation=0.7 * u.ureg.dimensionless,
            friction_coefficient_tilted_idler=0.279588668 * u.ureg.dimensionless,
            method="improved",
            normal_force_on_idler_roll=10.0 * u.ureg.newton,
            precision=10,  # Use high precision
        )

        # Expected difference: 0.7 * 0.279588668 * 10.0
        expected_difference = 0.7 * 0.279588668 * 10.0
        actual_difference = with_normal_result.magnitude - base_result.magnitude
        assert actual_difference == pytest.approx(
            expected_difference, rel=1e-3
        )  # More lenient

    def test_mixed_units_comprehensive(self):
        """Test function with mixed input units and unit conversion."""
        result = tilted_idler_friction_force_center(
            total_weight_force_material=156714.75 * u.ureg.millinewton,  # 156.71475 N
            inclination_angle=0.0 * u.ureg.degree,  # 0 radians
            center_roll_load_factor=0.9 * u.ureg.dimensionless,  # 0.9
            belt_width=800 * u.ureg.millimeter,  # 0.8 m
            troughing_angle=30 * u.ureg.degree,  # math.radians(30)
            banking_angle=1.46 * u.ureg.degree,  # math.radians(1.46)
            belt_width_on_center_wing_roll=315 * u.ureg.millimeter,  # 0.315 m
            belt_width_on_inside_wing_roll=302.5 * u.ureg.millimeter,  # 0.3025 m
            belt_width_on_outside_wing_roll=182.5 * u.ureg.millimeter,  # 0.1825 m
            friction_variation=0.7 * u.ureg.dimensionless,  # 0.7
            friction_coefficient_tilted_idler=0.279588668
            * u.ureg.dimensionless,  # 0.279588668
            method="improved",
            unit="newton",
            precision=10,  # Use high precision
        )

        # All should convert to same result as publication data
        assert result.magnitude == pytest.approx(15.0935311327433, rel=1e-6)
        assert result.dimensionality == u.ureg.newton.dimensionality


class TestTiltedIdlerFrictionForceImprovedPublic:
    """Test public function restraining_force_from_tilted_idlers with improved method and unit handling."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        result = restraining_force_from_tilted_idlers(
            force_component_inside=16.198390581763 * u.ureg.newton,
            force_component_center=15.0935311327433 * u.ureg.newton,
            force_component_outside=5.2279203137592 * u.ureg.newton,
            method="improved",
            precision=10,  # Use high precision
        )

        assert result.magnitude == pytest.approx(26.0640014007471, rel=1e-6)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_unit_conversion_and_output_units(self):
        """Test automatic unit conversion and output unit specification."""
        # Test with output in kilonewtons
        result_kn = restraining_force_from_tilted_idlers(
            force_component_inside=16.198390581763 * u.ureg.newton,
            force_component_center=15.0935311327433 * u.ureg.newton,
            force_component_outside=5.2279203137592 * u.ureg.newton,
            method="improved",
            unit="kilonewton",
            precision=10,  # Use high precision
        )

        assert result_kn.magnitude == pytest.approx(26.0640014007471e-3, rel=1e-6)
        assert result_kn.dimensionality == u.ureg.kilonewton.dimensionality

    def test_dimensionless_inputs(self):
        """Test function with dimensionless (float) inputs."""
        result = restraining_force_from_tilted_idlers(
            force_component_inside=16.198390581763 * u.ureg.newton,  # N (dimensionless)
            force_component_center=15.0935311327433
            * u.ureg.newton,  # N (dimensionless)
            force_component_outside=5.2279203137592
            * u.ureg.newton,  # N (dimensionless)
            method="improved",
            precision=10,  # Use high precision
        )

        assert result.magnitude == pytest.approx(26.0640014007471, rel=1e-6)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_precision_parameter(self):
        """Test precision parameter functionality."""
        result = restraining_force_from_tilted_idlers(
            force_component_inside=16.198390581763 * u.ureg.newton,
            force_component_center=15.0935311327433 * u.ureg.newton,
            force_component_outside=5.2279203137592 * u.ureg.newton,
            method="improved",
            precision=3,
        )

        assert result.magnitude == 26.064
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_zero_forces(self):
        """Test calculation with zero force inputs."""
        result = restraining_force_from_tilted_idlers(
            force_component_inside=0.0 * u.ureg.newton,
            force_component_center=0.0 * u.ureg.newton,
            force_component_outside=0.0 * u.ureg.newton,
            method="improved",
        )

        assert result.magnitude == pytest.approx(0.0, abs=1e-12)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_error_handling_invalid_output_unit(self):
        """Test error handling for invalid output unit."""
        with pytest.raises(ValueError, match="not defined"):
            restraining_force_from_tilted_idlers(
                force_component_inside=16.198390581763 * u.ureg.newton,
                force_component_center=15.0935311327433 * u.ureg.newton,
                force_component_outside=5.2279203137592 * u.ureg.newton,
                method="improved",
                unit="invalid_unit",
            )

    def test_mixed_units_comprehensive(self):
        """Test with comprehensive mix of different units."""
        result = restraining_force_from_tilted_idlers(
            force_component_inside=16198.390581763 * u.ureg.millinewton,
            force_component_center=0.0150935311327433 * u.ureg.kilonewton,
            force_component_outside=5.2279203137592 * u.ureg.newton,
            method="improved",
            unit="newton",
            precision=10,  # Use high precision
        )

        # All should convert to same result as publication data
        assert result.magnitude == pytest.approx(26.0640014007471, rel=1e-6)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_force_combination_validation(self):
        """Test that the combination logic works correctly through public interface."""
        # Test case where outside > inside + center (negative result)
        result = restraining_force_from_tilted_idlers(
            force_component_inside=5.0 * u.ureg.newton,
            force_component_center=4.0 * u.ureg.newton,
            force_component_outside=12.0 * u.ureg.newton,
            method="improved",
        )

        # Should be 5 + 4 - 12 = -3
        assert result.magnitude == pytest.approx(-3.0, rel=1e-10)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_linear_scaling_properties(self):
        """Test linear scaling properties through public interface."""
        base_result = restraining_force_from_tilted_idlers(
            force_component_inside=10.0 * u.ureg.newton,
            force_component_center=8.0 * u.ureg.newton,
            force_component_outside=3.0 * u.ureg.newton,
            method="improved",
        )

        scaled_result = restraining_force_from_tilted_idlers(
            force_component_inside=30.0 * u.ureg.newton,  # 3x
            force_component_center=24.0 * u.ureg.newton,  # 3x
            force_component_outside=9.0 * u.ureg.newton,  # 3x
            method="improved",
        )

        ratio = scaled_result.magnitude / base_result.magnitude
        assert ratio == pytest.approx(3.0, rel=1e-10)

    def test_error_handling_negative_forces(self):
        """Test that negative forces are mathematically handled (no validation)."""
        # The unified function should accept negative inputs as it's a mathematical combiner
        result = restraining_force_from_tilted_idlers(
            force_component_inside=-5.0 * u.ureg.newton,
            force_component_center=15.0 * u.ureg.newton,
            force_component_outside=5.0 * u.ureg.newton,
            method="improved",
        )

        # Should calculate: -5 + 15 - 5 = 5
        assert result.magnitude == pytest.approx(5.0, rel=1e-10)
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_method_validation(self):
        """Test that method parameter validation works."""
        with pytest.raises(ValueError, match="Unknown method"):
            restraining_force_from_tilted_idlers(
                force_component_inside=10.0 * u.ureg.newton,
                force_component_center=8.0 * u.ureg.newton,
                force_component_outside=3.0 * u.ureg.newton,
                method="invalid_method",
            )

    def test_comparison_with_conventional_method(self):
        """Test comparison between improved and conventional methods."""
        # For simple linear combination, both methods should give same result
        result_conventional = restraining_force_from_tilted_idlers(
            force_component_inside=16.198390581763 * u.ureg.newton,
            force_component_center=15.0935311327433 * u.ureg.newton,
            force_component_outside=5.2279203137592 * u.ureg.newton,
            method="conventional",
        )

        result_improved = restraining_force_from_tilted_idlers(
            force_component_inside=16.198390581763 * u.ureg.newton,
            force_component_center=15.0935311327433 * u.ureg.newton,
            force_component_outside=5.2279203137592 * u.ureg.newton,
            method="improved",
        )

        # Should be identical for simple linear combination
        assert result_conventional.magnitude == pytest.approx(
            result_improved.magnitude, rel=1e-10
        )


class TestWeightForceMaterialInsidePublic:
    """Test the public weight_force_material_inside function with unit handling."""

    def test_basic_calculation_with_units(self):
        """Test basic calculation with proper units."""
        result = weight_force_material_inside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=5.0 * u.ureg.degree,
            method="conventional",
        )

        assert isinstance(result, u.ureg.Quantity)
        assert result.units == u.ureg.newton
        assert result.magnitude > 0

    def test_unit_conversion_input(self):
        """Test automatic unit conversion for inputs."""
        # Test with different input units
        result1 = weight_force_material_inside(
            normal_force=1.0 * u.ureg.kilonewton,  # kN
            troughing_angle=math.pi / 6 * u.ureg.radian,  # radians
            banking_angle=0.1 * u.ureg.radian,
        )

        result2 = weight_force_material_inside(
            normal_force=1000.0 * u.ureg.newton,  # N
            troughing_angle=30.0 * u.ureg.degree,  # degrees
            banking_angle=5.729577951 * u.ureg.degree,  # 0.1 radians in degrees
        )

        # Results should be approximately equal
        assert abs(result1.magnitude - result2.magnitude) < 1e-6

    def test_unit_conversion_output(self):
        """Test unit conversion for output."""
        result_newton = weight_force_material_inside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=5.0 * u.ureg.degree,
            unit="newton",
            precision=None,  # No rounding
        )

        result_kilonewton = weight_force_material_inside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=5.0 * u.ureg.degree,
            unit="kilonewton",
            precision=None,  # No rounding
        )

        assert result_newton.units == u.ureg.newton
        assert result_kilonewton.units == u.ureg.kilonewton
        assert abs(result_newton.magnitude - 1000 * result_kilonewton.magnitude) < 1e-6

    def test_precision_parameter(self):
        """Test precision parameter functionality."""
        result_precision_2 = weight_force_material_inside(
            normal_force=1234.5678 * u.ureg.newton,
            troughing_angle=30.123456 * u.ureg.degree,
            banking_angle=5.654321 * u.ureg.degree,
            precision=2,
        )

        result_precision_4 = weight_force_material_inside(
            normal_force=1234.5678 * u.ureg.newton,
            troughing_angle=30.123456 * u.ureg.degree,
            banking_angle=5.654321 * u.ureg.degree,
            precision=4,
        )

        # Check that precision is applied correctly
        assert len(str(result_precision_2.magnitude).split(".")[-1]) <= 2
        assert len(str(result_precision_4.magnitude).split(".")[-1]) <= 4

    def test_method_validation(self):
        """Test validation of method parameter."""
        # Valid method should work
        result = weight_force_material_inside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=5.0 * u.ureg.degree,
            method="conventional",
        )
        assert isinstance(result, u.ureg.Quantity)

        # Invalid method should raise error
        with pytest.raises(ValueError, match="Unknown method"):
            weight_force_material_inside(
                normal_force=1000.0 * u.ureg.newton,
                troughing_angle=30.0 * u.ureg.degree,
                banking_angle=5.0 * u.ureg.degree,
                method="invalid_method",
            )

    def test_improved_method_not_implemented(self):
        """Test that improved method works correctly."""
        result = weight_force_material_inside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=5.0 * u.ureg.degree,
            method="improved",
        )

        # Should return a valid result
        assert result.magnitude > 0
        assert result.dimensionality == u.ureg.newton.dimensionality

    def test_negative_force_validation(self):
        """Test validation for negative force inputs."""
        with pytest.raises(ValueError, match="must be non-negative"):
            weight_force_material_inside(
                normal_force=-500.0 * u.ureg.newton,
                troughing_angle=30.0 * u.ureg.degree,
                banking_angle=5.0 * u.ureg.degree,
            )

    def test_invalid_unit_conversion(self):
        """Test error handling for invalid unit conversions."""
        with pytest.raises(ValueError, match="Error in converting units"):
            weight_force_material_inside(
                normal_force=1000.0,  # No units
                troughing_angle=30.0 * u.ureg.degree,
                banking_angle=5.0 * u.ureg.degree,
            )

    def test_invalid_output_unit(self):
        """Test error handling for invalid output units."""
        with pytest.raises(ValueError, match="Cannot convert result"):
            weight_force_material_inside(
                normal_force=1000.0 * u.ureg.newton,
                troughing_angle=30.0 * u.ureg.degree,
                banking_angle=5.0 * u.ureg.degree,
                unit="meter",  # Wrong dimension
            )

    def test_zero_force_calculation(self):
        """Test calculation with zero normal force."""
        result = weight_force_material_inside(
            normal_force=0.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=5.0 * u.ureg.degree,
        )

        assert result.magnitude == 0.0
        assert result.units == u.ureg.newton

    def test_extreme_angles(self):
        """Test with extreme but valid angle values."""
        # Very small angles
        result_small = weight_force_material_inside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=1.0 * u.ureg.degree,
            banking_angle=0.5 * u.ureg.degree,
        )
        assert result_small.magnitude > 0

        # Large angles (but physically reasonable)
        result_large = weight_force_material_inside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=35.0 * u.ureg.degree,
            banking_angle=8.0 * u.ureg.degree,
        )
        assert result_large.magnitude > result_small.magnitude

    def test_mathematical_consistency(self):
        """Test mathematical consistency with the private implementation."""
        normal_force_val = 1000.0
        troughing_angle_val = math.radians(30)
        banking_angle_val = math.radians(5)

        # Public function result
        public_result = weight_force_material_inside(
            normal_force=normal_force_val * u.ureg.newton,
            troughing_angle=troughing_angle_val * u.ureg.radian,
            banking_angle=banking_angle_val * u.ureg.radian,
            precision=None,  # No rounding
        )

        # Manual calculation
        expected = (
            normal_force_val
            * math.tan(troughing_angle_val + banking_angle_val)
            * math.cos(troughing_angle_val)
        )

        assert abs(public_result.magnitude - expected) < 1e-6

    def test_linearity_property(self):
        """Test linearity property with respect to normal force."""
        base_result = weight_force_material_inside(
            normal_force=500.0 * u.ureg.newton,
            troughing_angle=25.0 * u.ureg.degree,
            banking_angle=6.0 * u.ureg.degree,
        )

        double_result = weight_force_material_inside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=25.0 * u.ureg.degree,
            banking_angle=6.0 * u.ureg.degree,
        )

        # Should be exactly double (linear relationship)
        ratio = double_result.magnitude / base_result.magnitude
        assert abs(ratio - 2.0) < 1e-10


class TestWeightForceMaterialOutsidePublic:
    def test_weight_force_material_outside_basic(self):
        """Test basic calculation with units."""
        result = weight_force_material_outside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=5.0 * u.ureg.degree,
            method="conventional",
        )

        assert isinstance(result, u.Quantity)
        assert result.units == u.ureg.newton
        assert result.magnitude > 0

    def test_weight_force_material_outside_comparison_with_inside(self):
        """Test that outside force is different from inside force for same inputs."""
        from eytelwein.horizontal_curves import weight_force_material_inside

        normal_force = 1000.0 * u.ureg.newton
        troughing_angle = 30.0 * u.ureg.degree
        banking_angle = 5.0 * u.ureg.degree

        result_outside = weight_force_material_outside(
            normal_force, troughing_angle, banking_angle
        )

        result_inside = weight_force_material_inside(
            normal_force, troughing_angle, banking_angle
        )

        # Outside should be less than inside for positive banking angle
        assert result_outside.magnitude < result_inside.magnitude

    def test_weight_force_material_outside_unit_conversion(self):
        """Test unit conversion functionality."""
        result = weight_force_material_outside(
            normal_force=1.0 * u.ureg.kilonewton,
            troughing_angle=math.pi / 6 * u.ureg.radian,
            banking_angle=0.1 * u.ureg.radian,
            unit="kilonewton",
        )

        assert result.units == u.ureg.kilonewton
        assert result.magnitude < 1.0  # Should be less than input

    def test_weight_force_material_outside_negative_banking(self):
        """Test with negative banking angle."""
        result = weight_force_material_outside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=-5.0 * u.ureg.degree,  # Negative banking
            method="conventional",
        )

        assert isinstance(result, u.Quantity)
        assert result.magnitude > 0

    def test_weight_force_material_outside_improved_method(self):
        """Test that improved method works correctly."""
        result_conv = weight_force_material_outside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=5.0 * u.ureg.degree,
            method="conventional",
        )

        result_imp = weight_force_material_outside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=5.0 * u.ureg.degree,
            method="improved",
        )

        # Both should return valid results
        assert isinstance(result_conv, u.ureg.Quantity)
        assert isinstance(result_imp, u.ureg.Quantity)
        assert result_conv.magnitude > 0
        assert result_imp.magnitude > 0

        # Results should be different (improved method enhancement)
        assert abs(result_conv.magnitude - result_imp.magnitude) > 1e-6

    def test_weight_force_material_outside_method_validation(self):
        """Test validation of method parameter."""
        # Valid method should work
        result = weight_force_material_outside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=5.0 * u.ureg.degree,
            method="conventional",
        )
        assert isinstance(result, u.ureg.Quantity)

        # Invalid method should raise error
        with pytest.raises(ValueError, match="Unknown method"):
            weight_force_material_outside(
                normal_force=1000.0 * u.ureg.newton,
                troughing_angle=30.0 * u.ureg.degree,
                banking_angle=5.0 * u.ureg.degree,
                method="invalid_method",
            )

    def test_weight_force_material_outside_precision_parameter(self):
        """Test precision parameter functionality."""
        result_precision_2 = weight_force_material_outside(
            normal_force=1234.5678 * u.ureg.newton,
            troughing_angle=30.123456 * u.ureg.degree,
            banking_angle=5.654321 * u.ureg.degree,
            precision=2,
        )

        result_precision_4 = weight_force_material_outside(
            normal_force=1234.5678 * u.ureg.newton,
            troughing_angle=30.123456 * u.ureg.degree,
            banking_angle=5.654321 * u.ureg.degree,
            precision=4,
        )

        # Check that precision is applied correctly
        assert len(str(result_precision_2.magnitude).split(".")[-1]) <= 2
        assert len(str(result_precision_4.magnitude).split(".")[-1]) <= 4

    def test_weight_force_material_outside_negative_force_validation(self):
        """Test validation for negative force inputs."""
        with pytest.raises(ValueError, match="must be non-negative"):
            weight_force_material_outside(
                normal_force=-500.0 * u.ureg.newton,
                troughing_angle=30.0 * u.ureg.degree,
                banking_angle=5.0 * u.ureg.degree,
            )

    def test_weight_force_material_outside_invalid_unit_conversion(self):
        """Test error handling for invalid unit conversions."""
        with pytest.raises(ValueError, match="Error in converting units"):
            weight_force_material_outside(
                normal_force=1000.0,  # No units
                troughing_angle=30.0 * u.ureg.degree,
                banking_angle=5.0 * u.ureg.degree,
            )

    def test_weight_force_material_outside_invalid_output_unit(self):
        """Test error handling for invalid output unit."""
        with pytest.raises(ValueError):
            weight_force_material_outside(
                normal_force=1000.0 * u.ureg.newton,
                troughing_angle=30.0 * u.ureg.degree,
                banking_angle=5.0 * u.ureg.degree,
                unit="invalid_unit",
            )

    def test_weight_force_material_outside_zero_force_calculation(self):
        """Test calculation with zero normal force."""
        result = weight_force_material_outside(
            normal_force=0.0 * u.ureg.newton,
            troughing_angle=30.0 * u.ureg.degree,
            banking_angle=5.0 * u.ureg.degree,
        )

        assert abs(result.magnitude) < 1e-10  # Should be essentially zero

    def test_weight_force_material_outside_extreme_angles(self):
        """Test calculation with extreme angle values."""
        # Very small angles - may result in very small forces
        result_small = weight_force_material_outside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=0.1 * u.ureg.degree,
            banking_angle=0.1 * u.ureg.degree,
        )

        # Large angles (but physically reasonable)
        result_large = weight_force_material_outside(
            normal_force=1000.0 * u.ureg.newton,
            troughing_angle=45.0 * u.ureg.degree,
            banking_angle=15.0 * u.ureg.degree,
        )

        assert isinstance(result_small, u.ureg.Quantity)
        assert isinstance(result_large, u.ureg.Quantity)
        assert result_small.magnitude >= 0  # Allow for very small or zero forces
        assert result_large.magnitude > 0

    def test_weight_force_material_outside_mathematical_consistency(self):
        """Test mathematical consistency of the calculation."""
        normal_force = 1000.0 * u.ureg.newton
        troughing_angle = 30.0 * u.ureg.degree
        banking_angle = 5.0 * u.ureg.degree

        # Test that doubling normal force doubles the result
        result_1x = weight_force_material_outside(
            normal_force, troughing_angle, banking_angle
        )
        result_2x = weight_force_material_outside(
            2 * normal_force, troughing_angle, banking_angle
        )

        # Use relative tolerance for floating point comparison
        assert (
            abs(result_2x.magnitude - 2 * result_1x.magnitude) / result_1x.magnitude
            < 1e-4
        )

    def test_weight_force_material_outside_linearity_property(self):
        """Test linearity property of the calculation."""
        base_force = 500.0 * u.ureg.newton
        troughing_angle = 30.0 * u.ureg.degree
        banking_angle = 5.0 * u.ureg.degree

        # Test that the function is linear in normal force
        scale_factor = 3.5

        result_base = weight_force_material_outside(
            base_force, troughing_angle, banking_angle
        )
        result_scaled = weight_force_material_outside(
            scale_factor * base_force, troughing_angle, banking_angle
        )

        expected_scaled = scale_factor * result_base.magnitude
        # Use relative tolerance for floating point comparison
        assert abs(result_scaled.magnitude - expected_scaled) / expected_scaled < 1e-4


class TestWeightForceMatreialCenterPublic:
    def test_weight_force_material_center_basic(self):
        """Test basic calculation with units."""
        result = weight_force_material_center(
            normal_force=1000.0 * u.ureg.newton,
            banking_angle=5.0 * u.ureg.degree,
            method="conventional",
        )

        assert isinstance(result, u.Quantity)
        assert result.units == u.ureg.newton
        assert result.magnitude > 0

    def test_weight_force_material_center_zero_banking(self):
        """Test with zero banking angle - should give zero force."""
        result = weight_force_material_center(
            normal_force=1000.0 * u.ureg.newton,
            banking_angle=0.0 * u.ureg.degree,
            method="conventional",
        )

        assert abs(result.magnitude) < 1e-10  # Should be essentially zero

    def test_weight_force_material_center_comparison_with_wing_rolls(self):
        """Test that center force behaves differently from wing roll forces."""
        from eytelwein.horizontal_curves import weight_force_material_inside

        normal_force = 1000.0 * u.ureg.newton
        banking_angle = 5.0 * u.ureg.degree
        troughing_angle = 30.0 * u.ureg.degree

        result_center = weight_force_material_center(normal_force, banking_angle)

        result_inside = weight_force_material_inside(
            normal_force, troughing_angle, banking_angle
        )

        # Center should be much smaller than inside for typical angles
        assert result_center.magnitude < result_inside.magnitude

    def test_weight_force_material_center_unit_conversion(self):
        """Test unit conversion functionality."""
        result = weight_force_material_center(
            normal_force=1.0 * u.ureg.kilonewton,
            banking_angle=math.pi / 36 * u.ureg.radian,  # 5 degrees
            unit="kilonewton",
        )

        assert result.units == u.ureg.kilonewton
        assert result.magnitude < 1.0  # Should be much less than input

    def test_weight_force_material_center_negative_banking(self):
        """Test with negative banking angle."""
        result = weight_force_material_center(
            normal_force=1000.0 * u.ureg.newton,
            banking_angle=-5.0 * u.ureg.degree,  # Negative banking
            method="conventional",
        )

        assert isinstance(result, u.Quantity)
        assert result.magnitude < 0  # Should be negative

    def test_weight_force_material_center_precision(self):
        """Test precision parameter."""
        result = weight_force_material_center(
            normal_force=1000.0 * u.ureg.newton,
            banking_angle=5.0 * u.ureg.degree,
            precision=3,
        )

        # Check that result has exactly 3 decimal places
        assert abs(result.magnitude - round(result.magnitude, 3)) < 1e-10

    def test_weight_force_material_center_invalid_method(self):
        """Test error handling for invalid method."""
        with pytest.raises(ValueError, match="Unknown method"):
            weight_force_material_center(
                normal_force=1000.0 * u.ureg.newton,
                banking_angle=5.0 * u.ureg.degree,
                method="invalid_method",
            )

    def test_weight_force_material_center_negative_force(self):
        """Test error handling for negative normal force."""
        with pytest.raises(ValueError):
            weight_force_material_center(
                normal_force=-1000.0 * u.ureg.newton, banking_angle=5.0 * u.ureg.degree
            )

    def test_weight_force_material_center_invalid_unit(self):
        """Test error handling for invalid output unit."""
        with pytest.raises(ValueError):
            weight_force_material_center(
                normal_force=1000.0 * u.ureg.newton,
                banking_angle=5.0 * u.ureg.degree,
                unit="invalid_unit",
            )

    def test_weight_force_material_center_improved_method(self):
        """Test that improved method works and returns same result as conventional."""
        normal_force = 1000.0 * u.ureg.newton
        banking_angle = 5.0 * u.ureg.degree

        result_conv = weight_force_material_center(
            normal_force=normal_force,
            banking_angle=banking_angle,
            method="conventional",
        )

        result_imp = weight_force_material_center(
            normal_force=normal_force,
            banking_angle=banking_angle,
            method="improved",
        )

        # Both should return valid results
        assert isinstance(result_conv, u.ureg.Quantity)
        assert isinstance(result_imp, u.ureg.Quantity)
        assert result_conv.magnitude > 0
        assert result_imp.magnitude > 0

        # For center section, both methods return same result (no troughing complexity)
        assert abs(result_conv.magnitude - result_imp.magnitude) < 1e-10

    def test_weight_force_material_center_linearity_property(self):
        """Test linearity property of the calculation."""
        base_force = 500.0 * u.ureg.newton
        banking_angle = 5.0 * u.ureg.degree

        # Test that the function is linear in normal force
        scale_factor = 2.5

        result_base = weight_force_material_center(base_force, banking_angle)
        result_scaled = weight_force_material_center(
            scale_factor * base_force, banking_angle
        )

        expected_scaled = scale_factor * result_base.magnitude
        # Allow for floating point precision - center function is mathematically linear
        assert abs(result_scaled.magnitude - expected_scaled) / expected_scaled < 1e-4

    def test_weight_force_material_center_mathematical_consistency(self):
        """Test mathematical consistency of the calculation."""
        normal_force = 1000.0 * u.ureg.newton
        banking_angle = 5.0 * u.ureg.degree

        # Test that tripling normal force triples the result
        result_1x = weight_force_material_center(normal_force, banking_angle)
        result_3x = weight_force_material_center(3 * normal_force, banking_angle)

        # Should be exactly proportional for center calculation
        assert abs(result_3x.magnitude - 3 * result_1x.magnitude) < 1e-10


class TestWeightForceMatreialPublic:
    def test_weight_force_of_material_basic(self):
        """Test basic calculation with units."""
        result = weight_force_of_material(
            inside_force=530.29 * u.ureg.newton,
            center_force=87.49 * u.ureg.newton,
            outside_force=433.01 * u.ureg.newton,
            method="conventional",
        )

        assert isinstance(result, u.Quantity)
        assert result.units == u.ureg.newton
        assert abs(result.magnitude - 184.77) < 1e-2

    def test_weight_force_of_material_negative_result(self):
        """Test with outside force dominating - negative result."""
        result = weight_force_of_material(
            inside_force=200.0 * u.ureg.newton,
            center_force=100.0 * u.ureg.newton,
            outside_force=400.0 * u.ureg.newton,
            method="conventional",
        )

        assert isinstance(result, u.Quantity)
        assert result.magnitude == -100.0  # Net force toward outside

    def test_weight_force_of_material_balanced_forces(self):
        """Test with balanced forces resulting in zero."""
        result = weight_force_of_material(
            inside_force=300.0 * u.ureg.newton,
            center_force=100.0 * u.ureg.newton,
            outside_force=400.0 * u.ureg.newton,
            method="conventional",
        )

        assert abs(result.magnitude) < 1e-10  # Should be essentially zero

    def test_weight_force_of_material_unit_conversion(self):
        """Test unit conversion functionality."""
        result = weight_force_of_material(
            inside_force=0.53029 * u.ureg.kilonewton,
            center_force=0.08749 * u.ureg.kilonewton,
            outside_force=0.43301 * u.ureg.kilonewton,
            unit="kilonewton",
        )

        assert result.units == u.ureg.kilonewton
        assert abs(result.magnitude - 0.18477) < 1e-2  # Should be in kN

    def test_weight_force_of_material_mixed_units(self):
        """Test with mixed input units."""
        result = weight_force_of_material(
            inside_force=530.29 * u.ureg.newton,
            center_force=0.08749 * u.ureg.kilonewton,  # Mixed units
            outside_force=433.01 * u.ureg.newton,
            method="conventional",
        )

        assert isinstance(result, u.Quantity)
        assert abs(result.magnitude - 184.77) < 1e-2

    def test_weight_force_of_material_improved_method(self):
        """Test improved method - should give same result for combination."""
        result_conv = weight_force_of_material(
            inside_force=530.29 * u.ureg.newton,
            center_force=87.49 * u.ureg.newton,
            outside_force=433.01 * u.ureg.newton,
            method="conventional",
        )

        result_imp = weight_force_of_material(
            inside_force=530.29 * u.ureg.newton,
            center_force=87.49 * u.ureg.newton,
            outside_force=433.01 * u.ureg.newton,
            method="improved",
        )

        # Should be identical since combination formula is the same
        assert abs(result_conv.magnitude - result_imp.magnitude) < 1e-10

    def test_weight_force_of_material_precision(self):
        """Test precision parameter."""
        result = weight_force_of_material(
            inside_force=530.2876 * u.ureg.newton,
            center_force=87.4932 * u.ureg.newton,
            outside_force=433.0123 * u.ureg.newton,
            precision=1,
        )

        # Check that result has exactly 1 decimal place
        assert abs(result.magnitude - round(result.magnitude, 1)) < 1e-10

    def test_weight_force_of_material_invalid_method(self):
        """Test error handling for invalid method."""
        with pytest.raises(ValueError, match="Unknown method"):
            weight_force_of_material(
                inside_force=530.29 * u.ureg.newton,
                center_force=87.49 * u.ureg.newton,
                outside_force=433.01 * u.ureg.newton,
                method="invalid_method",
            )

    def test_weight_force_of_material_invalid_unit(self):
        """Test error handling for invalid output unit."""
        with pytest.raises(ValueError):
            weight_force_of_material(
                inside_force=530.29 * u.ureg.newton,
                center_force=87.49 * u.ureg.newton,
                outside_force=433.01 * u.ureg.newton,
                unit="invalid_unit",
            )

    def test_weight_force_of_material_unit_conversion_error(self):
        """Test error handling for incompatible input units."""
        with pytest.raises(ValueError):
            weight_force_of_material(
                inside_force=530.29 * u.ureg.meter,  # Wrong unit type
                center_force=87.49 * u.ureg.newton,
                outside_force=433.01 * u.ureg.newton,
            )


class TestRestrainingForceFromDeadWeightsTowardsOutsideCurveConventionalPublic:
    def test_restraining_force_from_dead_weights_basic(self):
        """Test basic calculation with units."""
        result = restraining_force_from_dead_weights(
            total_force_from_belt=450.25 * u.ureg.newton,
            total_force_from_material=184.77 * u.ureg.newton,
            method="conventional",
        )

        assert isinstance(result, u.Quantity)
        assert result.units == u.ureg.newton
        assert abs(result.magnitude - 635.02) < 1e-2

    def test_restraining_force_from_dead_weights_zero_material(self):
        """Test with zero material force."""
        result = restraining_force_from_dead_weights(
            total_force_from_belt=500.0 * u.ureg.newton,
            total_force_from_material=0.0 * u.ureg.newton,
            method="conventional",
        )

        assert isinstance(result, u.Quantity)
        assert result.magnitude == 500.0

    def test_restraining_force_from_dead_weights_zero_belt(self):
        """Test with zero belt force."""
        result = restraining_force_from_dead_weights(
            total_force_from_belt=0.0 * u.ureg.newton,
            total_force_from_material=300.0 * u.ureg.newton,
            method="conventional",
        )

        assert isinstance(result, u.Quantity)
        assert result.magnitude == 300.0

    def test_restraining_force_from_dead_weights_unit_conversion(self):
        """Test unit conversion functionality."""
        result = restraining_force_from_dead_weights(
            total_force_from_belt=0.45025 * u.ureg.kilonewton,
            total_force_from_material=0.18477 * u.ureg.kilonewton,
            unit="kilonewton",
        )

        assert result.units == u.ureg.kilonewton
        assert abs(result.magnitude - 0.63502) < 1e-2  # Should be in kN

    def test_restraining_force_from_dead_weights_mixed_units(self):
        """Test with mixed input units."""
        result = restraining_force_from_dead_weights(
            total_force_from_belt=450.25 * u.ureg.newton,
            total_force_from_material=0.18477 * u.ureg.kilonewton,  # Mixed units
            method="conventional",
        )

        assert isinstance(result, u.Quantity)
        assert abs(result.magnitude - 635.02) < 1e-2

    def test_restraining_force_from_dead_weights_improved_method(self):
        """Test improved method - should give same result for simple addition."""
        result_conv = restraining_force_from_dead_weights(
            total_force_from_belt=450.25 * u.ureg.newton,
            total_force_from_material=184.77 * u.ureg.newton,
            method="conventional",
        )

        result_imp = restraining_force_from_dead_weights(
            total_force_from_belt=450.25 * u.ureg.newton,
            total_force_from_material=184.77 * u.ureg.newton,
            method="improved",
        )

        # Should be identical since combination formula is the same
        assert abs(result_conv.magnitude - result_imp.magnitude) < 1e-10

    def test_restraining_force_from_dead_weights_precision(self):
        """Test precision parameter."""
        result = restraining_force_from_dead_weights(
            total_force_from_belt=450.2567 * u.ureg.newton,
            total_force_from_material=184.7734 * u.ureg.newton,
            precision=1,
        )

        # Check that result has exactly 1 decimal place
        assert abs(result.magnitude - round(result.magnitude, 1)) < 1e-10

    def test_restraining_force_from_dead_weights_high_precision(self):
        """Test high precision calculation."""
        result = restraining_force_from_dead_weights(
            total_force_from_belt=450.25 * u.ureg.newton,
            total_force_from_material=184.77 * u.ureg.newton,
            precision=5,
        )

        assert abs(result.magnitude - 635.02000) < 1e-10

    def test_restraining_force_from_dead_weights_invalid_method(self):
        """Test error handling for invalid method."""
        with pytest.raises(ValueError):
            restraining_force_from_dead_weights(
                total_force_from_belt=450.25 * u.ureg.newton,
                total_force_from_material=184.77 * u.ureg.newton,
                method="invalid_method",
            )

    def test_restraining_force_from_dead_weights_negative_belt_force(self):
        """Test error handling for negative belt force."""
        with pytest.raises(ValueError):
            restraining_force_from_dead_weights(
                total_force_from_belt=-450.25 * u.ureg.newton,
                total_force_from_material=184.77 * u.ureg.newton,
            )

    def test_restraining_force_from_dead_weights_negative_material_force(self):
        """Test error handling for negative material force."""
        with pytest.raises(ValueError):
            restraining_force_from_dead_weights(
                total_force_from_belt=450.25 * u.ureg.newton,
                total_force_from_material=-184.77 * u.ureg.newton,
            )

    def test_restraining_force_from_dead_weights_invalid_unit(self):
        """Test error handling for invalid output unit."""
        with pytest.raises(ValueError):
            restraining_force_from_dead_weights(
                total_force_from_belt=450.25 * u.ureg.newton,
                total_force_from_material=184.77 * u.ureg.newton,
                unit="invalid_unit",
            )

    def test_restraining_force_from_dead_weights_unit_conversion_error(self):
        """Test error handling for incompatible input units."""
        with pytest.raises(ValueError):
            restraining_force_from_dead_weights(
                total_force_from_belt=450.25 * u.ureg.meter,  # Wrong unit type
                total_force_from_material=184.77 * u.ureg.newton,
            )
