"""Tests for GDScriptParser."""

import pytest
from pathlib import Path

from mcp_gdscript.parser import GDScriptParser


@pytest.fixture
def parser():
	"""Create a parser instance."""
	return GDScriptParser()


@pytest.fixture
def sample_code():
	"""Sample GDScript code for testing."""
	return """
extends Node2D

signal my_signal

var my_variable: int = 10
var another_var: String = "test"

func my_function() -> void:
	print("Hello")

func another_function(param: int) -> int:
	return param * 2

class MyClass:
	var class_var = 5
"""


@pytest.fixture
def fixture_dir():
	"""Get the fixtures directory."""
	return Path(__file__).parent / "fixtures"


def test_parse_code(parser, sample_code):
	"""Test basic code parsing."""
	tree = parser.parse(sample_code)
	assert tree is not None
	assert tree.root_node is not None


def test_get_symbols(parser, sample_code):
	"""Test symbol extraction."""
	tree = parser.parse(sample_code)
	symbols = parser.get_symbols(tree)

	assert "classes" in symbols
	assert "functions" in symbols
	assert "variables" in symbols
	assert "signals" in symbols
	assert "enums" in symbols

	# Check that symbols were found
	assert len(symbols["functions"]) > 0
	assert len(symbols["variables"]) > 0
	assert len(symbols["signals"]) > 0


def test_find_symbol(parser, sample_code):
	"""Test finding a specific symbol."""
	tree = parser.parse(sample_code)

	# Find a function
	func_symbol = parser.find_symbol(tree, "my_function")
	assert func_symbol is not None
	assert func_symbol["name"] == "my_function"

	# Find a variable
	var_symbol = parser.find_symbol(tree, "my_variable")
	assert var_symbol is not None
	assert var_symbol["name"] == "my_variable"

	# Find a signal
	signal_symbol = parser.find_symbol(tree, "my_signal")
	assert signal_symbol is not None
	assert signal_symbol["name"] == "my_signal"

	# Non-existent symbol
	nonexistent = parser.find_symbol(tree, "nonexistent")
	assert nonexistent is None


def test_find_references_in_tree(parser, sample_code):
	"""Test finding symbol references."""
	tree = parser.parse(sample_code)

	# Find references to 'my_variable'
	references = parser.find_references(tree, "my_variable")
	assert isinstance(references, list)

	# Find references to 'my_function'
	func_refs = parser.find_references(tree, "my_function")
	assert isinstance(func_refs, list)


def test_get_dependencies(parser):
	"""Test dependency extraction."""
	code = """
extends Control
preload("res://scenes/player.tscn")
preload("res://scenes/enemy.tscn")
"""
	tree = parser.parse(code)
	deps = parser.get_dependencies(tree, code)

	assert "extends" in deps
	assert "preload" in deps
	assert "import" in deps

	assert len(deps["extends"]) > 0
	assert len(deps["preload"]) == 2


def test_get_structure(parser, sample_code):
	"""Test structure generation."""
	tree = parser.parse(sample_code)
	structure = parser.get_structure(tree, sample_code)

	assert isinstance(structure, str)
	assert "Functions" in structure or "functions" in structure.lower()
	assert "Variables" in structure or "variables" in structure.lower()


def test_parse_from_file(parser, fixture_dir):
	"""Test parsing from a file."""
	player_file = fixture_dir / "sample_player.gd"
	if player_file.exists():
		code = player_file.read_text(encoding="utf-8")
		tree = parser.parse(code)
		symbols = parser.get_symbols(tree)

		# Verify expected symbols are found
		function_names = [f["name"] for f in symbols["functions"]]
		assert "_ready" in function_names or "_ready" in str(symbols)


def test_find_references_in_file(parser, fixture_dir):
	"""Test finding references in a file."""
	player_file = fixture_dir / "sample_player.gd"
	if player_file.exists():
		code = player_file.read_text(encoding="utf-8")
		tree = parser.parse(code)

		# Find references to 'player_name'
		references = parser.find_references(tree, "player_name")
		assert isinstance(references, list)
		# Should find multiple references
		assert len(references) > 0


def test_empty_code(parser):
	"""Test parsing empty code."""
	tree = parser.parse("")
	assert tree is not None
	assert tree.root_node is not None


def test_invalid_code_handling(parser):
	"""Test handling of invalid code."""
	# GDScript parser should still create a tree even with errors
	code = "func broken( : void:"
	tree = parser.parse(code)
	assert tree is not None
