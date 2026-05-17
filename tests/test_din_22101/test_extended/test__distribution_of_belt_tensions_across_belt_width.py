import math
import pytest
from eytelwein.din_22101.extended._distribution_of_belt_tensions_across_belt_width import (
    _distance_belt_edge_deepest_level_of_trough,
)


def test_distance_belt_edge_deepest_level_of_trough_positive_values():
    result = _distance_belt_edge_deepest_level_of_trough(10.0, math.radians(30))
    assert result == pytest.approx(10.0 * math.sin(math.radians(30)))


def test_distance_belt_edge_deepest_level_of_trough_zero_angle():
    result = _distance_belt_edge_deepest_level_of_trough(10.0, 0.0)
    assert result == 0.0


def test_distance_belt_edge_deepest_level_of_trough_zero_part_of_belt():
    result = _distance_belt_edge_deepest_level_of_trough(0.0, math.radians(30))
    assert result == 0.0


def test_distance_belt_edge_deepest_level_of_trough_negative_part_of_belt():
    result = _distance_belt_edge_deepest_level_of_trough(-10.0, math.radians(30))
    assert result == pytest.approx(-10.0 * math.sin(math.radians(30)))


def test_distance_belt_edge_deepest_level_of_trough_negative_angle():
    result = _distance_belt_edge_deepest_level_of_trough(10.0, math.radians(-30))
    assert result == pytest.approx(10.0 * math.sin(math.radians(-30)))


def test_distance_belt_edge_deepest_level_of_trough_both_negative():
    result = _distance_belt_edge_deepest_level_of_trough(-10.0, math.radians(-30))
    assert result == pytest.approx(-10.0 * math.sin(math.radians(-30)))
