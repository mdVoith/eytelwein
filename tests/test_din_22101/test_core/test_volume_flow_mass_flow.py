import math
import pytest
from pint import Quantity

from eytelwein.din_22101.core.volume_flow_mass_flow import (
    reduction_factor_inclined_fill,
    reduction_factor_inclined_fill_1,
    solve_for_used_belt_width_from_cross_section,
    usable_belt_width,
    partial_cross_section_at_water_fill,
    partial_cross_section_above_water_fill,
    cross_section_of_fill,
    line_load_from_nominal_mass_flow_speed,
    line_load_from_nominal_load,
    nominal_mass_flow,
    nominal_volume_flow,
    cross_section_from_mass_flow_speed_density,
    mass_flow_from_cross_section_speed_density,
    mass_flow_from_volume_flow_density,
    volume_flow_from_mass_flow_density,
    volume_flow_from_cross_section_speed,
    cross_section_from_volume_flow_speed,
    effective_filling_ratio_from_areas,
    belt_edge_distance,
    length_of_material_on_side_roll,
    effective_filling_ratio,
)
from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


class TestUsableBeltWidth:
    def test_usable_belt_width_valid_belt_width(self):
        assert usable_belt_width(1000 * u.millimeter) == Quantity(850, u.millimeter)

    def test_usable_belt_width_belt_width_greater_than_2000(self):
        assert usable_belt_width(Quantity(2500, u.millimeter)) == Quantity(
            2250, u.millimeter
        )

    def test_usable_belt_width_belt_width_equal_to_2000(self):
        assert usable_belt_width(Quantity(2000, u.millimeter)) == Quantity(
            1750, u.millimeter
        )

    def test_usable_belt_width_belt_width_less_than_2000(self):
        assert usable_belt_width(Quantity(1500, u.millimeter)) == Quantity(
            1300, u.millimeter
        )

    def test_usable_belt_width_conversion_to_millimeters(self):
        # Test with meters
        belt_width_meters = Quantity(1, u.meter)
        result = usable_belt_width(belt_width_meters)
        assert result.units == u.millimeter
        assert (
            result.magnitude == 850.0
        )  # Assuming _usable_belt_width(1000) returns 850

        # Test with centimeters
        belt_width_centimeters = Quantity(100, u.centimeter)
        result = usable_belt_width(belt_width_centimeters)
        assert result.units == u.millimeter
        assert (
            result.magnitude == 850.0
        )  # Assuming _usable_belt_width(1000) returns 850

        # Test with millimeters
        belt_width_millimeters = Quantity(1000, u.millimeter)
        result = usable_belt_width(belt_width_millimeters)
        assert result.units == u.millimeter
        assert (
            result.magnitude == 850.0
        )  # Assuming _usable_belt_width(1000) returns 850

    def test_usable_belt_width_invalid_units(self):
        # Test with invalid unit
        belt_width_invalid = Quantity(1, u.second)
        with pytest.raises(ValueError, match="Error in converting belt_width"):
            usable_belt_width(belt_width_invalid)


class TestPartialCrossSectionAboveWaterFill:
    def test_partial_cross_section_above_water_fill_flat(self):
        result = partial_cross_section_above_water_fill(
            0 * u.millimeter, 850 * u.millimeter, 0 * u.degree, 10 * u.degree
        )
        assert result.magnitude == pytest.approx(31840, rel=1e-3)

    def test_partial_cross_section_above_water_fill_V_type(self):
        result = partial_cross_section_above_water_fill(
            0 * u.millimeter, 850 * u.millimeter, 30 * u.degree, 20 * u.degree
        )
        assert result.magnitude == pytest.approx(49300, rel=1e-3)

    def test_partial_cross_section_above_water_fill_three_type(self):
        result = partial_cross_section_above_water_fill(
            380 * u.millimeter, 850 * u.millimeter, 30 * u.degree, 20 * u.degree
        )
        assert result.magnitude == pytest.approx(56400, rel=1e-3)

    def test_partial_cross_section_above_water_fill_three_type_meter2(self):
        result = partial_cross_section_above_water_fill(
            380 * u.millimeter,
            850 * u.millimeter,
            30 * u.degree,
            20 * u.degree,
            unit="meter**2",
        )
        assert result.magnitude == pytest.approx(0.0564, rel=1e-3)

    def test_partial_cross_section_above_water_fill_no_slope(self):
        result = partial_cross_section_above_water_fill(
            380 * u.millimeter, 850 * u.millimeter, 30 * u.degree, 0 * u.degree
        )
        assert result.magnitude == 0.0

    def test_partial_cross_section_above_water_fill_deep_trough(self):
        result = partial_cross_section_above_water_fill(
            380 * u.millimeter, 1210 * u.millimeter, 30 * u.degree, 20 * u.degree
        )
        assert result.magnitude == pytest.approx(109800, rel=1e-3)

    def test_partial_cross_section_above_water_fill_deep_trough_radian(self):
        result = partial_cross_section_above_water_fill(
            380 * u.millimeter, 1210 * u.millimeter, 30 * u.degree, 0.3490 * u.radian
        )
        assert result.magnitude == pytest.approx(109800, rel=1e-3)

    def test_partial_cross_section_above_water_fill_zero_usable_belt_width(self):
        result = partial_cross_section_above_water_fill(
            380 * u.millimeter, 0 * u.millimeter, 30 * u.degree, 20 * u.degree
        )
        assert result.magnitude == pytest.approx(235.8, rel=1e-3)

    def test_partial_cross_section_above_water_fill_zero_troughing_angle(self):
        result = partial_cross_section_above_water_fill(
            380 * u.millimeter, 850 * u.millimeter, 0 * u.degree, 10 * u.degree
        )
        assert result.magnitude == pytest.approx(31840, rel=1e-3)

    def test_partial_cross_section_above_water_fill_three_type_false_unit(self):
        with pytest.raises(ValueError, match="Error in converting units:"):
            partial_cross_section_above_water_fill(
                380 * u.millimeter, 850 * u.kilogram, 30 * u.degree, 20 * u.degree
            )

    def test_partial_cross_section_above_water_fill_zero_values(self):
        result = partial_cross_section_above_water_fill(
            0 * u.millimeter, 0 * u.millimeter, 0 * u.degree, 0 * u.degree
        )
        assert result.magnitude == 0.0


class TestPartialCrossSectionAtWaterFill:
    def test_partial_cross_section_at_water_fill_typical_values(self):
        result = partial_cross_section_at_water_fill(
            380 * u.millimeter, 850 * u.millimeter, 35 * u.degree
        )
        assert result.magnitude == pytest.approx(77100, rel=1e-3)

    def test_partial_cross_section_at_water_fill_typical_values_meter(self):
        result = partial_cross_section_at_water_fill(
            0.380 * u.meter, 0.850 * u.meter, 35 * u.degree, unit="meter**2"
        )
        assert result.magnitude == pytest.approx(0.0771, rel=1e-3)
        assert result.units == u("meter**2")

    def test_partial_cross_section_at_water_fill_zero_center_roll_length(self):
        result = partial_cross_section_at_water_fill(
            0 * u.millimeter, 850 * u.millimeter, 35 * u.degree
        )
        assert result.magnitude == pytest.approx(84800, rel=1e-3)

    def test_partial_cross_section_at_water_fill_zero_usable_belt_width(self):
        with pytest.raises(
            ValueError,
            match="Calculated cross-section area A_2 is negative, which is physically impossible.",
        ):
            partial_cross_section_at_water_fill(
                500 * u.millimeter, 0 * u.millimeter, 30 * u.degree
            )

    def test_partial_cross_section_at_water_fill_zero_troughing_angle(self):
        result = partial_cross_section_at_water_fill(
            500 * u.millimeter, 1000 * u.millimeter, 0 * u.degree
        )
        assert result.magnitude == 0.0

    def test_partial_cross_section_at_water_fill_deep_trough(self):
        result = partial_cross_section_at_water_fill(
            380 * u.millimeter, 1210 * u.millimeter, 40 * u.degree
        )
        assert result.magnitude == pytest.approx(186171, rel=1e-3)

    def test_partial_cross_section_at_water_fill_deep_trough_radians(self):
        result = partial_cross_section_at_water_fill(
            380 * u.millimeter, 1210 * u.millimeter, 0.6981 * u.radian
        )
        assert result.magnitude == pytest.approx(186171, rel=1e-3)

    def test_partial_cross_section_at_water_fill_false_unit(self):
        with pytest.raises(ValueError, match="Error in converting units:"):
            partial_cross_section_at_water_fill(
                500 * u.second, 0 * u.millimeter, 30 * u.degree
            )

    def test_partial_cross_section_at_water_fill_handles_zero_values(self):
        result = partial_cross_section_at_water_fill(
            Quantity(0, u.millimeter), Quantity(0, u.millimeter), Quantity(0, u.degree)
        )
        assert result.magnitude == 0


class TestCrossSectionOfFill:
    def test_cross_section_of_fill_typical_values(self):
        result = cross_section_of_fill(
            380 * u.millimeter, 850 * u.millimeter, 35 * u.degree, 0 * u.degree
        )
        assert result.magnitude == pytest.approx(77100, rel=1e-3)

    def test_cross_section_of_fill_typical_values_20(self):
        result = cross_section_of_fill(
            380 * u.millimeter, 850 * u.millimeter, 35 * u.degree, 20 * u.degree
        )
        assert result.magnitude == pytest.approx(130400, rel=1e-3)

    def test_cross_section_of_fill_handles_zero_values(self):
        result = cross_section_of_fill(
            0 * u.millimeter, 0 * u.millimeter, 0 * u.degree, 0 * u.degree
        )
        assert result.magnitude == 0

    def test_cross_section_of_fill_deep_trough_20(self):
        result = cross_section_of_fill(
            380 * u.millimeter, 1210 * u.millimeter, 35 * u.degree, 20 * u.degree
        )
        assert result.magnitude == pytest.approx(273500, rel=1e-3)

    def test_cross_section_of_fill_typical_V_trough(self):
        result = cross_section_of_fill(
            0 * u.millimeter, 850 * u.millimeter, 35 * u.degree, 20 * u.degree
        )
        assert result.magnitude == pytest.approx(128900, rel=1e-3)

    def test_cross_section_of_fill_typical_flat(self):
        result = cross_section_of_fill(
            0 * u.millimeter, 850 * u.millimeter, 0 * u.degree, 20 * u.degree
        )
        assert result.magnitude == pytest.approx(65700, rel=1e-3)

    def test_cross_section_of_fill_typical_values_meter2(self):
        result = cross_section_of_fill(
            380 * u.millimeter,
            850 * u.millimeter,
            35 * u.degree,
            0 * u.degree,
            unit="meter**2",
        )
        assert result.magnitude == pytest.approx(0.0771, rel=1e-3)

    def test_cross_section_of_fill_deep_trough_20_radian(self):
        result = cross_section_of_fill(
            380 * u.millimeter, 1210 * u.millimeter, 35 * u.degree, 0.349 * u.radian
        )
        assert result.magnitude == pytest.approx(273500, rel=1e-3)

    def test_cross_section_of_fill_deep_trough_20_false_unit(self):
        with pytest.raises(ValueError, match="Error in converting units:"):
            cross_section_of_fill(
                380 * u.millimeter, 1210 * u.millimeter, 35 * u.degree, 0.349 * u.second
            )


class TestVolumeFlowMassFlow:
    def test_cross_section_from_volume_flow_speed(self):
        result = cross_section_from_volume_flow_speed(
            0.0522 * u.meter**3 / u.second, 2.09 * u.meter / u.second
        )
        assert result.magnitude == pytest.approx(0.024976, rel=1e-3)

    def test_volume_flow_from_cross_section_speed_calculates_correctly(self):
        result = volume_flow_from_cross_section_speed(
            0.024976 * u.meter**2, 2.09 * u.meter / u.second
        )
        assert result.magnitude == pytest.approx(0.0522, rel=1e-3)

    def test_volume_flow_from_cross_section_speed_handles_zero_values(self):
        result = volume_flow_from_cross_section_speed(
            0.0 * u.meter**2, 0.0 * u.meter / u.second
        )
        assert result.magnitude == 0.0

    def test_mass_flow_from_volume_flow_density(self):
        result = mass_flow_from_volume_flow_density(
            0.0522 * u.meter**3 / u.second, 1200 * u.kilogram / u.meter**3
        )
        assert result.magnitude == pytest.approx(225 / 3.6, rel=1e-2)

    def test_mass_flow_from_volume_flow_density_handles_zero_values(self):
        result = mass_flow_from_volume_flow_density(
            0.0 * u.meter**3 / u.second, 0.0 * u.kilogram / u.meter**3
        )
        assert result.magnitude == 0.0

    def test_mass_flow_from_cross_section_speed_density(self):
        result = mass_flow_from_cross_section_speed_density(
            0.024976 * u.meter**2,
            2.09 * u.meter / u.second,
            1200 * u.kilogram / u.meter**3,
        )
        assert result.magnitude == pytest.approx(225 / 3.6, rel=1e-2)

    def test_mass_flow_from_cross_section_speed_density_handles_zero_values(self):
        result = mass_flow_from_cross_section_speed_density(
            0.0 * u.meter**2, 0.0 * u.meter / u.second, 0.0 * u.kilogram / u.meter**3
        )
        assert result.magnitude == 0.0

    def test_cross_section_from_mass_flow_speed_density(self):
        result = cross_section_from_mass_flow_speed_density(
            62.5 * u.kilogram / u.second,
            2.09 * u.meter / u.second,
            1200 * u.kilogram / u.meter**3,
        )
        assert result.magnitude == pytest.approx(0.0249, rel=1e-3)

    def test_cross_section_from_mass_flow_speed_density_handles_zero_values(self):
        with pytest.raises(ValueError):
            cross_section_from_mass_flow_speed_density(
                0.0 * u.kilogram / u.second,
                0.0 * u.meter / u.second,
                0.0 * u.kilogram / u.meter**3,
            )

    def test_nominal_volume_flow(self):
        result = nominal_volume_flow(0.0522 * u.meter**3 / u.second, 1)
        assert result.magnitude == pytest.approx(0.0522, rel=1e-3)

    def test_nominal_volume_flow_filling_ratio(self):
        result = nominal_volume_flow(0.0522 * u.meter**3 / u.second, 0.9)
        assert result.magnitude == pytest.approx(0.047, rel=1e-3)

    def test_nominal_volume_flow_handles_zero_values(self):
        result = nominal_volume_flow(0.0 * u.meter**3 / u.second, 0.0)
        assert result.magnitude == 0.0

    def test_nominal_mass_flow(self):
        result = nominal_mass_flow(
            0.0522 * u.meter**3 / u.second, 1, 1200 * u.kilogram / u.meter**3
        )
        assert result.magnitude == pytest.approx(62.5, rel=1e-2)

    def test_nominal_mass_flow_filling_ratio(self):
        result = nominal_mass_flow(
            0.0522 * u.meter**3 / u.second, 0.9, 1200 * u.kilogram / u.meter**3
        )
        assert result.magnitude == pytest.approx(56.25, rel=1e-2)

    def test_nominal_mass_flow_handles_zero_values(self):
        result = nominal_mass_flow(
            0.0 * u.meter**3 / u.second, 0.0, 0.0 * u.kilogram / u.meter**3
        )
        assert result.magnitude == 0.0

    def test_line_load_from_nominal_load(self):
        result = line_load_from_nominal_load(
            0.02931 * u.meter**2, 0.85, 1200 * u.kilogram / u.meter**3
        )
        assert result.magnitude == pytest.approx(30, rel=1e-2)

    def test_line_load_from_nominal_load_handles_zero_values(self):
        result = line_load_from_nominal_load(
            0.0 * u.meter**2, 0.0, 0.0 * u.kilogram / u.meter**3
        )
        assert result.magnitude == 0.0

    def test_line_load_from_nominal_mass_flow_speed(self):
        result = line_load_from_nominal_mass_flow_speed(
            62.5 * u.kilogram / u.second, 2.09 * u.meter / u.second
        )
        assert result.magnitude == pytest.approx(30, rel=1e-2)

    def test_line_load_from_nominal_mass_flow_speed_handles_zero_values(self):
        with pytest.raises(ValueError):
            line_load_from_nominal_mass_flow_speed(
                0.0 * u.kilogram / u.second, 0.0 * u.meter / u.second
            )

    def test_volume_flow_from_cross_section_speed_other_units(self):
        result = volume_flow_from_cross_section_speed(
            0.024976 * u.meter**2, 2.09 * u.meter / u.second, unit="liter/second"
        )
        assert result.magnitude == pytest.approx(52.6, rel=1e-2)

    def test_mass_flow_from_volume_flow_density_other_units(self):
        result = mass_flow_from_volume_flow_density(
            0.0522 * u.meter**3 / u.second,
            1200 * u.kilogram / u.meter**3,
            unit="gram/second",
        )
        assert result.magnitude == pytest.approx(62640, rel=1e-2)

    def test_mass_flow_from_cross_section_speed_density_other_units(self):
        result = mass_flow_from_cross_section_speed_density(
            0.024976 * u.meter**2,
            2.09 * u.meter / u.second,
            1200 * u.kilogram / u.meter**3,
            unit="gram/second",
        )
        assert result.magnitude == pytest.approx(63000, rel=1e-2)

    def test_cross_section_from_volume_flow_speed_other_units(self):
        result = cross_section_from_volume_flow_speed(
            0.0522 * u.meter**3 / u.second,
            2.09 * u.meter / u.second,
            unit="centimeter**2",
        )
        assert result.magnitude == pytest.approx(249.62, rel=1e-2)

    def test_cross_section_from_mass_flow_speed_density_other_units(self):
        result = cross_section_from_mass_flow_speed_density(
            62.5 * u.kilogram / u.second,
            2.09 * u.meter / u.second,
            1200 * u.kilogram / u.meter**3,
            unit="centimeter**2",
        )
        assert result.magnitude == pytest.approx(249.62, rel=1e-2)

    def test_nominal_volume_flow_other_units(self):
        result = nominal_volume_flow(
            0.0522 * u.meter**3 / u.second, 1, unit="liter/second"
        )
        assert result.magnitude == pytest.approx(52.2, rel=1e-2)

    def test_nominal_mass_flow_other_units(self):
        result = nominal_mass_flow(
            0.0522 * u.meter**3 / u.second,
            1,
            1200 * u.kilogram / u.meter**3,
            unit="gram/second",
        )
        assert result.magnitude == pytest.approx(62640, rel=1e-2)

    def test_line_load_from_nominal_load_other_units(self):
        result = line_load_from_nominal_load(
            0.02931 * u.meter**2,
            0.85,
            1200 * u.kilogram / u.meter**3,
            unit="gram/meter",
        )
        assert result.magnitude == pytest.approx(29922, rel=1e-2)

    def test_line_load_from_nominal_mass_flow_speed_other_units(self):
        result = line_load_from_nominal_mass_flow_speed(
            62.5 * u.kilogram / u.second, 2.09 * u.meter / u.second, unit="gram/meter"
        )
        assert result.magnitude == pytest.approx(29922, rel=1e-2)

    def test_invalid_units(self):
        with pytest.raises(ValueError, match="Invalid unit"):
            volume_flow_from_cross_section_speed(
                0.024976 * u.meter**2, 2.09 * u.meter / u.second, unit="invalid_unit"
            )

        with pytest.raises(ValueError, match="Invalid unit"):
            mass_flow_from_volume_flow_density(
                0.0522 * u.meter**3 / u.second,
                1200 * u.kilogram / u.meter**3,
                unit="invalid_unit",
            )

        with pytest.raises(ValueError, match="Invalid unit"):
            mass_flow_from_cross_section_speed_density(
                0.024976 * u.meter**2,
                2.09 * u.meter / u.second,
                1200 * u.kilogram / u.meter**3,
                unit="invalid_unit",
            )

        with pytest.raises(ValueError, match="Invalid unit"):
            cross_section_from_volume_flow_speed(
                0.0522 * u.meter**3 / u.second,
                2.09 * u.meter / u.second,
                unit="invalid_unit",
            )

        with pytest.raises(ValueError, match="Invalid unit"):
            cross_section_from_mass_flow_speed_density(
                62.5 * u.kilogram / u.second,
                2.09 * u.meter / u.second,
                1200 * u.kilogram / u.meter**3,
                unit="invalid_unit",
            )

        with pytest.raises(ValueError, match="Invalid unit"):
            nominal_volume_flow(0.0522 * u.meter**3 / u.second, 1, unit="invalid_unit")

        with pytest.raises(ValueError, match="Invalid unit"):
            nominal_mass_flow(
                0.0522 * u.meter**3 / u.second,
                1,
                1200 * u.kilogram / u.meter**3,
                unit="invalid_unit",
            )

        with pytest.raises(ValueError, match="Invalid unit"):
            line_load_from_nominal_load(
                0.024976 * u.meter**2,
                0.85,
                1200 * u.kilogram / u.meter**3,
                unit="invalid_unit",
            )

        with pytest.raises(ValueError, match="Invalid unit"):
            line_load_from_nominal_mass_flow_speed(
                62.5 * u.kilogram / u.second,
                2.09 * u.meter / u.second,
                unit="invalid_unit",
            )

        # Test invalid quantities
        with pytest.raises(ValueError, match="Error in converting units"):
            mass_flow_from_cross_section_speed_density(
                0.024976 * u.meter,
                2.09 * u.meter / u.second,
                1200 * u.kilogram / u.meter**3,
            )

        with pytest.raises(ValueError, match="Error in converting units"):
            cross_section_from_volume_flow_speed(
                0.0522 * u.meter**3, 2.09 * u.meter / u.second
            )

        with pytest.raises(ValueError, match="Error in converting units"):
            cross_section_from_mass_flow_speed_density(
                62.5 * u.kilogram,
                2.09 * u.meter / u.second,
                1200 * u.kilogram / u.meter**3,
            )

        with pytest.raises(ValueError, match="Error in converting units"):
            nominal_volume_flow(0.0522 * u.meter**3, 1)

        with pytest.raises(ValueError, match="Error in converting units"):
            nominal_mass_flow(0.0522 * u.meter**3, 1, 1200 * u.kilogram)

        with pytest.raises(ValueError, match="Error in converting units"):
            line_load_from_nominal_load(
                0.024976 * u.meter, 0.85, 1200 * u.kilogram / u.meter**3
            )

        with pytest.raises(ValueError, match="Error in converting units"):
            line_load_from_nominal_mass_flow_speed(
                62.5 * u.kilogram, 2.09 * u.meter / u.second
            )


class TestSolveForUsedBeltWidthFromCrossSection:
    def test_happy_path(self):
        # These are dummy values; adjust as needed for your implementation
        target_cross_section = Quantity(100000, u.millimeter**2)
        center_roll_length = Quantity(500, u.millimeter)
        troughing_angle = Quantity(30, u.degree)
        equivalent_slope_angle = Quantity(10, u.degree)
        result = solve_for_used_belt_width_from_cross_section(
            target_cross_section,
            center_roll_length,
            troughing_angle,
            equivalent_slope_angle,
        )
        assert isinstance(result, Quantity)
        assert result.magnitude > 0

    def test_with_initial_guess(self):
        target_cross_section = Quantity(100000, u.millimeter**2)
        center_roll_length = Quantity(500, u.millimeter)
        troughing_angle = Quantity(30, u.degree)
        equivalent_slope_angle = Quantity(10, u.degree)
        initial_guess = Quantity(800, u.millimeter)
        result = solve_for_used_belt_width_from_cross_section(
            target_cross_section,
            center_roll_length,
            troughing_angle,
            equivalent_slope_angle,
            initial_guess=initial_guess,
        )
        assert isinstance(result, Quantity)
        assert result.magnitude > 0

    def test_invalid_unit(self):
        target_cross_section = Quantity(100000, u.millimeter**2)
        center_roll_length = Quantity(500, u.millimeter)
        troughing_angle = Quantity(30, u.degree)
        equivalent_slope_angle = Quantity(10, u.degree)
        with pytest.raises(ValueError, match="Invalid unit"):
            solve_for_used_belt_width_from_cross_section(
                target_cross_section,
                center_roll_length,
                troughing_angle,
                equivalent_slope_angle,
                unit="invalid_unit",
            )

    def test_error_in_converting_units(self):
        # Use an invalid unit for center_roll_length
        target_cross_section = Quantity(100000, u.millimeter**2)
        center_roll_length = Quantity(500, u.kilogram)
        troughing_angle = Quantity(30, u.degree)
        equivalent_slope_angle = Quantity(10, u.degree)
        with pytest.raises(ValueError, match="Error in converting units"):
            solve_for_used_belt_width_from_cross_section(
                target_cross_section,
                center_roll_length,
                troughing_angle,
                equivalent_slope_angle,
            )

    def test_calculation_error(self, monkeypatch):
        # Patch the private function to raise ValueError
        import eytelwein.din_22101.core.volume_flow_mass_flow as vfm

        def raise_value_error(*args, **kwargs):
            raise ValueError("No solution found")

        monkeypatch.setattr(
            vfm, "_solve_for_used_belt_width_from_cross_section", raise_value_error
        )

        target_cross_section = Quantity(100000, u.millimeter**2)
        center_roll_length = Quantity(500, u.millimeter)
        troughing_angle = Quantity(30, u.degree)
        equivalent_slope_angle = Quantity(10, u.degree)
        with pytest.raises(ValueError, match="Calculation error: No solution found"):
            solve_for_used_belt_width_from_cross_section(
                target_cross_section,
                center_roll_length,
                troughing_angle,
                equivalent_slope_angle,
            )

    def test_zero_cross_section(self):
        target_cross_section = Quantity(0, u.millimeter**2)
        center_roll_length = Quantity(500, u.millimeter)
        troughing_angle = Quantity(30, u.degree)
        equivalent_slope_angle = Quantity(10, u.degree)
        result = solve_for_used_belt_width_from_cross_section(
            target_cross_section,
            center_roll_length,
            troughing_angle,
            equivalent_slope_angle,
        )
        assert result.magnitude == 0

    def test_with_Conti_values(self):
        # These are dummy values; adjust as needed for your implementation
        """
        center_roll_length = 750.0
        troughing_angle = 30.0
        equivalent_slope_angle = 0.0
        usable_belt_width = 1750.0
        """
        target_cross_section = Quantity(0.9448, u.meter**2)
        center_roll_length = Quantity(1050, u.millimeter)
        troughing_angle = Quantity(35, u.degree)
        equivalent_slope_angle = Quantity(10, u.degree)
        result = solve_for_used_belt_width_from_cross_section(
            target_cross_section,
            center_roll_length,
            troughing_angle,
            equivalent_slope_angle,
            precision=2,
            unit="meter",
        )
        assert isinstance(result, Quantity)
        assert result.magnitude == pytest.approx(2.55, rel=1e-2)


class TestBeltEdgeDistance:
    def test_belt_edge_distance_standard_case(self):
        # Standard case with typical values
        belt_width = u.Quantity(2000, u.millimeter)
        used_belt_width = u.Quantity(1750, u.millimeter)
        result = belt_edge_distance(belt_width, used_belt_width)
        assert result.magnitude == pytest.approx(125.0, rel=1e-6)
        assert result.units == u.millimeter

    def test_belt_edge_distance_smaller_belt(self):
        # Smaller belt case
        belt_width = u.Quantity(1200, u.millimeter)
        used_belt_width = u.Quantity(1030, u.millimeter)
        result = belt_edge_distance(belt_width, used_belt_width)
        assert result.magnitude == pytest.approx(85.0, rel=1e-6)
        assert result.units == u.millimeter

    def test_belt_edge_distance_equal_widths(self):
        # When belt width equals used width (edge = 0)
        belt_width = u.Quantity(1000, u.millimeter)
        used_belt_width = u.Quantity(1000, u.millimeter)
        result = belt_edge_distance(belt_width, used_belt_width)
        assert result.magnitude == pytest.approx(0.0, rel=1e-6)
        assert result.units == u.millimeter

    def test_belt_edge_distance_handles_zero_values(self):
        # Zero values
        belt_width = u.Quantity(0, u.millimeter)
        used_belt_width = u.Quantity(0, u.millimeter)
        result = belt_edge_distance(belt_width, used_belt_width)
        assert result.magnitude == 0.0
        assert result.units == u.millimeter

    def test_belt_edge_distance_unit_conversion(self):
        # Test unit conversion - input in meters, output in cm
        belt_width = u.Quantity(2.0, u.meter)
        used_belt_width = u.Quantity(1.75, u.meter)
        result = belt_edge_distance(belt_width, used_belt_width, unit="centimeter")
        assert result.magnitude == pytest.approx(12.5, rel=1e-6)
        assert result.units == u.centimeter

    def test_belt_edge_distance_with_precision(self):
        # Test precision parameter
        belt_width = u.Quantity(2000, u.millimeter)
        used_belt_width = u.Quantity(1753, u.millimeter)
        result = belt_edge_distance(belt_width, used_belt_width, precision=0)
        assert result.magnitude == 124.0  # Rounded to 0 decimal places

    def test_belt_edge_distance_mixed_units(self):
        # Test with mixed units
        belt_width = u.Quantity(2.0, u.meter)
        used_belt_width = u.Quantity(1750, u.millimeter)
        result = belt_edge_distance(belt_width, used_belt_width)
        assert result.magnitude == pytest.approx(125.0, rel=1e-6)
        assert result.units == u.millimeter


class TestLengthOfMaterialOnSideRoll:
    def test_length_of_material_typical_case(self):
        # Standard case
        part_on_side_idler = u.Quantity(500, u.millimeter)
        belt_edge = u.Quantity(125, u.millimeter)
        result = length_of_material_on_side_roll(part_on_side_idler, belt_edge)
        assert result.magnitude == pytest.approx(375.0, rel=1e-6)
        assert result.units == u.millimeter

    def test_length_of_material_zero_edge(self):
        # When edge is zero, length equals part_on_side_idler
        part_on_side_idler = u.Quantity(500, u.millimeter)
        belt_edge = u.Quantity(0, u.millimeter)
        result = length_of_material_on_side_roll(part_on_side_idler, belt_edge)
        assert result.magnitude == pytest.approx(500.0, rel=1e-6)
        assert result.units == u.millimeter

    def test_length_of_material_equal_values(self):
        # When both values are equal, result should be zero
        part_on_side_idler = u.Quantity(250, u.millimeter)
        belt_edge = u.Quantity(250, u.millimeter)
        result = length_of_material_on_side_roll(part_on_side_idler, belt_edge)
        assert result.magnitude == pytest.approx(0.0, rel=1e-6)
        assert result.units == u.millimeter

    def test_length_of_material_unit_conversion(self):
        # Test unit conversion - input in meters, output in cm
        part_on_side_idler = u.Quantity(0.5, u.meter)
        belt_edge = u.Quantity(125, u.millimeter)
        result = length_of_material_on_side_roll(
            part_on_side_idler, belt_edge, unit="centimeter"
        )
        assert result.magnitude == pytest.approx(37.5, rel=1e-6)
        assert result.units == u.centimeter

    def test_length_of_material_with_precision(self):
        # Test precision parameter
        part_on_side_idler = u.Quantity(500, u.millimeter)
        belt_edge = u.Quantity(123.456, u.millimeter)
        result = length_of_material_on_side_roll(
            part_on_side_idler, belt_edge, precision=0
        )
        assert result.magnitude == 377.0  # Rounded to 0 decimal places


class TestReductionFactorInclinedFill1Public:
    def test_typical_values(self):
        """Test with typical angle values"""
        result = reduction_factor_inclined_fill_1(
            Quantity(10.0, u.degree), Quantity(20.0, u.degree)
        )
        # Calculate expected value
        cos2dmax = math.cos(math.radians(10.0)) ** 2
        cos2bdyn = math.cos(math.radians(20.0)) ** 2
        expected = math.sqrt((cos2dmax - cos2bdyn) / (1 - cos2dmax))
        assert result.magnitude == pytest.approx(expected, rel=1e-5)
        assert result.units == u.dimensionless

    def test_maximal_equals_dynamic(self):
        """Test when maximal inclination equals dynamic angle"""
        result = reduction_factor_inclined_fill_1(
            Quantity(20.0, u.degree), Quantity(20.0, u.degree)
        )
        assert result.magnitude == pytest.approx(0.0, abs=1e-5)
        assert result.units == u.dimensionless

    def test_with_precision(self):
        """Test precision parameter"""
        result = reduction_factor_inclined_fill_1(
            Quantity(10.0, u.degree), Quantity(20.0, u.degree), precision=2
        )
        # Calculate expected value with 2 decimal places
        cos2dmax = math.cos(math.radians(10.0)) ** 2
        cos2bdyn = math.cos(math.radians(20.0)) ** 2
        expected = round(math.sqrt((cos2dmax - cos2bdyn) / (1 - cos2dmax)), 2)
        assert result.magnitude == expected
        assert result.units == u.dimensionless

    def test_maximal_greater_than_dynamic(self):
        """Test error when maximal inclination is greater than dynamic angle"""
        with pytest.raises(
            ValueError,
            match="Calculation error: The maximal inclination angle must not be greater than the dynamic angle of slope.",
        ):
            reduction_factor_inclined_fill_1(
                Quantity(25.0, u.degree), Quantity(20.0, u.degree)
            )

    def test_division_by_zero(self):
        """Test error when input would cause division by zero"""
        with pytest.raises(ValueError):
            reduction_factor_inclined_fill_1(
                Quantity(0.0, u.degree), Quantity(30.0, u.degree)
            )

    def test_with_radians(self):
        """Test with input in radians instead of degrees"""
        result = reduction_factor_inclined_fill_1(
            Quantity(math.pi / 18, u.radian),  # 10 degrees
            Quantity(math.pi / 9, u.radian),  # 20 degrees
        )
        # Calculate expected value
        cos2dmax = math.cos(math.radians(10.0)) ** 2
        cos2bdyn = math.cos(math.radians(20.0)) ** 2
        expected = math.sqrt((cos2dmax - cos2bdyn) / (1 - cos2dmax))
        assert result.magnitude == pytest.approx(expected, rel=1e-5)
        assert result.units == u.dimensionless


class TestReductionFactorInclinedFillPublic:
    def test_typical_values(self):
        """Test with typical values and unit handling."""
        result = reduction_factor_inclined_fill(
            Quantity(100.0, u.millimeter**2),
            Quantity(500.0, u.millimeter**2),
            Quantity(0.8, u.dimensionless),
        )
        expected = 1 - (100.0 / 500.0) * (1 - 0.8)
        assert result.magnitude == pytest.approx(expected, rel=1e-5)
        assert result.units == u.dimensionless

    def test_different_area_units(self):
        """Test with different area units (cm² instead of mm²)."""
        result = reduction_factor_inclined_fill(
            Quantity(1.0, u.centimeter**2),  # 1 cm² = 100 mm²
            Quantity(5.0, u.centimeter**2),  # 5 cm² = 500 mm²
            Quantity(0.8, u.dimensionless),
        )
        expected = 1 - (100.0 / 500.0) * (1 - 0.8)
        assert result.magnitude == pytest.approx(expected, rel=1e-5)

    def test_zero_cross_section_error(self):
        """Test error when theoretical cross section is zero."""
        with pytest.raises(
            ValueError, match="Theoretical cross-section of fill cannot be zero"
        ):
            reduction_factor_inclined_fill(
                Quantity(100.0, u.millimeter**2),
                Quantity(0.0, u.millimeter**2),
                Quantity(0.8, u.dimensionless),
            )

    def test_precision_parameter(self):
        """Test the precision parameter."""
        result = reduction_factor_inclined_fill(
            Quantity(100.0, u.millimeter**2),
            Quantity(500.0, u.millimeter**2),
            Quantity(0.8, u.dimensionless),
            precision=2,
        )
        expected = round(1 - (100.0 / 500.0) * (1 - 0.8), 2)
        assert result.magnitude == expected

    def test_non_dimensionless_reduction_factor(self):
        """Test handling of invalid input units."""
        with pytest.raises(ValueError, match="Error in converting units"):
            reduction_factor_inclined_fill(
                Quantity(100.0, u.millimeter**2),
                Quantity(500.0, u.millimeter**2),
                Quantity(0.8, u.meter),  # Invalid unit for reduction factor
            )


class TestEffectiveFillingRatio:
    def test_typical_values(self):
        """Test with typical values."""
        result = effective_filling_ratio(0.8, 0.95 * u.dimensionless)
        assert result.magnitude == pytest.approx(0.76, rel=1e-10)
        assert result.units == u.dimensionless

    def test_zero_filling_ratio(self):
        """Test with zero filling ratio."""
        result = effective_filling_ratio(0.0, 0.95 * u.dimensionless)
        assert result.magnitude == pytest.approx(0.0, rel=1e-10)
        assert result.units == u.dimensionless

    def test_zero_reduction_factor(self):
        """Test with zero reduction factor."""
        result = effective_filling_ratio(0.8, 0.0 * u.dimensionless)
        assert result.magnitude == pytest.approx(0.0, rel=1e-10)
        assert result.units == u.dimensionless

    def test_values_above_one(self):
        """Test with values above one, which is technically possible but unusual."""
        result = effective_filling_ratio(1.1, 1.05 * u.dimensionless)
        assert result.magnitude == pytest.approx(1.155, rel=1e-10)
        assert result.units == u.dimensionless

    def test_precision(self):
        """Test with custom precision."""
        result = effective_filling_ratio(0.8, 0.95 * u.dimensionless, precision=2)
        assert result.magnitude == pytest.approx(0.76, rel=1e-10)
        assert result.units == u.dimensionless

    def test_unit_conversion(self):
        """Test with unit conversion (although dimensionless is the only valid unit)."""
        result = effective_filling_ratio(
            0.8, 0.95 * u.dimensionless, unit="dimensionless"
        )
        assert result.magnitude == pytest.approx(0.76, rel=1e-10)
        assert result.units == u.dimensionless

    def test_invalid_reduction_factor_units(self):
        """Test with invalid reduction factor units."""
        with pytest.raises(ValueError, match="Error in converting units"):
            effective_filling_ratio(0.8, 0.95 * u.meter)

    def test_invalid_output_unit(self):
        """Test with an invalid output unit."""
        with pytest.raises(ValueError, match="Invalid unit"):
            effective_filling_ratio(0.8, 0.95 * u.dimensionless, unit="meter")


class TestEffectiveFillingRatioFromAreasPublic:
    def test_effective_filling_ratio_from_areas_normal_case(self):
        """Test the effective filling ratio calculation with normal values."""
        theoretical_area = 0.2 * u.meter**2
        actual_area = 0.15 * u.meter**2
        expected_ratio = 0.75 * u.dimensionless
        result = effective_filling_ratio_from_areas(theoretical_area, actual_area)
        assert result.magnitude == expected_ratio.magnitude
        assert result.units == expected_ratio.units

    def test_effective_filling_ratio_from_areas_different_units(self):
        """Test using different but compatible units for the areas."""
        theoretical_area = 200000 * u.millimeter**2
        actual_area = 0.15 * u.meter**2
        expected_ratio = 0.75 * u.dimensionless
        result = effective_filling_ratio_from_areas(theoretical_area, actual_area)
        assert abs(result.magnitude - expected_ratio.magnitude) < 1e-5
        assert result.units == expected_ratio.units

    def test_effective_filling_ratio_from_areas_zero_theoretical(self):
        """Test the validation for zero theoretical area."""
        theoretical_area = 0.0 * u.meter**2
        actual_area = 0.15 * u.meter**2
        with pytest.raises(
            ValueError,
            match="Theoretical cross-section area must be greater than zero.",
        ):
            effective_filling_ratio_from_areas(theoretical_area, actual_area)

    def test_effective_filling_ratio_from_areas_different_output_unit(self):
        """Test with a different output unit (percent)."""
        theoretical_area = 0.2 * u.meter**2
        actual_area = 0.15 * u.meter**2
        result = effective_filling_ratio_from_areas(
            theoretical_area, actual_area, unit="percent"
        )
        expected_ratio = 75.0 * u.percent
        assert result.magnitude == expected_ratio.magnitude
        assert str(result.units) == str(expected_ratio.units)

    def test_effective_filling_ratio_from_areas_precision(self):
        """Test the precision parameter."""
        theoretical_area = 0.2 * u.meter**2
        actual_area = 0.1523 * u.meter**2
        result = effective_filling_ratio_from_areas(
            theoretical_area, actual_area, precision=2
        )
        expected_ratio = 0.76 * u.dimensionless
        assert result.magnitude == expected_ratio.magnitude

    def test_effective_filling_ratio_from_areas_invalid_output_unit(self):
        """Test with an invalid output unit."""
        theoretical_area = 0.2 * u.meter**2
        actual_area = 0.15 * u.meter**2
        with pytest.raises(
            ValueError, match="The output unit 'meter' must be dimensionless."
        ):
            effective_filling_ratio_from_areas(
                theoretical_area, actual_area, unit="meter"
            )

class TestVolumeFlowFromMassFlowDensity:
    """Test suite for volume_flow_from_mass_flow_density public API function."""

    def test_volume_flow_from_mass_flow_density_normal_case(self):
        """Test with typical conveyor belt parameters."""
        m_flow = 1800 * u.kilogram / u.second
        bulk_density = 1200 * u.kilogram / u.meter**3
        result = volume_flow_from_mass_flow_density(m_flow, bulk_density)
        assert result.magnitude == pytest.approx(1.5, rel=1e-3)
        assert result.units == u.meter**3 / u.second

    def test_volume_flow_from_mass_flow_density_custom_output_unit(self):
        """Test with custom output unit."""
        m_flow = 1800 * u.kilogram / u.second
        bulk_density = 1200 * u.kilogram / u.meter**3
        result = volume_flow_from_mass_flow_density(
            m_flow, bulk_density, unit="millimeter**3/second"
        )
        assert result.magnitude == pytest.approx(1.5e9, rel=1e-3)
        assert result.units == u.millimeter**3 / u.second

    def test_volume_flow_from_mass_flow_density_with_precision(self):
        """Test precision parameter."""
        m_flow = 1800 * u.kilogram / u.second
        bulk_density = 1200 * u.kilogram / u.meter**3
        result = volume_flow_from_mass_flow_density(m_flow, bulk_density, precision=2)
        assert result.magnitude == 1.5
        assert result.units == u.meter**3 / u.second

    def test_volume_flow_from_mass_flow_density_zero_mass_flow(self):
        """Test with zero mass flow."""
        m_flow = 0 * u.kilogram / u.second
        bulk_density = 1200 * u.kilogram / u.meter**3
        result = volume_flow_from_mass_flow_density(m_flow, bulk_density)
        assert result.magnitude == pytest.approx(0.0, abs=1e-10)

    def test_volume_flow_from_mass_flow_density_zero_density_raises_error(self):
        """Test that zero density raises ValueError."""
        m_flow = 1800 * u.kilogram / u.second
        bulk_density = 0 * u.kilogram / u.meter**3
        with pytest.raises(ValueError, match="Bulk density must be positive"):
            volume_flow_from_mass_flow_density(m_flow, bulk_density)

    def test_volume_flow_from_mass_flow_density_negative_density_raises_error(self):
        """Test that negative density raises ValueError."""
        m_flow = 1800 * u.kilogram / u.second
        bulk_density = -1200 * u.kilogram / u.meter**3
        with pytest.raises(ValueError, match="Bulk density must be positive"):
            volume_flow_from_mass_flow_density(m_flow, bulk_density)

    def test_volume_flow_from_mass_flow_density_unit_conversion_mass_flow(self):
        """Test that mass flow is correctly converted from different units."""
        # 1.8 megagram/second = 1800 kg/s
        m_flow = 1.8 * u.megagram / u.second
        bulk_density = 1200 * u.kilogram / u.meter**3
        result = volume_flow_from_mass_flow_density(m_flow, bulk_density)
        assert result.magnitude == pytest.approx(1.5, rel=1e-3)

    def test_volume_flow_from_mass_flow_density_unit_conversion_density(self):
        """Test that density is correctly converted from different units."""
        m_flow = 1800 * u.kilogram / u.second
        # 1.2 megagram/meter³ = 1200 kg/m³
        bulk_density = 1.2 * u.megagram / u.meter**3
        result = volume_flow_from_mass_flow_density(m_flow, bulk_density)
        assert result.magnitude == pytest.approx(1.5, rel=1e-3)

    def test_volume_flow_from_mass_flow_density_invalid_output_unit(self):
        """Test that invalid output unit raises ValueError."""
        m_flow = 1800 * u.kilogram / u.second
        bulk_density = 1200 * u.kilogram / u.meter**3
        with pytest.raises(ValueError, match="Invalid unit"):
            volume_flow_from_mass_flow_density(
                m_flow, bulk_density, unit="invalid_unit"
            )

    def test_volume_flow_from_mass_flow_density_small_values(self):
        """Test with small values."""
        m_flow = 0.1 * u.kilogram / u.second
        bulk_density = 100 * u.kilogram / u.meter**3
        result = volume_flow_from_mass_flow_density(m_flow, bulk_density)
        assert result.magnitude == pytest.approx(0.001, rel=1e-3)

    def test_volume_flow_from_mass_flow_density_large_values(self):
        """Test with large values."""
        m_flow = 100000 * u.kilogram / u.second
        bulk_density = 2500 * u.kilogram / u.meter**3
        result = volume_flow_from_mass_flow_density(m_flow, bulk_density)
        assert result.magnitude == pytest.approx(40.0, rel=1e-3)

    def test_volume_flow_from_mass_flow_density_bidirectional_with_original(self):
        """Test that inverse function composes correctly with original."""
        # Given original values
        original_volume_flow = 1.5 * u.meter**3 / u.second
        bulk_density = 1200 * u.kilogram / u.meter**3

        # Calculate mass flow using original function
        m_flow = mass_flow_from_volume_flow_density(original_volume_flow, bulk_density)

        # Recover volume_flow using new inverse function
        recovered_volume_flow = volume_flow_from_mass_flow_density(
            m_flow, bulk_density
        )

        # Should recover original value
        assert recovered_volume_flow.magnitude == pytest.approx(
            original_volume_flow.magnitude, rel=1e-5
        )

    def test_volume_flow_from_mass_flow_density_realistic_scenario(self):
        """Test with realistic conveyor belt parameters."""
        # Typical conveyor belt: 4000 kg/s mass flow with 1600 kg/m³ material
        m_flow = 4000 * u.kilogram / u.second
        bulk_density = 1600 * u.kilogram / u.meter**3
        result = volume_flow_from_mass_flow_density(m_flow, bulk_density)
        assert result.magnitude == pytest.approx(2.5, rel=1e-3)
        # Verify units
        assert result.units == u.meter**3 / u.second
