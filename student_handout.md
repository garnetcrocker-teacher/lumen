# LUMEN - The Semester Project (student handout)

All term you are building one game: **LUMEN**, where you pilot a research
submersible down a black ocean trench, keep it alive, and catalog the glowing
creatures you find. Each module we cover will have you apply concepts to this game.

---

## How each checkpoint works

Each checkpoint is a **Canvas assignment** with a `.zip` attached. Inside:

| File | What it is |
|---|---|
| `main.py` | the program - **you edit this**, only in the marked spots |
| `briefing.md` | the story, the exact task, and "done when" |
| `check.py` | run it any time to test your own work before you submit |
| `engine.py` | the shared game engine - **never edit this** |

### The rules

1. **You only edit between the marked lines** in `main.py`:
   ```
   # --- BEGIN YOUR CODE ---
   ...your code here...
   # --- END YOUR CODE ---
   ```
   Early checkpoints also say "fill in the function body, don't change the
   `def` line." Everything outside those spots is already written - leave it.
   From Checkpoint 3 on there are also marked sections for *earlier* checkpoints;
   those come pre-filled with a working reference version, and you're free to
   paste your own code from that week in over it (see "carries forward" below).

2. **`engine.py` is off-limits.** It runs the window and the game loop so you can
   focus on the week's concept. If a newer one is posted, replace the whole file.

3. **Check your own work first.** Run `python check.py`. It prints `[PASS]` /
   `[FAIL]` lines and a score out of 100, and tells you exactly which case
   failed. Fix and re-run until it's the score you want.

4. **Submit `main.py`.** Upload your edited `main.py` file to the Canvas
   assignment. That's the file your work is in. Don't upload `check.py` or
   `engine.py` - those are the same for everyone and you didn't touch them.
   The grade comes from running `check.py` on the `main.py` you turn in, so the
   score you saw in step 3 is the score you get.

---

## Your code carries forward

From Checkpoint 3 on, each `main.py` has a marked section for **every earlier
checkpoint's work**, not just the new one. Each of those older sections comes
pre-filled with a working reference version so the game always runs - but if you
did that checkpoint, paste **your own** code in over the reference. By the end of
the term the file is full of code you wrote: you built the whole game, one piece
at a time.

That reference version is only there so *this week's* checkpoint runs on its
own - leaving it untouched while you work on the current checkpoint is
completely fine. What's not fine: going back and turning in that reference code
as your own answer to the **earlier** checkpoint it came from, if you haven't
actually done that checkpoint yourself. That's an academic integrity violation,
the same as submitting anyone else's code would be.

## Missed a week? Joining late?

**You don't need any earlier checkpoint's files to start.** Because every older
section already has a working reference version, you can pick up at any
checkpoint. If the first one you ever open is Checkpoint 6, download the
Checkpoint 6 zip, do the one-time setup, and work on the new section - the
earlier parts already run. (You just won't have your own code in the older
sections, which is fine.)

---

## One-time setup

Follow **`SETUP.md`**. The short version, if you use VS Code: open the `lumen`
folder, then `Ctrl+Shift+P` > **Python: Create Environment** > *Venv* > pick a
Python 3.10+ > tick to select dependencies. After that the Run button and any new
terminal just work - you never "activate" anything.

Then, to work on a checkpoint: open its folder, run `python main.py` to play it
and `python check.py` to grade it.

---

## Getting help

- Read `briefing.md` all the way through first - the "Hints" section usually
  answers the thing you're stuck on. (To see it formatted: open it in VS Code and
  press `Ctrl+Shift+V`. More options in `SETUP.md`.)
- A `[FAIL]` line tells you the exact call that went wrong and what it expected.
- Reach out with questions! This is my first time making and using these assignments, so there will probably be some bumps along the way.
