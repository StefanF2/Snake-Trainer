"""
Erzeugt Trainingsdaten für SnakeTrainer.

Diese Datei ist Blackbox-Code.

Sie erstellt viele Beispiele für die KI.
Ein einfacher Regel-Lehrer entscheidet:

1. Nicht in eine Wand oder in den Körper fahren.
2. Möglichst in Richtung Futter gehen.
3. Wenn mehrere Aktionen möglich sind, wird eine gute Aktion gewählt.

Die erzeugten Daten werden in data/snake_training.csv gespeichert.
Danach kann das Modell mit train_model.py trainiert werden.

Wichtig:
Diese Datei überschreibt data/snake_training.csv.
"""

import csv
import os
import random
from collections import Counter

from engine.features import FEATURE_NAMES
from engine.snake_logic import (
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_STRAIGHT,
    DIRECTION_DOWN,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_UP,
    turn_direction,
)
from student_config import TRAINING_DATA_PATH


ROWS_PER_PATTERN = 20
RANDOM_SEED = 42

ACTIONS = [ACTION_LEFT, ACTION_STRAIGHT, ACTION_RIGHT]
DIRECTIONS = [DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT, DIRECTION_RIGHT]

ACTION_NAMES = {
    ACTION_LEFT: "links",
    ACTION_STRAIGHT: "geradeaus",
    ACTION_RIGHT: "rechts",
}


def get_direction_features(direction):
    """
    Wandelt eine Richtung in vier Zahlen um.

    Beispiel:
        Richtung rechts = [0, 0, 0, 1]
    """
    direction_up = int(direction == DIRECTION_UP)
    direction_down = int(direction == DIRECTION_DOWN)
    direction_left = int(direction == DIRECTION_LEFT)
    direction_right = int(direction == DIRECTION_RIGHT)

    return [
        direction_up,
        direction_down,
        direction_left,
        direction_right,
    ]


def get_food_relations():
    """
    Erstellt mögliche Positionen des Futters relativ zur Snake.

    Das Futter kann links, rechts, oben oder unten liegen.
    Es kann auch diagonal liegen.
    """
    x_relations = [
        (1, 0),  # Futter links
        (0, 0),  # gleiche Spalte
        (0, 1),  # Futter rechts
    ]

    y_relations = [
        (1, 0),  # Futter oben
        (0, 0),  # gleiche Zeile
        (0, 1),  # Futter unten
    ]

    relations = []

    for food_left, food_right in x_relations:
        for food_up, food_down in y_relations:
            # Das Futter soll nicht genau auf dem Kopf liegen.
            if food_left == 0 and food_right == 0 and food_up == 0 and food_down == 0:
                continue

            relations.append(
                (food_left, food_right, food_up, food_down)
            )

    return relations


def get_danger_patterns():
    """
    Erstellt alle Kombinationen von Gefahr vorne, links und rechts.
    """
    patterns = []

    for danger_front in [0, 1]:
        for danger_left in [0, 1]:
            for danger_right in [0, 1]:
                patterns.append(
                    (danger_front, danger_left, danger_right)
                )

    return patterns


def score_direction(new_direction, food_left, food_right, food_up, food_down):
    """
    Bewertet, ob eine Richtung zum Futter passt.

    Hohe Punktzahl bedeutet:
        Diese Richtung ist gut.

    Tiefe Punktzahl bedeutet:
        Diese Richtung geht eher vom Futter weg.
    """
    dx, dy = new_direction
    score = 0

    if food_right:
        if dx == 1:
            score += 3
        elif dx == -1:
            score -= 2

    if food_left:
        if dx == -1:
            score += 3
        elif dx == 1:
            score -= 2

    if food_down:
        if dy == 1:
            score += 3
        elif dy == -1:
            score -= 2

    if food_up:
        if dy == -1:
            score += 3
        elif dy == 1:
            score -= 2

    return score


def choose_teacher_action(
    direction,
    danger_front,
    danger_left,
    danger_right,
    food_left,
    food_right,
    food_up,
    food_down,
):
    """
    Wählt eine gute Aktion für einen Spielzustand.

    Diese Funktion ist der Regel-Lehrer.
    Er erzeugt die richtige Antwort für die Trainingsdaten.
    """
    danger_by_action = {
        ACTION_STRAIGHT: danger_front,
        ACTION_LEFT: danger_left,
        ACTION_RIGHT: danger_right,
    }

    safe_actions = []

    for action in ACTIONS:
        if danger_by_action[action] == 0:
            safe_actions.append(action)

    # Wenn alles gefährlich ist, gibt es keine gute Lösung mehr.
    # Dann nehmen wir geradeaus als Notfallwert.
    if not safe_actions:
        return ACTION_STRAIGHT

    best_action = safe_actions[0]
    best_score = -999

    for action in safe_actions:
        new_direction = turn_direction(direction, action)

        score = score_direction(
            new_direction,
            food_left,
            food_right,
            food_up,
            food_down,
        )

        # Kleine Bevorzugung für geradeaus.
        # Dadurch fährt die Snake ruhiger, wenn es sinnvoll ist.
        if action == ACTION_STRAIGHT:
            score += 0.2

        # Kleine zufällige Variation.
        # Dadurch entstehen nicht immer exakt gleiche Muster.
        score += random.random() * 0.01

        if score > best_score:
            best_score = score
            best_action = action

    return best_action


def create_feature_row(
    direction,
    danger_front,
    danger_left,
    danger_right,
    food_left,
    food_right,
    food_up,
    food_down,
):
    """
    Erstellt eine Feature-Zeile im gleichen Format wie features.py.
    """
    direction_features = get_direction_features(direction)

    return [
        danger_front,
        danger_left,
        danger_right,
        food_left,
        food_right,
        food_up,
        food_down,
    ] + direction_features


def generate_rows():
    """
    Erstellt viele Trainingszeilen.
    """
    rows = []
    food_relations = get_food_relations()
    danger_patterns = get_danger_patterns()

    for direction in DIRECTIONS:
        for danger_front, danger_left, danger_right in danger_patterns:
            for food_left, food_right, food_up, food_down in food_relations:
                features = create_feature_row(
                    direction,
                    danger_front,
                    danger_left,
                    danger_right,
                    food_left,
                    food_right,
                    food_up,
                    food_down,
                )

                action = choose_teacher_action(
                    direction,
                    danger_front,
                    danger_left,
                    danger_right,
                    food_left,
                    food_right,
                    food_up,
                    food_down,
                )

                row = features + [action]

                for _ in range(ROWS_PER_PATTERN):
                    rows.append(row)

    random.shuffle(rows)
    return rows


def write_csv(rows, data_path):
    """
    Speichert die erzeugten Trainingsdaten als CSV-Datei.
    """
    folder = os.path.dirname(data_path)

    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    header = FEATURE_NAMES + ["action"]

    with open(data_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(rows)


def print_summary(rows):
    """
    Gibt eine kurze Zusammenfassung aus.
    """
    action_counter = Counter(row[-1] for row in rows)

    print("Trainingsdaten erzeugt")
    print(f"Anzahl Zeilen: {len(rows)}")
    print()

    for action in ACTIONS:
        count = action_counter[action]
        name = ACTION_NAMES[action]
        print(f"Aktion {action} ({name}): {count}")

    print()
    print(f"Gespeichert unter: {TRAINING_DATA_PATH}")


def main():
    """
    Hauptprogramm.
    """
    random.seed(RANDOM_SEED)

    rows = generate_rows()
    write_csv(rows, TRAINING_DATA_PATH)
    print_summary(rows)


if __name__ == "__main__":
    main()