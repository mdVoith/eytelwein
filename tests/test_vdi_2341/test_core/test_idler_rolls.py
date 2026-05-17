import pytest
from eytelwein.din_22101 import IdlerSets
from eytelwein.vdi_2341.core.idler_rolls import (
    load_factor_determining_idler_roll_load_due_to_material,
    load_factor_determining_idler_roll_load_due_to_conveyor_belt,
)

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


class TestLoadFactorDeterminingIdlerRollLoadDueToMaterial:
    def test_flat_trough_with_quantity(self):
        # Test with flat trough arrangement and angle as Quantity
        result = load_factor_determining_idler_roll_load_due_to_material(
            idler_roll_arrangement=IdlerSets.FLAT_TROUGH, troughing_angle=30 * u.degree
        )
        assert result.magnitude == 1.0
        assert result.units == u.dimensionless

    def test_v_trough_with_quantity(self):
        # Test with V trough arrangement and angle as Quantity
        result = load_factor_determining_idler_roll_load_due_to_material(
            idler_roll_arrangement=IdlerSets.V_TROUGH, troughing_angle=30 * u.degree
        )
        assert result.magnitude == 0.5
        assert result.units == u.dimensionless

    def test_three_trough_with_quantity(self):
        # Test with three trough arrangement and angle as Quantity
        result = load_factor_determining_idler_roll_load_due_to_material(
            idler_roll_arrangement=IdlerSets.THREE_TROUGH, troughing_angle=30 * u.degree
        )
        # Expected: 0.5 + 0.005 * 30 = 0.5 + 0.15 = 0.65
        assert result.magnitude == 0.65
        assert result.units == u.dimensionless

    def test_three_trough_different_angle_with_quantity(self):
        # Test with three trough arrangement and different angle as Quantity
        result = load_factor_determining_idler_roll_load_due_to_material(
            idler_roll_arrangement=IdlerSets.THREE_TROUGH, troughing_angle=45 * u.degree
        )
        # Expected: 0.5 + 0.005 * 45 = 0.5 + 0.225 = 0.725
        assert result.magnitude == 0.725
        assert result.units == u.dimensionless

    def test_with_different_angle_unit(self):
        # Test with radians instead of degrees
        result = load_factor_determining_idler_roll_load_due_to_material(
            idler_roll_arrangement=IdlerSets.THREE_TROUGH,
            troughing_angle=(30 * u.degree).to("radian"),
        )
        # Should convert to degrees first, then calculate
        assert result.magnitude == 0.65
        assert result.units == u.dimensionless

    def test_with_precision(self):
        # Test with specified precision
        result = load_factor_determining_idler_roll_load_due_to_material(
            idler_roll_arrangement=IdlerSets.THREE_TROUGH,
            troughing_angle=30 * u.degree,
            precision=2,
        )
        assert result.magnitude == 0.65
        assert result.units == u.dimensionless

    def test_with_custom_unit(self):
        # Test with custom dimensionless unit
        result = load_factor_determining_idler_roll_load_due_to_material(
            idler_roll_arrangement=IdlerSets.THREE_TROUGH,
            troughing_angle=30 * u.degree,
            unit="percent",  # This will need to be scaled
        )
        # Expected result is 0.65 (dimensionless) = 65%
        assert result.magnitude == 65
        assert str(result.units) == "percent"

    def test_invalid_unit(self):
        # Test with invalid (non-dimensionless) unit
        with pytest.raises(ValueError) as excinfo:
            load_factor_determining_idler_roll_load_due_to_material(
                idler_roll_arrangement=IdlerSets.THREE_TROUGH,
                troughing_angle=30 * u.degree,
                unit="meter",
            )
        assert "must be dimensionless" in str(excinfo.value)

    def test_invalid_arrangement(self):
        # Test with invalid arrangement
        with pytest.raises(ValueError) as excinfo:
            load_factor_determining_idler_roll_load_due_to_material(
                idler_roll_arrangement=IdlerSets.DEEP_TROUGH,
                troughing_angle=30 * u.degree,
            )
        assert "Invalid idler roll arrangement" in str(excinfo.value)


class TestLoadFactorDeterminingIdlerRollLoadDueToConveyorBelt:
    def test_flat_trough_arrangement_with_quantities(self):
        """Test load factor calculation for flat trough arrangement with Quantity inputs."""
        result = load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.FLAT_TROUGH, 500 * u.millimeter, 1200 * u.millimeter
        )
        assert result == 1.0

    def test_v_trough_arrangement_with_quantities(self):
        """Test load factor calculation for V-trough arrangement with Quantity inputs."""
        result = load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.V_TROUGH, 500 * u.millimeter, 1200 * u.millimeter
        )
        assert result == 0.5

    def test_three_trough_arrangement_with_quantities(self):
        """Test load factor calculation for three-trough arrangement with Quantity inputs."""
        result = load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.THREE_TROUGH, 480 * u.millimeter, 1200 * u.millimeter
        )
        expected = (480.0 + 20.0) / 1200.0
        assert result == pytest.approx(expected, abs=1e-3)

    def test_different_input_units(self):
        """Test with different but compatible input units."""
        # Using meters for center length, centimeters for belt width
        result = load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.THREE_TROUGH,
            0.48 * u.meter,  # 480 mm
            120 * u.centimeter,  # 1200 mm
        )
        expected = (480.0 + 20.0) / 1200.0
        assert result == pytest.approx(expected, abs=1e-3)

    def test_precision_parameter(self):
        """Test precision parameter functionality."""
        result = load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.THREE_TROUGH,
            123.456 * u.millimeter,
            789.012 * u.millimeter,
            precision=2,
        )
        expected = round((123.456 + 20.0) / 789.012, 2)
        assert result == expected

    def test_zero_center_length_validation(self):
        """Test that zero center length raises ValueError."""
        with pytest.raises(
            ValueError, match="Center idler roll length must be positive"
        ):
            load_factor_determining_idler_roll_load_due_to_conveyor_belt(
                IdlerSets.THREE_TROUGH, 0 * u.millimeter, 1200 * u.millimeter
            )

    def test_negative_belt_width_validation(self):
        """Test that negative belt width raises ValueError."""
        with pytest.raises(ValueError, match="Belt width must be positive"):
            load_factor_determining_idler_roll_load_due_to_conveyor_belt(
                IdlerSets.THREE_TROUGH, 480 * u.millimeter, -1200 * u.millimeter
            )

    def test_incompatible_units_center_length(self):
        """Test that incompatible units for center length raise ValueError."""
        with pytest.raises(ValueError, match="Error in converting units"):
            load_factor_determining_idler_roll_load_due_to_conveyor_belt(
                IdlerSets.THREE_TROUGH,
                480 * u.kilogram,  # Wrong dimension
                1200 * u.millimeter,
            )

    def test_that_result_is_dimensionless(self):
        """Test that the result is dimensionless."""
        result = load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.THREE_TROUGH, 480 * u.millimeter, 1200 * u.millimeter
        )
        assert result.units == u.dimensionless
