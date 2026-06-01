# SnakeTrainer

## Name

Name:Stefan Filipov
Name:abdurahman kahssai

## Projektziel

Ich habe ein Snake-Spiel mit einem einfachen KI-Modus erstellt.

## Was habe ich geändert?

- Änderung 1: student_config.py
- Änderung 2: student_tasks.py
- Änderung 3:

## Was versteht die KI?

Die KI bekommt keine Bilder.

Sie bekommt Zahlen.

Diese Zahlen beschreiben die Spielsituation.

Beispiele:

- Gefahr vorne
- Gefahr links
- Futter links
- Futter rechts
- aktuelle Richtung

## Wie habe ich getestet?

Ich habe diesen Befehl ausgeführt:

```bash
pytest

````
## 3 Features aus dem Skript
- danger_front: Ist 1 wenn die Schlange bei einem Schritt geradeaus gegen eine Wand oder ihren Körper treffen würde, ansonsten wenn der Weg frei ist dann 0
- food_left: Ist 1 wenn das Futter links vom Kopf der Schlange liegt ansonsten 0
- direction_right: Ist 1 wenn sich die Schlange aktuell nach rechts bewegt ansonsten 0

## Notizen
#Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
