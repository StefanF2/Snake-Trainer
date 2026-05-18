"""
Diese Datei darfst du verändern.

Hier kannst du das Aussehen und das Spielgefühl anpassen.
"""

# Spielfeld
GRID_WIDTH = 24
GRID_HEIGHT = 18
GRID_SIZE = 20

# Spielgeschwindigkeit
SNAKE_SPEED = 7

# Farben
BACKGROUND_COLOR = "black"
GRID_COLOR = "darkslategray"
SNAKE_COLOR = "green"
SNAKE_HEAD_COLOR = "lime"
FOOD_COLOR = "red"
TEXT_COLOR = "white"

# Texte
GAME_TITLE = "SnakeTrainer"
HUMAN_MODE_TEXT = "Modus: Mensch"
AI_MODE_TEXT = "Modus: KI"
GAME_OVER_TEXT = "Game Over - Drücke R für Neustart"

# KI
USE_AI_BY_DEFAULT = False

# Trainingsdaten
SAVE_HUMAN_DATA = True
TRAINING_DATA_PATH = "data/snake_training.csv"
FALLBACK_TRAINING_DATA_PATH = "data/example_training.csv"
MODEL_PATH = "models/snake_mlp.joblib"