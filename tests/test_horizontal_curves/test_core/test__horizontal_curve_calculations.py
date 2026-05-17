"""
Tests for private horizontal curve calculation functions.

This module tests the private implementation functions without unit handling,
focusing on the core mathematical calculations and vectorization.
"""

import math
import pytest

from eytelwein.horizontal_curves.core._horizontal_curve_calculations import (
    _force_component_towards_inside_curve_from_belt_tension,
    _restraining_force_from_dead_weights_towards_outside_curve_conventional,
    _restraining_force_from_tilted_idlers_towards_outside_curve_improved,
    _tilted_idler_friction_force_center_conventional,
    _restraining_force_from_tilted_idlers_towards_outside_curve_conventional,
    _tilted_idler_friction_force_center_improved,
    _tilted_idler_friction_force_inside_conventional,
    _tilted_idler_friction_force_inside_improved,
    _tilted_idler_friction_force_outside_conventional,
    _tilted_idler_friction_force_outside_improved,
    _weight_force_belt_inside_conventional,
    _weight_force_belt_outside_conventional,
    _weight_force_belt_center_conventional,
    _weight_force_material_center_conventional,
    _weight_force_material_outside_conventional,
    _weight_force_of_belt_conventional,
    _weight_force_belt_inside_improved,
    _weight_force_belt_outside_improved,
    _weight_force_belt_center_improved,
    _weight_force_of_belt_improved,
    _weight_force_material_inside_conventional,
    _weight_force_of_material_conventional,
)


class TestPrivateForceFunctions:
    """Test private calculation functions without unit handling."""

    def test_basic_calculation(self):
        """Test basic force calculation with typical values."""
        belt_tension = 5000.0  # N
        idler_spacing = 1.2  # m
        curve_radius = 50.0  # m

        result = _force_component_towards_inside_curve_from_belt_tension(
            belt_tension, idler_spacing, curve_radius
        )

        expected = (
            belt_tension * idler_spacing / curve_radius
        )  # 5000 * 1.2 / 50 = 120 N
        assert result == pytest.approx(expected, rel=1e-10)
        assert result == pytest.approx(120.0, rel=1e-10)

    def test_different_parameters(self):
        """Test with different parameter combinations."""
        # Test case 1: Higher tension
        result1 = _force_component_towards_inside_curve_from_belt_tension(
            10000.0, 1.0, 100.0
        )
        assert result1 == pytest.approx(100.0, rel=1e-10)

        # Test case 2: Smaller radius (tighter curve)
        result2 = _force_component_towards_inside_curve_from_belt_tension(
            3000.0, 1.5, 25.0
        )
        assert result2 == pytest.approx(180.0, rel=1e-10)

        # Test case 3: Larger spacing
        result3 = _force_component_towards_inside_curve_from_belt_tension(
            4000.0, 2.0, 80.0
        )
        assert result3 == pytest.approx(100.0, rel=1e-10)

    def test_edge_cases(self):
        """Test edge cases for private function."""
        # Very small values
        result_small = _force_component_towards_inside_curve_from_belt_tension(
            0.001, 0.001, 0.1
        )
        assert result_small == pytest.approx(0.00001, rel=1e-10)

        # Very large values
        result_large = _force_component_towards_inside_curve_from_belt_tension(
            1e6, 10.0, 1000.0
        )
        assert result_large == pytest.approx(10000.0, rel=1e-10)

        # Zero tension
        result_zero = _force_component_towards_inside_curve_from_belt_tension(
            0.0, 1.0, 50.0
        )
        assert result_zero == pytest.approx(0.0, rel=1e-10)


class TestWeightForceBeltInside:
    """Test private weight force calculation functions."""

    def test_basic_calculation(self):
        """Test basic weight force calculation with typical values."""
        total_force = 10000.0  # N
        inclination = 0.1  # rad (≈5.7°)
        belt_width = 1.2  # m
        troughing = 0.349  # rad (≈20°)
        banking = 0.087  # rad (≈5°)
        inside_width = 0.4  # m

        result = _weight_force_belt_inside_conventional(
            total_force, inclination, belt_width, troughing, banking, inside_width
        )

        # Expected calculation verification
        expected = (
            total_force
            * math.cos(inclination)
            * (inside_width / belt_width)
            * math.sin(troughing + banking)
            * math.cos(troughing)
        )
        assert result == pytest.approx(expected, rel=1e-10)

    def test_zero_banking_angle(self):
        """Test with zero banking angle."""
        result = _weight_force_belt_inside_conventional(
            5000.0, 0.0, 1.0, 0.349, 0.0, 0.3
        )
        # Should still produce valid result
        assert result > 0

    def test_zero_inclination(self):
        """Test with horizontal belt (zero inclination)."""
        result = _weight_force_belt_inside_conventional(
            8000.0, 0.0, 1.5, 0.262, 0.1, 0.5
        )
        # cos(0) = 1, so should get full geometric effect
        expected = 8000.0 * (0.5 / 1.5) * math.sin(0.262 + 0.1) * math.cos(0.262)
        assert result == pytest.approx(expected, rel=1e-10)

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Very small angles
        result_small = _weight_force_belt_inside_conventional(
            1000.0, 0.001, 1.0, 0.01, 0.001, 0.33
        )
        assert result_small > 0

        # Large force values
        result_large = _weight_force_belt_inside_conventional(
            1e6, 0.1, 2.0, 0.349, 0.087, 0.6
        )
        assert result_large > 0


class TestWeightForceBeltOutside:
    """Test private weight force outside function."""

    def test_basic_calculation(self):
        """Test basic weight force calculation for outside wing roll."""
        total_force = 1000.0  # N
        inclination = 0.1  # radians (≈5.7°)
        belt_width = 1.2  # m
        troughing = math.radians(20)  # 20° in radians
        banking = math.radians(5)  # 5° in radians
        outside_width = 0.4  # m

        result = _weight_force_belt_outside_conventional(
            total_force, inclination, belt_width, troughing, banking, outside_width
        )

        # Expected calculation:
        # cos(0.1) * (0.4/1.2) * sin(20° - 5°) * cos(20°) * 1000
        expected = (
            math.cos(inclination)
            * (outside_width / belt_width)
            * math.sin(troughing - banking)
            * math.cos(troughing)
            * total_force
        )

        assert abs(result - expected) < 1e-10

    def test_zero_banking_angle(self):
        """Test calculation with zero banking angle."""
        total_force = 1000.0
        inclination = 0.0
        belt_width = 1.0
        troughing = math.radians(20)
        banking = 0.0  # No banking
        outside_width = 0.3

        result = _weight_force_belt_outside_conventional(
            total_force, inclination, belt_width, troughing, banking, outside_width
        )

        # With zero banking, should equal sin(troughing) * cos(troughing) * width_ratio
        expected = (
            math.cos(inclination)
            * (outside_width / belt_width)
            * math.sin(troughing)
            * math.cos(troughing)
            * total_force
        )

        assert abs(result - expected) < 1e-10

    def test_zero_inclination(self):
        """Test calculation with zero inclination."""
        total_force = 1000.0
        inclination = 0.0  # Horizontal belt
        belt_width = 1.0
        troughing = math.radians(20)
        banking = math.radians(5)
        outside_width = 0.3

        result = _weight_force_belt_outside_conventional(
            total_force, inclination, belt_width, troughing, banking, outside_width
        )

        # cos(0) = 1, so inclination factor should be 1
        expected = (
            1.0
            * (outside_width / belt_width)
            * math.sin(troughing - banking)
            * math.cos(troughing)
            * total_force
        )

        assert abs(result - expected) < 1e-10

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with very small force
        result = _weight_force_belt_outside_conventional(0.001, 0.0, 1.0, 0.0, 0.0, 0.5)
        assert result >= 0

        # Test with maximum width ratio
        result = _weight_force_belt_outside_conventional(
            1000.0, 0.0, 1.0, 0.0, 0.0, 1.0
        )
        assert result >= 0

        # Test with zero outside width
        result = _weight_force_belt_outside_conventional(
            1000.0, 0.0, 1.0, 0.0, 0.0, 0.0
        )
        assert result == 0.0


class TestWeightForceBeltCenterPrivate:
    """Test private weight force center function."""

    def test_basic_calculation(self):
        """Test basic weight force calculation for center section."""
        total_force = 1000.0  # N
        inclination = 0.1  # radians (≈5.7°)
        belt_width = 1.2  # m
        banking = math.radians(5)  # 5° in radians
        center_width = 0.4  # m

        result = _weight_force_belt_center_conventional(
            total_force, inclination, belt_width, banking, center_width
        )

        # Expected calculation:
        # cos(0.1) * (0.4/1.2) * sin(5°) * 1000
        expected = (
            math.cos(inclination)
            * (center_width / belt_width)
            * math.sin(banking)
            * total_force
        )

        assert abs(result - expected) < 1e-10

    def test_zero_banking_angle(self):
        """Test calculation with zero banking angle."""
        total_force = 1000.0
        inclination = 0.0
        belt_width = 1.0
        banking = 0.0  # No banking
        center_width = 0.3

        result = _weight_force_belt_center_conventional(
            total_force, inclination, belt_width, banking, center_width
        )

        # With zero banking, sin(0) = 0, so result should be 0
        assert result == 0.0

    def test_zero_inclination(self):
        """Test calculation with zero inclination."""
        total_force = 1000.0
        inclination = 0.0  # Horizontal belt
        belt_width = 1.0
        banking = math.radians(10)
        center_width = 0.3

        result = _weight_force_belt_center_conventional(
            total_force, inclination, belt_width, banking, center_width
        )

        # cos(0) = 1, so inclination factor should be 1
        expected = 1.0 * (center_width / belt_width) * math.sin(banking) * total_force

        assert abs(result - expected) < 1e-10

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with very small force
        result = _weight_force_belt_center_conventional(0.001, 0.0, 1.0, 0.1, 0.5)
        assert result >= 0

        # Test with maximum width ratio
        result = _weight_force_belt_center_conventional(1000.0, 0.0, 1.0, 0.1, 1.0)
        assert result >= 0

        # Test with zero center width
        result = _weight_force_belt_center_conventional(1000.0, 0.0, 1.0, 0.1, 0.0)
        assert result == 0.0

    def test_publication_data_verification(self):
        """Test calculation against publication data."""
        # Using specific publication data values
        total_force = 156.71475  # N
        inclination = math.radians(0)  # degrees
        belt_width = 0.8  # m (800 mm)
        banking = math.radians(1.46)  # degrees
        center_width = 0.315  # m

        result = _weight_force_belt_center_conventional(
            total_force, inclination, belt_width, banking, center_width
        )

        # Expected result: 1.57222125714098
        expected = 1.57222125714098
        assert abs(result - expected) < 1e-10


class TestWeightForceOfBeltPrivate:
    """Test private weight force of belt function."""

    def test_basic_calculation(self):
        """Test basic net weight force calculation."""
        inside_force = 10.0  # N
        center_force = 2.0  # N
        outside_force = 5.0  # N

        result = _weight_force_of_belt_conventional(
            inside_force, center_force, outside_force
        )

        # Expected: 10.0 + 2.0 - 5.0 = 7.0
        expected = 7.0
        assert abs(result - expected) < 1e-10

    def test_publication_data_verification(self):
        """Test calculation against publication data."""
        # Using the publication data from the individual force components
        # From our previous tests with corrected widths to match public test

        # Calculate individual forces using publication data
        total_force = 156.71475  # N
        inclination = math.radians(0)  # degrees
        belt_width = 0.8  # m (800 mm)
        banking = math.radians(1.46)  # degrees
        troughing = math.radians(30)  # degrees
        section_width = 0.315  # m (center width)
        outside_width = 0.1825  # m (corrected outside width)
        inside_width = 0.3025  # m (corrected inside width)

        inside_force = _weight_force_belt_inside_conventional(
            total_force, inclination, belt_width, troughing, banking, inside_width
        )
        center_force = _weight_force_belt_center_conventional(
            total_force, inclination, belt_width, banking, section_width
        )
        outside_force = _weight_force_belt_outside_conventional(
            total_force, inclination, belt_width, troughing, banking, outside_width
        )

        result = _weight_force_of_belt_conventional(
            inside_force, center_force, outside_force
        )

        # Expected result: 13.5633795467688 N
        expected = 13.5633795467688
        assert abs(result - expected) < 1e-10

    def test_zero_forces(self):
        """Test calculation with zero forces."""
        result = _weight_force_of_belt_conventional(0.0, 0.0, 0.0)
        assert result == 0.0

    def test_equal_inside_outside_forces(self):
        """Test calculation when inside and outside forces are equal."""
        inside_force = 10.0
        center_force = 3.0
        outside_force = 10.0  # Equal to inside

        result = _weight_force_of_belt_conventional(
            inside_force, center_force, outside_force
        )

        # Expected: 10.0 + 3.0 - 10.0 = 3.0 (only center force remains)
        expected = 3.0
        assert abs(result - expected) < 1e-10

    def test_negative_result(self):
        """Test calculation that results in negative net force."""
        inside_force = 5.0
        center_force = 1.0
        outside_force = 10.0  # Greater than inside + center

        result = _weight_force_of_belt_conventional(
            inside_force, center_force, outside_force
        )

        # Expected: 5.0 + 1.0 - 10.0 = -4.0
        expected = -4.0
        assert abs(result - expected) < 1e-10

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with very small forces
        result = _weight_force_of_belt_conventional(0.001, 0.0005, 0.0008)
        assert abs(result - 0.0007) < 1e-10

        # Test with large forces
        result = _weight_force_of_belt_conventional(10000.0, 1000.0, 8000.0)
        assert abs(result - 3000.0) < 1e-10


class TestWeightForceBeltInsideImproved:
    """Test improved weight force inside function."""

    def test_publication_data_verification(self):
        """Test with publication data - Grimmer & Kessler (1987) Teil II."""
        # Publication data
        total_weight_force_belt = 156.71475  # N
        inclination_angle = math.radians(0)  # degrees
        wing_roll_load_factor = 1.1  # Load factor for improved method
        belt_width = 0.8  # m (800 mm)
        troughing_angle = math.radians(30)  # degrees
        banking_angle = math.radians(1.46)  # degrees
        belt_width_on_inside_wing_roll = 0.3025  # m

        result = _weight_force_belt_inside_improved(
            total_weight_force_belt,
            inclination_angle,
            wing_roll_load_factor,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
        )

        expected = 34.0194976531535
        assert result == pytest.approx(expected, rel=1e-10)

    def test_basic_calculation(self):
        """Test basic weight force calculation with typical values."""
        total_force = 10000.0  # N
        inclination = 0.1  # rad (≈5.7°)
        load_factor = 1.5  # Load factor
        belt_width = 1.2  # m
        troughing = 0.349  # rad (≈20°)
        banking = 0.087  # rad (≈5°)
        inside_width = 0.4  # m

        result = _weight_force_belt_inside_improved(
            total_force,
            inclination,
            load_factor,
            belt_width,
            troughing,
            banking,
            inside_width,
        )

        # Expected calculation verification
        expected = (
            total_force
            * math.cos(inclination)
            * (load_factor * inside_width / belt_width)
            * math.sin(troughing + banking)
        )
        assert result == pytest.approx(expected, rel=1e-10)

    def test_load_factor_scaling(self):
        """Test that load factor scales the result linearly."""
        total_force = 5000.0
        inclination = 0.0
        belt_width = 1.0
        troughing = 0.349
        banking = 0.1
        inside_width = 0.3

        # Test with different load factors
        result_1x = _weight_force_belt_inside_improved(
            total_force, inclination, 1.0, belt_width, troughing, banking, inside_width
        )
        result_15x = _weight_force_belt_inside_improved(
            total_force, inclination, 1.5, belt_width, troughing, banking, inside_width
        )
        result_2x = _weight_force_belt_inside_improved(
            total_force, inclination, 2.0, belt_width, troughing, banking, inside_width
        )

        # Should scale linearly
        assert result_15x == pytest.approx(result_1x * 1.5, rel=1e-10)
        assert result_2x == pytest.approx(result_1x * 2.0, rel=1e-10)

    def test_zero_banking_angle(self):
        """Test with zero banking angle."""
        result = _weight_force_belt_inside_improved(
            5000.0, 0.0, 1.2, 1.0, 0.349, 0.0, 0.3
        )
        # Should still produce valid result
        assert result > 0

    def test_zero_inclination(self):
        """Test with horizontal belt (zero inclination)."""
        result = _weight_force_belt_inside_improved(
            8000.0, 0.0, 1.3, 1.5, 0.262, 0.1, 0.5
        )
        # cos(0) = 1, so should get full geometric effect
        expected = 8000.0 * (1.3 * 0.5 / 1.5) * math.sin(0.262 + 0.1)
        assert result == pytest.approx(expected, rel=1e-10)

    def test_zero_load_factor(self):
        """Test with zero load factor."""
        result = _weight_force_belt_inside_improved(
            1000.0, 0.0, 0.0, 1.0, 0.349, 0.1, 0.3
        )
        assert result == 0.0

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Very small angles
        result_small = _weight_force_belt_inside_improved(
            1000.0, 0.001, 1.1, 1.0, 0.01, 0.001, 0.33
        )
        assert result_small > 0

        # Large force values
        result_large = _weight_force_belt_inside_improved(
            1e6, 0.1, 1.5, 2.0, 0.349, 0.087, 0.6
        )
        assert result_large > 0

        # Maximum realistic load factor
        result_max_factor = _weight_force_belt_inside_improved(
            1000.0, 0.0, 2.0, 1.0, 0.349, 0.1, 0.3
        )
        assert result_max_factor > 0

    def test_comparison_with_conventional(self):
        """Test relationship with conventional method."""
        total_force = 1000.0
        inclination = 0.0
        belt_width = 1.0
        troughing = 0.349
        banking = 0.1
        inside_width = 0.3

        # Conventional result
        conventional = _weight_force_belt_inside_conventional(
            total_force, inclination, belt_width, troughing, banking, inside_width
        )

        # Improved with load factor 1.0 and multiplied by cos(troughing) should be similar
        improved_1x = _weight_force_belt_inside_improved(
            total_force, inclination, 1.0, belt_width, troughing, banking, inside_width
        )

        # The improved method without cos(troughing), so multiply conventional by 1/cos(troughing)
        expected_relationship = conventional / math.cos(troughing)
        assert improved_1x == pytest.approx(expected_relationship, rel=1e-10)


class TestWeightForceBeltOutsideImproved:
    """Test improved weight force outside function."""

    def test_publication_data_verification(self):
        """Test with publication data - Grimmer & Kessler (1987) Teil II."""
        # Publication data
        total_weight_force_belt = 156.71475  # N
        inclination_angle = math.radians(0)  # degrees
        wing_roll_load_factor = 1.1  # Load factor for improved method
        belt_width = 0.8  # m (800 mm)
        troughing_angle = math.radians(30)  # degrees
        banking_angle = math.radians(1.46)  # degrees
        belt_width_on_outside_wing_roll = 0.1825  # m

        result = _weight_force_belt_outside_improved(
            total_weight_force_belt,
            inclination_angle,
            wing_roll_load_factor,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_outside_wing_roll,
        )

        expected = 18.7886810270471
        assert result == pytest.approx(expected, rel=1e-10)

    def test_basic_calculation(self):
        """Test basic weight force calculation with typical values."""
        total_force = 10000.0  # N
        inclination = 0.1  # rad (≈5.7°)
        wing_load_factor = 1.5  # Wing load factor
        belt_width = 1.2  # m
        troughing = 0.349  # rad (≈20°)
        banking = 0.087  # rad (≈5°)
        outside_width = 0.6  # m

        result = _weight_force_belt_outside_improved(
            total_force,
            inclination,
            wing_load_factor,
            belt_width,
            troughing,
            banking,
            outside_width,
        )

        # Expected calculation verification
        expected = (
            total_force
            * math.cos(inclination)
            * (wing_load_factor * outside_width / belt_width)
            * math.sin(troughing - banking)
        )
        assert result == pytest.approx(expected, rel=1e-10)

    def test_wing_load_factor_scaling(self):
        """Test that wing load factor scales the result linearly."""
        total_force = 5000.0
        inclination = 0.0
        belt_width = 1.0
        troughing = 0.349
        banking = 0.1
        outside_width = 0.4

        # Test with different wing load factors
        result_1x = _weight_force_belt_outside_improved(
            total_force, inclination, 1.0, belt_width, troughing, banking, outside_width
        )
        result_15x = _weight_force_belt_outside_improved(
            total_force, inclination, 1.5, belt_width, troughing, banking, outside_width
        )
        result_2x = _weight_force_belt_outside_improved(
            total_force, inclination, 2.0, belt_width, troughing, banking, outside_width
        )

        # Should scale linearly
        assert result_15x == pytest.approx(result_1x * 1.5, rel=1e-10)
        assert result_2x == pytest.approx(result_1x * 2.0, rel=1e-10)

    def test_zero_banking_angle(self):
        """Test with zero banking angle."""
        result = _weight_force_belt_outside_improved(
            5000.0, 0.0, 1.2, 1.0, 0.349, 0.0, 0.4
        )
        # Banking = 0, so sin(troughing - 0) = sin(troughing)
        expected = 5000.0 * (1.2 * 0.4 / 1.0) * math.sin(0.349)
        assert result == pytest.approx(expected, rel=1e-10)

    def test_zero_inclination(self):
        """Test with horizontal belt (zero inclination)."""
        result = _weight_force_belt_outside_improved(
            8000.0, 0.0, 1.3, 1.5, 0.262, 0.1, 0.6
        )
        # cos(0) = 1, so should get full geometric effect
        expected = 8000.0 * (1.3 * 0.6 / 1.5) * math.sin(0.262 - 0.1)
        assert result == pytest.approx(expected, rel=1e-10)

    def test_zero_wing_load_factor(self):
        """Test with zero wing load factor."""
        result = _weight_force_belt_outside_improved(
            1000.0, 0.0, 0.0, 1.0, 0.349, 0.1, 0.4
        )
        assert result == 0.0

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Very small angles
        result_small = _weight_force_belt_outside_improved(
            1000.0, 0.001, 1.1, 1.0, 0.01, 0.001, 0.45
        )
        assert result_small > 0

        # Large force values
        result_large = _weight_force_belt_outside_improved(
            1e6, 0.1, 1.5, 2.0, 0.349, 0.087, 0.8
        )
        assert result_large > 0

        # Maximum realistic wing load factor
        result_max_factor = _weight_force_belt_outside_improved(
            1000.0, 0.0, 2.0, 1.0, 0.349, 0.1, 0.4
        )
        assert result_max_factor > 0

    def test_banking_angle_effects(self):
        """Test effects of different banking angles."""
        total_force = 1000.0
        inclination = 0.0
        wing_load_factor = 1.2
        belt_width = 1.0
        troughing = 0.349
        outside_width = 0.4

        # Positive banking
        result_pos = _weight_force_belt_outside_improved(
            total_force,
            inclination,
            wing_load_factor,
            belt_width,
            troughing,
            0.1,
            outside_width,
        )

        # Negative banking
        result_neg = _weight_force_belt_outside_improved(
            total_force,
            inclination,
            wing_load_factor,
            belt_width,
            troughing,
            -0.1,
            outside_width,
        )

        # Should be different due to sin(troughing ± banking)
        assert result_pos != result_neg

    def test_comparison_with_conventional(self):
        """Test relationship with conventional method."""
        total_force = 1000.0
        inclination = 0.0
        belt_width = 1.0
        troughing = 0.349
        banking = 0.1
        outside_width = 0.4

        # Conventional result
        conventional = _weight_force_belt_outside_conventional(
            total_force, inclination, belt_width, troughing, banking, outside_width
        )

        # Improved with wing load factor 1.0 and multiplied by cos(troughing) should be similar
        improved_1x = _weight_force_belt_outside_improved(
            total_force, inclination, 1.0, belt_width, troughing, banking, outside_width
        )

        # The improved method without cos(troughing), so multiply conventional by 1/cos(troughing)
        expected_relationship = conventional / math.cos(troughing)
        assert improved_1x == pytest.approx(expected_relationship, rel=1e-10)


class TestWeightForceBeltCenterImproved:
    """Test improved weight force center function."""

    def test_publication_data_verification(self):
        """Test with publication data - Grimmer & Kessler (1987) Teil II."""
        # Publication data
        total_weight_force_belt = 156.71475  # N
        inclination_angle = math.radians(0)  # degrees
        center_roll_load_factor = 0.9  # Load factor for improved method
        belt_width = 0.8  # m (800 mm)
        banking_angle = math.radians(1.46)  # degrees
        belt_width_on_center_wing_roll = 0.315  # m

        result = _weight_force_belt_center_improved(
            total_weight_force_belt,
            inclination_angle,
            center_roll_load_factor,
            belt_width,
            banking_angle,
            belt_width_on_center_wing_roll,
        )

        expected = 1.41499913142688
        assert result == pytest.approx(expected, rel=1e-10)

    def test_basic_calculation(self):
        """Test basic weight force calculation with typical values."""
        total_force = 10000.0  # N
        inclination = 0.1  # rad (≈5.7°)
        center_load_factor = 0.8  # Center load factor
        belt_width = 1.2  # m
        banking = 0.087  # rad (≈5°)
        center_width = 0.4  # m

        result = _weight_force_belt_center_improved(
            total_force,
            inclination,
            center_load_factor,
            belt_width,
            banking,
            center_width,
        )

        # Expected calculation verification
        expected = (
            total_force
            * math.cos(inclination)
            * (center_load_factor * center_width / belt_width)
            * math.sin(banking)
        )
        assert result == pytest.approx(expected, rel=1e-10)

    def test_center_load_factor_scaling(self):
        """Test that center load factor scales the result linearly."""
        total_force = 5000.0
        inclination = 0.0
        belt_width = 1.0
        banking = 0.1
        center_width = 0.4

        # Test with different center load factors
        result_05x = _weight_force_belt_center_improved(
            total_force, inclination, 0.5, belt_width, banking, center_width
        )
        result_08x = _weight_force_belt_center_improved(
            total_force, inclination, 0.8, belt_width, banking, center_width
        )
        result_1x = _weight_force_belt_center_improved(
            total_force, inclination, 1.0, belt_width, banking, center_width
        )

        # Should scale linearly
        assert result_08x == pytest.approx(result_1x * 0.8, rel=1e-10)
        assert result_05x == pytest.approx(result_1x * 0.5, rel=1e-10)

    def test_zero_banking_angle(self):
        """Test with zero banking angle."""
        result = _weight_force_belt_center_improved(5000.0, 0.0, 0.9, 1.0, 0.0, 0.4)
        # sin(0) = 0, so result should be 0
        assert result == 0.0

    def test_zero_inclination(self):
        """Test with horizontal belt (zero inclination)."""
        result = _weight_force_belt_center_improved(8000.0, 0.0, 0.9, 1.5, 0.1, 0.6)
        # cos(0) = 1, so should get full geometric effect
        expected = 8000.0 * (0.9 * 0.6 / 1.5) * math.sin(0.1)
        assert result == pytest.approx(expected, rel=1e-10)

    def test_zero_center_load_factor(self):
        """Test with zero center load factor."""
        result = _weight_force_belt_center_improved(1000.0, 0.0, 0.0, 1.0, 0.1, 0.4)
        assert result == 0.0

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Very small angles
        result_small = _weight_force_belt_center_improved(
            1000.0, 0.001, 0.9, 1.0, 0.01, 0.4
        )
        assert result_small > 0

        # Large force values
        result_large = _weight_force_belt_center_improved(
            1e6, 0.1, 0.8, 2.0, 0.087, 0.6
        )
        assert result_large > 0

        # Minimum realistic center load factor
        result_min_factor = _weight_force_belt_center_improved(
            1000.0, 0.0, 0.5, 1.0, 0.1, 0.4
        )
        assert result_min_factor > 0

    def test_banking_angle_effects(self):
        """Test effects of different banking angles."""
        total_force = 1000.0
        inclination = 0.0
        center_load_factor = 0.9
        belt_width = 1.0
        center_width = 0.4

        # Different banking angles
        result_small = _weight_force_belt_center_improved(
            total_force, inclination, center_load_factor, belt_width, 0.05, center_width
        )
        result_large = _weight_force_belt_center_improved(
            total_force, inclination, center_load_factor, belt_width, 0.15, center_width
        )

        # Larger banking should give larger result due to sin(banking)
        assert result_large > result_small

    def test_comparison_with_conventional(self):
        """Test relationship with conventional method."""
        total_force = 1000.0
        inclination = 0.0
        belt_width = 1.0
        banking = 0.1
        center_width = 0.4

        # Conventional result
        conventional = _weight_force_belt_center_conventional(
            total_force, inclination, belt_width, banking, center_width
        )

        # Improved with center load factor 1.0 should be exactly the same
        improved_1x = _weight_force_belt_center_improved(
            total_force, inclination, 1.0, belt_width, banking, center_width
        )

        # Should be identical since both methods use the same formula
        assert improved_1x == pytest.approx(conventional, rel=1e-10)


class TestWeightForceOfBeltImproved:
    """Test improved weight force of belt function."""

    def test_publication_data_verification(self):
        """Test with publication data - Grimmer & Kessler (1987) Teil II."""
        # Publication data for individual components
        total_weight_force_belt = 156.71475  # N
        inclination_angle = math.radians(0)  # degrees
        wing_roll_load_factor = 1.1  # Load factor for wing rolls
        center_roll_load_factor = 0.9  # Load factor for center roll
        belt_width = 0.8  # m (800 mm)
        troughing_angle = math.radians(30)  # degrees
        banking_angle = math.radians(1.46)  # degrees
        belt_width_on_inside_wing_roll = 0.3025  # m
        belt_width_on_outside_wing_roll = 0.1825  # m
        belt_width_on_center_wing_roll = 0.315  # m

        # Calculate individual components using improved methods
        inside_force = _weight_force_belt_inside_improved(
            total_weight_force_belt,
            inclination_angle,
            wing_roll_load_factor,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_inside_wing_roll,
        )

        center_force = _weight_force_belt_center_improved(
            total_weight_force_belt,
            inclination_angle,
            center_roll_load_factor,
            belt_width,
            banking_angle,
            belt_width_on_center_wing_roll,
        )

        outside_force = _weight_force_belt_outside_improved(
            total_weight_force_belt,
            inclination_angle,
            wing_roll_load_factor,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_outside_wing_roll,
        )

        # Calculate net force using improved method
        result = _weight_force_of_belt_improved(
            inside_force, center_force, outside_force
        )

        expected = 16.6458157575333
        assert result == pytest.approx(expected, rel=1e-10)

    def test_basic_calculation(self):
        """Test basic weight force summation with typical values."""
        inside_force = 100.0  # N
        center_force = 50.0  # N
        outside_force = 80.0  # N

        result = _weight_force_of_belt_improved(
            inside_force, center_force, outside_force
        )

        # Simple sum calculation
        expected = inside_force + center_force - outside_force
        assert result == pytest.approx(expected, rel=1e-10)

    def test_zero_forces(self):
        """Test with zero force components."""
        # All zeros
        result_all_zero = _weight_force_of_belt_improved(0.0, 0.0, 0.0)
        assert result_all_zero == 0.0

        # Zero inside force
        result_zero_inside = _weight_force_of_belt_improved(0.0, 50.0, 30.0)
        assert result_zero_inside == 20.0

        # Zero center force
        result_zero_center = _weight_force_of_belt_improved(100.0, 0.0, 30.0)
        assert result_zero_center == 70.0

        # Zero outside force
        result_zero_outside = _weight_force_of_belt_improved(100.0, 50.0, 0.0)
        assert result_zero_outside == 150.0

    def test_negative_forces(self):
        """Test with negative force values."""
        inside_force = -50.0  # N (could happen in unusual conditions)
        center_force = 100.0  # N
        outside_force = 30.0  # N

        result = _weight_force_of_belt_improved(
            inside_force, center_force, outside_force
        )
        expected = inside_force + center_force - outside_force
        assert result == pytest.approx(expected, rel=1e-10)

    def test_large_force_values(self):
        """Test with large force values."""
        inside_force = 1e6  # N
        center_force = 5e5  # N
        outside_force = 3e5  # N

        result = _weight_force_of_belt_improved(
            inside_force, center_force, outside_force
        )
        expected = inside_force + center_force - outside_force
        assert result == pytest.approx(expected, rel=1e-10)

    def test_force_balance_scenarios(self):
        """Test different force balance scenarios."""
        # Scenario 1: Outside force dominates
        result_outside_dom = _weight_force_of_belt_improved(50.0, 30.0, 100.0)
        assert result_outside_dom == -20.0  # Net force in opposite direction

        # Scenario 2: Inside force dominates
        result_inside_dom = _weight_force_of_belt_improved(200.0, 30.0, 50.0)
        assert result_inside_dom == 180.0

        # Scenario 3: Balanced forces
        result_balanced = _weight_force_of_belt_improved(100.0, 20.0, 120.0)
        assert result_balanced == 0.0

    def test_precision_with_small_differences(self):
        """Test precision with small force differences."""
        inside_force = 1000.000001  # N
        center_force = 500.000002  # N
        outside_force = 1500.000001  # N

        result = _weight_force_of_belt_improved(
            inside_force, center_force, outside_force
        )
        expected = inside_force + center_force - outside_force
        assert result == pytest.approx(expected, rel=1e-12)

    def test_comparison_with_conventional(self):
        """Test relationship with conventional method."""
        inside_force = 123.45  # N
        center_force = 67.89  # N
        outside_force = 45.67  # N

        # Conventional result
        conventional = _weight_force_of_belt_conventional(
            inside_force, center_force, outside_force
        )

        # Improved result
        improved = _weight_force_of_belt_improved(
            inside_force, center_force, outside_force
        )

        # Should be identical since both use the same formula
        assert improved == pytest.approx(conventional, rel=1e-10)

    def test_consistency_with_component_calculations(self):
        """Test consistency when using actual component force calculations."""
        # Test parameters
        total_force = 1000.0
        inclination = 0.0
        wing_load_factor = 1.2
        center_load_factor = 0.8
        belt_width = 1.0
        troughing = 0.349
        banking = 0.1
        inside_width = 0.35
        center_width = 0.3
        outside_width = 0.35

        # Calculate individual forces
        inside = _weight_force_belt_inside_improved(
            total_force,
            inclination,
            wing_load_factor,
            belt_width,
            troughing,
            banking,
            inside_width,
        )
        center = _weight_force_belt_center_improved(
            total_force,
            inclination,
            center_load_factor,
            belt_width,
            banking,
            center_width,
        )
        outside = _weight_force_belt_outside_improved(
            total_force,
            inclination,
            wing_load_factor,
            belt_width,
            troughing,
            banking,
            outside_width,
        )

        # Calculate net force
        net_force = _weight_force_of_belt_improved(inside, center, outside)

        # Verify the calculation is mathematically consistent
        expected_net = inside + center - outside
        assert net_force == pytest.approx(expected_net, rel=1e-10)


class TestTiltedIdlerFrictionForceConventional:
    """Test tilted idler friction force calculations - conventional method."""

    def test_tilted_idler_inside_conventional_publication_data(self):
        """Test tilted idler inside force calculation with publication data."""
        # Using publication data values (same geometry as belt tests)
        total_weight_force_material = 156.71475  # N (material only)
        inclination_angle = math.radians(0)  # degrees
        belt_width = 0.8  # m (800 mm)
        troughing_angle = math.radians(30)  # degrees
        banking_angle = math.radians(1.46)  # degrees
        belt_width_on_inside_wing_roll = 0.3025  # m
        friction_variation = 0.70  # placeholder for new parameter
        friction_coefficient_tilted_idler = (
            0.416183095606664  # placeholder for new parameter
        )
        normal_force_on_idler_roll = 0.0  # placeholder for new parameter

        # Expected test result from your docstring: 12.75292522
        expected_result = 12.75292522

        # This function is already implemented
        result = _tilted_idler_friction_force_inside_conventional(
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

        # Test the actual result
        assert abs(result - expected_result) < 1e-6

    def test_tilted_idler_outside_conventional_publication_data(self):
        """Test tilted idler outside force calculation with publication data."""
        # Using publication data values (same geometry as belt tests)
        total_weight_force_material = 156.71475  # N (material only)
        inclination_angle = math.radians(0)  # degrees
        belt_width = 0.8  # m (800 mm)
        troughing_angle = math.radians(30)  # degrees
        banking_angle = math.radians(1.46)  # degrees
        belt_width_on_outside_wing_roll = 0.1825  # m
        friction_variation = 0.70  # placeholder for new parameter
        friction_coefficient_tilted_idler = (
            0.216183095606664  # placeholder for new parameter
        )
        normal_force_on_idler_roll = 0.0  # placeholder for new parameter

        # Expected test result from your docstring: 4.11591981879653
        expected_result = 4.11591981879653

        result = _tilted_idler_friction_force_outside_conventional(
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

        # This assertion will be enabled once implementation is complete:
        assert abs(result - expected_result) < 1e-6

    def test_tilted_idler_center_conventional_publication_data(self):
        """Test tilted idler center force calculation with publication data."""
        # Using publication data values (same geometry as belt tests)
        total_weight_force_material = 156.71475  # N (material only)
        inclination_angle = math.radians(0)  # degrees
        troughing_angle = math.radians(30)  # degrees
        belt_width = 0.8  # m (800 mm)
        banking_angle = math.radians(1.46)  # degrees
        belt_width_on_center_wing_roll = 0.315  # m
        belt_width_on_inside_wing_roll = 0.3025  # m
        belt_width_on_outside_wing_roll = 0.1825  # m
        friction_variation = 0.70  # placeholder for new parameter
        friction_coefficient_tilted_idler = (
            0.279588668362082  # placeholder for new parameter
        )
        normal_force_on_idler_roll = 0.0  # placeholder for new parameter

        # Expected test result from your docstring: 16.77059015
        expected_result = 16.77059015

        result = _tilted_idler_friction_force_center_conventional(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_center_wing_roll,
            belt_width_on_inside_wing_roll,
            belt_width_on_outside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
        )

        # This assertion will be enabled once implementation is complete:
        assert abs(result - expected_result) < 1e-6

    def test_tilted_idler_net_force_conventional_publication_data(self):
        """Test net tilted idler force calculation with publication data."""
        # Component forces from test results
        tilted_idler_force_inside = 12.75292522
        tilted_idler_force_center = 16.77059015
        tilted_idler_force_outside = 4.115919819

        # Expected test result from your docstring: 25.40759555
        # Calculation: 12.75292522 + 16.77059015 - 4.115919819 = 25.40759555
        expected_result = 25.40759555

        # This function is already implemented (not NotImplementedError)
        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                tilted_idler_force_inside,
                tilted_idler_force_center,
                tilted_idler_force_outside,
            )
        )

        # This assertion should work now:
        assert abs(result - expected_result) < 1e-6


class TestTiltedIdlerFrictionForceConventionalNetCalculation:
    """Test private function _restraining_force_from_tilted_idlers_towards_outside_curve_conventional."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        # Component forces from test results
        weight_force_material_inside = 12.75292522
        weight_force_material_center = 16.77059015
        weight_force_material_outside = 4.115919819

        # Expected test result: 25.40759555
        # Calculation: 12.75292522 + 16.77059015 - 4.115919819 = 25.40759555
        expected_result = 25.40759555

        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                weight_force_material_inside,
                weight_force_material_center,
                weight_force_material_outside,
            )
        )

        assert result == pytest.approx(expected_result, rel=1e-10)

    def test_zero_forces(self):
        """Test calculation with zero force inputs."""
        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                0.0, 0.0, 0.0
            )
        )
        assert result == pytest.approx(0.0, abs=1e-12)

    def test_positive_forces_only(self):
        """Test calculation with only positive forces."""
        inside = 10.0
        center = 15.0
        outside = 5.0
        expected = inside + center - outside  # 10 + 15 - 5 = 20.0

        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                inside, center, outside
            )
        )
        assert result == pytest.approx(expected, rel=1e-10)

    def test_large_outside_force(self):
        """Test calculation where outside force is larger than inside + center."""
        inside = 5.0
        center = 8.0
        outside = 20.0
        expected = inside + center - outside  # 5 + 8 - 20 = -7.0

        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                inside, center, outside
            )
        )
        assert result == pytest.approx(expected, rel=1e-10)

    def test_equal_forces(self):
        """Test calculation with equal force components."""
        force_value = 10.0
        expected = force_value + force_value - force_value  # 10 + 10 - 10 = 10.0

        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                force_value, force_value, force_value
            )
        )
        assert result == pytest.approx(expected, rel=1e-10)

    def test_negative_forces(self):
        """Test calculation with negative force inputs."""
        inside = -5.0
        center = -3.0
        outside = -2.0
        expected = inside + center - outside  # -5 + (-3) - (-2) = -6.0

        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                inside, center, outside
            )
        )
        assert result == pytest.approx(expected, rel=1e-10)

    def test_mixed_sign_forces(self):
        """Test calculation with mixed positive/negative forces."""
        inside = 15.0
        center = -5.0
        outside = 8.0
        expected = inside + center - outside  # 15 + (-5) - 8 = 2.0

        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                inside, center, outside
            )
        )
        assert result == pytest.approx(expected, rel=1e-10)

    def test_very_small_forces(self):
        """Test calculation with very small force values."""
        inside = 1e-9
        center = 2e-9
        outside = 0.5e-9
        expected = inside + center - outside  # 1e-9 + 2e-9 - 0.5e-9 = 2.5e-9

        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                inside, center, outside
            )
        )
        assert result == pytest.approx(expected, rel=1e-8)

    def test_very_large_forces(self):
        """Test calculation with very large force values."""
        inside = 1e6
        center = 2e6
        outside = 0.5e6
        expected = inside + center - outside  # 1e6 + 2e6 - 0.5e6 = 2.5e6

        result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                inside, center, outside
            )
        )
        assert result == pytest.approx(expected, rel=1e-10)

    def test_mathematical_consistency(self):
        """Test mathematical consistency of the force combination."""
        # Test the commutative property for inside and center forces
        inside = 12.5
        center = 8.3
        outside = 4.1

        result1 = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                inside, center, outside
            )
        )
        result2 = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                center, inside, outside
            )
        )

        # Results should be the same due to addition being commutative
        assert result1 == pytest.approx(result2, rel=1e-12)

        # Test that doubling all forces doubles the result
        result_doubled = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_conventional(
                2 * inside, 2 * center, 2 * outside
            )
        )
        assert result_doubled == pytest.approx(2 * result1, rel=1e-10)


class TestTiltedIdlerFrictionForceOutsideConventional:
    """Test private function _tilted_idler_friction_force_outside_conventional."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        # Publication test data parameters - expected result: 4.11591981879653 N
        total_weight_force_material = 156.71475  # N
        inclination_angle = 0.0  # radians (0 degrees)
        belt_width = 0.8  # m
        troughing_angle = math.radians(30)  # 30 degrees
        banking_angle = math.radians(1.46)  # 1.46 degrees
        belt_width_on_outside_wing_roll = 0.1825  # m
        friction_variation = 0.7  # dimensionless
        friction_coefficient_tilted_idler = 0.216183095606664  # dimensionless
        normal_force_on_idler_roll = 0.0  # N

        result = _tilted_idler_friction_force_outside_conventional(
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

        # Check result against publication data
        assert result == pytest.approx(4.11591981879653, rel=1e-10)

    def test_zero_inclination_angle(self):
        """Test calculation with zero inclination angle."""
        result = _tilted_idler_friction_force_outside_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_outside_wing_roll=0.2,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=0.0,
        )

        assert result > 0
        assert isinstance(result, float)

    def test_zero_friction_variation(self):
        """Test calculation with zero friction variation."""
        result = _tilted_idler_friction_force_outside_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_outside_wing_roll=0.2,
            friction_variation=0.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=0.0,
        )

        assert result == 0.0

    def test_zero_friction_coefficient(self):
        """Test calculation with zero friction coefficient."""
        result = _tilted_idler_friction_force_outside_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_outside_wing_roll=0.2,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.0,
            normal_force_on_idler_roll=0.0,
        )

        assert result == 0.0

    def test_with_normal_force(self):
        """Test calculation with additional normal force on idler roll."""
        base_result = _tilted_idler_friction_force_outside_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_outside_wing_roll=0.2,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=0.0,
        )

        result_with_normal = _tilted_idler_friction_force_outside_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_outside_wing_roll=0.2,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=50.0,
        )

        # Result with normal force should be larger
        assert result_with_normal > base_result
        # Difference should be friction_variation * friction_coefficient * cos(troughing_angle) * normal_force
        expected_difference = 1.0 * 0.3 * math.cos(math.radians(20)) * 50.0
        assert result_with_normal - base_result == pytest.approx(
            expected_difference, rel=1e-10
        )

    def test_mathematical_consistency_linear_scaling(self):
        """Test mathematical consistency with linear scaling properties."""
        base_params = {
            "total_weight_force_material": 100.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_outside_wing_roll": 0.2,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_outside_conventional(**base_params)

        # Double material weight should roughly double the result (linear relationship)
        params_double_material = base_params.copy()
        params_double_material["total_weight_force_material"] = 200.0
        result_double_material = _tilted_idler_friction_force_outside_conventional(
            **params_double_material
        )

        assert result_double_material == pytest.approx(base_result * 2, rel=1e-10)

        # Double friction coefficient should double the result (linear relationship)
        params_double_friction = base_params.copy()
        params_double_friction["friction_coefficient_tilted_idler"] = 0.6
        result_double_friction = _tilted_idler_friction_force_outside_conventional(
            **params_double_friction
        )

        assert result_double_friction == pytest.approx(base_result * 2, rel=1e-10)

    def test_geometric_parameter_effects(self):
        """Test effects of geometric parameters on the calculation."""
        base_params = {
            "total_weight_force_material": 200.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_outside_wing_roll": 0.2,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_outside_conventional(**base_params)

        # Larger troughing angle should affect cos(troughing_angle) term
        params_larger_troughing = base_params.copy()
        params_larger_troughing["troughing_angle"] = math.radians(30)
        result_larger_troughing = _tilted_idler_friction_force_outside_conventional(
            **params_larger_troughing
        )

        # Result should be smaller due to smaller cos(30°) vs cos(20°)
        assert result_larger_troughing < base_result

        # Different belt width ratio should scale proportionally
        params_half_width_ratio = base_params.copy()
        params_half_width_ratio["belt_width_on_outside_wing_roll"] = (
            0.1  # Half the original
        )
        result_half_width = _tilted_idler_friction_force_outside_conventional(
            **params_half_width_ratio
        )

        # Result should be roughly half (due to width ratio effect)
        assert result_half_width == pytest.approx(base_result * 0.5, rel=1e-6)

    def test_inclination_angle_effects(self):
        """Test effects of inclination angle on the calculation."""
        base_params = {
            "total_weight_force_material": 200.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_outside_wing_roll": 0.2,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_outside_conventional(**base_params)

        # Inclination angle should reduce result due to cos(inclination_angle) factor
        params_inclined = base_params.copy()
        params_inclined["inclination_angle"] = math.radians(10)  # 10 degrees
        result_inclined = _tilted_idler_friction_force_outside_conventional(
            **params_inclined
        )

        # Result should be smaller due to cos(10°) < cos(0°) = 1
        assert result_inclined < base_result
        # Should be exactly cos(10°) times the base result
        assert result_inclined == pytest.approx(
            base_result * math.cos(math.radians(10)), rel=1e-10
        )

    def test_banking_angle_effects(self):
        """Test effects of banking angle on cos(troughing_angle - banking_angle) term."""
        base_params = {
            "total_weight_force_material": 200.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_outside_wing_roll": 0.2,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_outside_conventional(**base_params)

        # Zero banking angle should affect the cos(troughing_angle - banking_angle) term
        params_zero_banking = base_params.copy()
        params_zero_banking["banking_angle"] = 0.0
        result_zero_banking = _tilted_idler_friction_force_outside_conventional(
            **params_zero_banking
        )

        # Results should be different due to different cos(λ - β) values
        assert result_zero_banking != base_result

        # Larger banking angle
        params_larger_banking = base_params.copy()
        params_larger_banking["banking_angle"] = math.radians(5.0)
        result_larger_banking = _tilted_idler_friction_force_outside_conventional(
            **params_larger_banking
        )

        # Should also be different from base result
        assert result_larger_banking != base_result


class TestTiltedIdlerFrictionForceInsideConventional:
    """Test private function _tilted_idler_friction_force_inside_conventional."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        # Publication test data parameters - expected result: 12.75292522 N
        total_weight_force_material = 156.71475  # N
        inclination_angle = 0.0  # radians (0 degrees)
        belt_width = 0.8  # m
        troughing_angle = math.radians(30)  # 30 degrees
        banking_angle = math.radians(1.46)  # 1.46 degrees
        belt_width_on_inside_wing_roll = 0.3025  # m
        friction_variation = 0.7  # dimensionless
        friction_coefficient_tilted_idler = 0.416183095606664  # dimensionless
        normal_force_on_idler_roll = 0.0  # N

        result = _tilted_idler_friction_force_inside_conventional(
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

        # Check result against publication data
        assert result == pytest.approx(12.75292522, rel=1e-6)

    def test_zero_inclination_angle(self):
        """Test calculation with zero inclination angle."""
        result = _tilted_idler_friction_force_inside_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_inside_wing_roll=0.3,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=0.0,
        )

        assert result > 0
        assert isinstance(result, float)

    def test_zero_friction_variation(self):
        """Test calculation with zero friction variation."""
        result = _tilted_idler_friction_force_inside_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_inside_wing_roll=0.3,
            friction_variation=0.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=0.0,
        )

        assert result == 0.0

    def test_zero_friction_coefficient(self):
        """Test calculation with zero friction coefficient."""
        result = _tilted_idler_friction_force_inside_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_inside_wing_roll=0.3,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.0,
            normal_force_on_idler_roll=0.0,
        )

        assert result == 0.0

    def test_with_normal_force(self):
        """Test calculation with additional normal force on idler roll."""
        base_result = _tilted_idler_friction_force_inside_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_inside_wing_roll=0.3,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=0.0,
        )

        result_with_normal = _tilted_idler_friction_force_inside_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_inside_wing_roll=0.3,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=50.0,
        )

        # Result with normal force should be larger
        assert result_with_normal > base_result
        # Difference should be friction_variation * friction_coefficient * cos(troughing_angle) * normal_force
        expected_difference = 1.0 * 0.3 * math.cos(math.radians(20)) * 50.0
        assert result_with_normal - base_result == pytest.approx(
            expected_difference, rel=1e-10
        )

    def test_mathematical_consistency_linear_scaling(self):
        """Test mathematical consistency with linear scaling properties."""
        base_params = {
            "total_weight_force_material": 100.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_inside_wing_roll": 0.3,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_inside_conventional(**base_params)

        # Double material weight should double the result (linear relationship)
        params_double_material = base_params.copy()
        params_double_material["total_weight_force_material"] = 200.0
        result_double_material = _tilted_idler_friction_force_inside_conventional(
            **params_double_material
        )

        assert result_double_material == pytest.approx(base_result * 2, rel=1e-10)

        # Double friction coefficient should double the result (linear relationship)
        params_double_friction = base_params.copy()
        params_double_friction["friction_coefficient_tilted_idler"] = 0.6
        result_double_friction = _tilted_idler_friction_force_inside_conventional(
            **params_double_friction
        )

        assert result_double_friction == pytest.approx(base_result * 2, rel=1e-10)

    def test_geometric_parameter_effects(self):
        """Test effects of geometric parameters on the calculation."""
        base_params = {
            "total_weight_force_material": 200.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_inside_wing_roll": 0.3,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_inside_conventional(**base_params)

        # Larger troughing angle should affect cos(troughing_angle) term
        params_larger_troughing = base_params.copy()
        params_larger_troughing["troughing_angle"] = math.radians(30)
        result_larger_troughing = _tilted_idler_friction_force_inside_conventional(
            **params_larger_troughing
        )

        # Result should be smaller due to smaller cos(30°) vs cos(20°)
        assert result_larger_troughing < base_result

        # Different belt width ratio should scale proportionally
        params_half_width_ratio = base_params.copy()
        params_half_width_ratio["belt_width_on_inside_wing_roll"] = (
            0.15  # Half the original
        )
        result_half_width = _tilted_idler_friction_force_inside_conventional(
            **params_half_width_ratio
        )

        # Result should be roughly half (due to width ratio effect)
        assert result_half_width == pytest.approx(base_result * 0.5, rel=1e-6)

    def test_inclination_angle_effects(self):
        """Test effects of inclination angle on the calculation."""
        base_params = {
            "total_weight_force_material": 200.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_inside_wing_roll": 0.3,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_inside_conventional(**base_params)

        # Inclination angle should reduce result due to cos(inclination_angle) factor
        params_inclined = base_params.copy()
        params_inclined["inclination_angle"] = math.radians(10)  # 10 degrees
        result_inclined = _tilted_idler_friction_force_inside_conventional(
            **params_inclined
        )

        # Result should be smaller due to cos(10°) < cos(0°) = 1
        assert result_inclined < base_result
        # Should be exactly cos(10°) times the base result
        assert result_inclined == pytest.approx(
            base_result * math.cos(math.radians(10)), rel=1e-10
        )

    def test_banking_angle_effects(self):
        """Test effects of banking angle on cos(troughing_angle + banking_angle) term."""
        base_params = {
            "total_weight_force_material": 200.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_inside_wing_roll": 0.3,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_inside_conventional(**base_params)

        # Zero banking angle should affect the cos(troughing_angle + banking_angle) term
        params_zero_banking = base_params.copy()
        params_zero_banking["banking_angle"] = 0.0
        result_zero_banking = _tilted_idler_friction_force_inside_conventional(
            **params_zero_banking
        )

        # Results should be different due to different cos(λ + β) values
        assert result_zero_banking != base_result

        # Larger banking angle
        params_larger_banking = base_params.copy()
        params_larger_banking["banking_angle"] = math.radians(5.0)
        result_larger_banking = _tilted_idler_friction_force_inside_conventional(
            **params_larger_banking
        )

        # Should also be different from base result
        assert result_larger_banking != base_result


class TestTiltedIdlerFrictionForceCenterConventional:
    """Test private function _tilted_idler_friction_force_center_conventional."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        # Publication test data parameters - expected result: 16.77059015 N
        total_weight_force_material = 156.71475  # N
        inclination_angle = 0.0  # radians (0 degrees)
        belt_width = 0.8  # m
        troughing_angle = math.radians(30)  # 30 degrees
        banking_angle = math.radians(1.46)  # 1.46 degrees
        belt_width_on_center_wing_roll = 0.315  # m
        belt_width_on_inside_wing_roll = 0.3025  # m
        belt_width_on_outside_wing_roll = 0.1825  # m
        friction_variation = 0.7  # dimensionless
        friction_coefficient_tilted_idler = 0.279588668362082  # dimensionless
        normal_force_on_idler_roll = 0.0  # N

        result = _tilted_idler_friction_force_center_conventional(
            total_weight_force_material,
            inclination_angle,
            belt_width,
            troughing_angle,
            banking_angle,
            belt_width_on_center_wing_roll,
            belt_width_on_inside_wing_roll,
            belt_width_on_outside_wing_roll,
            friction_variation,
            friction_coefficient_tilted_idler,
            normal_force_on_idler_roll,
        )

        # Check result against publication data
        assert result == pytest.approx(16.77059015, rel=1e-6)

    def test_zero_inclination_angle(self):
        """Test calculation with zero inclination angle."""
        result = _tilted_idler_friction_force_center_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_center_wing_roll=0.4,
            belt_width_on_inside_wing_roll=0.3,
            belt_width_on_outside_wing_roll=0.3,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=0.0,
        )

        assert result > 0
        assert isinstance(result, float)

    def test_zero_friction_variation(self):
        """Test calculation with zero friction variation."""
        result = _tilted_idler_friction_force_center_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_center_wing_roll=0.4,
            belt_width_on_inside_wing_roll=0.3,
            belt_width_on_outside_wing_roll=0.3,
            friction_variation=0.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=0.0,
        )

        assert result == 0.0

    def test_zero_friction_coefficient(self):
        """Test calculation with zero friction coefficient."""
        result = _tilted_idler_friction_force_center_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_center_wing_roll=0.4,
            belt_width_on_inside_wing_roll=0.3,
            belt_width_on_outside_wing_roll=0.3,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.0,
            normal_force_on_idler_roll=0.0,
        )

        assert result == 0.0

    def test_with_normal_force(self):
        """Test calculation with additional normal force on idler roll."""
        base_result = _tilted_idler_friction_force_center_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_center_wing_roll=0.4,
            belt_width_on_inside_wing_roll=0.3,
            belt_width_on_outside_wing_roll=0.3,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=0.0,
        )

        result_with_normal = _tilted_idler_friction_force_center_conventional(
            total_weight_force_material=200.0,
            inclination_angle=0.0,
            belt_width=1.0,
            troughing_angle=math.radians(20),
            banking_angle=math.radians(2.0),
            belt_width_on_center_wing_roll=0.4,
            belt_width_on_inside_wing_roll=0.3,
            belt_width_on_outside_wing_roll=0.3,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.3,
            normal_force_on_idler_roll=50.0,
        )

        # Result with normal force should be larger
        assert result_with_normal > base_result
        # Difference should be friction_variation * friction_coefficient * normal_force
        expected_difference = 1.0 * 0.3 * 50.0
        assert result_with_normal - base_result == pytest.approx(
            expected_difference, rel=1e-10
        )

    def test_mathematical_consistency_linear_scaling(self):
        """Test mathematical consistency with linear scaling properties."""
        base_params = {
            "total_weight_force_material": 100.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_center_wing_roll": 0.4,
            "belt_width_on_inside_wing_roll": 0.3,
            "belt_width_on_outside_wing_roll": 0.3,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_center_conventional(**base_params)

        # Double material weight should double the result (linear relationship)
        params_double_material = base_params.copy()
        params_double_material["total_weight_force_material"] = 200.0
        result_double_material = _tilted_idler_friction_force_center_conventional(
            **params_double_material
        )

        assert result_double_material == pytest.approx(base_result * 2, rel=1e-10)

        # Double friction coefficient should double the result (linear relationship)
        params_double_friction = base_params.copy()
        params_double_friction["friction_coefficient_tilted_idler"] = 0.6
        result_double_friction = _tilted_idler_friction_force_center_conventional(
            **params_double_friction
        )

        assert result_double_friction == pytest.approx(base_result * 2, rel=1e-10)

    def test_geometric_parameter_effects(self):
        """Test effects of geometric parameters on the calculation."""
        base_params = {
            "total_weight_force_material": 200.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_center_wing_roll": 0.4,
            "belt_width_on_inside_wing_roll": 0.3,
            "belt_width_on_outside_wing_roll": 0.3,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_center_conventional(**base_params)

        # Larger troughing angle should affect sin(troughing_angle) terms
        params_larger_troughing = base_params.copy()
        params_larger_troughing["troughing_angle"] = math.radians(30)
        result_larger_troughing = _tilted_idler_friction_force_center_conventional(
            **params_larger_troughing
        )

        # Result should be different due to different sin(30°) vs sin(20°)
        assert result_larger_troughing != base_result

        # Different center width ratio should scale proportionally
        params_half_center_width = base_params.copy()
        params_half_center_width["belt_width_on_center_wing_roll"] = 0.2
        result_half_center = _tilted_idler_friction_force_center_conventional(
            **params_half_center_width
        )

        # Result should be different due to center width ratio effect
        assert result_half_center != base_result

    def test_inclination_angle_effects(self):
        """Test effects of inclination angle on the calculation."""
        base_params = {
            "total_weight_force_material": 200.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_center_wing_roll": 0.4,
            "belt_width_on_inside_wing_roll": 0.3,
            "belt_width_on_outside_wing_roll": 0.3,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_center_conventional(**base_params)

        # Inclination angle should reduce result due to cos(inclination_angle) factors
        params_inclined = base_params.copy()
        params_inclined["inclination_angle"] = math.radians(10)  # 10 degrees
        result_inclined = _tilted_idler_friction_force_center_conventional(
            **params_inclined
        )

        # Result should be smaller due to cos(10°) < cos(0°) = 1
        assert result_inclined < base_result
        # Should be exactly cos(10°) times the base result
        assert result_inclined == pytest.approx(
            base_result * math.cos(math.radians(10)), rel=1e-10
        )

    def test_banking_angle_effects(self):
        """Test effects of banking angle on the complex calculation."""
        base_params = {
            "total_weight_force_material": 200.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_center_wing_roll": 0.4,
            "belt_width_on_inside_wing_roll": 0.3,
            "belt_width_on_outside_wing_roll": 0.3,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_center_conventional(**base_params)

        # Zero banking angle should affect multiple terms
        params_zero_banking = base_params.copy()
        params_zero_banking["banking_angle"] = 0.0
        result_zero_banking = _tilted_idler_friction_force_center_conventional(
            **params_zero_banking
        )

        # Results should be different due to banking angle effects on center, inside, and outside terms
        assert result_zero_banking != base_result

        # Larger banking angle
        params_larger_banking = base_params.copy()
        params_larger_banking["banking_angle"] = math.radians(5.0)
        result_larger_banking = _tilted_idler_friction_force_center_conventional(
            **params_larger_banking
        )

        # Should also be different from base result
        assert result_larger_banking != base_result

    def test_width_distribution_effects(self):
        """Test effects of different width distributions on the calculation."""
        base_params = {
            "total_weight_force_material": 200.0,
            "inclination_angle": 0.0,
            "belt_width": 1.0,
            "troughing_angle": math.radians(20),
            "banking_angle": math.radians(2.0),
            "belt_width_on_center_wing_roll": 0.4,
            "belt_width_on_inside_wing_roll": 0.3,
            "belt_width_on_outside_wing_roll": 0.3,
            "friction_variation": 1.0,
            "friction_coefficient_tilted_idler": 0.3,
            "normal_force_on_idler_roll": 0.0,
        }

        base_result = _tilted_idler_friction_force_center_conventional(**base_params)

        # Different width distribution (more inside, less outside)
        params_different_widths = base_params.copy()
        params_different_widths["belt_width_on_inside_wing_roll"] = 0.4
        params_different_widths["belt_width_on_outside_wing_roll"] = 0.2
        result_different_widths = _tilted_idler_friction_force_center_conventional(
            **params_different_widths
        )

        # Result should be different due to different width distribution
        assert result_different_widths != base_result


class TestWeightForceMaterialInsideConventional:
    """Test the private _weight_force_material_inside_conventional function."""

    def test_basic_calculation(self):
        """Test basic calculation with typical values."""
        normal_force = 1000.0  # N
        troughing_angle = math.radians(30)  # 30 degrees
        banking_angle = math.radians(5)  # 5 degrees

        result = _weight_force_material_inside_conventional(
            normal_force, troughing_angle, banking_angle
        )

        expected = (
            normal_force
            * math.tan(troughing_angle + banking_angle)
            * math.cos(troughing_angle)
        )
        assert abs(result - expected) < 1e-10
        assert result > 0  # Should be positive for positive inputs

    def test_zero_banking_angle(self):
        """Test with zero banking angle."""
        normal_force = 500.0
        troughing_angle = math.radians(20)
        banking_angle = 0.0

        result = _weight_force_material_inside_conventional(
            normal_force, troughing_angle, banking_angle
        )

        expected = normal_force * math.tan(troughing_angle) * math.cos(troughing_angle)
        assert abs(result - expected) < 1e-10

    def test_zero_troughing_angle(self):
        """Test with zero troughing angle."""
        normal_force = 750.0
        troughing_angle = 0.0
        banking_angle = math.radians(3)

        result = _weight_force_material_inside_conventional(
            normal_force, troughing_angle, banking_angle
        )

        expected = normal_force * math.tan(banking_angle) * math.cos(0.0)
        expected = normal_force * math.tan(banking_angle)  # cos(0) = 1
        assert abs(result - expected) < 1e-10

    def test_zero_force(self):
        """Test with zero normal force."""
        normal_force = 0.0
        troughing_angle = math.radians(25)
        banking_angle = math.radians(4)

        result = _weight_force_material_inside_conventional(
            normal_force, troughing_angle, banking_angle
        )

        assert result == 0.0

    def test_different_angle_combinations(self):
        """Test with various angle combinations."""
        normal_force = 800.0

        # Test case 1: Typical industrial values
        result1 = _weight_force_material_inside_conventional(
            normal_force, math.radians(30), math.radians(5)
        )

        # Test case 2: Higher troughing angle
        result2 = _weight_force_material_inside_conventional(
            normal_force, math.radians(45), math.radians(5)
        )

        # Test case 3: Higher banking angle
        result3 = _weight_force_material_inside_conventional(
            normal_force, math.radians(30), math.radians(10)
        )

        # Higher troughing angle should generally give higher result
        assert result2 > result1

        # Higher banking angle should give higher result
        assert result3 > result1

    def test_mathematical_properties(self):
        """Test mathematical properties of the function."""
        normal_force = 600.0
        troughing_angle = math.radians(25)
        banking_angle = math.radians(6)

        # Test linearity with respect to normal force
        result_base = _weight_force_material_inside_conventional(
            normal_force, troughing_angle, banking_angle
        )

        result_double = _weight_force_material_inside_conventional(
            2 * normal_force, troughing_angle, banking_angle
        )

        # Should be exactly double (linear relationship)
        assert abs(result_double - 2 * result_base) < 1e-10

    def test_extreme_angles(self):
        """Test with extreme but valid angle values."""
        normal_force = 1000.0

        # Very small angles
        result_small = _weight_force_material_inside_conventional(
            normal_force, math.radians(1), math.radians(0.5)
        )
        assert result_small > 0

        # Large angles (but physically reasonable)
        result_large = _weight_force_material_inside_conventional(
            normal_force, math.radians(35), math.radians(8)
        )
        assert result_large > result_small

    def test_precision(self):
        """Test numerical precision with very precise inputs."""
        normal_force = 1234.5678
        troughing_angle = math.radians(30.123456)
        banking_angle = math.radians(5.654321)

        result = _weight_force_material_inside_conventional(
            normal_force, troughing_angle, banking_angle
        )

        # Manual calculation for verification
        expected = (
            normal_force
            * math.tan(troughing_angle + banking_angle)
            * math.cos(troughing_angle)
        )
        assert abs(result - expected) < 1e-12


class TestWeightForceMaterialOutsideConventional:
    def test_weight_force_material_outside_conventional_basic(self):
        """Test basic calculation with typical values."""
        normal_force = 1000.0  # N
        troughing_angle = math.radians(30)  # 30 degrees
        banking_angle = math.radians(5)  # 5 degrees

        result = _weight_force_material_outside_conventional(
            normal_force, troughing_angle, banking_angle
        )

        expected = (
            normal_force
            * math.tan(troughing_angle - banking_angle)
            * math.cos(troughing_angle)
        )
        assert abs(result - expected) < 1e-10
        assert result > 0  # Should be positive for positive inputs

    def test_weight_force_material_outside_conventional_zero_banking(self):
        """Test with zero banking angle."""
        normal_force = 500.0
        troughing_angle = math.radians(20)
        banking_angle = 0.0

        result = _weight_force_material_outside_conventional(
            normal_force, troughing_angle, banking_angle
        )

        expected = normal_force * math.tan(troughing_angle) * math.cos(troughing_angle)
        assert abs(result - expected) < 1e-10

    def test_weight_force_material_outside_conventional_large_banking(self):
        """Test with banking angle larger than troughing angle."""
        normal_force = 800.0
        troughing_angle = math.radians(20)
        banking_angle = math.radians(25)  # Larger than troughing

        result = _weight_force_material_outside_conventional(
            normal_force, troughing_angle, banking_angle
        )

        # Should handle negative angle difference (λ - β < 0)
        expected = (
            normal_force
            * math.tan(troughing_angle - banking_angle)
            * math.cos(troughing_angle)
        )
        assert abs(result - expected) < 1e-10


class TestWeightForceMaterialCenterConventional:
    def test_weight_force_material_center_conventional_basic(self):
        """Test basic calculation with typical values."""
        normal_force = 1000.0  # N
        banking_angle = math.radians(5)  # 5 degrees

        result = _weight_force_material_center_conventional(normal_force, banking_angle)

        expected = normal_force * math.tan(banking_angle)
        assert abs(result - expected) < 1e-10
        assert result > 0  # Should be positive for positive inputs

    def test_weight_force_material_center_conventional_zero_banking(self):
        """Test with zero banking angle."""
        normal_force = 500.0
        banking_angle = 0.0

        result = _weight_force_material_center_conventional(normal_force, banking_angle)

        assert abs(result - 0.0) < 1e-10  # Should be zero when banking is zero

    def test_weight_force_material_center_conventional_negative_banking(self):
        """Test with negative banking angle."""
        normal_force = 800.0
        banking_angle = math.radians(-10)  # Negative banking

        result = _weight_force_material_center_conventional(normal_force, banking_angle)

        expected = normal_force * math.tan(banking_angle)
        assert abs(result - expected) < 1e-10
        assert result < 0  # Should be negative for negative banking

    def test_weight_force_material_center_conventional_large_banking(self):
        """Test with large banking angle."""
        normal_force = 750.0
        banking_angle = math.radians(45)  # 45 degrees

        result = _weight_force_material_center_conventional(normal_force, banking_angle)

        expected = normal_force * math.tan(banking_angle)
        assert abs(result - expected) < 1e-10
        assert abs(result - normal_force) < 1e-10  # tan(45°) = 1


class TestWeightForceMaterialConventional:
    def test_weight_force_of_material_conventional_basic(self):
        """Test basic calculation with typical values."""
        inside_force = 530.29  # N
        center_force = 87.49  # N
        outside_force = 433.01  # N

        result = _weight_force_of_material_conventional(
            inside_force, center_force, outside_force
        )

        expected = inside_force + center_force - outside_force
        assert abs(result - expected) < 1e-10
        assert abs(result - 184.77) < 1e-2  # Should match expected value

    def test_weight_force_of_material_conventional_zero_center(self):
        """Test with zero center force."""
        inside_force = 500.0
        center_force = 0.0
        outside_force = 300.0

        result = _weight_force_of_material_conventional(
            inside_force, center_force, outside_force
        )

        expected = inside_force - outside_force
        assert abs(result - expected) < 1e-10
        assert result == 200.0

    def test_weight_force_of_material_conventional_negative_result(self):
        """Test case where outside force dominates (negative result)."""
        inside_force = 200.0
        center_force = 100.0
        outside_force = 400.0

        result = _weight_force_of_material_conventional(
            inside_force, center_force, outside_force
        )

        expected = inside_force + center_force - outside_force
        assert abs(result - expected) < 1e-10
        assert result == -100.0  # Net force toward outside

    def test_weight_force_of_material_conventional_balanced_forces(self):
        """Test case with balanced forces (zero result)."""
        inside_force = 300.0
        center_force = 100.0
        outside_force = 400.0

        result = _weight_force_of_material_conventional(
            inside_force, center_force, outside_force
        )

        assert abs(result) < 1e-10  # Should be essentially zero

    def test_weight_force_of_material_conventional_all_negative(self):
        """Test with all negative force inputs."""
        inside_force = -200.0
        center_force = -50.0
        outside_force = -150.0

        result = _weight_force_of_material_conventional(
            inside_force, center_force, outside_force
        )

        expected = inside_force + center_force - outside_force
        assert abs(result - expected) < 1e-10
        assert result == -100.0  # -200 + (-50) - (-150) = -100


class TestRestrainingForceFromDeadWeightsTowardsOutsideCurveConventional:
    def test_restraining_force_from_dead_weights_conventional_basic(self):
        """Test basic calculation with typical values."""
        belt_force = 450.25  # N
        material_force = 184.77  # N

        result = (
            _restraining_force_from_dead_weights_towards_outside_curve_conventional(
                belt_force, material_force
            )
        )

        expected = belt_force + material_force
        assert abs(result - expected) < 1e-10
        assert abs(result - 635.02) < 1e-2  # Should match expected value

    def test_restraining_force_from_dead_weights_conventional_zero_material(self):
        """Test with zero material force."""
        belt_force = 500.0
        material_force = 0.0

        result = (
            _restraining_force_from_dead_weights_towards_outside_curve_conventional(
                belt_force, material_force
            )
        )

        assert abs(result - belt_force) < 1e-10
        assert result == 500.0

    def test_restraining_force_from_dead_weights_conventional_zero_belt(self):
        """Test with zero belt force."""
        belt_force = 0.0
        material_force = 300.0

        result = (
            _restraining_force_from_dead_weights_towards_outside_curve_conventional(
                belt_force, material_force
            )
        )

        assert abs(result - material_force) < 1e-10
        assert result == 300.0

    def test_restraining_force_from_dead_weights_conventional_equal_forces(self):
        """Test with equal belt and material forces."""
        belt_force = 250.0
        material_force = 250.0

        result = (
            _restraining_force_from_dead_weights_towards_outside_curve_conventional(
                belt_force, material_force
            )
        )

        assert abs(result - 500.0) < 1e-10

    def test_restraining_force_from_dead_weights_conventional_large_values(self):
        """Test with large force values."""
        belt_force = 5000.0
        material_force = 3000.0

        result = (
            _restraining_force_from_dead_weights_towards_outside_curve_conventional(
                belt_force, material_force
            )
        )

        expected = belt_force + material_force
        assert abs(result - expected) < 1e-10
        assert result == 8000.0


class TestTiltedIdlerFrictionForceImprovedCalculation:
    """Test private function _restraining_force_from_tilted_idlers_towards_outside_curve_improved calculation."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        # Using provided test values - expected result: 26.0640014007471 N
        result = _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
            force_component_inside=16.198390581763,  # Inside improved result
            force_component_center=15.0935311327433,  # Center improved result
            force_component_outside=5.2279203137592,  # Outside improved result
        )

        # Expected test result: 26.0640014007471 N
        assert result == pytest.approx(26.0640014007471, rel=1e-6)

    def test_zero_forces(self):
        """Test calculation with all zero force inputs."""
        result = _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
            force_component_inside=0.0,
            force_component_center=0.0,
            force_component_outside=0.0,
        )
        assert result == pytest.approx(0.0, abs=1e-12)

    def test_mathematical_linearity(self):
        """Test mathematical linearity properties."""
        base_inside = 10.0
        base_center = 8.0
        base_outside = 3.0
        scale_factor = 2.5

        base_result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
                base_inside, base_center, base_outside
            )
        )

        scaled_result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
                base_inside * scale_factor,
                base_center * scale_factor,
                base_outside * scale_factor,
            )
        )

        assert scaled_result == pytest.approx(scale_factor * base_result, rel=1e-10)

    def test_force_combination_logic(self):
        """Test the specific force combination logic."""
        inside = 20.0
        center = 15.0
        outside = 5.0

        result = _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
            inside, center, outside
        )
        expected = inside + center - outside  # 20 + 15 - 5 = 30

        assert result == pytest.approx(expected, rel=1e-12)

    def test_negative_outside_force_effect(self):
        """Test effect when outside force is larger than inside+center."""
        inside = 5.0
        center = 4.0
        outside = 12.0  # Larger than inside + center

        result = _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
            inside, center, outside
        )
        expected = inside + center - outside  # 5 + 4 - 12 = -3

        assert result == pytest.approx(expected, rel=1e-12)
        assert result < 0  # Should be negative

    def test_large_values(self):
        """Test with large force values."""
        result = _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
            force_component_inside=1000.0,
            force_component_center=800.0,
            force_component_outside=200.0,
        )
        expected = 1000.0 + 800.0 - 200.0  # 1600.0
        assert result == pytest.approx(expected, rel=1e-10)

    def test_small_values(self):
        """Test with very small force values."""
        result = _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
            force_component_inside=1e-6,
            force_component_center=2e-6,
            force_component_outside=0.5e-6,
        )
        expected = 1e-6 + 2e-6 - 0.5e-6  # 2.5e-6
        assert result == pytest.approx(expected, rel=1e-10)

    def test_asymmetric_force_distribution(self):
        """Test with asymmetric force distributions."""
        # High inside, low center, medium outside
        result1 = _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
            50.0, 5.0, 15.0
        )
        expected1 = 50.0 + 5.0 - 15.0  # 40.0
        assert result1 == pytest.approx(expected1, rel=1e-12)

        # Low inside, high center, low outside
        result2 = _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
            5.0, 50.0, 2.0
        )
        expected2 = 5.0 + 50.0 - 2.0  # 53.0
        assert result2 == pytest.approx(expected2, rel=1e-12)

    def test_equal_force_components(self):
        """Test with equal force components."""
        force_value = 10.0
        result = _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
            force_value, force_value, force_value
        )
        expected = force_value + force_value - force_value  # 10.0
        assert result == pytest.approx(expected, rel=1e-12)

    def test_publication_data_consistency(self):
        """Test consistency with expected publication data relationships."""
        # Verify the relationship matches expected improved method results
        inside = 16.198390581763
        center = 15.0935311327433
        outside = 5.2279203137592

        manual_calc = inside + center - outside
        function_result = (
            _restraining_force_from_tilted_idlers_towards_outside_curve_improved(
                inside, center, outside
            )
        )

        assert function_result == pytest.approx(manual_calc, rel=1e-12)
        assert function_result == pytest.approx(26.0640014007471, rel=1e-6)


class TestTiltedIdlerFrictionForceImproved:
    """Test tilted idler friction force calculations - improved method."""

    def test_tilted_idler_inside_improved_not_implemented(self):
        """Test that improved method functions raise NotImplementedError."""
        # Remove this test since function is now implemented
        pass


class TestTiltedIdlerFrictionForceInsideImprovedCalculation:
    """Test private function _tilted_idler_friction_force_inside_improved calculation."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        # Parameters from TDD notes - expected result: 16.73387457 N
        result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.416183095606664,
            normal_force_on_idler_roll=0.0,
        )

        # Expected test result: 16.198390581763 N
        assert result == pytest.approx(16.198390581763, rel=1e-6)

    def test_zero_forces(self):
        """Test calculation with zero force inputs."""
        result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=0.0,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        assert result == pytest.approx(0.0, abs=1e-12)

    def test_zero_friction_coefficient(self):
        """Test calculation with zero friction coefficient."""
        result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.0,
            normal_force_on_idler_roll=0.0,
        )

        assert result == pytest.approx(0.0, abs=1e-12)

    def test_load_factor_influence(self):
        """Test influence of wing roll load factor."""
        base_result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.0,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        # Double the load factor - should increase result proportionally
        double_factor_result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=2.0,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        assert double_factor_result == pytest.approx(2.0 * base_result, rel=1e-10)

    def test_friction_variation_scaling(self):
        """Test friction variation factor scaling."""
        base_result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=1.0,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        # Half friction variation
        half_friction_result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.5,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        assert half_friction_result == pytest.approx(0.5 * base_result, rel=1e-10)

    def test_normal_force_contribution(self):
        """Test normal force contribution to total friction."""
        base_result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        # Add normal force
        normal_force = 10.0  # N
        with_normal_result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=normal_force,
        )

        # Expected addition: friction_variation * friction_coefficient * normal_force
        expected_addition = 0.7 * 0.429941 * 10.0
        assert with_normal_result == pytest.approx(
            base_result + expected_addition, rel=1e-10
        )

    def test_width_ratio_influence(self):
        """Test influence of width ratio on force calculation."""
        # Base case
        base_result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        # Double the inside width (keeping belt width same)
        double_width_result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.605,  # Double the width
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        # Should be approximately double (due to width ratio doubling)
        ratio = double_width_result / base_result
        assert ratio == pytest.approx(2.0, rel=1e-6)

    def test_angle_effects(self):
        """Test angle effects on calculation."""
        # Test with different troughing angles
        result_30deg = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        result_45deg = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(45),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        # Results should be different due to cosine factors
        assert result_30deg != result_45deg
        # 45 degree angle should give smaller result due to cos(45+1.46) < cos(30+1.46)
        assert result_45deg < result_30deg

    def test_mathematical_linearity(self):
        """Test mathematical linearity properties."""
        base_force = 100.0
        scale_factor = 2.5

        base_result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=base_force,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        scaled_result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=base_force * scale_factor,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        # Should scale linearly with force
        assert scaled_result == pytest.approx(scale_factor * base_result, rel=1e-10)

    def test_edge_case_very_small_values(self):
        """Test edge case with very small input values."""
        result = _tilted_idler_friction_force_inside_improved(
            total_weight_force_material=1e-6,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_inside_wing_roll=0.3025,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.429941,
            normal_force_on_idler_roll=0.0,
        )

        # Should handle small values correctly
        assert result > 0
        assert result < 1e-3  # Should be proportionally small


class TestTiltedIdlerFrictionForceOutsideImproved:
    """Test private function _tilted_idler_friction_force_outside_improved calculation."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        # Parameters from TDD notes - expected result: 4.527511808913801 N
        result = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=0.0,
        )

        # Expected test result: 5.2279203137592 N
        assert result == pytest.approx(5.2279203137592, rel=1e-6)

    def test_zero_weight_force(self):
        """Test function with zero weight force."""
        result = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=0.0,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=0.0,
        )
        assert result == pytest.approx(0.0, abs=1e-12)

    def test_zero_friction_coefficient(self):
        """Test function with zero friction coefficient."""
        result = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.0,
            normal_force_on_idler_roll=0.0,
        )
        assert result == pytest.approx(0.0, abs=1e-12)

    def test_normal_force_influence(self):
        """Test influence of normal force parameter."""
        base_result = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=0.0,
        )

        with_normal_result = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=10.0,
        )

        # Expected difference: 0.7 * 0.216183096 * 10.0
        expected_difference = 0.7 * 0.216183096 * 10.0
        actual_difference = with_normal_result - base_result
        assert actual_difference == pytest.approx(expected_difference, rel=1e-6)

    def test_load_factor_influence(self):
        """Test influence of wing roll load factor."""
        base_result = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.0,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=0.0,
        )

        improved_result = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=0.0,
        )

        # Improved method should give 10% higher result due to load factor
        ratio = improved_result / base_result
        assert ratio == pytest.approx(1.1, rel=1e-10)

    def test_mathematical_consistency(self):
        """Test mathematical consistency of the calculation."""
        # Test that result matches manual calculation
        total_weight = 156.71475
        wing_load_factor = 1.1
        belt_width = 0.8
        outside_width = 0.1825
        troughing_angle = math.radians(30)
        banking_angle = math.radians(1.46)
        friction_variation = 0.7
        friction_coeff = 0.216183096
        normal_force = 0.0

        # Manual calculation
        expected = (
            friction_variation
            * friction_coeff
            * (
                wing_load_factor
                * outside_width
                / belt_width
                * total_weight
                * math.cos(troughing_angle - banking_angle)
                * math.cos(0.0)  # inclination_angle
                + normal_force
            )
        )

        result = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=total_weight,
            inclination_angle=0.0,
            wing_roll_load_factor=wing_load_factor,
            belt_width=belt_width,
            troughing_angle=troughing_angle,
            banking_angle=banking_angle,
            belt_width_on_outside_wing_roll=outside_width,
            friction_variation=friction_variation,
            friction_coefficient_tilted_idler=friction_coeff,
            normal_force_on_idler_roll=normal_force,
        )

        assert result == pytest.approx(expected, rel=1e-12)

    def test_inclination_angle_effect(self):
        """Test effect of inclination angle."""
        base_result = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=0.0,
        )

        inclined_result = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=math.radians(10),  # 10 degree inclination
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=0.0,
        )

        # Inclined result should be smaller (cos(10°) < 1)
        assert inclined_result < base_result
        ratio = inclined_result / base_result
        assert ratio == pytest.approx(math.cos(math.radians(10)), rel=1e-10)

    def test_troughing_angle_effect(self):
        """Test effect of troughing angle."""
        result_30 = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=0.0,
        )

        result_45 = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(45),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=0.0,
        )

        # Different troughing angles should give different results
        assert result_30 != result_45

    def test_banking_angle_effect(self):
        """Test effect of banking angle."""
        result_positive = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=0.0,
        )

        result_negative = _tilted_idler_friction_force_outside_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            wing_roll_load_factor=1.1,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(-1.46),
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.216183096,
            normal_force_on_idler_roll=0.0,
        )

        # Different banking angles should give different results
        assert result_positive != result_negative


class TestTiltedIdlerFrictionForceCenterImproved:
    """Test private function _tilted_idler_friction_force_center_improved calculation."""

    def test_basic_calculation_with_publication_data(self):
        """Test basic calculation with publication data parameters."""
        # Parameters from TDD notes - expected result: 15.0935311327433 N
        result = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=0.0,
        )

        # Expected test result: 15.0935311327433 N
        assert result == pytest.approx(15.0935311327433, rel=1e-6)

    def test_zero_weight_force(self):
        """Test function with zero weight force."""
        result = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=0.0,
            inclination_angle=0.0,
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=0.0,
        )
        assert result == pytest.approx(0.0, abs=1e-12)

    def test_zero_friction_coefficient(self):
        """Test function with zero friction coefficient."""
        result = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.0,
            normal_force_on_idler_roll=0.0,
        )
        assert result == pytest.approx(0.0, abs=1e-12)

    def test_normal_force_influence(self):
        """Test influence of normal force parameter."""
        base_result = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=0.0,
        )

        with_normal_result = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=10.0,
        )

        # Expected difference: 0.7 * 0.279588668 * 10.0
        expected_difference = 0.7 * 0.279588668 * 10.0
        actual_difference = with_normal_result - base_result
        assert actual_difference == pytest.approx(expected_difference, rel=1e-6)

    def test_load_factor_influence(self):
        """Test influence of center roll load factor."""
        base_result = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            center_roll_load_factor=1.0,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=0.0,
        )

        improved_result = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=0.0,
        )

        # Improved method should give 90% of base result due to load factor
        ratio = improved_result / base_result
        assert ratio == pytest.approx(0.9, rel=1e-10)

    def test_mathematical_consistency(self):
        """Test mathematical consistency of the calculation."""
        # Test that result matches manual calculation
        total_weight = 156.71475
        center_load_factor = 0.9
        belt_width = 0.8
        center_width = 0.315
        inside_width = 0.3025
        outside_width = 0.1825
        troughing_angle = math.radians(30)
        banking_angle = math.radians(1.46)
        friction_variation = 0.7
        friction_coeff = 0.279588668
        normal_force = 0.0

        # Manual calculation following the mathematical formulation
        center_component = (
            center_load_factor
            * center_width
            / belt_width
            * total_weight
            * math.cos(banking_angle)
            * math.cos(0.0)  # inclination_angle
        )

        inside_component = (
            center_load_factor
            * inside_width
            / belt_width
            * total_weight
            * math.sin(troughing_angle + banking_angle)
            * math.sin(troughing_angle)
            * math.cos(0.0)  # inclination_angle
        )

        outside_component = (
            center_load_factor
            * outside_width
            / belt_width
            * total_weight
            * math.sin(troughing_angle - banking_angle)
            * math.sin(troughing_angle)
            * math.cos(0.0)  # inclination_angle
        )

        expected = (
            friction_variation
            * friction_coeff
            * (inside_component + center_component + outside_component + normal_force)
        )

        result = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=total_weight,
            inclination_angle=0.0,
            center_roll_load_factor=center_load_factor,
            belt_width=belt_width,
            troughing_angle=troughing_angle,
            banking_angle=banking_angle,
            belt_width_on_center_wing_roll=center_width,
            belt_width_on_inside_wing_roll=inside_width,
            belt_width_on_outside_wing_roll=outside_width,
            friction_variation=friction_variation,
            friction_coefficient_tilted_idler=friction_coeff,
            normal_force_on_idler_roll=normal_force,
        )

        assert result == pytest.approx(expected, rel=1e-12)

    def test_inclination_angle_effect(self):
        """Test effect of inclination angle."""
        base_result = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=0.0,
        )

        inclined_result = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=math.radians(10),  # 10 degree inclination
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=0.0,
        )

        # Inclined result should be smaller (cos(10°) < 1)
        assert inclined_result < base_result
        ratio = inclined_result / base_result
        assert ratio == pytest.approx(math.cos(math.radians(10)), rel=1e-10)

    def test_troughing_angle_effect(self):
        """Test effect of troughing angle."""
        result_30 = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=0.0,
        )

        result_45 = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(45),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=0.0,
        )

        # Different troughing angles should give different results
        assert result_30 != result_45

    def test_banking_angle_effect(self):
        """Test effect of banking angle."""
        result_positive = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=0.0,
        )

        result_negative = _tilted_idler_friction_force_center_improved(
            total_weight_force_material=156.71475,
            inclination_angle=0.0,
            center_roll_load_factor=0.9,
            belt_width=0.8,
            troughing_angle=math.radians(30),
            banking_angle=math.radians(-1.46),
            belt_width_on_center_wing_roll=0.315,
            belt_width_on_inside_wing_roll=0.3025,
            belt_width_on_outside_wing_roll=0.1825,
            friction_variation=0.7,
            friction_coefficient_tilted_idler=0.279588668,
            normal_force_on_idler_roll=0.0,
        )

        # Different banking angles should give different results
        assert result_positive != result_negative


class TestZeroDivisionProtection:
    """Test zero-division protection for all functions with division operations."""

    # Test 1: _force_component_towards_inside_curve_from_belt_tension
    def test_force_component_zero_horizontal_curve_radius(self):
        """Test that zero horizontal_curve_radius raises ValueError."""
        with pytest.raises(
            ValueError, match="horizontal_curve_radius must be positive"
        ):
            _force_component_towards_inside_curve_from_belt_tension(
                belt_tension=5000.0, idler_spacing=1.2, horizontal_curve_radius=0.0
            )

    def test_force_component_negative_horizontal_curve_radius(self):
        """Test that negative horizontal_curve_radius raises ValueError."""
        with pytest.raises(
            ValueError, match="horizontal_curve_radius must be positive"
        ):
            _force_component_towards_inside_curve_from_belt_tension(
                belt_tension=5000.0, idler_spacing=1.2, horizontal_curve_radius=-50.0
            )

    # Test 2: _weight_force_belt_inside_conventional
    def test_weight_force_belt_inside_conventional_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_inside_conventional(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                belt_width=0.0,
                troughing_angle=0.349,
                banking_angle=0.087,
                belt_width_on_inside_wing_roll=0.4,
            )

    def test_weight_force_belt_inside_conventional_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_inside_conventional(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                belt_width=-1.2,
                troughing_angle=0.349,
                banking_angle=0.087,
                belt_width_on_inside_wing_roll=0.4,
            )

    # Test 3: _weight_force_belt_outside_conventional
    def test_weight_force_belt_outside_conventional_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_outside_conventional(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                belt_width=0.0,
                troughing_angle=0.349,
                banking_angle=0.087,
                belt_width_on_outside_wing_roll=0.4,
            )

    def test_weight_force_belt_outside_conventional_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_outside_conventional(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                belt_width=-1.2,
                troughing_angle=0.349,
                banking_angle=0.087,
                belt_width_on_outside_wing_roll=0.4,
            )

    # Test 4: _weight_force_belt_center_conventional
    def test_weight_force_belt_center_conventional_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_center_conventional(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                belt_width=0.0,
                banking_angle=0.087,
                belt_width_on_center_wing_roll=0.4,
            )

    def test_weight_force_belt_center_conventional_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_center_conventional(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                belt_width=-1.2,
                banking_angle=0.087,
                belt_width_on_center_wing_roll=0.4,
            )

    # Test 5: _weight_force_belt_inside_improved
    def test_weight_force_belt_inside_improved_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_inside_improved(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                wing_roll_load_factor=1.5,
                belt_width=0.0,
                troughing_angle=0.349,
                banking_angle=0.087,
                belt_width_on_inside_wing_roll=0.4,
            )

    def test_weight_force_belt_inside_improved_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_inside_improved(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                wing_roll_load_factor=1.5,
                belt_width=-1.2,
                troughing_angle=0.349,
                banking_angle=0.087,
                belt_width_on_inside_wing_roll=0.4,
            )

    # Test 6: _weight_force_belt_outside_improved
    def test_weight_force_belt_outside_improved_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_outside_improved(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                wing_roll_load_factor=1.5,
                belt_width=0.0,
                troughing_angle=0.349,
                banking_angle=0.087,
                belt_width_on_outside_wing_roll=0.4,
            )

    def test_weight_force_belt_outside_improved_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_outside_improved(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                wing_roll_load_factor=1.5,
                belt_width=-1.2,
                troughing_angle=0.349,
                banking_angle=0.087,
                belt_width_on_outside_wing_roll=0.4,
            )

    # Test 7: _weight_force_belt_center_improved
    def test_weight_force_belt_center_improved_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_center_improved(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                center_roll_load_factor=0.8,
                belt_width=0.0,
                banking_angle=0.087,
                belt_width_on_center_wing_roll=0.4,
            )

    def test_weight_force_belt_center_improved_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _weight_force_belt_center_improved(
                total_weight_force_belt=10000.0,
                inclination_angle=0.1,
                center_roll_load_factor=0.8,
                belt_width=-1.2,
                banking_angle=0.087,
                belt_width_on_center_wing_roll=0.4,
            )

    # Test 8: _tilted_idler_friction_force_inside_conventional
    def test_tilted_idler_friction_force_inside_conventional_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_inside_conventional(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                belt_width=0.0,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_inside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )

    def test_tilted_idler_friction_force_inside_conventional_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_inside_conventional(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                belt_width=-1.2,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_inside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )

    # Test 9: _tilted_idler_friction_force_outside_conventional
    def test_tilted_idler_friction_force_outside_conventional_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_outside_conventional(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                belt_width=0.0,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_outside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )

    def test_tilted_idler_friction_force_outside_conventional_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_outside_conventional(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                belt_width=-1.2,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_outside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )

    # Test 10: _tilted_idler_friction_force_center_conventional
    def test_tilted_idler_friction_force_center_conventional_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_center_conventional(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                belt_width=0.0,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_center_wing_roll=0.4,
                belt_width_on_inside_wing_roll=0.3,
                belt_width_on_outside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )

    def test_tilted_idler_friction_force_center_conventional_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_center_conventional(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                belt_width=-1.2,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_center_wing_roll=0.4,
                belt_width_on_inside_wing_roll=0.3,
                belt_width_on_outside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )

    # Test 11: _tilted_idler_friction_force_inside_improved
    def test_tilted_idler_friction_force_inside_improved_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_inside_improved(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                wing_roll_load_factor=1.5,
                belt_width=0.0,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_inside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )

    def test_tilted_idler_friction_force_inside_improved_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_inside_improved(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                wing_roll_load_factor=1.5,
                belt_width=-1.2,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_inside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )

    # Test 12: _tilted_idler_friction_force_outside_improved
    def test_tilted_idler_friction_force_outside_improved_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_outside_improved(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                wing_roll_load_factor=1.5,
                belt_width=0.0,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_outside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )

    def test_tilted_idler_friction_force_outside_improved_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_outside_improved(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                wing_roll_load_factor=1.5,
                belt_width=-1.2,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_outside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )

    # Test 13: _tilted_idler_friction_force_center_improved
    def test_tilted_idler_friction_force_center_improved_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_center_improved(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                center_roll_load_factor=0.8,
                belt_width=0.0,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_center_wing_roll=0.4,
                belt_width_on_inside_wing_roll=0.3,
                belt_width_on_outside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )

    def test_tilted_idler_friction_force_center_improved_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _tilted_idler_friction_force_center_improved(
                total_weight_force_material=1000.0,
                inclination_angle=0.0,
                center_roll_load_factor=0.8,
                belt_width=-1.2,
                troughing_angle=math.radians(30),
                banking_angle=math.radians(5),
                belt_width_on_center_wing_roll=0.4,
                belt_width_on_inside_wing_roll=0.3,
                belt_width_on_outside_wing_roll=0.3,
                friction_variation=0.7,
                friction_coefficient_tilted_idler=0.28,
                normal_force_on_idler_roll=10.0,
            )
