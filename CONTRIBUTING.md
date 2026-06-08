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

Manual release (protected `main`):

Use this when you want to perform the release process yourself instead of the Release workflow.

1. Start from up-to-date `main` and create a temporary release branch:

```powershell
git fetch origin
git switch main
git pull --ff-only origin main
git switch -c release/tmp
```

2. Run Commitizen bump on the branch (choose PATCH, MINOR, or MAJOR):

```powershell
uv run --with commitizen cz bump --yes --increment PATCH
```

3. Read the bumped version and rename the branch to the canonical release name:

```powershell
$version = uv run --with commitizen cz version -p
$branch = "release/v$version"
git branch -m $branch
```

4. Push branch and tag (tag push triggers Publish to PyPI):

```powershell
git ls-remote --heads origin "$branch"
git ls-remote --tags origin "v$version"

# If this is a retry and the remote refs already exist from the same failed attempt,
# remove the stale release branch and tag before pushing again.
# Only do this if you are sure the refs are not needed anymore.
# git push origin --delete "$branch"
# git push origin ":refs/tags/v$version"

git push origin "HEAD:refs/heads/$branch"
git push origin "v$version"
```

5. Open a pull request back to `main` in the GitHub web UI:

```text
https://github.com/<owner>/<repo>/compare/main...release/v$version?expand=1
```

Use that compare page to create the PR with:
- Title: `chore(release): v$version`
- Body: `Manual release for v$version. Tag pushed and Publish to PyPI is running; merge this PR to land the version bump and changelog on main.`

6. Review and merge the release PR (merge or rebase preferred; avoid squash), then verify both Release/Publish results.

Notes:
- Do not push the bump commit directly to `main`; keep it on `release/vX.Y.Z` and merge via PR.
- This manual flow requires permission to push branches/tags and create pull requests.
- The `gh` CLI is optional; the web UI step above is the default documented path.
- If `git push origin "HEAD:refs/heads/$branch"` is rejected because `release/vX.Y.Z` already exists remotely, the branch is stale from a previous attempt. Delete the stale remote branch and tag for that version, then push again, or choose a new version if the tag has already been published.

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

Notes:
- `build:` is intentionally not used in this repository.
- Use `chore:` for packaging, build metadata, and distribution-configuration changes.
- The commit-msg hook rejects unsupported types so this stays consistent.

## Error: Python or dependency not installed
There may be a mixup of legacy python versions, system's python versions or virtual environments. However, UV is able to fix this automatically:
- Delete the ".venv" folder.
- Run:
    ```powershell
    uv sync
    ```
UV will then create a new ".venv" folder and install dependencies according to the "pyproject.toml" configuration.
Afterwards, rerun your original command (for example: `uv run pytest tests/ --tb=short`).
