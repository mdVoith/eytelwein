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
    _translating_mass_inertia_at_pulley_circumference,
    _mass_inertia_at_pulley_shaft,
    _reflected_translating_mass_inertia_at_motor_shaft,
    _component_inertia_referred_to_motor_shaft,
    _total_motor_shaft_rotational_inertia_from_equivalent_component_inertias,
    _total_motor_shaft_rotational_inertia_from_native_component_inertias,
    _low_speed_native_component_inertia_at_motor_shaft,
    _high_speed_native_component_inertia_at_motor_shaft,
    _fluid_coupling_inertia_referred_to_motor_shaft,
    _total_rotational_inertia_at_motor_shaft,
    _total_rotational_inertia_at_fluid_coupling_shaft,
    _rotational_inertia_breakdown_at_motor_shaft,
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


def test_translating_mass_inertia_at_pulley_circumference_basic() -> None:
    result = _translating_mass_inertia_at_pulley_circumference(100.0, 0.5)
    assert result == pytest.approx(25.0)


def test_mass_inertia_at_pulley_shaft_zero_native_inertia() -> None:
    """With zero native pulley inertia, should equal translating-only."""
    translating_only = _translating_mass_inertia_at_pulley_circumference(100.0, 0.5)
    result = _mass_inertia_at_pulley_shaft(100.0, 0.5, pulley_inertia_native_kg_m2=0.0)
    assert result == pytest.approx(translating_only)
    assert result == pytest.approx(25.0)


def test_mass_inertia_at_pulley_shaft_nonzero_native_inertia() -> None:
    """With nonzero native pulley inertia, should sum correctly."""
    translating_only = _translating_mass_inertia_at_pulley_circumference(100.0, 0.5)
    native_inertia = 5.0
    result = _mass_inertia_at_pulley_shaft(
        100.0, 0.5, pulley_inertia_native_kg_m2=native_inertia
    )
    assert result == pytest.approx(translating_only + native_inertia)
    assert result == pytest.approx(30.0)


def test_mass_inertia_at_pulley_shaft_negative_native_inertia_raises() -> None:
    with pytest.raises(ValueError, match="pulley_inertia_native_kg_m2"):
        _mass_inertia_at_pulley_shaft(100.0, 0.5, pulley_inertia_native_kg_m2=-1.0)


def test_reflected_translating_mass_inertia_at_motor_shaft_basic() -> None:
    result = _reflected_translating_mass_inertia_at_motor_shaft(1000.0, 1.0, 2.0)
    assert result == pytest.approx(250.0)


def test_component_inertia_referred_to_motor_shaft_basic() -> None:
    result = _component_inertia_referred_to_motor_shaft(1.2, 2.0)
    assert result == pytest.approx(0.3)


def test_total_motor_shaft_rotational_inertia_from_equivalent_component_inertias() -> (
    None
):
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
        2.0,
        20.0,
        8.0,
    )
    assert result == pytest.approx(503.227552)


def test_motor_shaft_rotational_inertia_per_drive_basic() -> None:
    result = _motor_shaft_rotational_inertia_per_drive(503.227552, 2)
    assert result == pytest.approx(251.613776)


def test_low_speed_native_component_inertia_requires_ratio_when_positive() -> None:
    with pytest.raises(ValueError, match="pulley_gear_ratio_motor_to_component"):
        _low_speed_native_component_inertia_at_motor_shaft(
            pulley_inertia_native_kg_m2=10.0,
        )


def test_layered_total_rotational_inertia_at_motor_shaft_mixed_components() -> None:
    low_speed = _low_speed_native_component_inertia_at_motor_shaft(
        pulley_inertia_native_kg_m2=40.0,
        pulley_gear_ratio_motor_to_component=2.0,
        low_speed_coupling_inertia_native_kg_m2=20.0,
        low_speed_coupling_gear_ratio_motor_to_component=2.0,
        low_speed_brake_inertia_native_kg_m2=8.0,
        low_speed_brake_gear_ratio_motor_to_component=2.0,
    )
    high_speed = _high_speed_native_component_inertia_at_motor_shaft(
        high_speed_coupling_inertia_native_kg_m2=3.0,
        high_speed_brake_inertia_native_kg_m2=2.0,
        fluid_coupling_inertia_native_kg_m2=4.0,
    )
    total = _total_rotational_inertia_at_motor_shaft(
        reflected_translating_mass_inertia_kg_m2=486.227552,
        gearbox_inertia_at_motor_shaft_kg_m2=10.0,
        low_speed_native_component_inertia_at_motor_shaft_kg_m2=low_speed,
        high_speed_native_component_inertia_at_motor_shaft_kg_m2=high_speed,
    )
    assert total == pytest.approx(522.227552)


def test_fluid_coupling_reference_functions() -> None:
    fluid_referred = _fluid_coupling_inertia_referred_to_motor_shaft(1.2, 2.0)
    assert fluid_referred == pytest.approx(0.3)

    total_at_fluid = _total_rotational_inertia_at_fluid_coupling_shaft(100.0, 20.0)
    assert total_at_fluid == pytest.approx(40000.0)


def test_rotational_inertia_breakdown_at_motor_shaft_keys_and_total() -> None:
    breakdown = _rotational_inertia_breakdown_at_motor_shaft(
        reflected_translating_mass_inertia_kg_m2=100.0,
        gearbox_inertia_at_motor_shaft_kg_m2=10.0,
        pulley_inertia_native_kg_m2=40.0,
        pulley_gear_ratio_motor_to_component=2.0,
        high_speed_coupling_inertia_native_kg_m2=3.0,
    )
    assert "low_speed_native_component_inertia_at_motor_shaft_kg_m2" in breakdown
    assert "high_speed_native_component_inertia_at_motor_shaft_kg_m2" in breakdown
    assert breakdown["total_rotational_inertia_at_motor_shaft_kg_m2"] == pytest.approx(
        123.0
    )
