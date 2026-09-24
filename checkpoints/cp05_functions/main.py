"""
LUMEN - Checkpoint 5
Module 5: Functions

    Run the game:      python main.py      (press ESC or close the window to quit)
    Check your work:    python check.py

Your job this week is the FOUR functions in the YOUR CODE section below:
current_alert, alert_color, handle_controls, draw_dashboard.

Until now, every function you've written has been a single, self-contained
calculation - given some numbers, work out an answer. This week your
functions call OTHER functions - the ones you already wrote in Checkpoints 3
and 4 - and replace code that used to just sit directly inside frame(). Two
of your four functions return a value; two don't return anything at all,
they just do something (drawing, or changing sub's state). That's the
difference between a value-returning function and a void function.

frame() below your code is provided - it's much shorter now, since your four
functions do the work it used to do inline.

Checkpoints 2, 3, and 4 are carried into the BOTTOM of this file:
  - Checkpoint 4's four functions (read_valid_depth, countdown_to_dive,
    draw_depth_ticks, draw_sonar_rings) are reference versions.
  - Checkpoint 3's five functions (clamp_battery, hull_status, oxygen_state,
    can_descend, overall_alert) are reference versions - your new functions
    this week call several of these directly.
  - Checkpoint 2's pre-dive intake is inside `if __name__ == "__main__":`.
Working reference versions are filled in so the game runs either way - if
you did those checkpoints, paste your own versions in over them.

Controls once it runs:  DOWN = dive,  UP = rise,  L = toggle light
"""

import engine

DESCENT_RATE = 20.0

OK_COLOR = (90, 200, 150)
CAUTION_COLOR = (230, 190, 90)
BREACH_COLOR = (230, 90, 80)

TICK_STEP = 100
TICK_MAX = 2000

SONAR_RANGE_MAX = 480
SWEEP_SECONDS = 16.0
PULSE_COUNT = 4

DIVE_COUNTDOWN = 5
BEEP_FREQ = 440
BEEP_MS = 150
URGENT_THRESHOLD = 3
URGENT_FREQ = 660
DIVE_FREQ = 220
DIVE_MS = 400

# --- BEGIN YOUR CODE (Checkpoint 5) -----------------------------------------

def current_alert(sub):
    """Combine the hull and oxygen readouts into one overall alert level -
    the same three lines frame() used to run inline, now packaged into a
    single reusable, value-returning function.

    Use your Checkpoint 3 functions: get the hull status from sub.depth and
    sub.rated_depth, get the oxygen state from sub.oxygen, then combine the
    two with overall_alert() and return whatever it gives you.
    """
    return "SAFE"


def alert_color(alert):
    """Return the RGB color tuple that matches an alert level:

        "DANGER"   -> (230, 90, 80)
        "WARNING"  -> (230, 190, 90)
        anything else -> (90, 200, 150)

    A function's return value doesn't have to be a number or string - a
    tuple works fine too.
    """
    return (90, 200, 150)


def handle_controls(sub):
    """Read the keyboard and update sub accordingly - everything frame()
    used to do with DOWN/UP/L, now living in its own function. This one's a
    void function: it changes sub's attributes directly and returns nothing.

        - DOWN held and can_descend(sub.ballast, sub.power, sub.hull) is
          True -> sub.descending = True
        - UP held -> sub.ascending = True
        - L just pressed (not held) -> flip sub.light_on
    """
    pass


def draw_dashboard(screen, sub, alert):
    """Draw every HUD readout except the depth gauge and sonar - everything
    frame() used to do with draw_hull_status/draw_hud_text, now living in
    its own void function. Takes the alert level as a parameter instead of
    recomputing it, since frame() already worked it out via current_alert().

        - engine.draw_hull_status(screen, ...) with the current hull status
          (hull_status(sub.depth, sub.rated_depth))
        - engine.draw_hud_text("O2: " + <oxygen state>,
          (engine.WIDTH // 2, 46), size=15, anchor="midtop",
          color=(150, 190, 210))
        - engine.draw_hud_text(f"STATUS: {alert}", (engine.WIDTH // 2, 66),
          size=14, anchor="midtop", color=<the matching alert color - you
          just wrote a function for exactly this>)
        - engine.draw_hud_text("DOWN dive   UP rise   L light   ESC quit",
          (16, engine.HEIGHT - 26), size=13, color=(120, 140, 155))
    """
    pass

# --- END YOUR CODE -----------------------------------------------------------


def frame(sub, screen):
    """The engine calls this ~60 times a second. Much shorter now - your
    four functions from this week, plus draw_depth_ticks/draw_sonar_rings
    from Checkpoint 4, do all the actual work. Nothing to change here."""
    draw_sonar_rings(screen, sub)
    draw_depth_ticks(screen, sub)

    alert = current_alert(sub)
    draw_dashboard(screen, sub, alert)
    handle_controls(sub)


# ============ CHECKPOINT 4 (carried over) - reference versions =============
#  Your four functions from Checkpoint 4. Working reference versions, so the
#  game runs - replace any of them with your own if you have them.
# =============================================================================

def read_valid_depth():
    depth = int(input("Target depth (m): "))
    while depth < 1 or depth > 6000:
        print("Out of range - enter 1 to 6000.")
        depth = int(input("Target depth (m): "))
    return depth


def countdown_to_dive(seconds):
    while seconds > 0:
        print(f"T-minus {seconds}...")
        if seconds <= URGENT_THRESHOLD:
            engine.play_tone(URGENT_FREQ, BEEP_MS)
        else:
            engine.play_tone(BEEP_FREQ, BEEP_MS)
        engine.wait(1)
        seconds -= 1
    print("DIVE.")
    engine.play_tone(DIVE_FREQ, DIVE_MS)


def draw_depth_ticks(screen, sub):
    for d in range(0, TICK_MAX + 1, TICK_STEP):
        status = hull_status(d, sub.rated_depth)
        if status == "OK":
            color = OK_COLOR
        elif status == "CAUTION":
            color = CAUTION_COLOR
        else:
            color = BREACH_COLOR
        y = engine.world_y_to_screen(sub, d)
        engine.draw_tick(screen, y, d, color)


def draw_sonar_rings(screen, sub):
    sonar_range = sub.power * (SONAR_RANGE_MAX / 100)
    for i in range(PULSE_COUNT):
        offset = i / PULSE_COUNT
        fraction = (engine.now() / SWEEP_SECONDS + offset) % 1.0
        radius = fraction * SONAR_RANGE_MAX
        if radius <= sonar_range:
            engine.draw_ring(screen, (engine.WIDTH // 2, engine.SUB_SCREEN_Y), radius)

# ============ end Checkpoint 4 ==============================================


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
# =============================================================================
if __name__ == "__main__":
    print("=" * 40)
    print("        LUMEN  -  PRE-DIVE INTAKE")
    print("=" * 40)
    pilot = input("Pilot name: ")
    target_depth = read_valid_depth()
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

    print()
    countdown_to_dive(DIVE_COUNTDOWN)
    engine.run(frame)      # launch the dive with the plan you just entered
