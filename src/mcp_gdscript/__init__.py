"""MCP server for GDScript syntax parsing using tree-sitter."""

__version__ = "0.1.0"
__author__ = "Your Name"
__description__ = "MCP server for GDScript syntax parsing using tree-sitter"

from .parser import GDScriptParser
from .server import GDScriptMCPServer
from .tools import GDScriptTools

__all__ = ["GDScriptParser", "GDScriptMCPServer", "GDScriptTools"]
