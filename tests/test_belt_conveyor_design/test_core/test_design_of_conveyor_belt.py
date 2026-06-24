import pytest
from pint import Quantity

from eytelwein.belt_conveyor_design.core.design_of_conveyor_belt import (
    belt_safety_factor_fromsplice_strength_and_belt_tension,
    splice_strength_from_belt_safety_factor_and_belt_tension,
    belt_tension_fromsplice_strength_and_belt_safety_factor,
)
from eytelwein.main.units import get_unit_registry

u = get_unit_registry()


def test_belt_safety_factor_fromsplice_strength_and_belt_tension_basic():
    result = belt_safety_factor_fromsplice_strength_and_belt_tension(
        splice_strength=2000.0 * u.newton / u.millimeter,
        belt_tension=250.0 * u.newton / u.millimeter,
    )

    assert isinstance(result, Quantity)
    assert result.magnitude == pytest.approx(8.0)
    assert result.units == u.dimensionless


def test_belt_safety_factor_fromsplice_strength_and_belt_tension_unit_conversion():
    # 2 kN/mm / 0.25 kN/mm = 8
    result = belt_safety_factor_fromsplice_strength_and_belt_tension(
        splice_strength=2.0 * u.kilonewton / u.millimeter,
        belt_tension=0.25 * u.kilonewton / u.millimeter,
    )

    assert result.magnitude == pytest.approx(8.0)
    assert result.units == u.dimensionless


def test_splice_strength_from_belt_safety_factor_and_belt_tension_basic():
    result = splice_strength_from_belt_safety_factor_and_belt_tension(
        belt_safety_factor=8.0 * u.dimensionless,
        belt_tension=250.0 * u.newton / u.millimeter,
    )

    assert isinstance(result, Quantity)
    assert result.magnitude == pytest.approx(2000.0)
    assert result.units == u.newton / u.millimeter


def test_belt_tension_fromsplice_strength_and_belt_safety_factor_basic():
    result = belt_tension_fromsplice_strength_and_belt_safety_factor(
        splice_strength=2000.0 * u.newton / u.millimeter,
        belt_safety_factor=8.0 * u.dimensionless,
    )

    assert isinstance(result, Quantity)
    assert result.magnitude == pytest.approx(250.0)
    assert result.units == u.newton / u.millimeter


def test_safety_factor_inverse_round_trip():
    splice_strength = 2000.0 * u.newton / u.millimeter
    belt_tension = 250.0 * u.newton / u.millimeter

    safety_factor = belt_safety_factor_fromsplice_strength_and_belt_tension(
        splice_strength=splice_strength,
        belt_tension=belt_tension,
    )
    recovered_splice_strength = splice_strength_from_belt_safety_factor_and_belt_tension(
        belt_safety_factor=safety_factor,
        belt_tension=belt_tension,
    )
    recovered_belt_tension = belt_tension_fromsplice_strength_and_belt_safety_factor(
        splice_strength=splice_strength,
        belt_safety_factor=safety_factor,
    )

    assert recovered_splice_strength.to(u.newton / u.millimeter).magnitude == pytest.approx(
        splice_strength.to(u.newton / u.millimeter).magnitude
    )
    assert recovered_belt_tension.to(u.newton / u.millimeter).magnitude == pytest.approx(
        belt_tension.to(u.newton / u.millimeter).magnitude
    )


def test_belt_safety_factor_with_output_percent_unit():
    result = belt_safety_factor_fromsplice_strength_and_belt_tension(
        splice_strength=2000.0 * u.newton / u.millimeter,
        belt_tension=250.0 * u.newton / u.millimeter,
        unit="percent",
    )

    assert result.magnitude == pytest.approx(800.0)
    assert result.units == u.percent


def test_belt_safety_factor_rejects_nonpositive_inputs():
    with pytest.raises(ValueError, match="splice_strength must be positive"):
        belt_safety_factor_fromsplice_strength_and_belt_tension(
            splice_strength=0.0 * u.newton / u.millimeter,
            belt_tension=250.0 * u.newton / u.millimeter,
        )

    with pytest.raises(ValueError, match="belt_tension must be positive"):
        belt_safety_factor_fromsplice_strength_and_belt_tension(
            splice_strength=2000.0 * u.newton / u.millimeter,
            belt_tension=0.0 * u.newton / u.millimeter,
        )


def test_splice_strength_rejects_nonpositive_inputs():
    with pytest.raises(ValueError, match="belt_safety_factor must be positive"):
        splice_strength_from_belt_safety_factor_and_belt_tension(
            belt_safety_factor=0.0 * u.dimensionless,
            belt_tension=250.0 * u.newton / u.millimeter,
        )

    with pytest.raises(ValueError, match="belt_tension must be positive"):
        splice_strength_from_belt_safety_factor_and_belt_tension(
            belt_safety_factor=8.0 * u.dimensionless,
            belt_tension=0.0 * u.newton / u.millimeter,
        )


def test_belt_tension_rejects_nonpositive_inputs():
    with pytest.raises(ValueError, match="splice_strength must be positive"):
        belt_tension_fromsplice_strength_and_belt_safety_factor(
            splice_strength=0.0 * u.newton / u.millimeter,
            belt_safety_factor=8.0 * u.dimensionless,
        )

    with pytest.raises(ValueError, match="belt_safety_factor must be positive"):
        belt_tension_fromsplice_strength_and_belt_safety_factor(
            splice_strength=2000.0 * u.newton / u.millimeter,
            belt_safety_factor=0.0 * u.dimensionless,
        )


def test_invalid_output_unit_raises_value_error():
    with pytest.raises(ValueError, match="Invalid unit"):
        belt_safety_factor_fromsplice_strength_and_belt_tension(
            splice_strength=2000.0 * u.newton / u.millimeter,
            belt_tension=250.0 * u.newton / u.millimeter,
            unit="invalid_unit",
        )


def test_incompatible_output_unit_raises_value_error():
    with pytest.raises(ValueError, match="Error in attaching unit"):
        splice_strength_from_belt_safety_factor_and_belt_tension(
            belt_safety_factor=8.0 * u.dimensionless,
            belt_tension=250.0 * u.newton / u.millimeter,
            unit="meter",
        )


def test_precision_rounding_applies_after_unit_conversion():
    result = belt_safety_factor_fromsplice_strength_and_belt_tension(
        splice_strength=2000.0 * u.newton / u.millimeter,
        belt_tension=333.0 * u.newton / u.millimeter,
        precision=2,
    )

    assert result.magnitude == pytest.approx(6.01)
    assert result.units == u.dimensionless
