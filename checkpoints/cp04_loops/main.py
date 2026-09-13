"""
LUMEN - Checkpoint 4
Module 4: Repetition Structures

    Run the game:      python main.py      (press ESC or close the window to quit)
    Check your work:    python check.py

Your job this week is the FOUR functions in the YOUR CODE section below.

frame() below your code is provided - the engine calls it every frame, nothing
to change there.

Checkpoints 2 and 3 are carried into the BOTTOM of this file:
  - Checkpoint 3's five functions (clamp_battery, hull_status, oxygen_state,
    can_descend, overall_alert) are reference versions, defined at the bottom.
  - Checkpoint 2's pre-dive intake is inside `if __name__ == "__main__":`,
    below that.
Working reference versions are filled in so the game runs either way - if you
did those checkpoints, paste your own versions in over them. (Keep the
clamp_battery(...) wrapper on the battery line, and note that the target depth
line now calls this week's read_valid_depth() instead of a plain int(input()).)

Controls once it runs:  DOWN = dive,  UP = rise,  L = toggle light
"""

import engine

DESCENT_RATE = 20.0           # named constant, from Checkpoint 2

OK_COLOR = (90, 200, 150)      # same colors draw_hull_status() uses
CAUTION_COLOR = (230, 190, 90)
BREACH_COLOR = (230, 90, 80)

METERS_PER_PERCENT = 20       # every 1 percent of battery is worth 20 m of descent
TICK_STEP = 100               # draw a depth marker every this many meters
TICK_MAX = 2000               # ... from 0 m down to this depth

SONAR_RANGE_MAX = 400         # how far sonar reaches, in pixels, at full battery
                               # (compare: the light only reaches 155 - sonar
                               # is your long-range sense, light is close-range detail)
SWEEP_SECONDS = 2.5           # how long one ping takes to travel out to max range
PULSE_COUNT = 4               # how many pulses are traveling outward at once

# --- BEGIN YOUR CODE (Checkpoint 4) -----------------------------------------

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
    """Return how many whole meters the sub can descend before the battery dies.

    Start at depth 0 with `start_power` percent of battery. Using a while loop,
    for as long as there is at least 1 whole percent of power left, spend
    1 percent and go METERS_PER_PERCENT meters deeper. Return the depth
    reached, as an int.

    Examples:  max_safe_depth(100) -> 2000     max_safe_depth(1) -> 20
               max_safe_depth(2)   -> 40       max_safe_depth(0) -> 0
    """
    return 0


def draw_depth_ticks(screen, sub):
    """Draw a depth marker every TICK_STEP meters, from 0 m down to TICK_MAX,
    colored by how dangerous that depth is - reusing hull_status() from
    Checkpoint 3 (it's carried over at the bottom of this file).

    Use a for loop over range(0, TICK_MAX + 1, TICK_STEP). For each depth d:
        - status = hull_status(d, sub.rated_depth)
        - pick a color: "OK" -> OK_COLOR, "CAUTION" -> CAUTION_COLOR,
          "BREACH" -> BREACH_COLOR
        - y = engine.world_y_to_screen(sub, d)     # d in meters -> y in pixels
        - engine.draw_tick(screen, y, d, color)    # draws the line + label
    """
    pass


def draw_sonar_rings(screen, sub):
    """Sonar reaches much farther than your light, and it isn't a fixed
    picture - a handful of pulses are always traveling outward and looping
    back, like a real active sonar ping. Range still depends on battery, same
    as the light.

    1. How far sonar reaches right now (0 at dead battery, SONAR_RANGE_MAX at
       a full one):
           sonar_range = sub.power * (SONAR_RANGE_MAX / 100)

    2. Loop `for i in range(PULSE_COUNT):` - each pulse starts at a different
       point along its outward trip so they end up evenly spread out:
           offset = i / PULSE_COUNT                 # 0, 0.25, 0.5, 0.75 for 4
           fraction = (engine.now() / SWEEP_SECONDS + offset) % 1.0
           radius = fraction * sonar_range
           engine.draw_ring(screen, (engine.WIDTH // 2, engine.SUB_SCREEN_Y), radius)

    `engine.now()` returns seconds since the game started, and it only ever
    goes up. Dividing by SWEEP_SECONDS and taking `% 1.0` is what turns that
    into a value that counts from 0 up to 1 and then starts over every
    SWEEP_SECONDS - that reset is what makes each pulse look like it travels
    out to sonar_range and then begins again at the sub, over and over.
    """
    pass

# --- END YOUR CODE -----------------------------------------------------------


def frame(sub, screen):
    """The engine calls this ~60 times a second. It already uses your four
    functions plus everything carried over from Checkpoint 3 - nothing to
    change here."""
    draw_sonar_rings(screen, sub)
    draw_depth_ticks(screen, sub)

    hull = hull_status(sub.depth, sub.rated_depth)
    oxy = oxygen_state(sub.oxygen)
    alert = overall_alert(hull, oxy)

    engine.draw_hull_status(screen, hull)
    engine.draw_hud_text("O2: " + oxy, (engine.WIDTH // 2, 46), size=15,
                         anchor="midtop", color=(150, 190, 210))

    if alert == "DANGER":
        alert_color = (230, 90, 80)
    elif alert == "WARNING":
        alert_color = (230, 190, 90)
    else:
        alert_color = (90, 200, 150)
    engine.draw_hud_text(f"STATUS: {alert}", (engine.WIDTH // 2, 66), size=14,
                         anchor="midtop", color=alert_color)

    engine.draw_hud_text(f"POWER RANGE: {max_safe_depth(sub.power)} m",
                         (engine.WIDTH // 2, 86), size=13, anchor="midtop",
                         color=(120, 170, 190))

    if engine.key_down("DOWN") and can_descend(sub.ballast, sub.power, sub.hull):
        sub.descending = True
    if engine.key_down("UP"):
        sub.ascending = True
    if engine.key_pressed("L"):
        sub.light_on = not sub.light_on

    engine.draw_hud_text("DOWN dive   UP rise   L light   ESC quit",
                         (16, engine.HEIGHT - 26), size=13, color=(120, 140, 155))


# ============ CHECKPOINT 3 (carried over) - reference versions =============
#  Your five functions from Checkpoint 3. Working reference versions, so the
#  game runs - replace any of them with your own if you have them.
# =============================================================================

def clamp_battery(battery_pct):
    if battery_pct > 100:
        return 100
    return battery_pct


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


def can_descend(ballast_kg, power_pct, hull_pct):
    return ballast_kg > 0 and power_pct > 0 and hull_pct > 0


def overall_alert(hull_label, oxygen_label):
    if hull_label == "BREACH" or oxygen_label == "CRITICAL":
        return "DANGER"
    elif hull_label == "CAUTION" or oxygen_label == "LOW":
        return "WARNING"
    else:
        return "SAFE"

# ============ end Checkpoint 3 ==============================================


# ============ CHECKPOINT 2 (carried over) - reference version ==============
#  Your pre-dive intake from Checkpoint 2. Working reference version, so the
#  game runs - replace it with your own if you have it.
#  One change from Checkpoint 3: target_depth now goes through this week's
#  read_valid_depth() instead of a plain int(input(...)).
# =============================================================================
if __name__ == "__main__":
    print("=" * 40)
    print("        LUMEN  -  PRE-DIVE INTAKE")
    print("=" * 40)
    pilot = input("Pilot name: ")
    target_depth = read_valid_depth()                                  # NEW this week
    ballast_kg = float(input("Ballast (kg): "))
    battery_pct = clamp_battery(float(input("Battery (%): ")))
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
