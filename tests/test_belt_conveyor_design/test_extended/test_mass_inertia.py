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
    translating_mass_inertia_at_pulley_circumference,
    mass_inertia_at_pulley_shaft,
    reflected_translating_mass_inertia_at_motor_shaft,
    component_inertia_referred_to_motor_shaft,
    fluid_coupling_inertia_referred_to_motor_shaft,
    motor_shaft_rotational_inertia_per_drive,
    total_low_speed_inertia,
    total_inertia_for_single_drive,
    fluid_coupling_design_inertia,
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


def test_translating_mass_inertia_at_pulley_circumference_basic() -> None:
    result = translating_mass_inertia_at_pulley_circumference(
        Quantity(100.0, u.kilogram),
        Quantity(0.5, u.meter),
    )
    assert result.units == u.kilogram * u.meter**2
    assert result.magnitude == pytest.approx(25.0)


def test_mass_inertia_at_pulley_shaft_zero_native_inertia() -> None:
    """With zero native pulley inertia, should equal translating-only."""
    result = mass_inertia_at_pulley_shaft(
        Quantity(100.0, u.kilogram),
        Quantity(0.5, u.meter),
        pulley_inertia_native=None,
    )
    assert result.units == u.kilogram * u.meter**2
    assert result.magnitude == pytest.approx(25.0)


def test_mass_inertia_at_pulley_shaft_nonzero_native_inertia() -> None:
    """With nonzero native pulley inertia, should sum correctly."""
    result = mass_inertia_at_pulley_shaft(
        Quantity(100.0, u.kilogram),
        Quantity(0.5, u.meter),
        pulley_inertia_native=Quantity(5.0, u.kilogram * u.meter**2),
    )
    assert result.units == u.kilogram * u.meter**2
    assert result.magnitude == pytest.approx(30.0)


def test_mass_inertia_at_pulley_shaft_negative_native_inertia_raises() -> None:
    with pytest.raises(ValueError, match="pulley_inertia_native"):
        mass_inertia_at_pulley_shaft(
            Quantity(100.0, u.kilogram),
            Quantity(0.5, u.meter),
            pulley_inertia_native=Quantity(-1.0, u.kilogram * u.meter**2),
        )


def test_translating_mass_inertia_at_pulley_circumference_spec_case() -> None:
    """Inertia at pulley shaft, before reflection to motor shaft."""
    result = translating_mass_inertia_at_pulley_circumference(
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


def test_motor_shaft_rotational_inertia_per_drive_basic() -> None:
    result = motor_shaft_rotational_inertia_per_drive(
        Quantity(503.227552, u.kilogram * u.meter**2),
        2,
    )
    assert result.magnitude == pytest.approx(251.613776)


def test_motor_shaft_rotational_inertia_per_drive_rejects_bool_motor_count() -> None:
    """Phase 5: motor_count must be int, not bool."""
    with pytest.raises(ValueError, match="motor_count.*int"):
        motor_shaft_rotational_inertia_per_drive(
            Quantity(503.227552, u.kilogram * u.meter**2),
            True,  # type: ignore
        )


def test_motor_shaft_rotational_inertia_per_drive_rejects_float_motor_count() -> None:
    """Phase 5: motor_count must be int, not float (even if value is whole)."""
    with pytest.raises(ValueError, match="motor_count.*int"):
        motor_shaft_rotational_inertia_per_drive(
            Quantity(503.227552, u.kilogram * u.meter**2),
            2.0,  # type: ignore
        )

    with pytest.raises(ValueError, match="motor_count.*int"):
        motor_shaft_rotational_inertia_per_drive(
            Quantity(503.227552, u.kilogram * u.meter**2),
            2.5,  # type: ignore
        )


def test_fluid_coupling_reference_functions() -> None:
    fluid_referred = fluid_coupling_inertia_referred_to_motor_shaft(
        Quantity(1.2, u.kilogram * u.meter**2),
        Quantity(2.0, u.dimensionless),
    )
    assert fluid_referred.magnitude == pytest.approx(0.3)


# Phase 4 tests: Fluid-coupling design inertia and total-low-speed inertia cascade


def test_fluid_coupling_design_inertia_basic() -> None:
    """Phase 4 reshaped: Fluid-coupling inertia from low-speed total + gearbox ratio + high-speed."""
    result = fluid_coupling_design_inertia(
        total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
        gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        high_speed_coupling_inertia=Quantity(3.0, u.kilogram * u.meter**2),
        high_speed_brake_inertia=Quantity(2.0, u.kilogram * u.meter**2),
        gearbox_inertia=Quantity(10.0, u.kilogram * u.meter**2),
        flywheel_inertia=Quantity(50.0, u.kilogram * u.meter**2),
    )
    assert isinstance(result, Quantity)
    assert result.units == u.kilogram * u.meter**2
    # reflected = 100 / 4 = 25; total = 25 + 3 + 2 + 10 + 50 = 90
    assert result.magnitude == pytest.approx(90.0)


def test_fluid_coupling_design_inertia_zero_gearbox() -> None:
    """Phase 4 reshaped: Optional gearbox inertia defaults to None/zero."""
    result = fluid_coupling_design_inertia(
        total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
        gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
    )
    # reflected = 100 / 4 = 25
    assert result.magnitude == pytest.approx(25.0)


# Phase 4 new cascade: total_low_speed_inertia + reshaped fluid_coupling_design_inertia


def test_total_low_speed_inertia_basic() -> None:
    """Phase 4: Total low-speed inertia sums mass_at_shaft + ls_coupling + ls_brake."""
    result = total_low_speed_inertia(
        mass_inertia_at_pulley_shaft=Quantity(100.0, u.kilogram * u.meter**2),
        low_speed_coupling_inertia=Quantity(20.0, u.kilogram * u.meter**2),
        low_speed_brake_inertia=Quantity(8.0, u.kilogram * u.meter**2),
    )
    assert isinstance(result, Quantity)
    assert result.units == u.kilogram * u.meter**2
    assert result.magnitude == pytest.approx(128.0)


def test_total_low_speed_inertia_zero_optional() -> None:
    """Phase 4: Optional low-speed components default to None/zero."""
    result = total_low_speed_inertia(
        mass_inertia_at_pulley_shaft=Quantity(100.0, u.kilogram * u.meter**2),
    )
    assert result.magnitude == pytest.approx(100.0)


def test_cascade_mass_inertia_to_fluid_coupling_design_inertia_public() -> None:
    """Phase 4 cascade (public): mass_inertia_at_pulley_shaft -> total_low_speed_inertia -> fluid_coupling_design_inertia."""
    # Step 1: Compute mass inertia at pulley shaft with native pulley inertia.
    mass_inertia = mass_inertia_at_pulley_shaft(
        translating_mass=Quantity(100.0, u.kilogram),
        drive_pulley_radius=Quantity(0.5, u.meter),
        pulley_inertia_native=Quantity(10.0, u.kilogram * u.meter**2),
    )
    # 100 * (0.5^2) + 10 = 25 + 10 = 35
    assert mass_inertia.magnitude == pytest.approx(35.0)

    # Step 2: Feed into total_low_speed_inertia with coupling, brake omitted (None = 0).
    total_low_speed = total_low_speed_inertia(
        mass_inertia_at_pulley_shaft=mass_inertia,
        low_speed_coupling_inertia=Quantity(5.0, u.kilogram * u.meter**2),
        low_speed_brake_inertia=None,
    )
    # 35 + 5 + 0 = 40
    assert total_low_speed.magnitude == pytest.approx(40.0)

    # Step 3: Feed into fluid_coupling_design_inertia with some high-speed components omitted (None).
    design_inertia = fluid_coupling_design_inertia(
        total_low_speed_inertia=total_low_speed,
        gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        high_speed_coupling_inertia=Quantity(3.0, u.kilogram * u.meter**2),
        high_speed_brake_inertia=None,
        gearbox_inertia=Quantity(2.0, u.kilogram * u.meter**2),
        flywheel_inertia=None,
    )
    # Reflect: 40 / (2^2) = 40 / 4 = 10
    # Total: 10 + 3 + 0 + 2 + 0 = 15
    assert design_inertia.magnitude == pytest.approx(15.0)


def test_mass_inertia_at_pulley_shaft_root_import_smoke_test() -> None:
    """Smoke test: mass_inertia_at_pulley_shaft accessible from package root."""
    # Verify export is available from package root
    from eytelwein.belt_conveyor_design import mass_inertia_at_pulley_shaft as root_func

    result = root_func(
        translating_mass=Quantity(100.0, u.kilogram),
        drive_pulley_radius=Quantity(0.5, u.meter),
    )
    assert isinstance(result, Quantity)
    assert result.units == u.kilogram * u.meter**2
    assert result.magnitude == pytest.approx(25.0)


# Phase 5 tests: Canonical single-drive total inertia


def test_total_inertia_for_single_drive_basic() -> None:
    """Phase 5: Per-drive total inertia with shared low-speed reflection divided by quantity_of_drives."""
    result = total_inertia_for_single_drive(
        total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
        quantity_of_drives=2,
        gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        high_speed_coupling_inertia=Quantity(3.0, u.kilogram * u.meter**2),
        high_speed_brake_inertia=Quantity(2.0, u.kilogram * u.meter**2),
        gearbox_inertia=Quantity(10.0, u.kilogram * u.meter**2),
        flywheel_inertia=Quantity(50.0, u.kilogram * u.meter**2),
        fluid_coupling_inertia=Quantity(1.0, u.kilogram * u.meter**2),
        motor_coupling_inertia=Quantity(1.0, u.kilogram * u.meter**2),
        motor_inertia=Quantity(2.0, u.kilogram * u.meter**2),
    )
    assert isinstance(result, Quantity)
    assert result.units == u.kilogram * u.meter**2
    # reflected = 100 / 4 = 25; divided = 25 / 2 = 12.5; total = 12.5 + 3 + 2 + 10 + 50 + 1 + 1 + 2 = 81.5
    assert result.magnitude == pytest.approx(81.5)


def test_total_inertia_for_single_drive_single_drive() -> None:
    """Phase 5: With single drive, divided inertia = reflected inertia (no division effect)."""
    result = total_inertia_for_single_drive(
        total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
        quantity_of_drives=1,
        gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
    )
    # reflected = 100 / 4 = 25; divided = 25 / 1 = 25
    assert result.magnitude == pytest.approx(25.0)


def test_total_inertia_for_single_drive_proves_quantity_divides_reflected_only() -> (
    None
):
    """Phase 5: Prove that quantity_of_drives divides only the reflected shared low-speed contribution."""
    # For 1 drive: reflected_per_drive = 25 / 1 = 25; motor_inertia = 5; total = 30
    result_1_drive = total_inertia_for_single_drive(
        total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
        quantity_of_drives=1,
        gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        motor_inertia=Quantity(5.0, u.kilogram * u.meter**2),
    )
    assert result_1_drive.magnitude == pytest.approx(30.0)

    # For 2 drives: reflected_per_drive = 25 / 2 = 12.5; motor_inertia = 5 (NOT divided); total = 17.5
    result_2_drives = total_inertia_for_single_drive(
        total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
        quantity_of_drives=2,
        gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        motor_inertia=Quantity(5.0, u.kilogram * u.meter**2),
    )
    assert result_2_drives.magnitude == pytest.approx(17.5)

    # For 4 drives: reflected_per_drive = 25 / 4 = 6.25; motor_inertia = 5 (NOT divided); total = 11.25
    result_4_drives = total_inertia_for_single_drive(
        total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
        quantity_of_drives=4,
        gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        motor_inertia=Quantity(5.0, u.kilogram * u.meter**2),
    )
    assert result_4_drives.magnitude == pytest.approx(11.25)


def test_total_inertia_for_single_drive_zero_low_speed() -> None:
    """Phase 5: With zero low-speed inertia, only high-speed/motor components remain."""
    result = total_inertia_for_single_drive(
        total_low_speed_inertia=Quantity(0.0, u.kilogram * u.meter**2),
        quantity_of_drives=2,
        gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        motor_inertia=Quantity(10.0, u.kilogram * u.meter**2),
    )
    assert result.magnitude == pytest.approx(10.0)


def test_total_inertia_for_single_drive_quantity_validation() -> None:
    """Phase 5: quantity_of_drives must be >= 1."""
    with pytest.raises(ValueError, match="quantity_of_drives"):
        total_inertia_for_single_drive(
            total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
            quantity_of_drives=0,
            gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        )

    with pytest.raises(ValueError, match="quantity_of_drives"):
        total_inertia_for_single_drive(
            total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
            quantity_of_drives=-1,
            gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        )


def test_total_inertia_for_single_drive_root_import_smoke_test() -> None:
    """Smoke test: total_inertia_for_single_drive accessible from package root."""
    from eytelwein.belt_conveyor_design import (
        total_inertia_for_single_drive as root_func,
    )

    result = root_func(
        total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
        quantity_of_drives=2,
        gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
    )
    assert isinstance(result, Quantity)
    assert result.units == u.kilogram * u.meter**2
    # reflected = 100 / 4 = 25; divided = 25 / 2 = 12.5
    assert result.magnitude == pytest.approx(12.5)


def test_total_inertia_for_single_drive_rejects_float_quantity_of_drives() -> None:
    """Phase 5: quantity_of_drives must be int, not float."""
    with pytest.raises(ValueError, match="quantity_of_drives.*int"):
        total_inertia_for_single_drive(
            total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
            quantity_of_drives=2.0,  # type: ignore
            gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        )

    with pytest.raises(ValueError, match="quantity_of_drives.*int"):
        total_inertia_for_single_drive(
            total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
            quantity_of_drives=2.5,  # type: ignore
            gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        )


def test_total_inertia_for_single_drive_rejects_bool_quantity_of_drives() -> None:
    """Phase 5: quantity_of_drives must be int, not bool."""
    with pytest.raises(ValueError, match="quantity_of_drives.*int"):
        total_inertia_for_single_drive(
            total_low_speed_inertia=Quantity(100.0, u.kilogram * u.meter**2),
            quantity_of_drives=True,  # type: ignore
            gearbox_ratio_motor_to_low_speed_side=Quantity(2.0, u.dimensionless),
        )


def test_fluid_coupling_design_inertia_delegates_to_single_drive_wrapper() -> None:
    """Phase 5: Prove wrapper delegation: fluid_coupling_design_inertia == total_inertia_for_single_drive(quantity=1, motor_terms=0) using Quantity API."""
    # Define test parameters
    total_low_speed = Quantity(100.0, u.kilogram * u.meter**2)
    gearbox_ratio = Quantity(2.0, u.dimensionless)
    hs_coupling = Quantity(3.0, u.kilogram * u.meter**2)
    hs_brake = Quantity(2.0, u.kilogram * u.meter**2)
    gearbox = Quantity(10.0, u.kilogram * u.meter**2)
    flywheel = Quantity(50.0, u.kilogram * u.meter**2)

    # Call fluid_coupling_design_inertia (delegates internally with motor-side = 0)
    design_result = fluid_coupling_design_inertia(
        total_low_speed_inertia=total_low_speed,
        gearbox_ratio_motor_to_low_speed_side=gearbox_ratio,
        high_speed_coupling_inertia=hs_coupling,
        high_speed_brake_inertia=hs_brake,
        gearbox_inertia=gearbox,
        flywheel_inertia=flywheel,
    )

    # Call total_inertia_for_single_drive with quantity=1 and motor-side terms zeroed
    canonical_result = total_inertia_for_single_drive(
        total_low_speed_inertia=total_low_speed,
        quantity_of_drives=1,
        gearbox_ratio_motor_to_low_speed_side=gearbox_ratio,
        high_speed_coupling_inertia=hs_coupling,
        high_speed_brake_inertia=hs_brake,
        gearbox_inertia=gearbox,
        flywheel_inertia=flywheel,
        fluid_coupling_inertia=None,
        motor_coupling_inertia=None,
        motor_inertia=None,
    )

    # Both should be equal
    assert design_result.magnitude == pytest.approx(canonical_result.magnitude)
    assert design_result.units == canonical_result.units
