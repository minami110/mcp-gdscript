"""Tests for GDScriptTools."""

import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from mcp_gdscript.tools import GDScriptTools


@pytest.fixture
def tools():
	"""Create a GDScriptTools instance."""
	return GDScriptTools()


@pytest.fixture
def fixture_dir():
	"""Get the fixtures directory."""
	return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_code():
	"""Sample GDScript code."""
	return """
extends Node2D

signal my_signal

var my_var: int = 10

func my_func() -> void:
	print("test")
	my_var = 20
"""


class TestAnalyzeFile:
	def test_analyze_existing_file(self, tools, fixture_dir):
		"""Test analyzing an existing file."""
		player_file = fixture_dir / "sample_player.gd"
		if player_file.exists():
			result = tools._analyze_file(str(player_file))
			assert not result.isError
			content = json.loads(result.content[0].text)
			assert "file" in content
			assert "symbols" in content
			assert "summary" in content

	def test_analyze_nonexistent_file(self, tools):
		"""Test analyzing a non-existent file."""
		result = tools._analyze_file("/nonexistent/file.gd")
		assert result.isError
		assert "not found" in result.content[0].text.lower()

	def test_analyze_non_gdscript_file(self, tools, tmp_path):
		"""Test analyzing a non-GDScript file."""
		txt_file = tmp_path / "test.txt"
		txt_file.write_text("random text")
		result = tools._analyze_file(str(txt_file))
		assert result.isError


class TestGetStructure:
	def test_get_structure(self, tools, fixture_dir):
		"""Test getting file structure."""
		player_file = fixture_dir / "sample_player.gd"
		if player_file.exists():
			result = tools._get_structure(str(player_file))
			assert not result.isError
			content = result.content[0].text
			assert "GDScript File Structure" in content or "Structure" in content

	def test_get_structure_nonexistent_file(self, tools):
		"""Test getting structure of non-existent file."""
		result = tools._get_structure("/nonexistent/file.gd")
		assert result.isError


class TestFindSymbol:
	def test_find_existing_symbol(self, tools, fixture_dir):
		"""Test finding an existing symbol."""
		player_file = fixture_dir / "sample_player.gd"
		if player_file.exists():
			result = tools._find_symbol(str(player_file), "_ready")
			if not result.isError:
				content = json.loads(result.content[0].text)
				assert content["name"] == "_ready"

	def test_find_nonexistent_symbol(self, tools, fixture_dir):
		"""Test finding a non-existent symbol."""
		player_file = fixture_dir / "sample_player.gd"
		if player_file.exists():
			result = tools._find_symbol(str(player_file), "nonexistent_symbol")
			assert result.isError


class TestGetDependencies:
	def test_get_dependencies(self, tools, fixture_dir):
		"""Test extracting dependencies."""
		player_file = fixture_dir / "sample_player.gd"
		if player_file.exists():
			result = tools._get_dependencies(str(player_file))
			assert not result.isError
			content = json.loads(result.content[0].text)
			assert "dependencies" in content
			assert "extends" in content["dependencies"]


class TestAnalyzeCode:
	def test_analyze_code(self, tools, sample_code):
		"""Test analyzing code directly."""
		result = tools._analyze_code(sample_code)
		assert not result.isError
		content = json.loads(result.content[0].text)
		assert "structure" in content
		assert "symbols" in content
		assert "summary" in content


class TestSetProjectRoot:
	def test_set_valid_project_root(self, tools, fixture_dir):
		"""Test setting a valid project root."""
		result = tools._set_project_root(str(fixture_dir))
		assert not result.isError
		content = json.loads(result.content[0].text)
		assert "project_root" in content
		assert "gdscript_files_count" in content
		assert content["status"] == "success"

	def test_set_nonexistent_project_root(self, tools):
		"""Test setting a non-existent project root."""
		result = tools._set_project_root("/nonexistent/path")
		assert result.isError

	def test_set_file_as_project_root(self, tools, fixture_dir):
		"""Test setting a file instead of directory as project root."""
		player_file = fixture_dir / "sample_player.gd"
		if player_file.exists():
			result = tools._set_project_root(str(player_file))
			assert result.isError


class TestGetProjectRoot:
	def test_get_project_root_not_set(self, tools):
		"""Test getting project root when not set."""
		result = tools._get_project_root()
		assert not result.isError
		assert "No project root" in result.content[0].text

	def test_get_project_root_after_set(self, tools, fixture_dir):
		"""Test getting project root after setting."""
		tools._set_project_root(str(fixture_dir))
		result = tools._get_project_root()
		assert not result.isError
		content = json.loads(result.content[0].text)
		assert "project_root" in content
		assert "gdscript_files_count" in content


class TestFindReferences:
	def test_find_references_without_project_root_or_file(self, tools):
		"""Test finding references without project root or file."""
		result = tools._find_references("my_symbol")
		assert result.isError
		assert "project root" in result.content[0].text.lower() or "file" in result.content[0].text.lower()

	def test_find_references_in_file(self, tools, fixture_dir):
		"""Test finding references in a specific file."""
		player_file = fixture_dir / "sample_player.gd"
		if player_file.exists():
			result = tools._find_references("player_name", str(player_file))
			assert not result.isError
			content = json.loads(result.content[0].text)
			assert "symbol" in content
			assert "total_references" in content
			assert "references" in content
			assert content["symbol"] == "player_name"

	def test_find_references_in_project(self, tools, fixture_dir):
		"""Test finding references across project."""
		tools._set_project_root(str(fixture_dir))
		result = tools._find_references("player_name")
		assert not result.isError
		content = json.loads(result.content[0].text)
		assert "symbol" in content
		assert "total_references" in content
		assert "references" in content

	def test_find_references_nonexistent_file(self, tools):
		"""Test finding references in non-existent file."""
		result = tools._find_references("symbol", "/nonexistent/file.gd")
		assert result.isError

	def test_find_references_with_no_matches(self, tools, fixture_dir):
		"""Test finding references that don't exist."""
		player_file = fixture_dir / "sample_player.gd"
		if player_file.exists():
			result = tools._find_references("nonexistent_symbol_xyz", str(player_file))
			assert not result.isError
			content = json.loads(result.content[0].text)
			assert content["total_references"] == 0


class TestLoadGDScriptFiles:
	def test_load_gdscript_files(self, tools, fixture_dir):
		"""Test loading GDScript files."""
		tools.project_root = fixture_dir
		tools._load_gdscript_files()
		assert len(tools._gdscript_files) > 0
		# All files should have .gd extension
		for file in tools._gdscript_files:
			assert file.suffix == ".gd"

	def test_load_gdscript_files_no_root(self, tools):
		"""Test loading files without project root."""
		tools.project_root = None
		tools._load_gdscript_files()
		assert len(tools._gdscript_files) == 0


class TestToolList:
	def test_get_tools_list(self, tools):
		"""Test getting list of available tools."""
		tools_list = tools.get_tools()
		assert len(tools_list) > 0

		tool_names = [tool.name for tool in tools_list]
		assert "analyze_gdscript_file" in tool_names
		assert "get_gdscript_structure" in tool_names
		assert "find_gdscript_symbol" in tool_names
		assert "get_gdscript_dependencies" in tool_names
		assert "analyze_gdscript_code" in tool_names
		assert "set_project_root" in tool_names
		assert "get_project_root" in tool_names
		assert "find_references" in tool_names


class TestHandleToolCall:
	def test_handle_analyze_file_tool(self, tools, fixture_dir):
		"""Test handling analyze_gdscript_file tool call."""
		player_file = fixture_dir / "sample_player.gd"
		if player_file.exists():
			result = tools.handle_tool_call("analyze_gdscript_file", {"file_path": str(player_file)})
			assert not result.isError

	def test_handle_unknown_tool(self, tools):
		"""Test handling unknown tool."""
		result = tools.handle_tool_call("unknown_tool", {})
		assert result.isError
		assert "Unknown tool" in result.content[0].text

	def test_handle_set_project_root_tool(self, tools, fixture_dir):
		"""Test handling set_project_root tool call."""
		result = tools.handle_tool_call("set_project_root", {"project_root": str(fixture_dir)})
		assert not result.isError

	def test_handle_find_references_tool(self, tools, fixture_dir):
		"""Test handling find_references tool call."""
		tools._set_project_root(str(fixture_dir))
		result = tools.handle_tool_call("find_references", {"symbol_name": "player_name"})
		assert not result.isError
