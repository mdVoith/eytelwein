"""Tests for public Pint wrappers in extended mass inertia module."""

import pytest
from pint import Quantity

from eytelwein.belt_conveyor_design.extended.mass_inertia import (
    translating_mass_from_line_load_and_segment_length,
    translating_mass_idler_carry,
    translating_mass_idler_return,
    translating_mass_belt,
    translating_mass_material,
    total_translating_mass_empty,
    total_translating_mass,
    drive_pulley_radius_from_drive_pulley_diameter,
    translating_mass_inertia_at_pulley_shaft,
    reflected_translating_mass_inertia_at_motor_shaft,
    component_inertia_referred_to_motor_shaft,
    total_motor_shaft_rotational_inertia_from_equivalent_component_inertias,
    total_motor_shaft_rotational_inertia_from_native_component_inertias,
    motor_shaft_rotational_inertia_per_drive,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


def test_translating_mass_from_line_load_and_segment_length_basic() -> None:
    result = translating_mass_from_line_load_and_segment_length(
        Quantity(10.0, u.kilogram / u.meter),
        Quantity(100.0, u.meter),
    )
    assert isinstance(result, Quantity)
    assert result.units == u.kilogram
    assert result.magnitude == pytest.approx(1000.0)


def test_translating_mass_material_spec_case() -> None:
    result = translating_mass_material(
        Quantity(124.7, u.kilogram / u.meter),
        Quantity(4303.0, u.meter),
    )
    assert result.magnitude == pytest.approx(536584.1, rel=0.005)


def test_total_translating_mass_empty_spec_case() -> None:
    idler_carry = translating_mass_idler_carry(
        Quantity(18503.0 / 4303.0, u.kilogram / u.meter),
        Quantity(4303.0, u.meter),
    )
    idler_return = translating_mass_idler_return(
        Quantity(6168.0 / 4303.0, u.kilogram / u.meter),
        Quantity(4303.0, u.meter),
    )
    belt = translating_mass_belt(
        Quantity(25.8875, u.kilogram / u.meter),
        Quantity(4303.0, u.meter),
    )
    result = total_translating_mass_empty(idler_carry, idler_return, belt)
    assert result.magnitude == pytest.approx(247458.825, rel=0.005)


def test_total_translating_mass_spec_case() -> None:
    result = total_translating_mass(
        Quantity(247458.825, u.kilogram),
        Quantity(536584.1, u.kilogram),
    )
    assert result.magnitude == pytest.approx(784042.925, rel=0.005)


def test_drive_pulley_radius_from_drive_pulley_diameter_basic() -> None:
    result = drive_pulley_radius_from_drive_pulley_diameter(Quantity(1.04, u.meter))
    assert result.units == u.meter
    assert result.magnitude == pytest.approx(0.52)


def test_translating_mass_inertia_at_pulley_shaft_basic() -> None:
    result = translating_mass_inertia_at_pulley_shaft(
        Quantity(100.0, u.kilogram),
        Quantity(0.5, u.meter),
    )
    assert result.units == u.kilogram * u.meter**2
    assert result.magnitude == pytest.approx(25.0)


def test_translating_mass_inertia_at_pulley_shaft_spec_case() -> None:
    """Inertia at pulley shaft, before reflection to motor shaft."""
    result = translating_mass_inertia_at_pulley_shaft(
        Quantity(247458.825, u.kilogram),
        Quantity(0.52, u.meter),
    )
    assert result.magnitude == pytest.approx(67116.766245, rel=0.005)


def test_reflected_translating_mass_inertia_at_motor_shaft_spec_case() -> None:
    result = reflected_translating_mass_inertia_at_motor_shaft(
        Quantity(247458.825, u.kilogram),
        Quantity(0.52, u.meter),
        Quantity(11.731, u.dimensionless),
    )
    assert result.magnitude == pytest.approx(486.227552, rel=0.005)


def test_reflected_translating_mass_inertia_at_motor_shaft_full_belt_case() -> None:
    """Full belt case with large mass and high speed reduction."""
    result = reflected_translating_mass_inertia_at_motor_shaft(
        Quantity(234511, u.kilogram),
        Quantity(0.4, u.meter),  # radius = 0.8 m diameter / 2
        Quantity(20.153, u.dimensionless),
    )
    assert result.magnitude == pytest.approx(92.4, rel=0.005)


def test_component_inertia_referred_to_motor_shaft_basic() -> None:
    result = component_inertia_referred_to_motor_shaft(
        Quantity(1.2, u.kilogram * u.meter**2),
        Quantity(2.0, u.dimensionless),
    )
    assert result.magnitude == pytest.approx(0.3)


def test_total_motor_shaft_rotational_inertia_from_equivalent_component_inertias() -> None:
    result = total_motor_shaft_rotational_inertia_from_equivalent_component_inertias(
        Quantity(486.227552, u.kilogram * u.meter**2),
        Quantity(10.0, u.kilogram * u.meter**2),
        Quantity(5.0, u.kilogram * u.meter**2),
        Quantity(2.0, u.kilogram * u.meter**2),
    )
    assert result.magnitude == pytest.approx(503.227552)


def test_total_motor_shaft_rotational_inertia_from_native_component_inertias() -> None:
    result = total_motor_shaft_rotational_inertia_from_native_component_inertias(
        Quantity(486.227552, u.kilogram * u.meter**2),
        Quantity(40.0, u.kilogram * u.meter**2),
        Quantity(2.0, u.dimensionless),
        Quantity(20.0, u.kilogram * u.meter**2),
        Quantity(2.0, u.dimensionless),
        Quantity(8.0, u.kilogram * u.meter**2),
        Quantity(2.0, u.dimensionless),
    )
    assert result.magnitude == pytest.approx(503.227552)


def test_motor_shaft_rotational_inertia_per_drive_basic() -> None:
    result = motor_shaft_rotational_inertia_per_drive(
        Quantity(503.227552, u.kilogram * u.meter**2),
        2,
    )
    assert result.magnitude == pytest.approx(251.613776)
