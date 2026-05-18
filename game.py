"""
SnakeTrainer-Spiel mit Pygame Zero.

Diese Datei zeigt das Spiel an.
Hier wird die Spiellogik mit der KI verbunden.

Du darfst hier kleine sichtbare Änderungen machen.
"""

import random

from pygame import Rect

from engine.ai_player import load_model, predict_action
from engine.data_recorder import save_training_row
from engine.features import extract_features
from engine.snake_logic import (
    ACTION_STRAIGHT,
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_UP,
    get_next_position,
    get_relative_action,
    is_collision,
    turn_direction,
)
from student_config import (
    BACKGROUND_COLOR,
    FOOD_COLOR,
    GAME_OVER_TEXT,
    GAME_TITLE,
    GRID_COLOR,
    GRID_HEIGHT,
    GRID_SIZE,
    GRID_WIDTH,
    SAVE_HUMAN_DATA,
    SNAKE_COLOR,
    SNAKE_HEAD_COLOR,
    SNAKE_SPEED,
    TEXT_COLOR,
    USE_AI_BY_DEFAULT,
)
from student_tasks import (
    format_high_score,
    format_score,
    get_ai_status_text,
    get_mode_text,
    is_high_score,
)


WIDTH = GRID_WIDTH * GRID_SIZE
HEIGHT = GRID_HEIGHT * GRID_SIZE
TITLE = GAME_TITLE


snake = []
direction = DIRECTION_RIGHT
food = (0, 0)

score = 0
high_score = 0

game_over = False
ai_mode = USE_AI_BY_DEFAULT
model = load_model()

move_timer = 0
pending_action = ACTION_STRAIGHT
status_message = "Pfeiltasten: bewegen | K: KI | R: Neustart"


def create_food():
    """
    Sucht ein freies Feld für das Futter.
    """
    free_positions = []

    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            position = (x, y)

            if position not in snake:
                free_positions.append(position)

    if not free_positions:
        return (0, 0)

    return random.choice(free_positions)


def reset_game():
    """
    Startet eine neue Runde.
    """
    global snake
    global direction
    global food
    global score
    global game_over
    global move_timer
    global pending_action
    global status_message

    center_x = GRID_WIDTH // 2
    center_y = GRID_HEIGHT // 2

    snake = [
        (center_x, center_y),
        (center_x - 1, center_y),
        (center_x - 2, center_y),
    ]

    direction = DIRECTION_RIGHT
    food = create_food()

    score = 0
    game_over = False
    move_timer = 0
    pending_action = ACTION_STRAIGHT
    status_message = "Neue Runde gestartet"


def draw_cell(position, color):
    """
    Zeichnet ein einzelnes Rasterfeld.
    """
    left = position[0] * GRID_SIZE
    top = position[1] * GRID_SIZE

    screen.draw.filled_rect(
        Rect((left, top), (GRID_SIZE - 1, GRID_SIZE - 1)),
        color,
    )


def draw_grid():
    """
    Zeichnet ein einfaches Raster.
    """
    for x in range(0, WIDTH, GRID_SIZE):
        screen.draw.line((x, 0), (x, HEIGHT), GRID_COLOR)

    for y in range(0, HEIGHT, GRID_SIZE):
        screen.draw.line((0, y), (WIDTH, y), GRID_COLOR)


def draw():
    """
    Zeichnet das Spiel.
    Diese Funktion wird von Pygame Zero automatisch aufgerufen.
    """
    screen.clear()
    screen.fill(BACKGROUND_COLOR)

    draw_grid()

    draw_cell(food, FOOD_COLOR)

    for index, part in enumerate(snake):
        if index == 0:
            draw_cell(part, SNAKE_HEAD_COLOR)
        else:
            draw_cell(part, SNAKE_COLOR)

    screen.draw.text(
        format_score(score),
        (10, 10),
        color=TEXT_COLOR,
        fontsize=28,
    )

    screen.draw.text(
        format_high_score(high_score),
        (10, 40),
        color=TEXT_COLOR,
        fontsize=24,
    )

    screen.draw.text(
        get_mode_text(ai_mode),
        (10, 68),
        color=TEXT_COLOR,
        fontsize=24,
    )

    screen.draw.text(
        status_message,
        (10, HEIGHT - 30),
        color=TEXT_COLOR,
        fontsize=20,
    )

    if game_over:
        screen.draw.text(
            GAME_OVER_TEXT,
            center=(WIDTH // 2, HEIGHT // 2),
            color=TEXT_COLOR,
            fontsize=36,
        )


def move_one_step():
    """
    Führt einen Spielschritt aus.
    """
    global snake
    global direction
    global food
    global score
    global high_score
    global game_over
    global pending_action
    global status_message

    if game_over:
        return

    features = extract_features(snake, direction, food, GRID_WIDTH, GRID_HEIGHT)

    if ai_mode:
        action = predict_action(model, features)
    else:
        action = pending_action

        if SAVE_HUMAN_DATA:
            save_training_row(features, action)

    pending_action = ACTION_STRAIGHT

    new_direction = turn_direction(direction, action)
    new_head = get_next_position(snake[0], new_direction)

    if is_collision(new_head, snake[1:], GRID_WIDTH, GRID_HEIGHT):
        game_over = True

        if is_high_score(score, high_score):
            high_score = score

        status_message = "Kollision"
        return

    direction = new_direction

    if new_head == food:
        snake = [new_head] + snake
        score += 1
        food = create_food()

        if is_high_score(score, high_score):
            high_score = score
    else:
        snake = [new_head] + snake[:-1]


def update(dt):
    """
    Aktualisiert das Spiel.
    Diese Funktion wird von Pygame Zero automatisch aufgerufen.
    """
    global move_timer

    if game_over:
        return

    move_timer += dt

    if move_timer >= 1 / SNAKE_SPEED:
        move_timer = 0
        move_one_step()


def on_key_down(key):
    """
    Reagiert auf Tasteneingaben.
    """
    global ai_mode
    global model
    global pending_action
    global status_message

    if key == keys.R:
        reset_game()
        return

    if key == keys.K:
        ai_mode = not ai_mode

        if ai_mode:
            model = load_model()
            status_message = get_ai_status_text(model is not None)
        else:
            status_message = "Mensch-Modus aktiv"

        return

    if ai_mode or game_over:
        return

    desired_direction = None

    if key == keys.UP:
        desired_direction = DIRECTION_UP

    if key == keys.DOWN:
        desired_direction = DIRECTION_DOWN

    if key == keys.LEFT:
        desired_direction = DIRECTION_LEFT

    if key == keys.RIGHT:
        desired_direction = DIRECTION_RIGHT

    if desired_direction is None:
        return

    action = get_relative_action(direction, desired_direction)

    if action is not None:
        pending_action = action


reset_game()