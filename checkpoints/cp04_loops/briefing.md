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
`hull_status`), and a long-range **sonar sweep** - pulses that continuously
travel outward from the sub, much farther than your light reaches, so you get
some awareness of what's out there before you're close enough to actually see
it. Both are drawn one piece at a time, with a loop.

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

Loop: `for d in range(0, TICK_MAX + 1, TICK_STEP):` (0, 100, 200, ... 2000).
For each depth `d`, figure out how dangerous it is and draw it in that color:

```python
status = hull_status(d, sub.rated_depth)   # your Checkpoint 3 function
if status == "OK":
    color = OK_COLOR
elif status == "CAUTION":
    color = CAUTION_COLOR
else:
    color = BREACH_COLOR
y = engine.world_y_to_screen(sub, d)
engine.draw_tick(screen, y, d, color)
```

`OK_COLOR`, `CAUTION_COLOR`, and `BREACH_COLOR` are already defined for you at
the top of the file - same colors the `HULL:` readout uses.

### 4. `draw_sonar_rings(screen, sub)` - a `for` loop, animated over time

Sonar reaches much farther than your light (`SONAR_RANGE_MAX = 400` pixels,
versus the light's `155`), and instead of sitting still, a few pulses are
always traveling outward and looping back - a real sonar ping, not a static
picture. Range still depends on battery, same as the light:

```python
sonar_range = sub.power * (SONAR_RANGE_MAX / 100)   # 0 at dead battery, 400 at full

for i in range(PULSE_COUNT):
    offset = i / PULSE_COUNT                  # 0, 0.25, 0.5, 0.75 for 4 pulses
    fraction = (engine.now() / SWEEP_SECONDS + offset) % 1.0
    radius = fraction * sonar_range
    engine.draw_ring(screen, (engine.WIDTH // 2, engine.SUB_SCREEN_Y), radius)
```

`engine.now()` returns seconds since the game started, and it only ever counts
up. Dividing by `SWEEP_SECONDS` and taking `% 1.0` turns that into a value
that climbs from 0 to 1 and then starts over every `SWEEP_SECONDS` - that reset
is what makes each pulse look like it travels out to `sonar_range` and then
begins again at the sub, on a loop, forever. At `t = 0` with full battery the
four pulses sit at radius `0, 100, 200, 300` - by `t = 1.25` (half a sweep)
they've moved to `100, 150, 0, 50` (that last one already wrapped around).

---

## Try it

Run `python main.py`. The pre-dive intake now rejects an out-of-range target
depth (try `-5`, then `99999`, then `1200`) before the window opens. Once
you're in: four sonar pulses should be visibly expanding outward from the sub
and looping back every couple of seconds, reaching much farther out than your
light's cone. The depth scale on the right should show green ticks near the
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
- `draw_sonar_rings`: `sonar_range` is computed once, before the loop - it
  doesn't change per pulse, only `offset` and `fraction` do. Type the formula
  exactly as given; the `%` (modulo) is what makes it wrap instead of growing
  forever.
- Both drawing functions return nothing. They just loop and draw.

## If you're stuck / joining late

You don't need your Checkpoint 2 or 3 files - the carried-over sections at the
bottom of `main.py` already have working versions of both, already wired
together (battery through `clamp_battery()`, target depth through this week's
`read_valid_depth()`). Do the `SETUP.md` setup if you haven't, then fill in the
four function bodies here. If you *did* do Checkpoints 2 and 3, swap your own
code into those sections so the game stays fully yours.
