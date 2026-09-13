# Checkpoint 4 - Depth Gauge, Sonar, and Battery Range

**Module 4: Repetition Structures**
**Concepts:** `while` loops, `for` loops with `range()`, input validation loops, accumulators, augmented assignment (`-=`, `+=`)

---

## The story so far

Checkpoints 2 and 3 are carried into this week's `main.py` - the pre-dive
intake at the very bottom, and your five Checkpoint 3 functions just above it.
This week the cockpit gets two new instruments, and both are actually *for*
something, not just decoration: a **depth gauge** running down the right edge
of the screen, color-coded by how dangerous each depth is (reusing last week's
`hull_status`), and a long-range **sonar sweep** - a few pulses that slowly and
continuously travel outward from the sub, much farther than your light
reaches, so you get some awareness of what's out there before you're close
enough to actually see it. Both are drawn one piece at a time, with a loop.

---

## What to do

Open `main.py`. Fill in the four functions between `BEGIN YOUR CODE
(Checkpoint 4)` and `END YOUR CODE`. Don't change the `def` lines.

> Below your code: `frame()` is provided (uses everything, including your new
> functions - nothing to change there), then a **Checkpoint 3 (carried over)**
> section with working reference versions of all five of last week's functions,
> then a **Checkpoint 2 (carried over)** section with the pre-dive intake. If
> you did those checkpoints, paste your own versions in over the references.
> One small wiring change either way: the pre-dive intake's target-depth line
> now calls this week's `read_valid_depth()` instead of a plain `int(input())`.

### 1. `read_valid_depth()` - a validation `while` loop

- Ask: `Target depth (m): ` and read a whole number (`int(input(...))`).
- If it's `< 1` or `> 6000`, print `Out of range - enter 1 to 6000.` and ask
  again.
- Loop until the number is in range, then `return` it as an `int`.
- Assume the pilot types digits. (Bad text like `"abc"` is a Module 6 problem.)

### 2. `max_safe_depth(start_power)` - an accumulator `while` loop

- Start at depth `0` with `start_power` percent of battery.
- `METERS_PER_PERCENT` is already defined (`= 20`): every 1 percent of battery
  buys 20 m of descent.
- While there is at least 1 whole percent of power left (`power >= 1`):
  subtract `1` from power, add `METERS_PER_PERCENT` to the depth.
- `return` the depth reached, as an `int`.

| Call | Returns |
|---|---|
| `max_safe_depth(100)` | `2000` |
| `max_safe_depth(50)` | `1000` |
| `max_safe_depth(1)` | `20` |
| `max_safe_depth(0)` | `0` |

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

Sonar reaches much farther than your light (`SONAR_RANGE_MAX = 400` pixels,
versus the light's `155`), and instead of sitting still, a few pulses are
always slowly traveling outward and looping back - a real sonar ping, not a
static picture. Range still depends on battery, same idea as the light:
`0` pixels at dead battery, `SONAR_RANGE_MAX` at a full one.

Loop over `range(PULSE_COUNT)`. Every pulse travels at the same speed, but
they don't all start at the same point in their trip - spread their starting
points evenly across `0` to `1` using `i / PULSE_COUNT` (so with 4 pulses:
`0, 0.25, 0.5, 0.75`).

A pulse's position is a fraction from `0` (just leaving the sub) to `1`
(reached max range). `engine.now()` returns seconds since the game started
and only ever counts up, so dividing it by `SWEEP_SECONDS` and adding a
pulse's own starting point gives a number that climbs forever. Taking that
value `% 1.0` (modulo) is what turns an endless climb into something that
counts `0 -> 1 -> 0 -> 1 ...`, once every `SWEEP_SECONDS` - without the `%`,
a pulse would just keep flying outward past the edge of the screen instead of
looping back to the sub.

Once you have that `0`-`1` fraction for a pulse, its radius is that fraction
of this frame's sonar range. Draw it centered on the sub with
`engine.draw_ring(screen, (engine.WIDTH // 2, engine.SUB_SCREEN_Y), radius)`.

Worked example, full battery: at `t = 0` the four pulses sit at radius
`0, 100, 200, 300` - by `t = 4.0` (half a sweep) they've moved to
`200, 300, 0, 100` (the third one already wrapped back around to `0`).

---

## Try it

Run `python main.py`. The pre-dive intake now rejects an out-of-range target
depth (try `-5`, then `99999`, then `1200`) before the window opens. Once
you're in: four sonar pulses should be slowly, smoothly expanding outward from
the sub and looping back every few seconds, reaching much farther out than
your light's cone. The depth scale on the right should show green ticks near the
surface, turning yellow past 1000 m and red past 1500 m (assuming a 1000 m
rated hull). Hold **DOWN** and watch `POWER RANGE` drop as the battery drains
- and watch the sonar pulses reach less and less far as `PWR` drops toward 0.
Confirm you can't descend once `PWR`, ballast, or `HULL` hits 0 - same gate as
last week, now with hull added.

---

## Done when

`python check.py` prints **19 / 19** (100 points). It checks:

- `read_valid_depth()` rejects out-of-range numbers and returns the first
  valid one, as an `int` (boundaries `1` and `6000` included)
- `max_safe_depth()` returns the values in the table above
- `draw_depth_ticks()` calls `engine.draw_tick` once per marker (`0` to
  `2000`), with the correct on-screen position **and** the correct color for
  each depth
- `draw_sonar_rings()` calls `engine.draw_ring` with the right radius for each
  pulse, at several different combinations of battery level and time, always
  centered on the sub

Submit your `main.py` to Canvas. (Run `check.py` first to see your score - the
grader runs the same check on the file you turn in.)

---

## Hints

- Validation loop shape: set the value once before the loop, then
  `while value < 1 or value > 6000:` ... ask again inside.
- In `max_safe_depth`, use two variables (`power`, `depth`) and `power -= 1`,
  `depth += METERS_PER_PERCENT` each pass. Return `depth`.
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
- Both drawing functions return nothing. They just loop and draw.

## If you're stuck / joining late

You don't need your Checkpoint 2 or 3 files - the carried-over sections at the
bottom of `main.py` already have working versions of both, already wired
together (battery through `clamp_battery()`, target depth through this week's
`read_valid_depth()`). Do the `SETUP.md` setup if you haven't, then fill in the
four function bodies here. If you *did* do Checkpoints 2 and 3, swap your own
code into those sections so the game stays fully yours.
