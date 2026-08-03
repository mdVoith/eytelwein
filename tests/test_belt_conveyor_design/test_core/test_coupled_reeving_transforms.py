"""Tests for coupled reeving transformation APIs.

Force-based coupled APIs with explicit effort/load terminology.
Coupled APIs provide both force and travel transforms together to prevent
field errors where one transform is applied but the other is forgotten.

Forward API: load_force + takeup_travel -> effort_force + rope_travel
Inverse API: effort_force + rope_travel -> load_force + takeup_travel
"""

import pytest
from pint import Quantity
from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
    rope_travel_from_takeup_travel,
    takeup_travel_from_rope_travel,
    effort_force_from_load_force,
    load_force_from_effort_force,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


class TestForwardCoupledAPI:
    """Test forward coupled transform: load_force + takeup_travel -> effort_force + rope_travel."""

    def test_forward_coupled_basic_return_type(self):
        """Forward coupled function returns dataclass with effort_force and rope_travel."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            effort_force_and_rope_travel_from_load_force_and_takeup_travel,
        )

        load_force = Quantity(29419.95, u.newton)  # 3000 kg * 9.80665 m/s^2
        takeup_travel = Quantity(1.5, u.meter)
        strand_count = 2

        result = effort_force_and_rope_travel_from_load_force_and_takeup_travel(
            load_force=load_force,
            takeup_travel=takeup_travel,
            strand_count=strand_count,
        )

        # Result should have effort_force and rope_travel attributes
        assert hasattr(result, "effort_force")
        assert hasattr(result, "rope_travel")
        assert isinstance(result.effort_force, Quantity)
        assert isinstance(result.rope_travel, Quantity)

    def test_forward_coupled_consistency_with_individual_transforms(self):
        """Forward coupled result should match individual transform results."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            effort_force_and_rope_travel_from_load_force_and_takeup_travel,
        )

        load_force = Quantity(29419.95, u.newton)
        takeup_travel = Quantity(1.5, u.meter)
        strand_count = 2

        coupled_result = effort_force_and_rope_travel_from_load_force_and_takeup_travel(
            load_force=load_force,
            takeup_travel=takeup_travel,
            strand_count=strand_count,
        )

        # Compare with individual transforms
        expected_effort_force = effort_force_from_load_force(
            load_force=load_force,
            strand_count=strand_count,
            unit="kilonewton",
        )
        expected_rope_travel = rope_travel_from_takeup_travel(
            takeup_travel=takeup_travel,
            strand_count=strand_count,
            unit="meter",
        )

        assert coupled_result.effort_force.magnitude == pytest.approx(
            expected_effort_force.magnitude, rel=1e-9
        )
        assert coupled_result.rope_travel.magnitude == pytest.approx(
            expected_rope_travel.magnitude, rel=1e-9
        )

    def test_forward_coupled_strand_count_validation(self):
        """Forward coupled API should validate strand_count."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            effort_force_and_rope_travel_from_load_force_and_takeup_travel,
        )

        load_force = Quantity(29419.95, u.newton)
        takeup_travel = Quantity(1.5, u.meter)

        with pytest.raises(ValueError, match="strand_count must be"):
            effort_force_and_rope_travel_from_load_force_and_takeup_travel(
                load_force=load_force,
                takeup_travel=takeup_travel,
                strand_count=0,  # Invalid
            )

        with pytest.raises(ValueError, match="strand_count must be"):
            effort_force_and_rope_travel_from_load_force_and_takeup_travel(
                load_force=load_force,
                takeup_travel=takeup_travel,
                strand_count=-1,  # Invalid
            )

    def test_forward_coupled_output_units(self):
        """Forward coupled API should support output unit specifications."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            effort_force_and_rope_travel_from_load_force_and_takeup_travel,
        )

        load_force = Quantity(29419.95, u.newton)
        takeup_travel = Quantity(1.5, u.meter)

        result = effort_force_and_rope_travel_from_load_force_and_takeup_travel(
            load_force=load_force,
            takeup_travel=takeup_travel,
            strand_count=1,
            force_unit="newton",
            travel_unit="millimeter",
        )

        assert result.effort_force.units == u.newton
        assert result.rope_travel.units == u.millimeter


class TestInverseCoupledAPI:
    """Test inverse coupled transform: effort_force + rope_travel -> load_force + takeup_travel."""

    def test_inverse_coupled_basic_return_type(self):
        """Inverse coupled function returns LoadForceAndTravel dataclass."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            load_force_and_takeup_travel_from_effort_force_and_rope_travel,
        )

        effort_force = Quantity(14709.975, u.newton)  # Half of load at 2 strands
        rope_travel = Quantity(3.0, u.meter)
        strand_count = 2

        result = load_force_and_takeup_travel_from_effort_force_and_rope_travel(
            effort_force=effort_force,
            rope_travel=rope_travel,
            strand_count=strand_count,
        )

        # Result should have load_force and takeup_travel attributes
        assert hasattr(result, "load_force")
        assert hasattr(result, "takeup_travel")
        assert isinstance(result.load_force, Quantity)
        assert isinstance(result.takeup_travel, Quantity)

    def test_inverse_coupled_consistency_with_individual_transforms(self):
        """Inverse coupled result should match individual transform results."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            load_force_and_takeup_travel_from_effort_force_and_rope_travel,
        )

        effort_force = Quantity(14709.975, u.newton)
        rope_travel = Quantity(3.0, u.meter)
        strand_count = 2

        coupled_result = load_force_and_takeup_travel_from_effort_force_and_rope_travel(
            effort_force=effort_force,
            rope_travel=rope_travel,
            strand_count=strand_count,
        )

        # Compare with individual transforms
        expected_load_force = load_force_from_effort_force(
            effort_force=effort_force,
            strand_count=strand_count,
            unit="kilonewton",
        )
        expected_takeup_travel = takeup_travel_from_rope_travel(
            rope_travel=rope_travel,
            strand_count=strand_count,
            unit="meter",
        )

        assert coupled_result.load_force.magnitude == pytest.approx(
            expected_load_force.magnitude, rel=1e-9
        )
        assert coupled_result.takeup_travel.magnitude == pytest.approx(
            expected_takeup_travel.magnitude, rel=1e-9
        )

    def test_inverse_coupled_strand_count_validation(self):
        """Inverse coupled API should validate strand_count."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            load_force_and_takeup_travel_from_effort_force_and_rope_travel,
        )

        effort_force = Quantity(14709.975, u.newton)
        rope_travel = Quantity(3.0, u.meter)

        with pytest.raises(ValueError, match="strand_count must be"):
            load_force_and_takeup_travel_from_effort_force_and_rope_travel(
                effort_force=effort_force,
                rope_travel=rope_travel,
                strand_count=0,  # Invalid
            )

        with pytest.raises(ValueError, match="strand_count must be"):
            load_force_and_takeup_travel_from_effort_force_and_rope_travel(
                effort_force=effort_force,
                rope_travel=rope_travel,
                strand_count=-1,  # Invalid
            )

    def test_inverse_coupled_output_units(self):
        """Inverse coupled API should support output unit specifications."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            load_force_and_takeup_travel_from_effort_force_and_rope_travel,
        )

        effort_force = Quantity(14709.975, u.newton)
        rope_travel = Quantity(3.0, u.meter)

        result = load_force_and_takeup_travel_from_effort_force_and_rope_travel(
            effort_force=effort_force,
            rope_travel=rope_travel,
            strand_count=1,
            force_unit="kilonewton",
            travel_unit="millimeter",
        )

        assert result.load_force.units == u.kilonewton
        assert result.takeup_travel.units == u.millimeter


class TestExportChain:
    """Test that coupled APIs are exported through the module hierarchy."""

    def test_forward_api_exported_from_core_module(self):
        """Forward coupled API should be available from core.belt_tensions_and_takeup_forces."""
        from eytelwein.belt_conveyor_design.core import (
            belt_tensions_and_takeup_forces,
        )

        assert hasattr(
            belt_tensions_and_takeup_forces,
            "effort_force_and_rope_travel_from_load_force_and_takeup_travel",
        )

    def test_inverse_api_exported_from_core_module(self):
        """Inverse coupled API should be available from core.belt_tensions_and_takeup_forces."""
        from eytelwein.belt_conveyor_design.core import (
            belt_tensions_and_takeup_forces,
        )

        assert hasattr(
            belt_tensions_and_takeup_forces,
            "load_force_and_takeup_travel_from_effort_force_and_rope_travel",
        )

    def test_forward_api_exported_from_core_init(self):
        """Forward coupled API should be exported from belt_conveyor_design.core."""
        from eytelwein.belt_conveyor_design.core import (
            effort_force_and_rope_travel_from_load_force_and_takeup_travel,
        )

        assert callable(effort_force_and_rope_travel_from_load_force_and_takeup_travel)

    def test_inverse_api_exported_from_core_init(self):
        """Inverse coupled API should be exported from belt_conveyor_design.core."""
        from eytelwein.belt_conveyor_design.core import (
            load_force_and_takeup_travel_from_effort_force_and_rope_travel,
        )

        assert callable(load_force_and_takeup_travel_from_effort_force_and_rope_travel)

    def test_forward_api_exported_from_package(self):
        """Forward coupled API should be exported from belt_conveyor_design package."""
        from eytelwein.belt_conveyor_design import (
            effort_force_and_rope_travel_from_load_force_and_takeup_travel,
        )

        assert callable(effort_force_and_rope_travel_from_load_force_and_takeup_travel)

    def test_inverse_api_exported_from_package(self):
        """Inverse coupled API should be exported from belt_conveyor_design package."""
        from eytelwein.belt_conveyor_design import (
            load_force_and_takeup_travel_from_effort_force_and_rope_travel,
        )

        assert callable(load_force_and_takeup_travel_from_effort_force_and_rope_travel)

    def test_result_type_exported_from_core_module(self):
        """LoadForceAndTravel result type should be available from core."""
        from eytelwein.belt_conveyor_design.core import (
            belt_tensions_and_takeup_forces,
        )

        assert hasattr(belt_tensions_and_takeup_forces, "LoadForceAndTravel")

    def test_old_names_not_available(self):
        """Old coupled API names should not be available."""
        from eytelwein.belt_conveyor_design.core import (
            belt_tensions_and_takeup_forces,
        )

        # These should not exist after the public API replacement
        assert not hasattr(
            belt_tensions_and_takeup_forces,
            "rope_force_and_travel_from_takeup_weight_and_travel",
        )
        assert not hasattr(
            belt_tensions_and_takeup_forces,
            "takeup_weight_and_travel_from_rope_force_and_travel",
        )
        assert not hasattr(belt_tensions_and_takeup_forces, "TakeupWeightAndTravel")


class TestRoundTripConsistency:
    """Test round-trip consistency: forward then inverse should recover original values."""

    def test_round_trip_load_force_and_travel(self):
        """Forward then inverse should recover original load_force and takeup_travel."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            effort_force_and_rope_travel_from_load_force_and_takeup_travel,
            load_force_and_takeup_travel_from_effort_force_and_rope_travel,
        )

        original_load_force = Quantity(29419.95, u.newton)
        original_takeup_travel = Quantity(1.5, u.meter)
        strand_count = 2

        # Forward transform
        forward_result = effort_force_and_rope_travel_from_load_force_and_takeup_travel(
            load_force=original_load_force,
            takeup_travel=original_takeup_travel,
            strand_count=strand_count,
        )

        # Inverse transform
        inverse_result = load_force_and_takeup_travel_from_effort_force_and_rope_travel(
            effort_force=forward_result.effort_force,
            rope_travel=forward_result.rope_travel,
            strand_count=strand_count,
        )

        # Check round-trip (convert original to same units for comparison)
        original_load_force_kn = original_load_force.to(u.kilonewton)
        assert inverse_result.load_force.magnitude == pytest.approx(
            original_load_force_kn.magnitude, rel=1e-8
        )
        assert inverse_result.takeup_travel.magnitude == pytest.approx(
            original_takeup_travel.magnitude, rel=1e-8
        )
