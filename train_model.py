"""
Training des KI-Modells.

Diese Datei liest Trainingsdaten aus einer CSV-Datei.
Danach wird ein kleines neuronales Netz trainiert.

Diese Datei ist fast vollständig Blackbox-Code.
Du führst sie aus.
Du darfst einzelne Werte ändern, wenn du eine Wahlaufgabe machst.
"""

import os

import joblib
import pandas as pd

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

from engine.features import FEATURE_NAMES
from student_config import (
    FALLBACK_TRAINING_DATA_PATH,
    MODEL_PATH,
    TRAINING_DATA_PATH,
)


def choose_data_path():
    """
    Wählt die passende Trainingsdatei.

    Wenn eigene Trainingsdaten vorhanden sind, werden diese genutzt.
    Sonst wird die Beispieldatei verwendet.
    """
    if os.path.exists(TRAINING_DATA_PATH):
        data = pd.read_csv(TRAINING_DATA_PATH)

        if len(data) >= 8:
            return TRAINING_DATA_PATH

    return FALLBACK_TRAINING_DATA_PATH


def train_model(data_path=None, model_path=MODEL_PATH):
    """
    Trainiert ein MLP-Modell mit Snake-Daten.
    """
    if data_path is None:
        data_path = choose_data_path()

    if not os.path.exists(data_path):
        raise FileNotFoundError("Keine Trainingsdatei gefunden.")

    data = pd.read_csv(data_path)

    if len(data) < 8:
        raise ValueError("Es sind zu wenige Trainingsdaten vorhanden.")

    required_columns = FEATURE_NAMES + ["action"]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"Spalte fehlt: {column}")

    x_values = data[FEATURE_NAMES]
    y_values = data["action"]

    if len(data) >= 12:
        x_train, x_test, y_train, y_test = train_test_split(
            x_values,
            y_values,
            test_size=0.25,
            random_state=42,
        )
    else:
        x_train = x_values
        x_test = x_values
        y_train = y_values
        y_test = y_values

    # TODO WAHL MITTEL:
    # Du darfst hidden_layer_sizes verändern.
    # Beispiel: (8,), (12,), (20,), (12, 6)
    model = MLPClassifier(
        hidden_layer_sizes=(12,),
        activation="relu",
        max_iter=1000,
        random_state=42,
    )

    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    model_folder = os.path.dirname(model_path)

    if model_folder and not os.path.exists(model_folder):
        os.makedirs(model_folder)

    joblib.dump(model, model_path)

    print(f"Verwendete Trainingsdatei: {data_path}")
    print(f"Trainingszeilen: {len(data)}")
    print(f"Testgenauigkeit: {accuracy:.2f}")
    print(f"Modell gespeichert unter: {model_path}")

    return accuracy


if __name__ == "__main__":
    train_model()