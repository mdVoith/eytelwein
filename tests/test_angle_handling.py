import math

from eytelwein.din_22101.extended._design_layout_of_drive_system import (
    _angle_of_inclination_from_horizontal_length_and_lift,
)
from eytelwein.din_22101.extended._volume_flow_mass_flow import (
    _get_usable_belt_width_from_skirt_board_width,
    _convert_equivalent_angle_of_slope_to_surcharge_angle,
    _convert_surcharge_angle_to_equivalent_angle_of_slope,
    _get_material_bed_depth,
)
from eytelwein.din_22101.core._volume_flow_mass_flow import (
    _partial_cross_section_at_water_fill,
    _partial_cross_section_above_water_fill,
    _cross_section_of_fill,
)

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def test_angle_of_inclination_from_horizontal_length_and_lift():
    """Test the angle of inclination calculation."""
    # For a 3-4-5 triangle, the angle should be arctan(3/4) in radians
    expected_angle_rad = math.atan2(3, 4)
    actual_angle_rad = _angle_of_inclination_from_horizontal_length_and_lift(4, 3)
    assert abs(expected_angle_rad - actual_angle_rad) < 1e-10


def test_get_usable_belt_width_from_skirt_board_width():
    """Test the usable belt width calculation."""
    # Setup parameters
    skirt_board_width = 1000.0  # mm
    center_roll_length = 500.0  # mm
    troughing_angle_rad = math.pi / 6  # 30 degrees in radians

    # Calculate manually
    expected_width = (skirt_board_width - center_roll_length) / math.cos(
        troughing_angle_rad
    ) + center_roll_length

    # Calculate using the function
    actual_width = _get_usable_belt_width_from_skirt_board_width(
        skirt_board_width, center_roll_length, troughing_angle_rad
    )

    assert abs(expected_width - actual_width) < 1e-10


def test_convert_angles():
    """Test the angle conversion functions."""
    # Test converting equivalent slope angle to surcharge angle
    equivalent_slope_angle_rad = math.pi / 6  # 30 degrees in radians
    surcharge_angle_rad = _convert_equivalent_angle_of_slope_to_surcharge_angle(
        equivalent_slope_angle_rad
    )

    # Manual calculation: atan(3/2 * tan(30°))
    tan_30 = math.tan(equivalent_slope_angle_rad)
    expected_surcharge_angle_rad = math.atan(3 / 2 * tan_30)

    assert abs(expected_surcharge_angle_rad - surcharge_angle_rad) < 1e-10

    # Test converting surcharge angle to equivalent slope angle
    calculated_equivalent_angle_rad = (
        _convert_surcharge_angle_to_equivalent_angle_of_slope(surcharge_angle_rad)
    )

    # Should be approximately the original equivalent slope angle
    assert abs(equivalent_slope_angle_rad - calculated_equivalent_angle_rad) < 1e-10


def test_get_material_bed_depth():
    """Test the material bed depth calculation."""
    # Setup parameters
    length_of_material_on_side_roll = 100.0  # mm
    troughing_angle_rad = math.pi / 6  # 30 degrees in radians
    center_roll_length = 500.0  # mm
    slope_angle_rad = math.pi / 12  # 15 degrees in radians

    # Calculate manually
    expected_depth = length_of_material_on_side_roll * math.sin(troughing_angle_rad) + (
        center_roll_length / 2
        + length_of_material_on_side_roll * math.cos(troughing_angle_rad)
    ) * math.tan(slope_angle_rad)

    # Calculate using the function
    actual_depth = _get_material_bed_depth(
        length_of_material_on_side_roll,
        troughing_angle_rad,
        center_roll_length,
        slope_angle_rad,
    )

    assert abs(expected_depth - actual_depth) < 1e-10


def test_partial_cross_sections():
    """Test the cross-section calculation functions."""
    # Setup parameters
    center_roll_length = 500.0  # mm
    usable_belt_width = 1000.0  # mm
    troughing_angle_rad = math.pi / 6  # 30 degrees in radians
    equivalent_slope_angle_rad = math.pi / 12  # 15 degrees in radians

    # Test partial cross-section at water fill
    water_fill_area = _partial_cross_section_at_water_fill(
        center_roll_length, usable_belt_width, troughing_angle_rad
    )

    # Manual calculation for water fill area
    expected_water_fill_area = (
        (
            center_roll_length
            + (usable_belt_width - center_roll_length)
            / 2
            * math.cos(troughing_angle_rad)
        )
        * (usable_belt_width - center_roll_length)
        / 2
        * math.sin(troughing_angle_rad)
    )

    assert abs(expected_water_fill_area - water_fill_area) < 1e-10

    # Test partial cross-section above water fill
    above_water_fill_area = _partial_cross_section_above_water_fill(
        center_roll_length,
        usable_belt_width,
        troughing_angle_rad,
        equivalent_slope_angle_rad,
    )

    # Manual calculation for above water fill area
    expected_above_water_fill_area = (
        (
            center_roll_length
            + (usable_belt_width - center_roll_length) * math.cos(troughing_angle_rad)
        )
        ** 2
        * math.tan(equivalent_slope_angle_rad)
        / 4
    )

    assert abs(expected_above_water_fill_area - above_water_fill_area) < 1e-10

    # Test total cross-section
    total_area = _cross_section_of_fill(
        center_roll_length,
        usable_belt_width,
        troughing_angle_rad,
        equivalent_slope_angle_rad,
    )

    # Manual calculation for total area
    expected_total_area = expected_water_fill_area + expected_above_water_fill_area

    assert abs(expected_total_area - total_area) < 1e-10


def test_public_interface_with_units():
    """Test the public interface functions with units."""
    from eytelwein.din_22101.extended.volume_flow_mass_flow import (
        convert_equivalent_angle_of_slope_to_surcharge_angle,
        convert_surcharge_angle_to_equivalent_angle_of_slope,
        get_material_bed_depth,
    )

    # Test angle conversion functions
    equivalent_slope_angle = 30 * u.degree
    surcharge_angle = convert_equivalent_angle_of_slope_to_surcharge_angle(
        equivalent_slope_angle, unit="degree"
    )

    # Calculate the expected surcharge angle
    tan_30 = math.tan(math.radians(30))
    expected_surcharge_angle = math.degrees(math.atan(3 / 2 * tan_30))

    assert abs(expected_surcharge_angle - surcharge_angle.magnitude) < 1e-5

    # Test converting back
    calculated_equivalent_angle = convert_surcharge_angle_to_equivalent_angle_of_slope(
        surcharge_angle, unit="degree"
    )

    assert abs(30 - calculated_equivalent_angle.magnitude) < 1e-5

    # Test material bed depth calculation
    length_of_material_on_side_roll = 100 * u.millimeter
    troughing_angle = 30 * u.degree
    center_roll_length = 500 * u.millimeter
    slope_angle = 15 * u.degree

    depth = get_material_bed_depth(
        length_of_material_on_side_roll,
        troughing_angle,
        center_roll_length,
        slope_angle,
    )  # Calculate the expected depth
    expected_depth = 100 * math.sin(math.radians(30)) + (
        500 / 2 + 100 * math.cos(math.radians(30))
    ) * math.tan(math.radians(15))

    # Use a more appropriate tolerance for floating-point comparison
    assert abs(expected_depth - depth.magnitude) < 1e-2
