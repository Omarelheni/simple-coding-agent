from mcp.server.mcpserver import MCPServer
from pathlib import Path
from .filesystem import register_filesystem_tools
from .testing import register_testing_tools
from .git import register_git_tools

WORKSPACE = Path("workspace").resolve()

mcp = MCPServer("coding-tools")

register_filesystem_tools(mcp)
register_testing_tools(mcp)
register_git_tools(mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")