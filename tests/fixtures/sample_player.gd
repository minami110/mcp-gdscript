extends CharacterBody2D
# Player character script

signal health_changed(new_health)
signal level_up

var player_name: String = "Player"
var max_health: int = 100
var current_health: int = 100
var speed: float = 200.0

func _ready() -> void:
	print("Player initialized: ", player_name)
	current_health = max_health

func _process(delta: float) -> void:
	var input_vector = Vector2.ZERO
	input_vector.x = Input.get_axis("ui_left", "ui_right")
	input_vector.y = Input.get_axis("ui_up", "ui_down")

	if input_vector != Vector2.ZERO:
		velocity = input_vector * speed
	else:
		velocity = Vector2.ZERO

	move_and_slide()

func take_damage(amount: int) -> void:
	current_health -= amount
	health_changed.emit(current_health)
	if current_health <= 0:
		die()

func heal(amount: int) -> void:
	current_health = min(current_health + amount, max_health)
	health_changed.emit(current_health)

func die() -> void:
	print(player_name, " has died!")
	queue_free()

func level_up_player() -> void:
	max_health += 20
	current_health = max_health
	level_up.emit()
