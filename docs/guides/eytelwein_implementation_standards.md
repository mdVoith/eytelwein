# Eytelwein Implementation Standards

**Note:** This document covers standards for implementing eytelwein functions and working with Pint Quantities in the Eytelwein package.

## Quick Reference

- [Development Environment](#development-environment)
- [Unit Registry Patterns](#unit-registry-patterns)
- [Array Broadcasting](#array-broadcasting)
- [Physical Meaningfulness Validation](#physical-meaningfulness-validation)
- [Error Messages](#error-messages)
- [Zero-Division Error Handling](#zero-division-error-handling)
- [Function Naming](#function-naming)
- [Test Structure](#test-structure)
- [Import Organization](#import-organization)
- [Implementation Template](#implementation-template)
- [Validation Workflow](#validation-workflow)

## Development Environment

### Tool Stack Requirements
- **Environment Manager**: UV (handles virtual environments and Python execution)
- **Shell examples in this guide**: validated on Windows PowerShell
- **Command Prefix**: Always use `uv run` for Python execution
- **Testing Framework**: pytest with UV integration

### Core Commands (PowerShell Compatible)

For testing Eytelwein calculations:
```powershell
# Run all tests
uv run pytest tests/ -v

# Run belt conveyor design tests
uv run pytest tests/test_belt_conveyor_design/ -v

# Run horizontal curves tests
uv run pytest tests/test_horizontal_curves/ -v

# Type check calculations
uv run mypy src/eytelwein/

# Format code
uv run ruff format src/ tests/
```

### PowerShell Syntax Standards

#### ✅ Correct Command Patterns
```powershell
# Single quotes for file paths
uv run pytest 'tests/' -v

# Double quotes for Python code with variables
uv run python -c "import sys; print(f'Python version: {sys.version}')"

# Proper escaping for complex strings
uv run python -c "from eytelwein.belt_conveyor_design.core.volume_flow_mass_flow import usable_belt_width; print(f'Imported: {usable_belt_width.__name__}')"

# Line continuation for long commands
uv run pytest `
  tests/test_belt_conveyor_design/ `
  -v
```

#### ❌ Problematic Patterns to Avoid
```powershell
# Mixed quote issues
uv run python -c 'print(f"Result: {value}")'  # ❌ Error

# Unescaped nested quotes
uv run python -c "print("hello")"  # ❌ Error

# Missing uv run prefix
python -m pytest tests/  # ❌ Wrong - doesn't use UV environment

# Direct python execution
python script.py  # ❌ Wrong - use uv run python script.py
```

### Error Handling in Commands

#### Safe Import Testing
```powershell
# ✅ Test a real Eytelwein import path
uv run python -c "from eytelwein.belt_conveyor_design.core.volume_flow_mass_flow import usable_belt_width; print(f'✅ Import works: {usable_belt_width.__name__}')"
```

## Unit Registry Patterns

### ✅ Module-Level Import (MANDATORY)
```python
# At module top - ALWAYS
from eytelwein.main.units import get_unit_registry
u = get_unit_registry()

def public_function(...):
    # Use u.newton, u.meter, etc. throughout module
    magnitude = input_value.to(u.meter).magnitude
```

### ❌ Function-Level Import (FORBIDDEN)
```python
# NEVER import inside functions
def public_function(...):
    from eytelwein.main.units import get_unit_registry  # ❌ Wrong!
    u = get_unit_registry()
```

### Dimensionless Values
Even dimensionless calculations must return Quantity objects:
```python
# Private function returns raw number
efficiency = _efficiency_calculation(...)

# Public function MUST attach units
result = efficiency * u.dimensionless
```

## Array Broadcasting

### Array Detection Pattern
```python
# Check Pint Quantity arrays first, then NumPy arrays
if hasattr(input_param, "magnitude") and isinstance(input_param.magnitude, np.ndarray):
    # Pint Quantity array
    array_data = input_param.magnitude
    primary_shape = array_data.shape
elif isinstance(input_param, np.ndarray):
    # NumPy array
    array_data = input_param
    primary_shape = array_data.shape
else:
    # Scalar
    primary_shape = (1,)
```

### Primary Shape Detection
```python
# Find first array input as primary shape reference
primary_shape = None
for param in [param1, param2, param3]:
    if hasattr(param, "magnitude") and isinstance(param.magnitude, np.ndarray):
        primary_shape = param.magnitude.shape
        break
    elif isinstance(param, np.ndarray):
        primary_shape = param.shape
        break

# Use np.full(primary_shape, scalar_value) for scalar expansion
```

### Scalar Expansion Pattern
```python
# Convert scalar to array with primary shape
if isinstance(param, (int, float)) or not hasattr(param, "shape"):
    param_array = np.full(primary_shape, param.to(u.target_unit).magnitude)
else:
    param_array = param.to(u.target_unit).magnitude
```

## Physical Meaningfulness Validation

### Core Principles

**Validation follows a "defense in depth" strategy with distinct responsibilities for public and private functions.**

The eytelwein package implements a systematic validation approach:
- **Public functions**: ALWAYS validate physical constraints after unit conversion
- **Private functions**: SELECTIVELY validate for critical constraints

### Validation Responsibility by Function Type

#### Public Functions (MANDATORY VALIDATION)

**All public functions MUST validate physical meaningfulness AFTER unit conversion.**

✅ **Required Validations:**
- Non-negativity for physical quantities (masses, lengths, areas, volumes, forces)
- Positivity for quantities that cannot be zero (denominators, belt widths, radii)
- Range constraints (angles between 0 and π, dimensionless factors ≥ 0)
- Array shape consistency when multiple array inputs are provided

**Pattern:**
```python
def public_calculation(
    value: Quantity,
    radius: Quantity,
    unit: str = "meter",
    precision: int = 2,
) -> Quantity:
    """Calculate something with unit handling."""
    # Step 1: Convert units
    try:
        value_m = value.to(u.meter)
        radius_m = radius.to(u.meter)
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Step 2: MANDATORY validation after unit conversion
    if value_m.magnitude < 0:
        raise ValueError("value must be non-negative")

    if radius_m.magnitude <= 0:
        raise ValueError(f"radius must be positive, got {radius}")

    # Step 3: Call private implementation
    result_magnitude = _private_calculation(value_m.magnitude, radius_m.magnitude)

    # Step 4: Return with units
    return result_magnitude * u.meter
```

**Rationale:**
1. Public functions are the user-facing interface boundary
2. Unit conversion happens here - validation must occur on converted values
3. Users receive clear errors with their original input units
4. Comprehensive validation provides predictable error semantics

#### Private Functions (SELECTIVE VALIDATION)

**Private functions validate selectively based on criticality.**

✅ **When to Validate in Private Functions:**
- **Division by zero risks**: Validate denominators before division
  ```python
  def _calculate_ratio(numerator: float, denominator: float) -> float:
      if denominator <= 0:
          raise ValueError(f"denominator must be positive, got {denominator}")
      return numerator / denominator
  ```

- **Mathematical domain constraints**: Validate inputs to functions with restricted domains
  ```python
  def _angle_from_sine(sine_value: float) -> float:
      if not (-1 <= sine_value <= 1):
          raise ValueError(f"sine_value must be in [-1, 1], got {sine_value}")
      return np.arcsin(sine_value)
  ```

- **Complex multi-parameter constraints**: Validate when physical relationships are non-obvious
  ```python
  def _belt_weight_distribution(center_load: float, wing_load: float) -> float:
      if center_load < 0 or wing_load < 0:
          raise ValueError("Load values must be non-negative")
      return center_load + 2 * wing_load
  ```

❌ **When to Skip Validation in Private Functions:**
- **Simple arithmetic operations**: Addition, subtraction, multiplication
  ```python
  def _belt_weight_per_square_meter(
      tension_member_weight: float,
      top_cover_thickness: float,
      bottom_cover_thickness: float,
      rubber_density: float,
  ) -> float:
      # No validation needed - simple arithmetic
      cover_weight = (top_cover_thickness + bottom_cover_thickness) * rubber_density
      return tension_member_weight + cover_weight
  ```

- **Functions guaranteed to receive pre-validated inputs**: When called only from validated public functions
- **Pure mathematical transforms**: Linear combinations without physical constraints

**Rationale:**
1. Avoids redundant validation overhead
2. Public functions already provide comprehensive input validation
3. Performance optimization for internal calculations
4. Maintains focus on critical mathematical safety (division, domain checks)

### Defense in Depth Pattern

**Most critical functions implement validation at BOTH levels:**

```python
# Private function - validates division safety
def _force_component_from_tension(
    belt_tension: float,
    idler_spacing: float,
    horizontal_curve_radius: float
) -> float:
    """Calculate force component [internal calculation]."""
    # Validate denominator to prevent division by zero
    if horizontal_curve_radius <= 0:
        raise ValueError(
            f"horizontal_curve_radius must be positive, got {horizontal_curve_radius}"
        )
    return belt_tension * idler_spacing / horizontal_curve_radius


# Public function - validates physical constraints after unit conversion
def force_component_towards_inside_curve_from_belt_tension(
    belt_tension: Quantity,
    idler_spacing: Quantity,
    horizontal_curve_radius: Quantity,
    unit: str = "newton",
    precision: int = 2,
) -> Quantity:
    """Calculate force component towards inside of curve."""
    # Convert units
    try:
        belt_tension_magnitude = belt_tension.to(u.newton).magnitude
        idler_spacing_magnitude = idler_spacing.to(u.meter).magnitude
        horizontal_curve_radius_magnitude = horizontal_curve_radius.to(u.meter).magnitude
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate after unit conversion (may duplicate private check, but with better error context)
    if np.any(horizontal_curve_radius_magnitude <= 0):
        raise ValueError("horizontal_curve_radius must be positive")

    # Safe to call private implementation
    result_magnitude = _force_component_from_tension(
        belt_tension_magnitude,
        idler_spacing_magnitude,
        horizontal_curve_radius_magnitude,
    )

    return result_magnitude * u.newton
```

**Benefits of Defense in Depth:**
1. Catches errors at multiple layers
2. Private validation protects against implementation bugs
3. Public validation provides user-friendly errors with original units
4. Redundant checks have minimal performance impact vs. safety benefit

### Array Validation Patterns

**For array inputs, validate all elements:**

```python
# Private function with array validation
def _calculate_stress(force_array: np.ndarray, area_array: np.ndarray) -> np.ndarray:
    """Calculate stress from force and area arrays."""
    # Validate all elements in denominator array
    if np.any(area_array <= 0):
        raise ValueError("All area values must be positive")

    return force_array / area_array


# Public function with array input validation
def calculate_stress_sections(
    forces: Union[Quantity, np.ndarray],
    areas: Union[Quantity, np.ndarray],
    unit: str = "pascal",
) -> Quantity:
    """Calculate stress for multiple sections."""
    try:
        force_magnitudes = forces.to(u.newton).magnitude
        area_magnitudes = areas.to(u.meter**2).magnitude
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate arrays after conversion
    if np.any(area_magnitudes <= 0):
        raise ValueError("areas must be positive")

    result_magnitudes = _calculate_stress(force_magnitudes, area_magnitudes)
    return result_magnitudes * u.pascal
```

### Validation Checklist

Before implementing any function, verify:

**Public Functions:**
- [ ] Unit conversion errors caught with try/except
- [ ] Physical constraints validated AFTER unit conversion
- [ ] Descriptive error messages include parameter names and invalid values
- [ ] Array inputs validated with `np.any()` or `np.all()`
- [ ] Invalid output units caught and reported

**Private Functions:**
- [ ] Division by zero prevented with explicit pre-checks
- [ ] Mathematical domain constraints validated (sqrt, log, arcsin inputs)
- [ ] Complex physical constraints checked when non-obvious
- [ ] Simple arithmetic functions may skip validation

## Error Messages

### Standard Templates
| Scenario | Template |
|----------|----------|
| Unit conversion | `"Error in converting units: {e}"` |
| Positive validation | `"{parameter_name} must be positive"` |
| Non-negative validation | `"{parameter_name} must be non-negative"` |
| Zero-division prevention | `"{parameter_name} must be positive, got {value}"` |
| Array shapes | `"Inconsistent array shapes: {param1_name} {shape1}, {param2_name} {shape2}"` |
| Invalid units | `"Invalid unit: {unit}. Error: {e}"` |
| Array validation | `"{parameter_name_plural} must be positive"` (for arrays) |

## Zero-Division Error Handling

### Core Principles

**All zero-division scenarios MUST be prevented using explicit pre-checks, not exception handling.**

This standard applies to all private and public functions in the Eytelwein library. The goal is to provide clear, predictable error semantics with descriptive messages that help users identify and fix input problems immediately.

### The Three Rules

#### Rule A: Use Explicit Pre-Checks
Always validate denominators BEFORE performing division operations. Use explicit conditional checks rather than try/except blocks.

```python
# ✅ CORRECT: Explicit pre-check
def _calculate_ratio(numerator: float, denominator: float) -> float:
    """Calculate ratio of numerator to denominator."""
    if denominator <= 0:
        raise ValueError(f"denominator must be positive, got {denominator}")
    return numerator / denominator

# ❌ INCORRECT: Exception handling
def _calculate_ratio(numerator: float, denominator: float) -> float:
    """Calculate ratio of numerator to denominator."""
    try:
        return numerator / denominator
    except ZeroDivisionError:
        raise ValueError("Denominator cannot be zero")
```

#### Rule B: Raise ValueError with Descriptive Messages
Error messages must include:
1. The parameter name
2. The actual invalid value
3. The requirement (e.g., "must be positive")

```python
# ✅ CORRECT: Descriptive error message
if belt_speed <= 0:
    raise ValueError(f"belt_speed must be positive, got {belt_speed}")

# ❌ INCORRECT: Vague error message
if belt_speed <= 0:
    raise ValueError("Belt speed cannot be zero")
```

#### Rule C: Avoid try/except ZeroDivisionError
Never catch `ZeroDivisionError` and re-raise as `ValueError`. This pattern:
- Allows the error to appear in stack traces (confusing users)
- Is less efficient (exception creation overhead)
- Provides less clear semantics

```python
# ❌ ANTI-PATTERN: Catching ZeroDivisionError
try:
    result = numerator / denominator
except ZeroDivisionError:
    raise ValueError("Denominator cannot be zero")

# ✅ CORRECT: Explicit pre-check
if denominator <= 0:
    raise ValueError(f"denominator must be positive, got {denominator}")
result = numerator / denominator
```

### Common Patterns

#### Scalar Validation (Private Functions)
```python
def _calculate_frequency(speed: float, radius: float) -> float:
    """Calculate rotational frequency."""
    # Validate denominator before division
    if radius <= 0:
        raise ValueError(f"radius must be positive, got {radius}")

    return speed / (2 * pi * radius)
```

#### Array Validation (Private Functions)
```python
def _calculate_stress(force_array: np.ndarray, area_array: np.ndarray) -> np.ndarray:
    """Calculate stress from force and area arrays."""
    # Validate all elements in denominator array
    if np.any(area_array <= 0):
        raise ValueError("All area values must be positive")

    return force_array / area_array
```

#### Public Function Validation (After Unit Conversion)
```python
def calculate_ratio(
    numerator: Quantity,
    denominator: Quantity,
    unit: str = "dimensionless",
    precision: int = 2,
) -> Quantity:
    """Calculate ratio with unit handling."""
    try:
        numerator_magnitude = numerator.to(u.meter).magnitude
        denominator_magnitude = denominator.to(u.meter).magnitude
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate after unit conversion
    if np.any(denominator_magnitude <= 0):
        raise ValueError("denominator must be positive")

    # Safe to perform division
    result_magnitude = _calculate_ratio(numerator_magnitude, denominator_magnitude)

    result = result_magnitude * u.dimensionless
    return result
```

### Rationale

**Why explicit pre-checks over exception handling?**

1. **Predictable Error Semantics**: `ValueError` consistently indicates invalid input, not runtime failure
2. **Clear Stack Traces**: Users never see `ZeroDivisionError` in traces, reducing confusion
3. **Better Error Messages**: Include specific parameter names and values
4. **Performance**: Avoid exception creation overhead
5. **Code Clarity**: Intent is explicit - "this parameter must be positive"

**Why check `<= 0` instead of `== 0`?**

Most physical parameters (radius, speed, density, etc.) cannot be negative. Checking for non-positive values catches both:
- Division by zero
- Physically impossible negative values

This provides more robust input validation with one check.

### Usage Examples
```python
# Parameter validation
if np.any(horizontal_curve_radius_magnitude <= 0):
    raise ValueError("horizontal_curve_radius must be positive")

# Array shape validation
if not (array1.shape == array2.shape == array3.shape):
    raise ValueError(
        f"Inconsistent array shapes: tensions {array1.shape}, "
        f"spacings {array2.shape}, radii {array3.shape}"
    )

# Unit conversion error
try:
    magnitude = input_value.to(u.meter).magnitude
except Exception as e:
    raise ValueError(f"Error in converting units: {e}")
```

## Function Naming

### Core Principles
1. **Mathematical precision over brevity**
2. **Include physical direction/orientation**
3. **Specify calculation type and inputs**
4. **Use full descriptive parameter names**

### Naming Patterns
```python
# ✅ Good - Mathematically precise
force_component_towards_inside_curve_from_belt_tension()
belt_resistance_due_to_gradient_from_height_differences()
power_required_from_belt_tensions_and_speed()

# ❌ Poor - Ambiguous
horizontal_curve_force()
belt_resistance()
power_calculation()
```

### Multi-Section Functions
Use `_sections` suffix for vectorized operations:
```python
force_component_towards_inside_curve_from_belt_tension_sections()
belt_resistance_due_to_material_load_sections()
```

### Parameter Naming
```python
# ✅ Full descriptive names
def calculation(
    belt_width: Quantity,
    horizontal_curve_radius: Quantity,
    material_bulk_density: Quantity
):

# ❌ Abbreviated names
def calculation(
    width: Quantity,
    radius: Quantity,
    density: Quantity
):
```

### Separate Functions for Different Output Types

When a calculation can be expressed in multiple related forms (e.g., total vs. per-unit-length), create separate functions with descriptive names rather than adding output type parameters.

**Pattern Example: Total Force vs. Force Per Meter**

```python
# ✅ Separate functions with clear names
def friction_resistance_of_skirting_board_from_material_flow(
    material_mass_flow: Quantity,
    belt_velocity: Quantity,
    # ... other parameters
    skirting_board_length: Quantity,
    unit: str = "newton",
    precision: Optional[int] = 2,
) -> Quantity:
    """
    Calculate friction resistance between material and lateral skirting board.

    Returns
    -------
    Quantity
        Friction resistance force with the specified unit (e.g., newton).

    See Also
    --------
    friction_resistance_per_meter_of_skirting_board_from_material_flow :
        Calculate the friction resistance per unit length.
    """
    # Implementation calculates total force
    pass


def friction_resistance_per_meter_of_skirting_board_from_material_flow(
    material_mass_flow: Quantity,
    belt_velocity: Quantity,
    # ... other parameters (same as above)
    skirting_board_length: Quantity,
    unit: str = "newton/meter",
    precision: Optional[int] = 2,
) -> Quantity:
    """
    Calculate friction resistance per unit length of skirting board.

    Returns
    -------
    Quantity
        Friction resistance force per unit length (e.g., newton/meter).

    See Also
    --------
    friction_resistance_of_skirting_board_from_material_flow :
        Calculate the total friction resistance force.

    Notes
    -----
    Mathematical relationship: F_total = F_per_meter * length
    """
    # Reuses total force function and divides by length
    total_force = friction_resistance_of_skirting_board_from_material_flow(
        material_mass_flow, belt_velocity, ..., unit="newton", precision=None
    )
    return total_force / skirting_board_length.to(u.meter)
```

**Benefits:**
- Clear, unambiguous function names indicating output type
- Separate default units appropriate for each output type
- Easy to find the right function for a specific use case
- "See Also" cross-references link related functions
- Test validation can verify mathematical relationship between functions

**Avoid:**
```python
# ❌ Don't use output_type parameters
def friction_resistance_of_skirting_board_from_material_flow(
    ...,
    output_type: str = "total",  # ❌ Makes function signature unclear
    unit: str = "newton",
):
    if output_type == "total":
        return calculate_total()
    elif output_type == "per_meter":
        return calculate_total() / length
```

## Test Structure

### Test Location
Eytelwein tests are organized by module in the `tests/` directory:

```
tests/
├── test_belt_conveyor_design/
│   ├── test_core/
│   │   ├── test__volume_flow_mass_flow.py
│   │   └── test_volume_flow_mass_flow.py
│   ├── test_extended/
│   ├── test_constants.py
│   └── test_public_api_belt_weight.py
├── test_horizontal_curves/
├── test_idler_design/
└── test_main/
```

### Required Test Coverage

Write tests that verify:

1. **Basic functionality**: Functions produce correct results for known inputs
2. **Unit conversion**: Results correctly convert between different units
3. **Array broadcasting**: Functions handle Pint Quantity arrays and scalar expansion
4. **Input validation**: Invalid inputs are rejected with clear error messages
5. **Physical meaningfulness**: Negative or zero values rejected where physically invalid
6. **Precision handling**: Results round correctly with precision parameter

### Test File Naming Convention
```python
# Private helper tests in the matching module test file
def test_{private_function}_{behavior}(self):
    """Test {description}."""

# Public wrapper tests in the corresponding public module test file
def test_{public_function}_{behavior}(self):
    """Test {description}."""

# Examples:
def test_belt_weight_positive_inputs(self):
def test_belt_weight_unit_conversion(self):
def test_belt_weight_array_broadcasting(self):
```

For paired private/public tests, the common pattern in this repo is:

```text
tests/test_belt_conveyor_design/test_core/test__volume_flow_mass_flow.py
tests/test_belt_conveyor_design/test_core/test_volume_flow_mass_flow.py
```

## Import Organization

### Standard Import Order
```python
"""Module docstring."""

# 1. Standard library
from typing import Union, Optional
import numpy as np

# 2. Third-party libraries
from pint import Quantity

# 3. Eytelwein core utilities (unit registry ALWAYS first)
from eytelwein.main.units import get_unit_registry

# 4. Local module imports
from ._private_module import (
    _private_function_1,
    _private_function_2,
)

# 5. Module-level initialization (CRITICAL)
u = get_unit_registry()
```

## Implementation Template

### Complete Function Template
```python
from typing import Union
import numpy as np
from pint import Quantity

from eytelwein.main.units import get_unit_registry
from ._private_module import _private_calculation

u = get_unit_registry()

def public_calculation_function(
    param1: Quantity,
    param2: Quantity,
    unit: str = "newton",
    precision: int = 2,
) -> Quantity:
    """
    Calculate [description] using [method].

    Parameters
    ----------
    param1 : Quantity
        Description with expected dimensions [unit].
    param2 : Quantity
        Description with expected dimensions [unit].
    unit : str, optional
        Output unit. Default is "newton".
    precision : int, optional
        Decimal places for results. Default is 2.

    Returns
    -------
    Quantity
        Calculated result with specified unit.

    Raises
    ------
    ValueError
        If unit conversion fails or parameters are invalid.
    """
    try:
        # Convert inputs to standard units
        param1_magnitude = param1.to(u.target_unit).magnitude
        param2_magnitude = param2.to(u.target_unit).magnitude
    except Exception as e:
        raise ValueError(f"Error in converting units: {e}")

    # Validate inputs
    if np.any(param1_magnitude <= 0):
        raise ValueError("param1 must be positive")

    if np.any(param2_magnitude <= 0):
        raise ValueError("param2 must be positive")

    # Validate output unit
    try:
        pint_unit = u.parse_units(unit)
    except Exception as e:
        raise ValueError(f"Invalid unit: {unit}. Error: {e}")

    # Calculate
    result_magnitude = _private_calculation(param1_magnitude, param2_magnitude)

    # Attach units
    result = result_magnitude * u.newton  # or u.dimensionless for ratios

    # Convert to requested unit
    try:
        result = result.to(pint_unit)
    except Exception as e:
        raise ValueError(f"Error in converting to {unit}: {e}")

    # Apply precision
    if precision is not None:
        result = np.round(result, precision)

    return result

def public_calculation_function_sections(
    param1: Union[Quantity, np.ndarray],
    param2: Union[Quantity, np.ndarray],
    unit: str = "newton",
    precision: int = 2,
    high_performance: bool = False,
) -> Quantity:
    """Vectorized version for multiple sections."""

    try:
        # Determine primary shape (first array found)
        primary_shape = None
        for param in [param1, param2]:
            if hasattr(param, "magnitude") and isinstance(param.magnitude, np.ndarray):
                primary_shape = param.magnitude.shape
                break
            elif isinstance(param, np.ndarray):
                primary_shape = param.shape
                break

        if primary_shape is None:
            primary_shape = (1,)

        # Convert to consistent arrays
        if hasattr(param1, "magnitude") and isinstance(param1.magnitude, np.ndarray):
            array1 = param1.to(u.target_unit).magnitude
        else:
            array1 = np.full(primary_shape, param1.to(u.target_unit).magnitude)

        # Similar for param2...

        # Validate shapes
        if not (array1.shape == array2.shape):
            raise ValueError(f"Inconsistent array shapes: param1 {array1.shape}, param2 {array2.shape}")

    except Exception as e:
        raise ValueError(f"Error in converting units to arrays: {e}")

    # Validate arrays
    if np.any(array1 <= 0):
        raise ValueError("param1 must be positive")

    # Choose implementation
    if high_performance and has_high_performance_implementation("function_name"):
        hp_impl = get_high_performance_implementation("function_name")
        if hp_impl is not None:
            forces = hp_impl(array1, array2)
        else:
            # Fallback to UFuncs
            vectorized_func = np.frompyfunc(_private_calculation, 2, 1)
            forces = np.array(vectorized_func(array1, array2), dtype=float)
    else:
        # Standard UFuncs implementation
        vectorized_func = np.frompyfunc(_private_calculation, 2, 1)
        forces = np.array(vectorized_func(array1, array2), dtype=float)

    # Ensure 1D array
    if forces.ndim > 1:
        forces = forces.flatten()

    # Attach units and convert
    result = forces * u.newton
    result = result.to(pint_unit)

    if precision is not None:
        result = np.round(result, precision)

    return result
```

## Validation Checklist

Before implementing any function, verify:

- [ ] Unit registry imported at module level with `u = get_unit_registry()`
- [ ] Public function validates physical meaningfulness AFTER unit conversion (see [Physical Meaningfulness Validation](#physical-meaningfulness-validation))
- [ ] Private function validates critical constraints (division by zero, mathematical domains)
- [ ] Array detection follows Pint-first, then NumPy pattern
- [ ] Error messages use standard templates
- [ ] Function names are mathematically precise and descriptive
- [ ] Test structure follows mandatory directory pattern
- [ ] Import organization follows standard order
- [ ] Both single and sections functions implemented (if applicable)
- [ ] High-performance parameter included for sections functions
- [ ] Dimensionless results include `u.dimensionless` unit attachment

## Validation Workflow

### Running Tests

When developing Eytelwein calculations:

#### 1. Run Affected Module Tests
```powershell
# Test a specific module (e.g., belt conveyor design)
uv run pytest tests/test_belt_conveyor_design/ -v

# Test a specific paired private/public module test file
uv run pytest tests/test_belt_conveyor_design/test_core/test_volume_flow_mass_flow.py -v
```

#### 2. Run Full Test Suite
```powershell
# Run all tests
uv run pytest tests/ -v

# Expected: All tests pass
```

#### 3. Type Check Implementation
```powershell
# Type check the source code
uv run mypy src/eytelwein/

# Expected: No type errors
```

#### 4. Format and Lint
```powershell
# Format code
uv run ruff format src/ tests/

# Check linting
uv run ruff check src/ tests/
```

## Input Type Handling Standards

### Current Design Decision
All public functions require strict Quantity inputs with explicit units. Raw numeric values (floats/integers) are not automatically converted to Quantity objects. This maintains architectural clarity, ensures type safety, and provides immediate feedback for incorrect input types. Users must explicitly specify units using the module-level unit registry pattern used in this repo (e.g., `* u.newton`, `* u.dimensionless`, or `u.Quantity(...)`).

### Future Consideration
Automatic conversion of dimensionless numeric inputs (friction coefficients, load factors) to Quantity objects may be reconsidered if user experience significantly benefits from this flexibility. Any future implementation would require formal documentation, consistent patterns across all functions, and comprehensive testing to ensure type safety is maintained.
