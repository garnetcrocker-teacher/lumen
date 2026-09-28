# Checkpoint 6 - The Dive Log

**Module 6: Files & Exceptions**
**Concepts:** opening/writing/reading files, append vs. write mode, `try`/`except`, checking whether a file exists, returning multiple values from a function

---

## The story so far

Every dive up to now has vanished the moment you close the window - no
record that it ever happened. This week the game keeps two files that
survive between runs:

- `dive_log.csv` grows by one line every dive - a running history of
  everything that's ever happened, oldest to newest.
- `best_dive.txt` holds only the *record* - the deepest dive anyone has
  ever survived. Most dives leave it untouched. It only gets overwritten
  when this dive is both alive at the end and deeper than whatever's
  already in it.

That's the real difference this week: opening a file in **append** mode
(`"a"`) adds to what's already there; opening it in **write** mode
(`"w"`) replaces it. `dive_log.csv` needs the first, unconditionally,
every time. `best_dive.txt` needs the second, but only *sometimes* -
you have to read what's already there and compare before deciding
whether this dive even earns a write.

Once the log has some history in it, it's worth reading back: before you
dive, the game tells you how many dives you've logged, your average
depth, your shallowest, and your deepest - a record to beat. The very
first time anyone ever runs the game, neither file exists yet - reading
them has to survive that without crashing.

The `def` lines are given again this week, like Checkpoint 4 - the
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
> to add either call yourself - just make the three functions work.

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

Open the file in append mode (`"a"`) so every call adds a line without
erasing what's already there. A `with` block is the cleanest way to make
sure the file gets closed once you're done writing to it.

### 2. `load_dive_stats(path=DIVE_LOG_PATH)` - returns four numbers

Reads the whole log and returns `(count, average, minimum, maximum)` -
how many dives have been logged, their average depth, the shallowest,
and the deepest. Skip the header line; every line after that is
`"pilot,depth,outcome"` - split each one apart, pull out the depth
field, and convert it to a `float`.

As you go through the rest of the file, keep four running values: a
count, a running total (so you can divide by the count at the end to get
the average), and a running minimum and maximum - the same shape as
tracking a running max anywhere else, just two of them at once, plus a
count and a total.

The very first time this ever runs, the file won't exist. Wrap whatever
opens the file in a `try`/`except FileNotFoundError`, and return
`(0, 0.0, 0.0, 0.0)` from the `except` block - a fresh install with
nothing logged yet isn't a bug, it's the expected starting state.

### 3. `save_best_dive(pilot, depth, alive, path=BEST_PATH)` - void

Tracks the deepest dive ever **survived**, in a file separate from the
growing log. `path` should hold at most two lines at any time -
whichever dive currently holds the record:

```
Pilot: <pilot>
Depth: <depth> m
```

A dive can only set a new record if `alive` is `True` - a dive that
ended in a hull breach doesn't get to claim the title, no matter how
deep it went.

Try to open and read `path` first, the same way `load_dive_stats`
handles a file that might not exist yet, and pull the existing record's
depth back out of it. Then decide: if the file didn't exist, or this
dive is alive *and* deeper than that depth, this dive becomes the new
record - open the file in **write** mode (`"w"`) and write the two
lines above for the new pilot and depth. Otherwise, leave the file
exactly as it was; most dives won't touch it at all.

---

## Try it

Delete any `dive_log.csv` or `best_dive.txt` you already have in this
folder before your first real test, so you're starting from "no dives
logged yet." Run `python main.py`: it should print that no dives are
logged before asking for a pilot name.

Fly the dive however you like and survive it, then close the window.
Both files should now exist: `dive_log.csv` with a header and one row,
`best_dive.txt` with a two-line record of that same dive (it's
automatically the record - it's the only dive on file). Run
`python main.py` again - this time it should greet you with your logged
stats instead. Dive a second time, staying *shallower* than the first
dive, and survive again: `dive_log.csv` should now have two rows, but
`best_dive.txt` should be completely unchanged - still showing the
first, deeper dive. Now dive a third time, going *deeper* than your
current record, and survive: `best_dive.txt` should update to this
dive. Finally, dive deeper still but let the sub die (run out of air or
breach the hull) - `dive_log.csv` gets the row like always, but
`best_dive.txt` should not change at all, since this dive didn't
survive to claim it.

---

## Done when

`python check.py` prints **17 / 17** (100 points). It checks, against
dedicated test files (never your real `dive_log.csv` or `best_dive.txt`):

- `load_dive_stats()` returns `(0, 0.0, 0.0, 0.0)` on a file that doesn't
  exist
- `save_dive_log()` creates the file with the header line first, then a
  data row, and does not rewrite the header on later calls - just appends
- the saved rows record the pilot's name and the correct outcome
- `load_dive_stats()` returns the correct count, average, minimum, and
  maximum across several logged dives, not just the first or last one
  written
- `save_best_dive()` sets the record on the first survived dive, leaves
  it alone when a later dive is shallower *or* didn't survive, and
  overwrites it when a later dive is both alive and deeper

Submit your `main.py` to Canvas. (Run `check.py` first to see your score
- the grader runs the same check on the file you turn in.)

---

## Hints

- `os.path.exists(path)` and `try`/`except FileNotFoundError` solve two
  different problems - `save_dive_log` uses the first (deciding whether
  to write a header). `load_dive_stats` and `save_best_dive` both use
  the second, for the same reason: reading a file that isn't there at
  all yet.
- `open(path, "a")` and `open(path, "w")` look almost identical but
  behave very differently - "a" never erases what's already in the file,
  "w" always does, the instant you open it (even if you never write
  anything). That's the whole reason `save_dive_log` writes unconditionally
  every time, while `save_best_dive` has to decide *whether* to write at
  all before it ever opens the file in write mode.
- A `with open(...) as f:` block closes the file for you automatically at
  the end of the block - no separate `f.close()` needed.
- Reading a file line by line and splitting each line on `,` (for the CSV
  log) or on whitespace (for `best_dive.txt`'s "Depth: 300.0 m" line)
  gives you a list of strings - remember to convert the number with
  `float()` before comparing it to anything, or you'll be comparing text
  instead of numbers.
- `load_dive_stats` returns four separate values in one `return`
  statement (`return a, b, c, d`) - Python packs them together
  automatically, and whoever calls the function can unpack them the same
  way: `count, average, minimum, maximum = load_dive_stats()`.

## If you're stuck / joining late

You don't need your Checkpoint 2, 3, 4, or 5 files - the carried-over
sections at the bottom of `main.py` already have working versions of all
four. Do the `SETUP.md` setup if you haven't, then write the three
functions here. If you *did* do the earlier checkpoints, swap your own
code into those sections so the game stays fully yours.
