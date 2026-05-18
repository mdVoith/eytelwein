import pytest
import math
from eytelwein.belt_conveyor_design.core._design_layout_of_drive_system import (
    _height_difference_from_section_length_and_inclination_angle,
    _angle_of_inclination_from_height_difference_and_section_length,
    _section_length_from_height_difference_and_inclination_angle,
)


class TestHeightDifferenceFromSectionLengthAndInclinationAngle:
    def test_inclined_section_real_values(self):
        """Test with inclined section (30 degrees)."""
        section_length = 4303.0  # meters
        inclination_angle = 0.00418  # radians

        result = _height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        expected = 18.0  # meters
        assert result == pytest.approx(expected, abs=1e-1)

    def test_horizontal_section(self):
        """Test with horizontal section (0 degrees)."""
        section_length = 100.0  # meters
        inclination_angle = 0.0  # radians (0 degrees)

        result = _height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: section_length * sin(0) = 100 * 0 = 0
        expected = 0.0
        assert result == pytest.approx(expected, abs=1e-6)

    def test_vertical_section(self):
        """Test with vertical section (90 degrees)."""
        section_length = 100.0  # meters
        inclination_angle = math.pi / 2  # radians (90 degrees)

        result = _height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: section_length * sin(90°) = 100 * 1 = 100
        expected = 100.0
        assert result == pytest.approx(expected, abs=1e-6)

    def test_inclined_section(self):
        """Test with inclined section (30 degrees)."""
        section_length = 100.0  # meters
        inclination_angle = math.pi / 6  # radians (30 degrees)

        result = _height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: section_length * sin(30°) = 100 * 0.5 = 50
        expected = 50.0
        assert result == pytest.approx(expected, abs=1e-6)

    def test_negative_angle(self):
        """Test with negative inclination angle (declining section)."""
        section_length = 100.0  # meters
        inclination_angle = -math.pi / 6  # radians (-30 degrees)

        result = _height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: section_length * sin(-30°) = 100 * (-0.5) = -50
        expected = -50.0
        assert result == pytest.approx(expected, abs=1e-6)

    def test_zero_length(self):
        """Test with zero section length."""
        section_length = 0.0  # meters
        inclination_angle = math.pi / 4  # radians (45 degrees)

        result = _height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: 0 * sin(45°) = 0
        expected = 0.0
        assert result == pytest.approx(expected, abs=1e-6)


class TestAngleOfInclinationFromHeightDifferenceAndSectionLength:
    def test_level_section(self):
        """Test with level section (0 height difference)."""
        height_difference = 0.0  # meters
        section_length = 100.0  # meters

        result = _angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )

        # Expected: asin(0/100) = 0 radians (0 degrees)
        expected = 0.0
        assert result == pytest.approx(expected, abs=1e-6)

    def test_vertical_section(self):
        """Test with vertical section (height = length)."""
        height_difference = 100.0  # meters
        section_length = 100.0  # meters

        result = _angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )

        # Expected: asin(100/100) = asin(1) = pi/2 radians (90 degrees)
        expected = math.pi / 2
        assert result == pytest.approx(expected, abs=1e-6)

    def test_inclined_section(self):
        """Test with inclined section (30 degrees)."""
        height_difference = 50.0  # meters
        section_length = 100.0  # meters

        result = _angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )

        # Expected: asin(50/100) = asin(0.5) = pi/6 radians (30 degrees)
        expected = math.pi / 6
        assert result == pytest.approx(expected, abs=1e-6)

    def test_declining_section(self):
        """Test with declining section (-30 degrees)."""
        height_difference = -50.0  # meters
        section_length = 100.0  # meters

        result = _angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )

        # Expected: asin(-50/100) = asin(-0.5) = -pi/6 radians (-30 degrees)
        expected = -math.pi / 6
        assert result == pytest.approx(expected, abs=1e-6)

    def test_real_values(self):
        """Test with real-world values."""
        height_difference = 18.0  # meters
        section_length = 4303.0  # meters

        result = _angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )

        # Expected: asin(18/4303) ≈ 0.00418 radians
        expected = 0.00418
        assert result == pytest.approx(expected, abs=1e-5)

    def test_zero_section_length(self):
        """Test that zero section_length raises ValueError."""
        with pytest.raises(ValueError, match="section_length must be positive"):
            _angle_of_inclination_from_height_difference_and_section_length(
                10.0, 0.0
            )

    def test_negative_section_length(self):
        """Test that negative section_length raises ValueError."""
        with pytest.raises(ValueError, match="section_length must be positive"):
            _angle_of_inclination_from_height_difference_and_section_length(
                10.0, -1.0
            )


class TestSectionLengthFromHeightDifferenceAndInclinationAngle:
    def test_vertical_section(self):
        """Test with vertical section (90 degrees)."""
        height_difference = 100.0  # meters
        inclination_angle = math.pi / 2  # radians (90 degrees)

        result = _section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )

        # Expected: height_difference / sin(90°) = 100 / 1 = 100
        expected = 100.0
        assert result == pytest.approx(expected, abs=1e-6)

    def test_inclined_section(self):
        """Test with inclined section (30 degrees)."""
        height_difference = 50.0  # meters
        inclination_angle = math.pi / 6  # radians (30 degrees)

        result = _section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )

        # Expected: height_difference / sin(30°) = 50 / 0.5 = 100
        expected = 100.0
        assert result == pytest.approx(expected, abs=1e-6)

    def test_declining_section(self):
        """Test with declining section (-30 degrees)."""
        height_difference = 50.0  # meters
        inclination_angle = -math.pi / 6  # radians (-30 degrees)

        result = _section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )

        # Expected: height_difference / sin(-30°) = 50 / (-0.5) = -100
        expected = -100.0
        assert result == pytest.approx(expected, abs=1e-6)

    def test_zero_height(self):
        """Test with zero height difference."""
        height_difference = 0.0  # meters
        inclination_angle = math.pi / 4  # radians (45 degrees)

        result = _section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )

        # Expected: 0 / sin(45°) = 0
        expected = 0.0
        assert result == pytest.approx(expected, abs=1e-6)

    def test_real_values(self):
        """Test with real-world values."""
        height_difference = 18.0  # meters
        inclination_angle = 0.00418  # radians

        result = _section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )  # Expected: height_difference / sin(0.00418) ≈ 18 / 0.00418 ≈ 4303
        expected = 4303.0
        assert result == pytest.approx(expected, abs=5.0)

    def test_zero_inclination_angle(self):
        """Test that zero inclination_angle raises ValueError."""
        with pytest.raises(ValueError, match="sin\\(inclination_angle\\) cannot be zero"):
            _section_length_from_height_difference_and_inclination_angle(
                10.0, 0.0
            )

    def test_pi_inclination_angle(self):
        """Test that pi inclination_angle raises ValueError (sin(pi) = 0)."""
        with pytest.raises(ValueError, match="sin\\(inclination_angle\\) cannot be zero"):
            _section_length_from_height_difference_and_inclination_angle(
                10.0, math.pi
            )
