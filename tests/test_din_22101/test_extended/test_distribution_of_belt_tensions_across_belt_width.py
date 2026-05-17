import pytest

from eytelwein.din_22101.extended.distribution_of_belt_tensions_across_belt_width import (
    distance_belt_edge_deepest_level_of_trough,
)

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def test_distance_belt_edge_deepest_level_of_trough_valid():
    result = distance_belt_edge_deepest_level_of_trough(
        u.Quantity(100, "millimeter"), u.Quantity(20, "degrees")
    )
    assert result.magnitude == pytest.approx(34.2, rel=1e-2)
    assert result.units == u.millimeter


def test_distance_belt_edge_deepest_level_of_trough_invalid_unit():
    with pytest.raises(ValueError, match="Invalid unit"):
        distance_belt_edge_deepest_level_of_trough(
            u.Quantity(100, "millimeter"), u.Quantity(20, "degrees"), "invalid_unit"
        )


def test_distance_belt_edge_deepest_level_of_trough_conversion_error():
    with pytest.raises(ValueError, match="Error in converting values"):
        distance_belt_edge_deepest_level_of_trough(
            "invalid_quantity", u.Quantity(20, "degrees")
        )
