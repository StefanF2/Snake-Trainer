from student_config import AI_MODE_TEXT, HUMAN_MODE_TEXT
from student_tasks import (
    format_high_score,
    format_score,
    get_mode_text,
    is_high_score,
)


def test_format_score():
    assert "5" in format_score(5)


def test_format_high_score():
    assert "12" in format_high_score(12)


def test_get_mode_text_ai():
    assert get_mode_text(True) == AI_MODE_TEXT + "-Modus"


def test_get_mode_text_human():
    assert get_mode_text(False) == HUMAN_MODE_TEXT + "-Modus"


def test_is_high_score_true():
    assert is_high_score(10, 5) is True


def test_is_high_score_false():
    assert is_high_score(3, 5) is False