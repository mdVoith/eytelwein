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
    _component_inertia_referred_to_motor_shaft,
    _total_low_speed_inertia,
    _fluid_coupling_design_inertia,
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


def test_component_inertia_referred_to_motor_shaft_basic() -> None:
    result = _component_inertia_referred_to_motor_shaft(1.2, 2.0)
    assert result == pytest.approx(0.3)


# Phase 4 tests: Fluid-coupling design inertia


def test_fluid_coupling_design_inertia_basic() -> None:
    """Phase 4 reshaped: Fluid-coupling inertia from low-speed total + gearbox ratio + high-speed."""
    # low_speed_total = 100
    # reflected = 100 / (2^2) = 25
    # high_speed components: coupling=3, brake=2, gearbox=10, flywheel=50
    # total = 25 + 3 + 2 + 10 + 50 = 90
    result = _fluid_coupling_design_inertia(
        total_low_speed_inertia_kg_m2=100.0,
        gearbox_ratio_motor_to_low_speed_side=2.0,
        high_speed_coupling_inertia_kg_m2=3.0,
        high_speed_brake_inertia_kg_m2=2.0,
        gearbox_inertia_kg_m2=10.0,
        flywheel_inertia_kg_m2=50.0,
    )
    assert result == pytest.approx(90.0)


def test_fluid_coupling_design_inertia_zero_gearbox() -> None:
    """Phase 4 reshaped: Optional gearbox inertia defaults to zero."""
    result = _fluid_coupling_design_inertia(
        total_low_speed_inertia_kg_m2=100.0,
        gearbox_ratio_motor_to_low_speed_side=2.0,
    )
    # reflected = 100 / 4 = 25
    assert result == pytest.approx(25.0)


def test_fluid_coupling_design_inertia_negative_raises() -> None:
    """Phase 4 reshaped: Negative low-speed inertia raises."""
    with pytest.raises(ValueError):
        _fluid_coupling_design_inertia(
            total_low_speed_inertia_kg_m2=-1.0,
            gearbox_ratio_motor_to_low_speed_side=2.0,
        )


# Phase 4 new cascade: total_low_speed_inertia + reshaped fluid_coupling_design_inertia


def test_total_low_speed_inertia_basic() -> None:
    """Phase 4: Total low-speed inertia sums mass_at_shaft + ls_coupling + ls_brake."""
    result = _total_low_speed_inertia(
        mass_inertia_at_pulley_shaft_kg_m2=100.0,
        low_speed_coupling_inertia_kg_m2=20.0,
        low_speed_brake_inertia_kg_m2=8.0,
    )
    assert result == pytest.approx(128.0)


def test_total_low_speed_inertia_zero_optional() -> None:
    """Phase 4: Optional low-speed components default to zero."""
    result = _total_low_speed_inertia(
        mass_inertia_at_pulley_shaft_kg_m2=100.0,
    )
    assert result == pytest.approx(100.0)


def test_total_low_speed_inertia_all_zero() -> None:
    """Phase 4: All components can be zero."""
    result = _total_low_speed_inertia(
        mass_inertia_at_pulley_shaft_kg_m2=0.0,
    )
    assert result == pytest.approx(0.0)


def test_total_low_speed_inertia_negative_raises() -> None:
    """Phase 4: Negative inertia raises."""
    with pytest.raises(ValueError):
        _total_low_speed_inertia(
            mass_inertia_at_pulley_shaft_kg_m2=-1.0,
        )


def test_fluid_coupling_design_inertia_reshaped_invalid_ratio_raises() -> None:
    """Phase 4 reshaped: Invalid gearbox ratio raises."""
    with pytest.raises(ValueError):
        _fluid_coupling_design_inertia(
            total_low_speed_inertia_kg_m2=100.0,
            gearbox_ratio_motor_to_low_speed_side=0.0,
        )


def test_fluid_coupling_design_inertia_reshaped_negative_high_speed_component_raises() -> (
    None
):
    """Phase 4 reshaped: Negative high-speed component raises."""
    with pytest.raises(ValueError):
        _fluid_coupling_design_inertia(
            total_low_speed_inertia_kg_m2=100.0,
            gearbox_ratio_motor_to_low_speed_side=2.0,
            high_speed_coupling_inertia_kg_m2=-1.0,
        )


def test_cascade_mass_inertia_to_fluid_coupling_design_inertia_private() -> None:
    """Phase 4 cascade (private): mass_inertia_at_pulley_shaft -> total_low_speed_inertia -> fluid_coupling_design_inertia."""
    # Step 1: Compute mass inertia at pulley shaft with native pulley inertia.
    mass_inertia = _mass_inertia_at_pulley_shaft(
        translating_mass_kg=100.0,
        drive_pulley_radius_m=0.5,
        pulley_inertia_native_kg_m2=10.0,
    )
    # 100 * (0.5^2) + 10 = 25 + 10 = 35
    assert mass_inertia == pytest.approx(35.0)

    # Step 2: Feed into total_low_speed_inertia with coupling, brake omitted (defaults to 0).
    total_low_speed = _total_low_speed_inertia(
        mass_inertia_at_pulley_shaft_kg_m2=mass_inertia,
        low_speed_coupling_inertia_kg_m2=5.0,
        low_speed_brake_inertia_kg_m2=0.0,
    )
    # 35 + 5 + 0 = 40
    assert total_low_speed == pytest.approx(40.0)

    # Step 3: Feed into fluid_coupling_design_inertia with some high-speed components omitted.
    design_inertia = _fluid_coupling_design_inertia(
        total_low_speed_inertia_kg_m2=total_low_speed,
        gearbox_ratio_motor_to_low_speed_side=2.0,
        high_speed_coupling_inertia_kg_m2=3.0,
        high_speed_brake_inertia_kg_m2=0.0,
        gearbox_inertia_kg_m2=2.0,
        flywheel_inertia_kg_m2=0.0,
    )
    # Reflect: 40 / (2^2) = 40 / 4 = 10
    # Total: 10 + 3 + 0 + 2 + 0 = 15
    assert design_inertia == pytest.approx(15.0)


# Phase 5 tests: Canonical single-drive total inertia


def test_total_inertia_for_single_drive_basic() -> None:
    """Phase 5: Per-drive total inertia with shared low-speed reflection divided by quantity_of_drives."""
    # low_speed_total = 100
    # quantity_of_drives = 2
    # reflected = 100 / (2^2) = 25
    # divided by quantity = 25 / 2 = 12.5
    # high_speed components: coupling=3, brake=2, gearbox=10, flywheel=50, fluid=1, motor_coupling=1, motor=2
    # total = 12.5 + 3 + 2 + 10 + 50 + 1 + 1 + 2 = 81.5
    from eytelwein.belt_conveyor_design.extended._mass_inertia import (
        _total_inertia_for_single_drive,
    )

    result = _total_inertia_for_single_drive(
        total_low_speed_inertia_kg_m2=100.0,
        quantity_of_drives=2,
        gearbox_ratio_motor_to_low_speed_side=2.0,
        high_speed_coupling_inertia_kg_m2=3.0,
        high_speed_brake_inertia_kg_m2=2.0,
        gearbox_inertia_kg_m2=10.0,
        flywheel_inertia_kg_m2=50.0,
        fluid_coupling_inertia_kg_m2=1.0,
        motor_coupling_inertia_kg_m2=1.0,
        motor_inertia_kg_m2=2.0,
    )
    assert result == pytest.approx(81.5)


def test_total_inertia_for_single_drive_single_drive() -> None:
    """Phase 5: With single drive, divided inertia = reflected inertia (no division effect)."""
    # low_speed_total = 100
    # quantity_of_drives = 1
    # reflected = 100 / (2^2) = 25
    # divided by quantity = 25 / 1 = 25
    # no high-speed components (all 0)
    # total = 25
    from eytelwein.belt_conveyor_design.extended._mass_inertia import (
        _total_inertia_for_single_drive,
    )

    result = _total_inertia_for_single_drive(
        total_low_speed_inertia_kg_m2=100.0,
        quantity_of_drives=1,
        gearbox_ratio_motor_to_low_speed_side=2.0,
    )
    assert result == pytest.approx(25.0)


def test_total_inertia_for_single_drive_proves_quantity_divides_reflected_only() -> (
    None
):
    """Phase 5: Prove that quantity_of_drives divides only the reflected shared low-speed contribution."""
    from eytelwein.belt_conveyor_design.extended._mass_inertia import (
        _total_inertia_for_single_drive,
    )

    # low_speed_total = 100, gearbox_ratio = 2, reflected = 25
    # For 1 drive: reflected_per_drive = 25 / 1 = 25; motor_inertia = 5; total = 30
    result_1_drive = _total_inertia_for_single_drive(
        total_low_speed_inertia_kg_m2=100.0,
        quantity_of_drives=1,
        gearbox_ratio_motor_to_low_speed_side=2.0,
        motor_inertia_kg_m2=5.0,
    )
    assert result_1_drive == pytest.approx(30.0)

    # For 2 drives: reflected_per_drive = 25 / 2 = 12.5; motor_inertia = 5 (NOT divided); total = 17.5
    result_2_drives = _total_inertia_for_single_drive(
        total_low_speed_inertia_kg_m2=100.0,
        quantity_of_drives=2,
        gearbox_ratio_motor_to_low_speed_side=2.0,
        motor_inertia_kg_m2=5.0,
    )
    assert result_2_drives == pytest.approx(17.5)

    # For 4 drives: reflected_per_drive = 25 / 4 = 6.25; motor_inertia = 5 (NOT divided); total = 11.25
    result_4_drives = _total_inertia_for_single_drive(
        total_low_speed_inertia_kg_m2=100.0,
        quantity_of_drives=4,
        gearbox_ratio_motor_to_low_speed_side=2.0,
        motor_inertia_kg_m2=5.0,
    )
    assert result_4_drives == pytest.approx(11.25)


def test_total_inertia_for_single_drive_zero_low_speed() -> None:
    """Phase 5: With zero low-speed inertia, only high-speed/motor components remain."""
    from eytelwein.belt_conveyor_design.extended._mass_inertia import (
        _total_inertia_for_single_drive,
    )

    result = _total_inertia_for_single_drive(
        total_low_speed_inertia_kg_m2=0.0,
        quantity_of_drives=2,
        gearbox_ratio_motor_to_low_speed_side=2.0,
        motor_inertia_kg_m2=10.0,
    )
    assert result == pytest.approx(10.0)


def test_total_inertia_for_single_drive_quantity_validation() -> None:
    """Phase 5: quantity_of_drives must be >= 1."""
    from eytelwein.belt_conveyor_design.extended._mass_inertia import (
        _total_inertia_for_single_drive,
    )

    with pytest.raises(ValueError, match="quantity_of_drives"):
        _total_inertia_for_single_drive(
            total_low_speed_inertia_kg_m2=100.0,
            quantity_of_drives=0,
            gearbox_ratio_motor_to_low_speed_side=2.0,
        )

    with pytest.raises(ValueError, match="quantity_of_drives"):
        _total_inertia_for_single_drive(
            total_low_speed_inertia_kg_m2=100.0,
            quantity_of_drives=-1,
            gearbox_ratio_motor_to_low_speed_side=2.0,
        )


def test_fluid_coupling_design_inertia_delegates_to_canonical_helper() -> None:
    """Phase 5: _fluid_coupling_design_inertia should delegate to _total_inertia_for_single_drive with motor-side terms zeroed."""
    from eytelwein.belt_conveyor_design.extended._mass_inertia import (
        _total_inertia_for_single_drive,
    )

    # Fluid-coupling design inertia = _total_inertia_for_single_drive with quantity=1 and motor terms = 0
    low_speed = 100.0
    gearbox_ratio = 2.0
    hs_coupling = 3.0
    hs_brake = 2.0
    gearbox = 10.0
    flywheel = 50.0

    # Expected behavior: reflected = 100 / 4 = 25; total = 25 + 3 + 2 + 10 + 50 = 90
    canonical_result = _total_inertia_for_single_drive(
        total_low_speed_inertia_kg_m2=low_speed,
        quantity_of_drives=1,
        gearbox_ratio_motor_to_low_speed_side=gearbox_ratio,
        high_speed_coupling_inertia_kg_m2=hs_coupling,
        high_speed_brake_inertia_kg_m2=hs_brake,
        gearbox_inertia_kg_m2=gearbox,
        flywheel_inertia_kg_m2=flywheel,
        fluid_coupling_inertia_kg_m2=0.0,
        motor_coupling_inertia_kg_m2=0.0,
        motor_inertia_kg_m2=0.0,
    )
    assert canonical_result == pytest.approx(90.0)

    # Now call fluid_coupling_design_inertia and verify it matches
    design_result = _fluid_coupling_design_inertia(
        total_low_speed_inertia_kg_m2=low_speed,
        gearbox_ratio_motor_to_low_speed_side=gearbox_ratio,
        high_speed_coupling_inertia_kg_m2=hs_coupling,
        high_speed_brake_inertia_kg_m2=hs_brake,
        gearbox_inertia_kg_m2=gearbox,
        flywheel_inertia_kg_m2=flywheel,
    )
    assert design_result == pytest.approx(canonical_result)


def test_total_inertia_for_single_drive_rejects_float_quantity_of_drives() -> None:
    """Phase 5: quantity_of_drives must be int, not float (even if value is whole)."""
    from eytelwein.belt_conveyor_design.extended._mass_inertia import (
        _total_inertia_for_single_drive,
    )

    with pytest.raises(ValueError, match="quantity_of_drives.*int"):
        _total_inertia_for_single_drive(
            total_low_speed_inertia_kg_m2=100.0,
            quantity_of_drives=2.0,  # type: ignore
            gearbox_ratio_motor_to_low_speed_side=2.0,
        )

    with pytest.raises(ValueError, match="quantity_of_drives.*int"):
        _total_inertia_for_single_drive(
            total_low_speed_inertia_kg_m2=100.0,
            quantity_of_drives=2.5,  # type: ignore
            gearbox_ratio_motor_to_low_speed_side=2.0,
        )


def test_total_inertia_for_single_drive_rejects_bool_quantity_of_drives() -> None:
    """Phase 5: quantity_of_drives must be int, not bool."""
    from eytelwein.belt_conveyor_design.extended._mass_inertia import (
        _total_inertia_for_single_drive,
    )

    with pytest.raises(ValueError, match="quantity_of_drives.*int"):
        _total_inertia_for_single_drive(
            total_low_speed_inertia_kg_m2=100.0,
            quantity_of_drives=True,  # type: ignore
            gearbox_ratio_motor_to_low_speed_side=2.0,
        )
