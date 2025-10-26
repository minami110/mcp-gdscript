# Game Manager - Singleton pattern
extends Node

signal game_started
signal game_paused
signal game_resumed
signal game_over

var is_paused = false
var current_level = 1
var total_score = 0

# Preload scenes
var level_scenes = {
    1: preload("res://levels/level_1.tscn"),
    2: preload("res://levels/level_2.tscn"),
    3: preload("res://levels/level_3.tscn"),
}

func _ready():
    # Make this a singleton
    process_mode = Node.PROCESS_MODE_ALWAYS
    print("Game Manager initialized")

func _process(delta):
    if Input.is_action_just_pressed("pause"):
        if is_paused:
            resume_game()
        else:
            pause_game()

func start_game():
    print("Starting game")
    game_started.emit()
    load_level(current_level)

func pause_game():
    is_paused = true
    get_tree().paused = true
    game_paused.emit()

func resume_game():
    is_paused = false
    get_tree().paused = false
    game_resumed.emit()

func load_level(level_number: int):
    if level_number not in level_scenes:
        print("Level ", level_number, " not found")
        return

    print("Loading level: ", level_number)
    get_tree().root.add_child(level_scenes[level_number].instantiate())

func add_score(points: int):
    total_score += points
    print("Score added: ", points, " Total: ", total_score)

func end_game():
    print("Game Over! Final Score: ", total_score)
    game_over.emit()
    await get_tree().create_timer(2.0).timeout
    get_tree().quit()

enum GameState { MENU, PLAYING, PAUSED, GAME_OVER }
