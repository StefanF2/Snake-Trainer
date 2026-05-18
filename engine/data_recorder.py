"""
Speichern von Trainingsdaten.

Diese Datei schreibt Spielzustände und Aktionen in eine CSV-Datei.
Damit kann später ein Modell trainiert werden.

Diese Datei ist Blackbox-Code.
Du darfst sie benutzen.
Du musst sie nicht vollständig verstehen.
"""

import csv
import os

from engine.features import FEATURE_NAMES
from engine.snake_logic import ACTION_LEFT, ACTION_RIGHT, ACTION_STRAIGHT
from student_config import TRAINING_DATA_PATH


CSV_HEADER = FEATURE_NAMES + ["action"]
ALLOWED_ACTIONS = [ACTION_LEFT, ACTION_STRAIGHT, ACTION_RIGHT]


def ensure_data_file(data_path=TRAINING_DATA_PATH):
    """
    Erstellt die Trainingsdatei, falls sie noch nicht existiert.
    """
    folder = os.path.dirname(data_path)

    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    if os.path.exists(data_path):
        return

    with open(data_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(CSV_HEADER)


def save_training_row(features, action, data_path=TRAINING_DATA_PATH):
    """
    Speichert eine einzelne Trainingszeile.
    """
    if len(features) != len(FEATURE_NAMES):
        raise ValueError("Die Anzahl der Features stimmt nicht.")

    if action not in ALLOWED_ACTIONS:
        raise ValueError("Die Aktion ist ungültig.")

    ensure_data_file(data_path)

    row = list(features) + [action]

    with open(data_path, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row)