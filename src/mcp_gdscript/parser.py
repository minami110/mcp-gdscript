"""GDScript parser wrapper using tree-sitter."""

from typing import Any, Optional
from tree_sitter_language_pack import get_language, get_parser
from tree_sitter import Tree, Node


class GDScriptParser:
    """Parser for GDScript using tree-sitter."""

    def __init__(self):
        """Initialize the GDScript parser."""
        self.language = get_language("gdscript")
        self.parser = get_parser("gdscript")

    def parse(self, code: str) -> Tree:
        """Parse GDScript code and return the syntax tree.

        Args:
            code: GDScript source code as string

        Returns:
            tree_sitter.Tree: The parsed syntax tree
        """
        return self.parser.parse(code.encode("utf-8"))

    def get_symbols(self, tree: Tree) -> dict[str, Any]:
        """Extract symbols (classes, functions, etc.) from the tree.

        Args:
            tree: The parsed syntax tree

        Returns:
            Dictionary with symbol information
        """
        symbols = {
            "classes": [],
            "functions": [],
            "variables": [],
            "signals": [],
            "enums": [],
        }

        self._extract_symbols(tree.root_node, symbols)
        return symbols

    def _extract_symbols(self, node: Node, symbols: dict[str, Any], depth: int = 0) -> None:
        """Recursively extract symbols from tree nodes.

        Args:
            node: Current tree node
            symbols: Symbol dictionary to populate
            depth: Current recursion depth
        """
        if depth > 20:  # Prevent infinite recursion
            return

        node_type = node.type

        if node_type == "class_definition":
            name = self._get_node_text(node, "name")
            if name:
                symbols["classes"].append({
                    "name": name,
                    "line": node.start_point[0] + 1,
                    "column": node.start_point[1],
                })

        elif node_type == "function_definition":
            name = self._get_node_text(node, "name")
            if name:
                symbols["functions"].append({
                    "name": name,
                    "line": node.start_point[0] + 1,
                    "column": node.start_point[1],
                })

        elif node_type == "signal_statement":
            name = self._get_node_text(node, "name")
            if name:
                symbols["signals"].append({
                    "name": name,
                    "line": node.start_point[0] + 1,
                    "column": node.start_point[1],
                })

        elif node_type == "enum_definition":
            name = self._get_node_text(node, "name")
            if name:
                symbols["enums"].append({
                    "name": name,
                    "line": node.start_point[0] + 1,
                    "column": node.start_point[1],
                })

        elif node_type in ("assignment", "variable_statement"):
            name = self._get_node_text(node, "name")
            if name:
                symbols["variables"].append({
                    "name": name,
                    "line": node.start_point[0] + 1,
                    "column": node.start_point[1],
                })

        # Recursively process child nodes
        for child in node.children:
            self._extract_symbols(child, symbols, depth + 1)

    def _get_node_text(self, node: Node, child_name: str = None) -> Optional[str]:
        """Get text content from a node or its named child.

        Args:
            node: The tree node
            child_name: Name of the child node to extract text from

        Returns:
            Text content or None
        """
        target_node = node

        if child_name:
            target_node = node.child_by_field_name(child_name)
            if not target_node:
                return None

        if target_node.type == "identifier":
            return target_node.text.decode("utf-8") if isinstance(target_node.text, bytes) else str(target_node.text)

        # Try to get the first identifier child
        for child in target_node.children:
            if child.type == "identifier":
                return child.text.decode("utf-8") if isinstance(child.text, bytes) else str(child.text)

        return None

    def get_structure(self, tree: Tree, code: str) -> str:
        """Get a high-level structure overview of the file.

        Args:
            tree: The parsed syntax tree
            code: The original source code

        Returns:
            Formatted structure string
        """
        symbols = self.get_symbols(tree)
        structure_lines = ["=== GDScript File Structure ===\n"]

        if symbols["classes"]:
            structure_lines.append("Classes:")
            for cls in symbols["classes"]:
                structure_lines.append(f"  - {cls['name']} (line {cls['line']})")

        if symbols["functions"]:
            structure_lines.append("\nFunctions:")
            for func in symbols["functions"]:
                structure_lines.append(f"  - {func['name']} (line {func['line']})")

        if symbols["signals"]:
            structure_lines.append("\nSignals:")
            for sig in symbols["signals"]:
                structure_lines.append(f"  - {sig['name']} (line {sig['line']})")

        if symbols["variables"]:
            structure_lines.append("\nVariables:")
            for var in symbols["variables"]:
                structure_lines.append(f"  - {var['name']} (line {var['line']})")

        if symbols["enums"]:
            structure_lines.append("\nEnums:")
            for enum in symbols["enums"]:
                structure_lines.append(f"  - {enum['name']} (line {enum['line']})")

        return "\n".join(structure_lines)

    def find_symbol(self, tree: Tree, symbol_name: str) -> Optional[dict[str, Any]]:
        """Find a symbol by name.

        Args:
            tree: The parsed syntax tree
            symbol_name: Name of the symbol to find

        Returns:
            Symbol information or None if not found
        """
        symbols = self.get_symbols(tree)

        for sym_type in ["classes", "functions", "signals", "variables", "enums"]:
            for sym in symbols[sym_type]:
                if sym["name"] == symbol_name:
                    return {
                        "type": sym_type[:-1],  # Remove trailing 's'
                        **sym,
                    }

        return None

    def get_dependencies(self, tree: Tree, code: str) -> dict[str, list[str]]:
        """Extract dependencies (extends, preload) from the file.

        Args:
            tree: The parsed syntax tree
            code: The original source code

        Returns:
            Dictionary with lists of dependencies
        """
        dependencies = {
            "extends": [],
            "preload": [],
            "import": [],
        }

        self._extract_dependencies(tree.root_node, dependencies)
        return dependencies

    def _extract_dependencies(self, node: Node, deps: dict[str, list[str]]) -> None:
        """Recursively extract dependencies from tree nodes.

        Args:
            node: Current tree node
            deps: Dependencies dictionary to populate
        """
        node_type = node.type

        # Check for extends statement
        if node_type == "extend_statement":
            path = self._extract_string_value(node)
            if path:
                deps["extends"].append(path)

        # Check for preload function calls
        elif node_type == "function_call":
            if self._is_preload_call(node):
                path = self._extract_string_argument(node)
                if path:
                    deps["preload"].append(path)

        # Check for import statements
        elif node_type == "import_statement":
            path = self._extract_string_value(node)
            if path:
                deps["import"].append(path)

        # Recursively process child nodes
        for child in node.children:
            self._extract_dependencies(child, deps)

    def _extract_string_value(self, node: Node) -> Optional[str]:
        """Extract string value from a node.

        Args:
            node: The tree node

        Returns:
            String value without quotes or None
        """
        for child in node.children:
            if child.type == "string":
                text = child.text.decode("utf-8") if isinstance(child.text, bytes) else str(child.text)
                # Remove quotes
                return text.strip('"\'')
        return None

    def _extract_string_argument(self, node: Node) -> Optional[str]:
        """Extract string argument from a function call node.

        Args:
            node: The function call node

        Returns:
            String value without quotes or None
        """
        # Find arguments node
        for child in node.children:
            if child.type == "arguments":
                for arg in child.children:
                    if arg.type == "string":
                        text = arg.text.decode("utf-8") if isinstance(arg.text, bytes) else str(arg.text)
                        return text.strip('"\'')
        return None

    def _is_preload_call(self, node: Node) -> bool:
        """Check if a function call is a preload call.

        Args:
            node: The function call node

        Returns:
            True if this is a preload call
        """
        for child in node.children:
            if child.type == "identifier":
                text = child.text.decode("utf-8") if isinstance(child.text, bytes) else str(child.text)
                if text == "preload":
                    return True
        return False
