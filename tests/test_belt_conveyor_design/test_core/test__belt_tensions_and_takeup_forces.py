import pytest


from eytelwein.belt_conveyor_design.core._belt_tensions_and_takeup_forces import (
    _minimum_belt_tension_from_sag_carry,
    _takeup_weight_force_from_takeup_weight,
    _takeup_weight_from_takeup_weight_force,
    _rope_travel_from_takeup_travel,
    _takeup_travel_from_rope_travel,
    _effort_force_from_load_force,
    _load_force_from_effort_force,
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

    def test_takeup_weight_force_from_takeup_weight_three_thousand_kg(self):
        """Convert 3000 kg takeup weight to force using standard gravity."""
        # 3000 kg -> 3000 * 9.80665 N = 29419.95 N = 29.41995 kN
        result = _takeup_weight_force_from_takeup_weight(takeup_weight_kg=3000.0)
        assert result == pytest.approx(29419.95, rel=1e-5)

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




class TestEffortForceFromLoadForce:
    """Test suite for the private _effort_force_from_load_force function."""

    def test_effort_force_from_load_force_happy_path(self):
        """Convert load force to effort force with typical value and strand_count=1."""
        # 1000 N load / 1 strand = 1000 N effort
        result = _effort_force_from_load_force(load_force_n=1000.0, strand_count=1)
        assert result == pytest.approx(1000.0, rel=1e-5)

    def test_effort_force_from_load_force_two_strands(self):
        """Verify ideal reeving: effort = load / strand_count."""
        # 1000 N load / 2 strands = 500 N effort
        result = _effort_force_from_load_force(load_force_n=1000.0, strand_count=2)
        assert result == pytest.approx(500.0, rel=1e-5)

    def test_effort_force_from_load_force_four_strands(self):
        """Verify ideal reeving with 4 strands."""
        # 2000 N load / 4 strands = 500 N effort
        result = _effort_force_from_load_force(load_force_n=2000.0, strand_count=4)
        assert result == pytest.approx(500.0, rel=1e-5)

    def test_effort_force_from_load_force_zero_load(self):
        """Zero load should yield zero effort."""
        result = _effort_force_from_load_force(load_force_n=0.0, strand_count=2)
        assert result == pytest.approx(0.0, abs=1e-9)

    def test_effort_force_from_load_force_default_strand_count(self):
        """Default strand_count should be 1."""
        result_with_default = _effort_force_from_load_force(load_force_n=1000.0)
        result_with_one = _effort_force_from_load_force(load_force_n=1000.0, strand_count=1)
        assert result_with_default == pytest.approx(result_with_one, rel=1e-9)

    def test_effort_force_from_load_force_strand_count_zero_raises_error(self):
        """strand_count=0 should raise ValueError (division guard)."""
        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            _effort_force_from_load_force(load_force_n=1000.0, strand_count=0)

    def test_effort_force_from_load_force_strand_count_negative_raises_error(self):
        """Negative strand_count should raise ValueError."""
        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            _effort_force_from_load_force(load_force_n=1000.0, strand_count=-2)


class TestLoadForceFromEffortForce:
    """Test suite for the private _load_force_from_effort_force function."""

    def test_load_force_from_effort_force_happy_path(self):
        """Convert effort force to load force with typical value and strand_count=1."""
        # 1000 N effort * 1 strand = 1000 N load
        result = _load_force_from_effort_force(effort_force_n=1000.0, strand_count=1)
        assert result == pytest.approx(1000.0, rel=1e-5)

    def test_load_force_from_effort_force_two_strands(self):
        """Verify ideal reeving inverse: load = effort * strand_count."""
        # 500 N effort * 2 strands = 1000 N load
        result = _load_force_from_effort_force(effort_force_n=500.0, strand_count=2)
        assert result == pytest.approx(1000.0, rel=1e-5)

    def test_load_force_from_effort_force_four_strands(self):
        """Verify ideal reeving inverse with 4 strands."""
        # 500 N effort * 4 strands = 2000 N load
        result = _load_force_from_effort_force(effort_force_n=500.0, strand_count=4)
        assert result == pytest.approx(2000.0, rel=1e-5)

    def test_load_force_from_effort_force_zero_effort(self):
        """Zero effort should yield zero load."""
        result = _load_force_from_effort_force(effort_force_n=0.0, strand_count=2)
        assert result == pytest.approx(0.0, abs=1e-9)

    def test_load_force_from_effort_force_default_strand_count(self):
        """Default strand_count should be 1."""
        result_with_default = _load_force_from_effort_force(effort_force_n=1000.0)
        result_with_one = _load_force_from_effort_force(effort_force_n=1000.0, strand_count=1)
        assert result_with_default == pytest.approx(result_with_one, rel=1e-9)

    def test_load_force_from_effort_force_strand_count_zero_raises_error(self):
        """strand_count=0 should raise ValueError (division guard)."""
        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            _load_force_from_effort_force(effort_force_n=1000.0, strand_count=0)

    def test_load_force_from_effort_force_strand_count_negative_raises_error(self):
        """Negative strand_count should raise ValueError."""
        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            _load_force_from_effort_force(effort_force_n=1000.0, strand_count=-2)

    def test_round_trip_load_to_effort_to_load(self):
        """Round-trip: load → effort → load should preserve value at any strand_count."""
        for sc in [1, 2, 3, 4]:
            original_load = 2000.0
            effort = _effort_force_from_load_force(load_force_n=original_load, strand_count=sc)
            recovered_load = _load_force_from_effort_force(
                effort_force_n=effort, strand_count=sc
            )
            assert recovered_load == pytest.approx(original_load, rel=1e-5)


class TestRopeTravelFromTakeupTravel:
    """Test suite for the private _rope_travel_from_takeup_travel function."""

    def test_identity_at_strand_count_one(self):
        """Verify strand_count=1 is identity: rope_travel = takeup_travel."""
        takeup_travel_m = 1.5
        result = _rope_travel_from_takeup_travel(
            takeup_travel_m=takeup_travel_m, strand_count=1
        )
        assert result == pytest.approx(takeup_travel_m, rel=1e-9)

    def test_scaling_with_strand_count_two(self):
        """Verify ideal reeving: rope_travel = takeup_travel * strand_count."""
        takeup_travel_m = 1.5
        result = _rope_travel_from_takeup_travel(
            takeup_travel_m=takeup_travel_m, strand_count=2
        )
        expected = takeup_travel_m * 2
        assert result == pytest.approx(expected, rel=1e-9)

    def test_scaling_with_strand_count_four(self):
        """Verify scaling for four strands."""
        takeup_travel_m = 1.0
        result = _rope_travel_from_takeup_travel(
            takeup_travel_m=takeup_travel_m, strand_count=4
        )
        expected = takeup_travel_m * 4
        assert result == pytest.approx(expected, rel=1e-9)

    def test_zero_travel_identity(self):
        """Zero travel should yield zero rope travel regardless of strand_count."""
        for sc in [1, 2, 3]:
            result = _rope_travel_from_takeup_travel(
                takeup_travel_m=0.0, strand_count=sc
            )
            assert result == pytest.approx(0.0, abs=1e-9)

    def test_strand_count_zero_raises_error(self):
        """strand_count=0 should raise ValueError (division guard)."""
        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            _rope_travel_from_takeup_travel(
                takeup_travel_m=1.5, strand_count=0
            )

    def test_strand_count_negative_raises_error(self):
        """Negative strand_count should raise ValueError."""
        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            _rope_travel_from_takeup_travel(
                takeup_travel_m=1.5, strand_count=-1
            )


class TestTakeupTravelFromRopeTravel:
    """Test suite for the private _takeup_travel_from_rope_travel function."""

    def test_identity_at_strand_count_one(self):
        """Verify strand_count=1 is identity: takeup_travel = rope_travel."""
        rope_travel_m = 3.0
        result = _takeup_travel_from_rope_travel(
            rope_travel_m=rope_travel_m, strand_count=1
        )
        assert result == pytest.approx(rope_travel_m, rel=1e-9)

    def test_scaling_with_strand_count_two(self):
        """Verify ideal reeving inverse: takeup_travel = rope_travel / strand_count."""
        rope_travel_m = 3.0
        result = _takeup_travel_from_rope_travel(
            rope_travel_m=rope_travel_m, strand_count=2
        )
        expected = rope_travel_m / 2
        assert result == pytest.approx(expected, rel=1e-9)

    def test_scaling_with_strand_count_four(self):
        """Verify scaling for four strands."""
        rope_travel_m = 4.0
        result = _takeup_travel_from_rope_travel(
            rope_travel_m=rope_travel_m, strand_count=4
        )
        expected = rope_travel_m / 4
        assert result == pytest.approx(expected, rel=1e-9)

    def test_zero_travel_identity(self):
        """Zero travel should yield zero takeup travel regardless of strand_count."""
        for sc in [1, 2, 3]:
            result = _takeup_travel_from_rope_travel(
                rope_travel_m=0.0, strand_count=sc
            )
            assert result == pytest.approx(0.0, abs=1e-9)

    def test_strand_count_zero_raises_error(self):
        """strand_count=0 should raise ValueError (division guard)."""
        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            _takeup_travel_from_rope_travel(
                rope_travel_m=3.0, strand_count=0
            )

    def test_strand_count_negative_raises_error(self):
        """Negative strand_count should raise ValueError."""
        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            _takeup_travel_from_rope_travel(
                rope_travel_m=3.0, strand_count=-1
            )

    def test_round_trip_takeup_to_rope_to_takeup(self):
        """Round-trip: takeup → rope → takeup should preserve value at any strand_count."""
        for sc in [1, 2, 3, 4]:
            original_takeup = 1.5
            rope = _rope_travel_from_takeup_travel(
                takeup_travel_m=original_takeup, strand_count=sc
            )
            recovered_takeup = _takeup_travel_from_rope_travel(
                rope_travel_m=rope, strand_count=sc
            )
            assert recovered_takeup == pytest.approx(original_takeup, rel=1e-9)
