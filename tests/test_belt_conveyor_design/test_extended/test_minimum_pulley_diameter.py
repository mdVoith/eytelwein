"""
Tests for public Pint Quantity wrapper functions in extended minimum pulley diameter module.
These wrap private float functions with unit conversion and validation.
Tests follow strict TDD: failing tests first.
"""

import math
import pytest
from pint import Quantity

from eytelwein.belt_conveyor_design.extended.minimum_pulley_diameter import (
    resulting_force_from_belt_tensions_and_wrap_angle,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


class TestResultingForceFromBeltTensionsAndWrapAngle:
    """Test public Pint wrapper for resulting_force_from_belt_tensions_and_wrap_angle"""

    def test_resulting_force_from_belt_tensions_and_wrap_angle_typical_values(self):
        """Test with typical values (kilonewton and radian)"""
        belt_tension_upper = Quantity(50.0, u.kilonewton)
        belt_tension_lower = Quantity(20.0, u.kilonewton)
        wrap_angle = Quantity(math.pi / 2, u.radian)  # 90 degrees
        result = resulting_force_from_belt_tensions_and_wrap_angle(
            belt_tension_upper, belt_tension_lower, wrap_angle, precision=None
        )
        assert isinstance(result, Quantity)
        assert result.units == u.kilonewton
        # F_T = sqrt((50 - 20*cos(π/2))^2 + (20*sin(π/2))^2)
        # F_T = sqrt((50 - 0)^2 + 20^2) = sqrt(2500 + 400) = sqrt(2900)
        expected_magnitude = math.sqrt(50**2 + 20**2)
        assert result.magnitude == pytest.approx(expected_magnitude, rel=1e-9)

    def test_resulting_force_from_belt_tensions_and_wrap_angle_degree_input(self):
        """Test with wrap angle in degrees gives same result as radian case"""
        belt_tension_upper = Quantity(50.0, u.kilonewton)
        belt_tension_lower = Quantity(20.0, u.kilonewton)
        wrap_angle = Quantity(90.0, u.degree)
        result = resulting_force_from_belt_tensions_and_wrap_angle(
            belt_tension_upper, belt_tension_lower, wrap_angle, precision=None
        )
        assert isinstance(result, Quantity)
        assert result.units == u.kilonewton
        # Same expected magnitude as radian case (90 degrees = π/2 radians)
        expected_magnitude = math.sqrt(50**2 + 20**2)
        assert result.magnitude == pytest.approx(expected_magnitude, rel=1e-9)

    def test_resulting_force_from_belt_tensions_and_wrap_angle_mixed_force_units(self):
        """Test with mixed force units (newton and kilonewton)"""
        belt_tension_upper = Quantity(50000.0, u.newton)
        belt_tension_lower = Quantity(20.0, u.kilonewton)
        wrap_angle = Quantity(math.pi / 2, u.radian)
        result = resulting_force_from_belt_tensions_and_wrap_angle(
            belt_tension_upper, belt_tension_lower, wrap_angle, precision=None
        )
        assert isinstance(result, Quantity)
        assert result.units == u.kilonewton
        # Same calculation: 50 kN upper, 20 kN lower, 90-degree wrap
        expected_magnitude = math.sqrt(50**2 + 20**2)
        assert result.magnitude == pytest.approx(expected_magnitude, rel=1e-9)

    def test_resulting_force_from_belt_tensions_and_wrap_angle_invalid_tension_unit(
        self,
    ):
        """Test with invalid unit for upper belt tension"""
        belt_tension_upper = Quantity(50.0, u.meter)  # Wrong unit!
        belt_tension_lower = Quantity(20.0, u.kilonewton)
        wrap_angle = Quantity(3.14159 / 2, u.radian)
        with pytest.raises(ValueError):
            resulting_force_from_belt_tensions_and_wrap_angle(
                belt_tension_upper, belt_tension_lower, wrap_angle
            )

    def test_resulting_force_from_belt_tensions_and_wrap_angle_invalid_angle_unit(self):
        """Test with invalid unit for wrap angle"""
        belt_tension_upper = Quantity(50.0, u.kilonewton)
        belt_tension_lower = Quantity(20.0, u.kilonewton)
        wrap_angle = Quantity(90.0, u.meter)  # Wrong unit!
        with pytest.raises(ValueError):
            resulting_force_from_belt_tensions_and_wrap_angle(
                belt_tension_upper, belt_tension_lower, wrap_angle
            )

    def test_resulting_force_from_belt_tensions_and_wrap_angle_negative_upper_raises(
        self,
    ):
        """Test that negative upper tension raises ValueError"""
        belt_tension_upper = Quantity(-50.0, u.kilonewton)
        belt_tension_lower = Quantity(20.0, u.kilonewton)
        wrap_angle = Quantity(3.14159 / 2, u.radian)
        with pytest.raises(ValueError):
            resulting_force_from_belt_tensions_and_wrap_angle(
                belt_tension_upper, belt_tension_lower, wrap_angle
            )

    def test_resulting_force_from_belt_tensions_and_wrap_angle_negative_lower_raises(
        self,
    ):
        """Test that negative lower tension raises ValueError"""
        belt_tension_upper = Quantity(50.0, u.kilonewton)
        belt_tension_lower = Quantity(-20.0, u.kilonewton)
        wrap_angle = Quantity(3.14159 / 2, u.radian)
        with pytest.raises(ValueError):
            resulting_force_from_belt_tensions_and_wrap_angle(
                belt_tension_upper, belt_tension_lower, wrap_angle
            )

    def test_resulting_force_from_belt_tensions_and_wrap_angle_precision(self):
        """Test precision parameter"""
        belt_tension_upper = Quantity(50.0, u.kilonewton)
        belt_tension_lower = Quantity(20.0, u.kilonewton)
        wrap_angle = Quantity(math.pi / 2, u.radian)
        result = resulting_force_from_belt_tensions_and_wrap_angle(
            belt_tension_upper, belt_tension_lower, wrap_angle, precision=3
        )
        assert isinstance(result, Quantity)
        # Verify precision was applied by comparing with unrounded version
        result_no_precision = resulting_force_from_belt_tensions_and_wrap_angle(
            belt_tension_upper, belt_tension_lower, wrap_angle, precision=None
        )
        # With precision, magnitude should have 3 decimal places (or fewer)
        assert result.magnitude == pytest.approx(
            round(result_no_precision.magnitude, 3)
        )
        # Verify expected magnitude is correct
        expected_magnitude = math.sqrt(50**2 + 20**2)
        assert result_no_precision.magnitude == pytest.approx(
            expected_magnitude, rel=1e-9
        )

    def test_resulting_force_from_belt_tensions_and_wrap_angle_output_unit(self):
        """Test custom output unit"""
        belt_tension_upper = Quantity(50.0, u.kilonewton)
        belt_tension_lower = Quantity(20.0, u.kilonewton)
        wrap_angle = Quantity(math.pi / 2, u.radian)
        result = resulting_force_from_belt_tensions_and_wrap_angle(
            belt_tension_upper,
            belt_tension_lower,
            wrap_angle,
            unit="newton",
            precision=None,
        )
        assert isinstance(result, Quantity)
        assert result.units == u.newton
        # Expected magnitude in newton (1 kN = 1000 N)
        expected_magnitude_kn = math.sqrt(50**2 + 20**2)
        expected_magnitude_n = expected_magnitude_kn * 1000
        assert result.magnitude == pytest.approx(expected_magnitude_n, rel=1e-9)


class TestImportSmoke:
    """Smoke tests for top-level and extended imports of new exports"""

    def test_import_from_extended_module(self):
        """Test import from eytelwein.belt_conveyor_design.extended"""
        # This should not raise
        from eytelwein.belt_conveyor_design.extended import (
            resulting_force_from_belt_tensions_and_wrap_angle,
        )

        assert callable(resulting_force_from_belt_tensions_and_wrap_angle)

    def test_import_from_belt_conveyor_design_module(self):
        """Test import from eytelwein.belt_conveyor_design"""
        # This should not raise
        from eytelwein.belt_conveyor_design import (
            resulting_force_from_belt_tensions_and_wrap_angle,
        )

        assert callable(resulting_force_from_belt_tensions_and_wrap_angle)

    def test_top_level_import_via_module_path(self):
        """Test accessing new export via eytelwein.belt_conveyor_design path"""
        import eytelwein

        assert hasattr(
            eytelwein.belt_conveyor_design,
            "resulting_force_from_belt_tensions_and_wrap_angle",
        )
        assert callable(
            eytelwein.belt_conveyor_design.resulting_force_from_belt_tensions_and_wrap_angle
        )
