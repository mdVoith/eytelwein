import math
import pytest
from eytelwein.belt_conveyor_design.core._volume_flow_mass_flow import (
    _reduction_factor_inclined_fill,
    _reduction_factor_inclined_fill_1,
    _solve_for_used_belt_width_from_cross_section,
    _usable_belt_width,
    _partial_cross_section_at_water_fill,
    _partial_cross_section_above_water_fill,
    _cross_section_of_fill,
    _cross_section_from_volume_flow_speed,
    _volume_flow_from_cross_section_speed,
    _mass_flow_from_volume_flow_density,
    _volume_flow_from_mass_flow_density,
    _bulk_density_from_mass_flow_volume_flow,
    _mass_flow_from_cross_section_speed_density,
    _cross_section_from_mass_flow_speed_density,
    _nominal_volume_flow,
    _nominal_mass_flow,
    _line_load_from_nominal_load,
    _line_load_from_nominal_mass_flow_speed,
    _belt_edge_distance,
    _length_of_material_on_side_roll,
    _effective_filling_ratio_from_areas,
    _effective_filling_ratio,
)


class TestUsableBeltWidth:
    def test_usable_belt_width_within_limit(self):
        result = _usable_belt_width(1500)
        assert result == 1300.0

    def test_usable_belt_width_at_limit(self):
        result = _usable_belt_width(2000)
        assert result == 1750.0

    def test_usable_belt_width_above_limit(self):
        result = _usable_belt_width(2500)
        assert result == 2250.0


class TestPartialCrossSectionAboveWaterFill:
    def test_partial_cross_section_above_water_fill_flat(self):
        result = _partial_cross_section_above_water_fill(0, 850, 0, math.radians(10))
        assert result == pytest.approx(31840, rel=1e-3)

    def test_partial_cross_section_above_water_fill_V_type(self):
        result = _partial_cross_section_above_water_fill(
            0, 850, math.radians(30), math.radians(20)
        )
        assert result == pytest.approx(49300, rel=1e-3)

    def test_partial_cross_section_above_water_fill_three_type(self):
        result = _partial_cross_section_above_water_fill(
            380, 850, math.radians(30), math.radians(20)
        )
        assert result == pytest.approx(56400, rel=1e-3)

    def test_partial_cross_section_above_water_fill_no_slope(self):
        result = _partial_cross_section_above_water_fill(380, 850, math.radians(30), 0)
        assert result == 0.0

    def test_partial_cross_section_above_water_fill_deep_trough(self):
        result = _partial_cross_section_above_water_fill(
            380, 1210, math.radians(30), math.radians(20)
        )
        assert result == pytest.approx(109800, rel=1e-3)

    def test_partial_cross_section_above_water_fill_zero_usable_belt_width(self):
        result = _partial_cross_section_above_water_fill(
            380, 0, math.radians(30), math.radians(20)
        )
        assert result == pytest.approx(235.8, rel=1e-3)

    def test_partial_cross_section_above_water_fill_zero_troughing_angle(self):
        result = _partial_cross_section_above_water_fill(380, 850, 0, math.radians(10))
        assert result == pytest.approx(31840, rel=1e-3)


class TestPartialCrossSectionAtWaterFill:
    def test_partial_cross_section_at_water_fill_typical_values(self):
        result = _partial_cross_section_at_water_fill(380, 850, math.radians(35))
        assert result == pytest.approx(77100, rel=1e-3)

    def test_partial_cross_section_at_water_fill_typical_values_meter(self):
        result = _partial_cross_section_at_water_fill(0.380, 0.850, math.radians(35))
        assert result == pytest.approx(0.0771, rel=1e-3)

    def test_partial_cross_section_at_water_fill_zero_center_roll_length(self):
        result = _partial_cross_section_at_water_fill(0, 850, math.radians(35))
        assert result == pytest.approx(84800, rel=1e-3)

    def test_partial_cross_section_at_water_fill_zero_usable_belt_width(self):
        result = _partial_cross_section_at_water_fill(500, 0, math.radians(30))
        assert result == pytest.approx(-35436, rel=1e-3)

    def test_partial_cross_section_at_water_fill_zero_troughing_angle(self):
        result = _partial_cross_section_at_water_fill(500, 1000, 0)
        assert result == 0.0

    def test_partial_cross_section_at_water_fill_deep_trough(self):
        result = _partial_cross_section_at_water_fill(380, 1210, math.radians(40))
        assert result == pytest.approx(186171, rel=1e-3)


class TestCrossSectionOfFill:
    def test_cross_section_of_fill_typical_values(self):
        result = _cross_section_of_fill(380, 850, math.radians(35), 0)
        assert result == pytest.approx(77100, rel=1e-3)

    def test_cross_section_of_fill_typical_values_20(self):
        result = _cross_section_of_fill(380, 850, math.radians(35), math.radians(20))
        assert result == pytest.approx(130400, rel=1e-3)

    def test_cross_section_of_fill_handles_zero_values(self):
        result = _cross_section_of_fill(0, 0, 0, 0)
        assert result == 0

    def test_cross_section_of_fill_deep_trough_20(self):
        result = _cross_section_of_fill(380, 1210, math.radians(35), math.radians(20))
        assert result == pytest.approx(273500, rel=1e-3)

    def test_cross_section_of_fill_typical_V_trough(self):
        result = _cross_section_of_fill(0, 850, math.radians(35), math.radians(20))
        assert result == pytest.approx(128900, rel=1e-3)

    def test_cross_section_of_fill_typical_flat(self):
        result = _cross_section_of_fill(0, 850, 0, math.radians(20))
        assert result == pytest.approx(65700, rel=1e-3)


class TestVolumeFlowMassFlow:
    def test_cross_section_from_volume_flow_speed(self):
        result = _cross_section_from_volume_flow_speed(0.0522, 2.09)
        assert result == pytest.approx(0.024976, rel=1e-3)

    def test_volume_flow_from_cross_section_speed_calculates_correctly(self):
        result = _volume_flow_from_cross_section_speed(0.024976, 2.09)
        assert result == pytest.approx(0.0522, rel=1e-3)

    def test_volume_flow_from_cross_section_speed_handles_zero_values(self):
        result = _volume_flow_from_cross_section_speed(0.0, 0.0)
        assert result == 0.0

    def test_mass_flow_from_volume_flow_density(self):
        result = _mass_flow_from_volume_flow_density(0.0522, 1200)
        assert result == pytest.approx(225 / 3.6, rel=1e-2)

    def test_mass_flow_from_volume_flow_density_handles_zero_values(self):
        result = _mass_flow_from_volume_flow_density(0.0, 0.0)
        assert result == 0.0

    def test_mass_flow_from_cross_section_speed_density(self):
        result = _mass_flow_from_cross_section_speed_density(0.024976, 2.09, 1200)
        assert result == pytest.approx(225 / 3.6, rel=1e-2)

    def test_mass_flow_from_cross_section_speed_density_handles_zero_values(self):
        result = _mass_flow_from_cross_section_speed_density(0.0, 0.0, 0.0)
        assert result == 0.0

    def test_cross_section_from_mass_flow_speed_density(self):
        result = _cross_section_from_mass_flow_speed_density(62.5, 2.09, 1200)
        assert result == pytest.approx(0.0249, rel=1e-3)

    def test_cross_section_from_mass_flow_speed_density_handles_zero_values(self):
        with pytest.raises(ValueError):
            _cross_section_from_mass_flow_speed_density(0.0, 0.0, 0.0)

    def test_nominal_volume_flow(self):
        result = _nominal_volume_flow(0.0522, 1)
        assert result == pytest.approx(0.0522, rel=1e-3)

    def test_nominal_volume_flow_filling_ratio(self):
        result = _nominal_volume_flow(0.0522, 0.9)
        assert result == pytest.approx(0.047, rel=1e-3)

    def test_nominal_volume_flow_handles_zero_values(self):
        result = _nominal_volume_flow(0.0, 0.0)
        assert result == 0.0

    def test_nominal_mass_flow(self):
        result = _nominal_mass_flow(0.0522, 1, 1200)
        assert result == pytest.approx(62.5, rel=1e-2)

    def test_nominal_mass_flow_filling_ratio(self):
        result = _nominal_mass_flow(0.0522, 0.9, 1200)
        assert result == pytest.approx(56.25, rel=1e-2)

    def test_nominal_mass_flow_handles_zero_values(self):
        result = _nominal_mass_flow(0.0, 0.0, 0.0)
        assert result == 0.0

    def test_line_load_from_nominal_load(self):
        result = _line_load_from_nominal_load(0.02931, 0.85, 1200)
        assert result == pytest.approx(30, rel=1e-2)

    def test_line_load_from_nominal_load_handles_zero_values(self):
        result = _line_load_from_nominal_load(0.0, 0.0, 0.0)
        assert result == 0.0

    def test_line_load_from_nominal_mass_flow_speed(self):
        result = _line_load_from_nominal_mass_flow_speed(62.5, 2.09)
        assert result == pytest.approx(30, rel=1e-2)

    def test_line_load_from_nominal_mass_flow_speed_handles_zero_values(self):
        with pytest.raises(ValueError):
            _line_load_from_nominal_mass_flow_speed(0.0, 0.0)


class TestSolveForUsedBeltWidthFromCrossSection:
    def test_solve_for_used_belt_width_typical(self):
        # Given parameters
        center_roll_length = 500.0  # mm
        troughing_angle = 35.0  # deg
        equivalent_slope_angle = 13.639  # deg
        usable_belt_width = 800.0  # mm

        # Calculate target cross section area using the same function
        target_cross_section_area = _cross_section_of_fill(
            center_roll_length,
            usable_belt_width,
            troughing_angle,
            equivalent_slope_angle,
        )

        # Now solve for usable_belt_width given the area
        result = _solve_for_used_belt_width_from_cross_section(
            target_cross_section_area,
            center_roll_length,
            troughing_angle,
            equivalent_slope_angle,
            initial_guess=usable_belt_width / 2,
        )
        assert result == pytest.approx(usable_belt_width, rel=1e-5)

    def test_solve_for_used_belt_width_zero_area(self):
        # All zero input should return zero usable belt width
        result = _solve_for_used_belt_width_from_cross_section(
            0.0, 0.0, 0.0, 0.0, initial_guess=1.0
        )
        print(f"Result for zero area: {result}")
        assert result == pytest.approx(0.0, abs=1e-8)

    def test_solve_for_used_belt_width_non_convergence(self):
        # Use impossible area to force non-convergence
        with pytest.raises(ValueError, match="Failed to converge"):
            _solve_for_used_belt_width_from_cross_section(
                1e12, 500.0, 35.0, 13.639, initial_guess=1.0, max_iterations=5
            )

    def test_solve_for_used_belt_width_with_custom_initial_guess(self):
        center_roll_length = 600.0
        troughing_angle = 20.0
        equivalent_slope_angle = 10.0
        usable_belt_width = 900.0

        target_cross_section_area = _cross_section_of_fill(
            center_roll_length,
            usable_belt_width,
            troughing_angle,
            equivalent_slope_angle,
        )

        # Use a custom initial guess far from the solution
        result = _solve_for_used_belt_width_from_cross_section(
            target_cross_section_area,
            center_roll_length,
            troughing_angle,
            equivalent_slope_angle,
            initial_guess=100.0,
        )
        assert result == pytest.approx(usable_belt_width, rel=1e-5)

    def test_solve_for_used_belt_width_with_conti_value(self):
        center_roll_length = 750.0
        troughing_angle = 30.0
        equivalent_slope_angle = 0.0
        usable_belt_width = 1750.0

        target_cross_section_area = _cross_section_of_fill(
            center_roll_length,
            usable_belt_width,
            troughing_angle,
            equivalent_slope_angle,
        )

        # Use a custom initial guess far from the solution
        result = _solve_for_used_belt_width_from_cross_section(
            target_cross_section_area,
            center_roll_length,
            troughing_angle,
            equivalent_slope_angle,
            initial_guess=100.0,
        )
        assert result == pytest.approx(usable_belt_width, rel=1e-5)

    def test_solve_for_used_belt_width_with_conti_value2(self):
        center_roll_length = 465.0
        troughing_angle = 45.0
        equivalent_slope_angle = 15.0
        usable_belt_width = 1030.0

        target_cross_section_area = _cross_section_of_fill(
            center_roll_length,
            usable_belt_width,
            troughing_angle,
            equivalent_slope_angle,
        )

        # Use a custom initial guess far from the solution
        result = _solve_for_used_belt_width_from_cross_section(
            target_cross_section_area,
            center_roll_length,
            troughing_angle,
            equivalent_slope_angle,
            initial_guess=100.0,
        )
        assert result == pytest.approx(usable_belt_width, rel=1e-5)


class TestBeltEdgeDistance:
    def test_belt_edge_distance_standard_case(self):
        # Standard case with typical values
        result = _belt_edge_distance(2000.0, 1750.0)
        assert result == pytest.approx(125.0, rel=1e-6)

    def test_belt_edge_distance_smaller_belt(self):
        # Smaller belt case
        result = _belt_edge_distance(1200.0, 1030.0)
        assert result == pytest.approx(85.0, rel=1e-6)

    def test_belt_edge_distance_equal_widths(self):
        # When belt width equals used width (edge = 0)
        result = _belt_edge_distance(1000.0, 1000.0)
        assert result == pytest.approx(0.0, rel=1e-6)

    def test_belt_edge_distance_handles_zero_values(self):
        # Zero values
        result = _belt_edge_distance(0.0, 0.0)
        assert result == 0.0


class TestLengthOfMaterialOnSideRoll:
    def test_length_of_material_standard_case(self):
        # Standard case
        result = _length_of_material_on_side_roll(500.0, 125.0)
        assert result == pytest.approx(375.0, rel=1e-6)

    def test_length_of_material_zero_edge(self):
        # When edge is zero, length equals part_on_side_idler
        result = _length_of_material_on_side_roll(500.0, 0.0)
        assert result == pytest.approx(500.0, rel=1e-6)

    def test_length_of_material_equal_values(self):
        # When both values are equal, result should be zero
        result = _length_of_material_on_side_roll(250.0, 250.0)
        assert result == pytest.approx(0.0, rel=1e-6)

    def test_length_of_material_handles_zero_values(self):
        # Zero values
        result = _length_of_material_on_side_roll(0.0, 0.0)
        assert result == 0.0


class TestReductionFactorInclinedFill1:
    def test_typical_values(self):
        # Example: maximal_inclination_angle = 10, dynamic_angle_of_slope = 20
        result = _reduction_factor_inclined_fill_1(10.0, 20.0)
        cos2dmax = math.cos(math.radians(10.0)) ** 2
        cos2bdyn = math.cos(math.radians(20.0)) ** 2
        expected = math.sqrt((cos2dmax - cos2bdyn) / (1 - cos2dmax))
        assert result == pytest.approx(expected, rel=1e-10)

    def test_zero_angles(self):
        # Both angles zero: should raise ValueError due to division by zero in denominator
        with pytest.raises(ValueError):
            _reduction_factor_inclined_fill_1(0.0, 0.0)

    def test_maximal_inclination_equals_dynamic_angle(self):
        # Should not raise, but sqrt of zero
        result = _reduction_factor_inclined_fill_1(20.0, 20.0)
        assert result == pytest.approx(0.0, abs=1e-12)

    def test_negative_maximal_inclination(self):
        # Negative maximal_inclination_angle, but abs is used in check
        result = _reduction_factor_inclined_fill_1(-10.0, 20.0)
        cos2dmax = math.cos(math.radians(-10.0)) ** 2
        cos2bdyn = math.cos(math.radians(20.0)) ** 2
        expected = math.sqrt((cos2dmax - cos2bdyn) / (1 - cos2dmax))
        assert result == pytest.approx(expected, rel=1e-10)

    def test_maximal_inclination_greater_than_dynamic_angle(self):
        # Should raise ValueError
        with pytest.raises(
            ValueError, match="must not be greater than the dynamic angle of slope"
        ):
            _reduction_factor_inclined_fill_1(25.0, 20.0)

    def test_fraction_negative(self):
        # If dynamic_angle_of_slope is much larger, denominator is non-zero but positive
        # With maximal_inclination_angle=0, should raise ValueError from pre-check
        with pytest.raises(ValueError):
            _reduction_factor_inclined_fill_1(0.0, 30.0)


class TestReductionFactorInclinedFill:
    def test_typical_values(self):
        """Test with typical values for cross sections and reduction factor."""
        # Example values
        partial_cs = 100.0  # 100 mm²
        total_cs = 500.0  # 500 mm²
        rf1 = 0.8  # reduction factor 1 = 0.8

        expected = 1 - (partial_cs / total_cs) * (1 - rf1)
        result = _reduction_factor_inclined_fill(partial_cs, total_cs, rf1)

        assert result == pytest.approx(expected, rel=1e-10)
        assert result == pytest.approx(0.96, rel=1e-10)  # 1 - (100/500)*(1-0.8) = 0.96

    def test_zero_partial_cross_section(self):
        """Test when partial cross section is zero."""
        result = _reduction_factor_inclined_fill(0.0, 500.0, 0.8)
        assert result == pytest.approx(1.0, rel=1e-10)

    def test_equal_cross_sections(self):
        """Test when partial equals total cross section."""
        result = _reduction_factor_inclined_fill(500.0, 500.0, 0.8)
        assert result == pytest.approx(0.8, rel=1e-10)  # 1 - 1*(1-0.8) = 0.8

    def test_reduction_factor_one(self):
        """Test when reduction factor 1 is 1.0."""
        result = _reduction_factor_inclined_fill(100.0, 500.0, 1.0)
        assert result == pytest.approx(1.0, rel=1e-10)  # 1 - (100/500)*(1-1) = 1.0

    def test_reduction_factor_zero(self):
        """Test when reduction factor 1 is 0.0."""
        result = _reduction_factor_inclined_fill(100.0, 500.0, 0.0)
        expected = 1 - (100.0 / 500.0)
        assert result == pytest.approx(expected, rel=1e-10)  # 1 - (100/500)*(1-0) = 0.8

    def test_division_by_zero_theoretical_cross_section(self):
        """Test division by zero when theoretical cross section is zero."""
        with pytest.raises(ValueError):
            _reduction_factor_inclined_fill(100.0, 0.0, 0.8)


class TestEffectiveFillingRatio:
    def test_typical_values(self):
        """Test with typical values."""
        result = _effective_filling_ratio(0.8, 0.95)
        assert result == pytest.approx(0.76, rel=1e-10)  # 0.8 * 0.95 = 0.76

    def test_zero_filling_ratio(self):
        """Test with zero filling ratio."""
        result = _effective_filling_ratio(0.0, 0.95)
        assert result == pytest.approx(0.0, rel=1e-10)

    def test_zero_reduction_factor(self):
        """Test with zero reduction factor."""
        result = _effective_filling_ratio(0.8, 0.0)
        assert result == pytest.approx(0.0, rel=1e-10)

    def test_values_above_one(self):
        """Test with values above one, which is technically possible but unusual."""
        result = _effective_filling_ratio(1.1, 1.05)
        assert result == pytest.approx(1.155, rel=1e-10)  # 1.1 * 1.05 = 1.155

    def test_negative_values(self):
        """Test with negative values, which should work mathematically but might not be physically valid."""
        result = _effective_filling_ratio(-0.5, 0.95)
        assert result == pytest.approx(-0.475, rel=1e-10)  # -0.5 * 0.95 = -0.475


class TestEffectiveFillingRatioFromAreas:
    def test_effective_filling_ratio_from_areas_normal_case(self):
        """Test the effective filling ratio calculation with normal values."""
        theoretical_area = 0.2
        actual_area = 0.15
        expected_ratio = 0.75
        result = _effective_filling_ratio_from_areas(theoretical_area, actual_area)
        assert abs(result - expected_ratio) < 1e-10

    def test_effective_filling_ratio_from_areas_full(self):
        """Test the effective filling ratio when the conveyor is fully loaded."""
        theoretical_area = 0.2
        actual_area = 0.2
        expected_ratio = 1.0
        result = _effective_filling_ratio_from_areas(theoretical_area, actual_area)
        assert result == expected_ratio

    def test_effective_filling_ratio_from_areas_empty(self):
        """Test the effective filling ratio when the conveyor is empty."""
        theoretical_area = 0.2
        actual_area = 0.0
        expected_ratio = 0.0
        result = _effective_filling_ratio_from_areas(theoretical_area, actual_area)
        assert result == expected_ratio

    def test_effective_filling_ratio_from_areas_division_by_zero(self):
        """Test division by zero error when theoretical area is zero."""
        with pytest.raises(ValueError):
            _effective_filling_ratio_from_areas(0.0, 0.15)


class TestNominalVolumeFlow:
    def test_nominal_volume_flow_standard_case(self):
        """Test with standard values."""
        cross_section = 0.1  # m²
        speed = 2.5  # m/s
        filling_ratio = 0.9  # dimensionless
        result = _nominal_volume_flow(cross_section * speed, filling_ratio)
        assert result == pytest.approx(0.225, rel=1e-10)  # 0.1 * 2.5 * 0.9 = 0.225

    def test_nominal_volume_flow_full_filling(self):
        """Test with 100% filling."""
        cross_section = 0.1  # m²
        speed = 2.5  # m/s
        filling_ratio = 1.0  # dimensionless
        result = _nominal_volume_flow(cross_section * speed, filling_ratio)
        assert result == pytest.approx(0.25, rel=1e-10)  # 0.1 * 2.5 * 1.0 = 0.25

    def test_nominal_volume_flow_zero_values(self):
        """Test with zero values."""
        # All zeros
        result = _nominal_volume_flow(0.0, 0.0)
        assert result == 0.0

        # Zero filling ratio
        result = _nominal_volume_flow(2.5, 0.0)
        assert result == 0.0


class TestNominalMassFlow:
    def test_nominal_mass_flow_standard_case(self):
        """Test with standard values."""
        cross_section = 0.1  # m²
        density = 1600  # kg/m³
        filling_ratio = 0.9  # dimensionless
        result = _nominal_mass_flow(cross_section, density, filling_ratio)
        assert result == pytest.approx(144, rel=1e-10)  # 0.1 * 1600 * 0.9 = 144

    def test_nominal_mass_flow_full_filling(self):
        """Test with 100% filling."""
        cross_section = 0.1  # m²
        density = 1600  # kg/m³
        filling_ratio = 1.0  # dimensionless
        result = _nominal_mass_flow(cross_section, density, filling_ratio)
        assert result == pytest.approx(160, rel=1e-10)  # 0.1 * 1600 * 1.0 = 160

    def test_nominal_mass_flow_zero_values(self):
        """Test with zero values."""
        # All zeros
        result = _nominal_mass_flow(0.0, 0.0, 0.0)
        assert result == 0.0

        result = _nominal_mass_flow(0.0, 2.5, 1600)
        assert result == 0.0

        result = _nominal_mass_flow(0.1, 0.0, 1600)
        assert result == 0.0

        result = _nominal_mass_flow(0.1, 2.5, 0.0)
        assert result == 0.0


class TestLineLoadFromNominalLoad:
    def test_line_load_from_nominal_load_standard_case(self):
        """Test with standard values."""
        nominal_load = 100.0  # kg/s
        speed = 2.5  # m/s
        result = _line_load_from_nominal_load(nominal_load, 1, speed)
        assert result == pytest.approx(250.0, rel=1e-10)  # 100 * 2.5 = 250

    def test_line_load_from_nominal_load_zero_nominal_load(self):
        """Test with zero nominal load."""
        result = _line_load_from_nominal_load(0.0, 1, 2.5)
        assert result == 0.0


class TestLineLoadFromNominalMassFlowSpeed:
    def test_line_load_from_nominal_mass_flow_speed_standard_case(self):
        """Test with standard values."""
        nominal_mass_flow = 100.0  # kg/s
        speed = 2.5  # m/s
        result = _line_load_from_nominal_mass_flow_speed(nominal_mass_flow, speed)
        assert result == pytest.approx(40.0, rel=1e-10)  # 100 / 2.5 = 40

    def test_line_load_from_nominal_mass_flow_speed_zero_nominal_mass_flow(self):
        """Test with zero nominal mass flow."""
        result = _line_load_from_nominal_mass_flow_speed(0.0, 2.5)
        assert result == 0.0

    def test_line_load_from_nominal_mass_flow_speed_zero_speed(self):
        """Test with zero speed (should raise ZeroDivisionError)."""
        with pytest.raises(ValueError):
            _line_load_from_nominal_mass_flow_speed(100.0, 0.0)

class TestVolumeFlowFromMassFlowDensity:
    """Test suite for _volume_flow_from_mass_flow_density (inverse function b)."""

    def test_normal_case(self):
        """Test with typical parameters."""
        m_flow = 1800.0  # kg/s
        bulk_density = 1200.0  # kg/m³
        result = _volume_flow_from_mass_flow_density(m_flow, bulk_density)
        expected = 1.5  # m³/s
        assert result == pytest.approx(expected)

    def test_small_values(self):
        """Test with small but positive values."""
        m_flow = 1.0  # kg/s
        bulk_density = 100.0  # kg/m³
        result = _volume_flow_from_mass_flow_density(m_flow, bulk_density)
        expected = 0.01  # m³/s
        assert result == pytest.approx(expected)

    def test_large_values(self):
        """Test with large values."""
        m_flow = 250000.0  # kg/s
        bulk_density = 2500.0  # kg/m³
        result = _volume_flow_from_mass_flow_density(m_flow, bulk_density)
        expected = 100.0  # m³/s
        assert result == pytest.approx(expected)

    def test_zero_mass_flow(self):
        """Test with zero mass flow."""
        m_flow = 0.0  # kg/s
        bulk_density = 1200.0  # kg/m³
        result = _volume_flow_from_mass_flow_density(m_flow, bulk_density)
        assert result == pytest.approx(0.0)

    def test_zero_density_raises_error(self):
        """Test that zero density raises ValueError."""
        m_flow = 1800.0
        bulk_density = 0.0
        with pytest.raises(ValueError, match="Bulk density must be positive"):
            _volume_flow_from_mass_flow_density(m_flow, bulk_density)

    def test_negative_density_raises_error(self):
        """Test that negative density raises ValueError."""
        m_flow = 1800.0
        bulk_density = -1200.0
        with pytest.raises(ValueError, match="Bulk density must be positive"):
            _volume_flow_from_mass_flow_density(m_flow, bulk_density)

    def test_return_type(self):
        """Test that return type is float."""
        result = _volume_flow_from_mass_flow_density(1800.0, 1200.0)
        assert isinstance(result, float)


class TestBulkDensityFromMassFlowVolumeFlow:
    """Test suite for _bulk_density_from_mass_flow_volume_flow (inverse function c)."""

    def test_normal_case(self):
        """Test with typical parameters."""
        m_flow = 1800.0  # kg/s
        volume_flow = 1.5  # m³/s
        result = _bulk_density_from_mass_flow_volume_flow(m_flow, volume_flow)
        expected = 1200.0  # kg/m³
        assert result == pytest.approx(expected)

    def test_small_values(self):
        """Test with small but positive values."""
        m_flow = 1.0  # kg/s
        volume_flow = 0.01  # m³/s
        result = _bulk_density_from_mass_flow_volume_flow(m_flow, volume_flow)
        expected = 100.0  # kg/m³
        assert result == pytest.approx(expected)

    def test_large_values(self):
        """Test with large values."""
        m_flow = 250000.0  # kg/s
        volume_flow = 100.0  # m³/s
        result = _bulk_density_from_mass_flow_volume_flow(m_flow, volume_flow)
        expected = 2500.0  # kg/m³
        assert result == pytest.approx(expected)

    def test_zero_mass_flow(self):
        """Test with zero mass flow."""
        m_flow = 0.0  # kg/s
        volume_flow = 1.5  # m³/s
        result = _bulk_density_from_mass_flow_volume_flow(m_flow, volume_flow)
        assert result == pytest.approx(0.0)

    def test_zero_volume_flow_raises_error(self):
        """Test that zero volume flow raises ValueError."""
        m_flow = 1800.0
        volume_flow = 0.0
        with pytest.raises(ValueError, match="Volume flow must be positive"):
            _bulk_density_from_mass_flow_volume_flow(m_flow, volume_flow)

    def test_negative_volume_flow_raises_error(self):
        """Test that negative volume flow raises ValueError."""
        m_flow = 1800.0
        volume_flow = -1.5
        with pytest.raises(ValueError, match="Volume flow must be positive"):
            _bulk_density_from_mass_flow_volume_flow(m_flow, volume_flow)

    def test_return_type(self):
        """Test that return type is float."""
        result = _bulk_density_from_mass_flow_volume_flow(1800.0, 1.5)
        assert isinstance(result, float)


class TestBidirectionalValidation:
    """Cross-function validation tests for all three functions."""

    def test_bidirectional_volume_flow_recovery(self):
        """Test that original and inverse function b compose correctly to recover volume_flow."""
        # Given original values
        original_volume_flow = 1.5  # m³/s
        bulk_density = 1200.0  # kg/m³

        # Calculate mass flow using original function
        m_flow = _mass_flow_from_volume_flow_density(
            original_volume_flow, bulk_density
        )

        # Recover volume_flow using inverse function b
        recovered_volume_flow = _volume_flow_from_mass_flow_density(
            m_flow, bulk_density
        )

        # Should recover original value within floating-point tolerance
        assert recovered_volume_flow == pytest.approx(original_volume_flow)

    def test_bidirectional_bulk_density_recovery(self):
        """Test that original and inverse function c compose correctly to recover bulk_density."""
        # Given original values
        original_bulk_density = 1200.0  # kg/m³
        volume_flow = 1.5  # m³/s

        # Calculate mass flow using original function
        m_flow = _mass_flow_from_volume_flow_density(
            volume_flow, original_bulk_density
        )

        # Recover bulk_density using inverse function c
        recovered_density = _bulk_density_from_mass_flow_volume_flow(
            m_flow, volume_flow
        )

        # Should recover original value within floating-point tolerance
        assert recovered_density == pytest.approx(original_bulk_density)

    def test_all_three_functions_satisfy_equation(self):
        """Test that all three functions are mathematically consistent."""
        # Given test values
        volume_flow = 2.0  # m³/s
        bulk_density = 1500.0  # kg/m³

        # Calculate mass flow using original function
        m_flow = _mass_flow_from_volume_flow_density(volume_flow, bulk_density)

        # All these calculations should satisfy: m_flow = volume_flow * bulk_density
        assert m_flow == pytest.approx(volume_flow * bulk_density)

        # Recovering each variable should give original
        assert _volume_flow_from_mass_flow_density(m_flow, bulk_density) == pytest.approx(
            volume_flow
        )
        assert _bulk_density_from_mass_flow_volume_flow(m_flow, volume_flow) == pytest.approx(
            bulk_density
        )

    def test_multiple_compositions_small_values(self):
        """Test bidirectional composition with small values."""
        original_volume_flow = 0.05  # m³/s
        original_density = 800.0  # kg/m³

        # Forward: volume_flow → mass_flow
        m_flow = _mass_flow_from_volume_flow_density(
            original_volume_flow, original_density
        )

        # Backward 1: mass_flow + density → volume_flow
        recovered_volume = _volume_flow_from_mass_flow_density(m_flow, original_density)
        assert recovered_volume == pytest.approx(original_volume_flow)

        # Backward 2: mass_flow + volume_flow → density
        recovered_density = _bulk_density_from_mass_flow_volume_flow(
            m_flow, original_volume_flow
        )
        assert recovered_density == pytest.approx(original_density)

    def test_multiple_compositions_large_values(self):
        """Test bidirectional composition with large values."""
        original_volume_flow = 50.0  # m³/s
        original_density = 2800.0  # kg/m³

        # Forward: volume_flow → mass_flow
        m_flow = _mass_flow_from_volume_flow_density(
            original_volume_flow, original_density
        )

        # Backward 1: mass_flow + density → volume_flow
        recovered_volume = _volume_flow_from_mass_flow_density(m_flow, original_density)
        assert recovered_volume == pytest.approx(original_volume_flow)

        # Backward 2: mass_flow + volume_flow → density
        recovered_density = _bulk_density_from_mass_flow_volume_flow(
            m_flow, original_volume_flow
        )
        assert recovered_density == pytest.approx(original_density)

    def test_zero_mass_flow_consistency(self):
        """Test that zero mass flow is handled consistently across all functions."""
        # If mass flow is zero, then either volume_flow or density must be zero
        m_flow = 0.0
        volume_flow = 1.5
        bulk_density = 0.0  # This makes m_flow = 0

        # Forward calculation
        calculated_m_flow = _mass_flow_from_volume_flow_density(
            volume_flow, bulk_density
        )
        assert calculated_m_flow == pytest.approx(0.0)

        # Inverse calculation for volume_flow (density is zero, should raise)
        with pytest.raises(ValueError):
            _volume_flow_from_mass_flow_density(m_flow, bulk_density)

    def test_conservation_across_different_scales(self):
        """Test that the relationship holds across different scales."""
        test_cases = [
            (0.1, 500.0),
            (1.0, 1000.0),
            (5.0, 1500.0),
            (10.0, 2000.0),
            (100.0, 2500.0),
        ]

        for volume_flow, density in test_cases:
            # Calculate mass flow
            m_flow = _mass_flow_from_volume_flow_density(volume_flow, density)

            # Verify the fundamental equation: m_flow = volume_flow * density
            assert m_flow == pytest.approx(volume_flow * density)

            # Verify both inverses recover the original values
            recovered_volume = _volume_flow_from_mass_flow_density(m_flow, density)
            recovered_density = _bulk_density_from_mass_flow_volume_flow(
                m_flow, volume_flow
            )

            assert recovered_volume == pytest.approx(volume_flow)
            assert recovered_density == pytest.approx(density)


class TestPhysicalValidation:
    """Tests to verify physical reasonableness of results."""

    def test_mass_flow_sign_preservation(self):
        """Test that mass flow preserves sign of volume flow."""
        # Positive volume flow
        m_flow_pos = _mass_flow_from_volume_flow_density(1.5, 1200.0)
        assert m_flow_pos > 0

        # Zero volume flow
        m_flow_zero = _mass_flow_from_volume_flow_density(0.0, 1200.0)
        assert m_flow_zero == 0.0

    def test_linear_scaling_mass_flow(self):
        """Test that mass flow scales linearly with volume flow and density."""
        v_flow = 1.0
        density = 1000.0

        m_flow1 = _mass_flow_from_volume_flow_density(v_flow, density)
        m_flow2 = _mass_flow_from_volume_flow_density(v_flow * 2, density)
        m_flow3 = _mass_flow_from_volume_flow_density(v_flow, density * 2)

        # Doubling volume_flow should double mass_flow
        assert m_flow2 == pytest.approx(m_flow1 * 2)

        # Doubling density should double mass_flow
        assert m_flow3 == pytest.approx(m_flow1 * 2)

    def test_typical_conveyor_belt_scenario(self):
        """Test with typical conveyor belt parameters."""
        # Typical conveyor belt scenario
        volume_flow = 2.5  # m³/s - moderate conveyor throughput
        bulk_density = 1600.0  # kg/m³ - typical aggregate material

        m_flow = _mass_flow_from_volume_flow_density(volume_flow, bulk_density)

        # Result should be physically reasonable: 4000 kg/s
        assert m_flow == pytest.approx(4000.0)

        # Verify inverse functions
        assert _volume_flow_from_mass_flow_density(m_flow, bulk_density) == pytest.approx(
            volume_flow
        )
        assert _bulk_density_from_mass_flow_volume_flow(m_flow, volume_flow) == pytest.approx(
            bulk_density
        )
