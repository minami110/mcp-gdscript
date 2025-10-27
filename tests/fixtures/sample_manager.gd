extends Node
# Game manager script

signal game_started
signal game_ended

var player_name: String = "MainPlayer"
var score: int = 0
var level: int = 1
var is_game_running: bool = false

var player_ref = null
var enemies = []

func _ready() -> void:
	print("Game Manager initialized")
	setup_game()

func setup_game() -> void:
	player_name = "Hero"
	score = 0
	level = 1
	is_game_running = false
	game_started.emit()

func start_game() -> void:
	is_game_running = true
	print("Starting game with player: ", player_name)
	spawn_enemies()

func spawn_enemies() -> void:
	var enemy_scene = preload("res://scenes/enemy.tscn")
	for i in range(3):
		var enemy = enemy_scene.instantiate()
		add_child(enemy)
		enemies.append(enemy)

func update_score(points: int) -> void:
	score += points
	print("Score updated: ", score)

func end_game() -> void:
	is_game_running = false
	print("Game ended. Final score: ", score)
	game_ended.emit()

func get_player_name() -> String:
	return player_name

func get_game_info() -> Dictionary:
	return {
		"player_name": player_name,
		"score": score,
		"level": level,
		"is_running": is_game_running
	}
