"""
LUMEN - Checkpoint 3
Module 3: Decision Structures and Boolean Logic

    Run the game:      python main.py      (press ESC or close the window to quit)
    Check your work:    python check.py

Your job this week is the THREE functions in the YOUR CODE section below.

frame() below your code is provided - the engine calls it every frame, nothing
to change there.

Your Checkpoint 2 pre-dive intake is at the BOTTOM of this file, in the
`if __name__ == "__main__":` block. A working reference version is filled in so
the game runs. If you did Checkpoint 2, paste your own version in over it - this
is your game now.

Controls once it runs:  DOWN = dive,  UP = rise,  L = toggle light
"""

import engine

DESCENT_RATE = 20.0        # named constant, from Checkpoint 2

# --- BEGIN YOUR CODE (Checkpoint 3) ----------------------------------------

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

# --- END YOUR CODE -------------------------------------------------------


def frame(sub, screen):
    """The engine calls this ~60 times a second. It already uses your three
    functions - nothing to change here. (You'll learn to write functions like
    this one in Module 5.)"""
    engine.draw_hull_status(screen, hull_status(sub.depth, sub.rated_depth))
    engine.draw_hud_text("O2: " + oxygen_state(sub.oxygen),
                         (engine.WIDTH // 2, 46), size=15, anchor="midtop",
                         color=(150, 190, 210))

    if engine.key_down("DOWN") and can_descend(sub.ballast, sub.power):
        sub.descending = True
    if engine.key_down("UP"):
        sub.ascending = True
    if engine.key_pressed("L"):
        sub.light_on = not sub.light_on

    engine.draw_hud_text("DOWN dive   UP rise   L light   ESC quit",
                         (16, engine.HEIGHT - 26), size=13, color=(120, 140, 155))


# ============ YOUR CODE - CHECKPOINT 2 (carried over) ======================
#  Your pre-dive intake from Checkpoint 2. This is a working reference version
#  so the game runs - replace it with your own Checkpoint 2 code if you have it.
#  `if __name__ == "__main__":` just means "only run this when you play the game
#  directly"; write the intake lines indented under it. More on it later.
# ==========================================================================
if __name__ == "__main__":
    print("=" * 40)
    print("        LUMEN  -  PRE-DIVE INTAKE")
    print("=" * 40)
    pilot = input("Pilot name: ")
    target_depth = int(input("Target depth (m): "))
    ballast_kg = float(input("Ballast (kg): "))
    battery_pct = float(input("Battery (%): "))
    descent_seconds = target_depth / DESCENT_RATE

    print()
    print("--- DIVE PLAN ---")
    print("Pilot:         ", pilot)
    print("Target depth:  ", target_depth, "m")
    print("Ballast:       ", ballast_kg, "kg")
    print("Battery:       ", battery_pct, "%")
    print(f"Descent time:   {descent_seconds:.1f} s")

    engine.save_diveplan(pilot, target_depth, ballast_kg, battery_pct)
    # ============ end Checkpoint 2 ============

    engine.run(frame)      # launch the dive with the plan you just entered
