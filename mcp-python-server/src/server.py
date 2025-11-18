"""Entry point for the sample MCP server.

This module wires all tools together using the ``FastMCP`` helper provided by the
``mcp`` reference implementation.  The server exposes a very small set of tools
that are intentionally simple and safe so the project can be used for local
experimentation or automated tests.
"""
from __future__ import annotations

import asyncio
import inspect
import logging
from typing import Any, Awaitable, Callable, Dict

from mcp.server.fastmcp import FastMCP

from .tools.executor import ExecutorTools
from .tools.filesystem import FilesystemTools
from .tools.templates import TemplateTools

LOGGER = logging.getLogger(__name__)


class MCPServer:
    """High level wrapper that owns the tool implementations."""

    def __init__(self) -> None:
        self._fs_tools = FilesystemTools()
        self._executor_tools = ExecutorTools()
        self._template_tools = TemplateTools()

        self._server = FastMCP(
            name="mcp-python-server",
            version="0.1.0",
            description="Sample MCP server that exposes filesystem, command, and template helpers.",
        )

        self._register_tools()

    @property
    def fastmcp(self) -> FastMCP:
        """Expose the underlying ``FastMCP`` instance for advanced integrations."""

        return self._server

    def _register_tools(self) -> None:
        """Register all tool handlers with the ``FastMCP`` instance."""

        server = self._server

        @server.tool()
        def read_file(path: str) -> Dict[str, Any]:
            """Read a text file from disk."""

            LOGGER.debug("read_file called with path=%s", path)
            content = self._fs_tools.read_file(path)
            return {"path": path, "content": content}

        @server.tool()
        def write_file(path: str, content: str) -> Dict[str, Any]:
            """Write content to a new file, replacing any existing data."""

            LOGGER.debug("write_file called with path=%s", path)
            self._fs_tools.write_file(path, content)
            return {"path": path, "status": "written"}

        @server.tool()
        def update_file(path: str, content: str) -> Dict[str, Any]:
            """Replace the contents of an existing file."""

            LOGGER.debug("update_file called with path=%s", path)
            self._fs_tools.update_file(path, content)
            return {"path": path, "status": "updated"}

        @server.tool()
        def list_directory(path: str) -> Dict[str, Any]:
            """List files and folders inside ``path``."""

            LOGGER.debug("list_directory called with path=%s", path)
            entries = self._fs_tools.list_directory(path)
            return {"path": path, "entries": entries}

        @server.tool()
        def run_command(cmd: list[str]) -> Dict[str, Any]:
            """Run a whitelisted command safely."""

            LOGGER.debug("run_command called with cmd=%s", cmd)
            result = self._executor_tools.run_command(cmd)
            return result

        @server.tool()
        def create_project_template(name: str, destination: str) -> Dict[str, Any]:
            """Copy a project template into the destination folder."""

            LOGGER.debug(
                "create_project_template called with name=%s destination=%s", name, destination
            )
            location = self._template_tools.create_project_template(name, destination)
            return {"template": name, "destination": str(location)}

    async def serve(self) -> None:
        """Start serving requests forever until cancelled."""

        LOGGER.info("Starting MCP server...")
        runner: Callable[[], Awaitable[None] | None] | None = None

        for candidate in ("run", "serve", "serve_forever"):
            method = getattr(self._server, candidate, None)
            if method and callable(method):
                runner = method  # type: ignore[assignment]
                break

        if runner is None:
            raise RuntimeError("FastMCP instance does not expose a runnable method")

        result = runner()
        if inspect.isawaitable(result):
            await result  # type: ignore[func-returns-value]


async def _main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(name)s: %(message)s")
    server = MCPServer()
    await server.serve()


if __name__ == "__main__":
    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        LOGGER.info("MCP server interrupted by user")
