import pytest
from eytelwein.din_22101.core.distribution_of_belt_tensions_across_belt_width import (
    compensation_length_at_transition_zone,
    difference_edge_and_center_belt_tensions_steel_cord_belts,
    difference_edge_and_center_belt_tensions_textile_belts,
    distance_belt_edge_to_pulley_surface_level,
    length_of_belt_edge_in_transition_zone,
    local_center_belt_force,
    local_edge_belt_force,
    maximal_allowable_pulley_lift,
    mean_belt_tension_related_to_belt_width,
    local_belt_force_related_to_belt_width,
    minimal_transition_length,
    part_of_belt_lying_on_side_idler,
    reference_length_of_transition_zone_for_steel_cord_belts,
)
from eytelwein.din_22101.constants import CoefficientMinimumTransitionLength

from eytelwein.main.units import get_unit_registry

# Get the unit registry
u = get_unit_registry()


def test_mean_belt_tension_valid_values():
    result = mean_belt_tension_related_to_belt_width(
        1000 * u.kilonewton, 500 * u.millimeter
    )
    assert result.magnitude == 2000.0
    assert result.units == (u.newton / u.millimeter)


def test_mean_belt_tension_zero_belt_width():
    with pytest.raises(ValueError):
        mean_belt_tension_related_to_belt_width(1000 * u.newton, 0 * u.millimeter)


def test_mean_belt_tension_invalid_unit():
    with pytest.raises(ValueError):
        mean_belt_tension_related_to_belt_width(
            1000 * u.newton, 500 * u.millimeter, unit="invalid_unit"
        )


def test_mean_belt_tension_conversion_error():
    with pytest.raises(ValueError):
        mean_belt_tension_related_to_belt_width(1000, 500 * u.millimeter)


def test_mean_belt_tension_negative_belt_width():
    with pytest.raises(ValueError):
        mean_belt_tension_related_to_belt_width(
        1000 * u.kilonewton, -500 * u.millimeter
    )


def test_mean_belt_tension_zero_local_belt_force():
    result = mean_belt_tension_related_to_belt_width(0 * u.newton, 500 * u.millimeter)
    assert result.magnitude == 0.0
    assert result.units == (u.newton / u.millimeter)


def test_local_belt_force_valid_values():
    result = local_belt_force_related_to_belt_width(
        2 * u.newton / u.millimeter, 500 * u.millimeter
    )
    assert result.magnitude == 1.0
    assert result.units == u.kilonewton


def test_local_belt_force_invalid_unit():
    with pytest.raises(ValueError):
        local_belt_force_related_to_belt_width(
            2 * u.newton / u.millimeter, 500 * u.millimeter, unit="invalid_unit"
        )


def test_local_belt_force_invalid_mean_belt_tension():
    with pytest.raises(ValueError):
        local_belt_force_related_to_belt_width("invalid_value", 500 * u.millimeter)


def test_local_belt_force_invalid_belt_width():
    with pytest.raises(ValueError):
        local_belt_force_related_to_belt_width(
            2 * u.newton / u.millimeter, "invalid_value"
        )


def test_local_belt_force_precision():
    result = local_belt_force_related_to_belt_width(
        2 * u.newton / u.millimeter, 500 * u.millimeter, precision=3
    )
    assert result.magnitude == 1.000
    assert result.units == u.kilonewton


def test_local_center_belt_force_valid_values():
    result = local_center_belt_force(
        2 * u.newton / u.millimeter,
        0.5 * u.meter,
        1 * u.meter,
        0.1 * u.newton / u.millimeter,
    )
    assert result.magnitude == pytest.approx(1.95, rel=1e-2)
    assert result.units == (u.newton / u.millimeter)


def test_local_center_belt_force_invalid_unit():
    with pytest.raises(ValueError):
        local_center_belt_force(
            2 * u.newton / u.millimeter,
            0.5 * u.meter,
            1 * u.meter,
            0.1 * u.newton / u.millimeter,
            unit="invalid_unit",
        )


def test_local_center_belt_force_conversion_error():
    with pytest.raises(ValueError):
        local_center_belt_force(
            "invalid_value",
            0.5 * u.meter,
            1 * u.meter,
            0.1 * u.newton / u.millimeter,
        )


def test_local_center_belt_force_zero_belt_width():
    with pytest.raises(ValueError, match="belt_width must be positive"):
        local_center_belt_force(
            2 * u.newton / u.millimeter,
            0.5 * u.meter,
            0 * u.meter,
            0.1 * u.newton / u.millimeter,
        )


def test_local_center_belt_force_negative_belt_width():
    with pytest.raises(ValueError, match="belt_width must be positive"):
        local_center_belt_force(
            2 * u.newton / u.millimeter,
            0.5 * u.meter,
            -1 * u.meter,
            0.1 * u.newton / u.millimeter,
        )


def test_local_center_belt_force_zero_mean_belt_tension():
    with pytest.raises(ValueError):
        local_center_belt_force(
            0 * u.newton / u.millimeter,
            0.5 * u.meter,
            1 * u.meter,
            0.1 * u.newton / u.millimeter,
        )


def test_local_center_belt_force_precision():
    result = local_center_belt_force(
        2 * u.newton / u.millimeter,
        0.5 * u.meter,
        1 * u.meter,
        0.1 * u.newton / u.millimeter,
        precision=3,
    )
    assert result.magnitude == pytest.approx(1.950, rel=1e-3)
    assert result.units == (u.newton / u.millimeter)


def test_part_of_belt_lying_on_side_idler_valid_values():
    result = part_of_belt_lying_on_side_idler(1000 * u.millimeter, 500 * u.millimeter)
    assert result.magnitude == pytest.approx(250.0, rel=1e-2)
    assert result.units == u.millimeter


def test_part_of_belt_lying_on_side_idler_invalid_unit():
    with pytest.raises(ValueError):
        part_of_belt_lying_on_side_idler(
            1000 * u.millimeter, 500 * u.millimeter, unit="invalid_unit"
        )


def test_part_of_belt_lying_on_side_idler_conversion_error():
    with pytest.raises(ValueError):
        part_of_belt_lying_on_side_idler("invalid_value", 500 * u.millimeter)


def test_part_of_belt_lying_on_side_idler_zero_belt_width():
    with pytest.raises(ValueError, match="belt_width must be positive"):
        part_of_belt_lying_on_side_idler(0 * u.millimeter, 500 * u.millimeter)


def test_part_of_belt_lying_on_side_idler_negative_belt_width():
    with pytest.raises(ValueError):
        part_of_belt_lying_on_side_idler(-1000 * u.millimeter, 500 * u.millimeter)


def test_part_of_belt_lying_on_side_idler_zero_length_center_roller():
    result = part_of_belt_lying_on_side_idler(1000 * u.millimeter, 0 * u.millimeter)
    assert result.magnitude == pytest.approx(500.0, rel=1e-2)
    assert result.units == u.millimeter


def test_part_of_belt_lying_on_side_idler_precision():
    result = part_of_belt_lying_on_side_idler(
        1000 * u.millimeter, 500 * u.millimeter, precision=3
    )
    assert result.magnitude == pytest.approx(250.000, rel=1e-3)
    assert result.units == u.millimeter


def test_local_edge_belt_force_valid_values():
    result = local_edge_belt_force(
        2 * u.newton / u.millimeter, 0.5 * u.newton / u.millimeter
    )
    assert result.magnitude == pytest.approx(2.5, rel=1e-2)
    assert result.units == (u.newton / u.millimeter)


def test_local_edge_belt_force_invalid_unit():
    with pytest.raises(ValueError):
        local_edge_belt_force(
            2 * u.newton / u.millimeter,
            0.5 * u.newton / u.millimeter,
            unit="invalid_unit",
        )


def test_local_edge_belt_force_conversion_error():
    with pytest.raises(ValueError):
        local_edge_belt_force("invalid_value", 0.5 * u.newton / u.millimeter)


def test_local_edge_belt_force_zero_difference():
    result = local_edge_belt_force(
        2 * u.newton / u.millimeter, 0 * u.newton / u.millimeter
    )
    assert result.magnitude == pytest.approx(2.0, rel=1e-2)
    assert result.units == (u.newton / u.millimeter)


def test_local_edge_belt_force_negative_difference():
    result = local_edge_belt_force(
        2 * u.newton / u.millimeter, -0.5 * u.newton / u.millimeter
    )
    assert result.magnitude == pytest.approx(1.5, rel=1e-2)
    assert result.units == (u.newton / u.millimeter)


def test_local_edge_belt_force_zero_center_force():
    result = local_edge_belt_force(
        0 * u.newton / u.millimeter, 0.5 * u.newton / u.millimeter
    )
    assert result.magnitude == pytest.approx(0.5, rel=1e-2)
    assert result.units == (u.newton / u.millimeter)


def test_local_edge_belt_force_precision():
    result = local_edge_belt_force(
        2 * u.newton / u.millimeter,
        0.5 * u.newton / u.millimeter,
        precision=3,
    )
    assert result.magnitude == pytest.approx(2.500, rel=1e-3)
    assert result.units == (u.newton / u.millimeter)


def test_minimal_transition_length_valid_values_ST():
    result = minimal_transition_length(
        CoefficientMinimumTransitionLength.ST, 2 * u.meter
    )
    assert result.magnitude == pytest.approx(28.0, rel=1e-2)
    assert result.units == u.meter


def test_minimal_transition_length_valid_values_EP():
    result = minimal_transition_length(
        CoefficientMinimumTransitionLength.EP, 2 * u.meter
    )
    assert result.magnitude == pytest.approx(17.0, rel=1e-2)
    assert result.units == u.meter


def test_minimal_transition_length_invalid_unit():
    with pytest.raises(ValueError):
        minimal_transition_length(1.5, 2 * u.meter, unit="invalid_unit")


def test_minimal_transition_length_conversion_error():
    with pytest.raises(ValueError):
        minimal_transition_length(1.5, "invalid_value")


def test_minimal_transition_length_zero_distance():
    result = minimal_transition_length(
        CoefficientMinimumTransitionLength.ST, 0 * u.meter
    )
    assert result.magnitude == pytest.approx(0.0, rel=1e-2)
    assert result.units == u.meter


def test_minimal_transition_length_negative_distance():
    result = minimal_transition_length(
        CoefficientMinimumTransitionLength.ST, -2 * u.meter
    )
    assert result.magnitude == pytest.approx(-28.0, rel=1e-2)
    assert result.units == u.meter


def test_minimal_transition_length_precision():
    result = minimal_transition_length(
        CoefficientMinimumTransitionLength.ST, 2 * u.meter, precision=3
    )
    assert result.magnitude == pytest.approx(28.000, rel=1e-3)
    assert result.units == u.meter


def test_distance_belt_edge_to_pulley_surface_level_valid_values():
    result = distance_belt_edge_to_pulley_surface_level(
        100 * u.millimeter, 50 * u.millimeter
    )
    assert result.magnitude == pytest.approx(50.0, rel=1e-2)
    assert result.units == u.millimeter


def test_distance_belt_edge_to_pulley_surface_level_invalid_unit():
    with pytest.raises(ValueError):
        distance_belt_edge_to_pulley_surface_level(
            100 * u.millimeter, 50 * u.millimeter, unit="invalid_unit"
        )


def test_distance_belt_edge_to_pulley_surface_level_conversion_error():
    with pytest.raises(ValueError):
        distance_belt_edge_to_pulley_surface_level("invalid_value", 50 * u.millimeter)


def test_distance_belt_edge_to_pulley_surface_level_zero_values():
    result = distance_belt_edge_to_pulley_surface_level(
        0 * u.millimeter, 0 * u.millimeter
    )
    assert result.magnitude == pytest.approx(0.0, rel=1e-2)
    assert result.units == u.millimeter


def test_distance_belt_edge_to_pulley_surface_level_negative_values():
    result = distance_belt_edge_to_pulley_surface_level(
        -100 * u.millimeter, 50 * u.millimeter
    )
    assert result.magnitude == pytest.approx(-150.0, rel=1e-2)
    assert result.units == u.millimeter


def test_distance_belt_edge_to_pulley_surface_level_precision():
    result = distance_belt_edge_to_pulley_surface_level(
        100 * u.millimeter, 50 * u.millimeter, precision=3
    )
    assert result.magnitude == pytest.approx(50.000, rel=1e-3)
    assert result.units == u.millimeter


def test_reference_length_of_transition_zone_valid_values():
    result = reference_length_of_transition_zone_for_steel_cord_belts(
        10 * u.meter, 5 * u.meter
    )
    assert result.magnitude == pytest.approx(15.0, rel=1e-2)
    assert result.units == u.meter


def test_reference_length_of_transition_zone_invalid_unit():
    with pytest.raises(ValueError):
        reference_length_of_transition_zone_for_steel_cord_belts(
            10 * u.meter, 5 * u.meter, unit="invalid_unit"
        )


def test_reference_length_of_transition_zone_conversion_error():
    with pytest.raises(ValueError):
        reference_length_of_transition_zone_for_steel_cord_belts(
            "invalid_value", 5 * u.meter
        )


def test_reference_length_of_transition_zone_zero_values():
    result = reference_length_of_transition_zone_for_steel_cord_belts(
        0 * u.meter, 0 * u.meter
    )
    assert result.magnitude == pytest.approx(0.0, rel=1e-2)
    assert result.units == u.meter


def test_reference_length_of_transition_zone_negative_values():
    result = reference_length_of_transition_zone_for_steel_cord_belts(
        -10 * u.meter, -5 * u.meter
    )
    assert result.magnitude == pytest.approx(-15.0, rel=1e-2)
    assert result.units == u.meter


def test_reference_length_of_transition_zone_precision():
    result = reference_length_of_transition_zone_for_steel_cord_belts(
        10 * u.meter, 5 * u.meter, precision=3
    )
    assert result.magnitude == pytest.approx(15.000, rel=1e-3)
    assert result.units == u.meter


def test_compensation_length_at_transition_zone_valid_values():
    result = compensation_length_at_transition_zone(
        100 * u.millimeter, 50 * u.millimeter, 200 * u.millimeter
    )
    assert result.magnitude == pytest.approx(4.13, rel=1e-2)
    assert result.units == u.meter


def test_compensation_length_at_transition_zone_invalid_unit():
    with pytest.raises(ValueError):
        compensation_length_at_transition_zone(
            100 * u.millimeter,
            50 * u.millimeter,
            200 * u.millimeter,
            unit="invalid_unit",
        )


def test_compensation_length_at_transition_zone_conversion_error():
    with pytest.raises(ValueError):
        compensation_length_at_transition_zone(
            "invalid_value", 50 * u.millimeter, 200 * u.millimeter
        )


def test_compensation_length_at_transition_zone_zero_values():
    with pytest.raises(ZeroDivisionError):
        compensation_length_at_transition_zone(
            0 * u.millimeter, 0 * u.millimeter, 0 * u.millimeter
        )


def test_compensation_length_at_transition_zone_negative_values():
    result = compensation_length_at_transition_zone(
        -100 * u.millimeter, -50 * u.millimeter, -200 * u.millimeter
    )
    assert result.magnitude == pytest.approx(-4.125, rel=1e-2)
    assert result.units == u.meter


def test_compensation_length_at_transition_zone_precision():
    result = compensation_length_at_transition_zone(
        100 * u.millimeter, 50 * u.millimeter, 200 * u.millimeter, precision=3
    )
    assert result.magnitude == 4.125
    assert result.units == u.meter


def test_length_of_belt_edge_in_transition_zone_valid_values():
    result = length_of_belt_edge_in_transition_zone(
        10 * u.meter,
        0.2 * u.meter,
        0.31 * u.meter,
        30 * u.degree,
    )
    assert result.magnitude == pytest.approx(10.000187, rel=1e-6)
    assert result.units == u.meter


def test_length_of_belt_edge_in_transition_zone_invalid_unit():
    with pytest.raises(ValueError):
        length_of_belt_edge_in_transition_zone(
            10 * u.meter,
            2 * u.meter,
            1 * u.meter,
            30 * u.degree,
            unit="invalid_unit",
        )


def test_length_of_belt_edge_in_transition_zone_conversion_error():
    with pytest.raises(ValueError):
        length_of_belt_edge_in_transition_zone(
            "invalid_value",
            2 * u.meter,
            1 * u.meter,
            30 * u.degree,
        )


def test_length_of_belt_edge_in_transition_zone_zero_values():
    result = length_of_belt_edge_in_transition_zone(
        0 * u.meter,
        0 * u.meter,
        0 * u.meter,
        0 * u.degree,
    )
    assert result.magnitude == pytest.approx(0.0, rel=1e-2)
    assert result.units == u.meter


def test_length_of_belt_edge_in_transition_zone_negative_values():
    result = length_of_belt_edge_in_transition_zone(
        -10 * u.meter,
        -0.2 * u.meter,
        -0.31 * u.meter,
        -30 * u.degree,
    )
    assert result.magnitude == pytest.approx(10.006385, rel=1e-6)
    assert result.units == u.meter


def test_length_of_belt_edge_in_transition_zone_precision():
    result = length_of_belt_edge_in_transition_zone(
        10 * u.meter,
        0.2 * u.meter,
        0.31 * u.meter,
        30 * u.degree,
        precision=3,
    )
    assert result.magnitude == pytest.approx(10.0002, rel=1e-4)
    assert result.units == u.meter


def test_difference_edge_and_center_belt_tensions_valid_values():
    result = difference_edge_and_center_belt_tensions_steel_cord_belts(
        10 * u.meter,
        5 * u.meter,
        15 * u.meter,
        200 * u.newton / u.millimeter,
    )
    assert result.magnitude == pytest.approx(66.666667, rel=1e-2)
    assert result.units == (u.newton / u.millimeter)


def test_difference_edge_and_center_belt_tensions_invalid_unit():
    with pytest.raises(ValueError):
        difference_edge_and_center_belt_tensions_steel_cord_belts(
            10 * u.meter,
            5 * u.meter,
            15 * u.meter,
            200 * u.newton / u.millimeter,
            unit="invalid_unit",
        )


def test_difference_edge_and_center_belt_tensions_conversion_error():
    with pytest.raises(ValueError):
        difference_edge_and_center_belt_tensions_steel_cord_belts(
            "invalid_value",
            5 * u.meter,
            15 * u.meter,
            200 * u.newton / u.millimeter,
        )


def test_difference_edge_and_center_belt_tensions_zero_values():
    result = difference_edge_and_center_belt_tensions_steel_cord_belts(
        0 * u.meter,
        0 * u.meter,
        1 * u.meter,
        200 * u.newton / u.millimeter,
    )
    assert result.magnitude == pytest.approx(0.0, rel=1e-2)
    assert result.units == (u.newton / u.millimeter)


def test_difference_edge_and_center_belt_tensions_negative_values():
    result = difference_edge_and_center_belt_tensions_steel_cord_belts(
        -10 * u.meter,
        -5 * u.meter,
        -15 * u.meter,
        -200 * u.newton / u.millimeter,
    )
    assert result.magnitude == pytest.approx(-66.666667, rel=1e-2)
    assert result.units == (u.newton / u.millimeter)


def test_difference_edge_and_center_belt_tensions_precision():
    result = difference_edge_and_center_belt_tensions_steel_cord_belts(
        10 * u.meter,
        5 * u.meter,
        15 * u.meter,
        200 * u.newton / u.millimeter,
        precision=3,
    )
    assert result.magnitude == pytest.approx(66.666667, rel=1e-3)
    assert result.units == (u.newton / u.millimeter)


def test_maximal_allowable_pulley_lift_valid():
    result = maximal_allowable_pulley_lift(u.Quantity(500, "millimeter"))
    assert result.magnitude == pytest.approx(166.67, rel=1e-2)
    assert result.units == u.millimeter


def test_maximal_allowable_pulley_lift_valid_with_different_unit():
    result = maximal_allowable_pulley_lift(u.Quantity(500, "millimeter"), unit="meter")
    assert result.magnitude == pytest.approx(0.17, rel=1e-2)
    assert result.units == u.meter


def test_maximal_allowable_pulley_lift_invalid_unit():
    with pytest.raises(ValueError, match="Invalid unit"):
        maximal_allowable_pulley_lift(
            u.Quantity(500, "millimeter"), unit="invalid_unit"
        )


def test_maximal_allowable_pulley_lift_conversion_error():
    with pytest.raises(ValueError, match="Error in converting values"):
        maximal_allowable_pulley_lift("invalid_quantity")


def test_difference_edge_and_center_belt_tensions_textile_belts_valid():
    result = difference_edge_and_center_belt_tensions_textile_belts(
        u.Quantity(1.2, "meter"),
        u.Quantity(1.0, "meter"),
        u.Quantity(200, "newton / millimeter"),
    )
    assert result.magnitude == pytest.approx(
        40.0, rel=1e-2
    )  # Replace with expected value
    assert result.units == u.Quantity(1, "newton / millimeter").units


def test_difference_edge_and_center_belt_tensions_textile_belts_invalid_unit():
    with pytest.raises(ValueError, match="Invalid unit"):
        difference_edge_and_center_belt_tensions_textile_belts(
            u.Quantity(1.2, "meter"),
            u.Quantity(1.0, "meter"),
            u.Quantity(200, "newton / millimeter"),
            unit="invalid_unit",
        )


def test_difference_edge_and_center_belt_tensions_textile_belts_conversion_error():
    with pytest.raises(ValueError, match="Error in converting values"):
        difference_edge_and_center_belt_tensions_textile_belts(
            "invalid_quantity",
            u.Quantity(1.0, "meter"),
            u.Quantity(200, "newton / millimeter"),
        )
