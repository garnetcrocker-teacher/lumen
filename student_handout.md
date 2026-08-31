# LUMEN - The Semester Project (student handout)

All term you are building one game: **LUMEN**, where you pilot a research
submersible down a black ocean trench, keep it alive, and catalog the glowing
creatures you find. Every module you learn goes straight into it. By December it
is a full, working game that you built.

---

## How each checkpoint works

Each checkpoint is a **Canvas assignment** with a `.zip` attached. Inside:

| File | What it is |
|---|---|
| `main.py` | the program - **you edit this**, only in the marked spots |
| `briefing.md` | the story, the exact task, and "done when" |
| `check.py` | run it to grade yourself; paste the output into Canvas |
| `engine.py` | the shared game engine - **never edit this** |

### The rules

1. **You only edit between the marked lines** in `main.py`:
   ```
   # --- BEGIN YOUR CODE ---
   ...your code here...
   # --- END YOUR CODE ---
   ```
   Early checkpoints also say "fill in the function body, don't change the
   `def` line." Everything outside those spots is already written.

2. **`engine.py` is off-limits.** It runs the window and the game loop so you can
   focus on the week's concept. If a new one is posted, replace the whole file.

3. **Grade yourself before submitting.** Run `python check.py`. It prints
   `[PASS]` / `[FAIL]` lines and a score out of 100. Copy that whole output into
   the Canvas text box. That is your submission.

---

## Fell behind? Missed a week?

**You do not need any previous checkpoint.** Every checkpoint's `main.py` already
contains a correct, finished version of all the earlier weeks. Download the
current one, do the setup once (below), and start there. Nothing is lost.

---

## One-time setup

Follow **`SETUP.md`**. Short version:

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # PowerShell   (see SETUP.md for cmd / Mac)
python -m pip install -r requirements.txt
```

Then, each work session, turn the venv on again (`Activate.ps1`), `cd` into the
checkpoint folder, and:

```
python main.py     # play / run it
python check.py     # grade it
```

---

## Getting help

- Read `briefing.md` all the way through first - the "Hints" section usually
  answers the thing you're stuck on.
- A `[FAIL]` line tells you the exact call that went wrong and what it expected.
- Bring the `check.py` output to office hours or post it on the discussion board.
