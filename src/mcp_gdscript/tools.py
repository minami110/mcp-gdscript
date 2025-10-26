"""MCP tools for GDScript analysis."""

import json
from pathlib import Path
from typing import Any

from mcp.types import Tool, TextContent, CallToolResult

from .parser import GDScriptParser


class GDScriptTools:
    """Collection of tools for GDScript analysis."""

    def __init__(self):
        """Initialize the tools."""
        self.parser = GDScriptParser()

    def get_tools(self) -> list[Tool]:
        """Get all available tools.

        Returns:
            List of Tool definitions
        """
        return [
            Tool(
                name="analyze_gdscript_file",
                description="Analyze a GDScript file and extract its structure (classes, functions, signals, variables, enums). Returns a comprehensive overview without reading the entire file into context.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the GDScript file to analyze",
                        }
                    },
                    "required": ["file_path"],
                },
            ),
            Tool(
                name="get_gdscript_structure",
                description="Get a high-level structure view of a GDScript file, showing all classes, functions, signals, and variables with their line numbers.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the GDScript file",
                        }
                    },
                    "required": ["file_path"],
                },
            ),
            Tool(
                name="find_gdscript_symbol",
                description="Search for a specific symbol (class, function, signal, etc.) in a GDScript file and get its details.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the GDScript file",
                        },
                        "symbol_name": {
                            "type": "string",
                            "description": "Name of the symbol to find",
                        },
                    },
                    "required": ["file_path", "symbol_name"],
                },
            ),
            Tool(
                name="get_gdscript_dependencies",
                description="Extract dependencies from a GDScript file (extends, preload, import statements).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the GDScript file",
                        }
                    },
                    "required": ["file_path"],
                },
            ),
            Tool(
                name="analyze_gdscript_code",
                description="Analyze GDScript code provided directly and extract its structure.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "GDScript source code to analyze",
                        }
                    },
                    "required": ["code"],
                },
            ),
        ]

    def handle_tool_call(self, tool_name: str, tool_input: dict[str, Any]) -> CallToolResult:
        """Handle a tool call.

        Args:
            tool_name: Name of the tool to execute
            tool_input: Input parameters for the tool

        Returns:
            CallToolResult with the output
        """
        try:
            if tool_name == "analyze_gdscript_file":
                return self._analyze_file(tool_input["file_path"])
            elif tool_name == "get_gdscript_structure":
                return self._get_structure(tool_input["file_path"])
            elif tool_name == "find_gdscript_symbol":
                return self._find_symbol(tool_input["file_path"], tool_input["symbol_name"])
            elif tool_name == "get_gdscript_dependencies":
                return self._get_dependencies(tool_input["file_path"])
            elif tool_name == "analyze_gdscript_code":
                return self._analyze_code(tool_input["code"])
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Unknown tool: {tool_name}")],
                    isError=True,
                )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {str(e)}")],
                isError=True,
            )

    def _analyze_file(self, file_path: str) -> CallToolResult:
        """Analyze a GDScript file.

        Args:
            file_path: Path to the file

        Returns:
            CallToolResult with analysis
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return CallToolResult(
                    content=[TextContent(type="text", text=f"File not found: {file_path}")],
                    isError=True,
                )

            if not path.suffix.lower() in [".gd", ".gdscript"]:
                return CallToolResult(
                    content=[TextContent(type="text", text="File must be a .gd or .gdscript file")],
                    isError=True,
                )

            code = path.read_text(encoding="utf-8")
            tree = self.parser.parse(code)
            symbols = self.parser.get_symbols(tree)

            result = {
                "file": file_path,
                "symbols": symbols,
                "summary": {
                    "total_classes": len(symbols["classes"]),
                    "total_functions": len(symbols["functions"]),
                    "total_signals": len(symbols["signals"]),
                    "total_variables": len(symbols["variables"]),
                    "total_enums": len(symbols["enums"]),
                },
            }

            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))],
                isError=False,
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error analyzing file: {str(e)}")],
                isError=True,
            )

    def _get_structure(self, file_path: str) -> CallToolResult:
        """Get structure view of a GDScript file.

        Args:
            file_path: Path to the file

        Returns:
            CallToolResult with structure
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return CallToolResult(
                    content=[TextContent(type="text", text=f"File not found: {file_path}")],
                    isError=True,
                )

            code = path.read_text(encoding="utf-8")
            tree = self.parser.parse(code)
            structure = self.parser.get_structure(tree, code)

            return CallToolResult(
                content=[TextContent(type="text", text=structure)],
                isError=False,
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error getting structure: {str(e)}")],
                isError=True,
            )

    def _find_symbol(self, file_path: str, symbol_name: str) -> CallToolResult:
        """Find a symbol in a GDScript file.

        Args:
            file_path: Path to the file
            symbol_name: Name of the symbol to find

        Returns:
            CallToolResult with symbol info
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return CallToolResult(
                    content=[TextContent(type="text", text=f"File not found: {file_path}")],
                    isError=True,
                )

            code = path.read_text(encoding="utf-8")
            tree = self.parser.parse(code)
            symbol = self.parser.find_symbol(tree, symbol_name)

            if symbol:
                return CallToolResult(
                    content=[TextContent(type="text", text=json.dumps(symbol, indent=2))],
                    isError=False,
                )
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Symbol '{symbol_name}' not found")],
                    isError=True,
                )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error finding symbol: {str(e)}")],
                isError=True,
            )

    def _get_dependencies(self, file_path: str) -> CallToolResult:
        """Get dependencies from a GDScript file.

        Args:
            file_path: Path to the file

        Returns:
            CallToolResult with dependencies
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return CallToolResult(
                    content=[TextContent(type="text", text=f"File not found: {file_path}")],
                    isError=True,
                )

            code = path.read_text(encoding="utf-8")
            tree = self.parser.parse(code)
            dependencies = self.parser.get_dependencies(tree, code)

            result = {
                "file": file_path,
                "dependencies": dependencies,
            }

            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))],
                isError=False,
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error getting dependencies: {str(e)}")],
                isError=True,
            )

    def _analyze_code(self, code: str) -> CallToolResult:
        """Analyze GDScript code provided directly.

        Args:
            code: GDScript source code

        Returns:
            CallToolResult with analysis
        """
        try:
            tree = self.parser.parse(code)
            symbols = self.parser.get_symbols(tree)
            structure = self.parser.get_structure(tree, code)

            result = {
                "structure": structure,
                "symbols": symbols,
                "summary": {
                    "total_classes": len(symbols["classes"]),
                    "total_functions": len(symbols["functions"]),
                    "total_signals": len(symbols["signals"]),
                    "total_variables": len(symbols["variables"]),
                    "total_enums": len(symbols["enums"]),
                },
            }

            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(result, indent=2))],
                isError=False,
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error analyzing code: {str(e)}")],
                isError=True,
            )
