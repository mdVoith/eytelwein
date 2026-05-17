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

2. Install pre-commit hooks:
    ```powershell
    uv run pre-commit install
    ```

3. Run tests:
    ```powershell
    uv run pytest
    ```

4. Run linting and formatting:
    ```powershell
    uv run ruff check --fix src/ tests/
    uv run ruff format src/ tests/
    ```

5. Run type checking:
    ```powershell
    uv run mypy src/
    ```

6. Commit using [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/):
    ```powershell
    git commit -m "feat: add new calculation for X"
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
     uv run MYAPP.py
    ```
UV will then create a new ".venv"-folder with a new virtual enviroment and will install all dependencies according to the "pyproject.toml" configuration file of your application.
Once installed, UV will go on running your app. Afterwards, you can repeat the above command to re-run the app.
