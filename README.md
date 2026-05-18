<p align="center">
  <img src="docs/assets/logo.svg" alt="Eytelwein logo" width="200">
  <h1 align="center">Eytelwein</h1>
  <p align="center">
    <em>Open-source belt conveyor calculation library for Python</em>
  </p>
</p>

<p align="center">
  <a href="https://github.com/mdVoith/eytelwein/actions"><img src="https://github.com/mdVoith/eytelwein/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/mdVoith/eytelwein/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/python-≥3.13-blue.svg" alt="Python">
</p>

---

Eytelwein provides production-grade engineering calculations for belt conveyor
systems — from steady-state resistance and drive layout to idler roll loading and
horizontal curve forces. All public functions use [Pint](https://pint.readthedocs.io/)
`Quantity` objects for full dimensional safety: units in, units out, no silent
conversion errors.

## Highlights

- **Dimensionally safe** — every input and output carries explicit physical units
- **Dual-layer architecture** — bare-math `_module.py` (fast, unit-free) + public `module.py` (Quantity-wrapped, validated)
- **Comprehensive test suite** — 1 455 tests covering core and extended calculations
- **Typed** — `py.typed` marker, compatible with mypy strict mode

## Module Overview

| Module | Description |
|--------|-------------|
| `eytelwein.belt_conveyor_design.core` | Volume/mass flow, belt tensions, drive layout, belt design, tension distribution, minimum pulley diameters, resistance & power |
| `eytelwein.belt_conveyor_design.extended` | Extended methods — mass inertia, design of conveyor belt, additional drive layout functions |
| `eytelwein.idler_design` | Idler roll load factor calculations |
| `eytelwein.horizontal_curves` | Lateral force analysis for horizontally curved belt conveyors |
| `eytelwein.main` | Shared utilities — unit registry singleton, physical constants |

## Installation

```bash
pip install git+https://github.com/voith/eytelwein.git
```

## Quick Start

```python
from eytelwein.main.units import get_unit_registry
u = get_unit_registry()

from eytelwein.belt_conveyor_design import usable_belt_width

# Calculate usable belt width for a 1200 mm belt
b = usable_belt_width(belt_width=1200 * u.mm)
print(b)  # 1050.0 millimeter
```

## Real-World Example Script

For a more practical, end-to-end workflow, run the example script in
`examples/real_world_cross_section_flow.py`.

It demonstrates a compact sizing pipeline with hard-coded values:

- usable belt width from belt geometry
- cross-section of fill from trough geometry
- volume flow from cross-section and belt speed
- mass flow from volume flow and bulk density
- inverse cross-check for required usable width

```bash
python examples/real_world_cross_section_flow.py
```

## Feature Examples

Dedicated, runnable scripts are available under `examples/features/`.

- `a_output_unit_minimum_tension.py`
  Demonstrates changing output units for the same calculation
  (minimum belt tension in N and kN).
- `b_imperial_input_dual_output.py`
  Uses imperial inputs and calls the same function twice to produce
  imperial output and SI output.
- `c_unit_errors_are_caught.py`
  Shows dimensional unit mismatch handling (expected `ValueError`).
- `d_physically_invalid_inputs_are_caught.py`
  Shows physically invalid input handling (expected `ValueError`).
- `e_output_precision_control.py`
  Shows how to control rounding with `precision` (default, custom,
  and unrounded output).
- `f_round_trip_consistency.py`
  Shows forward/inverse round-trip checks and validates numerical
  consistency within explicit tolerances.
- `g_constants_and_enums.py`
  Shows using public enums (`IdlerSets`) and shared constants in
  practical calculations.

Run each from repository root:

```bash
python examples/features/a_output_unit_minimum_tension.py
python examples/features/b_imperial_input_dual_output.py
python examples/features/c_unit_errors_are_caught.py
python examples/features/d_physically_invalid_inputs_are_caught.py
python examples/features/e_output_precision_control.py
python examples/features/f_round_trip_consistency.py
python examples/features/g_constants_and_enums.py
```

## Architecture

```
src/eytelwein/
├── belt_conveyor_design/
│   ├── core/           # Fundamental steady-state calculations
│   │   ├── _module.py  # Pure math (float in / float out)
│   │   └── module.py   # Quantity-wrapped public API
│   ├── extended/       # Additional / derived calculations
│   ├── data/           # Lookup tables (CSV)
│   └── constants.py    # Enums & domain constants
├── idler_design/
│   └── core/           # Idler roll load factors
├── horizontal_curves/
│   └── core/           # Lateral force components
└── main/
    ├── units.py        # UnitRegistry singleton
    └── constants.py    # Physical constants (via scipy)
```

## Mathematical Background

The calculations implement established belt conveyor engineering methodologies
covering:

- **Resistance and power** — main, secondary, and gradient resistances for steady-state operation
- **Belt tensions** — minimum tensions from sag constraints, tension distribution across belt width
- **Drive system layout** — torque, power, and speed relationships for single and multi-drive configurations
- **Volume and mass flow** — cross-sectional fill geometry, reduction factors for inclined conveyors
- **Minimum pulley diameters** — based on belt tension member type and load classification
- **Idler roll loading** — load distribution factors for various trough configurations
- **Horizontal curves** — centripetal, gravity, and tilted-idler restraining forces (conventional and improved methods)

## Development

```bash
# Clone and install
git clone https://github.com/voith/eytelwein.git
cd eytelwein
uv sync

# Run checks
uv run pytest               # 1455 tests
uv run ruff check src/ tests/
uv run mypy src/
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

Apache-2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE).

Copyright 2025 Voith Group.
