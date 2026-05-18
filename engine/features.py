"""
Feature-Extraktion für die Snake-KI.

Ein Modell kann nicht direkt mit dem ganzen Spiel arbeiten.
Darum wandeln wir den Spielzustand in Zahlen um.

Diese Zahlen nennt man Features.
"""

from engine.snake_logic import (
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_STRAIGHT,
    get_next_position,
    is_collision,
    turn_direction,
)


FEATURE_NAMES = [
    "danger_front",
    "danger_left",
    "danger_right",
    "food_left",
    "food_right",
    "food_up",
    "food_down",
    "direction_up",
    "direction_down",
    "direction_left",
    "direction_right",
]


def extract_features(snake, direction, food, grid_width, grid_height):
    """
    Wandelt den aktuellen Spielzustand in eine Liste von Zahlen um.

    Jede Zahl ist 0 oder 1.
    """
    head = snake[0]
    body_without_head = snake[1:]

    front_direction = turn_direction(direction, ACTION_STRAIGHT)
    left_direction = turn_direction(direction, ACTION_LEFT)
    right_direction = turn_direction(direction, ACTION_RIGHT)

    front_position = get_next_position(head, front_direction)
    left_position = get_next_position(head, left_direction)
    right_position = get_next_position(head, right_direction)

    danger_front = int(is_collision(front_position, body_without_head, grid_width, grid_height))
    danger_left = int(is_collision(left_position, body_without_head, grid_width, grid_height))
    danger_right = int(is_collision(right_position, body_without_head, grid_width, grid_height))

    food_left = int(food[0] < head[0])
    food_right = int(food[0] > head[0])
    food_up = int(food[1] < head[1])
    food_down = int(food[1] > head[1])

    direction_up = int(direction == (0, -1))
    direction_down = int(direction == (0, 1))
    direction_left = int(direction == (-1, 0))
    direction_right = int(direction == (1, 0))

    return [
        danger_front,
        danger_left,
        danger_right,
        food_left,
        food_right,
        food_up,
        food_down,
        direction_up,
        direction_down,
        direction_left,
        direction_right,
    ]