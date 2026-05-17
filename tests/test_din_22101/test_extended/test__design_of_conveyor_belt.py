import pytest
from eytelwein.din_22101.extended._design_of_conveyor_belt import _line_load_belt
from eytelwein.din_22101.extended._design_of_conveyor_belt import (
    _line_load_belt_from_belt_weight_per_square_meter,
)
from eytelwein.din_22101.extended._design_of_conveyor_belt import (
    _belt_weight_per_square_meter,
)


def test_belt_weight_per_square_meter_basic():
    # Example: tension member 5 kg/m², covers 0.01 m + 0.005 m, density 1200 kg/m³
    result = _belt_weight_per_square_meter(
        tension_member_weight=8.67,
        top_cover_thickness=0.006,
        bottom_cover_thickness=0.004,
        rubber_density=1100.0,
    )
    expected = 19.67
    assert pytest.approx(result, rel=1e-9) == expected


def test_belt_weight_per_square_meter_zero_covers():
    # No covers, only tension member
    result = _belt_weight_per_square_meter(
        tension_member_weight=7.0,
        top_cover_thickness=0.0,
        bottom_cover_thickness=0.0,
        rubber_density=1200.0,
    )
    assert result == 7.0


def test_belt_weight_per_square_meter_zero_tension_member():
    # No tension member, only covers
    result = _belt_weight_per_square_meter(
        tension_member_weight=0.0,
        top_cover_thickness=0.01,
        bottom_cover_thickness=0.01,
        rubber_density=1000.0,
    )
    expected = (0.01 + 0.01) * 1000.0  # 0.02*1000 = 20
    assert pytest.approx(result, rel=1e-9) == expected


def test_belt_weight_per_square_meter_all_zeros():
    # All zero inputs
    result = _belt_weight_per_square_meter(
        tension_member_weight=0.0,
        top_cover_thickness=0.0,
        bottom_cover_thickness=0.0,
        rubber_density=0.0,
    )
    assert result == 0.0


def test_belt_weight_per_square_meter_negative_inputs():
    # Negative values should be handled mathematically (not physically meaningful)
    result = _belt_weight_per_square_meter(
        tension_member_weight=-2.0,
        top_cover_thickness=-0.01,
        bottom_cover_thickness=-0.01,
        rubber_density=1000.0,
    )
    expected = -2.0 + (-0.01 + -0.01) * 1000.0  # -2 + (-0.02)*1000 = -2 - 20 = -22
    assert pytest.approx(result, rel=1e-9) == expected


def test_line_load_belt_basic():
    # Example: tension member 8.67 kg/m², covers 0.006 m + 0.004 m, density 1100 kg/m³, width 1.0 m
    result = _line_load_belt(
        tension_member_weight=8.67,
        belt_width=1.25,
        top_cover_thickness=0.006,
        bottom_cover_thickness=0.004,
        rubber_density=1100.0,
    )
    expected = (
        8.67 + (0.006 + 0.004) * 1100.0
    ) * 1.25  # (8.67 + 11) * 1.25 = 19.67 * 1.25 = 24.5875
    assert pytest.approx(result, rel=1e-9) == expected


def test_line_load_belt_zero_width():
    # Zero width should result in zero line load
    result = _line_load_belt(
        tension_member_weight=10.0,
        belt_width=0.0,
        top_cover_thickness=0.01,
        bottom_cover_thickness=0.01,
        rubber_density=1200.0,
    )
    assert result == 0.0


def test_line_load_belt_zero_covers():
    # No covers, only tension member
    result = _line_load_belt(
        tension_member_weight=7.0,
        belt_width=0.8,
        top_cover_thickness=0.0,
        bottom_cover_thickness=0.0,
        rubber_density=1200.0,
    )
    expected = 7.0 * 0.8
    assert pytest.approx(result, rel=1e-9) == expected


def test_line_load_belt_zero_tension_member():
    # No tension member, only covers
    result = _line_load_belt(
        tension_member_weight=0.0,
        belt_width=1.2,
        top_cover_thickness=0.01,
        bottom_cover_thickness=0.01,
        rubber_density=1000.0,
    )
    expected = ((0.01 + 0.01) * 1000.0) * 1.2  # 20 * 1.2 = 24
    assert pytest.approx(result, rel=1e-9) == expected


def test_line_load_belt_all_zeros():
    # All zero inputs
    result = _line_load_belt(
        tension_member_weight=0.0,
        belt_width=0.0,
        top_cover_thickness=0.0,
        bottom_cover_thickness=0.0,
        rubber_density=0.0,
    )
    assert result == 0.0


def test_line_load_belt_negative_inputs():
    # Negative values should be handled mathematically (not physically meaningful)
    result = _line_load_belt(
        tension_member_weight=-2.0,
        belt_width=-1.5,
        top_cover_thickness=-0.01,
        bottom_cover_thickness=-0.01,
        rubber_density=1000.0,
    )
    expected = (
        -2.0 + (-0.01 + -0.01) * 1000.0
    ) * -1.5  # (-2 - 20) * -1.5 = -22 * -1.5 = 33
    assert pytest.approx(result, rel=1e-9) == expected


def test_line_load_belt_from_belt_weight_per_square_meter_basic():
    # Example: 19.67 kg/m², 1.25 m width
    result = _line_load_belt_from_belt_weight_per_square_meter(19.67, 1.25)
    expected = 19.67 * 1.25  # 24.5875
    assert pytest.approx(result, rel=1e-9) == expected


def test_line_load_belt_from_belt_weight_per_square_meter_zero_weight():
    # Zero weight per square meter
    result = _line_load_belt_from_belt_weight_per_square_meter(0.0, 2.0)
    assert result == 0.0


def test_line_load_belt_from_belt_weight_per_square_meter_zero_width():
    # Zero width
    result = _line_load_belt_from_belt_weight_per_square_meter(15.0, 0.0)
    assert result == 0.0


def test_line_load_belt_from_belt_weight_per_square_meter_all_zeros():
    # Both inputs zero
    result = _line_load_belt_from_belt_weight_per_square_meter(0.0, 0.0)
    assert result == 0.0


def test_line_load_belt_from_belt_weight_per_square_meter_negative_inputs():
    # Negative values should be handled mathematically
    result = _line_load_belt_from_belt_weight_per_square_meter(-10.0, -2.0)
    expected = -10.0 * -2.0  # 20.0
    assert pytest.approx(result, rel=1e-9) == expected


def test_line_load_belt_from_belt_weight_per_square_meter_negative_weight():
    # Negative weight per square meter, positive width
    result = _line_load_belt_from_belt_weight_per_square_meter(-5.0, 3.0)
    expected = -5.0 * 3.0  # -15.0
    assert pytest.approx(result, rel=1e-9) == expected


def test_line_load_belt_from_belt_weight_per_square_meter_negative_width():
    # Positive weight per square meter, negative width
    result = _line_load_belt_from_belt_weight_per_square_meter(8.0, -1.5)
    expected = 8.0 * -1.5  # -12.0
    assert pytest.approx(result, rel=1e-9) == expected
