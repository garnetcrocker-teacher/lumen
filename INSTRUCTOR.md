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
or the Git URL - from cp03 on, each checkpoint's `main.py` contains a working
reference solution to the *immediately preceding* checkpoint (the carry-forward
model - see "Carry-forward model" above).

An optional read-only public GitHub mirror containing only the *current*
checkpoint is fine for students who ask.

### There is no clean fix for the early-answer-key exposure, and that's fine

Publishing checkpoint N necessarily hands out a working answer to checkpoint
N-1. A Canvas `unlock_at` on the assignment plus a lock on its Files folder
looks like a fix, but it isn't one once late submission is allowed: a student
still legitimately working on N-1 after the class has moved on is, by design,
exactly the student who should *not* yet see N-1's answer sitting in N's
`main.py` - and locking N to N-1's due date does nothing for them, while
locking it any looser protects no one. There's no timestamp that satisfies
"available to everyone who needs to keep moving" and "invisible to anyone still
working on the previous week" at once.

Given that, don't try to engineer around it - manage it instead:

- **Publish each checkpoint only when you're actually ready for students to see
  it**, not automatically on a schedule. The gate is you deciding to ask for the
  upload, not a Canvas date.
- **Grade from the submitted `main.py`, not a self-reported score** (already the
  model - see Grading below), and skim submissions for a suspiciously-perfect,
  suspiciously-early Checkpoint 2 that looks copied from a Checkpoint 3 packet.
- **Lean on the proctored module tests** for the individual-accountability
  backstop that self-paced, late-submission-friendly checkpoints can't provide
  on their own.

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

To grade one submission by hand: drop it into a clean copy of the checkpoint
folder as `main.py` and run `python check.py`.

To grade a whole folder at once: `python tools/grade.py <checkpoint_folder_name>
<submissions_folder>` (e.g. `python tools/grade.py cp02_io Student_Grading/cp02_io`).
It runs every `.py` file in that folder (any name except `main.py`/`check.py`/
`engine.py`) through a fresh copy of that checkpoint's canonical `check.py` +
`engine.py` in an isolated temp dir - never the possibly-stale copies sitting in
the submissions folder itself, and never touching one student's file while
grading another's. A 15-second timeout guards against a hung/looping submission
blocking the batch. Writes `grades.csv` (student, file, status, score, points) and
`logs/<name>.txt` (that student's full `[PASS]`/`[FAIL]` output) into the
submissions folder - both already covered by the `Student_*` `.gitignore` entries.

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
| **cp04_loops** | Sep 17, 22 | 4 - Repetition | `while` input-validation (`read_valid_depth`) and a `while` launch countdown with an `if`/`else` inside it (`countdown_to_dive`, beeps via new `engine.play_tone`/`engine.wait`); `for` loop over `range()` coloring the depth gauge by a decision reused from cp03's `hull_status`; `for` loop over `PULSE_COUNT` animating an outward-sweeping, battery-scaled sonar ping via `engine.now()` and `%` wraparound | boundary-focused value checks; countdown text/beep-order/wait-count checks; tick position + color; sonar radius at controlled `(power, t)` combinations |
| **cp05_functions** | Sep 24, 29, Oct 1 | 5 - Functions | `frame()`'s two real jobs (drawing the dashboard, reading the keyboard) split into two void functions students name and write entirely themselves - no `def` line given, unlike every other checkpoint. `handle_controls()` also gains unbounded sideways movement (`LEFT`/`RIGHT` -> `sub.moving_left`/`sub.moving_right`, two more flags in the exact shape of the existing ones) - genuinely new, not copyable from cp04. Two more functions are value-returning: `format_distance(meters)` turns the engine's new `sub.total_drift` odometer into "340 m"/"1.2 km", and `distance_to_base(edge_m)` turns `engine.distance_to_base_edge(sub)` (distance to the edge of a circular recharge base - depth counts, not just sideways position - that refills O2/power instead of draining them while the sub sits inside it) into "340 m"/"IN RANGE" by calling `format_distance` internally - both called from inside `draw_dashboard()`, so students see a void function calling value-returning ones of their own, one of which calls another | key-handling side effects incl. the `can_descend` gate and the new drift flags; exact draw calls (text/position/size/color) with no extras or omissions, checked across all three alert levels; `format_distance()`'s and `distance_to_base()`'s formatting branches each checked directly |
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

### Hint-fading rule

Briefing hints should get *less* helpful as the semester goes on - fading
scaffolds, not the same hand-holding all 12 weeks. Tie it to phase, not to each
individual checkpoint:

| Phase | Checkpoints | Modules | Hint style |
|---|---|---|---|
| Syntax scaffolding | cp02-cp04 | 2-4 | Near-literal on *values*: exact rules/thresholds as a table, a worked micro-example, and any brand-new engine API named explicitly (they can't guess `engine.draw_ring` exists). Not near-literal on *logic*: describe what a loop/condition needs to do in prose, don't hand them the assignment lines to copy. (cp04's `draw_sonar_rings` was rewritten from a literal code block to this prose style after review - see note below.) |
| Concept pointers | cp05-cp09 | 5-9 (Functions, Files, Lists, Strings, Dicts) | Name the right tool or pattern ("you need something that builds a list one item at a time - which list method does that?"). No ready-to-paste code. |
| Debugging prompts | cp10-cp12 | 10-12 (Classes, Inheritance, Recursion) | Socratic only - "what does printing X right before the return show you?" No syntax at all. Fewer hints too (1-2, not 4-5). |
| Final project | - | - | No built-in hints - office hours / discussion board is the hint. |

What does **not** fade: `check.py`'s `[FAIL] ... (got X, expected Y)` output.
That's diagnostic feedback, not a spoiler - it's the safety net that keeps this
from stranding anyone even as the prose hints get terser.

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

### Horizontal movement - what it's for, and where it's going

cp05 adds `LEFT`/`RIGHT` (`sub.moving_left`/`sub.moving_right`, applied in
`_update_systems` exactly like `descending`/`ascending`) as its "make this
week substantial" addition, once two manufactured functions got cut and the
checkpoint was left feeling too thin. `sub.x` already existed
("horizontal drift") but was never wired to anything; it's now a real,
unbounded world position - no floor or ceiling, matching how depth already
has no ceiling.

The sub stays pinned at screen center; `_draw_submarine` and `_draw_darkness`
were changed to stop offsetting by `sub.x` (they used to, which used to make
the sub visibly slide across a static background - backwards from the
scrolling-world model). The world scrolls past it instead, the same mental
model vertical movement already uses. New `world_x_to_screen(sub, world_x)`
mirrors `world_y_to_screen` and is **not used by anything yet** - it's there
for Module 7, when creatures get a fixed `(x, y)` in the world and need to
scroll past the same way everything else does. This is the same
"build the instrument now, cash it in later" pattern as cp04's sonar range.

The one thing that needed solving to make sideways movement visible *this
week*, before creatures exist to prove it's real: `_draw_background` is a
pure vertical color gradient with zero horizontal variation, so scrolling
it literally shows nothing. Fix was to reinterpret the existing snow
particles' stored x as a world coordinate (they already existed, already
had per-particle positions, already updated every frame) and draw them via
`world_x_to_screen(...) % WIDTH`, tiling every `WIDTH` pixels - a working
parallax cue today, using infrastructure that was already there, without
needing to invent new background art.

This is an `engine.py` change, made by the instructor, not a student
hand-off - fully consistent with retiring the ownership-migration plan
above. `handle_controls()` only sets the two flags, mirroring the existing
`DOWN`/`UP` lines exactly; all the rendering and physics-application
complexity stays engine-side, same as `draw_ring`/`play_tone` before it.

`_draw_base_hud` now also shows a `POSITION` line right under `DEPTH`
(`f"POSITION {sub.x:+7.1f} m"`, signed so students can tell left from
right at a glance), pushing `depth_zone_name`/`TARGET`/`BALLAST` down one
row each (94/112/130/148). This is passive display, not student-written -
no checkpoint's `check.py` covers it, since `_draw_base_hud` only ever
runs inside `engine.run()`'s real game loop, which is skipped entirely in
headless/check.py mode. Verified instead by calling `_draw_base_hud`
directly against a real (non-None) headless `pygame.Surface` with
`draw_text` mocked, for both a positive and a negative `sub.x`.

The point of exposing this now: it's the player-facing half of a
navigation mechanic, the other half being the recharge base and
`distance_to_base()` (see below) - and the same groundwork pays off
again later for a planned sonar/creature alert that names a world x
(e.g. "Large Creature at x 500"), which the player will read against
this same `POSITION` line. Same "build the instrument now, cash it in
later" move as `world_x_to_screen`. `sub.x` exists in every checkpoint
via the shared `Submarine.__init__`, but only reads as "0.0" until
cp05's sideways movement gives it something to show.

### The odometer (`format_distance`) - why cp05 got a third function

Even with sideways movement added, cp05's two functions were still mostly
transcription (copy from Checkpoint 4) plus two one-line mirrors of the
`DOWN`/`UP` pattern - not much genuinely new thinking. Rather than invent a
third function that decomposes existing logic (the `alert_color`/
`current_alert` mistake from earlier in this checkpoint's history), the fix
adds a genuinely new mechanic tied to the movement feature itself: the
engine now tracks `sub.total_drift`, a running total in meters of sideways
distance covered in *either* direction (both `moving_left` and
`moving_right` add to it in `_update_systems` - it never nets out to zero
the way `sub.x` does, verified directly: 10s right then 10s left leaves
`sub.x == 0.0` but `sub.total_drift == 1200.0`).

Turning that number into something displayable - "340 m" below 1000,
"1.2 km" at or above - needs real, novel `if`/`else` logic with no
Checkpoint 4 source to copy, unlike everything else in this checkpoint.
`format_distance(meters)` is that function: value-returning, called from
inside `draw_dashboard` (function-calling-function, squarely a Module 5
concept), and displayed as a dashboard line, bottom-right, mirroring the
hint line's bottom-left position. `check.py` tests it directly (two
boundary cases) in addition to checking the rendered line. This is the
kind of "new" cp05 was missing: not a thinner slice of existing code, but
a small self-contained feature that happens to exercise exactly the
write-a-function skill Module 5 is about.

### The recharge base (`distance_to_base`) - cp05's fourth function

Once `POSITION` existed, the natural next question was "toward what?" -
raw coordinates aren't interesting without something to navigate to. The
first attempt at an answer was an arbitrary single-point "dive site"
(`sub.target_x` + `heading_to_target()`, direction word and all) - cut
after feedback that a random exact coordinate that does nothing on
arrival is thematically empty. It's replaced with something that actually
does something: a circular recharge base. `Submarine.__init__` now sets
`sub.base_x`, `sub.base_depth` (both randomized, so the base sits
somewhere different in both dimensions each dive) and `sub.base_radius`
(fixed at 120m). Stepping inside the circle - measured as real
straight-line distance, so depth counts exactly as much as sideways
position, not just an x-only check - flips `_update_systems` from
draining oxygen/power to refilling them (8%/s oxygen, 6%/s power, both
capped at 100). Hull decay is untouched either way; the base recharges
consumables, it doesn't repair damage.

The geometry itself is instructor-side: `engine.distance_to_base_edge(sub)`
computes straight-line distance to `(base_x, base_depth)` minus
`base_radius` (0 or negative once inside), living next to
`world_x_to_screen`/`world_y_to_screen` as another engine-owned spatial
helper - sqrt-based 2D distance is scope creep for a "how do I write a
function" checkpoint, so it's handed to students as a given, the same way
`hull_status`'s threshold values are given rather than derived.

`distance_to_base(edge_m)` is what students write: `edge_m <= 0` returns
`"IN RANGE"`, otherwise it returns `format_distance(edge_m)`. That reuse
matters: `format_distance` is now called from two different places
(`draw_dashboard` directly, and from inside `distance_to_base`), which is
what keeps it a real function rather than a repeat of the
`alert_color`/`current_alert` mistake - a function with only one caller
and no duplication removed. Deliberately, the engine's own always-on HUD
never reveals raw `base_x`/`base_depth` anywhere - only the student's own
`draw_dashboard`, via a correct `distance_to_base()`, tells the player how
close they are. That's what makes writing the function worth doing
instead of ornamental.

Verified end-to-end, not just via `check.py`: ran the real `_update_systems`
loop, confirmed oxygen/power drain outside the base and refill (capped at
100) inside it; then simulated drifting toward a random base position for
the exact number of frames needed to reach it, confirming the edge
distance shrank throughout, hit exactly `"IN RANGE"` at the boundary, and
both consumables climbed from there while stationary inside. `check.py`
still 21 checks (two `distance_to_base` boundary cases, one for the
rendered `BASE` line, line-count check at 5); solution still 21/21, blank
stub still 0/21, no regressions on cp02/cp03/cp04.

The base was invisible on screen until now - `check.py`/the dashboard
readout were the only way to know it existed. `_draw_recharge_base`
(engine.py, purely visual, no student involvement) fixes that: converts
`(sub.base_x, sub.base_depth)` to a screen position via the existing
`world_x_to_screen`/`world_y_to_screen`, then draws a small marker circle
plus a glow using the pre-existing `draw_glow()` helper (the same additive
soft-glow function already used elsewhere, not new code). Drawn *after*
`_draw_darkness`, same placement as `_draw_target_line` - deliberately, so
it reads as "the base emits its own light and stays visible regardless of
how dark it is nearby," rather than being swallowed by the murk the way an
unlit object would be. Explicitly kept simple per instructor direction -
"doesn't need to be anything graphically detailed" - real visual design
is deferred to whenever recharge bases become their own class. Skips
drawing entirely once far enough off-screen (cheap bounds check before any
blit). Verified with direct pixel sampling (marker color exactly matches
at the computed screen position; glow visible partway out; untouched
black further away; off-screen case draws nothing), and by running the
*real* (non-headless-skip) drawing pipeline for 120 frames with the dummy
SDL driver to confirm nothing crashes outside the check.py fast path.

**Three attempts to get this right (post-launch):** reported symptom was
"in range" over a much taller depth interval than horizontal interval,
and the `BASE` readout reporting distances that didn't match real depth
differences shown by the `DEPTH` ticks.

1. First guess: a speed mismatch (`drift_speed` 60 vs `dive_rate`/
   `rise_rate` ~20-24). Wrong - reverted. Speed has nothing to do with a
   static boundary check.
2. Second guess: `distance_to_base_edge` compared `sub.x` and `sub.depth`
   as equal-scale inputs, but `world_x_to_screen` doesn't scale x while
   `world_y_to_screen` stretches depth by `PIXELS_PER_METER` (4x) to get
   a screen position - so scaled the depth term by `PIXELS_PER_METER`
   before measuring, to match screen space. This fixed the *visual*
   mismatch but broke the *number*: it silently multiplied every real
   depth difference by 4 before displaying it (a real 100m difference
   started reading as "400 m"), directly contradicting `DEPTH`/
   `POSITION`, which are always real, unscaled meters. Also wrong -
   reverted.
3. The actual fix: keep `distance_to_base_edge` in real meters, unscaled,
   symmetric between `dx` and `dy` - consistent with every other distance
   readout in the game. The visual mismatch was never really a bug in the
   check; it's that a genuine circle in real meters, run through the
   screen's own anisotropic mapping (depth stretched 4x, sideways
   position not), legitimately renders as a tall ellipse - the same
   reason `DEPTH` tick marks sit farther apart on screen than an equal
   sideways distance would. So `_draw_recharge_base` now draws an ellipse
   (`rx = base_radius`, `ry = base_radius * PIXELS_PER_METER`) instead of
   a circle, matching the true boundary exactly without touching what
   gets displayed.

Verified: a real depth difference of 220m against a 120m radius now
reports "100 m" (not "400 m"), and a 120m real offset on either axis
alone gives an identical edge distance of exactly 0 - both matching
`DEPTH`/`POSITION`'s units directly. Pixel-sampled the drawn ellipse's
actual extents (scanned rows/columns for the outline color) and confirmed
they land at exactly `rx` horizontally and `ry` vertically. Re-ran the
real (non-headless-skip) drawing pipeline with the default radius (where
`ry` extends to 480px, well past the 600px-tall window) to confirm
nothing crashes at that size. No `check.py` regressions through any of
the three attempts, since nothing there depends on `drift_speed` or the
scale `distance_to_base_edge` operates in.

### Sonar - what it's for, and where it's going

cp04's sonar sweep isn't meant to stay decoration. The design intent is a
two-tier detection model once creatures exist:

- **Light** = short range (`155` px), full detail - if something's in it, you
  can see exactly what it is. Costs battery continuously while on.
- **Sonar** = long range (`480` px, cp04's `SONAR_RANGE_MAX`), coarse
  awareness only - tells you *something's* out there and roughly how far, not
  what it is. Also battery-scaled (`sonar_range = power * (SONAR_RANGE_MAX/100)`).

That split is the actual point: it gives a reason to approach a sonar contact
cautiously (worth the battery to light it up and look?) instead of only ever
reacting to what's already lit.

**Module 7 (Lists) - the concrete next step:** once a `creatures` list exists,
loop over it, compute each creature's distance from the sub, and light up (or
draw a blip on) whichever pulse/ring band it falls within - turning the sweep
from a pure instrument reading into a real "how many things, how close"
readout. Good Lists material: iterate a list, compute something per item,
draw conditionally.

**Later, if still worth it when we get there:**
- Module 9 (Dicts): differentiate blips by creature type via a lookup, without
  fully identifying them - sonar tells you enough to decide, not everything.
- Module 10/11 (Classes/Inheritance): each `Creature` subclass overrides how it
  reads on sonar (a Leviathan pings very differently than plankton).

Net effect by midterm: sonar says something's near -> decide whether it's
worth the battery to close in and light it up -> once lit, scan/catalog it
(Module 9's dict + discovered-species set). Built entirely from concepts the
syllabus already covers, in order.

### cp04 revision: max_safe_depth deleted, countdown_to_dive added, sonar physics fixed

Four review passes after the first cp04 draft, based on direct feedback:

- **`max_safe_depth` and its `POWER RANGE` HUD readout are gone entirely -
  not just demoted to provided code.** It was first cut as a student `while`
  loop for being a fake loop (`start_power * METERS_PER_PERCENT` is one
  multiplication, no repetition needed) and kept as provided code for one
  revision - but a further question ("what's the actual relationship
  between battery and depth here?") exposed that there isn't one: battery
  in this sim only drains while the light is on (`_update_systems` in
  `engine.py`), never from depth. The readout wasn't an arbitrary constant
  standing in for something real, it was describing a mechanic that flatly
  doesn't exist. Provided-but-fictional was worse than not having it, so it
  was deleted outright, HUD line included.
- **`countdown_to_dive(seconds)` fills the vacated fourth-function slot**: a
  `while` loop with an `if`/`else` inside it (Module 3 review layered into
  Module 4), printing a `T-minus ...` launch sequence and beeping through two
  new `engine.py` helpers, `play_tone(freq_hz, ms)` and `wait(seconds)`.
  `play_tone` synthesizes a square/sine buffer on the fly with the stdlib
  `array` module (no sound asset files, no new dependency) and plays it via
  `pygame.mixer`; both are no-ops under `LUMEN_HEADLESS=1` and get
  lambda-mocked in `check.py` the same way `draw_ring`/`draw_tick` already
  are, so grading never actually waits or makes noise.
- **Sonar pacing**: `SWEEP_SECONDS` went 2.5 -> 8.0 -> 16.0 and
  `SONAR_RANGE_MAX` 400 -> 480 across two rounds of "too fast/flashy, and it
  should outrange the light more" feedback. At the current values a pulse
  resets once every 4 seconds (`SWEEP_SECONDS / PULSE_COUNT`) instead of
  every 0.625s originally.
- **Sonar physics fix - speed decoupled from battery.** The original formula
  was `radius = fraction * sonar_range`, where `fraction` cycles 0->1 on a
  fixed `SWEEP_SECONDS` clock regardless of battery. That means a pulse
  covers less distance in the same time as `sonar_range` shrinks - i.e. it
  visibly slows down as the battery drains, which was flagged as physically
  wrong (a sonar ping doesn't travel slower because your receiver is
  weaker). Fix: compute the pulse's true position at constant speed
  (`radius = fraction * SONAR_RANGE_MAX`, never scaled by battery), then
  only draw it `if radius <= sonar_range` - low battery now means pulses
  vanish from view partway out instead of crawling. This directly touched
  the student-facing docstring (added as its step 5) even though the
  instructor had just hand-edited that docstring's steps 1-3 and asked that
  it not be changed again - resolved by asking first rather than overwriting
  silently, since the two instructions were in direct conflict. `check.py`'s
  sonar test now expects a *subset* of the 4 pulses per frame (only the ones
  currently within `sonar_range`), not always all 4.

### Ownership migration - retired (see below for why)

The original plan here was: by the end of the course, students should feel
like they wrote the whole game, including chunks of `engine.py` itself, by
**opening `engine.py` up for direct editing once a checkpoint had the
background to do so** - a fenced YOUR CODE region inside the engine file,
same convention as `main.py`, just relocated.

**That plan is retired.** The reasoning that killed it: `main.py`'s
carry-forward pattern only works as an exercise because each week's new
code is genuinely new - there's no working version of this week's function
sitting anywhere for a student to peek at before they write it. `engine.py`,
by contrast, has been fully working and fully visible since Module 2. Asking
a student to "write" a function that's already sitting there, complete, in
a file they already have open, isn't an exercise - it's transcription. This
is a different, deeper problem than the max_safe_depth/alert_color mistake
(those were real logic, just unnecessarily split out); this is "the
assignment has no puzzle in it at all," no matter how the region is fenced
or how sparse the surrounding hints are.

The distinction that survives: reproducing existing engine internals (the
`Submarine` class, `world_y_to_screen`, anything already running) has this
problem. Writing genuinely new content that doesn't exist anywhere yet -
the `Creature` class(es) at Module 10/11, once creatures exist - does not,
since there's nothing finished to copy. Whether that new content physically
lives in `engine.py` or `main.py` is just a file-organization choice at that
point, not a different kind of ownership.

Softer alternative, not a graded exercise: nudge students to *read* through
`engine.py` once they have the background to follow it (e.g. a one-line
suggestion in a later briefing - "this is a good week to go read the
Submarine class now that you know what a class is"), rather than asking them
to reproduce it. Understanding beats rewriting-what-already-works here.

Historical roadmap (superseded by the above, kept for context on what was
tried and why it changed):

- **Module 5 (Functions):** done as planned - `frame()`'s contents split into
  named functions in `main.py`. Didn't touch `engine.py`; the actual
  instructor prompted directly for that at the time and it was talked back
  down to this for two reasons - `frame()`'s decomposition is a purer Module 5
  lesson on its own, and `tools/sync_engine.py`'s one-canonical-file model
  still isn't carry-forward-aware, so Module 10 remains the right place to
  pay that cost.

  First draft had four functions (`current_alert`, `alert_color`,
  `handle_controls`, `draw_dashboard`) with pre-written `def` lines, like
  every prior checkpoint. Instructor review cut it to two, on two separate
  grounds:
  - **`current_alert` and `alert_color` were both manufactured splits**, the
    same mistake as cp04's original `max_safe_depth` - called from exactly
    one place each, no duplication avoided. `frame()`'s only two genuine
    seams are drawing vs. input handling, so that's what got kept:
    `draw_dashboard(screen, sub, alert)` and `handle_controls(sub)`, both
    void. The 3-line hull/oxygen/alert computation stays inline in the
    *provided* `frame()` - it doesn't need to be a separate function just
    because `frame()` used to be messy; `frame()` not being "your code"
    means it doesn't have to be minimal, only correct.
  - **The `def` lines were removed entirely.** The instructor's original
    framing for this checkpoint was explicitly "students write the headers
    themselves" - giving a pre-written `def name(params):` line (as every
    checkpoint before this one does) undercuts that regardless of how sparse
    the rest of the scaffolding is. The YOUR CODE section is now a comment
    specifying the two required names/signatures in prose, with no code at
    all - `python main.py` genuinely raises `NameError` until both exist.
    That's a real, deliberate regression from the "the game always runs,
    even blank" guarantee every earlier checkpoint keeps; accepted here
    because the task is small enough (copy two groups of lines out of your
    own Checkpoint 4 `frame()`, name them, done) that the safety net matters
    less than the point of the exercise. `check.py` still fails a blank
    submission cleanly (0/13, no crash) via its existing `hasattr` checks.
- **Module 7 (Lists) / Module 9 (Dicts):** build the creature list and the
  catalog dict as student-owned from the start (in `main.py`, since that's new
  content, not a migration) rather than engine-managed state a checkpoint
  merely reads.
- ~~**Module 10 (Classes):** the first real `engine.py` hand-off candidate -
  open up the `Submarine` class (and `Creature`) for students to author
  directly in the engine file... "I wrote the submarine" becomes literally
  true.~~ **Retired** - the `Submarine` class already runs and is already
  visible; asking students to rewrite it is the transcription problem above.
  `Creature` (Module 10/11) is a different case - see below.
- ~~**Module 11 (Inheritance):** creature subclasses, likely also written
  directly into (or alongside) the engine's class hierarchy.~~ **Still
  possibly true, but not as a "hand-off"** - if `Creature` subclasses get
  written directly in `engine.py` rather than `main.py`, that's just a file
  placement choice once creatures exist, not engine ownership migrating.
- ~~**Final project:** by this point as much of `engine.py` as is reasonable
  should have passed through student hands...~~ **Retired.** The goal now is
  that students have written substantial, real code all semester (which
  `main.py` alone already delivers) - not that they've specifically touched
  the file named `engine.py`.

The `tools/sync_engine.py` infrastructure concern this used to raise (a
carry-forward-aware engine sync, once `engine.py` is partly student-edited)
is moot - `engine.py` stays fully instructor-owned and identical across
every checkpoint, same as `check.py` always has been. No sync rework needed.

---

## Status of this repo

- [x] `engine.py` v1.0 - window, loop, keyboard, ocean/darkness rendering, sub systems sim, HUD (pilot / target-depth line / ballast->dive-rate / power), dive-plan I/O, `draw_tick` (optional color arg from cp04 on), `draw_ring`, `draw_hud_text` (dashboard layer composited on top of the darkness so status readouts never get dimmed - see below), `play_tone`/`wait` (synthesized beeps + pause, from cp04 on - no-ops under `LUMEN_HEADLESS`)
- [x] `cp02_io`, `cp03_decisions`, `cp04_loops`, `cp05_functions` - complete (main + briefing + check + reference solution)
- [ ] `cp06` - `cp12` - not built yet
- [ ] `solution/lumen_full.py` - the finished game for playtesting - not built yet
- [ ] `tools/build_zips.py` - one-command per-checkpoint zip builder - not built yet
