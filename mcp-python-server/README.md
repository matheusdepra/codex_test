# MCP Python Server

A fully working [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server written in Python. The server exposes a handful of safe, high-value tools that allow Large Language Models (LLMs) or other MCP clients to inspect the filesystem, edit files, execute controlled commands, and bootstrap sample projects from templates.

## What is the Model Context Protocol?

The Model Context Protocol defines a standard way for tools, data sources, and LLMs to communicate. MCP servers expose *tools* that can be invoked by clients. Tools are described by JSON schemas and support streaming results over a WebSocket transport. The protocol allows LLMs to explore environments, call domain-specific functions, and share session state in a controlled manner.

This repository provides a small but complete MCP server you can use locally while experimenting with Codex, Claude, or any MCP-compatible orchestrator.

## Project Layout

```
mcp-python-server/
├── src/
│   ├── server.py            # Entry point and tool registration
│   ├── tools/
│   │   ├── filesystem.py    # Read/write/list filesystem helpers
│   │   ├── executor.py      # Safe command execution utilities
│   │   └── templates.py     # Project template management
│   └── utils/
│       └── __init__.py
├── templates/               # Ready-to-copy project templates
│   ├── fastapi-basic/
│   ├── express-basic/
│   └── readme-sample/
├── pyproject.toml           # Python package metadata
├── mcp.json                 # MCP server manifest for Codex/Claude
└── README.md
```

## Requirements

- Python 3.10+
- The [`mcp`](https://pypi.org/project/mcp/) reference SDK (installed automatically via `pip`)
- Optional: `fastapi` and `uvicorn` when working with the FastAPI template

Install dependencies in editable mode:

```bash
pip install -e .
```

## Running the server locally

1. Clone this repository or copy the `mcp-python-server` directory to your workspace.
2. Install dependencies: `pip install -e .`
3. Start the server:

   ```bash
   python -m src.server
   ```

   The server binds to a standard MCP transport and waits for a client connection. Logs are emitted to standard output for easy debugging.

## Registering the server with Codex or Claude

### Codex

1. Open the Codex client and navigate to **Settings → MCP Servers**.
2. Click **Add MCP Server** and select **Python**.
3. Provide the path to the project and use the command from `mcp.json`:

   ```
   python -m src.server
   ```
4. Save the configuration. Codex will spawn the process and connect via MCP.

### Claude Desktop (or any other compatible LLM)

1. Open the Claude client, go to **Settings → Tools → Model Context Protocol**.
2. Add a new server configuration, again pointing to `python -m src.server` as the launch command.
3. Claude will connect to the running server whenever the workspace is active.

## Available Tools

### Filesystem Tools

| Tool | Description |
| ---- | ----------- |
| `read_file(path)` | Returns the UTF-8 contents of the file. |
| `write_file(path, content)` | Creates or replaces the file with the given content. |
| `update_file(path, content)` | Updates existing files by replacing their contents. |
| `list_directory(path)` | Returns a sorted listing of names in the directory. |

### Command Executor Tools

| Tool | Description |
| ---- | ----------- |
| `run_command(cmd)` | Runs a whitelisted command (`python`, `pip install`, `pip list`, `ls`). Returns stdout, stderr, and the exit code. |

### Template Tools

| Tool | Description |
| ---- | ----------- |
| `create_project_template(name, destination)` | Copies the contents of a template directory into the destination folder. |

## Testing each tool manually

You can call each tool directly using the MCP client of your choice. The examples below use pseudo payloads to illustrate the expected inputs/outputs.

1. **Read a file**

   ```json
   {
     "tool": "read_file",
     "arguments": {"path": "README.md"}
   }
   ```

2. **Write a file**

   ```json
   {
     "tool": "write_file",
     "arguments": {"path": "notes/todo.txt", "content": "Initial TODO list"}
   }
   ```

3. **Update a file**

   ```json
   {
     "tool": "update_file",
     "arguments": {"path": "notes/todo.txt", "content": "Updated content"}
   }
   ```

4. **List a directory**

   ```json
   {
     "tool": "list_directory",
     "arguments": {"path": "."}
   }
   ```

5. **Run a command**

   ```json
   {
     "tool": "run_command",
     "arguments": {"cmd": ["python", "--version"]}
   }
   ```

6. **Copy a template**

   ```json
   {
     "tool": "create_project_template",
     "arguments": {"name": "fastapi-basic", "destination": "./my-fastapi-app"}
   }
   ```

## Creating new tools

1. Add a new Python module or function under `src/tools/`.
2. Expose it through the server in `src/server.py` using the `@server.tool()` decorator from `FastMCP`.
3. Provide input validation and logging similar to the existing tools.
4. Update this README with usage instructions to help future users.

## Security considerations and limitations

- **Whitelisted commands only.** The executor tool denies any command that does not start with the allowed prefixes (`python`, `pip install`, `pip list`, `ls`). No shell expansion or destructive operations are permitted.
- **Explicit file writes.** Files are always written using UTF-8 and the parent directories are automatically created when necessary.
- **No network reachability guarantees.** If the server or templates require network access (e.g., installing packages), ensure your environment allows it.
- **Logging.** Basic logging is enabled to trace tool usage. Avoid storing secrets in log output.
- **Templates are static.** Template copying simply replicates directory structures—there is no templating engine or variable substitution.

## Extending the server

- Add additional templates by creating new directories inside `templates/`.
- Introduce new MCP tools by augmenting the `MCPServer` class.
- Wrap additional transports (HTTP, WebSocket) by building on the `FastMCP` helper from the `mcp` Python SDK.

With these building blocks, you can use Codex (or another MCP-aware assistant) to scaffold entire projects, manage files, and run quick commands entirely through the Model Context Protocol interface.
