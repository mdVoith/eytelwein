# eytelwein

Belt conveyor calculation library implementing DIN 22101, VDI 2341, and horizontal curve standards.

## Features

- **DIN 22101** — Volume/mass flow, belt tensions, drive system layout, belt design, belt width distribution, minimum pulley diameters, resistance & power for steady operations (core + extended methods)
- **VDI 2341** — Idler roll calculations
- **Horizontal Curves** — Research-based horizontal curve force calculations
- **Quantity-based API** — All public functions accept and return [Pint](https://pint.readthedocs.io/) `Quantity` objects for dimensional safety

## Installation

```bash
pip install eytelwein
```

## Quick Start

```python
from eytelwein.main.units import get_unit_registry

ureg = get_unit_registry()

# Example: use DIN 22101 volume/mass flow calculations
from eytelwein.din_22101.core.volume_flow_mass_flow import (
    cross_sectional_area_of_bulk_material_on_belt,
)
```

## Dependencies

- Python >= 3.13
- numpy >= 2.2.4
- pint >= 0.24.4
- scipy >= 1.15.0

## Development

```bash
uv sync
uv run pytest
uv run ruff check src/ tests/
uv run mypy src/
```

## License

Apache-2.0 — see [LICENSE](LICENSE) for details.
