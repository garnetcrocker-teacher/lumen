"""
LUMEN - Checkpoint 7
Module 7: Lists & Tuples

    Run the game:      python main.py      (press ESC or close the window to quit)
    Check your work:    python check.py

Your job this week is the six functions in the YOUR CODE section below:
spawn_creatures, distance_to_creature, update_creatures, cull_creatures,
sonar_contacts, draw_creatures. The def lines and docstrings are already
written; fill in each body.

The ocean now has creatures. The list `creatures` holds all of them, and
each creature is a tuple: (x, depth, speed). That's its sideways position
in meters, its depth in meters, and how fast it swims sideways in meters
per second (negative swims left). The world is endless, so the game only
keeps a small crowd near you: each frame frame() moves the creatures, drops
the ones that fell too far away, and spawns new ones off screen to replace
them. Your light only reaches about 40 meters, but sonar hears much
farther, so the dashboard has a new CONTACTS line.

frame() is provided and new this week. It calls your functions for you.

Checkpoints 2 through 6 are carried into the bottom of this file as
reference versions: Checkpoint 6's three functions (save_dive_log,
load_dive_stats, save_best_dive), Checkpoint 5's four (format_distance,
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
import random

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

DIVE_LOG_PATH = "dive_log.csv"
DIVE_LOG_HEADER = "pilot,depth,outcome"
BEST_PATH = "best_dive.txt"

CREATURE_TARGET = 8              # how many creatures the game keeps near you
SPAWN_MIN_DX = 130.0             # new creatures start this far to the side (meters)...
SPAWN_MAX_DX = 240.0             # ...up to this far
SPAWN_DEPTH_SPREAD = 100.0       # and up to this far above or below you (meters)
MIN_CREATURE_DEPTH = 30.0        # but never shallower than this
MAX_CREATURE_SPEED = 6.0         # meters per second, either direction
CULL_DISTANCE = 300.0            # creatures farther than this are dropped (meters)
SONAR_RANGE_M = SONAR_RANGE_MAX / engine.PIXELS_PER_METER   # sonar reach at full power (meters)

creatures = []                   # a list of (x, depth, speed) tuples

# --- BEGIN YOUR CODE (Checkpoint 7) -----------------------------------------

def spawn_creatures(sub, count):
    """Return a list of `count` new creatures placed around the sub. Each
    one is a tuple (x, depth, speed):
        x      SPAWN_MIN_DX to SPAWN_MAX_DX meters from sub.x, on a
               randomly chosen side (left or right), so it starts off screen
        depth  random, within SPAWN_DEPTH_SPREAD meters above or below
               sub.depth, but never shallower than MIN_CREATURE_DEPTH
        speed  random, from -MAX_CREATURE_SPEED to MAX_CREATURE_SPEED

    The random module has a function for a random float in a range and one
    for picking from a sequence. Start from an empty list and add each
    creature as you make it.
    """
    return []


def distance_to_creature(sub, creature):
    """Return the straight-line distance in meters from the sub to one
    creature, using the Pythagorean theorem on the sideways gap and the
    depth gap, same as Checkpoint 5. Pull the creature's x and depth out of
    the tuple by index or by unpacking. Its speed doesn't matter here.
    """
    return 0.0


def update_creatures(creatures, seconds):
    """Move every creature sideways for `seconds` of swimming: its x changes
    by its speed times seconds, and its depth and speed stay the same.

    Tuples can't be changed, so build a replacement tuple and store it back
    in the same spot in the list. That means you need each creature's
    position in the list, not just the creature. Change the list itself;
    there is nothing to return.
    """
    pass


def cull_creatures(sub, creatures):
    """Return a new list holding only the creatures within CULL_DISTANCE
    meters of the sub, in their original order. Use distance_to_creature
    for the distance.

    Don't remove items from a list while looping over it, because the loop
    skips items. Build up a new list of the ones you're keeping instead.
    """
    return creatures


def sonar_contacts(sub, creatures):
    """Return a list of distances in meters, one for each creature sonar can
    hear, nearest first. Sonar hears a creature that is within the sonar
    range: SONAR_RANGE_M meters at full power, shrinking in proportion to
    sub.power (50% power hears half as far). Return the distances, not the
    creatures. Return an empty list if nothing is in range.

    Collect the distances in a list, then sort it.
    """
    return []


def draw_creatures(screen, sub, creatures):
    """Draw every creature. For each one, convert its world position to a
    screen position with engine.world_x_to_screen and
    engine.world_y_to_screen, then call
    engine.draw_creature(screen, (screen_x, screen_y), facing).

    facing is 1 for a creature swimming right (speed 0 or more) and -1 for
    one swimming left. engine.draw_creature skips anything that is off
    screen for you.

    Void. Nothing to return.
    """
    pass

# --- END YOUR CODE -----------------------------------------------------------


def frame(sub, screen):
    """The engine calls this ~60 times a second. New this week, and nothing
    to change here."""
    global creatures
    update_creatures(creatures, engine.dt())
    creatures = cull_creatures(sub, creatures)
    if len(creatures) < CREATURE_TARGET:
        creatures = creatures + spawn_creatures(sub, CREATURE_TARGET - len(creatures))
    draw_creatures(screen, sub, creatures)

    draw_sonar_rings(screen, sub)
    draw_depth_ticks(screen, sub)

    hull = hull_status(sub.depth, sub.rated_depth)
    oxy = oxygen_state(sub.oxygen)
    alert = overall_alert(hull, oxy)

    draw_dashboard(screen, sub, alert)

    contacts = sonar_contacts(sub, creatures)
    contact_text = f"CONTACTS: {len(contacts)}"
    if len(contacts) > 0:
        contact_text += "   NEAREST: " + format_distance(contacts[0])
    engine.draw_hud_text(contact_text, (engine.WIDTH // 2, 104), size=13,
                         anchor="midtop", color=(120, 140, 155))

    handle_controls(sub)


# ============ CHECKPOINT 6 (carried over) - reference versions =============
#  Your three functions from Checkpoint 6. Working reference versions, so the
#  game runs - replace any of them with your own if you have them.
# =============================================================================

def save_dive_log(pilot, depth, alive, path=DIVE_LOG_PATH):
    is_new = not os.path.exists(path)
    outcome = "SURVIVED" if alive else "LOST"
    with open(path, "a") as f:
        if is_new:
            f.write(DIVE_LOG_HEADER + "\n")
        f.write(f"{pilot},{depth},{outcome}\n")


def load_dive_stats(path=DIVE_LOG_PATH):
    try:
        with open(path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return 0, 0.0, 0.0, 0.0

    count = 0
    total = 0.0
    minimum = None
    maximum = None
    for line in lines[1:]:
        fields = line.strip().split(",")
        try:
            depth = float(fields[1])
        except ValueError:
            continue
        count += 1
        total += depth
        if minimum is None or depth < minimum:
            minimum = depth
        if maximum is None or depth > maximum:
            maximum = depth

    if count == 0:
        return 0, 0.0, 0.0, 0.0
    return count, total / count, minimum, maximum


def save_best_dive(pilot, depth, alive, path=BEST_PATH):
    if not alive:
        return

    try:
        with open(path, "r") as f:
            lines = f.readlines()
        current_best = float(lines[1].split()[1])
    except FileNotFoundError:
        current_best = None

    if current_best is None or depth > current_best:
        with open(path, "w") as f:
            f.write(f"Pilot: {pilot}\n")
            f.write(f"Depth: {depth} m\n")

# ============ end Checkpoint 6 ==============================================


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
