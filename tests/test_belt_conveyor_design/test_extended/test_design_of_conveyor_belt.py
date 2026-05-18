import pytest
from pint import Quantity
from eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt import (
    belt_weight_per_square_meter,
    line_load_belt,
    line_load_belt_from_belt_weight_per_square_meter,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


def test_belt_weight_per_square_meter_basic(monkeypatch):
    # Patch the private implementation to a known calculation for test
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._belt_weight_per_square_meter",
        lambda tmw, tct, bct, rd: tmw + (tct + bct) * rd,
    )
    tension_member_weight = 8.67 * u.kilogram / u.meter**2
    top_cover_thickness = 6 * u.millimeter
    bottom_cover_thickness = 4 * u.millimeter
    rubber_density = 1100 * u.kilogram / u.meter**3

    # (2+1)mm = 0.003m, so added rubber = 0.003*1200 = 3.6kg/m2, total = 8.6
    result = belt_weight_per_square_meter(
        tension_member_weight,
        top_cover_thickness,
        bottom_cover_thickness,
        rubber_density,
        unit="kilogram/meter**2",
        precision=2,
    )
    assert isinstance(result, Quantity)
    assert result.magnitude == 19.67
    assert result.units == u.kilogram / u.meter**2


def test_belt_weight_per_square_meter_unit_conversion(monkeypatch):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._belt_weight_per_square_meter",
        lambda tmw, tct, bct, rd: tmw + (tct + bct) * rd,
    )
    tension_member_weight = 5000 * u.gram / u.meter**2
    top_cover_thickness = 0.2 * u.centimeter
    bottom_cover_thickness = 10 * u.millimeter
    rubber_density = 1.2 * u.gram / u.centimeter**3

    # 0.2cm + 1cm = 1.2cm = 0.012m, 1.2g/cm3 = 1200kg/m3
    # (0.012*1200) + 5 = 14.4 + 5 = 19.4
    result = belt_weight_per_square_meter(
        tension_member_weight,
        top_cover_thickness,
        bottom_cover_thickness,
        rubber_density,
        unit="kg/m^2",
        precision=1,
    )
    assert pytest.approx(result.magnitude, 0.1) == 19.4
    assert result.units == u.kilogram / u.meter**2


def test_belt_weight_per_square_meter_invalid_unit(monkeypatch):
    tension_member_weight = 5 * u.kilogram / u.meter**2
    top_cover_thickness = 2 * u.millimeter
    bottom_cover_thickness = 1 * u.millimeter
    rubber_density = 1200 * u.kilogram / u.meter**3
    with pytest.raises(ValueError, match="Invalid unit"):
        belt_weight_per_square_meter(
            tension_member_weight,
            top_cover_thickness,
            bottom_cover_thickness,
            rubber_density,
            unit="not_a_unit",
        )


@pytest.mark.parametrize(
    "tmw, tct, bct, rd, err_msg",
    [
        (
            -1 * u.kilogram / u.meter**2,
            2 * u.millimeter,
            1 * u.millimeter,
            1200 * u.kilogram / u.meter**3,
            "Tension member weight cannot be negative",
        ),
        (
            5 * u.kilogram / u.meter**2,
            -2 * u.millimeter,
            1 * u.millimeter,
            1200 * u.kilogram / u.meter**3,
            "Top cover thickness cannot be negative",
        ),
        (
            5 * u.kilogram / u.meter**2,
            2 * u.millimeter,
            -1 * u.millimeter,
            1200 * u.kilogram / u.meter**3,
            "Bottom cover thickness cannot be negative",
        ),
        (
            5 * u.kilogram / u.meter**2,
            2 * u.millimeter,
            1 * u.millimeter,
            0 * u.kilogram / u.meter**3,
            "Rubber density must be positive",
        ),
        (
            5 * u.kilogram / u.meter**2,
            2 * u.millimeter,
            1 * u.millimeter,
            -10 * u.kilogram / u.meter**3,
            "Rubber density must be positive",
        ),
    ],
)
def test_belt_weight_per_square_meter_invalid_values(
    monkeypatch, tmw, tct, bct, rd, err_msg
):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._belt_weight_per_square_meter",
        lambda tmw, tct, bct, rd: 0,
    )
    with pytest.raises(ValueError, match=err_msg):
        belt_weight_per_square_meter(tmw, tct, bct, rd)


def test_belt_weight_per_square_meter_precision(monkeypatch):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._belt_weight_per_square_meter",
        lambda tmw, tct, bct, rd: 8.123456,
    )
    tension_member_weight = 5 * u.kilogram / u.meter**2
    top_cover_thickness = 2 * u.millimeter
    bottom_cover_thickness = 1 * u.millimeter
    rubber_density = 1200 * u.kilogram / u.meter**3

    result = belt_weight_per_square_meter(
        tension_member_weight,
        top_cover_thickness,
        bottom_cover_thickness,
        rubber_density,
        precision=3,
    )
    assert result.magnitude == 8.123


def test_belt_weight_per_square_meter_no_precision(monkeypatch):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._belt_weight_per_square_meter",
        lambda tmw, tct, bct, rd: 8.123456,
    )
    tension_member_weight = 5 * u.kilogram / u.meter**2
    top_cover_thickness = 2 * u.millimeter
    bottom_cover_thickness = 1 * u.millimeter
    rubber_density = 1200 * u.kilogram / u.meter**3

    result = belt_weight_per_square_meter(
        tension_member_weight,
        top_cover_thickness,
        bottom_cover_thickness,
        rubber_density,
        precision=None,
    )
    assert pytest.approx(result.magnitude, 1e-6) == 8.123456


def test_line_load_belt_basic(monkeypatch):
    # Patch the private implementation to a known calculation for test
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._line_load_belt",
        lambda tmw, bw, tct, bct, rd: (tmw + (tct + bct) * rd) * bw,
    )
    tension_member_weight = 8.67 * u.kilogram / u.meter**2
    belt_width = 1.25 * u.meter
    top_cover_thickness = 6 * u.millimeter
    bottom_cover_thickness = 4 * u.millimeter
    rubber_density = 1100 * u.kilogram / u.meter**3

    # (0.006+0.004)*1100 = 11kg/m2, total per m2 = 19.67, line load = 19.67*1.25 = 24.59
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
    assert pytest.approx(result.magnitude, 0.01) == 24.58
    assert result.magnitude == 24.59
    assert result.units == u.kilogram / u.meter


def test_line_load_belt_unit_conversion(monkeypatch):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._line_load_belt",
        lambda tmw, bw, tct, bct, rd: (tmw + (tct + bct) * rd) * bw,
    )
    tension_member_weight = 5000 * u.gram / u.meter**2
    belt_width = 120 * u.centimeter
    top_cover_thickness = 0.2 * u.centimeter
    bottom_cover_thickness = 10 * u.millimeter
    rubber_density = 1.2 * u.gram / u.centimeter**3

    # (0.2+1.0)cm = 1.2cm = 0.012m, 1.2g/cm3 = 1200kg/m3, 5kg/m2
    # (0.012*1200)+5 = 14.4+5=19.4kg/m2, width=1.2m, line load=19.4*1.2=23.28
    result = line_load_belt(
        tension_member_weight,
        belt_width,
        top_cover_thickness,
        bottom_cover_thickness,
        rubber_density,
        unit="kg/m",
        precision=2,
    )
    assert pytest.approx(result.magnitude, 0.01) == 23.28
    assert result.units == u.kilogram / u.meter


def test_line_load_belt_invalid_unit(monkeypatch):
    tension_member_weight = 5 * u.kilogram / u.meter**2
    belt_width = 1 * u.meter
    top_cover_thickness = 2 * u.millimeter
    bottom_cover_thickness = 1 * u.millimeter
    rubber_density = 1200 * u.kilogram / u.meter**3
    with pytest.raises(ValueError, match="Invalid unit"):
        line_load_belt(
            tension_member_weight,
            belt_width,
            top_cover_thickness,
            bottom_cover_thickness,
            rubber_density,
            unit="not_a_unit",
        )


@pytest.mark.parametrize(
    "tmw, bw, tct, bct, rd, err_msg",
    [
        (
            -1 * u.kilogram / u.meter**2,
            1 * u.meter,
            2 * u.millimeter,
            1 * u.millimeter,
            1200 * u.kilogram / u.meter**3,
            "Tension member weight cannot be negative",
        ),
        (
            5 * u.kilogram / u.meter**2,
            0 * u.meter,
            2 * u.millimeter,
            1 * u.millimeter,
            1200 * u.kilogram / u.meter**3,
            "Belt width must be positive",
        ),
        (
            5 * u.kilogram / u.meter**2,
            -1 * u.meter,
            2 * u.millimeter,
            1 * u.millimeter,
            1200 * u.kilogram / u.meter**3,
            "Belt width must be positive",
        ),
        (
            5 * u.kilogram / u.meter**2,
            1 * u.meter,
            -2 * u.millimeter,
            1 * u.millimeter,
            1200 * u.kilogram / u.meter**3,
            "Top cover thickness cannot be negative",
        ),
        (
            5 * u.kilogram / u.meter**2,
            1 * u.meter,
            2 * u.millimeter,
            -1 * u.millimeter,
            1200 * u.kilogram / u.meter**3,
            "Bottom cover thickness cannot be negative",
        ),
        (
            5 * u.kilogram / u.meter**2,
            1 * u.meter,
            2 * u.millimeter,
            1 * u.millimeter,
            0 * u.kilogram / u.meter**3,
            "Rubber density must be positive",
        ),
        (
            5 * u.kilogram / u.meter**2,
            1 * u.meter,
            2 * u.millimeter,
            1 * u.millimeter,
            -10 * u.kilogram / u.meter**3,
            "Rubber density must be positive",
        ),
    ],
)
def test_line_load_belt_invalid_values(monkeypatch, tmw, bw, tct, bct, rd, err_msg):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._line_load_belt",
        lambda tmw, bw, tct, bct, rd: 0,
    )
    with pytest.raises(ValueError, match=err_msg):
        line_load_belt(tmw, bw, tct, bct, rd)


def test_line_load_belt_precision(monkeypatch):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._line_load_belt",
        lambda tmw, bw, tct, bct, rd: 8.123456,
    )
    tension_member_weight = 5 * u.kilogram / u.meter**2
    belt_width = 1 * u.meter
    top_cover_thickness = 2 * u.millimeter
    bottom_cover_thickness = 1 * u.millimeter
    rubber_density = 1200 * u.kilogram / u.meter**3

    result = line_load_belt(
        tension_member_weight,
        belt_width,
        top_cover_thickness,
        bottom_cover_thickness,
        rubber_density,
        precision=3,
    )
    assert result.magnitude == 8.123


def test_line_load_belt_no_precision(monkeypatch):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._line_load_belt",
        lambda tmw, bw, tct, bct, rd: 8.123456,
    )
    tension_member_weight = 5 * u.kilogram / u.meter**2
    belt_width = 1 * u.meter
    top_cover_thickness = 2 * u.millimeter
    bottom_cover_thickness = 1 * u.millimeter
    rubber_density = 1200 * u.kilogram / u.meter**3

    result = line_load_belt(
        tension_member_weight,
        belt_width,
        top_cover_thickness,
        bottom_cover_thickness,
        rubber_density,
        precision=None,
    )
    assert pytest.approx(result.magnitude, 1e-6) == 8.123456


def test_line_load_belt_from_belt_weight_per_square_meter_basic(monkeypatch):
    # Patch the private implementation to a known calculation for test
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._line_load_belt_from_belt_weight_per_square_meter",
        lambda bwpsm, bw: bwpsm * bw,
    )
    belt_weight_per_square_meter = 19.67 * u.kilogram / u.meter**2
    belt_width = 1.25 * u.meter
    result = line_load_belt_from_belt_weight_per_square_meter(
        belt_weight_per_square_meter,
        belt_width,
        unit="kilogram/meter",
        precision=2,
    )
    assert isinstance(result, Quantity)
    assert result.magnitude == 24.59
    assert pytest.approx(result.magnitude, 0.01) == 24.58
    assert result.units == u.kilogram / u.meter


def test_line_load_belt_from_belt_weight_per_square_meter_unit_conversion(monkeypatch):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._line_load_belt_from_belt_weight_per_square_meter",
        lambda bwpsm, bw: bwpsm * bw,
    )
    belt_weight_per_square_meter = 2000 * u.gram / u.meter**2
    belt_width = 120 * u.centimeter
    # 2000 g/m2 = 2 kg/m2, 120 cm = 1.2 m, so 2*1.2 = 2.4 kg/m
    result = line_load_belt_from_belt_weight_per_square_meter(
        belt_weight_per_square_meter,
        belt_width,
        unit="kg/m",
        precision=3,
    )
    assert pytest.approx(result.magnitude, 1e-6) == 2.4
    assert result.units == u.kilogram / u.meter


def test_line_load_belt_from_belt_weight_per_square_meter_invalid_unit(monkeypatch):
    belt_weight_per_square_meter = 5 * u.kilogram / u.meter**2
    belt_width = 1 * u.meter
    with pytest.raises(ValueError, match="Invalid unit"):
        line_load_belt_from_belt_weight_per_square_meter(
            belt_weight_per_square_meter,
            belt_width,
            unit="not_a_unit",
        )


@pytest.mark.parametrize(
    "bwpsm, bw, err_msg",
    [
        (
            -1 * u.kilogram / u.meter**2,
            1 * u.meter,
            "Belt weight per square meter cannot be negative",
        ),
        (
            5 * u.kilogram / u.meter**2,
            0 * u.meter,
            "Belt width must be positive",
        ),
        (
            5 * u.kilogram / u.meter**2,
            -1 * u.meter,
            "Belt width must be positive",
        ),
    ],
)
def test_line_load_belt_from_belt_weight_per_square_meter_invalid_values(
    monkeypatch, bwpsm, bw, err_msg
):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._line_load_belt_from_belt_weight_per_square_meter",
        lambda bwpsm, bw: 0,
    )
    with pytest.raises(ValueError, match=err_msg):
        line_load_belt_from_belt_weight_per_square_meter(bwpsm, bw)


def test_line_load_belt_from_belt_weight_per_square_meter_precision(monkeypatch):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._line_load_belt_from_belt_weight_per_square_meter",
        lambda bwpsm, bw: 8.123456,
    )
    belt_weight_per_square_meter = 5 * u.kilogram / u.meter**2
    belt_width = 1 * u.meter
    result = line_load_belt_from_belt_weight_per_square_meter(
        belt_weight_per_square_meter,
        belt_width,
        precision=3,
    )
    assert result.magnitude == 8.123


def test_line_load_belt_from_belt_weight_per_square_meter_no_precision(monkeypatch):
    monkeypatch.setattr(
        "eytelwein.belt_conveyor_design.extended.design_of_conveyor_belt._line_load_belt_from_belt_weight_per_square_meter",
        lambda bwpsm, bw: 8.123456,
    )
    belt_weight_per_square_meter = 5 * u.kilogram / u.meter**2
    belt_width = 1 * u.meter
    result = line_load_belt_from_belt_weight_per_square_meter(
        belt_weight_per_square_meter,
        belt_width,
        precision=None,
    )
    assert pytest.approx(result.magnitude, 1e-6) == 8.123456
