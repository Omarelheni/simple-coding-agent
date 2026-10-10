
import subprocess
from pathlib import Path
from mcp.server.mcpserver import MCPServer

WORKSPACE = Path("workspace").resolve()

def run_tests():
    result = subprocess.run(
        ["pytest","-q"],
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
        timeout=30
    )
    return {
        "exist_code": result.returncode,
        "stdout": result.stdout[-10000:],
        "stderr": result.stderr[-10000:],
    }

def register_testing_tools(mcp: MCPServer):
    """Registers testing tools with the MCP server."""
    mcp.tool()(run_tests)