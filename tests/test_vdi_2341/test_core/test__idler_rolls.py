import pytest
from eytelwein.din_22101 import IdlerSets
from eytelwein.vdi_2341.core._idler_rolls import (
    _load_factor_determining_idler_roll_load_due_to_material,
    _load_factor_determining_idler_roll_load_due_to_conveyor_belt,
)


class TestLoadFactorDeterminingIdlerRollLoadDueToMaterial:
    def test_flat_trough(self):
        # Test with flat trough arrangement
        result = _load_factor_determining_idler_roll_load_due_to_material(
            idler_roll_arrangement=IdlerSets.FLAT_TROUGH, troughing_angle=30
        )
        assert result == 1.0

    def test_v_trough(self):
        # Test with V trough arrangement
        result = _load_factor_determining_idler_roll_load_due_to_material(
            idler_roll_arrangement=IdlerSets.V_TROUGH, troughing_angle=30
        )
        assert result == 0.5

    def test_three_trough(self):
        # Test with three trough arrangement
        result = _load_factor_determining_idler_roll_load_due_to_material(
            idler_roll_arrangement=IdlerSets.THREE_TROUGH, troughing_angle=30
        )
        # Expected: 0.5 + 0.005 * 30 = 0.5 + 0.15 = 0.65
        assert result == 0.65

    def test_three_trough_different_angle(self):
        # Test with three trough arrangement and different angle
        result = _load_factor_determining_idler_roll_load_due_to_material(
            idler_roll_arrangement=IdlerSets.THREE_TROUGH, troughing_angle=45
        )
        # Expected: 0.5 + 0.005 * 45 = 0.5 + 0.225 = 0.725
        assert result == 0.725

    def test_invalid_arrangement(self):
        # Test with invalid arrangement (e.g., DEEP_TROUGH)
        with pytest.raises(ValueError) as excinfo:
            _load_factor_determining_idler_roll_load_due_to_material(
                idler_roll_arrangement=IdlerSets.DEEP_TROUGH, troughing_angle=30
            )
        assert "Invalid idler roll arrangement" in str(excinfo.value)

    def test_invalid_arrangement_five_trough(self):
        # Test with another invalid arrangement
        with pytest.raises(ValueError) as excinfo:
            _load_factor_determining_idler_roll_load_due_to_material(
                idler_roll_arrangement=IdlerSets.FIVE_TROUGH, troughing_angle=30
            )
        assert "Invalid idler roll arrangement" in str(excinfo.value)


class TestLoadFactorDeterminingIdlerRollLoadDueToConveyorBelt:
    def test_flat_trough_arrangement(self):
        """Test load factor calculation for flat trough arrangement."""
        result = _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.FLAT_TROUGH, 500.0, 1200.0
        )
        assert result == 1.0

    def test_v_trough_arrangement(self):
        """Test load factor calculation for V-trough arrangement."""
        result = _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.V_TROUGH, 500.0, 1200.0
        )
        assert result == 0.5

    def test_three_trough_arrangement(self):
        """Test load factor calculation for three-trough arrangement."""
        # Test case: center roll 480mm, belt width 1200mm
        # Expected: (480 + 20) / 1200 = 500 / 1200 = 0.41666...
        result = _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.THREE_TROUGH, 480.0, 1200.0
        )
        expected = (480.0 + 20.0) / 1200.0
        assert result == pytest.approx(expected)

    def test_three_trough_arrangement_different_values(self):
        """Test load factor calculation for three-trough arrangement with different values."""
        # Test case: center roll 600mm, belt width 1000mm
        # Expected: (600 + 20) / 1000 = 620 / 1000 = 0.62
        result = _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.THREE_TROUGH, 600.0, 1000.0
        )
        expected = (600.0 + 20.0) / 1000.0
        assert result == pytest.approx(expected)

    def test_three_trough_arrangement_edge_case_zero_center_length(self):
        """Test load factor calculation with zero center length."""
        # Even with zero center length, the constant 20mm is added
        result = _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.THREE_TROUGH, 0.0, 1200.0
        )
        expected = 20.0 / 1200.0
        assert result == pytest.approx(expected)

    def test_three_trough_arrangement_small_belt_width(self):
        """Test load factor calculation with small belt width."""
        result = _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.THREE_TROUGH, 480.0, 500.0
        )
        expected = (480.0 + 20.0) / 500.0
        assert result == pytest.approx(expected)

    def test_three_trough_arrangement_precision(self):
        """Test calculation precision for three-trough arrangement."""
        result = _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.THREE_TROUGH, 123.456, 789.012
        )
        expected = (123.456 + 20.0) / 789.012
        assert result == pytest.approx(expected, rel=1e-9)

    def test_floating_point_inputs(self):
        """Test that function handles floating point inputs correctly."""
        result = _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
            IdlerSets.THREE_TROUGH, 123.45, 678.90
        )
        expected = (123.45 + 20.0) / 678.90
        assert result == pytest.approx(expected)

    def test_three_trough_arrangement_zero_belt_width(self):
        """Test that zero belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
                IdlerSets.THREE_TROUGH, 480.0, 0.0
            )

    def test_three_trough_arrangement_negative_belt_width(self):
        """Test that negative belt_width raises ValueError."""
        with pytest.raises(ValueError, match="belt_width must be positive"):
            _load_factor_determining_idler_roll_load_due_to_conveyor_belt(
                IdlerSets.THREE_TROUGH, 480.0, -1200.0
            )
