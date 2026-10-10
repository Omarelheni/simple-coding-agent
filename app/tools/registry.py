import json

from ..mcp_server.filesystem import read_file, list_files, write_file
from app.security.commands import run_command
import asyncio
from ..mcp_server.testing import run_tests
from app.mcp_client.client import MCPClient

READ_ONLY_TOOLS = {
    "list_files",
    "read_file",
}

WRITE_TOOLS = {
    "write_file",
}

TOOL_DEFINITIONS = {
    "read_file": {
        "description": "Reads the content of a file relative to the workspace root.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file relative to the workspace root.",
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
    "list_files": {
        "description": "Lists all files in a directory relative to the workspace root.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": (
                        "Lists files in a directory. "
                        "The argument must be named 'path'. "
                        "Use '.' to list the workspace root."
                    ), 
                }
            },
            "required": ["path"],
            "additionalProperties": False,
        },
    },
    "write_file": {
        "description": "Writes content to a file relative to the workspace root.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file relative to the workspace root.",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file.",
                },
            },
            "required": ["path", "content"],
            "additionalProperties": False,
        },
    },
    "run_tests": {
        "description": "Runs tests in the workspace.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
    "git_status": {
        "description": "Returns the status of the git repository in the workspace.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
    "run_command_line": {
        "description": "Executes a command line command and returns its output.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "The command to execute as a list of strings. "
                        "you can use the command line tool to run allowed commands. "
                        "allowed commands are: python, pytest, ruff, git. "
                        "For example, ['ls', '-la']."
                    ),
                }
            },
            "required": ["command"],
            "additionalProperties": False,
        },
    },

}

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": name,
            "description": definition["description"],
            "parameters": definition["parameters"],
        },
    }
    for name, definition in TOOL_DEFINITIONS.items()
]


async def execute_tool(mcp_client: MCPClient, tool_name: str, arguments: dict | str | None):

    if arguments is None:
        arguments = {}
    elif isinstance(arguments, str):
        arguments = json.loads(arguments) if arguments.strip() else {}

    if not isinstance(arguments, dict):
        raise ValueError(f"Tool arguments for '{tool_name}' must be a JSON object.")

    if tool_name in READ_ONLY_TOOLS:
        print(f"Executing read-only tool '{tool_name}' with arguments: {arguments}")
    elif tool_name in WRITE_TOOLS:
        response = ask_user_for_approval()
        if response in ("no", "n"):
            raise PermissionError(f"User denied permission to execute write tool '{tool_name}'.")
    
    return await mcp_client.call_tool(tool_name, arguments)


def ask_user_for_approval():
    approval = input("Do you approve the changes? (yes/no): ")
    return approval.lower() == "yes"

