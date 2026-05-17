import math

import pytest
from pint import Quantity
from eytelwein.belt_conveyor_design.extended.volume_flow_mass_flow import (
    required_skirtboard_height_from_cross_section,
    get_usable_belt_width_from_skirt_board_width,
    convert_equivalent_angle_of_slope_to_surcharge_angle,
    convert_surcharge_angle_to_equivalent_angle_of_slope,
    convert_surcharge_angles,
    maximal_cross_section_skirt_board_known_geometry,
    get_material_bed_depth,
    material_bed_width,
)
from eytelwein.belt_conveyor_design.extended._volume_flow_mass_flow import (
    _get_usable_belt_width_from_skirt_board_width,
)

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


class TestMaximalCrossSectionSkirtBoardKnownGeometry:
    def test_maximal_cross_section_skirt_board_known_geometry_happy_path(self):
        center_roll_length = Quantity(459, u.millimeter)
        skirt_board_width = Quantity(813, u.millimeter)
        skirt_board_height = Quantity(60, u.millimeter)
        troughing_angle = Quantity(35, u.degree)
        equivalent_slope_angle = Quantity(13.639, u.degree)
        result = maximal_cross_section_skirt_board_known_geometry(
            center_roll_length,
            skirt_board_width,
            skirt_board_height,
            troughing_angle,
            equivalent_slope_angle,
        )
        assert result.magnitude == pytest.approx(167225.472, rel=1e3)

    def test_maximal_cross_section_skirt_board_known_geometry_invalid_unit(self):
        center_roll_length = Quantity(100, u.millimeter)
        skirt_board_width = Quantity(50, u.millimeter)
        skirt_board_height = Quantity(20, u.millimeter)
        troughing_angle = Quantity(30, u.degree)
        equivalent_slope_angle = Quantity(10, u.degree)
        with pytest.raises(ValueError, match="Invalid unit"):
            maximal_cross_section_skirt_board_known_geometry(
                center_roll_length,
                skirt_board_width,
                skirt_board_height,
                troughing_angle,
                equivalent_slope_angle,
                unit="invalid_unit",
            )

    def test_maximal_cross_section_skirt_board_known_geometry_invalid_unit_passing(
        self,
    ):
        center_roll_length = Quantity(100, u.kilogram)
        skirt_board_width = Quantity(50, u.millimeter)
        skirt_board_height = Quantity(20, u.millimeter)
        troughing_angle = Quantity(30, u.degree)
        equivalent_slope_angle = Quantity(10, u.degree)
        with pytest.raises(ValueError, match="Error in converting"):
            maximal_cross_section_skirt_board_known_geometry(
                center_roll_length,
                skirt_board_width,
                skirt_board_height,
                troughing_angle,
                equivalent_slope_angle,
            )

    def test_maximal_cross_section_skirt_board_known_geometry_negative_cross_section(
        self,
    ):
        center_roll_length = Quantity(-1000, u.millimeter)
        skirt_board_width = Quantity(-50, u.millimeter)
        skirt_board_height = Quantity(-20, u.millimeter)
        troughing_angle = Quantity(30, u.degree)
        equivalent_slope_angle = Quantity(10, u.degree)
        with pytest.raises(
            ValueError,
            match="Calculated cross-section area is negative, which is physically impossible.",
        ):
            maximal_cross_section_skirt_board_known_geometry(
                center_roll_length,
                skirt_board_width,
                skirt_board_height,
                troughing_angle,
                equivalent_slope_angle,
            )

    def test_maximal_cross_section_skirt_board_known_geometry_zero_values(self):
        center_roll_length = Quantity(0, u.millimeter)
        skirt_board_width = Quantity(0, u.millimeter)
        skirt_board_height = Quantity(0, u.millimeter)
        troughing_angle = Quantity(0, u.degree)
        equivalent_slope_angle = Quantity(0, u.degree)
        result = maximal_cross_section_skirt_board_known_geometry(
            center_roll_length,
            skirt_board_width,
            skirt_board_height,
            troughing_angle,
            equivalent_slope_angle,
        )
        assert result.magnitude == 0


class TestRequiredSkirtboardHeightFromCrossSection:
    def test_required_skirtboard_height_from_cross_section(self):
        result = required_skirtboard_height_from_cross_section(
            459 * u.millimeter,
            813 * u.millimeter,
            35.0 * u.degree,
            13.639 * u.degree,
            167225.472 * u.millimeter**2,
        )
        assert result.magnitude == pytest.approx(60.17, rel=1e-1)

    def test_required_skirtboard_height_from_cross_section_zero_values(self):
        result = required_skirtboard_height_from_cross_section(
            0.0 * u.millimeter,
            0.0 * u.millimeter,
            0.0 * u.degree,
            0.0 * u.degree,
            0.0 * u.millimeter**2,
        )
        assert result.magnitude == 0.0

    def test_required_skirtboard_height_from_cross_section_negative_values(self):
        with pytest.raises(
            ValueError, match="Calculated skirt board height is negative"
        ):
            required_skirtboard_height_from_cross_section(
                459 * u.millimeter,
                -813 * u.millimeter,
                35.0 * u.degree,
                13.639 * u.degree,
                167225.472 * u.millimeter**2,
            )

    def test_required_skirtboard_height_from_cross_section_invalid_unit(self):
        with pytest.raises(ValueError, match="Invalid unit"):
            required_skirtboard_height_from_cross_section(
                459 * u.millimeter,
                813 * u.millimeter,
                35.0 * u.degree,
                13.639 * u.degree,
                167225.472 * u.millimeter**2,
                unit="invalid_unit",
            )


class TestUsableBeltWidthFromSkirts:
    def test_get_usable_belt_width_from_skirt_board_width_happy_path(self):
        result = get_usable_belt_width_from_skirt_board_width(
            Quantity(800, u.millimeter),
            Quantity(450, u.millimeter),
            Quantity(35.0, u.degree),
        )
        assert result.magnitude == pytest.approx(877, rel=1e-3)

    def test_get_usable_belt_width_from_skirt_board_width_zero_values(self):
        result = get_usable_belt_width_from_skirt_board_width(
            Quantity(0.0, u.millimeter),
            Quantity(0.0, u.millimeter),
            Quantity(0.0, u.degree),
        )
        assert result.magnitude == 0.0

    def test_get_usable_belt_width_from_skirt_board_width_flat(self):
        result = get_usable_belt_width_from_skirt_board_width(
            Quantity(800, u.millimeter),
            Quantity(450, u.millimeter),
            Quantity(0.0, u.degree),
        )
        assert result.magnitude == pytest.approx(800, rel=1e-3)

    def test_get_usable_belt_width_from_skirt_board_width_negative_values(self):
        with pytest.raises(
            ValueError,
            match="Calculated skirt board height is negative, which is physically impossible.",
        ):
            get_usable_belt_width_from_skirt_board_width(
                Quantity(-800, u.millimeter),
                Quantity(-450, u.millimeter),
                Quantity(-35.0, u.degree),
            )

    def test_get_usable_belt_width_from_skirt_board_width_invalid_unit(self):
        with pytest.raises(ValueError, match="Invalid unit"):
            get_usable_belt_width_from_skirt_board_width(
                Quantity(800, u.millimeter),
                Quantity(450, u.millimeter),
                Quantity(35.0, u.degree),
                unit="invalid_unit",
            )

    def test_public_matches_private_happy_path(self):
        """Public wrapper must produce the same result as the private function."""
        skirt_board_width = 800.0
        center_roll_length = 450.0
        troughing_angle_deg = 35.0

        private_result = _get_usable_belt_width_from_skirt_board_width(
            skirt_board_width, center_roll_length, math.radians(troughing_angle_deg)
        )
        public_result = get_usable_belt_width_from_skirt_board_width(
            skirt_board_width=Quantity(skirt_board_width, u.millimeter),
            center_roll_length=Quantity(center_roll_length, u.millimeter),
            troughing_angle=Quantity(troughing_angle_deg, u.degree),
        )
        assert public_result.magnitude == pytest.approx(private_result, rel=1e-5)

    def test_public_matches_private_flat(self):
        """Flat belt (0° troughing): public and private must agree."""
        skirt_board_width = 1200.0
        center_roll_length = 600.0

        private_result = _get_usable_belt_width_from_skirt_board_width(
            skirt_board_width, center_roll_length, 0.0
        )
        public_result = get_usable_belt_width_from_skirt_board_width(
            skirt_board_width=Quantity(skirt_board_width, u.millimeter),
            center_roll_length=Quantity(center_roll_length, u.millimeter),
            troughing_angle=Quantity(0.0, u.degree),
        )
        assert public_result.magnitude == pytest.approx(private_result, rel=1e-5)
        # For a flat belt the usable width equals the skirt board width
        assert public_result.magnitude == pytest.approx(skirt_board_width, rel=1e-5)

    def test_public_matches_private_various_angles(self):
        """Public and private must agree across a range of troughing angles."""
        skirt_board_width = 1000.0
        center_roll_length = 500.0
        for angle_deg in [0.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0]:
            private_result = _get_usable_belt_width_from_skirt_board_width(
                skirt_board_width,
                center_roll_length,
                math.radians(angle_deg),
            )
            public_result = get_usable_belt_width_from_skirt_board_width(
                skirt_board_width=Quantity(skirt_board_width, u.millimeter),
                center_roll_length=Quantity(center_roll_length, u.millimeter),
                troughing_angle=Quantity(angle_deg, u.degree),
            )
            assert public_result.magnitude == pytest.approx(
                private_result, rel=1e-5
            ), f"Mismatch at {angle_deg}°"

    def test_keyword_args_match_positional(self):
        """Keyword arguments must map to the correct private-function parameters."""
        result_kw = get_usable_belt_width_from_skirt_board_width(
            skirt_board_width=Quantity(800, u.millimeter),
            center_roll_length=Quantity(450, u.millimeter),
            troughing_angle=Quantity(35.0, u.degree),
        )
        result_pos = get_usable_belt_width_from_skirt_board_width(
            Quantity(800, u.millimeter),
            Quantity(450, u.millimeter),
            Quantity(35.0, u.degree),
        )
        assert result_kw.magnitude == pytest.approx(result_pos.magnitude, rel=1e-10)


class TestConvertSurchargeAngles:
    def test_convert_equivalent_angle_of_slope_to_surcharge_angle_happy_path(self):
        result = convert_equivalent_angle_of_slope_to_surcharge_angle(
            Quantity(20.0, u.degree)
        )
        assert result.magnitude == pytest.approx(28.633, rel=1e-2)

    def test_convert_equivalent_angle_of_slope_to_surcharge_angle_zero_values(self):
        result = convert_equivalent_angle_of_slope_to_surcharge_angle(
            Quantity(0.0, u.degree)
        )
        assert result.magnitude == 0.0

    def test_convert_surcharge_angle_to_equivalent_angle_of_slope(self):
        result = convert_surcharge_angle_to_equivalent_angle_of_slope(
            Quantity(20.0, u.degree)
        )
        assert result.magnitude == pytest.approx(13.639, rel=1e-2)

    def test_convert_surcharge_angle_to_equivalent_angle_of_slope_zero_values(self):
        result = convert_surcharge_angle_to_equivalent_angle_of_slope(
            Quantity(0.0, u.degree)
        )
        assert result.magnitude == 0.0

    def test_convert_surcharge_angles(self):
        result = convert_surcharge_angles(
            slope_angle=Quantity(20.0, u.degree)
        )
        assert result["slope_angle"]["value"] == 20.0
        assert result["surcharge_angle"]["value"] == pytest.approx(28.633, rel=1e-2)

    def test_convert_surcharge_angles_other_way(self):
        result = convert_surcharge_angles(
            surcharge_angle=Quantity(20.0, u.degree)
        )
        assert result["surcharge_angle"]["value"] == 20.0
        assert result["slope_angle"]["value"] == pytest.approx(13.639, rel=1e-2)

    def test_convert_surcharge_angles_no_input(self):
        with pytest.raises(
            ValueError,
            match="Either equivalent_slope_angle or surcharge_angle must be set.",
        ):
            convert_surcharge_angles()

    def test_convert_surcharge_angles_both_inputs(self):
        with pytest.raises(
            ValueError,
            match="Either equivalent_slope_angle or surcharge_angle must be set.",
        ):
            convert_surcharge_angles(
                slope_angle=Quantity(20.0, u.degree),
                surcharge_angle=Quantity(20.0, u.degree),
            )


class TestGetMaterialBedDepth:
    def test_get_material_bed_depth_standard_case(self):
        # Test with typical values
        result = get_material_bed_depth(
            length_of_material_on_side_roll=u.Quantity(300.0, u.millimeter),
            troughing_angle=u.Quantity(35.0, u.degree),
            center_roll_length=u.Quantity(500.0, u.millimeter),
            slope_angle=u.Quantity(20.0, u.degree),
        )
        assert result.magnitude == pytest.approx(352.54, rel=1e-2)
        assert result.units == u.millimeter

    def test_get_material_bed_depth_flat_troughing(self):
        # Test with zero troughing angle (flat belt)
        result = get_material_bed_depth(
            length_of_material_on_side_roll=u.Quantity(300.0, u.millimeter),
            troughing_angle=u.Quantity(0.0, u.degree),
            center_roll_length=u.Quantity(500.0, u.millimeter),
            slope_angle=u.Quantity(20.0, u.degree),
        )
        assert result.magnitude == pytest.approx(200.2, rel=1e-2)
        assert result.units == u.millimeter

    def test_get_material_bed_depth_zero_slope(self):
        # Test with zero slope angle
        result = get_material_bed_depth(
            length_of_material_on_side_roll=u.Quantity(300.0, u.millimeter),
            troughing_angle=u.Quantity(35.0, u.degree),
            center_roll_length=u.Quantity(500.0, u.millimeter),
            slope_angle=u.Quantity(0.0, u.degree),
        )
        assert result.magnitude == pytest.approx(172.08, rel=1e-2)
        assert result.units == u.millimeter

    def test_get_material_bed_depth_unit_conversion(self):
        # Test unit conversion - input in meters, output in cm
        result = get_material_bed_depth(
            length_of_material_on_side_roll=u.Quantity(0.3, u.meter),
            troughing_angle=u.Quantity(35.0, u.degree),
            center_roll_length=u.Quantity(0.5, u.meter),
            slope_angle=u.Quantity(20.0, u.degree),
            unit="centimeter",
        )
        assert result.magnitude == pytest.approx(35.25, rel=1e-2)
        assert result.units == u.centimeter

    def test_get_material_bed_depth_with_precision(self):
        # Test precision parameter
        result = get_material_bed_depth(
            length_of_material_on_side_roll=u.Quantity(300.0, u.millimeter),
            troughing_angle=u.Quantity(35.0, u.degree),
            center_roll_length=u.Quantity(500.0, u.millimeter),
            slope_angle=u.Quantity(20.0, u.degree),
            precision=0,
        )
        assert result.magnitude == 353.0  # Rounded to 0 decimal places

    def test_get_material_bed_depth_mixed_units(self):
        # Test with mixed units
        result = get_material_bed_depth(
            length_of_material_on_side_roll=u.Quantity(0.3, u.meter),
            troughing_angle=u.Quantity(35.0, u.degree),
            center_roll_length=u.Quantity(500.0, u.millimeter),
            slope_angle=u.Quantity(20.0, u.degree),
        )
        assert result.magnitude == pytest.approx(352.54, rel=1e-2)
        assert result.units == u.millimeter


class TestMaterialBedWidth:
    """Test suite for material_bed_width public function"""

    def test_material_bed_width_normal_case(self):
        """Test with typical input values"""
        result = material_bed_width(
            center_roll_length=Quantity(500.0, u.millimeter),
            length_of_material_cover_on_wing_roll=Quantity(300.0, u.millimeter),
            troughing_angle=Quantity(35.0, u.degree),
        )
        # Expected: 500 + 2 * cos(35°) * 300 = 991.52 mm
        assert result.magnitude == pytest.approx(991.52, rel=1e-2)
        assert result.units == u.millimeter

    def test_material_bed_width_unit_conversion_to_cm(self):
        """Test unit conversion - input in mm, output in cm"""
        result = material_bed_width(
            center_roll_length=Quantity(500.0, u.millimeter),
            length_of_material_cover_on_wing_roll=Quantity(300.0, u.millimeter),
            troughing_angle=Quantity(35.0, u.degree),
            unit="centimeter",
        )
        # Expected: 991.52 mm = 99.152 cm
        assert result.magnitude == pytest.approx(99.152, rel=1e-2)
        assert result.units == u.centimeter

    def test_material_bed_width_unit_conversion_to_meter(self):
        """Test unit conversion - input in mm, output in meter"""
        result = material_bed_width(
            center_roll_length=Quantity(500.0, u.millimeter),
            length_of_material_cover_on_wing_roll=Quantity(300.0, u.millimeter),
            troughing_angle=Quantity(35.0, u.degree),
            unit="meter",
        )
        # Expected: 991.52 mm = 0.99152 m
        assert result.magnitude == pytest.approx(0.99152, rel=1e-2)
        assert result.units == u.meter

    def test_material_bed_width_mixed_input_units(self):
        """Test with mixed input units"""
        result = material_bed_width(
            center_roll_length=Quantity(0.5, u.meter),
            length_of_material_cover_on_wing_roll=Quantity(300.0, u.millimeter),
            troughing_angle=Quantity(35.0, u.degree),
        )
        # Should convert everything to mm and calculate
        assert result.magnitude == pytest.approx(991.52, rel=1e-2)
        assert result.units == u.millimeter

    def test_material_bed_width_with_precision(self):
        """Test precision parameter"""
        result = material_bed_width(
            center_roll_length=Quantity(500.0, u.millimeter),
            length_of_material_cover_on_wing_roll=Quantity(300.0, u.millimeter),
            troughing_angle=Quantity(35.0, u.degree),
            precision=1,
        )
        # Result should be rounded to 1 decimal place
        assert result.magnitude == pytest.approx(991.5, abs=0.1)

    def test_material_bed_width_zero_angle(self):
        """Test with zero troughing angle (flat belt)"""
        result = material_bed_width(
            center_roll_length=Quantity(500.0, u.millimeter),
            length_of_material_cover_on_wing_roll=Quantity(300.0, u.millimeter),
            troughing_angle=Quantity(0.0, u.degree),
        )
        # Expected: 500 + 2 * cos(0°) * 300 = 500 + 600 = 1100 mm
        assert result.magnitude == pytest.approx(1100.0, rel=1e-2)

    def test_material_bed_width_90_degree_angle(self):
        """Test with 90 degree troughing angle"""
        result = material_bed_width(
            center_roll_length=Quantity(500.0, u.millimeter),
            length_of_material_cover_on_wing_roll=Quantity(300.0, u.millimeter),
            troughing_angle=Quantity(90.0, u.degree),
        )
        # Expected: 500 + 2 * cos(90°) * 300 = 500 mm
        assert result.magnitude == pytest.approx(500.0, rel=1e-2)

    def test_material_bed_width_large_conveyors(self):
        """Test with large conveyor dimensions"""
        result = material_bed_width(
            center_roll_length=Quantity(2000.0, u.millimeter),
            length_of_material_cover_on_wing_roll=Quantity(500.0, u.millimeter),
            troughing_angle=Quantity(35.0, u.degree),
        )
        # Expected: 2000 + 2 * cos(35°) * 500 = 2819.2 mm
        assert result.magnitude == pytest.approx(2819.2, rel=1e-2)

    def test_material_bed_width_invalid_output_unit(self):
        """Test that invalid output unit raises ValueError"""
        with pytest.raises(ValueError, match="Invalid unit"):
            material_bed_width(
                center_roll_length=Quantity(500.0, u.millimeter),
                length_of_material_cover_on_wing_roll=Quantity(300.0, u.millimeter),
                troughing_angle=Quantity(35.0, u.degree),
                unit="invalid_unit",
            )

    def test_material_bed_width_invalid_input_unit(self):
        """Test that invalid input unit raises ValueError"""
        with pytest.raises(ValueError, match="Error in converting"):
            material_bed_width(
                center_roll_length=Quantity(500.0, u.kilogram),
                length_of_material_cover_on_wing_roll=Quantity(300.0, u.millimeter),
                troughing_angle=Quantity(35.0, u.degree),
            )

    def test_material_bed_width_radian_angles(self):
        """Test with angles specified in radians"""
        import math

        result = material_bed_width(
            center_roll_length=Quantity(500.0, u.millimeter),
            length_of_material_cover_on_wing_roll=Quantity(300.0, u.millimeter),
            troughing_angle=Quantity(math.radians(35.0), u.radian),
        )
        # Should give same result as 35 degrees
        assert result.magnitude == pytest.approx(991.52, rel=1e-2)

    def test_material_bed_width_negative_result_raises_error(self):
        """Test that negative result raises ValueError (physically impossible)"""
        with pytest.raises(ValueError, match="physically impossible"):
            material_bed_width(
                center_roll_length=Quantity(-1000.0, u.millimeter),
                length_of_material_cover_on_wing_roll=Quantity(-500.0, u.millimeter),
                troughing_angle=Quantity(35.0, u.degree),
            )
