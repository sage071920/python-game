# Mein Pygame Survival Spiel

Ein einfaches Survival-Spiel erstellt mit Pygame, bei dem Spieler Ressourcen sammeln, craften und eine Welt erkunden können.

## Features
- Spielerbewegung mit Energie-System
- Inventar-Management
- Crafting-System
- Chunk-basierte Welt
- Interaktive Items (Holz, Stein, etc.)
- Pausenmenü

## Voraussetzungen
- Python 3.11.9
- Pygame
- Pillow (PIL)

## Installation
1. Repository klonen:
   ```bash
   git clone https://github.com/sage071920/python-game.git

	2.	Abhängigkeiten installieren:

pip install -r requirements.txt


	3.	Spiel starten:

python src/main.py



Steuerung
	•	WASD / Pfeiltasten: Bewegung
	•	Shift: Sprinten (verbraucht Energie)
	•	E: Mit Items interagieren
	•	Q: Item droppen
	•	1-5: Inventar-Slots auswählen
	•	I: Crafting-Menü öffnen
	•	ESC: Pausenmenü

Projektstruktur

mein-spiel/
├── src/                # Quellcode
│   ├── main.py        # Hauptspiel-Logik
│   ├── player.py      # Spieler-Klasse
│   ├── items.py       # Item-System
│   └── dungeon.py     # Dungeon-Logik
├── pngs/              # Bildressourcen
└── README.md          # Dokumentation

Bekannte Abhängigkeiten
	•	pygame: Für die Spiel-Engine
	•	PIL: Für Bildverarbeitung
	•	random: Für Zufallsgenerierung

Hinweise
	•	Stelle sicher, dass alle PNG-Dateien im pngs/-Verzeichnis vorhanden sind.
	•	Das Spiel speichert Screenshots temporär im pngs/-Verzeichnis.
