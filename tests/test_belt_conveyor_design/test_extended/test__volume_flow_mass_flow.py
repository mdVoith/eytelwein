import pytest
import math

from eytelwein.belt_conveyor_design.extended._volume_flow_mass_flow import (
    _maximal_cross_section_skirt_board_known_geometry,
    _get_usable_belt_width_from_skirt_board_width,
    _required_skirtboard_height_from_cross_section,
    _convert_equivalent_angle_of_slope_to_surcharge_angle,
    _convert_surcharge_angle_to_equivalent_angle_of_slope,
    _convert_surcharge_angles,
    _get_material_bed_depth,
    _material_bed_width,
)


class TestCrossSectionSkirtBoardKnownGeometry:
    def test_cross_section_skirt_board_known_geometry(self):
        result = _maximal_cross_section_skirt_board_known_geometry(
            459, 813, 60, math.radians(35.0), math.radians(13.639)
        )
        assert result == pytest.approx(167225.472, rel=1e3)

    def test_cross_section_skirt_board_known_geometry_zero_values(self):
        result = _maximal_cross_section_skirt_board_known_geometry(
            0.0, 0.0, 0.0, 0.0, 0.0
        )
        assert result == 0.0


class TestRequiredSkirtboardHeightFromCrossSection:
    def test_required_skirtboard_height_from_cross_section(self):
        result = _required_skirtboard_height_from_cross_section(
            459, 813, math.radians(35.0), math.radians(13.639), 167225.472
        )
        assert result == pytest.approx(60.17, rel=1e-1)

    def test_required_skirtboard_height_from_cross_section_zero_values(self):
        result = _required_skirtboard_height_from_cross_section(0.0, 0.0, 0.0, 0.0, 0.0)
        assert result == 0.0


class TestUsableBeltWidthFromSkirts:
    def test_get_usable_belt_width_from_skirt_board_width_happy_path(self):
        result = _get_usable_belt_width_from_skirt_board_width(
            800, 450, math.radians(35.0)
        )
        assert result == pytest.approx(877, rel=1e-3)

    def test_get_usable_belt_width_from_skirt_board_width_zero_values(self):
        result = _get_usable_belt_width_from_skirt_board_width(0.0, 0.0, 0.0)
        assert result == 0.0

    def test_get_usable_belt_width_from_skirt_board_width_flat(self):
        result = _get_usable_belt_width_from_skirt_board_width(800, 450, 0.0)
        assert result == pytest.approx(800, rel=1e-3)


class TestConvertSurchargeAngles:
    def test_convert_equivalent_angle_of_slope_to_surcharge_angle_happy_path(self):
        result = _convert_equivalent_angle_of_slope_to_surcharge_angle(
            math.radians(20.0)
        )
        assert result == pytest.approx(math.radians(28.633), rel=1e-2)

    def test_convert_equivalent_angle_of_slope_to_surcharge_angle_zero_values(self):
        result = _convert_equivalent_angle_of_slope_to_surcharge_angle(0.0)
        assert result == 0.0

    def test_convert_surcharge_angle_to_equivalent_angle_of_slope(self):
        result = _convert_surcharge_angle_to_equivalent_angle_of_slope(
            math.radians(20.0)
        )
        assert result == pytest.approx(math.radians(13.639), rel=1e-2)

    def test_convert_surcharge_angle_to_equivalent_angle_of_slope_zero_values(self):
        result = _convert_surcharge_angle_to_equivalent_angle_of_slope(0.0)
        assert result == 0.0

    def test_convert_surcharge_angles(self):
        result = _convert_surcharge_angles(
            slope_angle_rad=math.radians(20.0)
        )
        assert result["slope_angle"] == math.radians(20.0)
        assert result["surcharge_angle"] == pytest.approx(math.radians(28.633), rel=1e-2)

    def test_convert_surcharge_angles_other_way(self):
        result = _convert_surcharge_angles(
            surcharge_angle_rad=math.radians(20.0)
        )
        assert result["surcharge_angle"] == math.radians(20.0)
        assert result["slope_angle"] == pytest.approx(math.radians(13.639), rel=1e-2)

    def test_convert_surcharge_angles_no_input(self):
        with pytest.raises(
            ValueError,
            match="Either equivalent_slope_angle or surcharge_angle must be set.",
        ):
            _convert_surcharge_angles()

    def test_convert_surcharge_angles_both_inputs(self):
        with pytest.raises(
            ValueError,
            match="Either equivalent_slope_angle or surcharge_angle must be set.",
        ):
            _convert_surcharge_angles(
                slope_angle_rad=math.radians(20.0),
                surcharge_angle_rad=math.radians(20.0),
            )


class TestGetMaterialBedDepth:
    def test_get_material_bed_depth_standard_case(self):
        # Test with typical values
        result = _get_material_bed_depth(
            length_of_material_on_side_roll=300.0,  # 300 mm
            troughing_angle_rad=math.radians(35.0),  # 35 degrees in radians
            center_roll_length=500.0,  # 500 mm
            slope_angle_rad=math.radians(20.0),  # 20 degrees in radians
        )
        # Expected: material_on_side_roll * sin(troughing_angle) + (center_roll/2 + material_on_side_roll * cos(troughing_angle)) * tan(slope_angle)
        # = 300 * sin(35°) + (250 + 300 * cos(35°)) * tan(20°)
        # = 300 * 0.5736 + (250 + 300 * 0.8192) * 0.3640
        # = 172.08 + (250 + 245.76) * 0.3640
        # = 172.08 + 495.76 * 0.3640
        # = 172.08 + 180.46
        # = 352.54
        expected = 352.54
        assert result == pytest.approx(expected, rel=1e-2)

    def test_get_material_bed_depth_flat_troughing(self):
        # Test with zero troughing angle (flat belt)
        result = _get_material_bed_depth(
            length_of_material_on_side_roll=300.0,
            troughing_angle_rad=0.0,
            center_roll_length=500.0,
            slope_angle_rad=math.radians(20.0),
        )
        # With zero troughing angle, the sin term becomes zero
        # Expected: (center_roll/2 + material_on_side_roll) * tan(slope_angle)
        # = (250 + 300) * tan(20°)
        # = 550 * 0.3640
        # = 200.2
        expected = 200.2
        assert result == pytest.approx(expected, rel=1e-2)

    def test_get_material_bed_depth_zero_slope(self):
        # Test with zero slope angle
        result = _get_material_bed_depth(
            length_of_material_on_side_roll=300.0,
            troughing_angle_rad=math.radians(35.0),
            center_roll_length=500.0,
            slope_angle_rad=0.0,
        )
        # With zero slope angle, the tangent term becomes zero
        # Expected: material_on_side_roll * sin(troughing_angle)
        # = 300 * sin(35°)
        # = 300 * 0.5736
        # = 172.08
        expected = 172.08
        assert result == pytest.approx(expected, rel=1e-2)

    def test_get_material_bed_depth_zero_material_on_side(self):
        # Test with no material on side roll
        result = _get_material_bed_depth(
            length_of_material_on_side_roll=0.0,
            troughing_angle_rad=math.radians(35.0),
            center_roll_length=500.0,
            slope_angle_rad=math.radians(20.0),
        )
        # With zero material on side roll, both sine and cosine terms involving it become zero
        # Expected: (center_roll/2) * tan(slope_angle)
        # = 250 * tan(20°)
        # = 250 * 0.3640
        # = 91.0
        expected = 91.0
        assert result == pytest.approx(expected, rel=1e-2)

    def test_get_material_bed_depth_all_zeros(self):
        # Test with all zeros (edge case)
        result = _get_material_bed_depth(0.0, 0.0, 0.0, 0.0)
        assert result == 0.0


class TestMaterialBedWidth:
    """Test suite for _material_bed_width function"""

    def test_material_bed_width_normal_case(self):
        """Test with typical input values"""
        # center_roll_length = 500 mm
        # length_of_material_cover_on_wing_roll = 300 mm
        # troughing_angle = 35 degrees = 0.6109 rad
        # Expected: 500 + 2 * cos(35°) * 300
        #         = 500 + 2 * 0.8192 * 300
        #         = 500 + 491.52
        #         = 991.52 mm
        result = _material_bed_width(500.0, 300.0, math.radians(35.0))
        assert result == pytest.approx(991.52, rel=1e-2)

    def test_material_bed_width_second_normal_case(self):
        """Test with typical input values"""
        # center_roll_length = 0.692 m
        # length_of_material_cover_on_wing_roll = 0.417 m
        # troughing_angle = 35 degrees = 0.6109 rad
        # Expected: 692 + 2 * cos(35°) * 417
        #         = 692 + 2 * 0.8192 * 417
        #         = 692 + 683.52
        #         = 1375.52 mm
        result = _material_bed_width(0.692, 0.417, math.radians(35.0))
        assert result == pytest.approx(1.37552, rel=1e-2)

    def test_material_bed_width_zero_angle(self):
        """Test with zero troughing angle (flat belt)"""
        # When angle = 0, cos(0) = 1
        # Expected: 500 + 2 * 1 * 300 = 500 + 600 = 1100 mm
        result = _material_bed_width(500.0, 300.0, 0.0)
        assert result == pytest.approx(1100.0, rel=1e-2)

    def test_material_bed_width_90_degree_angle(self):
        """Test with 90 degree troughing angle"""
        # When angle = 90°, cos(90°) = 0
        # Expected: 500 + 2 * 0 * 300 = 500 mm
        result = _material_bed_width(500.0, 300.0, math.radians(90.0))
        assert result == pytest.approx(500.0, rel=1e-2)

    def test_material_bed_width_zero_material_cover(self):
        """Test with zero material cover on wing roll"""
        # Expected: center_roll_length + 2 * cos(angle) * 0 = center_roll_length
        result = _material_bed_width(500.0, 0.0, math.radians(35.0))
        assert result == pytest.approx(500.0, rel=1e-2)

    def test_material_bed_width_zero_center_roll(self):
        """Test with zero center roll length"""
        # Expected: 0 + 2 * cos(35°) * 300 = 491.52 mm
        result = _material_bed_width(0.0, 300.0, math.radians(35.0))
        assert result == pytest.approx(491.52, rel=1e-2)

    def test_material_bed_width_all_zeros(self):
        """Test with all zero values"""
        result = _material_bed_width(0.0, 0.0, 0.0)
        assert result == 0.0

    def test_material_bed_width_large_values(self):
        """Test with large conveyor dimensions"""
        # center_roll_length = 2000 mm
        # length_of_material_cover_on_wing_roll = 500 mm
        # angle = 35°
        # Expected: 2000 + 2 * cos(35°) * 500 = 2000 + 819.2 = 2819.2 mm
        result = _material_bed_width(2000.0, 500.0, math.radians(35.0))
        assert result == pytest.approx(2819.2, rel=1e-2)

    def test_material_bed_width_small_values(self):
        """Test with very small conveyor dimensions"""
        # center_roll_length = 10 mm
        # length_of_material_cover_on_wing_roll = 5 mm
        # angle = 35°
        result = _material_bed_width(10.0, 5.0, math.radians(35.0))
        expected = 10.0 + 2 * math.cos(math.radians(35.0)) * 5.0
        assert result == pytest.approx(expected, rel=1e-2)

    def test_material_bed_width_various_angles(self):
        """Test with different angles to verify formula"""
        center_roll = 500.0
        material_cover = 300.0

        # Test multiple angles
        for angle_deg in [15, 25, 35, 45, 55]:
            angle_rad = math.radians(angle_deg)
            result = _material_bed_width(center_roll, material_cover, angle_rad)
            expected = center_roll + 2 * math.cos(angle_rad) * material_cover
            assert result == pytest.approx(expected, rel=1e-6)
