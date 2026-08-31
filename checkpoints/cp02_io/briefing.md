# Checkpoint 2 - Pre-Dive Intake

**Module 2: Input, Processing, and Output**
**Concepts:** `input()`, `print()`, variables, `int()` / `float()` conversion, arithmetic, named constants

---

## The story so far

You are the pilot of the submersible *Lumen*. Before every dive, mission control
files a **dive plan**: who's diving, how deep they're going, how much ballast
(sinking weight) they're carrying, and how charged the battery is.

This week you write the intake form. Next week the submarine starts using it.

---

## What to do

Open `main.py`. Between the two lines that say `BEGIN YOUR CODE` and
`END YOUR CODE`, write the program:

| # | Step | Store in | Notes |
|---|------|----------|-------|
| 1 | Ask for the pilot's name | `pilot` | plain text, no conversion |
| 2 | Ask for target depth in metres | `target_depth` | whole number - use `int(input(...))` |
| 3 | Ask for ballast in kg | `ballast_kg` | decimal ok - use `float(input(...))` |
| 4 | Ask for battery charge percent | `battery_pct` | decimal ok - use `float(...)` |
| 5 | Compute descent time | `descent_seconds` | `target_depth / DESCENT_RATE` |
| 6 | Print the briefing | - | pilot, depth, ballast, battery, descent time to 1 decimal |

`DESCENT_RATE` is already defined for you at the top of the file (20.0 m/s).

---

## Example run

```
========================================
        LUMEN  -  PRE-DIVE INTAKE
========================================
Pilot name: Marlow
Target depth (m): 450
Ballast (kg): 40
Battery (%): 100

--- DIVE PLAN ---
Pilot:          Marlow
Target depth:   450 m
Ballast:        40.0 kg
Battery:        100.0 %
Descent time:   22.5 s
```

Your wording and spacing don't have to match exactly, but the **five values must
appear** and the descent time must be **22.5** for this input.

After you close the little briefing window that pops up, you're done.

---

## Done when

`python check.py` prints **9 / 9** (100 points). It checks that:

- the program runs without crashing
- `diveplan.json` gets written
- `pilot` is saved as the text `Marlow`
- `target_depth` is saved as the **integer** `450` (not the text `"450"`)
- `ballast_kg` and `battery_pct` are saved as **floats** (`40.0`, `100.0`)
- the printed briefing contains the pilot name, the depth, and the descent time `22.5`

Paste the check.py output into the Canvas submission.

---

## Hints

- `int(input("Target depth (m): "))` does the asking and the converting in one line.
- To show one decimal place: `print("Descent time:", round(descent_seconds, 1), "s")`
  or an f-string: `print(f"Descent time: {descent_seconds:.1f} s")`.
- If `check.py` says `target_depth` is text, you forgot `int(...)` on that line.
- Run `python main.py` yourself first and just make sure it looks right.

## If you're stuck / joining late

You don't need any previous checkpoint to do this one. Make sure you've done the
one-time setup in `SETUP.md` (the venv), then work only in `main.py`.
