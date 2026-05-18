"""
Reine Spiellogik für Snake.

Diese Datei zeichnet nichts auf den Bildschirm.
Sie berechnet nur Bewegung und Kollision.

Diese Datei ist Arbeits-Code.
Einige Funktionen sollst du grob verstehen.
"""

ACTION_LEFT = 0
ACTION_STRAIGHT = 1
ACTION_RIGHT = 2

DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)
DIRECTION_LEFT = (-1, 0)
DIRECTION_RIGHT = (1, 0)


def turn_direction(direction, action):
    """
    Berechnet die neue Richtung nach einer Aktion.

    Args:
        direction: aktuelle Richtung, zum Beispiel (1, 0)
        action: 0 = links, 1 = geradeaus, 2 = rechts
    """
    dx, dy = direction

    if action == ACTION_STRAIGHT:
        return direction

    if action == ACTION_LEFT:
        return (dy, -dx)

    if action == ACTION_RIGHT:
        return (-dy, dx)

    raise ValueError("Unbekannte Aktion")


def get_next_position(head, direction):
    """
    Berechnet die nächste Position des Snake-Kopfes.
    """
    return (head[0] + direction[0], head[1] + direction[1])


def is_collision(position, snake_body, grid_width, grid_height):
    """
    Prüft, ob eine Position mit Wand oder Körper kollidiert.
    """
    x, y = position

    if x < 0 or x >= grid_width:
        return True

    if y < 0 or y >= grid_height:
        return True

    if position in snake_body:
        return True

    return False


def get_relative_action(current_direction, desired_direction):
    """
    Wandelt eine gewünschte Richtung in eine relative Aktion um.

    Beispiel:
        aktuelle Richtung: rechts
        gewünschte Richtung: oben
        Ergebnis: links drehen
    """
    if desired_direction == current_direction:
        return ACTION_STRAIGHT

    if desired_direction == turn_direction(current_direction, ACTION_LEFT):
        return ACTION_LEFT

    if desired_direction == turn_direction(current_direction, ACTION_RIGHT):
        return ACTION_RIGHT

    # Eine direkte Umkehr ist bei Snake nicht erlaubt.
    return None