"""
Physical and mathematical constants for the Eytelwein package.

This module provides physical constants with proper units using the Eytelwein
unit registry, ensuring dimensional consistency across calculations.

All physical and mathematical constants are sourced from scipy.constants
for scientific accuracy and future-proofing.

Note on naming conventions:
--------------------------
We use "STANDARD_GRAVITY" rather than just "GRAVITY" for several reasons:
1. Scientific Precision: It specifically refers to the internationally defined constant
   value of 9.80665 m/s², rather than local gravitational acceleration which varies.
2. Physical Reality: Actual gravity varies across Earth's surface - it's stronger at the
   poles (9.83 m/s²), weaker at the equator (9.78 m/s²), and decreases with altitude.
3. Engineering Context: For conveyor belt calculations, the standard
   reference value ensures consistency regardless of location.
4. Naming Convention: This follows established naming patterns in scientific libraries
   and engineering standards.
"""

from eytelwein.main.units import get_unit_registry
from scipy import constants as spc

# Get the Eytelwein unit registry
u = get_unit_registry()

# Physical constants using scipy.constants and registry units
# Use try-except to handle Sphinx import issues gracefully
try:
    STANDARD_GRAVITY = spc.g * u.meter / u.second**2  # Standard gravity (9.80665 m/s²)
except (TypeError, AttributeError):
    # If unit computation fails during documentation generation,
    # create a mock object that will work for Sphinx but won't break tests
    class MockStandardGravity:
        def __init__(self):
            self.magnitude = spc.g

        def __str__(self):
            return f"{spc.g} meter / second ** 2"

        def __repr__(self):
            return f"<MockStandardGravity: {self.magnitude} m/s²>"

        def __mul__(self, other):
            return self.magnitude * other

        def __rmul__(self, other):
            return other * self.magnitude

        def __truediv__(self, other):
            return self.magnitude / other

        def __gt__(self, other):
            return self.magnitude > other

        def __lt__(self, other):
            return self.magnitude < other

        def check(self, dimension_string):
            # Mock the pint quantity check method
            return dimension_string == "[length]/[time]^2"

    STANDARD_GRAVITY = MockStandardGravity()

# Mathematical constants from scipy.constants
PI = spc.pi  # π (3.14159...)

# If raw values are needed for performance-critical code
STANDARD_GRAVITY_VALUE = spc.g  # 9.80665
PI_VALUE = spc.pi  # 3.141592653589793
