"""
INSTRUCTOR REFERENCE - a correct Checkpoint 2 main.py.
Do not ship this to students. This is the "between the dashed lines" portion,
shown in full context.

Runs from anywhere - the two lines below put the repo root on the import path
so `import engine` finds the one canonical engine.py. Student checkpoints don't
need this; each of those folders has its own engine.py copy.
"""

import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import engine

DESCENT_RATE = 20.0

print("=" * 40)
print("        LUMEN  -  PRE-DIVE INTAKE")
print("=" * 40)

# --- BEGIN YOUR CODE ---------------------------------------------------------
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
# --- END YOUR CODE ---------------------------------------------------------

engine.save_diveplan(pilot, target_depth, ballast_kg, battery_pct)
engine.show_briefing(pilot, target_depth, ballast_kg, battery_pct)
