import subprocess
from pathlib import Path

WORKSPACE = Path("workspace").resolve()

ALLOWED_COMMANDS = {
    "python",
    "pytest",
    "ruff",
    "git",
}


def run_command(command: list[str]) -> dict:
    if not command:
        raise ValueError("Command cannot be empty.")

    if not isinstance(command, list) or not all(
        isinstance(arg, str) for arg in command
    ):
        raise ValueError("Command must be a list of strings.")

    executable = Path(command[0]).name

    if executable not in ALLOWED_COMMANDS:
        raise PermissionError(
            f"Command '{executable}' is not allowed."
        )

    try:
        result = subprocess.run(
            command,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=60,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Command timed out after 60 seconds.",
            "returncode": -1,
        }

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }