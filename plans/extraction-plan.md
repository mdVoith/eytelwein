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

## Phase 3: Renaming (if package name changes from `eytelwein`)

- Find-and-replace all `from eytelwein.` → `from <new_name>.`
- Rename `src/eytelwein/` → `src/<new_name>/`
- Update `pyproject.toml`
- Run full test suite after each rename batch

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
- Update all imports in domain
- Single PR

---

## Key Constraints

- No early rounding in calculation code
- Quantity-only API (Pint Quantity in/out, never bare floats)
- Private/public function pattern: `_foo.py` (bare math) + `foo.py` (Quantity-wrapped)
- `uv run` for all commands
- Windows-first dev (PowerShell)
- No project-management terms in code identifiers
