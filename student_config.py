"""
Diese Datei darfst du verändern.

Hier kannst du das Aussehen und das Spielgefühl anpassen.
"""

# Spielfeld
GRID_WIDTH = 24
GRID_HEIGHT = 24 # Erste änderung: von 18 auf 24
GRID_SIZE = 20

# Spielgeschwindigkeit
SNAKE_SPEED = 6 # Zweite änderung: von 7 auf 6

# Farben
BACKGROUND_COLOR = "black"
GRID_COLOR = "darkgray"
SNAKE_COLOR = "green"
SNAKE_HEAD_COLOR = "darkgreen" # Dritte änderung: von lime auf darkgreen
FOOD_COLOR = "red"
TEXT_COLOR = "white"

# Texte
GAME_TITLE = "SnakeTrainer"
HUMAN_MODE_TEXT = "Modus: Mensch"
AI_MODE_TEXT = "Modus: KI"
GAME_OVER_TEXT = " Du hast verloren! - Drücke R für Neustart"

# KI
USE_AI_BY_DEFAULT = False

# Trainingsdaten
SAVE_HUMAN_DATA = True
TRAINING_DATA_PATH = "data/snake_training.csv"
FALLBACK_TRAINING_DATA_PATH = "data/example_training.csv"
MODEL_PATH = "models/snake_mlp.joblib"