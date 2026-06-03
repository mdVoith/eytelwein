# Contributing to eytelwein

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for dependency management
- Git

## Setup

```powershell
git clone <repo-url>
cd eytelwein
uv sync
```

## Development Workflow

1. Create a feature branch:
    ```powershell
    git checkout -b feat/your-feature
    ```

2. Run tests:
    ```powershell
    uv run pytest tests/ --tb=short
    ```

3. Run linting and formatting:
    ```powershell
    uv run ruff check src/ tests/
    uv run ruff format src/ tests/
    ```

4. Run type checking:
    ```powershell
    uv run mypy src/
    ```

5. Commit using [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/):
    ```powershell
    git commit -m "feat: add new calculation for X"
    ```

## CI, Docs, and Release Workflows

- CI workflow ([.github/workflows/ci.yml](.github/workflows/ci.yml)) runs on pull requests to `main` and pushes to `main`. It runs ruff, mypy, and pytest.
- Docs workflow ([.github/workflows/docs.yml](.github/workflows/docs.yml)) runs on pull requests, pushes to `main`, and manual dispatch.
  - Pull requests build docs only.
  - Pushes to `main` (and manual dispatch on `main`) also deploy docs to GitHub Pages.
- Release workflow ([.github/workflows/release.yml](.github/workflows/release.yml)) runs manually on `main` and uses Commitizen to bump version, update `CHANGELOG.md`, push a tag, and open a release pull request.
    - It pushes the `vX.Y.Z` tag (which triggers Publish) and opens a PR with the version + changelog bump for `main`. `main` stays protected; no bypass is required.
    - This workflow requires repository secret `RELEASE_PAT` (PAT with Contents and Pull requests write access).
- Publish workflow ([.github/workflows/publish.yml](.github/workflows/publish.yml)) runs only when a tag matching `v*` is pushed.
  - This means releases are tag-driven and do not happen on every PR or every merge.

## Releasing a New Version

1. Merge changes into `main` and ensure CI is green.
2. Trigger the Release workflow in GitHub Actions and select bump type (PATCH, MINOR, MAJOR).
3. The workflow runs Commitizen, pushes the `vX.Y.Z` tag (triggering Publish to PyPI), and opens a `release/vX.Y.Z` pull request.
4. Review and merge the release PR (preferably with a merge or rebase, not squash) to land the version bump and changelog on `main`.
5. Monitor the Release and Publish runs in GitHub Actions and verify the package on PyPI.

Manual fallback (if needed):

```powershell
uv run cz bump
git push origin vX.Y.Z
```

## Code Conventions

- **Quantity-only API**: public functions accept and return `pint.Quantity`, never bare floats
- **Private/public pattern**: `_foo.py` contains bare math, `foo.py` wraps it with unit handling
- **No early rounding**: preserve precision through calculation chains
- **Type hints**: required on all function signatures
- **PEP 8**: enforced via ruff

## Commit Message Types

| Type | Description | Version Bump |
|------|-------------|--------------|
| `fix:` | Bug fix | PATCH |
| `feat:` | New feature | MINOR |
| `feat!:` / `BREAKING CHANGE:` | Breaking change | MAJOR |
| `docs:` | Documentation | No bump |
| `refactor:` | Refactoring | PATCH |
| `test:` | Tests | PATCH |
| `ci:` | CI changes | PATCH |
| `chore:` | Maintenance | PATCH |

## Error: Python or dependency not installed
There may be a mixup of legacy python versions, system's python versions or virtual environments. However, UV is able to fix this automatically:
- Delete the ".venv" folder.
- Run:
    ```powershell
    uv sync
    ```
UV will then create a new ".venv" folder and install dependencies according to the "pyproject.toml" configuration.
Afterwards, rerun your original command (for example: `uv run pytest tests/ --tb=short`).
