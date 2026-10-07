"""
LUMEN - Checkpoint 6
Module 6: Files & Exceptions

    Run the game:      python main.py      (press ESC or close the window to quit)
    Check your work:    python check.py

Your job this week is the three functions in the YOUR CODE section
below: save_dive_log, load_dive_stats, save_best_dive. The def lines
and docstrings are already written; fill in each body.

Every dive touches two files that survive between runs of the game.
dive_log.csv grows by one line per dive, a running history that
save_dive_log writes and load_dive_stats reads back. best_dive.txt
holds only the current record, the deepest dive ever survived: most
dives leave it alone, and save_best_dive only overwrites it when this
dive is alive and deeper than what's already there. Neither file
exists the first time anyone runs the game, so reading either one has
to survive that.

Already wired up outside the YOUR CODE section: load_dive_stats() runs
at the top of the pre-dive intake, and save_dive_log()/save_best_dive()
both run right after engine.run() returns, using the sub it hands back.
You don't need to add either call yourself.

Checkpoints 2 through 5 are carried into the bottom of this file as
reference versions: Checkpoint 5's four functions (format_distance,
distance_to_base, draw_dashboard, handle_controls), Checkpoint 4's four
(read_valid_depth, countdown_to_dive, draw_depth_ticks,
draw_sonar_rings), Checkpoint 3's five (clamp_battery, hull_status,
oxygen_state, can_descend, overall_alert), and Checkpoint 2's intake
inside `if __name__ == "__main__":`. If you did those checkpoints,
paste your own versions in over them.

Controls once it runs: DOWN dive, UP rise, LEFT/RIGHT drift sideways,
L toggle light.
"""

import os

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

DIVE_LOG_PATH = "dive_log.csv"          # grows by one line every dive
DIVE_LOG_HEADER = "pilot,depth,outcome"
BEST_PATH = "best_dive.txt"             # overwritten only when the record is beaten

# --- BEGIN YOUR CODE (Checkpoint 6) -----------------------------------------

def save_dive_log(pilot, depth, alive, path=DIVE_LOG_PATH):
    """Append one line to the CSV dive log at `path`: the pilot's name,
    the final depth reached, and the outcome ("SURVIVED" if `alive` is
    True, "LOST" otherwise), comma-separated in the same shape as
    DIVE_LOG_HEADER above.

    If the file doesn't exist yet, write DIVE_LOG_HEADER as its own
    line first. Check os.path.exists(path) before opening the file,
    since opening it in append mode is what would create it.

    Open the file in append mode ("a") so every call adds a line
    without erasing what's already there.

    Void. Nothing to return.
    """
    pass


def load_dive_stats(path=DIVE_LOG_PATH):
    """Read the dive log at `path` and return (count, average, minimum,
    maximum): how many dives have been logged, their average depth,
    the shallowest, and the deepest.

    Skip the header line. Every line after that is
    "pilot,depth,outcome": split it apart, pull out the depth field,
    and convert it to a float. Track a running count, total, minimum,
    and maximum as you go, then divide the total by the count for the
    average.

    A row's depth field might not convert to a float (a hand-edited or
    corrupted line). Wrap that conversion in its own try/except
    ValueError and skip the row instead of letting it crash the whole
    read.

    The first time this runs, the file won't exist yet. Wrap the open
    in try/except FileNotFoundError and return (0, 0.0, 0.0, 0.0) from
    the except block.
    """
    return 0, 0.0, 0.0, 0.0


def save_best_dive(pilot, depth, alive, path=BEST_PATH):
    """Track the deepest dive ever survived in a file separate from the
    growing log. `path` holds at most two lines, for whichever dive
    currently holds the record:
        Pilot: <pilot>
        Depth: <depth> m

    A dive can only set a new record if `alive` is True.

    Try to open and read `path` first, the same way load_dive_stats
    handles a file that might not exist yet, and pull the existing
    record's depth back out of it. If the file didn't exist, or this
    dive is alive and deeper than that depth, write the two lines above
    to `path` in write mode ("w") for the new pilot and depth.
    Otherwise leave the file alone.

    Void. Nothing to return.
    """
    pass

# --- END YOUR CODE -----------------------------------------------------------


def frame(sub, screen):
    """The engine calls this ~60 times a second. Nothing to change here -
    unchanged from Checkpoint 5."""
    draw_sonar_rings(screen, sub)
    draw_depth_ticks(screen, sub)

    hull = hull_status(sub.depth, sub.rated_depth)
    oxy = oxygen_state(sub.oxygen)
    alert = overall_alert(hull, oxy)

    draw_dashboard(screen, sub, alert)
    handle_controls(sub)


# ============ CHECKPOINT 5 (carried over) - reference versions =============
#  Your four functions from Checkpoint 5. Working reference versions, so the
#  game runs - replace any of them with your own if you have them.
# =============================================================================

def format_distance(meters):
    if meters < 1000:
        return f"{meters:.0f} m"
    else:
        return f"{meters / 1000:.1f} km"


def distance_to_base(sub):
    dx = sub.x - sub.base_x
    dy = sub.depth - sub.base_depth
    distance = (dx ** 2 + dy ** 2) ** 0.5
    edge_m = distance - sub.base_radius
    if edge_m <= 0:
        return "IN RANGE"
    return format_distance(edge_m)


def draw_dashboard(screen, sub, alert):
    engine.draw_hull_status(screen, hull_status(sub.depth, sub.rated_depth))
    engine.draw_hud_text("O2: " + oxygen_state(sub.oxygen), (engine.WIDTH // 2, 46),
                         size=15, anchor="midtop", color=(150, 190, 210))
    if alert == "DANGER":
        color = (230, 90, 80)
    elif alert == "WARNING":
        color = (230, 190, 90)
    else:
        color = (90, 200, 150)
    engine.draw_hud_text(f"STATUS: {alert}", (engine.WIDTH // 2, 66), size=14,
                         anchor="midtop", color=color)
    engine.draw_hud_text("DOWN dive   UP rise   LEFT/RIGHT drift   L light   ESC quit",
                         (16, engine.HEIGHT - 26), size=13, color=(120, 140, 155))
    engine.draw_hud_text("DRIFTED: " + format_distance(sub.total_drift),
                         (engine.WIDTH - 16, engine.HEIGHT - 26), size=13,
                         anchor="topright", color=(120, 140, 155))
    engine.draw_hud_text("BASE: " + distance_to_base(sub),
                         (engine.WIDTH // 2, 86), size=13,
                         anchor="midtop", color=(120, 140, 155))


def handle_controls(sub):
    if engine.key_down("DOWN") and can_descend(sub.ballast, sub.power, sub.hull):
        sub.descending = True
    if engine.key_down("UP"):
        sub.ascending = True
    if engine.key_down("LEFT"):
        sub.moving_left = True
    if engine.key_down("RIGHT"):
        sub.moving_right = True
    if engine.key_pressed("L"):
        sub.light_on = not sub.light_on

# ============ end Checkpoint 5 ==============================================


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
    count, average, minimum, maximum = load_dive_stats()

    print("=" * 40)
    print("        LUMEN  -  PRE-DIVE INTAKE")
    print("=" * 40)
    if count > 0:
        print(f"{count} dive(s) logged - best {maximum:.1f} m, "
              f"average {average:.1f} m, shallowest {minimum:.1f} m.")
    else:
        print("No dives logged yet - this will be the first.")
    print()

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
    sub = engine.run(frame)      # launch the dive with the plan you just entered
    save_dive_log(pilot, sub.depth, sub.alive)
    save_best_dive(pilot, sub.depth, sub.alive)
