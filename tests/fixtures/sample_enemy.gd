extends CharacterBody2D
# Enemy character script

signal enemy_defeated

var enemy_name: String = "Goblin"
var health: int = 50
var attack_power: int = 10
var detection_range: float = 300.0
var target = null

enum State {
	IDLE,
	CHASE,
	ATTACK,
	DEAD
}

var current_state: State = State.IDLE

func _ready() -> void:
	print("Enemy spawned: ", enemy_name)
	health = 50

func _process(delta: float) -> void:
	match current_state:
		State.IDLE:
			patrol()
		State.CHASE:
			chase_target()
		State.ATTACK:
			attack_target()
		State.DEAD:
			pass

func patrol() -> void:
	# Simple patrol logic
	var nearby = get_tree().get_nodes_in_group("player")
	if nearby.size() > 0:
		target = nearby[0]
		current_state = State.CHASE

func chase_target() -> void:
	if target and is_instance_valid(target):
		var distance = global_position.distance_to(target.global_position)
		if distance < attack_power:
			current_state = State.ATTACK
	else:
		current_state = State.IDLE

func attack_target() -> void:
	if target and is_instance_valid(target):
		target.take_damage(attack_power)

func take_damage(damage: int) -> void:
	health -= damage
	if health <= 0:
		die()

func die() -> void:
	print(enemy_name, " defeated!")
	enemy_defeated.emit()
	queue_free()
