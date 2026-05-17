import pytest
from math import isclose


def test_constants_defined():
    """Test that all constants are defined."""
    from eytelwein.main.constants import (
        STANDARD_GRAVITY,
        PI,
        STANDARD_GRAVITY_VALUE,
        PI_VALUE,
    )

    assert STANDARD_GRAVITY is not None
    assert PI is not None
    assert STANDARD_GRAVITY_VALUE is not None
    assert PI_VALUE is not None


def test_constants_values():
    """Test that constants have expected values."""
    from eytelwein.main.constants import (
        STANDARD_GRAVITY,
        PI,
        STANDARD_GRAVITY_VALUE,
        PI_VALUE,
    )

    assert isclose(STANDARD_GRAVITY.magnitude, 9.80665, rel_tol=1e-10)
    assert isclose(PI, 3.141592653589793, rel_tol=1e-10)
    assert STANDARD_GRAVITY_VALUE == STANDARD_GRAVITY.magnitude
    assert PI_VALUE == PI


def test_constants_units():
    """Test that constants have correct units."""
    from eytelwein.main.constants import STANDARD_GRAVITY, PI

    assert STANDARD_GRAVITY.check("[length]/[time]^2")
    assert isinstance(PI, float)


def test_physical_properties():
    """Test fundamental physical properties of constants."""
    from eytelwein.main.constants import STANDARD_GRAVITY, PI

    assert STANDARD_GRAVITY > 0
    assert PI > 3 and PI < 4


def test_gravity_regression():
    """Ensure STANDARD_GRAVITY hasn't changed since last release."""
    from eytelwein.main.constants import STANDARD_GRAVITY_VALUE

    EXPECTED_GRAVITY = 9.80665
    assert STANDARD_GRAVITY_VALUE == EXPECTED_GRAVITY
