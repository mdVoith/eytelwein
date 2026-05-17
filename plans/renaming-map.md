# Eytelwein → Convexus Renaming Map

> **Purpose**: Machine-readable mapping of all renames performed in the eytelwein
> extraction (Phase 3). Use this file with an AI coding agent to update `convexus`
> imports after switching to the `eytelwein` PyPI package.
>
> **How to use in convexus**: Find-and-replace all old import paths/names with the
> new ones listed below. Every section is organized OLD → NEW.

---

## 1. Top-Level Module Renames

These are the subpackage names exported from `eytelwein`.

| Old module path | New module path |
|---|---|
| `eytelwein.din_22101` | `eytelwein.belt_conveyor_design` |
| `eytelwein.din_22101.core` | `eytelwein.belt_conveyor_design.core` |
| `eytelwein.din_22101.extended` | `eytelwein.belt_conveyor_design.extended` |
| `eytelwein.din_22101.data` | `eytelwein.belt_conveyor_design.data` |
| `eytelwein.din_22101.constants` | `eytelwein.belt_conveyor_design.constants` |
| `eytelwein.vdi_2341` | `eytelwein.idler_design` |
| `eytelwein.vdi_2341.core` | `eytelwein.idler_design.core` |
| `eytelwein.vdi_2341.constants` | `eytelwein.idler_design.constants` |

Unchanged:
- `eytelwein.horizontal_curves` (already standard-free)
- `eytelwein.main` (no standard references)

---

## 2. Directory Renames (source)

| Old path | New path |
|---|---|
| `src/eytelwein/din_22101/` | `src/eytelwein/belt_conveyor_design/` |
| `src/eytelwein/vdi_2341/` | `src/eytelwein/idler_design/` |

All contents move with the directory. Internal structure (`core/`, `extended/`, `data/`) is unchanged.

---

## 3. Directory Renames (tests)

| Old path | New path |
|---|---|
| `tests/test_din_22101/` | `tests/test_belt_conveyor_design/` |
| `tests/test_vdi_2341/` | `tests/test_idler_design/` |

All test files keep their names. Only the parent directory changes.

---

## 4. File Renames

| Old file | New file |
|---|---|
| `src/eytelwein/belt_conveyor_design/data/minimum_pulley_diameters_DIN_22101.csv` | `src/eytelwein/belt_conveyor_design/data/minimum_pulley_diameters.csv` |

---

## 5. CSV Column Renames

File: `src/eytelwein/belt_conveyor_design/data/minimum_pulley_diameters.csv`

| Old column name | New column name |
|---|---|
| `D_Tr_as_per_equation_80_mm` | `reference_diameter_mm` |

---

## 6. Import Path Changes (for convexus find-and-replace)

### din_22101 → belt_design

Every import like:
```python
from eytelwein.din_22101.core.volume_flow_mass_flow import usable_belt_width
from eytelwein.din_22101.extended.design_layout_of_drive_system import mechanical_torque_from_belt_force
from eytelwein.din_22101.constants import IdlerSets
from eytelwein.din_22101 import usable_belt_width
from eytelwein import din_22101
```

Becomes:
```python
from eytelwein.belt_conveyor_design.core.volume_flow_mass_flow import usable_belt_width
from eytelwein.belt_conveyor_design.extended.design_layout_of_drive_system import mechanical_torque_from_belt_force
from eytelwein.belt_conveyor_design.constants import IdlerSets
from eytelwein.belt_conveyor_design import usable_belt_width
from eytelwein import belt_conveyor_design
```

### vdi_2341 → idler_loads

Every import like:
```python
from eytelwein.vdi_2341.core.idler_rolls import load_factor_determining_idler_roll_load_due_to_material
from eytelwein.vdi_2341 import load_factor_determining_idler_roll_load_due_to_material
from eytelwein import vdi_2341
```

Becomes:
```python
from eytelwein.idler_design.core.idler_rolls import load_factor_determining_idler_roll_load_due_to_material
from eytelwein.idler_design import load_factor_determining_idler_roll_load_due_to_material
from eytelwein import idler_design
```

### Attribute access

| Old | New |
|---|---|
| `eytelwein.din_22101.some_function()` | `eytelwein.belt_conveyor_design.some_function()` |
| `eytelwein.vdi_2341.some_function()` | `eytelwein.idler_design.some_function()` |

---

## 7. `__init__.py` Export Changes

### `src/eytelwein/__init__.py`

| Old export | New export |
|---|---|
| `from . import din_22101` | `from . import belt_conveyor_design` |
| `from . import vdi_2341` | `from . import idler_design` |
| `"din_22101"` in `__all__` | `"belt_conveyor_design"` in `__all__` |
| `"vdi_2341"` in `__all__` | `"idler_design"` in `__all__` |

Docstring: remove all mentions of "DIN 22101" and "VDI 2341". Describe modules by engineering domain only.

### `src/eytelwein/belt_conveyor_design/__init__.py` (was `din_22101/__init__.py`)

All internal imports change prefix:
```
from eytelwein.din_22101.core.X  →  from eytelwein.belt_conveyor_design.core.X
from eytelwein.din_22101.extended.X  →  from eytelwein.belt_conveyor_design.extended.X
from eytelwein.din_22101.constants  →  from eytelwein.belt_conveyor_design.constants
```

### `src/eytelwein/idler_design/__init__.py` (was `vdi_2341/__init__.py`)

```
from eytelwein.vdi_2341.core.idler_rolls  →  from eytelwein.idler_design.core.idler_rolls
```

---

## 8. Docstring Standard-Reference Removals

Across ALL `.py` files, remove or replace these patterns:

| Pattern to find | Replacement |
|---|---|
| `according to DIN 22101` | _(delete phrase or replace with "for belt conveyor systems")_ |
| `per DIN 22101` | _(delete phrase)_ |
| `DIN 22101-3` | _(delete reference)_ |
| `DIN 22101` | _(delete reference)_ |
| `according to VDI 2341` | _(delete phrase or replace with "for idler roll loading")_ |
| `per VDI 2341` | _(delete phrase)_ |
| `VDI 2341` | _(delete reference)_ |
| `equation_80` | `reference_diameter` (in CSV column context) |
| `"based on established standards including DIN 22101 and VDI 2341"` | `"based on established engineering methodologies"` |
| `"Belt conveyor calculations according to DIN 22101 standard"` | `"Belt conveyor design calculations"` |
| `"Idler roll calculations according to VDI 2341 standard"` | `"Idler roll load calculations"` |

---

## 9. Function Names — NO CHANGES

All function names are already domain-generic. No renames needed:

- `usable_belt_width` — keeps name
- `gradient_resistance` — keeps name
- `minimum_diameter_of_group_A_pulleys` — keeps name (A/B/C are engineering classifications)
- `load_factor_determining_idler_roll_load_due_to_material` — keeps name
- All 150+ public functions — keep names

---

## 10. Enum/Constant Names — NO CHANGES

All enum names describe engineering concepts, not standards:

- `PulleyGroups` (A, B, C) — universal engineering classification
- `MinimumPulleyDiameterCoefficient` (B, P, E, St) — belt material codes
- `PulleyLoadFactor` — percentage-based load ranges
- `IdlerSets` (FLAT_TROUGH, V_TROUGH, etc.) — geometry descriptors
- `BeltCoverCharacteristicsAssessments` — quality tiers
- `CoefficientMinimumTransitionLength` (EP, ST) — material type coefficients
- `BeltCarcassType` (TEXTILE, STEEL_CORD) — material type
- `STANDARD_GRAVITY` — physics constant, not standard-specific

---

## 11. Private Implementation Renames (parameters, docstring formulas, comments)

### 11a. Parameter name renames (actual code identifiers)

| File | Old parameter name | New parameter name |
|---|---|---|
| `extended/_volume_flow_mass_flow.py` | `equivalent_slope_angle_DIN22101_rad` | `slope_angle_rad` |
| `extended/_volume_flow_mass_flow.py` | `surcharge_angle_ISO5048_rad` | `surcharge_angle_rad` |
| (public wrapper too) | same pattern | same rename |

### 11b. Greek letter replacements in docstring formulas

| Old | New | Context |
|---|---|---|
| `λ` | `troughing_angle` | belt trough geometry |
| `β` | `slope_angle` | conveyor inclination |
| `α` | `wrap_angle` | belt wrap on pulley |
| `ρ` | `bulk_density` | material density |
| `μ` | `friction_coefficient` (qualify per friction pair, e.g. `friction_belt_pulley`, `friction_chute_material`) | friction |

### 11c. DIN 22101-specific formula abbreviations in docstrings

These appear in docstring math formulas (primarily in `core/_resistance_and_power_for_steady_operations.py`):

| Old | New | Meaning |
|---|---|---|
| `F_Sch` | `chute_resistance_force` | friction resistance at skirting/chute |
| `c_Rank` | `rankine_factor` | Rankine earth pressure coefficient |
| `b_Sch` | `chute_width` | skirting board width |
| `l_Sch` | `chute_length` | skirting board length |
| `I_m` | `mass_flow` | material mass flow rate |
| `μ₂` | `friction_between_chute_and_conveyed_material` | chute-material friction coefficient |
| `q_B` | `line_load_belt` | belt linear mass (already the parameter name) |
| `q_G` | `line_load_material` | material linear mass (already the parameter name) |

### 11d. NO CHANGES — keep as-is

- **Grimmer & Kessler (Teil I/II)** — scientific publication reference, not a copyrighted standard. Keep.
- **`F_St`, `F_w`** — these do not appear as code identifiers, only in docstring math if at all
- **`m'G`, `m'L`** — same, docstring-only and mapped to English parameter names already

---

## Quick Reference: Regex Patterns for convexus migration

```
# Module path renames (Python imports)
s/eytelwein\.din_22101/eytelwein.belt_conveyor_design/g
s/eytelwein\.vdi_2341/eytelwein.idler_design/g

# Bare module references (import statements, __all__)
s/\bdin_22101\b/belt_conveyor_design/g
s/\bvdi_2341\b/idler_design/g

# Docstring standard references (review each match)
s/according to DIN 22101//g
s/per DIN 22101//g
s/DIN 22101-3//g
s/DIN 22101//g
s/according to VDI 2341//g
s/per VDI 2341//g
s/VDI 2341//g
```
