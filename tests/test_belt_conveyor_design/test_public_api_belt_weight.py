"""
Test public API imports for belt weight functions.

Verifies that belt-weight functions are properly exposed through
eytelwein.belt_conveyor_design public API:
- belt_weight_per_square_meter
- line_load_belt
- line_load_belt_from_belt_weight_per_square_meter
"""

import pytest
from pint import Quantity
from eytelwein.belt_conveyor_design import (
    belt_weight_per_square_meter,
    line_load_belt,
    line_load_belt_from_belt_weight_per_square_meter,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


class TestPublicApiBeltWeight:
    """Test that belt weight functions are exported from public API."""

    def test_belt_weight_per_square_meter_public_api(self):
        """belt_weight_per_square_meter is callable from public API."""
        tension_member_weight = 8.67 * u.kilogram / u.meter**2
        top_cover_thickness = 6 * u.millimeter
        bottom_cover_thickness = 4 * u.millimeter
        rubber_density = 1100 * u.kilogram / u.meter**3

        result = belt_weight_per_square_meter(
            tension_member_weight,
            top_cover_thickness,
            bottom_cover_thickness,
            rubber_density,
            unit="kilogram/meter**2",
            precision=2,
        )

        assert isinstance(result, Quantity)
        # Verify the result has the correct dimensionality (areal mass)
        expected_unit = u.kilogram / u.meter**2
        assert result.dimensionality == expected_unit.dimensionality
        assert result.magnitude > 0

    def test_line_load_belt_public_api(self):
        """line_load_belt is callable from public API."""
        tension_member_weight = 8.67 * u.kilogram / u.meter**2
        belt_width = 1.5 * u.meter
        top_cover_thickness = 6 * u.millimeter
        bottom_cover_thickness = 4 * u.millimeter
        rubber_density = 1100 * u.kilogram / u.meter**3

        result = line_load_belt(
            tension_member_weight,
            belt_width,
            top_cover_thickness,
            bottom_cover_thickness,
            rubber_density,
            unit="kilogram/meter",
            precision=2,
        )

        assert isinstance(result, Quantity)
        # Verify the result has the correct dimensionality (line load)
        expected_unit = u.kilogram / u.meter
        assert result.dimensionality == expected_unit.dimensionality
        assert result.magnitude > 0

    def test_line_load_belt_from_belt_weight_per_square_meter_public_api(self):
        """line_load_belt_from_belt_weight_per_square_meter is callable from public API."""
        belt_weight_m2 = 15.0 * u.kilogram / u.meter**2
        belt_width = 1.5 * u.meter

        result = line_load_belt_from_belt_weight_per_square_meter(
            belt_weight_m2,
            belt_width,
            unit="kilogram/meter",
            precision=2,
        )

        assert isinstance(result, Quantity)
        # Verify the result has the correct dimensionality (line load)
        expected_unit = u.kilogram / u.meter
        assert result.dimensionality == expected_unit.dimensionality
        # 15 kg/m² * 1.5 m = 22.5 kg/m
        assert pytest.approx(result.magnitude, 0.1) == 22.5
