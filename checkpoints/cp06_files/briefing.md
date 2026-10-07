# Checkpoint 6 - The Dive Log

**Module 6: Files & Exceptions**
**Concepts:** opening/writing/reading files, append vs. write mode, `try`/`except`, checking whether a file exists, returning multiple values from a function

---

## The story so far

Every dive up to now has vanished the moment you close the window. This
week the game keeps two files that survive between runs.

- `dive_log.csv` grows by one line every dive: a running history of
  everything that's happened, oldest to newest.
- `best_dive.txt` holds only the *record*, the deepest dive anyone has
  ever survived. Most dives leave it untouched; it only gets overwritten
  when this dive is both alive at the end and deeper than whatever's
  already in it.

Opening a file in **append** mode (`"a"`) adds to what's already there.
Opening it in **write** mode (`"w"`) replaces it. `dive_log.csv` needs
the first, every time, unconditionally. `best_dive.txt` needs the
second, but only sometimes: you have to read what's already there and
compare before deciding whether this dive even earns a write.

Once the log has some history in it, it's worth reading back. Before
you dive, the game tells you how many dives you've logged, your
average depth, your shallowest, and your deepest. Neither file exists
the first time anyone runs the game, so reading them has to survive
that without crashing.

The `def` lines are given again this week, same as Checkpoint 4. The
exercise is what goes inside them.

---

## What to do

Open `main.py`. Fill in the bodies of the three functions between `BEGIN
YOUR CODE (Checkpoint 6)` and `END YOUR CODE`. Don't change any `def`
line.

> Below your code: `frame()` is provided, unchanged from Checkpoint 5,
> then a **Checkpoint 5 (carried over)** section with reference versions
> of last week's four functions, then **Checkpoint 4**, **Checkpoint 3**,
> and **Checkpoint 2 (carried over)** the same way. If you did those
> checkpoints, paste your own versions in over the references.
>
> Also already wired up for you, outside the YOUR CODE section:
> `load_dive_stats()` is called at the top of the pre-dive intake, and
> `save_dive_log()`/`save_best_dive()` are both called right after
> `engine.run()` returns, using the `sub` it hands back. You don't need
> to add either call yourself.

### 1. `save_dive_log(pilot, depth, alive, path=DIVE_LOG_PATH)` - void

Appends one line to the CSV file at `path`, recording this dive: the
pilot's name, the final depth reached, and the outcome (`"SURVIVED"` if
`alive` is `True`, `"LOST"` otherwise). Join those three pieces into one
comma-separated line, the same shape as `DIVE_LOG_HEADER` (already
defined near the top of `main.py`).

If the file doesn't exist yet, this is the first dive ever logged, so
write `DIVE_LOG_HEADER` as a line by itself before this dive's line.
Check `os.path.exists(path)` before you open the file: opening it is
what would create it.

Open the file in append mode (`"a"`) so every call adds a line without
erasing what's already there.

### 2. `load_dive_stats(path=DIVE_LOG_PATH)` - returns four numbers

Reads the whole log and returns `(count, average, minimum, maximum)`:
how many dives have been logged, their average depth, the shallowest,
and the deepest. Skip the header line. Every line after that is
`"pilot,depth,outcome"`: split each one apart, pull out the depth
field, and convert it to a `float`.

Track a running count, a running total, and a running minimum and
maximum as you go, then divide the total by the count for the average.

The first time this runs, the file won't exist yet. Wrap the open in
`try`/`except FileNotFoundError` and return `(0, 0.0, 0.0, 0.0)` from
the `except` block. A fresh install with nothing logged yet isn't a
bug, it's the expected starting state.

### 3. `save_best_dive(pilot, depth, alive, path=BEST_PATH)` - void

Tracks the deepest dive ever survived, in a file separate from the
growing log. `path` holds at most two lines, for whichever dive
currently holds the record:

```
Pilot: <pilot>
Depth: <depth> m
```

A dive can only set a new record if `alive` is `True`. A dive that
ended in a hull breach doesn't get to claim the title, no matter how
deep it went.

Try to open and read `path` first, the same way `load_dive_stats`
handles a file that might not exist yet, and pull the existing
record's depth back out of it. If the file didn't exist, or this dive
is alive *and* deeper than that depth, write the two lines above to
`path` in write mode (`"w"`) for the new pilot and depth. Otherwise
leave the file alone.

---

## Try it

Delete any `dive_log.csv` or `best_dive.txt` already in this folder,
then run `python main.py`. It should report no dives logged.

Survive a dive, then close the window. Both files should now exist,
with `best_dive.txt` showing that dive as the record. Survive a
second, shallower dive: `dive_log.csv` gains a row, `best_dive.txt`
doesn't change. Survive a third, deeper dive: `best_dive.txt` updates.
Dive deeper again but die: `dive_log.csv` gets the row, `best_dive.txt`
still doesn't change.

---

## Done when

`python check.py` prints **17 / 17** (100 points). It checks, against
dedicated test files (never your real `dive_log.csv` or `best_dive.txt`):

- `load_dive_stats()` returns `(0, 0.0, 0.0, 0.0)` on a file that doesn't
  exist
- `save_dive_log()` writes the header once, then appends a row per call
- saved rows record the pilot's name and the correct outcome
- `load_dive_stats()` returns the correct count, average, minimum, and
  maximum across several logged dives
- `save_best_dive()` sets the record on the first survived dive, leaves
  it alone for a shallower or unsurvived dive, and overwrites it for a
  deeper survived one

Submit `main.py` to Canvas. `check.py` runs the same checks the grader
uses.

---

## Hints

- `save_dive_log` uses `os.path.exists(path)` to decide whether to
  write a header. `load_dive_stats` and `save_best_dive` use
  `try`/`except FileNotFoundError` instead, for the same file-might-not-
  exist problem on the read side.
- `"a"` never erases what's in the file; `"w"` always does, the instant
  you open it. That's why `save_best_dive` has to decide whether to
  write before it ever opens the file in write mode.
- `with open(...) as f:` closes the file automatically, no `f.close()`
  needed.
- Convert the depth field with `float()` before comparing it to
  anything, or you'll be comparing text instead of numbers.
- `return a, b, c, d` packs multiple values into one tuple; unpack it
  the same way on the other end: `count, average, minimum, maximum =
  load_dive_stats()`.

## If you're stuck / joining late

The carried-over sections at the bottom of `main.py` already have
working versions of Checkpoints 2 through 5, so you don't need those
files. Do the `SETUP.md` setup if you haven't, then write the three
functions here. If you did the earlier checkpoints, swap your own code
into those sections.
