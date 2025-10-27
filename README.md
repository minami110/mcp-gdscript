# mcp-gdscript

A Model Context Protocol (MCP) server for GDScript code analysis. This server allows AI assistants to understand GDScript code structure without reading entire files, making it efficient for large codebases.

## Features

- **File Structure Analysis**: Extract classes, functions, signals, variables, and enums from GDScript files
- **Symbol Search**: Find specific symbols and get their location and type
- **Dependency Extraction**: Identify extends, preload, and import statements
- **Direct Code Analysis**: Analyze GDScript code snippets without file I/O
- **Tree-Sitter Powered**: Accurate parsing using the official GDScript tree-sitter grammar

## Installation & Usage

### With uvx (Recommended)

The simplest way to use this server - no installation required:

```json
{
  "mcpServers": {
    "gdscript": {
      "command": "uvx",
      "args": ["mcp-gdscript"]
    }
  }
}
```

### With npm/npx

```json
{
  "mcpServers": {
    "gdscript": {
      "command": "npx",
      "args": ["mcp-gdscript"]
    }
  }
}
```

### Local Installation

```bash
# Clone the repository
git clone https://github.com/minami110/mcp-gdscript
cd mcp-gdscript

# Install in development mode
pip install -e .

# Run the server
mcp-gdscript
```

## Available Tools

### File-Based Analysis Tools

#### 1. `analyze_gdscript_file`

Analyze a GDScript file and extract its complete structure.

**Input:**
- `file_path` (string): Path to the .gd or .gdscript file

**Output:**
Returns JSON with:
- `symbols`: Lists of classes, functions, signals, variables, and enums with line numbers
- `summary`: Total counts for each symbol type

**Example:**
```json
{
  "file": "scenes/player.gd",
  "symbols": {
    "classes": [],
    "functions": [
      {"name": "_ready", "line": 5, "column": 0},
      {"name": "_process", "line": 10, "column": 0}
    ],
    "signals": [
      {"name": "health_changed", "line": 2, "column": 0}
    ],
    "variables": [],
    "enums": []
  },
  "summary": {
    "total_classes": 0,
    "total_functions": 2,
    "total_signals": 1,
    "total_variables": 0,
    "total_enums": 0
  }
}
```

#### 2. `get_gdscript_structure`

Get a human-readable structure view of a GDScript file.

**Input:**
- `file_path` (string): Path to the .gd or .gdscript file

**Output:**
A formatted text representation showing the file structure with line numbers.

**Example output:**
```
=== GDScript File Structure ===

Signals:
  - health_changed (line 2)

Functions:
  - _ready (line 5)
  - _process (line 10)
```

#### 3. `find_gdscript_symbol`

Search for a specific symbol in a file.

**Input:**
- `file_path` (string): Path to the .gd or .gdscript file
- `symbol_name` (string): Name of the symbol to find

**Output:**
Symbol information including type, name, and location.

**Example:**
```json
{
  "type": "function",
  "name": "_ready",
  "line": 5,
  "column": 0
}
```

#### 4. `get_gdscript_dependencies`

Extract all dependencies from a GDScript file.

**Input:**
- `file_path` (string): Path to the .gd or .gdscript file

**Output:**
Lists of extends, preload, and import statements.

**Example:**
```json
{
  "file": "scenes/enemy.gd",
  "dependencies": {
    "extends": ["Character"],
    "preload": ["res://scenes/explosion.tscn"],
    "import": []
  }
}
```

#### 5. `analyze_gdscript_code`

Analyze GDScript code provided directly as a string.

**Input:**
- `code` (string): GDScript source code

**Output:**
Complete analysis including structure, symbols, and summary.

### Project Management Tools

#### 6. `set_project_root`

Set the project root directory to enable project-wide analysis.

**Input:**
- `project_root` (string): Path to the project root directory

**Output:**
Confirmation with indexed GDScript files count.

**Example:**
```json
{
  "project_root": "/home/user/godot_project",
  "gdscript_files_count": 42,
  "status": "success"
}
```

#### 7. `get_project_root`

Get the current project root directory and file count.

**Input:**
- None

**Output:**
Current project root path and indexed file count.

**Example:**
```json
{
  "project_root": "/home/user/godot_project",
  "gdscript_files_count": 42
}
```

### Code Analysis Tools

#### 8. `find_references`

Find all references to a symbol across the project or in a specific file.

**Input:**
- `symbol_name` (string): Name of the symbol to find references for
- `file_path` (optional string): Limit search to a specific file. If not provided and project root is set, searches entire project.

**Output:**
List of all locations where the symbol is referenced.

**Example:**
```json
{
  "symbol": "player_name",
  "total_references": 5,
  "references": [
    {
      "file": "scripts/player.gd",
      "line": 15,
      "column": 8,
      "end_line": 15,
      "end_column": 19
    },
    {
      "file": "scripts/manager.gd",
      "line": 42,
      "column": 12,
      "end_line": 42,
      "end_column": 23
    }
  ]
}
```

**Use Cases:**
- Find all usages of a variable or function
- Understand dependencies between files
- Refactor safely by checking all references
- Trace data flow in your project

## Use Cases

1. **Codebase Navigation**: Quickly understand the structure of large GDScript files
2. **API Documentation**: Generate documentation from code structure
3. **Dependency Analysis**: Understand script relationships and dependencies
4. **Code Review**: Get structure overview before detailed review
5. **Refactoring Aid**: Understand what needs to be updated when refactoring

## Configuration

### Environment Variables

- `RUST_LOG`: Set logging level (e.g., `debug`, `info`, `warn`)

### Performance Tips

- For large files (>10MB), the server efficiently extracts structure without loading full content into context
- Symbol extraction is optimized for typical GDScript files (< 50MB)
- The tree-sitter parser uses cached grammar for performance

## Limitations

- Currently optimized for GDScript 4.x and later
- Complex macro expansions may not be fully analyzed
- Some edge cases in dynamic code patterns may not be captured

## Development

### Setup
```bash
pip install -e ".[dev]"
```

### Testing
```bash
pytest
```

### Code Style
```bash
black .
ruff check .
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Tree-Sitter](https://tree-sitter.github.io/tree-sitter/)
- [Tree-Sitter Language Pack](https://github.com/Goldziher/tree-sitter-language-pack)
- [GDScript Documentation](https://docs.godotengine.org/en/stable/getting_started/scripting/gdscript/index.html)

## Troubleshooting

### "Module not found" errors
Make sure you're using Python 3.10 or later and have installed the server correctly.

### Parse errors for GDScript 3.x
This server is optimized for GDScript 4.x. For GDScript 3.x, some features may not work as expected.

### Performance issues
If analyzing very large files, consider:
1. Splitting large scripts into smaller modules
2. Using the structure tool instead of full analysis
3. Analyzing specific symbols instead of entire files
