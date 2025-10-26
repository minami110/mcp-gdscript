"""Main MCP server for GDScript analysis."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, CallToolResult

from .tools import GDScriptTools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class GDScriptMCPServer:
    """MCP Server for GDScript analysis."""

    def __init__(self):
        """Initialize the MCP server."""
        self.server = Server("mcp-gdscript")
        self.tools = GDScriptTools()
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up MCP request handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools."""
            logger.info("Listing available tools")
            return self.tools.get_tools()

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> CallToolResult:
            """Handle tool calls."""
            logger.info(f"Calling tool: {name} with arguments: {arguments}")

            result = self.tools.handle_tool_call(name, arguments)

            return CallToolResult(content=result.content, isError=result.isError)

    async def run(self) -> None:
        """Run the MCP server."""
        logger.info("Starting GDScript MCP server")
        async with stdio_server() as (read_stream, write_stream):
            logger.info("GDScript MCP server is running")
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main() -> None:
    """Main entry point for the server."""
    server = GDScriptMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
