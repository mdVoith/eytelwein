"""Tests for private raw-float helpers in extended mass inertia module."""

import pytest

from eytelwein.belt_conveyor_design.extended._mass_inertia import (
    _translating_mass_from_line_load_and_segment_length,
    _translating_mass_idler_carry,
    _translating_mass_idler_return,
    _translating_mass_belt,
    _translating_mass_material,
    _total_translating_mass_empty,
    _total_translating_mass,
    _drive_pulley_radius_from_drive_pulley_diameter,
    _translating_mass_inertia_at_pulley_shaft,
    _reflected_translating_mass_inertia_at_motor_shaft,
    _component_inertia_referred_to_motor_shaft,
    _total_motor_shaft_rotational_inertia_from_equivalent_component_inertias,
    _total_motor_shaft_rotational_inertia_from_native_component_inertias,
    _motor_shaft_rotational_inertia_per_drive,
)


def test_translating_mass_from_line_load_and_segment_length_basic() -> None:
    result = _translating_mass_from_line_load_and_segment_length(10.0, 100.0)
    assert result == pytest.approx(1000.0)


def test_translating_mass_specialized_functions_delegate_to_primitive() -> None:
    line_load = 25.0
    segment_length = 80.0
    expected = _translating_mass_from_line_load_and_segment_length(
        line_load, segment_length
    )
    assert _translating_mass_idler_carry(line_load, segment_length) == expected
    assert _translating_mass_idler_return(line_load, segment_length) == expected
    assert _translating_mass_belt(line_load, segment_length) == expected
    assert _translating_mass_material(line_load, segment_length) == expected


def test_total_translating_mass_empty_basic() -> None:
    result = _total_translating_mass_empty(18503.0, 6168.0, 111393.9125)
    assert result == pytest.approx(247458.825, rel=0.005)


def test_total_translating_mass_basic() -> None:
    result = _total_translating_mass(247458.825, 536584.1)
    assert result == pytest.approx(784042.925, rel=0.005)


def test_drive_pulley_radius_from_drive_pulley_diameter_basic() -> None:
    result = _drive_pulley_radius_from_drive_pulley_diameter(1.04)
    assert result == pytest.approx(0.52)


def test_translating_mass_inertia_at_pulley_shaft_basic() -> None:
    result = _translating_mass_inertia_at_pulley_shaft(100.0, 0.5)
    assert result == pytest.approx(25.0)


def test_reflected_translating_mass_inertia_at_motor_shaft_basic() -> None:
    result = _reflected_translating_mass_inertia_at_motor_shaft(1000.0, 1.0, 2.0)
    assert result == pytest.approx(250.0)


def test_component_inertia_referred_to_motor_shaft_basic() -> None:
    result = _component_inertia_referred_to_motor_shaft(1.2, 0.5)
    assert result == pytest.approx(0.3)


def test_total_motor_shaft_rotational_inertia_from_equivalent_component_inertias() -> None:
    result = _total_motor_shaft_rotational_inertia_from_equivalent_component_inertias(
        486.227552,
        10.0,
        5.0,
        2.0,
    )
    assert result == pytest.approx(503.227552)


def test_total_motor_shaft_rotational_inertia_from_native_component_inertias() -> None:
    result = _total_motor_shaft_rotational_inertia_from_native_component_inertias(
        486.227552,
        40.0,
        0.5,
        20.0,
        0.5,
        8.0,
        0.5,
    )
    assert result == pytest.approx(503.227552)


def test_motor_shaft_rotational_inertia_per_drive_basic() -> None:
    result = _motor_shaft_rotational_inertia_per_drive(503.227552, 2)
    assert result == pytest.approx(251.613776)
