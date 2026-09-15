"""
LUMEN - Checkpoint 4
Module 4: Repetition Structures

    Run the game:      python main.py      (press ESC or close the window to quit)
    Check your work:    python check.py

Your job this week is the FOUR functions in the YOUR CODE section below:
read_valid_depth, countdown_to_dive, draw_depth_ticks, draw_sonar_rings.

frame() below your code is provided - nothing to change there.

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

TICK_STEP = 100               # draw a depth marker every this many meters
TICK_MAX = 2000               # ... from 0 m down to this depth

SONAR_RANGE_MAX = 480         # how far sonar reaches, in pixels, at full battery
                               # (compare: the light only reaches 155 - sonar
                               # is your long-range sense, light is close-range detail)
SWEEP_SECONDS = 16.0          # how long one ping takes to travel out to max range
PULSE_COUNT = 4               # how many pulses are traveling outward at once

DIVE_COUNTDOWN = 5            # seconds counted down before the dive begins
BEEP_FREQ = 440               # ordinary countdown beep, in Hz
BEEP_MS = 150                 # ... and how long it lasts, in milliseconds
URGENT_THRESHOLD = 3          # T-minus this many seconds or fewer -> urgent beep
URGENT_FREQ = 660             # higher-pitched beep for the last few seconds
DIVE_FREQ = 220               # low tone played once, at "DIVE."
DIVE_MS = 400

# --- BEGIN YOUR CODE (Checkpoint 4) -----------------------------------------

def read_valid_depth():
    """Ask the pilot 'Target depth (m): ' and read a whole number.

    If the number is less than 1 or greater than 6000, print
        Out of range - enter 1 to 6000.
    and ask again. Keep looping until the number is in range, then return it
    as an int.

    Use a while loop. (Assume the pilot types digits.)
    """
    return 0


def countdown_to_dive(seconds):
    """Count down out loud before the dive begins - a launch sequence, not
    just a delay.

    From `seconds` down to 1, once per number:
        - print(f"T-minus {seconds}...")
        - play a beep: engine.play_tone(BEEP_FREQ, BEEP_MS) normally, but
          engine.play_tone(URGENT_FREQ, BEEP_MS) instead once `seconds` is
          URGENT_THRESHOLD or less (the last few seconds sound more urgent)
        - engine.wait(1) to pause one second
        - subtract 1 from `seconds`

    Once the count reaches 0, print("DIVE.") and play the longer launch tone:
    engine.play_tone(DIVE_FREQ, DIVE_MS).

    Use a while loop, with an if/else inside it to pick the beep.
    """
    pass


def draw_depth_ticks(screen, sub):
    """Draw a depth marker every TICK_STEP meters, from 0 m up to and
    including TICK_MAX, colored by how dangerous that depth is - reusing
    hull_status() from Checkpoint 3 (it's carried over at the bottom of this
    file).

    For each depth d:
        - status = hull_status(d, sub.rated_depth)
        - pick a color: "OK" -> OK_COLOR, "CAUTION" -> CAUTION_COLOR,
          "BREACH" -> BREACH_COLOR
        - y = engine.world_y_to_screen(sub, d)     # d in meters -> y in pixels
        - engine.draw_tick(screen, y, d, color)    # draws the line + label

    Use a for loop with range() so d takes on every multiple of TICK_STEP
    from 0 through TICK_MAX (remember range()'s stop value is exclusive).
    """
    pass


def draw_sonar_rings(screen, sub):
    """Sonar reaches much farther than your light, and it isn't a fixed
    picture - a handful of pulses are always slowly traveling outward, then
    resetting back to the sub and starting over, like a real active sonar
    ping. (They don't shrink back inward - each one just restarts at 0 once
    it's traveled far enough. More on that in step 2.) Range still depends
    on battery, same idea as the light: 0 pixels at dead battery,
    SONAR_RANGE_MAX pixels at a full one.

    Think of engine.now() as a stopwatch that starts at 0 when the game
    opens and never stops climbing. Using that number to compute a pulse's current
    radius takes five steps:

    1. How far into ONE outward trip are we, ignoring any looping?
       engine.now() / SWEEP_SECONDS - this only ever grows: 0, 0.1, 0.5,
       1.0, 1.5, 2.3, and on forever. Each whole number is one full ping finished.

    2. Turn that endless growth into a repeating 0-to-1 cycle.
       Taking that value modulo 1 (`% 1.0`) throws away the whole-number
       part and keeps only what's left over - 2.3 % 1.0 is 0.3. That's the
       trick that makes a pulse restart at the sub every SWEEP_SECONDS
       instead of flying off past the edge of the screen forever.

    3. Give each pulse its own starting point in that cycle, so all
       PULSE_COUNT pulses end up spread out instead of stacked on each
       other. Loop over range(PULSE_COUNT); for pulse i, add i / PULSE_COUNT
       (0, 0.25, 0.5, 0.75 for 4 pulses) before taking % 1.0.

    4. Turn that 0-to-1 "how far along" number into a pixel radius by
       multiplying it by SONAR_RANGE_MAX - this is the pulse's true
       position. It always travels at the same speed; battery doesn't slow
       it down, only shortens how far you can still detect it (next step).

    5. Only draw the pulse if that radius is within THIS FRAME's
       battery-scaled sonar_range (sub.power * (SONAR_RANGE_MAX / 100)).
       Past that point the ping is still out there, traveling at the same
       speed as always - your equipment just can't pick it up yet, so skip
       drawing it rather than showing it at some shrunken radius.

    Draw each visible pulse centered on the sub with:
        engine.draw_ring(screen, (engine.WIDTH // 2, engine.SUB_SCREEN_Y), radius)
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

    print()
    countdown_to_dive(DIVE_COUNTDOWN)                                   # NEW this week
    engine.run(frame)      # launch the dive with the plan you just entered
