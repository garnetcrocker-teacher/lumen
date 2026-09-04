"""
INSTRUCTOR REFERENCE - a correct Checkpoint 3 main.py (the five function bodies).
Do not ship this to students.

The two lines below put the repo root on the import path so `import engine`
finds the one canonical engine.py, no matter where you run this from.
"""

import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import engine

DESCENT_RATE = 20.0


# --- BEGIN YOUR CODE (Checkpoint 3) ----------------------------------------

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

# --- END YOUR CODE ---------------------------------------------------------


def frame(sub, screen):
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


# ============ Checkpoint 2 (carried over) - reference version ==============
if __name__ == "__main__":
    print("=" * 40)
    print("        LUMEN  -  PRE-DIVE INTAKE")
    print("=" * 40)
    pilot = input("Pilot name: ")
    target_depth = int(input("Target depth (m): "))
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

    engine.run(frame)
