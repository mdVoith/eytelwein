"""Tests for coupled reeving transformation APIs.

Coupled APIs provide both force and travel transforms together to prevent
field errors where one transform is applied but the other is forgotten.
"""

import pytest
from pint import Quantity
from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
    takeup_weight_force_from_takeup_weight,
    takeup_weight_from_takeup_weight_force,
    rope_travel_from_takeup_travel,
    takeup_travel_from_rope_travel,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


class TestCoupledRopeForceAndTravelFromTakeup:
    """Test coupled transform: takeup_weight + takeup_travel -> rope_force + rope_travel."""

    def test_coupled_rope_force_and_travel_basic(self):
        """Coupled function returns dataclass with rope_force and rope_travel."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            rope_force_and_travel_from_takeup_weight_and_travel,
        )

        takeup_weight = Quantity(3000.0, u.kilogram)
        takeup_travel = Quantity(1.5, u.meter)
        strand_count = 2

        result = rope_force_and_travel_from_takeup_weight_and_travel(
            takeup_weight=takeup_weight,
            takeup_travel=takeup_travel,
            strand_count=strand_count,
        )

        # Result should have rope_force and rope_travel attributes
        assert hasattr(result, "rope_force")
        assert hasattr(result, "rope_travel")
        assert isinstance(result.rope_force, Quantity)
        assert isinstance(result.rope_travel, Quantity)

    def test_coupled_consistency_with_individual_transforms_forward(self):
        """Coupled result should match individual transform results."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            rope_force_and_travel_from_takeup_weight_and_travel,
        )

        takeup_weight = Quantity(3000.0, u.kilogram)
        takeup_travel = Quantity(1.5, u.meter)
        strand_count = 2

        coupled_result = rope_force_and_travel_from_takeup_weight_and_travel(
            takeup_weight=takeup_weight,
            takeup_travel=takeup_travel,
            strand_count=strand_count,
        )

        # Compare with individual transforms
        expected_rope_force = takeup_weight_force_from_takeup_weight(
            takeup_weight=takeup_weight,
            strand_count=strand_count,
            unit="kilonewton",
        )
        expected_rope_travel = rope_travel_from_takeup_travel(
            takeup_travel=takeup_travel,
            strand_count=strand_count,
            unit="meter",
        )

        assert coupled_result.rope_force.magnitude == pytest.approx(
            expected_rope_force.magnitude, rel=1e-9
        )
        assert coupled_result.rope_travel.magnitude == pytest.approx(
            expected_rope_travel.magnitude, rel=1e-9
        )

    def test_coupled_strand_count_validation(self):
        """Coupled API should validate strand_count."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            rope_force_and_travel_from_takeup_weight_and_travel,
        )

        takeup_weight = Quantity(3000.0, u.kilogram)
        takeup_travel = Quantity(1.5, u.meter)

        with pytest.raises(ValueError, match="strand_count must be"):
            rope_force_and_travel_from_takeup_weight_and_travel(
                takeup_weight=takeup_weight,
                takeup_travel=takeup_travel,
                strand_count=0,  # Invalid
            )

        with pytest.raises(ValueError, match="strand_count must be"):
            rope_force_and_travel_from_takeup_weight_and_travel(
                takeup_weight=takeup_weight,
                takeup_travel=takeup_travel,
                strand_count=-1,  # Invalid
            )

    def test_coupled_output_units(self):
        """Coupled API should support output unit specifications."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            rope_force_and_travel_from_takeup_weight_and_travel,
        )

        takeup_weight = Quantity(3000.0, u.kilogram)
        takeup_travel = Quantity(1.5, u.meter)

        result = rope_force_and_travel_from_takeup_weight_and_travel(
            takeup_weight=takeup_weight,
            takeup_travel=takeup_travel,
            strand_count=1,
            force_unit="newton",
            travel_unit="millimeter",
        )

        assert result.rope_force.units == u.newton
        assert result.rope_travel.units == u.millimeter


class TestCoupledTakeupWeightAndTravelFromRopeForce:
    """Test coupled inverse transform: rope_force + rope_travel -> takeup_weight + takeup_travel."""

    def test_coupled_takeup_weight_and_travel_basic(self):
        """Coupled inverse function returns dataclass with takeup_weight and takeup_travel."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            takeup_weight_and_travel_from_rope_force_and_travel,
        )

        rope_force = Quantity(58839.9, u.newton)
        rope_travel = Quantity(3.0, u.meter)
        strand_count = 2

        result = takeup_weight_and_travel_from_rope_force_and_travel(
            rope_force=rope_force,
            rope_travel=rope_travel,
            strand_count=strand_count,
        )

        # Result should have takeup_weight and takeup_travel attributes
        assert hasattr(result, "takeup_weight")
        assert hasattr(result, "takeup_travel")
        assert isinstance(result.takeup_weight, Quantity)
        assert isinstance(result.takeup_travel, Quantity)

    def test_coupled_consistency_with_individual_transforms_inverse(self):
        """Inverse coupled result should match individual transform results."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            takeup_weight_and_travel_from_rope_force_and_travel,
        )

        rope_force = Quantity(58839.9, u.newton)
        rope_travel = Quantity(3.0, u.meter)
        strand_count = 2

        coupled_result = takeup_weight_and_travel_from_rope_force_and_travel(
            rope_force=rope_force,
            rope_travel=rope_travel,
            strand_count=strand_count,
        )

        # Compare with individual transforms
        expected_takeup_weight = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=rope_force,
            strand_count=strand_count,
            unit="kilogram",
        )
        expected_takeup_travel = takeup_travel_from_rope_travel(
            rope_travel=rope_travel,
            strand_count=strand_count,
            unit="meter",
        )

        assert coupled_result.takeup_weight.magnitude == pytest.approx(
            expected_takeup_weight.magnitude, rel=1e-9
        )
        assert coupled_result.takeup_travel.magnitude == pytest.approx(
            expected_takeup_travel.magnitude, rel=1e-9
        )

    def test_coupled_inverse_strand_count_validation(self):
        """Inverse coupled API should validate strand_count."""
        from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
            takeup_weight_and_travel_from_rope_force_and_travel,
        )

        rope_force = Quantity(58839.9, u.newton)
        rope_travel = Quantity(3.0, u.meter)

        with pytest.raises(ValueError, match="strand_count must be"):
            takeup_weight_and_travel_from_rope_force_and_travel(
                rope_force=rope_force,
                rope_travel=rope_travel,
                strand_count=0,  # Invalid
            )


class TestCoupledExportChain:
    """Test that coupled APIs are exported through the module hierarchy."""

    def test_coupled_forward_exported_from_core_module(self):
        """Forward coupled API should be available from core.belt_tensions_and_takeup_forces."""
        from eytelwein.belt_conveyor_design.core import (
            belt_tensions_and_takeup_forces,
        )

        assert hasattr(
            belt_tensions_and_takeup_forces, "rope_force_and_travel_from_takeup_weight_and_travel"
        )

    def test_coupled_inverse_exported_from_core_module(self):
        """Inverse coupled API should be available from core.belt_tensions_and_takeup_forces."""
        from eytelwein.belt_conveyor_design.core import (
            belt_tensions_and_takeup_forces,
        )

        assert hasattr(
            belt_tensions_and_takeup_forces, "takeup_weight_and_travel_from_rope_force_and_travel"
        )

    def test_coupled_forward_exported_from_core_init(self):
        """Forward coupled API should be exported from belt_conveyor_design.core."""
        from eytelwein.belt_conveyor_design.core import (
            rope_force_and_travel_from_takeup_weight_and_travel,
        )

        assert callable(rope_force_and_travel_from_takeup_weight_and_travel)

    def test_coupled_inverse_exported_from_core_init(self):
        """Inverse coupled API should be exported from belt_conveyor_design.core."""
        from eytelwein.belt_conveyor_design.core import (
            takeup_weight_and_travel_from_rope_force_and_travel,
        )

        assert callable(takeup_weight_and_travel_from_rope_force_and_travel)

    def test_coupled_forward_exported_from_package(self):
        """Forward coupled API should be exported from belt_conveyor_design package."""
        from eytelwein.belt_conveyor_design import (
            rope_force_and_travel_from_takeup_weight_and_travel,
        )

        assert callable(rope_force_and_travel_from_takeup_weight_and_travel)

    def test_coupled_inverse_exported_from_package(self):
        """Inverse coupled API should be exported from belt_conveyor_design package."""
        from eytelwein.belt_conveyor_design import (
            takeup_weight_and_travel_from_rope_force_and_travel,
        )

        assert callable(takeup_weight_and_travel_from_rope_force_and_travel)
