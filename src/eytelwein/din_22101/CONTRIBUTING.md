# Operating System
We recommend developing on Windows 10 or Windows 11. If you are using a different operating system, you may need to adjust some of the instructions in this guide.

# IDE: VS Code
We recommend using Visual Studio Code as your IDE. It is a lightweight, open-source code editor that is available on all platforms. You can download it from https://code.visualstudio.com/.

This script will set up your development environment for VSCode by default, but you can opt-out during CLI setup.

# Python best-practices

This guide follows the advice given in this blog post: https://www.stuartellis.name/articles/python-modern-practices/

# Managing Python Installations
## Install Pyenv

1. Purpose:
    - Pyenv is primarily focused on managing multiple Python versions.
2. Features:
    - Allows you to easily switch between multiple versions of Python. Integrates well with virtual environments.
    - Simple and lightweight, mainly for Python version management.
3. Usage:
    - Install and manage different Python versions.
    - Set global and local Python versions for projects.

To install pynev run:
```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "$([System.Environment]::GetFolderPath('UserProfile'))\install-pyenv-win.ps1"; & "$([System.Environment]::GetFolderPath('UserProfile'))\install-pyenv-win.ps1"
```
Use this command also for updating pyenv, however, there is a command to update pyenv "officially". It is very slow.

```powershell
pyenv update
```
## Install Python and dependency management

Install the below version of python and define it as your global enviroment (run both commands):

```powershell
pyenv install 3.13.1
pyenv global 3.13.1
```

Insure the right Python version is installed

```powershell
python --version
```

Install pipx for globally installed tools and applications that are not specific to a single project.

```powershell
python -m pip install pipx
 ```

Then install uv into your global python enviroment as standard dependencie manager.

```powershell
python -m pipx install uv
```

To set uv globaly run (You may need to close and reopen the powershell for pipx to be found):

```powershell
pipx ensurepath
```

If any command should not be found although you installed the package, make sure the right PATH to the package is set in your User Enviroment variables: `https://www.computerhope.com/issues/ch000549.htm`.
See also Chapter Trouble Shooting.

# Use Git
Make sure git is installed on your PC correctly and you are loged in with your account

1. **Install git**:

    - Download the git installer from `https://git-scm.com/downloads`
    - Run the installer and follow the setup instructions
    - Select the default options unless you have specific preferences.
    Verify the installation by opening **Powershell** and running:
        ```powershell
        git --version
        ```

2. **Configure git**:
    - Configure your username and email in the Powershell:
        Example:
        ```Powershell
        git config --global user.name "Your Name"
        git config --global user.email "your.email@example.com"
        ```
    - To check your configuration settings, run:
        ```Powershell
        git config --list
        ```
    - Set global default branch name to main (optional, this is already the default for new versions of git):
        ```Powershell
        git config --global init.defaultBranch main
        ```
3. **Download git extension in VS-Code**:
    - In VS-Code go to extenstion (Ctrl+Shift+X) and install search git
    - Install the git extension pack

# Development Process
This guide will help you understand the standards and practices we follow to ensure high-quality code and efficient collaboration. Please read through the following guidelines carefully before contributing to the project.

1.  **PEP 8 - Style Guide**
    - follow the suggested Style Guide for coding defined in PEP 8 `https://peps.python.org/pep-0008/`
    - e. g. do not submit comments that are not relevant to the project (unused Code, unnecessary hints/comments)

2.  **UV for python Managing**
    - use uv to manage your project and its dependencies

    - make sure to always stay in .venv created for this project. To activate the .venv run:

        ```powershell
        .venv/Scripts/activate
        ```
        be sure to be in the root of your Project when running this command
    - to add dependencies to your pyproject.toml run

        Example:
        ```powershell
        uv add your_dependency
        ```
    - use uv to also execute your code

        Example:
        ```powershell
        uv run path/to/your/code.py
        ```

3.  **Language Syntax**
    - use type hints in your Code
    - use data-classes for data validation
    - Format Strings with f-strings

4.  **Code-formatting**
    - use ruff to check your Code's formatting and quality
        ```powershell
        uv run ruff check --fix --unsafe-fixes
        uv run ruff format
        ```

5.  **Test with Pytest**
    - use pytest to test your code
        ```powershell
        uv run pytest
        ```

6.  **Usage of git and pre-commit hook**
    - be sure to always pull and fetch your code before contributing. that way you ensure to be working on the newest version
        ```powershell
        git pull
        git fetch
        ```

    - regularly stage, commit and push your changes to have version control over your Code

        Example:
        ```powershell
        git add .
        git commit -m "Your commit Message"
        git push
        ```

    - to check your code a pre-commit hook is used to ensure the quality of your Code before every commit. The pre-commit hook checks:
        - Language Syntax using pytest
        - your Code formatting and linting using ruff
        - your Typehints using mypy

7.  **CI/CD-Pipeline**
    - a CI-Pipeline is used to check the quality of your Code, run the tests from the pre-commit hook again and also package
    - a CD-Pipeline is used to build and deploy your code.
    - The pipelines get triggered with every push to the main branch of your repo.

8. **Versioning**
    - The versioning for the repo code is done by the CI/CD Pipeline following the standardized versioning after SemVer (MAJOR.MINOR.PATCH).
    - Use standardized commit messages to ensure correct versioning.
         Example:
        ```powershell
        git commit -m "fix: Removed bug" (bumps PATCH)
        git commit -m "feat: Added small feature" (bumps MINOR)
        git commit -m "BREAKING CHANGE: Introduced new breaking change" (bumps MAJOR)
        ```
        Also see `https://www.conventionalcommits.org/en/v1.0.0/`

        | Type               | Description                              | Version Bump             |
        | ------------------ | ---------------------------------------- | ------------------------ |
        | `fix:`             | Bug fix                                  | **PATCH** (0.0.x → 0.0.x+1) |
        | `perf:`            | Performance improvement                  | **PATCH**                 |
        | `chore:`           | Maintenance (tooling, dependencies)      | **PATCH**                 |
        | `test:`            | Adding or modifying tests                | **PATCH**                 |
        | `ci:`              | Changes to CI/CD pipelines               | **PATCH**                 |
        | `refactor:`         | Code refactoring (no behavior change)     | **PATCH**                 |
        | `docs:`            | Documentation update                     | _No bump_                 |
        | `style:`            | Code style changes                       | _No bump_                 |
        | `feat:`            | Introduces a new feature                  | **MINOR** (0.x.0 → 0.x+1.0) |
        | `BREAKING CHANGE:` or `feat!:` | Backward-incompatible change               | **MAJOR** (x.0.0 → x+1.0.0) |
        | `revert:`           | Reverts a previous commit                | _No bump_                 |


# Setting Up CI/CD

To run the CI/CD Pipeline for every push and have continuous versioning of your code in a changelog, you need to set up a pipeline in Azure for every repo.

Also, ensure that your Project Build Service has the permission to contribute, contribute to pull requests, and create branches.

![alt text](images/image.png)

# Troubleshooting
## Python version mismatch

Check that the global installation of uv is not managing python versions on your machine. List all managed python versions (change USERNAME):

```powershell
dir %APPDATA%\uv\python
```
and delete them with
```powershell
uv python uninstall PYTHONVERSION
```

## Pyenv, pipx, uv or git not found
If pyenv, pipx, uv or git is not found in the PowerShell although it is already installed.

- Close and reopen the PowerShell (if in Windows PowerShell)
- Press Ctrl + Shift + P and type Reload Window (if in VS Code)

If still not found, check your Windows PATH Environment variables and add the path to the User Environment Variables manually

 (Guide to set PATH variables: `https://www.computerhope.com/issues/ch000549.htm`)

Locations of the Packages to add to PATH after following the installation guide:
- pyenv: C:\Users\your_user\.pyenv\pyenv-win\
- pipx: C:\Users\your_user\.pyenv\pyenv-win\versions\3.13.1\Scripts\pipx.exe
- uv: C:\Users\your_user\pipx\venvs\uv\Scripts\

## Error: Python or dependency not installed
There may be a mixup of legacy python versions, system's python versions or virtual environments. However, UV is able to fix this automatically:
- Delete the ".venv" folder.
- Run:
    ```powershell
     uv run MYAPP.py
    ```
UV will then create a new ".venv"-folder with a new virtual enviroment and will install all dependencies according to the "pyproject.toml" configuration file of your application.
Once installed, UV will go on running your app. Afterwards, you can repeat the above command to re-run the app.


# DIN 22101 Library Structure and Design

The DIN 22101 library implements calculations according to the DIN 22101 standard for belt conveyor design. Understanding its structure and design principles is essential for effective contributions.

## Core vs Extended Functionality

The library is organized into two main modules:

### Core Module (`din_22101/core/`)

The core part of the library offers all equations and functionality which is directly present in the DIN 22101 standard. It also includes direct derivatives of these functions. For example:

- An equation like `b = B - 250 mm` for calculating the usable belt width can be found inverted to get the belt width `B` from the known usable belt width (`B = b + 250 mm`).
- Functions are closely named according to the definitions in the "Symbols and units" section of DIN 22101.
- When numerical methods (like optimization) are utilized to solve an inverse problem (e.g., determining the usable belt width from a given cross section), the function is prefixed with `solve_for_`.
- Core functionality also includes concepts not explicitly defined in the standard's text but easily determined from other equations (like belt edge, which is the difference between belt width and usable belt width divided by two).

### Extended Module (`din_22101/extended/`)

Extended functionality builds upon core calculations to provide:

- Higher-level composite functions combining multiple core calculations
- Alternative calculation methods and interpretations
- Convenience functions for common industry applications
- Functions that may incorporate values or methods from related standards
- Numerical solutions to complex interrelated equations

## Implementation Pattern

Each module follows a consistent implementation pattern:

1. **Private Implementation**: `_module_name.py` contains pure calculation functions with basic types
   - Example: `_volume_flow_mass_flow.py` implements the raw calculations
   - No unit handling
   - Validation: generally speaking there is no validation. However, if the standard DIN 22101 explicitly names restrictions on parameters, those validations and limit checks will be implemented in the private functions.
   - Functions prefixed with underscore (e.g., `_cross_section_of_fill`)

2. **Public Interface**: `module_name.py` wraps private functions with proper unit handling
   - Converts input units to standard units for calculation
   - Validates inputs
   - Validates physical integrity of results.
   - Wraps the private function result with proper units
   - Provides comprehensive docstrings
   - Example: `volume_flow_mass_flow.py` exports user-facing functions with Pint unit support

## Naming Conventions

- **Direct Calculations**: Named after the physical quantity being calculated
  - Example: `cross_section_of_fill`, `usable_belt_width`

- **Inverse Problems**: Prefix with `solve_for_` when using numerical methods
  - Example: `solve_for_used_belt_width_from_cross_section`

- **Unit Conversion**: Functions that convert between units or different standards
  - Example: `convert_surcharge_angles` between DIN 22101 and ISO 5048

## Standard Function Structure

Public functions typically follow this pattern:

```python
def function_name(param1: Quantity, param2: Quantity, unit: str = "default_unit", precision: int = 2) -> Quantity:
    """Comprehensive docstring with description, parameters, returns, and examples."""
    try:
        # 1. Convert inputs to standard units
        param1_std = param1.to(standard_unit1)
        param2_std = param2.to(standard_unit2)
    except Exception as e:
        raise ValueError(f"Error converting units: {e}")

    # 2. Validate inputs
    if param1_std.magnitude <= 0:
        raise ValueError("Parameter must be positive")

    # 3. Call private implementation
    result_std = (_function_name(param1_std.magnitude, param2_std.magnitude) *
                 standard_unit_result)

    # 4. First convert to requested output unit
    result = result_std.to(u.parse_units(unit))

    # 5. Then apply precision if specified
    if precision is not None:
        result = round(result, precision)

    return result
```

## Testing Approach

Each function should have corresponding tests in the `tests` directory that verify:

1. Correct calculation results against known values
2. Proper handling of edge cases
3. Appropriate error messages for invalid inputs
4. Unit conversion correctness

## Contribution Guidelines for DIN 22101

When adding new functionality:

1. Determine if it belongs in `core/` or `extended/` based on the principles above
2. Create both private and public implementations following the established pattern
3. Include comprehensive tests with valid test cases
4. Document the physical meaning and source of equations in docstrings
5. Follow the standard error handling and unit conversion pattern

When modifying existing functionality:

1. Ensure backward compatibility unless explicitly creating a breaking change
2. Update all affected tests
3. Document changes in docstrings and update function signatures as needed
