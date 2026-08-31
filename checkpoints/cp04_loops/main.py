"""
LUMEN - Checkpoint 4
Module 4: Repetition Structures

    Run the game:      python main.py      (press ESC or close the window to quit)
    Check your work:    python check.py

You fill in the BODIES of the three functions between the dashed lines.
Do NOT change the `def` lines, and do NOT touch anything below `END YOUR CODE`.

Controls once it runs:  DOWN = dive,  UP = rise,  L = toggle light
"""

import engine

METRES_PER_PERCENT = 20       # every 1 percent of battery is worth 20 m of descent
TICK_STEP = 100               # draw a depth marker every this many metres
TICK_MAX = 2000               # ... from 0 m down to this depth

# --- BEGIN YOUR CODE ---------------------------------------------------------

def read_valid_depth():
    """Ask the pilot 'Target depth (m): ' and read a whole number.

    If the number is less than 1 or greater than 6000, print
        Out of range - enter 1 to 6000.
    and ask again. Keep looping until the number is in range, then return it
    as an int.

    Use a while loop. (Assume the pilot types digits - handling bad text like
    "abc" comes in Module 6.)
    """
    return 0


def max_safe_depth(start_power):
    """Return how many whole metres the sub can descend before the battery dies.

    Start at depth 0 with `start_power` percent of battery. Using a while loop,
    for as long as there is at least 1 whole percent of power left, spend
    1 percent and go METRES_PER_PERCENT metres deeper. Return the depth
    reached, as an int.

    Examples:  max_safe_depth(100) -> 2000     max_safe_depth(1) -> 20
               max_safe_depth(2)   -> 40       max_safe_depth(0) -> 0
    """
    return 0


def draw_depth_ticks(screen, sub):
    """Draw a depth marker every TICK_STEP metres, from 0 m down to TICK_MAX.

    Use a for loop over range(0, TICK_MAX + 1, TICK_STEP). For each depth d:
        y = engine.world_y_to_screen(sub, d)     # d in metres -> y in pixels
        engine.draw_tick(screen, y, d)           # draws the line + label
    """
    pass

# --- END YOUR CODE ---------------------------------------------------------


def frame(sub, screen):
    draw_depth_ticks(screen, sub)
    engine.draw_text(screen, f"POWER RANGE: {max_safe_depth(sub.power)} m",
                     (engine.WIDTH // 2, 16), size=16, anchor="midtop",
                     color=(150, 190, 210))

    if engine.key_down("DOWN"):
        sub.descending = True
    if engine.key_down("UP"):
        sub.ascending = True
    if engine.key_pressed("L"):
        sub.light_on = not sub.light_on

    engine.draw_text(screen, "DOWN dive   UP rise   L light   ESC quit",
                     (16, engine.HEIGHT - 26), size=13, color=(120, 140, 155))


if __name__ == "__main__":
    print("=" * 40)
    print("     LUMEN  -  DIVE CLEARANCE")
    print("=" * 40)
    cleared_depth = read_valid_depth()
    print(f"Cleared to dive to {cleared_depth} m.")
    engine.save_diveplan("Pilot", cleared_depth, 40.0, 100.0)
    engine.run(frame)
