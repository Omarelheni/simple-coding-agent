# Mini Coding Agent

A small interactive Python coding agent that uses Groq for language-model responses and an MCP server to expose workspace tools. The agent can inspect and edit files, run tests and permitted commands, and check Git status.

## Requirements

- Python 3.10 or newer
- A Groq API key

## Setup

Create and activate a virtual environment from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the runtime packages:

```bash
pip install groq python-dotenv mcp pytest
```

Create a `.env` file in the repository root with the following values:

```dotenv
GROP_API_KEY=your_groq_api_key
MODEL_NAME=your_groq_model_name
```

The client currently reads the API key from `GROP_API_KEY` (spelled exactly as shown) and requires `MODEL_NAME`. Keep `.env` private; it is excluded from Git.

## Run

From the repository root, start the interactive agent:

```bash
python -m app.main
```

Enter a coding task at the prompt. Enter `exit` to quit. The tool dispatcher displays a confirmation prompt before file writes. The current denial handling should not be relied on as a security boundary; review the implementation before using this agent with sensitive files.

## Workspace and tools

The agent's file operations and command execution are scoped to the `workspace/` directory. Available tools include:

- List, read, and write workspace files
- Run tests
- Check Git status

File paths are checked to prevent access outside the workspace. The command runner, when used, restricts executables to `python`, `pytest`, `ruff`, and `git`, and runs commands without a shell and with a time limit. File writes trigger an interactive confirmation prompt, but the current denial handling is not a reliable safeguard.

## Tests

Run the repository tests from the repository root:

```bash
pytest -q
```

## Project layout

- `app/agent/` — agent loop, state, and system instructions
- `app/llm/` — Groq client integration
- `app/mcp_client/` — MCP client connection
- `app/mcp_server/` — filesystem, testing, and Git tools
- `app/security/` — workspace path checks and command restrictions
- `app/tools/` — tool schemas and dispatch
- `tests/` — project tests
- `workspace/` — files exposed to the agent

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE).
