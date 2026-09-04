# Checkpoint 3 - Hull, Air, and the Decision to Dive

**Module 3: Decision Structures and Boolean Logic**
**Concepts:** `if` / `elif` / `else`, comparison operators, `and` / `or` / `not`, returning a value

---

## The story so far

The submarine now reads the dive plan you built in Checkpoint 2 - that code is
carried into this week's `main.py`, at the bottom - and actually descends. But
the deep is dangerous: too deep and the hull fails, the air runs down the whole
time, and you should not be able to dive when you're out of ballast or power. The
engine tracks all those numbers - it just needs **you** to make the judgement
calls.

---

## What to do

Open `main.py`. This week's work is the bodies of the five functions between
`BEGIN YOUR CODE (Checkpoint 3)` and `END YOUR CODE`. Don't change the `def`
lines.

> The bottom of the file has a **Checkpoint 2 (carried over)** section with a
> working reference copy of last week's pre-dive intake. If you did Checkpoint 2,
> paste your own version in there - it's your game. Either way, don't touch
> `frame()`, and see the note below about wiring in `clamp_battery()`.

### 1. `clamp_battery(battery_pct)`

Battery gauges can't read more than 100%. If `battery_pct` is greater than 100,
return `100` instead. Otherwise return `battery_pct` unchanged.

This one is already wired up for you: the pre-dive intake at the bottom of the
file calls `clamp_battery(float(input(...)))` on the raw input. If you paste in
your *own* Checkpoint 2 code, wrap that same line the same way.

(There's a one-line way to write this with a function called `min()` - you'll
meet it later in the course. For now, use a plain `if` statement.)

### 2. `hull_status(depth_m, rated_m)`

| Condition | Return |
|---|---|
| `depth_m` less than `rated_m` | `"OK"` |
| `depth_m` at least `rated_m`, but less than `1.5 * rated_m` | `"CAUTION"` |
| `depth_m` at least `1.5 * rated_m` | `"BREACH"` |

### 3. `oxygen_state(oxygen_pct)`

| Condition | Return |
|---|---|
| greater than 50 | `"GOOD"` |
| greater than 15, up to and including 50 | `"LOW"` |
| 15 or less | `"CRITICAL"` |

### 4. `can_descend(ballast_kg, power_pct, hull_pct)`

Return `True` only when **all three** are true: `ballast_kg > 0`,
`power_pct > 0`, **and** `hull_pct > 0`. Otherwise return `False`. Chain two
`and`s together.

### 5. `overall_alert(hull_label, oxygen_label)`

Combine your hull and oxygen readouts into one overall alert level:

| Condition | Return |
|---|---|
| `hull_label` is `"BREACH"` **or** `oxygen_label` is `"CRITICAL"` | `"DANGER"` |
| otherwise, `hull_label` is `"CAUTION"` **or** `oxygen_label` is `"LOW"` | `"WARNING"` |
| otherwise (both are fine) | `"SAFE"` |

Check the `"DANGER"` condition **first**. A `"CAUTION"` hull with `"CRITICAL"`
oxygen must come out `"DANGER"`, not `"WARNING"` - if you check the WARNING
condition first, that combination gets it wrong.

---

## What your dive plan controls

The four values from the Checkpoint 2 intake all feed into the dive. The engine
shows them on the HUD as you play:

| You entered | What it does in the game |
|---|---|
| **Pilot name** | shown top-right on the HUD - and on the sub's epitaph if you don't make it back |
| **Target depth** | the mission goal: a "m to go" readout, and a dashed **TARGET DEPTH** line in the water once you're near it |
| **Ballast (kg)** | sinking weight - more ballast means a faster dive (`DIVE __ m/s` on the HUD) |
| **Battery (%)** | your starting `PWR` - runs the light and, via `can_descend`, decides when you can't go deeper |

---

## Try it

Run `python main.py`. Type a dive plan at the prompts - try **pilot** your name,
**target depth** `900`, **ballast** `70`, **battery** `150` (yes, over 100 - see
what `PWR` starts at). When the window opens: your name is top-right,
`BALLAST 70 kg -> DIVE ~29 m/s`, and `TARGET 900 m (... m to go)`. Hold **DOWN**
to dive - watch the `HULL:` readout go `OK`
-> `CAUTION` -> `BREACH` past 1000 m and 1500 m, watch the TARGET line appear and
turn green as you pass 900 m, and confirm that once `PWR` hits 0 you can no
longer descend. Also watch the new `STATUS:` line under `O2:` - it should turn
from green `SAFE` to yellow `WARNING` around the time `HULL:` hits `CAUTION`,
and to red `DANGER` once it hits `BREACH`.

Notice the `HULL:`, `O2:`, and `STATUS:` readouts stay perfectly readable even
in total darkness, just like the O2 / PWR / HULL bars in the top-left - they're
cockpit instruments, not something you're seeing through the window. Only the
water outside goes dark.

---

## Done when

`python check.py` prints **28 / 28** (100 points). It imports your five
functions and calls them with these values:

```
clamp_battery(150)  -> 100      clamp_battery(100)  -> 100
clamp_battery(101)  -> 100      clamp_battery(99.5) -> 99.5
clamp_battery(0)    -> 0

hull_status(500, 1000)   -> "OK"          oxygen_state(80) -> "GOOD"
hull_status(999, 1000)   -> "OK"          oxygen_state(51) -> "GOOD"
hull_status(1000, 1000)  -> "CAUTION"     oxygen_state(50) -> "LOW"
hull_status(1499, 1000)  -> "CAUTION"     oxygen_state(16) -> "LOW"
hull_status(1500, 1000)  -> "BREACH"      oxygen_state(15) -> "CRITICAL"
hull_status(4000, 1000)  -> "BREACH"      oxygen_state(0)  -> "CRITICAL"

can_descend(40, 100, 100) -> True     can_descend(0, 100, 100) -> False
can_descend(40, 0, 100)   -> False    can_descend(40, 100, 0)  -> False
can_descend(0, 0, 0)      -> False

overall_alert("OK", "GOOD")             -> "SAFE"
overall_alert("CAUTION", "GOOD")        -> "WARNING"
overall_alert("OK", "LOW")              -> "WARNING"
overall_alert("BREACH", "GOOD")         -> "DANGER"
overall_alert("OK", "CRITICAL")         -> "DANGER"
overall_alert("CAUTION", "CRITICAL")    -> "DANGER"
```

Submit your `main.py` to Canvas. (Run `check.py` first to see your score - the
grader runs the same check on the file you turn in.)

---

## Hints

- `clamp_battery` needs one `if`, no `elif`: `if battery_pct > 100:` set it to
  `100`; either way, `return battery_pct` at the end.
- Decide whether each comparison is `<` or `<=` and test it.
- `elif` handles "the previous condition was false, now check this one".
- `can_descend` needs no `if` at all - one `return` with two `and`s.
- `overall_alert` is an `if` / `elif` / `else`, each condition joined with `or`.
  Order matters: put the `"DANGER"` check first, `"WARNING"` second, or the
  mixed case (bad hull, fine oxygen - or the reverse) will come out wrong.
- Return the string (or number), don't `print()` it. The game and the checker
  both need the returned value.

## If you're stuck / joining late

You don't need your Checkpoint 2 files to start - the carried-over section at the
bottom of `main.py` already has a working version, already wired to
`clamp_battery()`. Do the `SETUP.md` setup if you haven't, then fill in the five
function bodies. If you *did* do Checkpoint 2, swap your own intake code into
that bottom section (keeping the `clamp_battery(...)` wrapper on the battery
line) so the game is fully yours.
