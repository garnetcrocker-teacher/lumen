"""
INSTRUCTOR REFERENCE - a correct Checkpoint 6 main.py (the two function bodies).
Do not ship this to students.

The sys.path shim lets this run from any working directory.
"""

import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

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

DIVE_LOG_PATH = "dive_log.csv"
DIVE_LOG_HEADER = "pilot,depth,outcome"
BEST_PATH = "best_dive.txt"

# --- BEGIN YOUR CODE (Checkpoint 6) -----------------------------------------

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

# --- END YOUR CODE -----------------------------------------------------------


def frame(sub, screen):
    draw_sonar_rings(screen, sub)
    draw_depth_ticks(screen, sub)

    hull = hull_status(sub.depth, sub.rated_depth)
    oxy = oxygen_state(sub.oxygen)
    alert = overall_alert(hull, oxy)

    draw_dashboard(screen, sub, alert)
    handle_controls(sub)


# ============ Checkpoint 5 (carried over) - reference versions =============
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
# ============ end Checkpoint 5 ============


# ============ Checkpoint 4 (carried over) - reference versions =============
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
# ============ end Checkpoint 4 ============


# ============ Checkpoint 3 (carried over) - reference versions =============
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
# ============ end Checkpoint 3 ============


# ============ Checkpoint 2 (carried over) - reference version ==============
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
    sub = engine.run(frame)
    save_dive_log(pilot, sub.depth, sub.alive)
    save_best_dive(pilot, sub.depth, sub.alive)
