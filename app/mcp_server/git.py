import subprocess

from app.security.commands import run_command
from mcp.server.mcpserver import MCPServer


def git_status():
    return run_command(["git", "status","--short"])

def register_git_tools(mcp: MCPServer):
    """Registers git tools with the MCP server."""
    mcp.tool()(git_status)