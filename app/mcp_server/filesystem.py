from pathlib import Path
from mcp.server.mcpserver import MCPServer

WORKSPACE = Path("workspace").resolve()

def read_file(path: str) -> str:
    """Reads the content of a file."""
    target = (WORKSPACE / path).resolve()
    if not target.is_relative_to(WORKSPACE):
        raise ValueError("Path is outside the workspace")
    if not target.is_file():
        raise FileNotFoundError(f"File not found: {target}")
    return target.read_text()

def list_files(path: str) -> list[str]:
    """Lists all files in a directory."""
    target = (WORKSPACE / path).resolve()
    if not target.is_relative_to(WORKSPACE):
        raise ValueError("Path is outside the workspace")
    if not target.is_dir():
        raise NotADirectoryError(f"Not a directory: {target}")
    return [str(p.relative_to(WORKSPACE)) for p in target.rglob('*') if p.is_file()]

def write_file(path: str, content: str) -> None:
    """Writes content to a file."""
    target = (WORKSPACE / path).resolve()
    if not target.is_relative_to(WORKSPACE):
        raise ValueError("Path is outside the workspace")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)

def run_tests() -> None:
    """Runs tests for the filesystem module."""
    # Test read_file
    write_file("test_dir/test_file.txt", "Hello, World!")
    assert read_file("test_dir/test_file.txt") == "Hello, World!"

    # Test list_files
    write_file("test_dir/file1.txt", "File 1")
    write_file("test_dir/file2.txt", "File 2")
    files = list_files("test_dir")
    assert set(files) == {"test_dir/test_file.txt", "test_dir/file1.txt", "test_dir/file2.txt"}

    # Test write_file
    write_file("test_dir/new_file.txt", "New File Content")
    assert read_file("test_dir/new_file.txt") == "New File Content"

    print("All tests passed.")



def register_filesystem_tools(mcp: MCPServer):
    """Registers filesystem tools with the MCP server."""
    mcp.tool()(read_file)
    mcp.tool()(write_file)
    mcp.tool()(list_files)