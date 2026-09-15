# Checkpoint 4 - Launch Countdown, Depth Gauge, and Sonar

**Module 4: Repetition Structures**
**Concepts:** `while` loops, `for` loops with `range()`, input validation loops, an `if`/`else` inside a loop, augmented assignment (`-=`, `+=`)

---

## The story so far

Checkpoints 2 and 3 are carried into this week's `main.py` - the pre-dive
intake at the very bottom, and your five Checkpoint 3 functions just above it.
This week adds a launch countdown before the dive begins, plus two new cockpit
instruments once you're in the water, and none of it is just decoration: a
**countdown** that counts down out loud and beeps before the window even
opens, a **depth gauge** running down the right edge of the screen,
color-coded by how dangerous each depth is (reusing last week's
`hull_status`), and a long-range **sonar sweep** - a few pulses that slowly
and continuously travel outward from the sub, much farther than your light
reaches, so you get some awareness of what's out there before you're close
enough to actually see it. All three are built with a loop.

(An earlier version of this checkpoint had a fourth function,
`max_safe_depth`, and a `POWER RANGE` readout built from it - "how many
meters you can dive before the battery dies." It's gone now: it turned out
to be pure fiction. Battery in this game only drains while the light is on
(check `engine.py`'s `_update_systems` if you want proof); it never drains
from depth. So the stat wasn't describing a made-up conversion rate, it was
describing a mechanic that doesn't exist. Better to cut it than keep a
number that lies to the pilot.)

---

## What to do

Open `main.py`. Fill in the four functions between `BEGIN YOUR CODE
(Checkpoint 4)` and `END YOUR CODE`. Don't change the `def` lines.

> Below your code: `frame()` is provided (nothing to change there), then a
> **Checkpoint 3 (carried over)** section with working
> reference versions of all five of last week's functions, then a
> **Checkpoint 2 (carried over)** section with the pre-dive intake. If you did
> those checkpoints, paste your own versions in over the references. One
> small wiring change either way: the pre-dive intake's target-depth line now
> calls this week's `read_valid_depth()` instead of a plain `int(input())`,
> and right before launch it now calls your new `countdown_to_dive()`.

### 1. `read_valid_depth()` - a validation `while` loop

- Ask: `Target depth (m): ` and read a whole number (`int(input(...))`).
- If it's `< 1` or `> 6000`, print `Out of range - enter 1 to 6000.` and ask
  again.
- Loop until the number is in range, then `return` it as an `int`.
- Assume the pilot types digits. (Bad text like `"abc"` is a Module 6 problem.)

### 2. `countdown_to_dive(seconds)` - a `while` loop with a decision inside it

A real launch sequence, not just a delay. From `seconds` down to `1`, once per
number:

| Step | What to do |
|---|---|
| 1 | `print(f"T-minus {seconds}...")` |
| 2 | play a beep - normally `engine.play_tone(BEEP_FREQ, BEEP_MS)`, but once `seconds` is `URGENT_THRESHOLD` or less, the higher-pitched `engine.play_tone(URGENT_FREQ, BEEP_MS)` instead |
| 3 | `engine.wait(1)` - pause one second |
| 4 | subtract `1` from `seconds` |

Once the count reaches `0`: `print("DIVE.")` and play the longer launch tone,
`engine.play_tone(DIVE_FREQ, DIVE_MS)`.

`BEEP_FREQ`, `BEEP_MS`, `URGENT_THRESHOLD`, `URGENT_FREQ`, `DIVE_FREQ`, and
`DIVE_MS` are already defined at the top of the file.

| Call | Prints | Beeps at |
|---|---|---|
| `countdown_to_dive(5)` | `T-minus 5...` ... `T-minus 1...` `DIVE.` | normal, normal, urgent, urgent, urgent, then the dive tone |
| `countdown_to_dive(2)` | `T-minus 2...` `T-minus 1...` `DIVE.` | urgent, urgent, then the dive tone |

### 3. `draw_depth_ticks(screen, sub)` - a `for` loop, colored by a decision

Loop over `range(0, TICK_MAX + 1, TICK_STEP)` so `d` takes on `0, 100, 200,
... 2000` (the `+ 1` is what makes `2000` itself get included - `range`'s stop
value is normally exclusive). For each depth `d`:

| Step | What to do |
|---|---|
| 1 | `status = hull_status(d, sub.rated_depth)` (your Checkpoint 3 function) |
| 2 | pick a color: `"OK"` -> `OK_COLOR`, `"CAUTION"` -> `CAUTION_COLOR`, otherwise `BREACH_COLOR` |
| 3 | `y = engine.world_y_to_screen(sub, d)` - converts meters to a screen position |
| 4 | `engine.draw_tick(screen, y, d, color)` - draws the line + label |

`OK_COLOR`, `CAUTION_COLOR`, and `BREACH_COLOR` are already defined for you at
the top of the file - same colors the `HULL:` readout uses.

### 4. `draw_sonar_rings(screen, sub)` - a `for` loop, animated over time

Sonar reaches much farther than your light (`SONAR_RANGE_MAX = 480` pixels,
versus the light's `155`), and instead of sitting still, a few pulses are
always slowly traveling outward and looping back - a real sonar ping, not a
static picture. Range still depends on battery, same idea as the light: `0`
pixels at dead battery, `SONAR_RANGE_MAX` at a full one.

Think of `engine.now()` as a stopwatch that starts at `0` when the game opens
and never stops climbing. Getting from that number to one pulse's radius
takes five steps:

1. **How far into one outward trip are we, ignoring any looping?**
   `engine.now() / SWEEP_SECONDS` - this only ever grows: `0, 0.1, 0.5, 1.0,
   1.5, 2.3`, and on forever. Each whole number is one full trip finished.
2. **Turn that endless growth into a repeating `0`-to-`1` cycle.** Taking that
   value modulo `1` (`% 1.0`) throws away the whole-number part and keeps
   only what's left over - `2.3 % 1.0` is `0.3`. That's the trick that makes
   a pulse restart at the sub every `SWEEP_SECONDS` instead of flying off
   past the edge of the screen forever.
3. **Give each pulse its own starting point in that cycle**, so all
   `PULSE_COUNT` pulses end up spread out instead of stacked on each other.
   Loop over `range(PULSE_COUNT)`; for pulse `i`, add `i / PULSE_COUNT` (`0,
   0.25, 0.5, 0.75` for 4 pulses) before taking `% 1.0`.
4. **Turn that `0`-to-`1` "how far along" number into a pixel radius** by
   multiplying it by `SONAR_RANGE_MAX` - this is the pulse's *true*
   position. It always travels at the same speed; battery doesn't slow it
   down, only shortens how far you can still detect it (next step).
5. **Only draw the pulse if that radius is within this frame's
   battery-scaled `sonar_range`** (`sub.power * (SONAR_RANGE_MAX / 100)`).
   Past that point the ping is still out there, traveling at the same speed
   as always - your equipment just can't pick it up yet, so skip drawing it
   rather than showing it at some shrunken radius.

Draw each visible pulse centered on the sub with
`engine.draw_ring(screen, (engine.WIDTH // 2, engine.SUB_SCREEN_Y), radius)`.

Worked example, full battery (`sonar_range` equals `SONAR_RANGE_MAX`, so
every pulse is always visible): at `t = 0` the four pulses sit at radius `0,
120, 240, 360` - by `t = 8.0` (half a sweep) they've moved to `240, 360, 0,
120` (the third one already wrapped back around to `0`).

At lower battery, `sonar_range` shrinks below `SONAR_RANGE_MAX`, so some
pulses will be traveling *past* what you can currently detect at any given
moment - step 5 is what makes those simply not get drawn that frame, rather
than bunching up at a shrunken edge. Expect anywhere from `0` to
`PULSE_COUNT` pulses visible at once, depending on where each one happens to
be in its trip.

---

## Try it

Run `python main.py`. The pre-dive intake now rejects an out-of-range target
depth (try `-5`, then `99999`, then `1200`). After you enter your dive plan,
the terminal should count down out loud - `T-minus 5...` through `T-minus
1...`, beeping each second (higher-pitched for the last 3), then `DIVE.` -
before the window opens. Once you're in: four sonar pulses should be slowly,
smoothly expanding outward from the sub and looping back every several
seconds, reaching much farther out than your light's cone. The depth scale on
the right should show green ticks near the surface, turning yellow past 1000
m and red past 1500 m (assuming a 1000 m rated hull). Leave the light on for
a while and watch `PWR` drain - as it drops, the sonar pulses should start
disappearing before they reach the edge of the screen instead of shrinking
in toward the sub; they're still moving at the same speed, your instrument
just can't detect them that far out anymore. Confirm you can't descend once
`PWR`, ballast, or `HULL` hits 0 - same gate as last week, now with hull
added.

---

## Done when

`python check.py` prints **20 / 20** (100 points). It checks:

- `read_valid_depth()` rejects out-of-range numbers and returns the first
  valid one, as an `int` (boundaries `1` and `6000` included)
- `countdown_to_dive()` prints the right `T-minus` / `DIVE.` lines, beeps at
  the right pitch at each step, and pauses once per second
- `draw_depth_ticks()` calls `engine.draw_tick` once per marker (`0` to
  `2000`), with the correct on-screen position **and** the correct color for
  each depth
- `draw_sonar_rings()` calls `engine.draw_ring` with the right radius for
  each *currently visible* pulse (some may be out of range and correctly not
  drawn), at several different combinations of battery level and time,
  always centered on the sub

Submit your `main.py` to Canvas. (Run `check.py` first to see your score - the
grader runs the same check on the file you turn in.)

---

## Hints

- Validation loop shape: set the value once before the loop, then
  `while value < 1 or value > 6000:` ... ask again inside.
- `countdown_to_dive`: the `if`/`else` picking the beep goes *inside* the
  `while`, checked fresh each pass - `seconds` is a different number every
  time around.
- `range(0, TICK_MAX + 1, TICK_STEP)` - the `+ 1` is what makes `2000` itself
  get drawn.
- `draw_depth_ticks` needs an `if`/`elif`/`else` *inside* the `for` loop - one
  decision per depth, every time around.
- `draw_sonar_rings`: `sonar_range` only depends on `sub.power`, so compute it
  once before the loop, not once per pulse - only each pulse's own fraction
  changes.
- If your pulses never seem to reset, double check you're taking `% 1.0` of
  the whole `(engine.now() / SWEEP_SECONDS + offset)` expression, not just
  part of it.
- Multiply by `SONAR_RANGE_MAX` to get a pulse's radius, *not* `sonar_range`
  - `sonar_range` only comes in for the visibility check (step 5). Mixing
  the two up is what makes pulses speed up and slow down as the battery
  drains, instead of just fading from view at a shorter distance.
- All three drawing/countdown functions return nothing. They just loop
  (and print, or draw).

## If you're stuck / joining late

You don't need your Checkpoint 2 or 3 files - the carried-over sections at the
bottom of `main.py` already have working versions of both, already wired
together (battery through `clamp_battery()`, target depth through this week's
`read_valid_depth()`). Do the `SETUP.md` setup if you haven't, then fill in the
four function bodies here. If you *did* do Checkpoints 2 and 3, swap your own
code into those sections so the game stays fully yours.
