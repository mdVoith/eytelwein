import pytest


from eytelwein.belt_conveyor_design.core._belt_tensions_and_takeup_forces import (
    _minimum_belt_tension_from_sag_carry,
    _takeup_weight_force_from_takeup_weight,
    _takeup_weight_from_takeup_weight_force,
)


class TestMinimumBeltTensionFromSagCarry:
    """Test suite for the private _minimum_belt_tension_from_sag_carry function."""

    def test_minimum_belt_tension_from_sag_carry_happy_path(self):
        """Calculate minimum belt tension with typical carry run values."""
        # line_load_belt: 5 kg/m
        # line_load_material: 10 kg/m
        # idler_spacing: 1.5 m
        # allowable_sag: 0.01 (1% as dimensionless fraction)
        # Expected: T = (5 + 10) * 9.80665 * 1.5 / (8 * 0.01)
        #                = 15 * 9.80665 * 1.5 / 0.08 = 220.649625 / 0.08 = 2758.1203125 N
        result = _minimum_belt_tension_from_sag_carry(
            line_load_belt_kg_per_m=5.0,
            line_load_material_kg_per_m=10.0,
            idler_spacing_m=1.5,
            allowable_sag=0.01,
        )
        assert result == pytest.approx(2758.1203125, rel=1e-5)

    def test_minimum_belt_tension_from_sag_carry_zero_load_belt(self):
        """Test with zero belt load (material load only)."""
        result = _minimum_belt_tension_from_sag_carry(
            line_load_belt_kg_per_m=0.0,
            line_load_material_kg_per_m=10.0,
            idler_spacing_m=1.5,
            allowable_sag=0.01,
        )
        # T = (0 + 10) * 9.80665 * 1.5 / 0.08 = 147.09975 / 0.08 = 1838.746875 N
        assert result == pytest.approx(1838.746875, rel=1e-5)

    def test_minimum_belt_tension_from_sag_carry_zero_material_load(self):
        """Test with zero material load (belt load only)."""
        result = _minimum_belt_tension_from_sag_carry(
            line_load_belt_kg_per_m=5.0,
            line_load_material_kg_per_m=0.0,
            idler_spacing_m=1.5,
            allowable_sag=0.01,
        )
        # T = (5 + 0) * 9.80665 * 1.5 / 0.08 = 73.549875 / 0.08 = 919.3734375 N
        assert result == pytest.approx(919.3734375, rel=1e-5)

    def test_minimum_belt_tension_from_sag_carry_smaller_sag_higher_tension(self):
        """Test that smaller sag requires higher tension (inverse relationship)."""
        result_large_sag = _minimum_belt_tension_from_sag_carry(
            line_load_belt_kg_per_m=5.0,
            line_load_material_kg_per_m=10.0,
            idler_spacing_m=1.5,
            allowable_sag=0.02,
        )
        result_small_sag = _minimum_belt_tension_from_sag_carry(
            line_load_belt_kg_per_m=5.0,
            line_load_material_kg_per_m=10.0,
            idler_spacing_m=1.5,
            allowable_sag=0.01,
        )
        # Smaller sag requires higher tension (inverse relationship)
        assert result_small_sag > result_large_sag

    def test_minimum_belt_tension_from_sag_carry_zero_sag_raises_error(self):
        """Sag percent of zero should raise ValueError."""
        with pytest.raises(ValueError, match="allowable_sag.*must be positive"):
            _minimum_belt_tension_from_sag_carry(
                line_load_belt_kg_per_m=5.0,
                line_load_material_kg_per_m=10.0,
                idler_spacing_m=1.5,
                allowable_sag=0.0,
            )

    def test_minimum_belt_tension_from_sag_carry_negative_sag_raises_error(self):
        """Negative sag percent should raise ValueError."""
        with pytest.raises(ValueError, match="allowable_sag.*must be positive"):
            _minimum_belt_tension_from_sag_carry(
                line_load_belt_kg_per_m=5.0,
                line_load_material_kg_per_m=10.0,
                idler_spacing_m=1.5,
                allowable_sag=-1.0,
            )

    def test_minimum_belt_tension_from_sag_carry_different_spacings(self):
        """Test with different idler spacings (longer spacing = higher tension needed)."""
        result_short_spacing = _minimum_belt_tension_from_sag_carry(
            line_load_belt_kg_per_m=5.0,
            line_load_material_kg_per_m=10.0,
            idler_spacing_m=1.0,
            allowable_sag=0.01,
        )
        result_long_spacing = _minimum_belt_tension_from_sag_carry(
            line_load_belt_kg_per_m=5.0,
            line_load_material_kg_per_m=10.0,
            idler_spacing_m=2.0,
            allowable_sag=0.01,
        )
        # Longer spacing requires higher tension
        assert result_long_spacing > result_short_spacing


class TestTakeupWeightForceFromTakeupWeight:
    """Test suite for the private _takeup_weight_force_from_takeup_weight function."""

    def test_takeup_weight_force_from_takeup_weight_happy_path(self):
        """Convert takeup weight to takeup weight force with typical value."""
        # 100 kg → 100 * 9.80665 N = 980.665 N
        result = _takeup_weight_force_from_takeup_weight(takeup_weight_kg=100.0)
        assert result == pytest.approx(980.665, rel=1e-5)

    def test_takeup_weight_force_from_takeup_weight_zero_value(self):
        """Convert zero takeup weight to zero force."""
        result = _takeup_weight_force_from_takeup_weight(takeup_weight_kg=0.0)
        assert result == pytest.approx(0.0, abs=1e-9)


class TestTakeupWeightFromTakeupWeightForce:
    """Test suite for the private _takeup_weight_from_takeup_weight_force function."""

    def test_takeup_weight_from_takeup_weight_force_happy_path(self):
        """Convert takeup weight force to takeup weight with typical value."""
        # 980.665 N → 980.665 / 9.80665 kg = 100 kg
        result = _takeup_weight_from_takeup_weight_force(takeup_weight_force_n=980.665)
        assert result == pytest.approx(100.0, rel=1e-5)

    def test_takeup_weight_from_takeup_weight_force_zero_value(self):
        """Convert zero force to zero takeup weight."""
        result = _takeup_weight_from_takeup_weight_force(takeup_weight_force_n=0.0)
        assert result == pytest.approx(0.0, abs=1e-9)
