# GDScript MCP Server - Usage Examples

This document shows practical examples of how to use the GDScript MCP server with Claude.

## Setup

Add this to your Claude configuration (`~/.claude/claude.json` or Claude Desktop settings):

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

## Example 1: Understanding a Player Script

**Request:**
```
I need to understand the structure of my player.gd script. What functions and signals does it have?
```

**Claude uses:**
```
gdscript get_gdscript_structure
file_path: "scenes/player.gd"
```

**Output:**
```
=== GDScript File Structure ===

Signals:
  - health_changed (line 6)
  - died (line 7)

Variables:
  - speed (line 9)
  - jump_force (line 10)
  - gravity (line 11)
  - health (line 12)
  - max_health (line 13)

Functions:
  - _ready (line 21)
  - _process (line 25)
  - take_damage (line 47)
  - heal (line 54)
  - die (line 61)
  - _on_health_changed (line 71)
```

Now Claude can understand the script structure without reading the entire file!

## Example 2: Finding a Specific Function

**Request:**
```
Where is the take_damage function defined in my player script and what line is it on?
```

**Claude uses:**
```
gdscript find_gdscript_symbol
file_path: "scenes/player.gd"
symbol_name: "take_damage"
```

**Output:**
```json
{
  "type": "function",
  "name": "take_damage",
  "line": 47,
  "column": 0
}
```

## Example 3: Understanding Dependencies

**Request:**
```
What external resources does my game_manager.gd depend on?
```

**Claude uses:**
```
gdscript get_gdscript_dependencies
file_path: "scripts/game_manager.gd"
```

**Output:**
```json
{
  "file": "scripts/game_manager.gd",
  "dependencies": {
    "extends": ["Node"],
    "preload": [
      "res://levels/level_1.tscn",
      "res://levels/level_2.tscn",
      "res://levels/level_3.tscn"
    ],
    "import": []
  }
}
```

## Example 4: Complete File Analysis

**Request:**
```
Analyze my enemy.gd script and show me a complete breakdown of all its components.
```

**Claude uses:**
```
gdscript analyze_gdscript_file
file_path: "enemies/enemy.gd"
```

**Output:**
```json
{
  "file": "enemies/enemy.gd",
  "symbols": {
    "classes": [],
    "functions": [
      {"name": "_ready", "line": 12, "column": 0},
      {"name": "_process", "line": 18, "column": 0},
      {"name": "take_damage", "line": 35, "column": 0},
      {"name": "patrol", "line": 42, "column": 0},
      {"name": "chase_player", "line": 52, "column": 0},
      {"name": "attack", "line": 65, "column": 0}
    ],
    "signals": [
      {"name": "died", "line": 6, "column": 0},
      {"name": "spotted", "line": 7, "column": 0}
    ],
    "variables": [
      {"name": "speed", "line": 9, "column": 0},
      {"name": "health", "line": 10, "column": 0}
    ],
    "enums": [
      {"name": "State", "line": 20, "column": 0}
    ]
  },
  "summary": {
    "total_classes": 0,
    "total_functions": 6,
    "total_signals": 2,
    "total_variables": 2,
    "total_enums": 1
  }
}
```

## Example 5: Analyzing Code Snippets

**Request:**
```
Can you analyze this GDScript snippet I wrote?
```

**Code snippet:**
```gdscript
class_name PlayerStats
extends Node

signal level_up
signal experience_gained

var level = 1
var experience = 0
var max_experience = 100

func gain_experience(amount: int):
    experience += amount
    experience_gained.emit(amount)

    if experience >= max_experience:
        level_up.emit()
        level += 1
        experience = 0
```

**Claude uses:**
```
gdscript analyze_gdscript_code
code: "[the complete code above]"
```

**Output:**
```json
{
  "structure": "=== GDScript File Structure ===\n\nSignals:\n  - level_up (line 4)\n  - experience_gained (line 5)\n\nVariables:\n  - level (line 7)\n  - experience (line 8)\n  - max_experience (line 9)\n\nFunctions:\n  - gain_experience (line 11)",
  "symbols": {
    "classes": [],
    "functions": [
      {"name": "gain_experience", "line": 11, "column": 0}
    ],
    "signals": [
      {"name": "level_up", "line": 4, "column": 0},
      {"name": "experience_gained", "line": 5, "column": 0}
    ],
    "variables": [
      {"name": "level", "line": 7, "column": 0},
      {"name": "experience", "line": 8, "column": 0},
      {"name": "max_experience", "line": 9, "column": 0}
    ],
    "enums": []
  }
}
```

## Real-World Workflow

### Scenario: Refactoring a Large Script

1. **Initial Analysis:**
   ```
   I need to refactor my game_manager.gd script. What's the current structure?
   ```
   Claude uses `get_gdscript_structure` to get an overview.

2. **Identify Dependencies:**
   ```
   What does game_manager depend on?
   ```
   Claude uses `get_gdscript_dependencies` to understand what needs to be preserved.

3. **Find Related Code:**
   ```
   Where are all the signal definitions in this file?
   ```
   Claude uses `find_gdscript_symbol` to locate each signal.

4. **Detailed Analysis:**
   ```
   Show me all the analysis for this file.
   ```
   Claude uses `analyze_gdscript_file` to get complete details.

5. **Code Review:**
   Claude can now provide refactoring suggestions based on the structure analysis.

## Benefits Over Traditional Approaches

### Without MCP Server:
- Claude must read entire files into context
- Large files consume significant tokens
- No structured understanding of code
- Context limits on file size

### With MCP Server:
✅ Quick structure overview without full file content
✅ Efficient token usage
✅ Structured, machine-readable code analysis
✅ Handle large files without context limits
✅ Symbol-level queries
✅ Dependency tracking

## Tips for Best Results

1. **For Large Projects:** Use `get_gdscript_structure` first to understand file organization
2. **For Specific Lookups:** Use `find_gdscript_symbol` to locate particular functions
3. **For Dependency Analysis:** Use `get_gdscript_dependencies` before major refactors
4. **For Code Review:** Use `analyze_gdscript_file` to understand complete file structure
5. **For Quick Checks:** Use `analyze_gdscript_code` for code snippets

## Troubleshooting

### Server not starting
```bash
# Check Python version
python --version  # Should be 3.10+

# Test with verbose logging
RUST_LOG=debug uvx mcp-server-gdscript-tree-sitter
```

### File not found errors
- Use absolute paths: `/home/user/project/scenes/player.gd`
- Or relative to working directory: `scenes/player.gd`

### Parse errors
- Ensure the file is valid GDScript 4.x syntax
- Check for unclosed strings or comments
- Verify file encoding is UTF-8

## Integration with Other Tools

You can use this MCP server alongside other tools in Claude:
- Document generation
- Code quality analysis
- Testing frameworks
- Version control systems

Claude can coordinate between tools to provide comprehensive code understanding.
