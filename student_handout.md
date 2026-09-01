# LUMEN - The Semester Project (student handout)

All term you are building one game: **LUMEN**, where you pilot a research
submersible down a black ocean trench, keep it alive, and catalog the glowing
creatures you find. Each module you learn gets used in it.

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

## Missed a week? Joining late?

**You don't need any earlier checkpoint's files.** Every checkpoint's zip is
complete and stands on its own. Anything from earlier modules that the game still
needs is already taken care of - it's either inside `engine.py`, or already
written into the parts of `main.py` you don't edit. If the first checkpoint you
ever open is Checkpoint 6, download the Checkpoint 6 zip, do the one-time setup,
and start there.

Each checkpoint's `main.py` is a fresh copy - you don't paste in your code from
previous weeks. Your finished checkpoints stay in their own folders as a record
of what you built.

---

## One-time setup

Follow **`SETUP.md`**. The short version, if you use VS Code: open the `lumen`
folder, then `Ctrl+Shift+P` > **Python: Create Environment** > *Venv* > pick a
Python 3.10+ > tick `requirements.txt`. After that the Run button and any new
terminal just work - you never "activate" anything.

Then, to work on a checkpoint: open its folder, run `python main.py` to play it
and `python check.py` to grade it.

---

## Getting help

- Read `briefing.md` all the way through first - the "Hints" section usually
  answers the thing you're stuck on. (To see it formatted: open it in VS Code and
  press `Ctrl+Shift+V`. More options in `SETUP.md`.)
- A `[FAIL]` line tells you the exact call that went wrong and what it expected.
- Bring the `check.py` output to office hours or post it on the discussion board.
