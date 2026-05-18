"""
Tests for the Eytelwein unit registry module.
"""

import pytest
from eytelwein.main.units import (
    get_unit_registry,
    ensure_quantity,
    convert_to,
    format_quantity,
    Quantity,
)


def test_unit_registry_singleton():
    """Test that get_unit_registry returns the same instance every time."""
    reg1 = get_unit_registry()
    reg2 = get_unit_registry()
    assert reg1 is reg2


def test_quantity_creation():
    """Test creating quantities with the unit registry."""
    ureg = get_unit_registry()
    q = ureg.Quantity(10, "meter")
    assert q.magnitude == 10
    assert q.units == ureg.meter


def test_ensure_quantity():
    """Test the ensure_quantity function."""
    # With a scalar and unit
    q1 = ensure_quantity(5, "m/s")
    assert q1.magnitude == 5
    assert str(q1.units) == "meter / second"

    # With an existing quantity
    ureg = get_unit_registry()
    q2 = ureg.Quantity(10, "kg")
    q2_ensured = ensure_quantity(q2)
    assert q2 is q2_ensured

    # Error case - no unit provided for scalar
    with pytest.raises(ValueError):
        ensure_quantity(5)


def test_convert_to():
    """Test the convert_to function."""
    ureg = get_unit_registry()
    q = ureg.Quantity(1000, "mm")
    converted = convert_to(q, "meter")
    assert converted.magnitude == 1
    assert converted.units == ureg.meter

    # Test with incompatible units
    q = ureg.Quantity(10, "meter")
    with pytest.raises(Exception):
        convert_to(q, "kilogram")


def test_format_quantity():
    """Test the format_quantity function."""
    ureg = get_unit_registry()
    q = ureg.Quantity(1.2345, "meter")

    # Default format
    formatted = format_quantity(q)
    assert formatted == "1.234 meter"

    # Custom format
    formatted = format_quantity(q, ".2f")
    assert formatted == "1.23 meter"


def test_conveyor_specific_units():
    """Test conveyor-specific units defined in the registry."""
    ureg = get_unit_registry()

    # Test ton/tonne
    q1 = ureg.Quantity(1, "ton")
    q2 = ureg.Quantity(1000, "kg")
    assert q1 == q2

    # Test kilonewton
    q1 = ureg.Quantity(1, "kilonewton")
    q2 = ureg.Quantity(1000, "newton")
    assert q1 == q2


def test_quantity_shorthand():
    """Test the Quantity shorthand."""
    q = Quantity(10, "meter")
    assert q.magnitude == 10
    assert str(q.units) == "meter"
