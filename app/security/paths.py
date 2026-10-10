from pathlib import Path

WORKSPACE = Path("workspace").resolve()

def resolve_path(path: str) -> Path:
    """Resolves a path relative to the workspace."""
    target = (WORKSPACE / path).resolve()
    if not target.is_relative_to(WORKSPACE):
        raise ValueError("Path is outside the workspace")
    return target