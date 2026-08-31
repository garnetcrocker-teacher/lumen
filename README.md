# LUMEN

A semester-long Pygame project for **Intro to Python**. Students build one game
across 12 weekly checkpoints - one per textbook module - and by the end they have
a full, working game they wrote themselves.

**LUMEN** is an atmospheric deep-sea game: you pilot a research submersible down a
black ocean trench, manage oxygen / battery / hull pressure, and catalog the
bioluminescent creatures you find in the dark. Low-twitch, exploration-driven,
drawn entirely with simple shapes and glow.

---

## For the instructor

Start with **[INSTRUCTOR.md](INSTRUCTOR.md)** - repo layout, the semester map
(module -> checkpoint), how to edit and sync the engine, and how grading works.

## For students

- **[SETUP.md](SETUP.md)** - one-time virtual-environment setup (do this first)
- **[student_handout.md](student_handout.md)** - how the checkpoints work, and
  how to join late without penalty
- Each `checkpoints/cpNN_*/` folder has its own `briefing.md`

## Quick start

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1            # PowerShell; see SETUP.md for cmd / macOS
python -m pip install -r requirements.txt

cd checkpoints\cp02_io
python main.py
python check.py
```

## Requirements

Python 3.10+ and `pygame-ce` (see `requirements.txt`). Everything is drawn with
`pygame.draw` - no art assets to manage.

## Build status

`engine.py` v1.0 and checkpoints **cp02**, **cp03** are complete. cp04-cp12 and
the full reference game are in progress - see the checklist at the bottom of
`INSTRUCTOR.md`.
