"""
In dieser Datei löst du kleine Programmieraufgaben.

Die Funktionen werden vom Spiel verwendet.
Du kannst sie mit pytest testen.
"""

from student_config import AI_MODE_TEXT, HUMAN_MODE_TEXT


def format_score(score):
    """
    Erstellt den Text für die Punkteanzeige.

    Beispiel:
        score = 5
        Rückgabe: "Score: 5"
    """
    # TODO PFLICHT LEICHT:
    # Verändere den Text, wenn du möchtest.
    # Beispiel: "Punkte: 5"
    return f"Punktzahl: <{score}>" # Änderung 1: Von Score: auf Punktzahl:


def format_high_score(high_score):
    """
    Erstellt den Text für den Highscore.

    Beispiel:
        high_score = 12
        Rückgabe: "Highscore: 12"
    """
    # TODO PFLICHT LEICHT:
    # Gib einen Text mit dem Highscore zurück.
    return f"Highscore: <{high_score}>"

def get_mode_text(ai_mode):
    """
    Erstellt den Text für den aktuellen Spielmodus.

    Args:
        ai_mode: True bedeutet KI-Modus.
        ai_mode: False bedeutet Mensch-Modus.
    """
    # TODO PFLICHT MITTEL:
    # Lies die if-Anweisung.
    # Erkläre in deiner Dokumentation, was hier passiert.
    if ai_mode:
        return AI_MODE_TEXT + "-Modus"

    return HUMAN_MODE_TEXT + "-Modus" 


def is_high_score(score, high_score):
    """
    Prüft, ob ein neuer Highscore erreicht wurde.
    """
    # TODO PFLICHT LEICHT:
    # Diese Funktion soll True zurückgeben,
    # wenn score grösser ist als high_score.
    return score > high_score


def get_ai_status_text(model_loaded):
    """
    Erstellt eine kurze Meldung für den KI-Modus.
    """
    # TODO WAHL MITTEL:
    # Passe die Texte an.
    if model_loaded:
        return "KI-Modell geladen"

    return "Kein KI-Modell gefunden"