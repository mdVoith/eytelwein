from eytelwein.belt_conveyor_design.constants import PulleyLoadFactor
from eytelwein.belt_conveyor_design.core._minimum_pulley_diameter import (
    _get_max_width_related_tension_at_group_A_pulleys,
)


def test_max_width_tension_above_60_up_to_100():
    result = _get_max_width_related_tension_at_group_A_pulleys(
        800, PulleyLoadFactor.above_60_up_to_100
    )
    assert result == 100.0


def test_max_width_tension_above_100():
    result = _get_max_width_related_tension_at_group_A_pulleys(
        800, PulleyLoadFactor.above_100
    )
    assert result == 140.0


def test_max_width_tension_default_value():
    result = _get_max_width_related_tension_at_group_A_pulleys(800)
    assert result == 100.0


def test_max_width_tension_zero_strength():
    result = _get_max_width_related_tension_at_group_A_pulleys(
        0, PulleyLoadFactor.above_60_up_to_100
    )
    assert result == 0.0


def test_max_width_tension_negative_strength():
    result = _get_max_width_related_tension_at_group_A_pulleys(
        -800, PulleyLoadFactor.above_60_up_to_100
    )
    assert result == -100.0
