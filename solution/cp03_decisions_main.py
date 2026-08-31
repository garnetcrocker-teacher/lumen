"""
INSTRUCTOR REFERENCE - a correct Checkpoint 3 main.py (the three function bodies).
Do not ship this to students.

The two lines below put the repo root on the import path so `import engine`
finds the one canonical engine.py, no matter where you run this from.
"""

import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import engine


# --- BEGIN YOUR CODE ---------------------------------------------------------

def hull_status(depth_m, rated_m):
    if depth_m < rated_m:
        return "OK"
    elif depth_m < 1.5 * rated_m:
        return "CAUTION"
    else:
        return "BREACH"


def oxygen_state(oxygen_pct):
    if oxygen_pct > 50:
        return "GOOD"
    elif oxygen_pct > 15:
        return "LOW"
    else:
        return "CRITICAL"


def can_descend(ballast_kg, power_pct):
    return ballast_kg > 0 and power_pct > 0

# --- END YOUR CODE ---------------------------------------------------------


def frame(sub, screen):
    engine.draw_hull_status(screen, hull_status(sub.depth, sub.rated_depth))
    engine.draw_text(screen, "O2: " + oxygen_state(sub.oxygen),
                     (engine.WIDTH // 2, 46), size=15, anchor="midtop",
                     color=(150, 190, 210))

    if engine.key_down("DOWN") and can_descend(sub.ballast, sub.power):
        sub.descending = True
    if engine.key_down("UP"):
        sub.ascending = True
    if engine.key_pressed("L"):
        sub.light_on = not sub.light_on

    engine.draw_text(screen, "DOWN dive   UP rise   L light   ESC quit",
                     (16, engine.HEIGHT - 26), size=13, color=(120, 140, 155))


engine.run(frame)
