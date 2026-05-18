import math
import pytest
from eytelwein.belt_conveyor_design.core._distribution_of_belt_tensions_across_belt_width import (
    _compensation_length_at_transition_zone,
    _difference_edge_and_center_belt_tensions_steel_cord_belts,
    _distance_belt_edge_to_pulley_surface_level,
    _length_of_belt_edge_in_transition_zone,
    _maximal_allowable_pulley_lift,
    _mean_belt_tension_related_to_belt_width,
    _local_belt_force_related_to_belt_width,
    _reference_length_of_transition_zone_for_steel_cord_belts,
)
from eytelwein.belt_conveyor_design.core._distribution_of_belt_tensions_across_belt_width import (
    _local_center_belt_force,
    _part_of_belt_lying_on_side_idler,
    _local_edge_belt_force,
)
from eytelwein.belt_conveyor_design.core._distribution_of_belt_tensions_across_belt_width import (
    _minimal_transition_length,
)

from eytelwein.belt_conveyor_design.core._distribution_of_belt_tensions_across_belt_width import (
    _difference_edge_and_center_belt_tensions_textile_belts,
)


def test_mean_belt_tension_positive_values():
    result = _mean_belt_tension_related_to_belt_width(1000.0, 500.0)
    assert result == 2.0


def test_mean_belt_tension_zero_belt_width():
    """Test that zero belt_width raises ValueError."""
    with pytest.raises(ValueError, match="belt_width must be positive"):
        _mean_belt_tension_related_to_belt_width(1000.0, 0.0)


def test_mean_belt_tension_negative_belt_width():
    """Test that negative belt_width raises ValueError."""
    with pytest.raises(ValueError, match="belt_width must be positive"):
        _mean_belt_tension_related_to_belt_width(1000.0, -500.0)


def test_mean_belt_tension_zero_local_belt_tension():
    result = _mean_belt_tension_related_to_belt_width(0.0, 500.0)
    assert result == 0.0


def test_mean_belt_tension_negative_local_belt_tension():
    result = _mean_belt_tension_related_to_belt_width(-1000.0, 500.0)
    assert result == -2.0


def test_local_belt_force_positive_values():
    result = _local_belt_force_related_to_belt_width(2.0, 500.0)
    assert result == 1000.0


def test_local_belt_force_negative_belt_width():
    result = _local_belt_force_related_to_belt_width(2.0, -500.0)
    assert result == -1000.0


def test_local_belt_force_zero_mean_belt_tension():
    result = _local_belt_force_related_to_belt_width(0.0, 500.0)
    assert result == 0.0


def test_local_belt_force_negative_mean_belt_tension():
    result = _local_belt_force_related_to_belt_width(-2.0, 500.0)
    assert result == -1000.0


def test_local_center_belt_force_positive_values():
    result = _local_center_belt_force(10.0, 2.0, 4.0, 6.0)
    assert result == 7.0


def test_local_center_belt_force_zero_belt_width():
    with pytest.raises(ValueError, match="belt_width must be positive"):
        _local_center_belt_force(10.0, 2.0, 0.0, 6.0)


def test_local_center_belt_force_negative_belt_width():
    with pytest.raises(ValueError, match="belt_width must be positive"):
        _local_center_belt_force(10.0, 2.0, -4.0, 6.0)


def test_local_center_belt_force_zero_difference_edge_and_center_belt_tensions():
    result = _local_center_belt_force(10.0, 2.0, 4.0, 0.0)
    assert result == 10.0


def test_local_center_belt_force_negative_difference_edge_and_center_belt_tensions():
    result = _local_center_belt_force(10.0, 2.0, 4.0, -6.0)
    assert result == 13


def test_local_center_belt_force_zero_part_of_belt_lying_on_side_idler():
    result = _local_center_belt_force(10.0, 0.0, 4.0, 6.0)
    assert result == 10.0


def test_local_center_belt_force_negative_part_of_belt_lying_on_side_idler():
    result = _local_center_belt_force(10.0, -2.0, 4.0, 6.0)
    assert result == 13


def test_local_center_belt_force_raises_value_error():
    with pytest.raises(ValueError) as excinfo:
        _local_center_belt_force(10.0, 4.0, 4.0, 11.0)
    assert (
        str(excinfo.value)
        == "The local center belt force shall not be negative. Value: -1.0"
    )


def test_part_of_belt_lying_on_side_idler_positive_values():
    result = _part_of_belt_lying_on_side_idler(10.0, 6.0)
    assert result == 2.0


def test_part_of_belt_lying_on_side_idler_zero_belt_width():
    """Test that zero belt_width is calculated (no validation in private function)."""
    result = _part_of_belt_lying_on_side_idler(0.0, 6.0)
    assert result == -3.0  # (0.0 - 6.0) / 2


def test_part_of_belt_lying_on_side_idler_zero_length_center_roller():
    result = _part_of_belt_lying_on_side_idler(10.0, 0.0)
    assert result == 5.0


def test_part_of_belt_lying_on_side_idler_negative_belt_width():
    """Test that negative belt_width is calculated (no validation in private function)."""
    result = _part_of_belt_lying_on_side_idler(-10.0, 6.0)
    assert result == -8.0  # (-10.0 - 6.0) / 2


def test_part_of_belt_lying_on_side_idler_negative_length_center_roller():
    result = _part_of_belt_lying_on_side_idler(10.0, -6.0)
    assert result == 8.0


def test_part_of_belt_lying_on_side_idler_equal_belt_width_and_length_center_roller():
    result = _part_of_belt_lying_on_side_idler(10.0, 10.0)
    assert result == 0.0


def test_local_edge_belt_force_positive_values():
    result = _local_edge_belt_force(10.0, 5.0)
    assert result == 15.0


def test_local_edge_belt_force_zero_difference_edge_and_center_belt_tensions():
    result = _local_edge_belt_force(10.0, 0.0)
    assert result == 10.0


def test_local_edge_belt_force_negative_difference_edge_and_center_belt_tensions():
    result = _local_edge_belt_force(10.0, -5.0)
    assert result == 5.0


def test_local_edge_belt_force_zero_local_center_belt_force():
    result = _local_edge_belt_force(0.0, 5.0)
    assert result == 5.0


def test_local_edge_belt_force_negative_local_center_belt_force():
    result = _local_edge_belt_force(-10.0, 5.0)
    assert result == -5.0


def test_local_edge_belt_force_both_negative_values():
    result = _local_edge_belt_force(-10.0, -5.0)
    assert result == -15.0


def test_minimal_transition_length_positive_values():
    result = _minimal_transition_length(8.5, 5.0)
    assert result == 42.5  # 8.5 * 5.0


def test_minimal_transition_length_zero_distance():
    result = _minimal_transition_length(2.0, 0.0)
    assert result == 0.0


def test_minimal_transition_length_negative_distance():
    result = _minimal_transition_length(2.0, -5.0)
    assert result == -10.0


def test_minimal_transition_length_zero_coefficient():
    result = _minimal_transition_length(0.0, 5.0)
    assert result == 0.0


def test_minimal_transition_length_negative_coefficient():
    result = _minimal_transition_length(-2.0, 5.0)
    assert result == -10.0


def test_distance_belt_edge_to_pulley_surface_level_positive_values():
    result = _distance_belt_edge_to_pulley_surface_level(10.0, 4.0)
    assert result == 6.0


def test_distance_belt_edge_to_pulley_surface_level_zero_pulley_lift():
    result = _distance_belt_edge_to_pulley_surface_level(10.0, 0.0)
    assert result == 10.0


def test_distance_belt_edge_to_pulley_surface_level_zero_distance():
    result = _distance_belt_edge_to_pulley_surface_level(0.0, 4.0)
    assert result == -4.0


def test_distance_belt_edge_to_pulley_surface_level_negative_distance():
    result = _distance_belt_edge_to_pulley_surface_level(-10.0, 4.0)
    assert result == -14.0


def test_distance_belt_edge_to_pulley_surface_level_negative_pulley_lift():
    result = _distance_belt_edge_to_pulley_surface_level(10.0, -4.0)
    assert result == 14.0


def test_distance_belt_edge_to_pulley_surface_level_both_negative_values():
    result = _distance_belt_edge_to_pulley_surface_level(-10.0, -4.0)
    assert result == -6.0


def test_reference_length_of_transition_zone_positive_values():
    result = _reference_length_of_transition_zone_for_steel_cord_belts(10.0, 5.0)
    assert result == 15.0


def test_reference_length_of_transition_zone_zero_minimal_transition_length():
    result = _reference_length_of_transition_zone_for_steel_cord_belts(0.0, 5.0)
    assert result == 5.0


def test_reference_length_of_transition_zone_zero_compensation_length():
    result = _reference_length_of_transition_zone_for_steel_cord_belts(10.0, 0.0)
    assert result == 10.0


def test_reference_length_of_transition_zone_both_zero():
    result = _reference_length_of_transition_zone_for_steel_cord_belts(0.0, 0.0)
    assert result == 0.0


def test_reference_length_of_transition_zone_negative_minimal_transition_length():
    result = _reference_length_of_transition_zone_for_steel_cord_belts(-10.0, 5.0)
    assert result == -5.0


def test_reference_length_of_transition_zone_negative_compensation_length():
    result = _reference_length_of_transition_zone_for_steel_cord_belts(10.0, -5.0)
    assert result == 5.0


def test_reference_length_of_transition_zone_both_negative():
    result = _reference_length_of_transition_zone_for_steel_cord_belts(-10.0, -5.0)
    assert result == -15.0


def test_compensation_length_at_transition_zone_positive_values():
    result = _compensation_length_at_transition_zone(10.0, 2.0, 6.0)
    assert result == 90 * (10.0 - 2.0) * (1 - 2.0 / (3 * 6.0))


def test_compensation_length_at_transition_zone_zero_pulley_lift():
    result = _compensation_length_at_transition_zone(10.0, 0.0, 6.0)
    assert result == 90 * (10.0 - 0.0) * (1 - 0.0 / (3 * 6.0))


def test_compensation_length_at_transition_zone_zero_distance():
    result = _compensation_length_at_transition_zone(0.0, 2.0, 6.0)
    assert result == 90 * (0.0 - 2.0) * (1 - 2.0 / (3 * 6.0))


def test_compensation_length_at_transition_zone_zero_maximal_allowed_pulley_lift():
    with pytest.raises(ZeroDivisionError):
        _compensation_length_at_transition_zone(10.0, 2.0, 0.0)


def test_compensation_length_at_transition_zone_negative_distance():
    result = _compensation_length_at_transition_zone(-10.0, 2.0, 6.0)
    assert result == 90 * (-10.0 - 2.0) * (1 - 2.0 / (3 * 6.0))


def test_compensation_length_at_transition_zone_negative_pulley_lift():
    result = _compensation_length_at_transition_zone(10.0, -2.0, 6.0)
    assert result == 90 * (10.0 - (-2.0)) * (1 - (-2.0) / (3 * 6.0))


def test_compensation_length_at_transition_zone_negative_maximal_allowed_pulley_lift():
    result = _compensation_length_at_transition_zone(10.0, 2.0, -6.0)
    assert result == 90 * (10.0 - 2.0) * (1 - 2.0 / (3 * -6.0))


def test_compensation_length_at_transition_zone_all_zero():
    result = _compensation_length_at_transition_zone(0.0, 0.0, 1.0)
    assert result == 90 * (0.0 - 0.0) * (1 - 0.0 / (3 * 1.0))


def test_compensation_length_at_transition_zone_all_negative():
    result = _compensation_length_at_transition_zone(-10.0, -2.0, -6.0)
    assert result == 90 * (-10.0 - (-2.0)) * (1 - (-2.0) / (3 * -6.0))


def test_length_of_belt_edge_in_transition_zone_positive_values():
    result = _length_of_belt_edge_in_transition_zone(10.0, 5.0, 3.0, math.radians(30))
    expected = math.sqrt(
        10.0**2
        + 5.0**2
        + 2 * 3.0**2
        - 2
        * 3.0
        * (5.0 * math.sin(math.radians(30)) + 3.0 * math.cos(math.radians(30)))
    )
    assert result == pytest.approx(expected)


def test_length_of_belt_edge_in_transition_zone_zero_values():
    result = _length_of_belt_edge_in_transition_zone(0.0, 0.0, 0.0, 0.0)
    assert result == 0.0


def test_length_of_belt_edge_in_transition_zone_zero_troughing_angle():
    result = _length_of_belt_edge_in_transition_zone(10.0, 5.0, 3.0, 0.0)
    expected = math.sqrt(
        10.0**2
        + 5.0**2
        + 2 * 3.0**2
        - 2 * 3.0 * (5.0 * math.sin(0.0) + 3.0 * math.cos(0.0))
    )
    assert result == pytest.approx(expected)


def test_length_of_belt_edge_in_transition_zone_negative_values():
    result = _length_of_belt_edge_in_transition_zone(
        -10.0, -5.0, -3.0, math.radians(30)
    )
    expected = math.sqrt(
        (-10.0) ** 2
        + (-5.0) ** 2
        + 2 * (-3.0) ** 2
        - 2
        * (-3.0)
        * ((-5.0) * math.sin(math.radians(30)) + (-3.0) * math.cos(math.radians(30)))
    )
    assert result == pytest.approx(expected)


def test_length_of_belt_edge_in_transition_zone_large_values():
    result = _length_of_belt_edge_in_transition_zone(1e6, 1e5, 1e4, math.radians(45))
    expected = math.sqrt(
        (1e6) ** 2
        + (1e5) ** 2
        + 2 * (1e4) ** 2
        - 2
        * (1e4)
        * ((1e5) * math.sin(math.radians(45)) + (1e4) * math.cos(math.radians(45)))
    )
    assert result == pytest.approx(expected)


def test_length_of_belt_edge_in_transition_zone_small_values():
    result = _length_of_belt_edge_in_transition_zone(
        0.001, 0.002, 0.003, math.radians(15)
    )
    expected = math.sqrt(
        0.001**2
        + 0.002**2
        + 2 * 0.003**2
        - 2
        * 0.003
        * (0.002 * math.sin(math.radians(15)) + 0.003 * math.cos(math.radians(15)))
    )
    assert result == pytest.approx(expected)


def test_difference_edge_and_center_belt_tensions_positive_values():
    result = _difference_edge_and_center_belt_tensions_steel_cord_belts(
        12.0, 10.0, 5.0, 1000.0
    )
    assert result == 400.0  # (12.0 - 10.0) * 1000.0 / 5.0


def test_difference_edge_and_center_belt_tensions_zero_length_of_belt_edge():
    result = _difference_edge_and_center_belt_tensions_steel_cord_belts(
        0.0, 10.0, 5.0, 1000.0
    )
    assert result == -2000.0  # (0.0 - 10.0) * 1000.0 / 5.0


def test_difference_edge_and_center_belt_tensions_zero_minimal_transition_length():
    result = _difference_edge_and_center_belt_tensions_steel_cord_belts(
        12.0, 0.0, 5.0, 1000.0
    )
    assert result == 2400.0  # (12.0 - 0.0) * 1000.0 / 5.0


def test_difference_edge_and_center_belt_tensions_zero_reference_length():
    with pytest.raises(ValueError, match="reference_length_of_transition_zone_for_steel_cord_belts"):
        _difference_edge_and_center_belt_tensions_steel_cord_belts(
            12.0, 10.0, 0.0, 1000.0
        )


def test_difference_edge_and_center_belt_tensions_zero_elastic_modulus():
    result = _difference_edge_and_center_belt_tensions_steel_cord_belts(
        12.0, 10.0, 5.0, 0.0
    )
    assert result == 0.0  # (12.0 - 10.0) * 0.0 / 5.0


def test_difference_edge_and_center_belt_tensions_negative_values():
    result = _difference_edge_and_center_belt_tensions_steel_cord_belts(
        -12.0, -10.0, -5.0, -1000.0
    )
    assert result == -400.0  # (-12.0 - (-10.0)) * -1000.0 / -5.0


def test_difference_edge_and_center_belt_tensions_large_values():
    result = _difference_edge_and_center_belt_tensions_steel_cord_belts(
        1e6, 1e5, 1e4, 1e3
    )
    assert result == 90_000.0  # (1e6 - 1e5) * 1e3 / 1e4


def test_difference_edge_and_center_belt_tensions_small_values():
    result = _difference_edge_and_center_belt_tensions_steel_cord_belts(
        0.001, 0.0001, 0.0005, 1000.0
    )
    assert result == 1800  # (0.001 - 0.0001) * 1000.0 / 0.0005


def test_maximal_allowable_pulley_lift_positive_value():
    result = _maximal_allowable_pulley_lift(9.0)
    assert result == pytest.approx(3.0)


def test_maximal_allowable_pulley_lift_zero_value():
    """Test that zero distance raises ValueError."""
    with pytest.raises(ValueError, match="distance_from_edge_to_deepest_trough_level must be positive"):
        _maximal_allowable_pulley_lift(0.0)


def test_maximal_allowable_pulley_lift_negative_value():
    """Test that negative distance raises ValueError."""
    with pytest.raises(ValueError, match="distance_from_edge_to_deepest_trough_level must be positive"):
        _maximal_allowable_pulley_lift(-9.0)


def test_difference_edge_and_center_belt_tensions_textile_belts_positive_values():
    result = _difference_edge_and_center_belt_tensions_textile_belts(
        length_of_belt_edge_in_transition_zone=10.0,
        minimal_transition_length=5.0,
        elastic_modulus=200.0,
    )
    assert result == pytest.approx((10.0 - 5.0) * 200.0 / 5.0)


def test_difference_edge_and_center_belt_tensions_textile_belts_zero_minimal_transition_length():
    with pytest.raises(
        ValueError, match="minimal_transition_length"
    ):
        _difference_edge_and_center_belt_tensions_textile_belts(
            length_of_belt_edge_in_transition_zone=10.0,
            minimal_transition_length=0.0,
            elastic_modulus=200.0,
        )


def test_difference_edge_and_center_belt_tensions_textile_belts_negative_values():
    result = _difference_edge_and_center_belt_tensions_textile_belts(
        length_of_belt_edge_in_transition_zone=-10.0,
        minimal_transition_length=5.0,
        elastic_modulus=200.0,
    )
    assert result == pytest.approx((-10.0 - 5.0) * 200.0 / 5.0)


def test_difference_edge_and_center_belt_tensions_textile_belts_zero_length_of_belt_edge():
    result = _difference_edge_and_center_belt_tensions_textile_belts(
        length_of_belt_edge_in_transition_zone=0.0,
        minimal_transition_length=5.0,
        elastic_modulus=200.0,
    )
    assert result == pytest.approx((0.0 - 5.0) * 200.0 / 5.0)


def test_difference_edge_and_center_belt_tensions_textile_belts_zero_elastic_modulus():
    result = _difference_edge_and_center_belt_tensions_textile_belts(
        length_of_belt_edge_in_transition_zone=10.0,
        minimal_transition_length=5.0,
        elastic_modulus=0.0,
    )
    assert result == 0.0
