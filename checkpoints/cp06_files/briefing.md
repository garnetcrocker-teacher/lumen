# Checkpoint 6 - The Dive Log

**Module 6: Files & Exceptions**
**Concepts:** opening/writing/reading files, `with` blocks, `try`/`except`, checking whether a file exists

---

## The story so far

Every dive up to now has vanished the moment you close the window - no
record that it ever happened. This week the game keeps a small log file,
`dive_log.csv`, that survives between runs: every dive, however it ends,
gets written to it as one line - who piloted it, how deep they got, and
whether they made it back.

Once that log exists, it's worth something: before you dive, the game
can tell you the deepest anyone has ever gotten, so you have a record to
beat. The very first time anyone ever runs the game, that file doesn't
exist yet - reading it has to survive that without crashing.

You're writing two functions this week. Unlike Checkpoint 5, the `def`
lines are written for you again - the exercise is what goes inside them.

---

## What to do

Open `main.py`. Fill in the bodies of the two functions between `BEGIN
YOUR CODE (Checkpoint 6)` and `END YOUR CODE`. Don't change either `def`
line.

> Below your code: `frame()` is provided, unchanged from Checkpoint 5,
> then a **Checkpoint 5 (carried over)** section with reference versions
> of last week's four functions, then **Checkpoint 4**, **Checkpoint 3**,
> and **Checkpoint 2 (carried over)** the same way. If you did those
> checkpoints, paste your own versions in over the references.
>
> Also already wired up for you, outside the YOUR CODE section:
> `load_best_depth()` is called right at the top of the pre-dive intake,
> and `save_dive_log()` is called right after `engine.run()` returns,
> using the `sub` it hands back. You don't need to add either call
> yourself - just make the functions themselves work.

### 1. `save_dive_log(pilot, depth, alive, path=DIVE_LOG_PATH)` - void

Appends one line to the CSV file at `path`, recording this dive: the
pilot's name, the final depth reached, and the outcome - `"SURVIVED"` if
`alive` is `True`, `"LOST"` otherwise. Join those three pieces into one
comma-separated line, the same shape as `DIVE_LOG_HEADER` (already
defined near the top of `main.py`).

If the file doesn't exist yet, this is the first dive ever logged - write
`DIVE_LOG_HEADER` as a line by itself first, *before* this dive's line.
`os.path.exists(path)` tells you whether the file is already there -
check that **before** you open it, since opening it is what would create
it.

Open the file in append mode so every call adds a line without erasing
what's already in it. A `with` block is the cleanest way to make sure the
file gets closed once you're done writing to it.

### 2. `load_best_depth(path=DIVE_LOG_PATH)` - returns a float

Returns the deepest depth any dive in the log has ever reached, as a
`float`. Skip the header line - every line after that is
`"pilot,depth,outcome"`. Split each one apart, pull out the depth field,
convert it to a `float`, and keep the largest one you've seen as you go
through the whole file.

The very first time this ever runs, the file won't exist. Wrap whatever
opens the file in a `try`/`except FileNotFoundError`, and return `0.0`
from the `except` block - a fresh install with nothing logged yet isn't a
bug, it's the expected starting state.

---

## Try it

Delete any `dive_log.csv` you already have in this folder before your
first real test, so you're starting from the "no dives logged yet" case.
Run `python main.py`: it should print something like "No dives logged
yet - this will be the first." before asking for a pilot name.

Fly the dive however you like, then close the window (or let the sub run
out of air/hull). A `dive_log.csv` file should now exist in the folder,
with a header line and one row for that dive. Run `python main.py` again
- this time it should greet you with your personal best depth instead,
and each additional dive should add one more row to the file, never
erasing the ones already there.

---

## Done when

`python check.py` prints **10 / 10** (100 points). It checks, against a
dedicated test file (never your real `dive_log.csv`):

- `load_best_depth()` returns `0.0` - a `float`, not an `int` or a string
  - on a file that doesn't exist
- `save_dive_log()` creates the file with the header line first, then a
  data row, and does not rewrite the header on later calls - just appends
- the saved row records the pilot's name and the correct outcome
  (`"SURVIVED"` / `"LOST"`)
- `load_best_depth()` returns the *largest* depth across several logged
  dives, not just the first or the last one written

Submit your `main.py` to Canvas. (Run `check.py` first to see your score
- the grader runs the same check on the file you turn in.)

---

## Hints

- `os.path.exists(path)` and `try`/`except FileNotFoundError` solve two
  different problems here - `save_dive_log` uses the first (deciding
  whether to write a header), `load_best_depth` uses the second (handling
  a file that isn't there at all). You don't need both in the same
  function.
- A `with open(path, "a") as f:` block writes without erasing what's
  already in the file, and closes it for you automatically at the end of
  the block - no separate `f.close()` needed.
- Reading a file line by line and splitting each line on `,` gives you a
  list of strings - remember to convert the depth field with `float()`
  before comparing it to anything, or you'll be comparing text instead of
  numbers.
- Keep a running "best so far" variable as you read through the lines,
  the same shape as tracking a running max anywhere else - update it only
  when the current line's depth is larger than what you're holding.

## If you're stuck / joining late

You don't need your Checkpoint 2, 3, 4, or 5 files - the carried-over
sections at the bottom of `main.py` already have working versions of all
four. Do the `SETUP.md` setup if you haven't, then write the two
functions here. If you *did* do the earlier checkpoints, swap your own
code into those sections so the game stays fully yours.
