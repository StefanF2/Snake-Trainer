"""
KI-Spieler für Snake.

Diese Datei lädt ein trainiertes Modell.
Danach fragt sie das Modell nach einer Aktion.

Diese Datei ist Blackbox-Code.
"""

import os

import joblib

from engine.snake_logic import ACTION_LEFT, ACTION_RIGHT, ACTION_STRAIGHT
from student_config import MODEL_PATH


ALLOWED_ACTIONS = [ACTION_LEFT, ACTION_STRAIGHT, ACTION_RIGHT]


def load_model(model_path=MODEL_PATH):
    """
    Lädt ein trainiertes Modell.

    Wenn kein Modell gefunden wird, gibt die Funktion None zurück.
    """
    if not os.path.exists(model_path):
        return None

    return joblib.load(model_path)


def predict_action(model, features):
    """
    Fragt das Modell nach der nächsten Aktion.

    Rückgabe:
        0 = links
        1 = geradeaus
        2 = rechts
    """
    if model is None:
        return ACTION_STRAIGHT

    prediction = model.predict([features])[0]
    action = int(prediction)

    if action not in ALLOWED_ACTIONS:
        return ACTION_STRAIGHT

    return action