# LUMEN - instructor guide

A semester-long Pygame project for Intro to Python (Gaddis, *Starting Out with
Python*). Students build one game across 12 checkpoints, one per module.

**Carry-forward model.** From cp03 on, each checkpoint's `main.py` contains a
marked section for every earlier checkpoint plus the new week's blanks. Earlier
sections ship pre-filled with a reference solution, so:

- a student who did the earlier weeks pastes their own code in over the reference
  (the point: by December the file is theirs, built piece by piece);
- a student joining late still gets a runnable game and only has to do the
  current section.

`check.py` grades **only the current week's** work, so it doesn't matter whose
version of the earlier code is in the file. Downside: every later checkpoint's
`main.py` contains the earlier reference solutions - fine, since those weeks are
already due, but don't post checkpoints ahead of schedule.

---

## Repo layout

```
lumen/
  engine.py              canonical shared engine - the ONLY copy you edit
  requirements.txt       pygame-ce, pinned
  SETUP.md               student venv instructions (Windows / Mac / Linux)
  student_handout.md     one-page "how checkpoints work" - hand out week 1
  INSTRUCTOR.md          this file
  checkpoints/
    cp02_io/             main.py + briefing.md + check.py + engine.py (copy)
    cp03_decisions/
    ...                  cp04 ... cp12 (to be built)
  solution/              reference answers - DO NOT distribute
  tools/
    sync_engine.py       copies engine.py into every checkpoint folder
```

### Editing the engine

Edit **only** `lumen/engine.py`, then run:

```
python tools/sync_engine.py
```

That copies it into every `checkpoints/cpNN/` folder (each ships as a
self-contained zip, so each needs its own copy). Bump `ENGINE_VERSION` in
`engine.py` when you make a change students must pick up, and tell them in the
Canvas announcement: "replace your engine.py; it should say ENGINE_VERSION 1.1".

---

## Distributing to students

Per checkpoint: zip the `checkpoints/cpNN_name/` folder and attach it to a Canvas
assignment, released on the module schedule below. Do **not** post the whole repo
or the Git URL - each checkpoint's `main.py` contains the solutions to all
earlier checkpoints.

An optional read-only public GitHub mirror containing only the *current*
checkpoint is fine for students who ask.

---

## Grading

Every checkpoint has `check.py`. It runs offline, opens no window, prints
`[PASS]`/`[FAIL]` per requirement and a line like:

```
SCORE: 16 / 16      POINTS: 100 / 100
```

**Students submit their `main.py`** - the file they edited - to the Canvas
assignment. Not the check.py output (trivially forgeable) and not check.py itself
(identical for everyone). `check.py` is the student's own pre-flight check; you
run the same `check.py` on the `main.py` they turned in to produce the grade.

To grade: drop each submitted `main.py` into a clean copy of the checkpoint
folder and run `python check.py`. A `tools/grade.py` that does this over a folder
of submissions is on the to-do list.

Canvas assignment is 100 points; `check.py` already normalizes to 100. Suggested
weight: each checkpoint small; the payoff is the finished game and the Module 12
/ Final capstone.

`check.py` can still be gamed by hard-coding returns to match the visible test
cases. Skim each `main.py` (you're collecting them anyway) and lean on the
proctored module tests for individual accountability. Later checkpoints' `check.py`
use less predictable inputs to raise the effort of faking it.

---

## Semester map

Class dates are taken straight from the calendar you supplied. "Due" dates are
suggestions - about a week after the module block closes, kept clear of the
proctored module tests.

| Checkpoint | Class dates | Module | Students write (concept) | check.py verifies |
|---|---|---|---|---|
| **cp02_io** | Sep 1, 8 | 2 - Input/Processing/Output | Terminal pre-dive intake: `input()`, `int()`/`float()`, arithmetic, formatted `print()` | dive plan saved with correct types; briefing printed |
| **cp03_decisions** | Sep 10, 15 | 3 - Decisions & Boolean Logic | Bodies of `clamp_battery()` (if), `hull_status()`, `oxygen_state()` (if/elif/else), `can_descend()` (3-arg `and` chain), `overall_alert()` (elif + `or`, order-sensitive) | 28 known input/output cases, boundary- and ordering-focused |
| **cp04_loops** | Sep 17, 22 | 4 - Repetition | `for` loop drawing depth-gauge ticks; sonar sweep loop; `while` input-validation on the pre-dive | gauge tick count; sonar completes one sweep; bad input re-prompts |
| **cp05_functions** | Sep 24, 29, Oct 1 | 5 - Functions | Refactor frame code into `draw_hud()`, `update_sub()`, `spawn_creature()`, `check_systems()` with params + returns | each function callable in isolation, correct returns; game still runs |
| **cp06_files** | Oct 6, 8 | 6 - Files & Exceptions | `save_dive_log()`, `load_best_depth()` with `try/except FileNotFoundError`; append discoveries to CSV | file written/read; missing file handled; best depth persists |
| **cp07_lists** | Oct 15, 20, 22 | 7 - Lists & Tuples | Single creature -> `creatures = []`; spawn/append; `for c in creatures` update+draw; cull; `(x, y)` tuples; max/min/len over depths | many independent creatures; list ops correct; stats correct |
| **cp08_strings** | Oct 27 | 8 - More About Strings | Species-code builder `f"{p}-{n:04d}"`; parse a scanned code back with slicing/`split`; normalize names; reverse/shift decode puzzle | code format; round-trip parse; decode returns expected string |
| **cp09_dicts** | Oct 29, Nov 3 | 9 - Dictionaries & Sets | `CATALOG = {code: {...}}`; `discovered = set()`; score = sum of points; `DEPTH_ZONES` lookup; achievements set | no double-scoring; catalog counts; zone lookup by depth |
| **cp10_classes** | Nov 5, 10, 12 | 10 - Classes & OOP | `class Creature` (`__init__`, `update`, `draw`, `distance_to`); `class Submarine`; convert list-of-dicts -> list-of-objects | objects constructed; methods return/behave correctly |
| **cp11_inheritance** | Nov 17 | 11 - Inheritance | `Jellyfish`, `Anglerfish`, `Leviathan` subclasses; override `update`/`draw`; `super().__init__` | subclass behavior differs; `isinstance` checks; base still works |
| **cp12_recursion** | Nov 19 | 12 - Recursion | Recursive trench generator (shrinking depth budget) OR recursive sonar flood-fill of a cavern | base case terminates; bounded depth; output shape correct |
| **Final** | Dec 1, 3 | - | Pick 1-2 from a feature menu + README mapping features to modules | chosen feature works; full loop runs end to end |

Dec 8 is the comprehensive final exam - not project work.

### Concept-scaffolding rule

Before Module 5, students never write `def` - the `def` line is pre-written and
they fill the body. Before Module 7 they never see a list literal in *their*
region; before Module 9, no dict literal in their region. The engine and the
provided parts of `main.py` absorb everything the class hasn't reached yet.

Carried-over sections only ever use constructs from the module that first
introduced them, so pasting last week's own code in is always within reach. The
cp02 intake sits in an `if __name__ == "__main__":` block from cp03 on; that line
is labelled "provided boilerplate, more on it later" and students just write the
intake indented beneath it (one extra indent vs. how they wrote it in cp02).

### Two drawing surfaces - keep this straight when building cp05+

Inside `frame(sub, screen)`, anything drawn straight onto `screen` is *world*
content: `_draw_darkness()` runs right after `frame_fn` returns, so it gets
covered/dimmed once you're deep and outside the light radius. That's exactly
what you want for creatures later on (Module 7+) - the light should have to find
them.

Status readouts are the opposite: they should read like cockpit instruments, not
things you see through the window, so they must stay visible in total darkness.
`draw_hull_status()`, `draw_tick()`, and the new `draw_hud_text()` all render
onto a separate transparent `_state.hud_surface` that the engine composites back
on top *after* `_draw_darkness()`. Use `draw_hud_text()` (not `draw_text()`) for
any new dashboard-style readout a checkpoint adds inside `frame()` - `draw_text()`
targets whatever surface you hand it (normally the world `screen`), so calling it
directly from `frame()` will get swallowed by the dark the moment depth ramps up.
This was the cp03 bug: the HULL/O2 status was drawn with `draw_text(screen, ...)`
inside `frame()`, so it rendered before `_draw_darkness` and got covered.

---

## Status of this repo

- [x] `engine.py` v1.0 - window, loop, keyboard, ocean/darkness rendering, sub systems sim, HUD (pilot / target-depth line / ballast->dive-rate / power), dive-plan I/O, `draw_tick`, `draw_hud_text` (dashboard layer composited on top of the darkness so status readouts never get dimmed - see below)
- [x] `cp02_io`, `cp03_decisions`, `cp04_loops` - complete (main + briefing + check + reference solution)
- [ ] `cp05` - `cp12` - not built yet
- [ ] `solution/lumen_full.py` - the finished game for playtesting - not built yet
- [ ] `tools/build_zips.py` - one-command per-checkpoint zip builder - not built yet
