import pytest

from pint import Quantity
from eytelwein.belt_conveyor_design.core.belt_tensions_and_takeup_forces import (
    minimum_belt_tension_from_sag_carry,
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
