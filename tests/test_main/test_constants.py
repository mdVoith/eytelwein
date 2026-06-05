from math import isclose
from pathlib import Path
import re
import tomllib


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


def test_version_is_synced_between_pyproject_and_runtime():
    """Guard against release-version drift between metadata and __version__."""
    repo_root = Path(__file__).resolve().parents[2]
    pyproject_path = repo_root / "pyproject.toml"
    init_path = repo_root / "src" / "eytelwein" / "__init__.py"

    pyproject_version = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))["project"][
        "version"
    ]

    init_content = init_path.read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', init_content, re.MULTILINE)
    assert match is not None, "Could not find __version__ string literal in src/eytelwein/__init__.py"
    runtime_version = match.group(1)

    assert runtime_version == pyproject_version
