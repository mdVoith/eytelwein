# Private-to-Public Function Implementation Guide

## Overview

This guide provides a step-by-step process for implementing public API functions from private functions in the Eytelwein/Convexus codebase.

**Important**: This guide must be used with the comprehensive implementation standards documented in [`eytelwein_implementation_standards.md`](eytelwein_implementation_standards.md), which contains:
- Unit registry patterns
- Array broadcasting standards
- Error message templates
- Function naming guidelines
- Test structure requirements
- Import organization standards

## Table of Contents

1. [Private vs. Public Functions](#private-vs-public-functions)
2. [Implementation Pattern](#implementation-pattern)
3. [Parameter Validation](#parameter-validation)
4. [Complete Example](#complete-example)
5. [Best Practices](#best-practices)

## Private vs. Public Functions

| Private Functions | Public Functions |
|-------------------|------------------|
| Implement pure calculation logic | Handle unit conversion and validation |
| Take raw numeric inputs | Take `Quantity` objects as inputs |
| Perform minimal input validation | Provide comprehensive error handling |
| Named with underscore prefix | Named without underscore prefix |
| Reside in `_module_name.py` files | Reside in `module_name.py` files |
| Include mathematical formulas in docstrings | Include detailed parameter documentation |
| Focused on mathematical correctness | Focus on user-friendly interface |
| No unit handling | Manage unit conversion and precision |

## Implementation Pattern

### Step 1: Create Private Function

1. Define the private function in the appropriate `_module_name.py` file.
2. Use only raw numeric inputs (typically `float` or `int`).
3. Document the expected units in parameter and return value comments.
4. Implement the calculation logic without unit management.
5. Write a clear docstring with mathematical formulas and references.

Example:
```python
def _length_of_material_on_side_roll(
    part_of_belt_lying_on_side_idler: float, belt_edge_distance: float
) -> float:
    """
    Calculates the length of material on the side roll of a conveyor belt.

    Args:
        part_of_belt_lying_on_side_idler (float): The length of the belt segment that lies
            on the side idler (in millimeters).
        belt_edge_distance (float): The distance from the edge of the belt to the point where
            the material ends (in millimeters).

    Returns:
        float: The effective length of material on the side roll (in millimeters).
    """
    return part_of_belt_lying_on_side_idler - belt_edge_distance
```

### Step 2: Create Public Function

1. Import the private function in the corresponding public module.
2. Define the public function with `Quantity` parameters.
3. Add type hints for all parameters and return values.
4. Include unit and precision parameters with appropriate defaults.
5. Write a comprehensive docstring with parameter details and physical meaning.

Example:
```python
def length_of_material_on_side_roll(
    part_of_belt_lying_on_side_idler: Quantity,
    belt_edge_distance: Quantity,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the length of material on the side roll of a conveyor belt.

    This function calculates the effective length of material on the side roll by subtracting
    the belt edge distance from the part of belt lying on the side idler.

    Parameters:
    part_of_belt_lying_on_side_idler (Quantity): The length of the belt segment that lies on the side idler.
    belt_edge_distance (Quantity): The distance from the edge of the belt to the point where the material ends.
    unit (str, optional): The unit for the returned length. Defaults to "millimeter".
    precision (int, optional): The number of decimal places to round the result to. Defaults to 2.

    Returns:
    Quantity: The calculated effective length of material on the side roll with the specified unit.

    Raises:
    ValueError: If there is an error in converting units.
    """
    try:
        # Convert inputs to standard units
        part_on_side_idler_mm = part_of_belt_lying_on_side_idler.to(u.millimeter)
        belt_edge_distance_mm = belt_edge_distance.to(u.millimeter)
    except Exception as e:
        raise ValueError(f"Error in converting length units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call private implementation
    length_mm = (
        _length_of_material_on_side_roll(
            part_on_side_idler_mm.magnitude, belt_edge_distance_mm.magnitude
        )
        * u.millimeter
    )

    # Convert to requested output unit
    result = length_mm.to(pint_unit)

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
```

## Parameter Validation

### Zero-Division Prevention

**Critical Rule**: Always validate denominator parameters BEFORE performing division operations. Use explicit pre-checks, not exception handling.

For comprehensive zero-division handling standards, see the [Zero-Division Error Handling](eytelwein_implementation_standards.md#zero-division-error-handling) section in `eytelwein_implementation_standards.md`.

### Validation Template for Denominators

#### Private Function Pattern
```python
def _calculate_frequency(translatory_speed: float, radius: float) -> float:
    """
    Calculate rotational frequency from translatory speed and radius.

    Parameters
    ----------
    translatory_speed : float
        Speed in m/s.
    radius : float
        Radius in meters.

    Returns
    -------
    float
        Frequency in Hz.

    Raises
    ------
    ValueError
        If radius is not positive.
    """
    # Explicit pre-check BEFORE division
    if radius <= 0:
        raise ValueError(f"radius must be positive, got {radius}")

    # Safe to perform division
    return translatory_speed / (2 * pi * radius)
```

#### Public Function Pattern
```python
def calculate_frequency(
    translatory_speed: Quantity,
    radius: Quantity,
    unit: str = "hertz",
    precision: int = 2,
) -> Quantity:
    """
    Calculate rotational frequency from translatory speed and radius.

    Parameters
    ----------
    translatory_speed : Quantity
        Translatory speed with length/time dimensions.
    radius : Quantity
        Radius with length dimensions.
    unit : str, optional
        Output unit. Default is "hertz".
    precision : int, optional
        Decimal places. Default is 2.

    Returns
    -------
    Quantity
        Calculated frequency with specified unit.

    Raises
    ------
    ValueError
        If unit conversion fails or radius is not positive.
    """
    try:
        # Convert inputs to standard units
        speed_magnitude = translatory_speed.to(u.meter / u.second).magnitude
        radius_magnitude = radius.to(u.meter).magnitude
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate denominator after unit conversion
    if np.any(radius_magnitude <= 0):
        raise ValueError("radius must be positive")

    # Validate output unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call private function (already validated)
    frequency_magnitude = _calculate_frequency(speed_magnitude, radius_magnitude)

    # Attach units and convert
    result = frequency_magnitude * u.hertz
    result = result.to(pint_unit)

    if precision is not None:
        result = np.round(result, precision)

    return result
```

### Key Validation Points

1. **Private Functions**: Validate parameters at the beginning, before any calculations
2. **Public Functions**: Validate after unit conversion (magnitudes may change)
3. **Error Messages**: Include parameter name and actual value
4. **Array Validation**: Use `np.any()` to check all elements
5. **Check `<= 0`**: Catches both zero and negative values (typically physically invalid)

### Anti-Patterns to Avoid

```python
# ❌ NEVER use try/except for division
try:
    result = numerator / denominator
except ZeroDivisionError:
    raise ValueError("Denominator cannot be zero")

# ❌ NEVER have vague error messages
if denominator == 0:
    raise ValueError("Invalid input")

# ✅ ALWAYS use explicit pre-checks with descriptive messages
if denominator <= 0:
    raise ValueError(f"denominator must be positive, got {denominator}")
result = numerator / denominator
```

### Step 3: Add to Module's `__init__.py`

1. Export the private function in the private section of `__init__.py`.
2. Export the public function in the public section of `__init__.py`.

Example for core module `__init__.py`:
```python
# Private functions from module (e.g., _volume_flow_mass_flow)
from eytelwein.core._calculations import (
    # ... other private functions
    _length_of_material_on_side_roll,
    # ... other private functions
)

# ... other imports

__all__ = [
    # ... other public functions
    "length_of_material_on_side_roll",
    # ... other public functions
]
```

Example for package-level `__init__.py`:
```python
# ... other imports

# Core - Public functions
from eytelwein.belt_conveyor_design import (
    # ... other public functions
    length_of_material_on_side_roll,
    # ... other public functions
)

# ... other imports

__all__ = [
    # ... other public functions
    "length_of_material_on_side_roll",
    # ... other public functions
]
```

## Complete Example

### Private Function (`_volume_flow_mass_flow.py`)

```python
def _length_of_material_on_side_roll(
    part_of_belt_lying_on_side_idler: float, belt_edge_distance: float
) -> float:
    """
    Calculates the length of material on the side roll of a conveyor belt.

    Args:
        part_of_belt_lying_on_side_idler (float): The length of the belt segment that lies
            on the side idler (in millimeters).
        belt_edge_distance (float): The distance from the edge of the belt to the point where
            the material ends (in millimeters).

    Returns:
        float: The effective length of material on the side roll (in millimeters).
    """
    return part_of_belt_lying_on_side_idler - belt_edge_distance
```

### Public Function (`volume_flow_mass_flow.py`)

```python
def length_of_material_on_side_roll(
    part_of_belt_lying_on_side_idler: Quantity,
    belt_edge_distance: Quantity,
    unit: str = "millimeter",
    precision: int = 2,
) -> Quantity:
    """
    Calculate the length of material on the side roll of a conveyor belt.

    This function calculates the effective length of material on the side roll by subtracting
    the belt edge distance from the part of belt lying on the side idler.

    Parameters:
    part_of_belt_lying_on_side_idler (Quantity): The length of the belt segment that lies on the side idler.
    belt_edge_distance (Quantity): The distance from the edge of the belt to the point where the material ends.
    unit (str, optional): The unit for the returned length. Defaults to "millimeter".
    precision (int, optional): The number of decimal places to round the result to. Defaults to 2.

    Returns:
    Quantity: The calculated effective length of material on the side roll with the specified unit.

    Raises:
    ValueError: If there is an error in converting units.
    """
    try:
        # Convert inputs to standard units
        part_on_side_idler_mm = part_of_belt_lying_on_side_idler.to(u.millimeter)
        belt_edge_distance_mm = belt_edge_distance.to(u.millimeter)
    except Exception as e:
        raise ValueError(f"Error in converting length units: {e}")

    # Ensure the unit is a valid Pint unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Call private implementation
    length_mm = (
        _length_of_material_on_side_roll(
            part_on_side_idler_mm.magnitude, belt_edge_distance_mm.magnitude
        )
        * u.millimeter
    )

    # Convert to requested output unit
    result = length_mm.to(pint_unit)

    # Apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
```

### Private Function Tests (`test__volume_flow_mass_flow.py`)

```python
class TestLengthOfMaterialOnSideRoll:
    def test_length_of_material_standard_case(self):
        # Standard case
        result = _length_of_material_on_side_roll(500.0, 125.0)
        assert result == pytest.approx(375.0, rel=1e-6)

    def test_length_of_material_zero_edge(self):
        # When edge is zero, length equals part_on_side_idler
        result = _length_of_material_on_side_roll(500.0, 0.0)
        assert result == pytest.approx(500.0, rel=1e-6)

    def test_length_of_material_equal_values(self):
        # When both values are equal, result should be zero
        result = _length_of_material_on_side_roll(250.0, 250.0)
        assert result == pytest.approx(0.0, rel=1e-6)

    def test_length_of_material_handles_zero_values(self):
        # Zero values
        result = _length_of_material_on_side_roll(0.0, 0.0)
        assert result == 0.0
```

### Public Function Tests (`test_volume_flow_mass_flow.py`)

```python
class TestLengthOfMaterialOnSideRoll:
    def test_length_of_material_typical_case(self):
        # Standard case
        part_on_side_idler = u.Quantity(500, u.millimeter)
        belt_edge = u.Quantity(125, u.millimeter)
        result = length_of_material_on_side_roll(part_on_side_idler, belt_edge)
        assert result.magnitude == pytest.approx(375.0, rel=1e-6)
        assert result.units == u.millimeter

    def test_length_of_material_zero_edge(self):
        # When edge is zero, length equals part_on_side_idler
        part_on_side_idler = u.Quantity(500, u.millimeter)
        belt_edge = u.Quantity(0, u.millimeter)
        result = length_of_material_on_side_roll(part_on_side_idler, belt_edge)
        assert result.magnitude == pytest.approx(500.0, rel=1e-6)
        assert result.units == u.millimeter

    def test_length_of_material_equal_values(self):
        # When both values are equal, result should be zero
        part_on_side_idler = u.Quantity(250, u.millimeter)
        belt_edge = u.Quantity(250, u.millimeter)
        result = length_of_material_on_side_roll(part_on_side_idler, belt_edge)
        assert result.magnitude == pytest.approx(0.0, rel=1e-6)
        assert result.units == u.millimeter

    def test_length_of_material_unit_conversion(self):
        # Test unit conversion - input in meters, output in cm
        part_on_side_idler = u.Quantity(0.5, u.meter)
        belt_edge = u.Quantity(125, u.millimeter)
        result = length_of_material_on_side_roll(
            part_on_side_idler, belt_edge, unit="centimeter"
        )
        assert result.magnitude == pytest.approx(37.5, rel=1e-6)
        assert result.units == u.centimeter

    def test_length_of_material_with_precision(self):
        # Test precision parameter
        part_on_side_idler = u.Quantity(500, u.millimeter)
        belt_edge = u.Quantity(123.456, u.millimeter)
        result = length_of_material_on_side_roll(
            part_on_side_idler, belt_edge, precision=0
        )
        assert result.magnitude == 377.0  # Rounded to 0 decimal places
        assert result.units == u.millimeter

    def test_length_of_material_invalid_unit(self):
        # Test with invalid unit
        part_on_side_idler = u.Quantity(500, u.millimeter)
        belt_edge = u.Quantity(125, u.millimeter)
        with pytest.raises(ValueError) as excinfo:
            length_of_material_on_side_roll(
                part_on_side_idler, belt_edge, unit="invalid_unit"
            )
        assert "Invalid unit" in str(excinfo.value)

    def test_length_of_material_incompatible_unit(self):
        # Test with incompatible unit
        part_on_side_idler = u.Quantity(500, u.millimeter)
        belt_edge = u.Quantity(125, u.millimeter)
        with pytest.raises(ValueError) as excinfo:
            length_of_material_on_side_roll(
                part_on_side_idler, belt_edge, unit="second"
            )
        assert "Cannot convert" in str(excinfo.value)
```

## Best Practices

1. **Separation of Concerns**: Private functions focus on calculation logic, public functions handle API and unit management
2. **Consistent Parameter Ordering**: Required parameters first, optional parameters next, unit and precision parameters last
3. **Mathematical Correctness**: Use radians for angles internally, SI units for calculations, document equation sources
4. **Documentation**: Include parameter descriptions with units, return values with units, valid input ranges, and references

For detailed implementation standards, refer to [`eytelwein_implementation_standards.md`](eytelwein_implementation_standards.md).
