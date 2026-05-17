import os
import subprocess
import sys


def main():
    # Only run in CI. Locally the hook will exit successfully (no-op).
    if not os.environ.get("CI"):
        print("==> Skipping pip-compile locally (pip-compile runs only on CI).")
        sys.exit(0)

    candidates = []

    venv_exe = ".venv\\Scripts\\pip-compile.exe"
    if os.path.exists(venv_exe):
        candidates.append([venv_exe, "pyproject.toml", "-o", "requirements.txt"])

    candidates.append(
        [
            sys.executable,
            "-m",
            "piptools.scripts.compile",
            "pyproject.toml",
            "-o",
            "requirements.txt",
        ]
    )
    candidates.append(
        [
            sys.executable,
            "-m",
            "piptools.compile",
            "pyproject.toml",
            "-o",
            "requirements.txt",
        ]
    )
    candidates.append(["pip-compile", "pyproject.toml", "-o", "requirements.txt"])

    last_exc = None
    for cmd in candidates:
        try:
            print("==> Trying:", " ".join(cmd))
            result = subprocess.run(cmd, capture_output=True, text=True)
        except FileNotFoundError as exc:
            last_exc = exc
            print(f"==> Command not found: {cmd[0]}")
            continue

        output = (result.stdout or "") + (result.stderr or "")
        if result.returncode == 0:
            print(output)
            return

        print(output)
        sys.exit(result.returncode)

    print("Failed to find a working pip-compile command. Last error:")
    if last_exc:
        print(str(last_exc))
    sys.exit(2)


if __name__ == "__main__":
    main()
