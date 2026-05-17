import pytest
import math
from eytelwein.main.units import get_unit_registry
from eytelwein.din_22101.core.design_layout_of_drive_system import (
    height_difference_from_section_length_and_inclination_angle,
)

from eytelwein.din_22101.core.design_layout_of_drive_system import (
    angle_of_inclination_from_height_difference_and_section_length,
)
from eytelwein.din_22101.core.design_layout_of_drive_system import (
    section_length_from_height_difference_and_inclination_angle,
)


# Get the unit registry
u = get_unit_registry()


class TestHeightDifferenceFromSectionLengthAndInclinationAngle:
    def test_horizontal_section(self):
        """Test with horizontal section (0 degrees)."""
        section_length = 100 * u.meter
        inclination_angle = 0 * u.degree

        result = height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: section_length * sin(0) = 100 * 0 = 0
        expected = 0 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-6)
        assert result.units == expected.units

    def test_vertical_section(self):
        """Test with vertical section (90 degrees)."""
        section_length = 100 * u.meter
        inclination_angle = 90 * u.degree

        result = height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: section_length * sin(90°) = 100 * 1 = 100
        expected = 100 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-6)
        assert result.units == expected.units

    def test_inclined_section(self):
        """Test with inclined section (30 degrees)."""
        section_length = 100 * u.meter
        inclination_angle = 30 * u.degree

        result = height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: section_length * sin(30°) = 100 * 0.5 = 50
        expected = 50 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-6)
        assert result.units == expected.units

    def test_negative_angle(self):
        """Test with negative inclination angle (declining section)."""
        section_length = 100 * u.meter
        inclination_angle = -30 * u.degree

        result = height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: section_length * sin(-30°) = 100 * (-0.5) = -50
        expected = -50 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-6)
        assert result.units == expected.units

    def test_zero_length(self):
        """Test with zero section length."""
        section_length = 0 * u.meter
        inclination_angle = 45 * u.degree

        result = height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: 0 * sin(45°) = 0
        expected = 0 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-6)
        assert result.units == expected.units

    def test_different_length_unit(self):
        """Test with different input length unit."""
        section_length = 100 * u.feet
        inclination_angle = 30 * u.degree

        result = height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: section_length * sin(30°) = 100 * 0.5 = 50 feet = 15.24 meters
        expected_meters = 15.24 * u.meter
        assert result.magnitude == pytest.approx(expected_meters.magnitude, abs=1e-2)
        assert result.units == expected_meters.units

    def test_different_angle_unit(self):
        """Test with different input angle unit."""
        section_length = 100 * u.meter
        inclination_angle = math.pi / 6 * u.radian  # equivalent to 30 degrees

        result = height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle
        )

        # Expected: section_length * sin(30°) = 100 * 0.5 = 50
        expected = 50 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-6)
        assert result.units == expected.units

    def test_custom_output_unit(self):
        """Test with custom output unit."""
        section_length = 100 * u.meter
        inclination_angle = 30 * u.degree

        result = height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle, unit="feet"
        )

        # Expected: 50 meters = 164.04 feet
        expected = 164.04 * u.feet
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-2)
        assert result.units == expected.units

    def test_custom_precision(self):
        """Test with custom precision."""
        section_length = 100 * u.meter
        inclination_angle = 30 * u.degree

        result = height_difference_from_section_length_and_inclination_angle(
            section_length, inclination_angle, precision=1
        )

        # Expected: 50 meters rounded to 1 decimal place
        expected = 50.0 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-6)
        assert result.units == expected.units
        assert str(result.magnitude).endswith(
            ".0"
        )  # Check it's rounded to 1 decimal place

    def test_invalid_length_unit(self):
        """Test with invalid length unit."""
        section_length = 100 * u.second  # time unit, not length
        inclination_angle = 30 * u.degree

        with pytest.raises(ValueError, match="Error in converting units"):
            height_difference_from_section_length_and_inclination_angle(
                section_length, inclination_angle
            )

    def test_invalid_angle_unit(self):
        """Test with invalid angle unit."""
        section_length = 100 * u.meter
        inclination_angle = 30 * u.meter  # length unit, not angle

        with pytest.raises(ValueError, match="Error in converting units"):
            height_difference_from_section_length_and_inclination_angle(
                section_length, inclination_angle
            )

    def test_negative_length(self):
        """Test with negative section length."""
        section_length = -100 * u.meter
        inclination_angle = 30 * u.degree

        with pytest.raises(ValueError, match="Section length must be non-negative"):
            height_difference_from_section_length_and_inclination_angle(
                section_length, inclination_angle
            )

    def test_invalid_output_unit(self):
        """Test with invalid output unit."""
        section_length = 100 * u.meter
        inclination_angle = 30 * u.degree

        with pytest.raises(ValueError, match="Invalid unit"):
            height_difference_from_section_length_and_inclination_angle(
                section_length, inclination_angle, unit="invalid_unit"
            )


class TestAngleOfInclinationFromHeightDifferenceAndSectionLength:
    def test_level_section(self):
        """Test with level section (0 height difference)."""
        height_difference = 0 * u.meter
        section_length = 100 * u.meter

        result = angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )

        # Expected: asin(0/100) = 0 radians (0 degrees)
        expected = 0 * u.radian
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-6)
        assert result.units == expected.units

    def test_vertical_section(self):
        """Test with vertical section (height = length)."""
        height_difference = 100 * u.meter
        section_length = 100 * u.meter

        result = angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )
        # Expected: asin(100/100) = asin(1) = pi/2 radians (90 degrees)
        expected = (math.pi / 2) * u.radian
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units

    def test_inclined_section(self):
        """Test with inclined section (30 degrees)."""
        height_difference = 50 * u.meter
        section_length = 100 * u.meter

        result = angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )
        # Expected: asin(50/100) = asin(0.5) = pi/6 radians (30 degrees)
        expected = (math.pi / 6) * u.radian
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units

    def test_declining_section(self):
        """Test with declining section (-30 degrees)."""
        height_difference = -50 * u.meter
        section_length = 100 * u.meter

        result = angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )
        # Expected: asin(-50/100) = asin(-0.5) = -pi/6 radians (-30 degrees)
        expected = -(math.pi / 6) * u.radian
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units

    def test_real_values(self):
        """Test with real-world values."""
        height_difference = 18 * u.meter
        section_length = 4303 * u.meter

        result = angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )
        # Expected: asin(18/4303) ≈ 0.00418 radians
        expected = 0.00418 * u.radian
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units

    def test_different_length_units(self):
        """Test with different input length units."""
        height_difference = 15 * u.feet
        section_length = 100 * u.feet

        result = angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )
        # Expected: asin(15/100) = asin(0.15) ≈ 0.150798 radians
        expected = 0.150798 * u.radian
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units

    def test_mixed_length_units(self):
        """Test with mixed input length units."""
        height_difference = 5 * u.meter
        section_length = 50 * u.feet

        result = angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length
        )

        # Expected: asin(5/15.24) = asin(0.328) ≈ 0.334 radians
        # 50 feet ≈ 15.24 meters
        expected = 0.334 * u.radian
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units

    def test_output_in_degrees(self):
        """Test with output in degrees."""
        height_difference = 50 * u.meter
        section_length = 100 * u.meter

        result = angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length, unit="degree"
        )

        # Expected: asin(50/100) = asin(0.5) = 30 degrees
        expected = 30 * u.degree
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-6)
        assert result.units == expected.units

    def test_custom_precision(self):
        """Test with custom precision."""
        height_difference = 50 * u.meter
        section_length = 100 * u.meter

        result = angle_of_inclination_from_height_difference_and_section_length(
            height_difference, section_length, precision=1
        )

        # Expected: 0.5236 radians rounded to 1 decimal place = 0.5
        assert str(result.magnitude).endswith(".5")

    def test_invalid_length_unit(self):
        """Test with invalid length unit."""
        height_difference = 50 * u.second  # time unit, not length
        section_length = 100 * u.meter

        with pytest.raises(ValueError, match="Error in converting units"):
            angle_of_inclination_from_height_difference_and_section_length(
                height_difference, section_length
            )

    def test_invalid_output_unit(self):
        """Test with invalid output unit."""
        height_difference = 50 * u.meter
        section_length = 100 * u.meter

        with pytest.raises(ValueError, match="Invalid angle unit"):
            angle_of_inclination_from_height_difference_and_section_length(
                height_difference,
                section_length,
                unit="meter",  # length unit, not angle
            )

    def test_zero_section_length(self):
        """Test with zero section length."""
        height_difference = 50 * u.meter
        section_length = 0 * u.meter

        with pytest.raises(ValueError, match="Section length must be positive"):
            angle_of_inclination_from_height_difference_and_section_length(
                height_difference, section_length
            )

    def test_negative_section_length(self):
        """Test with negative section length."""
        height_difference = 50 * u.meter
        section_length = -100 * u.meter

        with pytest.raises(ValueError, match="Section length must be positive"):
            angle_of_inclination_from_height_difference_and_section_length(
                height_difference, section_length
            )

    def test_height_exceeds_length(self):
        """Test with height difference exceeding section length."""
        height_difference = 150 * u.meter
        section_length = 100 * u.meter

        with pytest.raises(
            ValueError, match="Height difference .* cannot exceed section length"
        ):
            angle_of_inclination_from_height_difference_and_section_length(
                height_difference, section_length
            )


class TestSectionLengthFromHeightDifferenceAndInclinationAngle:
    def test_vertical_section(self):
        """Test with vertical section (90 degrees)."""
        height_difference = 100 * u.meter
        inclination_angle = 90 * u.degree

        result = section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )

        # Expected: height_difference / sin(90°) = 100 / 1 = 100
        expected = 100 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units

    def test_inclined_section(self):
        """Test with inclined section (30 degrees)."""
        height_difference = 50 * u.meter
        inclination_angle = 30 * u.degree

        result = section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )

        # Expected: height_difference / sin(30°) = 50 / 0.5 = 100
        expected = 100 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units

    def test_declining_section(self):
        """Test with declining section (-30 degrees)."""
        height_difference = 50 * u.meter
        inclination_angle = -30 * u.degree

        result = section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )

        # Expected: height_difference / sin(-30°) = 50 / (-0.5) = -100
        expected = -100 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units

    def test_zero_height(self):
        """Test with zero height difference."""
        height_difference = 0 * u.meter
        inclination_angle = 45 * u.degree

        result = section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )

        # Expected: 0 / sin(45°) = 0
        expected = 0 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units

    def test_real_values(self):
        """Test with real-world values."""
        height_difference = 18 * u.meter
        inclination_angle = 0.00418 * u.radian

        result = section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )
        # Expected: height_difference / sin(0.00418) ≈ 18 / 0.00418 ≈ 4303
        expected = 4303 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=5.0)
        assert result.units == expected.units

    def test_different_height_unit(self):
        """Test with different input height unit."""
        height_difference = 50 * u.feet
        inclination_angle = 30 * u.degree

        result = section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )
        # Expected: 50 feet / sin(30°) = 50 feet / 0.5 = 100 feet
        expected_feet = 100 * u.feet
        # Convert the result to feet for comparison
        result_feet = result.to(u.feet)
        assert result_feet.magnitude == pytest.approx(expected_feet.magnitude, abs=1e-1)
        assert result_feet.units == expected_feet.units

    def test_different_angle_unit(self):
        """Test with different input angle unit."""
        height_difference = 50 * u.meter
        inclination_angle = math.pi / 6 * u.radian  # equivalent to 30 degrees

        result = section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle
        )

        # Expected: 50 / sin(30°) = 50 / 0.5 = 100
        expected = 100 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units

    def test_custom_output_unit(self):
        """Test with custom output unit."""
        height_difference = 50 * u.meter
        inclination_angle = 30 * u.degree

        result = section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle, unit="feet"
        )

        # Expected: 100 meters = 328.08 feet
        expected = 328.08 * u.feet
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-2)
        assert result.units == expected.units

    def test_custom_precision(self):
        """Test with custom precision."""
        height_difference = 50 * u.meter
        inclination_angle = 30 * u.degree

        result = section_length_from_height_difference_and_inclination_angle(
            height_difference, inclination_angle, precision=1
        )

        # Expected: 100 meters rounded to 1 decimal place
        expected = 100.0 * u.meter
        assert result.magnitude == pytest.approx(expected.magnitude, abs=1e-3)
        assert result.units == expected.units
        assert str(result.magnitude).endswith(
            ".0"
        )  # Check it's rounded to 1 decimal place

    def test_invalid_height_unit(self):
        """Test with invalid height unit."""
        height_difference = 50 * u.second  # time unit, not length
        inclination_angle = 30 * u.degree

        with pytest.raises(ValueError, match="Error in converting units"):
            section_length_from_height_difference_and_inclination_angle(
                height_difference, inclination_angle
            )

    def test_invalid_angle_unit(self):
        """Test with invalid angle unit."""
        height_difference = 50 * u.meter
        inclination_angle = 30 * u.meter  # length unit, not angle

        with pytest.raises(ValueError, match="Error in converting units"):
            section_length_from_height_difference_and_inclination_angle(
                height_difference, inclination_angle
            )

    def test_negative_height(self):
        """Test with negative height difference."""
        height_difference = -50 * u.meter
        inclination_angle = 30 * u.degree

        with pytest.raises(ValueError, match="Height difference must be non-negative"):
            section_length_from_height_difference_and_inclination_angle(
                height_difference, inclination_angle
            )

    def test_zero_angle(self):
        """Test with zero inclination angle."""
        height_difference = 50 * u.meter
        inclination_angle = 0 * u.degree

        with pytest.raises(
            ValueError, match="Inclination angle cannot be zero or very close to zero"
        ):
            section_length_from_height_difference_and_inclination_angle(
                height_difference, inclination_angle
            )

    def test_nearly_zero_angle(self):
        """Test with nearly zero inclination angle."""
        height_difference = 50 * u.meter
        inclination_angle = 1e-11 * u.radian

        with pytest.raises(
            ValueError, match="Inclination angle cannot be zero or very close to zero"
        ):
            section_length_from_height_difference_and_inclination_angle(
                height_difference, inclination_angle
            )

    def test_invalid_output_unit(self):
        """Test with invalid output unit."""
        height_difference = 50 * u.meter
        inclination_angle = 30 * u.degree

        with pytest.raises(ValueError, match="Invalid unit"):
            section_length_from_height_difference_and_inclination_angle(
                height_difference, inclination_angle, unit="invalid_unit"
            )
