# Example GDScript file demonstrating various GDScript features
extends CharacterBody2D

# Signals
signal health_changed(new_health)
signal died

# Variables
var speed = 200.0
var jump_force = -400.0
var gravity = 800.0
var health = 100
var max_health = 100

# Preloaded resources
var death_effect = preload("res://effects/death.tscn")
var attack_sound = preload("res://sounds/attack.wav")

# Enums
enum State { IDLE, RUNNING, JUMPING, FALLING, ATTACKING }
var current_state = State.IDLE

# Called when the node enters the scene tree
func _ready():
    print("Player initialized")
    connect("health_changed", Callable(self, "_on_health_changed"))

# Called every frame
func _process(delta):
    if not is_on_floor():
        velocity.y += gravity * delta

    if Input.is_action_pressed("ui_right"):
        velocity.x = speed
        current_state = State.RUNNING
    elif Input.is_action_pressed("ui_left"):
        velocity.x = -speed
        current_state = State.RUNNING
    else:
        velocity.x = 0
        current_state = State.IDLE

    if Input.is_action_just_pressed("ui_accept") and is_on_floor():
        velocity.y = jump_force
        current_state = State.JUMPING

    move_and_slide()

# Apply damage to the player
func take_damage(amount: int):
    health -= amount
    health_changed.emit(health)

    if health <= 0:
        die()

# Heal the player
func heal(amount: int):
    health = min(health + amount, max_health)
    health_changed.emit(health)

# Handle player death
func die():
    died.emit()
    var effect = death_effect.instantiate()
    get_parent().add_child(effect)
    effect.global_position = global_position
    queue_free()

# Signal callback
func _on_health_changed(new_health):
    print("Health changed to: ", new_health)
