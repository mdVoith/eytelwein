---
name: private-to-public-function
description: 'Implement public Eytelwein API functions from private calculation helpers. Use for wrapping private numeric functions with Quantity-based public APIs, adding unit conversion and validation, updating __init__.py exports, and writing matching private/public tests.'
argument-hint: 'What private function or public wrapper are you implementing?'
---

# Private To Public Function Implementation

Use this skill when turning an internal numeric helper into a public API function in the Eytelwein codebase. It focuses on the handoff between private raw-magnitude calculations and public `Quantity`-aware wrappers, plus the required exports and paired tests.

## When to Use

- Promoting a private helper into a public function
- Adding a new public wrapper around an existing private calculation
- Splitting calculation logic from unit handling and validation
- Fixing a public API that performs too much math inline instead of delegating to a private helper
- Adding matching private and public tests for a new API function
- Updating module exports after a new function is added

## Core Rules

1. Private functions implement pure calculation logic on raw numeric inputs.
2. Public functions accept `Quantity` inputs and handle unit conversion, validation, output units, and precision.
3. Private functions live in underscore-prefixed modules and use underscore-prefixed names.
4. Public functions live in the corresponding public module and expose the user-facing API.
5. Denominator and other critical constraints must be validated explicitly before division.
6. Public wrappers must export through the relevant `__init__.py` files.
7. Private and public layers both need targeted tests.
8. This workflow must follow the broader standards in the Eytelwein implementation guide.

## Procedure

### 1. Decide Whether the Split Is Correct

Before writing code, confirm the function should follow this pattern.

Use a private plus public split when:

- the core math can operate on plain magnitudes
- unit conversion and output formatting are interface concerns
- the function is part of the public engineering API

Do not collapse everything into one public function unless the calculation is trivial and the private helper would add no clarity.

### 2. Implement the Private Function First

In the underscore-prefixed module:

- add the private function with raw numeric parameters
- document expected units in the docstring or parameter descriptions
- keep the implementation focused on the formula itself
- validate only critical constraints such as division denominators or restricted mathematical domains
- avoid unit handling and output formatting in the private layer

The private function should be easy to test directly for mathematical correctness.

### 3. Implement the Public Wrapper

In the corresponding public module:

- import the private helper
- define the public function with `Quantity` parameters
- add `unit` and `precision` parameters where appropriate
- convert inputs into the standard working units inside `try/except`
- validate physical constraints after unit conversion
- validate the requested output unit
- call the private function with magnitudes only
- attach the correct output unit
- convert to the requested output unit
- apply rounding or precision only at the public layer

The public function is the user-friendly interface. It should explain physical meaning, accepted input quantities, return units, and failure conditions.

### 4. Handle Validation at the Right Layer

Use this split consistently:

- private function: validate at the beginning when a denominator or mathematical domain can fail
- public function: validate again after conversion when user-facing physical constraints matter

For denominator checks:

- use explicit pre-checks such as `<= 0`
- use `np.any()` for arrays
- raise `ValueError` with descriptive parameter-focused messages

Do not use `try/except ZeroDivisionError` as the validation strategy.

### 5. Export the Function Correctly

After implementation:

- export the private function in the private section of the module-level `__init__.py` if that package exposes private helpers internally
- export the public function in the public section of the module-level `__init__.py`
- export the public function again in any package-level `__init__.py` that forms part of the public API surface
- update `__all__` where the package uses it

If the import chain is incomplete, the implementation is not finished even if the function code itself is correct.

### 6. Write the Paired Tests

Add both private and public tests.

#### Private tests

Verify:

- core mathematical correctness
- standard numeric cases
- edge cases such as zero or equal values when meaningful
- denominator validation or other critical internal constraints

#### Public tests

Verify:

- basic `Quantity` usage with expected units
- input unit conversion
- output unit conversion
- precision handling
- invalid output unit errors
- incompatible unit errors
- validation messages for invalid physical inputs

Use the mandatory Eytelwein test structure from the broader standards.

### 7. Validate the Import Chain and Runtime Behavior

After tests are written:

- run the private test file
- run the public test file
- run the enclosing module test suite
- validate public import access through the package import chain
- run a small smoke test with realistic values

Use `uv run` for all Python execution and testing in this repository.

## Debugging Decision Points

Use these branches to narrow failures quickly.

- The public function works locally but cannot be imported from the package: inspect `__init__.py` exports and `__all__`.
- The public function mixes math and unit handling awkwardly: move magnitude-only logic into the private helper.
- A denominator error appears as runtime failure instead of `ValueError`: add explicit pre-checks in the private layer and user-facing validation in the public layer.
- Unit conversion errors are confusing or inconsistent: standardize the public wrapper's conversion and output-unit validation flow.
- Tests cover only the public API: add a direct private test file to lock down the formula itself.
- The public wrapper passes through raw numbers: tighten the signature back to `Quantity` inputs.

## Completion Checklist

Do not consider the task complete until all relevant items pass.

- [ ] Private helper exists in the correct underscore-prefixed module
- [ ] Private helper operates on raw numeric inputs only
- [ ] Public wrapper accepts `Quantity` inputs and returns `Quantity`
- [ ] Public wrapper performs unit conversion, validation, output conversion, and precision handling
- [ ] Critical denominator or domain checks use explicit pre-validation
- [ ] Private and public functions are exported through the correct `__init__.py` files
- [ ] Private tests verify mathematical correctness directly
- [ ] Public tests verify unit handling, precision, and error behavior
- [ ] Documentation includes parameter descriptions with units, return values with units, valid input ranges, and references
- [ ] Import-chain validation succeeds
- [ ] Smoke test with realistic values succeeds under `uv run`

## Related Skills and References

- Use [../eytelwein-implementation/SKILL.md](../eytelwein-implementation/SKILL.md) for the broader Eytelwein standards on unit registry usage, array broadcasting, naming, and test layout.
- See [docs/guides/private_to_public_function_implementation_guide.md](../../../docs/guides/private_to_public_function_implementation_guide.md) for the full walkthrough and examples.
- See [docs/guides/eytelwein_implementation_standards.md](../../../docs/guides/eytelwein_implementation_standards.md) for the underlying implementation standards this skill depends on.
