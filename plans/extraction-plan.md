# Eytelwein Open-Source Extraction Plan

## Phase 1: Fresh Repo Setup — COMPLETE

| Task | Status | Notes |
|------|--------|-------|
| Copy `src/eytelwein/` (58 files) | Done | |
| Copy `tests/` (44 files) | Done | |
| Fix `din_22101/constants.py` import from `domain` | Done | Changed to `eytelwein.main.units` |
| Remove cross-repo test `test_constants_consistency` | Done | Tested against convexus `domain` |
| `pyproject.toml` — name=eytelwein, deps | Done | Added numpy, pint, scipy |
| Apache-2.0 LICENSE | Done | |
| README.md | Done | |
| **1458 tests pass** | Done | |

### Discovered: `scipy` dependency
`eytelwein.main.constants` uses `scipy.constants` for physical constants (gravity).
Added `scipy>=1.15.0` to dependencies.

---

## Phase 2: Cleanup — COMPLETE

### Files DELETED

| File | Reason | Status |
|------|--------|--------|
| `src/eytelwein/din_22101/conveyor_belt.py` | Empty file, 0 bytes. No code imports it. | DELETED |
| `src/eytelwein/din_22101/README.md` | Empty, 0 bytes | DELETED |
| `src/eytelwein/vdi_2341/README.md` | Empty, 0 bytes | DELETED |
| `src/eytelwein/din_22101/calculations.toml` | Convexus dependency-graph manifest. No code in eytelwein references it. | DELETED |
| `src/eytelwein/examples/` | `units_example.py` had fake hardcoded results, no educational value. | DELETED |
| `src/eytelwein/utils/performance.py` | YAGNI plugin registry, zero actual registrations. Consumers updated to use standard impl directly. | DELETED |
| `src/eytelwein/utils/` | Empty after performance.py removal. No remaining references. | DELETED |
| `src/eytelwein/din_22101/CONTRIBUTING.md` | Duplicate of root CONTRIBUTING.md | DELETED |
| `src/eytelwein/vdi_2341/CONTRIBUTING.md` | Duplicate of root CONTRIBUTING.md | DELETED |
| `job--build-exe.yml` | PyInstaller exe build, not relevant for library | DELETED |
| `job--change-log.yml` | Replaced by ci-post-merge.yml | DELETED |
| `run_pip-compile_ci.py` | Not needed with uv | DELETED |
| `docs/build/` | Stale Sphinx build artifacts for old eytelwein_export | DELETED |

### Files UPDATED

| File | Changes |
|------|---------|
| `CONTRIBUTING.md` | Rewritten for standalone OSS library |
| `.pre-commit-config.yaml` | Updated hook versions, removed pip-compile hook |
| `ci-pr.yml` | Uses uv, removed requirements.txt refs, removed coverage |
| `ci-post-merge.yml` | Removed requirements.txt path, limited to py3.13 |
| `job--pre-commit.yml` | Uses uv instead of pip |
| `docs/source/conf.py` | Fixed project name and copyright |

`high_performance` parameter removed from 6 function signatures + 3 tests removed.
**1455 tests pass after full cleanup.**

### Remaining FLAG

| File | Issue | Action |
|------|-------|--------|
| `src/eytelwein/din_22101/data/minimum_pulley_diameters_DIN_22101.csv` | **COPYRIGHT RISK**: CSV lookup table derived from DIN 22101 standard. Column names reference "equation_80" from the standard text. Publishing verbatim standard data tables may infringe copyright. Also: CSV format is fragile (semicolon-delimited). | **FLAG — decision needed before Phase 4 (publish)**: (a) remove entirely and compute from formulas, (b) replace with generalized data, (c) legal review before publishing |

---

## Phase 3: Standards Decoupling (Option C — Hybrid) — PENDING

**Goal**: Remove all references to copyrighted standards (DIN 22101, VDI 2341) from
module names and docstrings. Function names, enum names, and private variables are
already domain-generic and stay unchanged.

**Reference**: [`plans/renaming-map.md`](renaming-map.md) — full mapping of every rename.

### Step 3a: Rename directories

| Old | New |
|---|---|
| `src/eytelwein/din_22101/` | `src/eytelwein/belt_conveyor_design/` |
| `src/eytelwein/vdi_2341/` | `src/eytelwein/idler_design/` |
| `tests/test_din_22101/` | `tests/test_belt_conveyor_design/` |
| `tests/test_vdi_2341/` | `tests/test_idler_design/` |

### Step 3b: Fix all import paths

- `eytelwein.din_22101` → `eytelwein.belt_conveyor_design` (in all `__init__.py`, source, and test files)
- `eytelwein.vdi_2341` → `eytelwein.idler_design` (in all `__init__.py`, source, and test files)
- Run full test suite after

### Step 3c: Rename CSV file + column

- `minimum_pulley_diameters_DIN_22101.csv` → `minimum_pulley_diameters.csv`
- Column `D_Tr_as_per_equation_80_mm` → `reference_diameter_mm`
- Update all code that reads this CSV

### Step 3d: Strip docstring standard references

- Remove all "according to DIN 22101", "per VDI 2341", "DIN 22101-3", equation references
- Update root `__init__.py` docstring
- Run full test suite after

### Step 3e: Validate

- `uv run pytest tests/` — all tests pass
- `uv run ruff check src/` — no lint issues
- `uv run mypy src/` — no type errors
- Manual review of `renaming-map.md` — all items addressed

---

## Phase 4: Publish to GitHub + PyPI

- Create public GitHub repo
- Add GitHub Actions CI (pytest, ruff, mypy on py3.13)
- Add PyPI publish workflow (on tag push)
- Tag v0.1.0
- Publish

---

## Phase 5: Switch Convexus

- Add `eytelwein>=0.1.0` to convexus dependencies
- Remove `src/eytelwein/` from convexus
- Update all imports in domain using `plans/renaming-map.md` as reference
- Single PR

---

## Phase 6: Cleanup

- Copy `plans/renaming-map.md` into convexus repo (for reference during switchover)
- Delete `plans/renaming-map.md` from eytelwein repo
- Delete `plans/extraction-plan.md` from eytelwein repo (extraction is complete)
- Commit cleanup

---

## Key Constraints

- No early rounding in calculation code
- Quantity-only API (Pint Quantity in/out, never bare floats)
- Private/public function pattern: `_foo.py` (bare math) + `foo.py` (Quantity-wrapped)
- `uv run` for all commands
- Windows-first dev (PowerShell)
- No project-management terms in code identifiers
