"""
LUMEN - Checkpoint 2
Module 2: Input, Processing, and Output

    Run your program:   python main.py
    Check your work:    python check.py

You only edit the lines BETWEEN the two dashed comment lines.
Everything above and below them is already done for you.

Read briefing.md for exactly what each numbered step must do.
"""

import engine

DESCENT_RATE = 20.0        # metres per second - a named constant. Do not change it.

print("=" * 40)
print("        LUMEN  -  PRE-DIVE INTAKE")
print("=" * 40)

# --- BEGIN YOUR CODE ---------------------------------------------------------
#
# 1. Ask the pilot for their name.            Store it in   pilot
# 2. Ask for the target depth in metres.      Store it in   target_depth
#       This must be a whole number - wrap the input in int(...).
# 3. Ask for the ballast mass in kilograms.   Store it in   ballast_kg
#       This can have a decimal - wrap the input in float(...).
# 4. Ask for the battery charge as a percent. Store it in   battery_pct
#       Also a decimal - use float(...).
# 5. Calculate the estimated descent time and store it in   descent_seconds
#       descent_seconds = target_depth divided by DESCENT_RATE
# 6. print() a briefing that shows, on separate lines:
#       the pilot name, the target depth, the ballast, the battery,
#       and the descent time rounded to 1 decimal place.
#
# Delete the five placeholder lines below and write your own.

pilot = ""
target_depth = 0
ballast_kg = 0.0
battery_pct = 0.0
descent_seconds = 0.0

# --- END YOUR CODE ---------------------------------------------------------

engine.save_diveplan(pilot, target_depth, ballast_kg, battery_pct)
engine.show_briefing(pilot, target_depth, ballast_kg, battery_pct)
