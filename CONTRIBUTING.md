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

4. **Handling Branches**
    - After you've selected a feature to work on, create a branch in your local repo
        ```powershell
        git checkout -b "new_branch"
        ```
    - Run following command to integrate the pre-commit hook
        ```powershell
        pre-commit install
        ```
        Make sure that always all hooks are passed and no errors are raised
    - Pull down the main branch from the remote repository to get the most up to date changes
        ```powershell
        git pull origin main
        ```
    - Merge the latest main branch changes into your feature branch
        ```powershell
        git merge main
        ```
        Resolve all merging conflicts if any occur
    - When your feature is complete, push your branch to the remote repository
        ```powershell
        git push origin new_branch
        ```
    - Create a pull request to merge your feature branch into the main branch through your repository's web interface (Azure DevOps, GitHub, etc.)

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

In Azure DevOps, go to Pipelines and click on new Pipeline. Choose your Code
location (In this Case Azure Repos Git). Click on the repo you want to create a
Pipeline for. If your azure-pipelines.yml is already in your Repo it should be
detected automatically. Otherwise choose "Create Pipeline from existing .yml" and give the path to your .yml file.

Click on run to finish the setup.


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
