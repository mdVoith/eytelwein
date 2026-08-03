import pytest

from pint import Quantity
from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
    minimum_belt_tension_from_sag_carry,
    takeup_weight_force_from_takeup_weight,
    takeup_weight_from_takeup_weight_force,
)
from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


class TestMinimumBeltTensionFromSagCarryPublic:
    """Test suite for the public minimum_belt_tension_from_sag_carry function."""

    def test_minimum_belt_tension_from_sag_carry_happy_path(self):
        """Public wrapper produces correct result with proper units."""
        line_load_belt = Quantity(5.0, u.kilogram / u.meter)
        line_load_material = Quantity(10.0, u.kilogram / u.meter)
        idler_spacing = Quantity(1.5, u.meter)
        allowable_sag = Quantity(0.01, u.dimensionless)

        result = minimum_belt_tension_from_sag_carry(
            line_load_belt=line_load_belt,
            line_load_material=line_load_material,
            idler_spacing=idler_spacing,
            allowable_sag=allowable_sag,
        )

        # Should return Quantity with force units (default kN)
        assert isinstance(result, Quantity)
        # T = (5+10) * 9.80665 * 1.5 / (8 * 0.01) = 2758.1203125 N = 2.75812 kN
        assert result.magnitude == pytest.approx(2.75812, rel=1e-3)
        assert result.units == u.kilonewton

    def test_minimum_belt_tension_from_sag_carry_unit_conversion(self):
        """Test unit conversion for line loads and idler spacing."""
        # Convert from different units
        line_load_belt = Quantity(5000.0, u.gram / u.meter)
        line_load_material = Quantity(10000.0, u.gram / u.meter)
        idler_spacing = Quantity(1500.0, u.millimeter)
        allowable_sag = Quantity(0.01, u.dimensionless)

        result = minimum_belt_tension_from_sag_carry(
            line_load_belt=line_load_belt,
            line_load_material=line_load_material,
            idler_spacing=idler_spacing,
            allowable_sag=allowable_sag,
        )

        # Should match the result from the kg/m and meter version
        assert result.magnitude == pytest.approx(2.75812, rel=1e-3)

    def test_minimum_belt_tension_from_sag_carry_output_unit_newton(self):
        """Test output unit specification in newtons."""
        line_load_belt = Quantity(5.0, u.kilogram / u.meter)
        line_load_material = Quantity(10.0, u.kilogram / u.meter)
        idler_spacing = Quantity(1.5, u.meter)
        allowable_sag = Quantity(0.01, u.dimensionless)

        result = minimum_belt_tension_from_sag_carry(
            line_load_belt=line_load_belt,
            line_load_material=line_load_material,
            idler_spacing=idler_spacing,
            allowable_sag=allowable_sag,
            unit="newton",
        )

        # Should be in newtons
        assert result.magnitude == pytest.approx(2758.1203125, rel=1e-3)
        assert result.units == u.newton

    def test_minimum_belt_tension_from_sag_carry_invalid_unit(self):
        """Invalid output unit should raise ValueError."""
        line_load_belt = Quantity(5.0, u.kilogram / u.meter)
        line_load_material = Quantity(10.0, u.kilogram / u.meter)
        idler_spacing = Quantity(1.5, u.meter)
        allowable_sag = Quantity(0.01, u.dimensionless)

        with pytest.raises(ValueError, match="Invalid unit"):
            minimum_belt_tension_from_sag_carry(
                line_load_belt=line_load_belt,
                line_load_material=line_load_material,
                idler_spacing=idler_spacing,
                allowable_sag=allowable_sag,
                unit="invalid_unit",
            )

    def test_minimum_belt_tension_from_sag_carry_invalid_line_load_belt_units(self):
        """Invalid line_load_belt units should raise ValueError during conversion."""
        line_load_belt = Quantity(5.0, u.kilogram)  # Wrong units - no /length
        line_load_material = Quantity(10.0, u.kilogram / u.meter)
        idler_spacing = Quantity(1.5, u.meter)
        allowable_sag = Quantity(0.01, u.dimensionless)

        with pytest.raises(ValueError, match="Error in unit conversion"):
            minimum_belt_tension_from_sag_carry(
                line_load_belt=line_load_belt,
                line_load_material=line_load_material,
                idler_spacing=idler_spacing,
                allowable_sag=allowable_sag,
            )

    def test_minimum_belt_tension_from_sag_carry_invalid_line_load_material_units(self):
        """Invalid line_load_material units should raise ValueError during conversion."""
        line_load_belt = Quantity(5.0, u.kilogram / u.meter)
        line_load_material = Quantity(10.0, u.kilogram)  # Wrong units - no /length
        idler_spacing = Quantity(1.5, u.meter)
        allowable_sag = Quantity(0.01, u.dimensionless)

        with pytest.raises(ValueError, match="Error in unit conversion"):
            minimum_belt_tension_from_sag_carry(
                line_load_belt=line_load_belt,
                line_load_material=line_load_material,
                idler_spacing=idler_spacing,
                allowable_sag=allowable_sag,
            )

    def test_minimum_belt_tension_from_sag_carry_invalid_idler_spacing_units(self):
        """Invalid idler_spacing units should raise ValueError during conversion."""
        line_load_belt = Quantity(5.0, u.kilogram / u.meter)
        line_load_material = Quantity(10.0, u.kilogram / u.meter)
        idler_spacing = Quantity(1.5, u.kilogram)  # Wrong units
        allowable_sag = Quantity(0.01, u.dimensionless)

        with pytest.raises(ValueError, match="Error in unit conversion"):
            minimum_belt_tension_from_sag_carry(
                line_load_belt=line_load_belt,
                line_load_material=line_load_material,
                idler_spacing=idler_spacing,
                allowable_sag=allowable_sag,
            )

    def test_minimum_belt_tension_from_sag_carry_negative_line_load_belt(self):
        """Negative line_load_belt should raise ValueError."""
        line_load_belt = Quantity(-5.0, u.kilogram / u.meter)
        line_load_material = Quantity(10.0, u.kilogram / u.meter)
        idler_spacing = Quantity(1.5, u.meter)
        allowable_sag = Quantity(0.01, u.dimensionless)

        with pytest.raises(ValueError, match="line_load_belt cannot be negative"):
            minimum_belt_tension_from_sag_carry(
                line_load_belt=line_load_belt,
                line_load_material=line_load_material,
                idler_spacing=idler_spacing,
                allowable_sag=allowable_sag,
            )

    def test_minimum_belt_tension_from_sag_carry_negative_line_load_material(self):
        """Negative line_load_material should raise ValueError."""
        line_load_belt = Quantity(5.0, u.kilogram / u.meter)
        line_load_material = Quantity(-10.0, u.kilogram / u.meter)
        idler_spacing = Quantity(1.5, u.meter)
        allowable_sag = Quantity(0.01, u.dimensionless)

        with pytest.raises(ValueError, match="line_load_material cannot be negative"):
            minimum_belt_tension_from_sag_carry(
                line_load_belt=line_load_belt,
                line_load_material=line_load_material,
                idler_spacing=idler_spacing,
                allowable_sag=allowable_sag,
            )

    def test_minimum_belt_tension_from_sag_carry_negative_idler_spacing(self):
        """Negative idler_spacing should raise ValueError."""
        line_load_belt = Quantity(5.0, u.kilogram / u.meter)
        line_load_material = Quantity(10.0, u.kilogram / u.meter)
        idler_spacing = Quantity(-1.5, u.meter)
        allowable_sag = Quantity(0.01, u.dimensionless)

        with pytest.raises(ValueError, match="idler_spacing cannot be negative"):
            minimum_belt_tension_from_sag_carry(
                line_load_belt=line_load_belt,
                line_load_material=line_load_material,
                idler_spacing=idler_spacing,
                allowable_sag=allowable_sag,
            )

    def test_minimum_belt_tension_from_sag_carry_non_quantity_raises(self):
        """Non-Quantity inputs should raise ValueError during unit conversion."""
        with pytest.raises(ValueError, match="Error in unit conversion"):
            minimum_belt_tension_from_sag_carry(
                line_load_belt=5.0,  # float, not Quantity
                line_load_material=Quantity(10.0, u.kilogram / u.meter),
                idler_spacing=Quantity(1.5, u.meter),
                allowable_sag=Quantity(0.01, u.dimensionless),
            )

    def test_minimum_belt_tension_from_sag_carry_incompatible_output_unit(self):
        """Incompatible output unit (e.g., meter) should raise ValueError."""
        with pytest.raises(ValueError, match="Error in attaching unit"):
            minimum_belt_tension_from_sag_carry(
                line_load_belt=Quantity(5.0, u.kilogram / u.meter),
                line_load_material=Quantity(10.0, u.kilogram / u.meter),
                idler_spacing=Quantity(1.5, u.meter),
                allowable_sag=Quantity(0.01, u.dimensionless),
                unit="meter",
            )

    def test_minimum_belt_tension_from_sag_carry_no_precision(self):
        """Test with no rounding (precision=None)."""
        line_load_belt = Quantity(5.0, u.kilogram / u.meter)
        line_load_material = Quantity(10.0, u.kilogram / u.meter)
        idler_spacing = Quantity(1.5, u.meter)
        allowable_sag = Quantity(0.01, u.dimensionless)

        result = minimum_belt_tension_from_sag_carry(
            line_load_belt=line_load_belt,
            line_load_material=line_load_material,
            idler_spacing=idler_spacing,
            allowable_sag=allowable_sag,
            precision=None,
        )

        # Should have full precision (unrounded)
        assert isinstance(result, Quantity)
        assert result.units == u.kilonewton

    def test_minimum_belt_tension_from_sag_carry_with_precision_rounding(self):
        """Test explicit precision rounding with non-None value."""
        line_load_belt = Quantity(5.0, u.kilogram / u.meter)
        line_load_material = Quantity(10.0, u.kilogram / u.meter)
        idler_spacing = Quantity(1.5, u.meter)
        allowable_sag = Quantity(0.01, u.dimensionless)

        # Round to 2 decimal places
        result = minimum_belt_tension_from_sag_carry(
            line_load_belt=line_load_belt,
            line_load_material=line_load_material,
            idler_spacing=idler_spacing,
            allowable_sag=allowable_sag,
            precision=2,
        )

        # Unrounded: 2.758120... kN, rounded to 2 decimals: 2.76 kN
        assert isinstance(result, Quantity)
        assert result.magnitude == pytest.approx(2.76, rel=1e-5)
        assert result.units == u.kilonewton


class TestTakeupWeightForceFromTakeupWeightPublic:
    """Test suite for the public takeup_weight_force_from_takeup_weight function."""

    def test_takeup_weight_force_from_takeup_weight_happy_path(self):
        """Public wrapper produces correct result with proper units."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        result = takeup_weight_force_from_takeup_weight(takeup_weight=takeup_weight)

        # Should return Quantity with force units (default kN)
        assert isinstance(result, Quantity)
        # F = 3000 kg * 9.80665 m/s² = 29419.95 N = 29.41995 kN
        assert result.magnitude == pytest.approx(29.41995, rel=1e-4)
        assert result.units == u.kilonewton

    def test_takeup_weight_force_from_takeup_weight_unit_conversion(self):
        """Test unit conversion for takeup weight input."""
        # Convert from grams to kg (equivalent)
        takeup_weight = Quantity(3000000.0, u.gram)

        result = takeup_weight_force_from_takeup_weight(takeup_weight=takeup_weight)

        # Should match the result from kg version
        assert result.magnitude == pytest.approx(29.41995, rel=1e-4)
        assert result.units == u.kilonewton

    def test_takeup_weight_force_from_takeup_weight_output_unit_newton(self):
        """Test output unit specification in newtons."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        result = takeup_weight_force_from_takeup_weight(
            takeup_weight=takeup_weight, unit="newton"
        )

        # Should be in newtons
        assert result.magnitude == pytest.approx(29419.95, rel=1e-4)
        assert result.units == u.newton

    def test_takeup_weight_force_from_takeup_weight_invalid_input_unit(self):
        """Invalid input unit (e.g., meter) should raise ValueError during conversion."""
        takeup_weight = Quantity(3000.0, u.meter)

        with pytest.raises(ValueError, match="Error in unit conversion"):
            takeup_weight_force_from_takeup_weight(takeup_weight=takeup_weight)

    def test_takeup_weight_force_from_takeup_weight_invalid_output_unit(self):
        """Invalid output unit should raise ValueError."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        with pytest.raises(ValueError, match="Invalid unit"):
            takeup_weight_force_from_takeup_weight(
                takeup_weight=takeup_weight, unit="invalid_unit"
            )

    def test_takeup_weight_force_from_takeup_weight_incompatible_output_unit(self):
        """Incompatible output unit (e.g., meter) should raise ValueError."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        with pytest.raises(ValueError, match="Error in attaching unit"):
            takeup_weight_force_from_takeup_weight(
                takeup_weight=takeup_weight, unit="meter"
            )

    def test_takeup_weight_force_from_takeup_weight_negative_weight(self):
        """Negative takeup weight should raise ValueError."""
        takeup_weight = Quantity(-3000.0, u.kilogram)

        with pytest.raises(ValueError, match="takeup_weight cannot be negative"):
            takeup_weight_force_from_takeup_weight(takeup_weight=takeup_weight)

    def test_takeup_weight_force_from_takeup_weight_non_quantity_raises(self):
        """Non-Quantity inputs should raise ValueError during unit conversion."""
        with pytest.raises(ValueError, match="Error in unit conversion"):
            takeup_weight_force_from_takeup_weight(takeup_weight=3000.0)  # float, not Quantity

    def test_takeup_weight_force_from_takeup_weight_no_precision(self):
        """Test with no rounding (precision=None)."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        result = takeup_weight_force_from_takeup_weight(
            takeup_weight=takeup_weight, precision=None
        )

        # Should have full precision (unrounded)
        assert isinstance(result, Quantity)
        assert result.units == u.kilonewton

    def test_takeup_weight_force_from_takeup_weight_with_precision_rounding(self):
        """Test explicit precision rounding with non-None value."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        # Round to 2 decimal places
        result = takeup_weight_force_from_takeup_weight(
            takeup_weight=takeup_weight, precision=2
        )

        # F = 3000 kg * 9.80665 m/s² = 29419.95 N = 29.41995 kN
        # Rounded to 2 decimals: 29.42 kN
        assert isinstance(result, Quantity)
        assert result.magnitude == pytest.approx(29.42, rel=1e-5)
        assert result.units == u.kilonewton


class TestTakeupWeightFromTakeupWeightForcePublic:
    """Test suite for the public takeup_weight_from_takeup_weight_force function."""

    def test_takeup_weight_from_takeup_weight_force_happy_path(self):
        """Public wrapper produces correct result with proper units."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        result = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force
        )

        # Should return Quantity with mass units (default kg)
        assert isinstance(result, Quantity)
        # m = 29419.95 N / 9.80665 m/s² = 3000 kg
        assert result.magnitude == pytest.approx(3000.0, rel=1e-4)
        assert result.units == u.kilogram

    def test_takeup_weight_from_takeup_weight_force_unit_conversion(self):
        """Test unit conversion for takeup weight force input."""
        # Convert from kN to N (equivalent)
        takeup_weight_force = Quantity(29.41995, u.kilonewton)

        result = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force
        )

        # Should match the result from N version
        assert result.magnitude == pytest.approx(3000.0, rel=1e-4)
        assert result.units == u.kilogram

    def test_takeup_weight_from_takeup_weight_force_output_unit_gram(self):
        """Test output unit specification in grams."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        result = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force, unit="gram"
        )

        # Should be in grams
        assert result.magnitude == pytest.approx(3000000.0, rel=1e-4)
        assert result.units == u.gram

    def test_takeup_weight_from_takeup_weight_force_invalid_input_unit(self):
        """Invalid input unit (e.g., meter) should raise ValueError during conversion."""
        takeup_weight_force = Quantity(29419.95, u.meter)

        with pytest.raises(ValueError, match="Error in unit conversion"):
            takeup_weight_from_takeup_weight_force(
                takeup_weight_force=takeup_weight_force
            )

    def test_takeup_weight_from_takeup_weight_force_invalid_output_unit(self):
        """Invalid output unit should raise ValueError."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        with pytest.raises(ValueError, match="Invalid unit"):
            takeup_weight_from_takeup_weight_force(
                takeup_weight_force=takeup_weight_force, unit="invalid_unit"
            )

    def test_takeup_weight_from_takeup_weight_force_incompatible_output_unit(self):
        """Incompatible output unit (e.g., newton) should raise ValueError."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        with pytest.raises(ValueError, match="Error in attaching unit"):
            takeup_weight_from_takeup_weight_force(
                takeup_weight_force=takeup_weight_force, unit="newton"
            )

    def test_takeup_weight_from_takeup_weight_force_negative_force(self):
        """Negative takeup weight force should raise ValueError."""
        takeup_weight_force = Quantity(-29419.95, u.newton)

        with pytest.raises(ValueError, match="takeup_weight_force cannot be negative"):
            takeup_weight_from_takeup_weight_force(
                takeup_weight_force=takeup_weight_force
            )

    def test_takeup_weight_from_takeup_weight_force_non_quantity_raises(self):
        """Non-Quantity inputs should raise ValueError during unit conversion."""
        with pytest.raises(ValueError, match="Error in unit conversion"):
            takeup_weight_from_takeup_weight_force(
                takeup_weight_force=29419.95
            )  # float, not Quantity

    def test_takeup_weight_from_takeup_weight_force_no_precision(self):
        """Test with no rounding (precision=None)."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        result = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force, precision=None
        )

        # Should have full precision (unrounded)
        assert isinstance(result, Quantity)
        assert result.units == u.kilogram

    def test_takeup_weight_from_takeup_weight_force_with_precision_rounding(self):
        """Test explicit precision rounding with non-None value."""
        # 30000 N / 9.80665 m/s² = 3059.07... kg
        takeup_weight_force = Quantity(30000.0, u.newton)

        # Round to 1 decimal place
        result = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force, precision=1
        )

        # Unrounded: 3059.07... kg, rounded to 1 decimal: 3059.1 kg
        assert isinstance(result, Quantity)
        assert result.magnitude == pytest.approx(3059.1, rel=1e-5)
        assert result.units == u.kilogram


class TestTakeupWeightForceFromTakeupWeightWithStrandCountPublic:
    """Test suite for public takeup_weight_force_from_takeup_weight with strand_count."""

    def test_identity_at_strand_count_one(self):
        """Verify backward compatibility: strand_count=1 gives same result as default."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        result = takeup_weight_force_from_takeup_weight(
            takeup_weight=takeup_weight, strand_count=1
        )

        # F = 3000 kg * 9.80665 m/s² / 1 = 29419.95 N = 29.41995 kN
        assert result.magnitude == pytest.approx(29.41995, rel=1e-4)
        assert result.units == u.kilonewton

    def test_default_strand_count_is_one(self):
        """Default strand_count should be 1."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        result_with_default = takeup_weight_force_from_takeup_weight(
            takeup_weight=takeup_weight
        )
        result_with_explicit_one = takeup_weight_force_from_takeup_weight(
            takeup_weight=takeup_weight, strand_count=1
        )

        assert result_with_default.magnitude == pytest.approx(
            result_with_explicit_one.magnitude, rel=1e-9
        )

    def test_reeving_scaling_two_strands(self):
        """Verify ideal reeving: F = m * g / strand_count."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        result = takeup_weight_force_from_takeup_weight(
            takeup_weight=takeup_weight, strand_count=2
        )

        # F = 3000 * 9.80665 / 2 = 14709.975 N = 14.709975 kN
        expected = 3000.0 * 9.80665 / 2 / 1000  # Convert to kN
        assert result.magnitude == pytest.approx(expected, rel=1e-4)
        assert result.units == u.kilonewton

    def test_reeving_scaling_four_strands(self):
        """Verify ideal reeving with 4 strands."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        result = takeup_weight_force_from_takeup_weight(
            takeup_weight=takeup_weight, strand_count=4, unit="newton"
        )

        # F = 3000 * 9.80665 / 4 = 7354.9875 N
        expected = 3000.0 * 9.80665 / 4
        assert result.magnitude == pytest.approx(expected, rel=1e-4)
        assert result.units == u.newton

    def test_unit_conversion_with_strand_count(self):
        """Unit conversion still works with strand_count parameter."""
        takeup_weight = Quantity(3000000.0, u.gram)  # 3000 kg in grams

        result = takeup_weight_force_from_takeup_weight(
            takeup_weight=takeup_weight, strand_count=2, unit="newton"
        )

        # Should match 3000 kg result with 2 strands
        expected = 3000.0 * 9.80665 / 2
        assert result.magnitude == pytest.approx(expected, rel=1e-4)

    def test_negative_strand_count_raises_error(self):
        """Negative strand_count should raise ValueError."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            takeup_weight_force_from_takeup_weight(
                takeup_weight=takeup_weight, strand_count=-1
            )

    def test_zero_strand_count_raises_error(self):
        """strand_count=0 should raise ValueError."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            takeup_weight_force_from_takeup_weight(
                takeup_weight=takeup_weight, strand_count=0
            )

    def test_negative_weight_still_rejected(self):
        """Negative weight should still be rejected after unit conversion."""
        takeup_weight = Quantity(-3000.0, u.kilogram)

        with pytest.raises(ValueError, match="takeup_weight cannot be negative"):
            takeup_weight_force_from_takeup_weight(
                takeup_weight=takeup_weight, strand_count=2
            )

    def test_strand_count_not_integer_raises_error(self):
        """Non-integer strand_count should raise ValueError."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        with pytest.raises(ValueError, match="strand_count.*integer"):
            takeup_weight_force_from_takeup_weight(
                takeup_weight=takeup_weight, strand_count=2.5
            )

    def test_strand_count_with_array_quantity(self):
        """Array Quantity input should broadcast with strand_count."""
        import numpy as np

        weights = np.array([1000.0, 2000.0, 3000.0])
        takeup_weight = Quantity(weights, u.kilogram)

        result = takeup_weight_force_from_takeup_weight(
            takeup_weight=takeup_weight, strand_count=2, unit="newton"
        )

        # Each should be weight * g / 2
        expected = weights * 9.80665 / 2
        assert np.allclose(result.magnitude, expected, rtol=1e-4)


class TestTakeupWeightFromTakeupWeightForceWithStrandCountPublic:
    """Test suite for public takeup_weight_from_takeup_weight_force with strand_count."""

    def test_identity_at_strand_count_one(self):
        """Verify backward compatibility: strand_count=1 gives same result as default."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        result = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force, strand_count=1
        )

        # m = 29419.95 N / 9.80665 m/s² / 1 = 3000 kg
        assert result.magnitude == pytest.approx(3000.0, rel=1e-4)
        assert result.units == u.kilogram

    def test_default_strand_count_is_one(self):
        """Default strand_count should be 1."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        result_with_default = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force
        )
        result_with_explicit_one = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force, strand_count=1
        )

        assert result_with_default.magnitude == pytest.approx(
            result_with_explicit_one.magnitude, rel=1e-9
        )

    def test_reeving_inverse_two_strands(self):
        """Verify ideal reeving inverse: m = F * strand_count / g."""
        takeup_weight_force = Quantity(14709.975, u.newton)

        result = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force, strand_count=2
        )

        # m = 14709.975 * 2 / 9.80665 = 3000 kg
        expected = 14709.975 * 2 / 9.80665
        assert result.magnitude == pytest.approx(expected, rel=1e-4)
        assert result.units == u.kilogram

    def test_reeving_inverse_four_strands(self):
        """Verify ideal reeving inverse with 4 strands."""
        takeup_weight_force = Quantity(7354.9875, u.newton)

        result = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force, strand_count=4, unit="kilogram"
        )

        # m = 7354.9875 * 4 / 9.80665 = 3000 kg
        expected = 7354.9875 * 4 / 9.80665
        assert result.magnitude == pytest.approx(expected, rel=1e-4)

    def test_unit_conversion_with_strand_count(self):
        """Unit conversion still works with strand_count parameter."""
        takeup_weight_force = Quantity(14709.975, u.kilonewton)  # Convert from kN to N internally

        result = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force, strand_count=2, unit="kilogram"
        )

        # Should match expected value
        expected = 14709.975 * 1000 * 2 / 9.80665  # kN to N conversion
        assert result.magnitude == pytest.approx(expected, rel=1e-4)

    def test_negative_strand_count_raises_error(self):
        """Negative strand_count should raise ValueError."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        with pytest.raises(ValueError, match="strand_count.*negative|must be.*positive"):
            takeup_weight_from_takeup_weight_force(
                takeup_weight_force=takeup_weight_force, strand_count=-1
            )

    def test_zero_strand_count_raises_error(self):
        """strand_count=0 should raise ValueError."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            takeup_weight_from_takeup_weight_force(
                takeup_weight_force=takeup_weight_force, strand_count=0
            )

    def test_negative_force_still_rejected(self):
        """Negative force should still be rejected after unit conversion."""
        takeup_weight_force = Quantity(-29419.95, u.newton)

        with pytest.raises(ValueError, match="takeup_weight_force cannot be negative"):
            takeup_weight_from_takeup_weight_force(
                takeup_weight_force=takeup_weight_force, strand_count=2
            )

    def test_strand_count_not_integer_raises_error(self):
        """Non-integer strand_count should raise ValueError."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        with pytest.raises(ValueError, match="strand_count.*integer"):
            takeup_weight_from_takeup_weight_force(
                takeup_weight_force=takeup_weight_force, strand_count=2.5
            )

    def test_round_trip_force_weight_force_with_strand_count(self):
        """Round-trip: force → weight → force should preserve value at any strand_count."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        for sc in [1, 2, 3, 4]:
            weight = takeup_weight_from_takeup_weight_force(
                takeup_weight_force=takeup_weight_force, strand_count=sc
            )
            recovered_force = takeup_weight_force_from_takeup_weight(
                takeup_weight=weight, strand_count=sc, unit="newton"
            )
            assert recovered_force.magnitude == pytest.approx(
                takeup_weight_force.magnitude, rel=1e-4
            )

    def test_strand_count_with_array_quantity(self):
        """Array Quantity input should broadcast with strand_count."""
        import numpy as np

        forces = np.array([9806.65, 19613.3, 29419.95])
        takeup_weight_force = Quantity(forces, u.newton)

        result = takeup_weight_from_takeup_weight_force(
            takeup_weight_force=takeup_weight_force, strand_count=2, unit="kilogram"
        )

        # Each should be force * 2 / g
        expected = forces * 2 / 9.80665
        assert np.allclose(result.magnitude, expected, rtol=1e-4)


class TestBoolStrandCountRejection:
    """Test suite for explicit bool rejection in strand_count parameter."""

    def test_bool_true_strand_count_rejected_takeup_weight_force_from_weight(self):
        """bool(True) should be explicitly rejected as strand_count in takeup_weight_force_from_takeup_weight."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        with pytest.raises(ValueError, match="strand_count.*must be an integer"):
            takeup_weight_force_from_takeup_weight(
                takeup_weight=takeup_weight, strand_count=True  # type: ignore
            )

    def test_bool_false_strand_count_rejected_takeup_weight_force_from_weight(self):
        """bool(False) should be explicitly rejected as strand_count in takeup_weight_force_from_takeup_weight."""
        takeup_weight = Quantity(3000.0, u.kilogram)

        with pytest.raises(ValueError, match="strand_count.*must be an integer"):
            takeup_weight_force_from_takeup_weight(
                takeup_weight=takeup_weight, strand_count=False  # type: ignore
            )

    def test_bool_true_strand_count_rejected_takeup_weight_from_force(self):
        """bool(True) should be explicitly rejected as strand_count in takeup_weight_from_takeup_weight_force."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        with pytest.raises(ValueError, match="strand_count.*must be an integer"):
            takeup_weight_from_takeup_weight_force(
                takeup_weight_force=takeup_weight_force, strand_count=True  # type: ignore
            )

    def test_bool_false_strand_count_rejected_takeup_weight_from_force(self):
        """bool(False) should be explicitly rejected as strand_count in takeup_weight_from_takeup_weight_force."""
        takeup_weight_force = Quantity(29419.95, u.newton)

        with pytest.raises(ValueError, match="strand_count.*must be an integer"):
            takeup_weight_from_takeup_weight_force(
                takeup_weight_force=takeup_weight_force, strand_count=False  # type: ignore
            )


class TestNonNdarrayArrayLikeNegativeValidation:
    """Test suite for hardened negative-input validation with non-ndarray array-like objects."""

    def test_negative_weight_with_list_like_magnitude_raises_valueerror(self):
        """Negative weight with list-like magnitude should normalize to ValueError."""
        # Create a custom array-like class that doesn't support < comparison properly
        class CustomArrayLike:
            def __init__(self, value):
                self.value = value

            def __lt__(self, other):
                # Raise TypeError to simulate comparison failure
                raise TypeError("Cannot compare CustomArrayLike with scalar")

        # Patch Quantity to return our custom array-like magnitude
        import unittest.mock as mock

        with mock.patch.object(
            Quantity, "magnitude", new_callable=mock.PropertyMock
        ) as mock_magnitude:
            mock_magnitude.return_value = CustomArrayLike(-100.0)

            with pytest.raises(ValueError, match="takeup_weight cannot be negative"):
                takeup_weight_force_from_takeup_weight(
                    takeup_weight=Quantity(-3000.0, u.kilogram)
                )

    def test_negative_force_with_list_like_magnitude_raises_valueerror(self):
        """Negative force with list-like magnitude should normalize to ValueError."""
        # Create a custom array-like class that doesn't support < comparison properly
        class CustomArrayLike:
            def __init__(self, value):
                self.value = value

            def __lt__(self, other):
                # Raise TypeError to simulate comparison failure
                raise TypeError("Cannot compare CustomArrayLike with scalar")

        # Patch Quantity to return our custom array-like magnitude
        import unittest.mock as mock

        with mock.patch.object(
            Quantity, "magnitude", new_callable=mock.PropertyMock
        ) as mock_magnitude:
            mock_magnitude.return_value = CustomArrayLike(-100.0)

            with pytest.raises(ValueError, match="takeup_weight_force cannot be negative"):
                takeup_weight_from_takeup_weight_force(
                    takeup_weight_force=Quantity(-29419.95, u.newton)
                )
