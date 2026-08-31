"""
LUMEN - Checkpoint 3
Module 3: Decision Structures and Boolean Logic

    Run the game:      python main.py      (press ESC or close the window to quit)
    Check your work:   python check.py

You fill in the BODIES of the three functions between the dashed lines.
Do NOT change the `def` lines. Do NOT touch frame() or the last line.

Controls once it runs:  DOWN = dive,  UP = rise,  L = toggle light
"""

import engine

# --- BEGIN YOUR CODE ---------------------------------------------------------

def hull_status(depth_m, rated_m):
    """Return a string describing the pressure load on the hull:

        "OK"       when depth_m is less than rated_m
        "CAUTION"  when depth_m is at least rated_m but less than 1.5 * rated_m
        "BREACH"   when depth_m is at least 1.5 * rated_m

    Example:  hull_status(500, 1000)  ->  "OK"
              hull_status(1000, 1000) ->  "CAUTION"
              hull_status(1500, 1000) ->  "BREACH"
    """
    return "OK"          # replace this with an if / elif / else


def oxygen_state(oxygen_pct):
    """Return a string for the current oxygen level:

        "GOOD"      when oxygen_pct is greater than 50
        "LOW"       when oxygen_pct is greater than 15 but not greater than 50
        "CRITICAL"  when oxygen_pct is 15 or less
    """
    return "GOOD"        # replace this with an if / elif / else


def can_descend(ballast_kg, power_pct):
    """Return True only when it is safe to dive deeper:
    there must be ballast left (more than 0 kg) AND
    some battery power left (more than 0 percent).
    Otherwise return False.

    Use the `and` keyword.
    """
    return True          # replace this with a boolean expression

# --- END YOUR CODE ---------------------------------------------------------


def frame(sub, screen):
    """The engine calls this ~60 times a second. It already uses your three
    functions - you don't need to change anything in here."""
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
