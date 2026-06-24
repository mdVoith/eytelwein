import pytest

from eytelwein.belt_conveyor_design.core._design_of_conveyor_belt import (
    _belt_safety_factor_fromsplice_strength_and_belt_tension,
    _splice_strength_from_belt_safety_factor_and_belt_tension,
    _belt_tension_fromsplice_strength_and_belt_safety_factor,
)


def test_belt_safety_factor_fromsplice_strength_and_belt_tension_basic():
    result = _belt_safety_factor_fromsplice_strength_and_belt_tension(
        splice_strength_n_per_mm=2000.0,
        belt_tension_n_per_mm=250.0,
    )
    assert result == pytest.approx(8.0)


def test_splice_strength_from_belt_safety_factor_and_belt_tension_basic():
    result = _splice_strength_from_belt_safety_factor_and_belt_tension(
        belt_safety_factor=8.0,
        belt_tension_n_per_mm=250.0,
    )
    assert result == pytest.approx(2000.0)


def test_belt_tension_fromsplice_strength_and_belt_safety_factor_basic():
    result = _belt_tension_fromsplice_strength_and_belt_safety_factor(
        splice_strength_n_per_mm=2000.0,
        belt_safety_factor=8.0,
    )
    assert result == pytest.approx(250.0)


def test_belt_safety_factor_fromsplice_strength_and_belt_tension_rejects_zero_tension():
    with pytest.raises(ValueError, match="belt_tension_n_per_mm must be positive"):
        _belt_safety_factor_fromsplice_strength_and_belt_tension(
            splice_strength_n_per_mm=2000.0,
            belt_tension_n_per_mm=0.0,
        )


def test_belt_tension_fromsplice_strength_and_belt_safety_factor_rejects_zero_safety_factor():
    with pytest.raises(ValueError, match="belt_safety_factor must be positive"):
        _belt_tension_fromsplice_strength_and_belt_safety_factor(
            splice_strength_n_per_mm=2000.0,
            belt_safety_factor=0.0,
        )
