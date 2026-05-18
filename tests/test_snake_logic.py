import pytest

from engine.snake_logic import (
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_STRAIGHT,
    DIRECTION_RIGHT,
    DIRECTION_UP,
    get_next_position,
    get_relative_action,
    is_collision,
    turn_direction,
)


def test_turn_direction_straight():
    assert turn_direction((1, 0), ACTION_STRAIGHT) == (1, 0)


def test_turn_direction_left_from_right():
    assert turn_direction((1, 0), ACTION_LEFT) == (0, -1)


def test_turn_direction_right_from_right():
    assert turn_direction((1, 0), ACTION_RIGHT) == (0, 1)


def test_turn_direction_invalid_action():
    with pytest.raises(ValueError):
        turn_direction((1, 0), 99)


def test_get_next_position():
    assert get_next_position((5, 5), (1, 0)) == (6, 5)


def test_collision_with_left_wall():
    assert is_collision((-1, 5), [], 24, 18) is True


def test_collision_with_body():
    body = [(5, 5), (6, 5)]
    assert is_collision((5, 5), body, 24, 18) is True


def test_no_collision():
    body = [(5, 5), (6, 5)]
    assert is_collision((7, 5), body, 24, 18) is False


def test_get_relative_action_left():
    assert get_relative_action(DIRECTION_RIGHT, DIRECTION_UP) == ACTION_LEFT