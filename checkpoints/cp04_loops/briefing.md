# Checkpoint 4 - Loops: Clearance, Range, and the Depth Scale

**Module 4: Repetition Structures**
**Concepts:** `while` loops, `for` loops with `range()`, input validation loops, accumulators, augmented assignment (`-=`, `+=`)

---

## The story so far

Two upgrades this week. Before the dive, mission control won't accept an
impossible target depth - it makes you re-enter until it's sane. And the cockpit
now paints a **depth scale** down the right side of the window, plus a readout of
how far your current battery could actually take you.

All three are loops.

---

## What to do

Open `main.py`. Fill in the three function bodies between `BEGIN YOUR CODE` and
`END YOUR CODE`. Don't change the `def` lines.

### 1. `read_valid_depth()` - a validation `while` loop

- Ask: `Target depth (m): ` and read a whole number (`int(input(...))`).
- If it's `< 1` or `> 6000`, print `Out of range - enter 1 to 6000.` and ask again.
- Loop until the number is in range, then `return` it as an `int`.
- Assume the pilot types digits. (Bad text like `"abc"` is a Module 6 problem.)

### 2. `max_safe_depth(start_power)` - an accumulator `while` loop

- Start at depth `0` with `start_power` percent of battery.
- `METRES_PER_PERCENT` is already defined (`= 20`): every 1 percent of battery
  buys 20 m of descent.
- While there is at least 1 whole percent of power left (`power >= 1`):
  subtract `1` from power, add `METRES_PER_PERCENT` to the depth.
- `return` the depth reached, as an `int`.

| Call | Returns |
|---|---|
| `max_safe_depth(100)` | `2000` |
| `max_safe_depth(50)` | `1000` |
| `max_safe_depth(1)` | `20` |
| `max_safe_depth(0)` | `0` |

### 3. `draw_depth_ticks(screen, sub)` - a `for` loop over `range()`

- Loop: `for d in range(0, TICK_MAX + 1, TICK_STEP):` (0, 100, 200, ... 2000).
- For each depth `d`:
  ```python
  y = engine.world_y_to_screen(sub, d)
  engine.draw_tick(screen, y, d)
  ```
- That's the whole body - the engine handles the actual drawing and hides
  markers that are off-screen.

---

## Try it

Run `python main.py`. At the prompt, type `-5`, then `99999`, then `450` - you
should get two "out of range" messages, then the game opens. Once you're in,
hold **DOWN** and watch the metre labels on the right slide past, and watch
`POWER RANGE` drop as the battery drains.

---

## Done when

`python check.py` prints **13 / 13** (100 points). It checks:

- `read_valid_depth()` rejects out-of-range numbers and returns the first valid
  one, as an `int` (tested with `-5, 70000, 0, 450` and with boundaries `1` and `6000`)
- `max_safe_depth()` returns the values in the table above
- `draw_depth_ticks()` calls `engine.draw_tick` once per marker, for depths
  `0, 100, 200, ... , 2000` in order

Paste the check.py output into the Canvas submission.

---

## Hints

- Validation loop shape: set the value once before the loop, then
  `while value < 1 or value > 6000:` ... ask again inside.
- In `max_safe_depth`, use two variables (`power`, `depth`) and `power -= 1`,
  `depth += METRES_PER_PERCENT` each pass. Return `depth`.
- `range(0, TICK_MAX + 1, TICK_STEP)` - the `+ 1` is what makes `2000` itself
  get drawn.
- `draw_depth_ticks` returns nothing. It just loops and draws.

## If you're stuck / joining late

You don't need your Checkpoint 2 or 3 files. This checkpoint stands alone -
`main.py` here has its own pre-dive step and the engine handles the rest. Do the
`SETUP.md` setup if you haven't, then edit only the three function bodies here.
