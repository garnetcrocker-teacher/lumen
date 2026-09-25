"""
LUMEN - Checkpoint 5
Module 5: Functions

    Run the game:      python main.py      (press ESC or close the window to quit)
    Check your work:    python check.py

Your job this week is the THREE functions in the YOUR CODE section below:
draw_dashboard, format_distance, handle_controls. Unlike every checkpoint
so far, the def lines aren't already written for you - see the YOUR CODE
section for exactly what to write.

frame() has so far done two separate jobs: drawing the dashboard, and
reading the keyboard. Until now both jobs just sat inline, mixed together.
This week you pull each one out into its own function - both draw_dashboard
and handle_controls are void functions (they do something and hand nothing
back).

Most of draw_dashboard and handle_controls is sitting almost word-for-word
inside your Checkpoint 4 main.py's frame() function - open it side by side
with this file. For that part you're not writing new logic, you're deciding
which existing lines belong together, giving that group a name and a
parameter list, and writing the def line yourself.

format_distance is different: it's genuinely new, there's nothing to copy
for it anywhere. It's also your first value-returning function since
Checkpoint 3 - it hands a string back to whatever calls it (draw_dashboard,
in this case).

Because nothing is pre-written this week, `python main.py` will crash with
a NameError until both functions exist - that's expected, not a bug. Get
both written (even roughly) before you try running it.

frame() below your code is provided - it's much shorter now, since your two
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

Controls once it runs:  DOWN = dive,  UP = rise,  LEFT/RIGHT = drift
sideways,  L = toggle light
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
#
# Write three functions here. Open your Checkpoint 4 main.py's frame() next
# to this file for the first and last one - nearly every line you need is
# already sitting in there, word-for-word.
#
# format_distance(meters) - returns a string, e.g. "340 m" or "1.2 km"
#     sub.total_drift is a running total (built by the engine, in meters)
#     of how far you've drifted sideways, either direction. Nothing to copy
#     here - write the logic yourself:
#         - below 1000, show it in meters, no decimal place: "340 m"
#         - 1000 or above, show it in kilometers, one decimal place instead:
#           "1.2 km"
#     This is a value-returning function - it hands the string back to
#     whatever calls it, instead of drawing or changing anything itself.
#
# draw_dashboard(screen, sub, alert)
#     Everything frame() used to do with draw_hull_status/draw_hud_text:
#     the hull status, the "O2: ..." line, the "STATUS: ..." line (colored
#     to match - the if/elif/else that used to pick that color goes here
#     too), and the controls line at the bottom - now reading exactly
#     "DOWN dive   UP rise   LEFT/RIGHT drift   L light   ESC quit" (updated
#     for this week's new keys). `alert` is handed to you already worked
#     out, since it's computed in frame before you pass it to this function.
#
#     One more line, and this one is new - nothing to copy for it either.
#     Add a fourth draw_hud_text call: the text should read exactly
#     "DRIFTED: " followed by whatever format_distance(sub.total_drift)
#     returns. Put it in the bottom-right corner, mirroring the hint line's
#     bottom-left spot: position (engine.WIDTH - 16, engine.HEIGHT - 26),
#     anchor "topright", same size (13) and color (120, 140, 155) as the
#     hint line.
#
# handle_controls(sub)
#     Everything frame() used to do with handling DOWN / UP / L.
#       (NOT DRAWING these controls though, that should be done above)
#     PLUS something new this week, not in Checkpoint 4: LEFT and RIGHT now
#     let you drift sideways. There's nothing to copy for this part - mirror
#     the exact shape of your DOWN/UP lines instead:
#         - LEFT held -> sub.moving_left = True
#         - RIGHT held -> sub.moving_right = True
#     The engine applies the actual movement and keeps the odometer; you're
#     just setting the flag, same as you already do for sub.descending/
#     sub.ascending.
#
# All three are void except format_distance, which returns a string - no
# def line is written for you on any of them; name and parameters are your
# call.
# --- END YOUR CODE -----------------------------------------------------------


def frame(sub, screen):
    """The engine calls this ~60 times a second. Much shorter now - your two
    functions from this week, plus draw_depth_ticks/draw_sonar_rings from
    Checkpoint 4, do all the actual work. Nothing to change here."""
    draw_sonar_rings(screen, sub)
    draw_depth_ticks(screen, sub)

    hull = hull_status(sub.depth, sub.rated_depth)
    oxy = oxygen_state(sub.oxygen)
    alert = overall_alert(hull, oxy)

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
