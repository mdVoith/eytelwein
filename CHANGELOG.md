## v0.1.5 (2026-06-30)

### Feat

- remove unused inertia functions and related tests
- unify single-drive inertia model
- add total pulley shaft inertia function
- add translating mass inertia calculation at pulley shaft with unit tests

### Refactor

- switch translating mass calculation to a canonical aggregate implementation as single source of truth and with fewer regression paths plus derived thin wrapper implementations for useful cases
- use one gearbox ratio for low-speed inertia
- rename translating mass inertia function
- rename gearbox gear ratio parameters to drive gear ratio for clarity
- update variable names for clarity in mass inertia calculations and use gear ratio
- Refactor mass inertia tests

## v0.1.4 (2026-06-24)

### Feat

- update function names for belt safety factor calculations for consistency
- add design functions for conveyor belt safety factor and tension calculations, with unit tests

## v0.1.3 (2026-06-19)

### Feat

- add public resulting force wrapper
- export takeup weight conversions
- add public takeup weight conversions
- add test for converting 3000 kg takeup weight to force
- add private takeup weight conversions

### Refactor

- remove local commit type enforcement hook and update bump message format

## v0.1.2 (2026-06-08)

### Fix

- update version to 0.1.1 and remove unused documentation
- logo path in README

### Refactor

- precision handling in calculations across multiple modules. Use `None` as default.

## v0.1.1 (2026-06-03)

## v0.1.0 (2026-06-02)

### Feat

- initial release of eytelwein belt conveyor library

### Fix

- **ci**: update conditions for uploading pages artifact and deployment to include workflow_dispatch (#7)
- update repository URLs in README and pyproject.toml (#4)
- update CI badge link in README.md to point to the correct repository (#1)
- resolve mypy type errors in units.py and horizontal_curve_calculations.py
- remove unused pytest import in test_constants
