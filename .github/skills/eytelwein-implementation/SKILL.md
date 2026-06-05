---
name: eytelwein-implementation
description: 'Implement, extend, or review Eytelwein functions and modules. Use for unit-registry patterns, Quantity-only APIs, array broadcasting, physical validation, zero-division prevention, mathematically precise naming, UV-based test workflows, and Eytelwein test structure.'
argument-hint: 'What Eytelwein function, module, or standard are you implementing?'
---

# Eytelwein Implementation

Use this skill when adding or modifying code in the Eytelwein library. It packages the standards for unit handling, public-versus-private validation responsibilities, array broadcasting, naming, test layout, and the exact UV-based validation sequence expected in this repository.

## When to Use

- Adding a new Eytelwein public function
- Adding a matching private helper implementation
- Implementing `_sections` vectorized functions
- Reviewing a function for unit-safety and physical validation
- Fixing array broadcasting or shape mismatch bugs
- Preventing division-by-zero and unit-conversion regressions
- Building or reviewing Eytelwein test coverage and import-chain validation

## Core Rules

1. Use `uv run` for Python execution, tests, and validation commands.
2. Import the unit registry at module scope and initialize `u = get_unit_registry()` once.
3. Public functions accept strict `Quantity` inputs with explicit units.
4. Public functions always validate physical constraints after unit conversion.
5. Private functions validate only critical mathematical or physical constraints.
6. Prevent zero-division with explicit pre-checks, not `ZeroDivisionError` handling.
7. Use the Pint-first, then NumPy array detection and broadcasting pattern.
8. Function names must be mathematically precise and explicit about direction, source, or output type.
9. Follow the mandatory Eytelwein test directory structure.
10. Never hardcode physical constants. Use `STANDARD_GRAVITY_VALUE` from `eytelwein.main.constants`; check that module before writing any numeric constant inline.
11. Standard input validation is `.to()` inside `try/except` → `ValueError`. Do not add `isinstance(param, Quantity)` checks or upfront output-unit dimensionality pre-checks — both are non-standard, inconsistent with the rest of the codebase, and produce `TypeError` instead of `ValueError`.
12. When calling an eytelwein public function and you need the result in a specific unit, pass `unit="target_unit"` to the function call. Never call with the default unit then `.to(target)` afterward — `precision` rounds in the **output unit**, so rounding in the wrong unit (e.g. m³/s) then converting (to m³/h, ×3600) amplifies rounding error catastrophically.
13. **No early rounding in calculation code.** When a wrapper function calls another eytelwein public function as an intermediate step, avoid low-precision rounding on that intermediate result. Omit `precision=` when the default behavior is acceptable, or use enough precision for the downstream calculation. Display rounding belongs at the final public return layer, not in intermediate calculation steps.

## Procedure

### 1. Confirm the Function Boundary

Before writing code, decide:

- whether the function is public, private, or both
- whether a `_sections` vectorized variant is required
- the expected physical dimensions of every parameter
- the canonical output quantity and unit family
- whether the result is dimensional or dimensionless

If the function can return related output forms such as total versus per-unit-length, prefer separate functions with explicit names instead of an `output_type` parameter.

### 2. Set Up the Module Correctly

At module scope:

- import `get_unit_registry` from `eytelwein.main.units`
- initialize `u = get_unit_registry()`
- organize imports in the standard order
- import performance helpers only if the module needs high-performance dispatch

Do not import the unit registry inside functions.

### 3. Implement the Private Calculation Layer

Private functions should work on magnitudes and remain focused on the core math.

Validate only where needed:

- denominators before division
- restricted mathematical domains such as `sqrt`, `log`, or inverse trig inputs
- non-obvious multi-parameter physical constraints

Do not add redundant validation to simple arithmetic helpers that only receive pre-validated inputs.

### 4. Implement the Public Quantity-Aware Layer

Public functions are the interface boundary and must:

- accept `Quantity` inputs, not raw numbers
- convert inputs to standard working units inside `try/except`
- validate physical meaningfulness after unit conversion
- attach output units explicitly, including `u.dimensionless` for dimensionless results
- parse and validate requested output units
- convert to the requested output unit
- apply precision only at the public return layer when appropriate

If unit conversion fails, raise `ValueError` with the standard conversion message pattern.

### 5. Apply Defense-in-Depth Validation

Use this split consistently:

- public functions: comprehensive physical validation after conversion
- private functions: critical mathematical safety checks only

For the most failure-prone calculations, it is acceptable and preferred to validate at both layers.

### 6. Handle Zero-Division Explicitly

Before any division:

- check scalar denominators with explicit comparisons such as `<= 0`
- check array denominators with `np.any(array <= 0)`
- raise `ValueError` that includes the parameter name and invalid value when practical

Do not catch `ZeroDivisionError` and re-raise it. The pre-check is the standard.

### 7. Implement Array Broadcasting Deliberately

For `_sections` functions:

- detect Pint Quantity arrays before plain NumPy arrays
- determine the primary shape from the first array input encountered
- expand scalar inputs with `np.full(primary_shape, scalar_value)`
- validate that all resulting arrays share a consistent shape
- flatten higher-dimensional outputs if the API expects 1D results
- attach units only after the vectorized calculation result is produced

If `high_performance` is supported, use the standard performance-dispatch pattern with fallback to the default vectorized implementation.

### 8. Name Functions Precisely

Function names should communicate:

- the physical quantity being computed
- the orientation or direction if relevant
- the source inputs when needed for clarity
- whether the function returns per-section data via `_sections`
- whether the output is total or per-unit-length by using separate function names

Avoid short or generic names that hide the physical meaning.

### 9. Build Tests in the Required Structure

Use the mandatory directory pattern:

- `tests/test_{module_name}/` — top-level test directory for a module
- `tests/test_{module_name}/test_core/` — test subdirectory for core private functions
- Tests should be named `test__{private_module}.py` or `test_{public_module}.py` to reflect what is being tested

Cover the expected categories:

- private function mathematical correctness
- public function unit conversion and error handling
- precision behavior
- array broadcasting and mixed scalar-array inputs
- edge cases and invalid values
- `_sections` high-performance and fallback behavior when applicable

### 10. Validate in the Standard Sequence

After implementation, run validation in this order with `uv run`:

1. private-function tests
2. public-function tests
3. full module test suite
4. import-chain validation from the public module
5. functional smoke test with realistic values

When preparing changes for completion, also run formatting, type checking, and any broader module-level regression suite that applies.

## Debugging Decision Points

Use these branches to narrow failures quickly.

- Import works only inside one function or test: inspect whether the unit registry or public exports were placed incorrectly.
- A public API accepts raw numerics or ambiguous units: tighten the boundary to strict `Quantity` inputs.
- Errors surface as `ZeroDivisionError`: replace runtime exception handling with explicit denominator validation.
- Array behavior is inconsistent across scalars and arrays: inspect primary-shape detection and scalar expansion logic.
- Output values are right in magnitude but lose units: inspect the public return layer and dimensionless attachment.
- Naming feels ambiguous: split the API into separate, more precise functions rather than adding flags.
- Tests pass for scalars but fail for `_sections`: inspect broadcasting, shape checks, and flattening behavior.

## Completion Checklist

Do not consider Eytelwein work complete until all relevant items pass.

- [ ] Module-level unit registry pattern is used
- [ ] Public APIs require explicit `Quantity` inputs
- [ ] Public validation happens after unit conversion
- [ ] Private functions guard critical mathematical constraints
- [ ] Zero-division is prevented with pre-checks
- [ ] Array broadcasting follows the Pint-first pattern
- [ ] Error messages follow the standard templates
- [ ] Function names are physically and mathematically precise
- [ ] Tests follow the mandatory Eytelwein directory layout
- [ ] Private, public, module, import, and smoke validations are run with `uv run`
- [ ] Dimensionless outputs are returned as `Quantity` values with `u.dimensionless`
- [ ] Physical constants use `STANDARD_GRAVITY_VALUE` from `eytelwein.main.constants` — no hardcoded `g` values
- [ ] Input validation uses `.to()` inside `try/except` only — no `isinstance` checks, no output-unit dimensionality pre-checks

## Reference

- See [docs/guides/eytelwein_implementation_standards.md](../../../docs/guides/eytelwein_implementation_standards.md) for extended rationale, templates, and command examples.
