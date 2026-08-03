import pytest

from pint import Quantity
from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
    minimum_belt_tension_from_sag_carry,
    takeup_weight_force_from_takeup_weight,
    takeup_weight_from_takeup_weight_force,
    rope_travel_from_takeup_travel,
    takeup_travel_from_rope_travel,
    effort_force_from_load_force,
    load_force_from_effort_force,
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




class TestEffortForceFromLoadForcePublic:
    """Test suite for public effort_force_from_load_force function."""

    def test_effort_force_from_load_force_happy_path(self):
        """Convert load force to effort force with typical value and strand_count=1."""
        load_force = Quantity(2000.0, u.newton)

        result = effort_force_from_load_force(
            load_force=load_force, strand_count=1
        )

        # effort = 2000 N / 1 = 2000 N = 2 kN
        assert result.magnitude == pytest.approx(2.0, rel=1e-4)
        assert result.units == u.kilonewton

    def test_effort_force_from_load_force_two_strands(self):
        """Verify ideal reeving: effort = load / strand_count."""
        load_force = Quantity(2000.0, u.newton)

        result = effort_force_from_load_force(
            load_force=load_force, strand_count=2, unit="newton"
        )

        # effort = 2000 / 2 = 1000 N
        assert result.magnitude == pytest.approx(1000.0, rel=1e-4)
        assert result.units == u.newton

    def test_effort_force_from_load_force_four_strands(self):
        """Verify ideal reeving with 4 strands."""
        load_force = Quantity(4000.0, u.newton)

        result = effort_force_from_load_force(
            load_force=load_force, strand_count=4, unit="kilonewton"
        )

        # effort = 4000 / 4 = 1000 N = 1 kN
        assert result.magnitude == pytest.approx(1.0, rel=1e-4)

    def test_effort_force_from_load_force_unit_conversion(self):
        """Test unit conversion for load force input."""
        load_force = Quantity(2.0, u.kilonewton)

        result = effort_force_from_load_force(
            load_force=load_force, strand_count=2, unit="newton"
        )

        # effort = 2000 N / 2 = 1000 N
        assert result.magnitude == pytest.approx(1000.0, rel=1e-4)

    def test_effort_force_from_load_force_default_strand_count(self):
        """Default strand_count should be 1."""
        load_force = Quantity(2000.0, u.newton)

        result_with_default = effort_force_from_load_force(load_force=load_force)
        result_with_one = effort_force_from_load_force(
            load_force=load_force, strand_count=1
        )

        assert result_with_default.magnitude == pytest.approx(
            result_with_one.magnitude, rel=1e-9
        )

    def test_effort_force_from_load_force_negative_load_raises_error(self):
        """Negative load force should raise ValueError."""
        load_force = Quantity(-2000.0, u.newton)

        with pytest.raises(ValueError, match="load_force cannot be negative"):
            effort_force_from_load_force(load_force=load_force)

    def test_effort_force_from_load_force_negative_strand_count_raises_error(self):
        """Negative strand_count should raise ValueError."""
        load_force = Quantity(2000.0, u.newton)

        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            effort_force_from_load_force(load_force=load_force, strand_count=-1)

    def test_effort_force_from_load_force_zero_strand_count_raises_error(self):
        """strand_count=0 should raise ValueError."""
        load_force = Quantity(2000.0, u.newton)

        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            effort_force_from_load_force(load_force=load_force, strand_count=0)

    def test_effort_force_from_load_force_non_integer_strand_count_raises_error(self):
        """Non-integer strand_count should raise ValueError."""
        load_force = Quantity(2000.0, u.newton)

        with pytest.raises(ValueError, match="strand_count.*integer"):
            effort_force_from_load_force(load_force=load_force, strand_count=2.5)


class TestLoadForceFromEffortForcePublic:
    """Test suite for public load_force_from_effort_force function."""

    def test_load_force_from_effort_force_happy_path(self):
        """Convert effort force to load force with typical value and strand_count=1."""
        effort_force = Quantity(2000.0, u.newton)

        result = load_force_from_effort_force(
            effort_force=effort_force, strand_count=1
        )

        # load = 2000 N * 1 = 2000 N = 2 kN
        assert result.magnitude == pytest.approx(2.0, rel=1e-4)
        assert result.units == u.kilonewton

    def test_load_force_from_effort_force_two_strands(self):
        """Verify ideal reeving inverse: load = effort * strand_count."""
        effort_force = Quantity(1000.0, u.newton)

        result = load_force_from_effort_force(
            effort_force=effort_force, strand_count=2, unit="newton"
        )

        # load = 1000 * 2 = 2000 N
        assert result.magnitude == pytest.approx(2000.0, rel=1e-4)
        assert result.units == u.newton

    def test_load_force_from_effort_force_four_strands(self):
        """Verify ideal reeving inverse with 4 strands."""
        effort_force = Quantity(1000.0, u.newton)

        result = load_force_from_effort_force(
            effort_force=effort_force, strand_count=4, unit="kilonewton"
        )

        # load = 1000 * 4 = 4000 N = 4 kN
        assert result.magnitude == pytest.approx(4.0, rel=1e-4)

    def test_load_force_from_effort_force_unit_conversion(self):
        """Test unit conversion for effort force input."""
        effort_force = Quantity(1.0, u.kilonewton)

        result = load_force_from_effort_force(
            effort_force=effort_force, strand_count=2, unit="newton"
        )

        # load = 1000 * 2 = 2000 N
        assert result.magnitude == pytest.approx(2000.0, rel=1e-4)

    def test_load_force_from_effort_force_default_strand_count(self):
        """Default strand_count should be 1."""
        effort_force = Quantity(2000.0, u.newton)

        result_with_default = load_force_from_effort_force(effort_force=effort_force)
        result_with_one = load_force_from_effort_force(
            effort_force=effort_force, strand_count=1
        )

        assert result_with_default.magnitude == pytest.approx(
            result_with_one.magnitude, rel=1e-9
        )

    def test_load_force_from_effort_force_negative_effort_raises_error(self):
        """Negative effort force should raise ValueError."""
        effort_force = Quantity(-2000.0, u.newton)

        with pytest.raises(ValueError, match="effort_force cannot be negative"):
            load_force_from_effort_force(effort_force=effort_force)

    def test_load_force_from_effort_force_negative_strand_count_raises_error(self):
        """Negative strand_count should raise ValueError."""
        effort_force = Quantity(2000.0, u.newton)

        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            load_force_from_effort_force(effort_force=effort_force, strand_count=-1)

    def test_load_force_from_effort_force_zero_strand_count_raises_error(self):
        """strand_count=0 should raise ValueError."""
        effort_force = Quantity(2000.0, u.newton)

        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            load_force_from_effort_force(effort_force=effort_force, strand_count=0)

    def test_load_force_from_effort_force_non_integer_strand_count_raises_error(self):
        """Non-integer strand_count should raise ValueError."""
        effort_force = Quantity(2000.0, u.newton)

        with pytest.raises(ValueError, match="strand_count.*integer"):
            load_force_from_effort_force(effort_force=effort_force, strand_count=2.5)

    def test_round_trip_effort_load_effort(self):
        """Round-trip: effort → load → effort should preserve value at any strand_count."""
        for sc in [1, 2, 3, 4]:
            original_effort = Quantity(1000.0, u.newton)
            load = load_force_from_effort_force(
                effort_force=original_effort, strand_count=sc
            )
            recovered_effort = effort_force_from_load_force(
                load_force=load, strand_count=sc, unit="newton"
            )
            assert recovered_effort.magnitude == pytest.approx(
                original_effort.magnitude, rel=1e-4
            )


class TestRopeTravelFromTakeupTravelPublic:
    """Test suite for public rope_travel_from_takeup_travel function with reeving."""

    def test_identity_at_strand_count_one(self):
        """Verify backward compatibility: strand_count=1 is identity."""
        takeup_travel = Quantity(1.5, u.meter)

        result = rope_travel_from_takeup_travel(
            takeup_travel=takeup_travel, strand_count=1
        )

        # rope_travel = 1.5 * 1 = 1.5 m
        assert result.magnitude == pytest.approx(1.5, rel=1e-9)
        assert result.units == u.meter

    def test_default_strand_count_is_one(self):
        """Default strand_count should be 1."""
        takeup_travel = Quantity(1.5, u.meter)

        result_with_default = rope_travel_from_takeup_travel(
            takeup_travel=takeup_travel
        )
        result_with_explicit_one = rope_travel_from_takeup_travel(
            takeup_travel=takeup_travel, strand_count=1
        )

        assert result_with_default.magnitude == pytest.approx(
            result_with_explicit_one.magnitude, rel=1e-9
        )

    def test_reeving_scaling_two_strands(self):
        """Verify ideal reeving: rope_travel = takeup_travel * strand_count."""
        takeup_travel = Quantity(1.5, u.meter)

        result = rope_travel_from_takeup_travel(
            takeup_travel=takeup_travel, strand_count=2
        )

        # rope_travel = 1.5 * 2 = 3.0 m
        assert result.magnitude == pytest.approx(3.0, rel=1e-9)
        assert result.units == u.meter

    def test_reeving_scaling_four_strands(self):
        """Verify ideal reeving with 4 strands."""
        takeup_travel = Quantity(0.5, u.meter)

        result = rope_travel_from_takeup_travel(
            takeup_travel=takeup_travel, strand_count=4, unit="millimeter"
        )

        # rope_travel = 0.5 * 4 = 2.0 m = 2000 mm
        assert result.magnitude == pytest.approx(2000.0, rel=1e-6)
        assert result.units == u.millimeter

    def test_unit_conversion_with_strand_count(self):
        """Unit conversion still works with strand_count parameter."""
        takeup_travel = Quantity(1500.0, u.millimeter)

        result = rope_travel_from_takeup_travel(
            takeup_travel=takeup_travel, strand_count=2, unit="meter"
        )

        # rope_travel = 1.5 m * 2 = 3.0 m
        assert result.magnitude == pytest.approx(3.0, rel=1e-9)
        assert result.units == u.meter

    def test_negative_strand_count_raises_error(self):
        """Negative strand_count should raise ValueError."""
        takeup_travel = Quantity(1.5, u.meter)

        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            rope_travel_from_takeup_travel(
                takeup_travel=takeup_travel, strand_count=-1
            )

    def test_zero_strand_count_raises_error(self):
        """strand_count=0 should raise ValueError."""
        takeup_travel = Quantity(1.5, u.meter)

        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            rope_travel_from_takeup_travel(
                takeup_travel=takeup_travel, strand_count=0
            )

    def test_bool_strand_count_raises_error(self):
        """Bool strand_count should raise ValueError."""
        takeup_travel = Quantity(1.5, u.meter)

        with pytest.raises(ValueError, match="strand_count.*must be.*int"):
            rope_travel_from_takeup_travel(
                takeup_travel=takeup_travel, strand_count=True  # type: ignore
            )

    def test_rope_travel_array_broadcast(self):
        """Array Quantity input should broadcast with strand_count."""
        import numpy as np

        travels = np.array([1.0, 1.5, 2.0])
        takeup_travel = Quantity(travels, u.meter)

        result = rope_travel_from_takeup_travel(
            takeup_travel=takeup_travel, strand_count=2, unit="meter"
        )

        # Each should be takeup_travel * strand_count
        expected = travels * 2
        assert np.allclose(result.magnitude, expected, rtol=1e-9)


class TestTakeupTravelFromRopeTravelPublic:
    """Test suite for public takeup_travel_from_rope_travel function (reeving inverse)."""

    def test_identity_at_strand_count_one(self):
        """Verify backward compatibility: strand_count=1 is identity."""
        rope_travel = Quantity(3.0, u.meter)

        result = takeup_travel_from_rope_travel(
            rope_travel=rope_travel, strand_count=1
        )

        # takeup_travel = 3.0 / 1 = 3.0 m
        assert result.magnitude == pytest.approx(3.0, rel=1e-9)
        assert result.units == u.meter

    def test_default_strand_count_is_one(self):
        """Default strand_count should be 1."""
        rope_travel = Quantity(3.0, u.meter)

        result_with_default = takeup_travel_from_rope_travel(
            rope_travel=rope_travel
        )
        result_with_explicit_one = takeup_travel_from_rope_travel(
            rope_travel=rope_travel, strand_count=1
        )

        assert result_with_default.magnitude == pytest.approx(
            result_with_explicit_one.magnitude, rel=1e-9
        )

    def test_reeving_inverse_two_strands(self):
        """Verify ideal reeving inverse: takeup_travel = rope_travel / strand_count."""
        rope_travel = Quantity(3.0, u.meter)

        result = takeup_travel_from_rope_travel(
            rope_travel=rope_travel, strand_count=2
        )

        # takeup_travel = 3.0 / 2 = 1.5 m
        assert result.magnitude == pytest.approx(1.5, rel=1e-9)
        assert result.units == u.meter

    def test_reeving_inverse_four_strands(self):
        """Verify ideal reeving inverse with 4 strands."""
        rope_travel = Quantity(4000.0, u.millimeter)

        result = takeup_travel_from_rope_travel(
            rope_travel=rope_travel, strand_count=4, unit="meter"
        )

        # takeup_travel = 4.0 / 4 = 1.0 m
        assert result.magnitude == pytest.approx(1.0, rel=1e-9)
        assert result.units == u.meter

    def test_unit_conversion_with_strand_count(self):
        """Unit conversion still works with strand_count parameter."""
        rope_travel = Quantity(3000.0, u.millimeter)

        result = takeup_travel_from_rope_travel(
            rope_travel=rope_travel, strand_count=2, unit="meter"
        )

        # takeup_travel = 3.0 / 2 = 1.5 m
        assert result.magnitude == pytest.approx(1.5, rel=1e-9)
        assert result.units == u.meter

    def test_negative_strand_count_raises_error(self):
        """Negative strand_count should raise ValueError."""
        rope_travel = Quantity(3.0, u.meter)

        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            takeup_travel_from_rope_travel(
                rope_travel=rope_travel, strand_count=-1
            )

    def test_zero_strand_count_raises_error(self):
        """strand_count=0 should raise ValueError."""
        rope_travel = Quantity(3.0, u.meter)

        with pytest.raises(ValueError, match="strand_count.*must be.*positive"):
            takeup_travel_from_rope_travel(
                rope_travel=rope_travel, strand_count=0
            )

    def test_bool_strand_count_raises_error(self):
        """Bool strand_count should raise ValueError."""
        rope_travel = Quantity(3.0, u.meter)

        with pytest.raises(ValueError, match="strand_count.*must be.*int"):
            takeup_travel_from_rope_travel(
                rope_travel=rope_travel, strand_count=True  # type: ignore
            )

    def test_round_trip_takeup_to_rope_to_takeup(self):
        """Round-trip: takeup → rope → takeup should preserve value at any strand_count."""
        for sc in [1, 2, 3, 4]:
            original_takeup = Quantity(1.5, u.meter)
            rope = rope_travel_from_takeup_travel(
                takeup_travel=original_takeup, strand_count=sc
            )
            recovered_takeup = takeup_travel_from_rope_travel(
                rope_travel=rope, strand_count=sc
            )
            assert recovered_takeup.magnitude == pytest.approx(
                original_takeup.magnitude, rel=1e-9
            )

    def test_rope_travel_from_takeup_travel_array_broadcast(self):
        """Array Quantity input should broadcast with strand_count."""
        import numpy as np

        travels = np.array([1.0, 1.5, 2.0])
        takeup_travel = Quantity(travels, u.meter)

        result = rope_travel_from_takeup_travel(
            takeup_travel=takeup_travel, strand_count=2, unit="meter"
        )

        # Each should be takeup_travel * strand_count
        expected = travels * 2
        assert np.allclose(result.magnitude, expected, rtol=1e-9)

    def test_takeup_travel_from_rope_travel_array_broadcast(self):
        """Array Quantity input should broadcast with strand_count for inverse."""
        import numpy as np

        travels = np.array([2.0, 3.0, 4.0])
        rope_travel = Quantity(travels, u.meter)

        result = takeup_travel_from_rope_travel(
            rope_travel=rope_travel, strand_count=2, unit="meter"
        )

        # Each should be rope_travel / strand_count
        expected = travels / 2
        assert np.allclose(result.magnitude, expected, rtol=1e-9)


class TestWorkedReevingExamplesPublic:
    """Pin exact worked reeving examples discussed during design review."""

    def test_n6_effort_100n_gives_600n_load_and_6m_rope_travel(self):
        """For n=6, 100 N effort and 1 m load lift should yield 600 N load and 6 m rope travel."""
        effort_force = Quantity(100.0, u.newton)
        load_travel = Quantity(1.0, u.meter)

        load_force = load_force_from_effort_force(
            effort_force=effort_force,
            strand_count=6,
            unit="newton",
        )
        rope_travel = rope_travel_from_takeup_travel(
            takeup_travel=load_travel,
            strand_count=6,
            unit="meter",
        )

        assert load_force.magnitude == pytest.approx(600.0, rel=1e-9)
        assert load_force.units == u.newton
        assert rope_travel.magnitude == pytest.approx(6.0, rel=1e-9)
        assert rope_travel.units == u.meter

    def test_n2_load_600n_gives_300n_effort_and_2m_rope_travel(self):
        """For n=2, 600 N load and 1 m load lift should yield 300 N effort and 2 m rope travel."""
        load_force = Quantity(600.0, u.newton)
        load_travel = Quantity(1.0, u.meter)

        effort_force = effort_force_from_load_force(
            load_force=load_force,
            strand_count=2,
            unit="newton",
        )
        rope_travel = rope_travel_from_takeup_travel(
            takeup_travel=load_travel,
            strand_count=2,
            unit="meter",
        )

        assert effort_force.magnitude == pytest.approx(300.0, rel=1e-9)
        assert effort_force.units == u.newton
        assert rope_travel.magnitude == pytest.approx(2.0, rel=1e-9)
        assert rope_travel.units == u.meter


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
