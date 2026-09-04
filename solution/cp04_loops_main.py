"""
INSTRUCTOR REFERENCE - a correct Checkpoint 4 main.py (the three function bodies).
Do not ship this to students.

The sys.path shim lets this run from any working directory.
"""

import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import engine

METERS_PER_PERCENT = 20
TICK_STEP = 100
TICK_MAX = 2000

# --- BEGIN YOUR CODE ---------------------------------------------------------

def read_valid_depth():
    depth = int(input("Target depth (m): "))
    while depth < 1 or depth > 6000:
        print("Out of range - enter 1 to 6000.")
        depth = int(input("Target depth (m): "))
    return depth


def max_safe_depth(start_power):
    power = start_power
    depth = 0
    while power >= 1:
        power -= 1
        depth += METERS_PER_PERCENT
    return depth


def draw_depth_ticks(screen, sub):
    for d in range(0, TICK_MAX + 1, TICK_STEP):
        y = engine.world_y_to_screen(sub, d)
        engine.draw_tick(screen, y, d)

# --- END YOUR CODE ---------------------------------------------------------


def frame(sub, screen):
    draw_depth_ticks(screen, sub)
    engine.draw_hud_text(f"POWER RANGE: {max_safe_depth(sub.power)} m",
                         (engine.WIDTH // 2, 16), size=16, anchor="midtop",
                         color=(150, 190, 210))

    if engine.key_down("DOWN"):
        sub.descending = True
    if engine.key_down("UP"):
        sub.ascending = True
    if engine.key_pressed("L"):
        sub.light_on = not sub.light_on

    engine.draw_hud_text("DOWN dive   UP rise   L light   ESC quit",
                         (16, engine.HEIGHT - 26), size=13, color=(120, 140, 155))


if __name__ == "__main__":
    print("=" * 40)
    print("     LUMEN  -  DIVE CLEARANCE")
    print("=" * 40)
    cleared_depth = read_valid_depth()
    print(f"Cleared to dive to {cleared_depth} m.")
    engine.save_diveplan("Pilot", cleared_depth, 40.0, 100.0)
    engine.run(frame)
