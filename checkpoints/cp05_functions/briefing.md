# Checkpoint 5 - Breaking frame() Apart

**Module 5: Functions**
**Concepts:** defining and calling functions, value-returning vs. void functions, parameters, calling a function from inside another function

---

## The story so far

`frame()` has been doing a lot of work. By Checkpoint 4 it was computing the
hull/oxygen/alert status, drawing four separate HUD lines, and handling three
keys - all inline, all in one function. That's exactly the kind of tangle
Module 5 exists to fix: pull related work out into its own named function, so
`frame()` just calls a handful of clearly-named pieces instead of running
thirty lines of mixed logic.

This week you're not adding a new instrument - you're reorganizing code you
already understand into four functions, two of which *return a value* and
two of which don't return anything at all (they just do something). Nothing
you write this week changes what the game looks like when it runs; if you do
it right, it should look and play exactly like Checkpoint 4 did.

---

## What to do

Open `main.py`. Write the FOUR functions between `BEGIN YOUR CODE
(Checkpoint 5)` and `END YOUR CODE`. This time you're not just filling in a
body under a `def` line someone else planned out - you're deciding what each
function does and calling your own other functions from inside it, the same
way `frame()` calls them.

> Below your code: `frame()` is provided, now much shorter, then a
> **Checkpoint 4 (carried over)** section with reference versions of last
> week's four functions, then **Checkpoint 3 (carried over)** with reference
> versions of all five of that week's functions - your new functions this
> week call several of those directly - then **Checkpoint 2 (carried over)**
> with the pre-dive intake. If you did those checkpoints, paste your own
> versions in over the references.

### 1. `current_alert(sub)` - value-returning

Combines the hull and oxygen readouts into one overall alert level, the same
three lines `frame()` used to run by itself. Call your Checkpoint 3
functions - `hull_status`, then `oxygen_state`, then `overall_alert` - and
return whatever the last one gives you. Nothing is drawn here; this function
only computes and hands back a string.

### 2. `alert_color(alert)` - value-returning

| `alert` | Returns |
|---|---|
| `"DANGER"` | `(230, 90, 80)` |
| `"WARNING"` | `(230, 190, 90)` |
| anything else | `(90, 200, 150)` |

A function's return value doesn't have to be a number or a string - a color
tuple works just as well.

### 3. `handle_controls(sub)` - void

Everything `frame()` used to do with `DOWN` / `UP` / `L`:

| Condition | Effect |
|---|---|
| `DOWN` held **and** `can_descend(sub.ballast, sub.power, sub.hull)` | `sub.descending = True` |
| `UP` held | `sub.ascending = True` |
| `L` just pressed (not held) | flip `sub.light_on` |

This one changes `sub` directly and returns nothing - that's what makes it a
void function instead of a value-returning one.

### 4. `draw_dashboard(screen, sub, alert)` - void

Everything `frame()` used to do with `draw_hull_status` / `draw_hud_text`.
Takes `alert` as a parameter rather than recomputing it, since `frame()`
already has it from `current_alert()`.

| Line | Position | Size | Color |
|---|---|---|---|
| hull status (`engine.draw_hull_status`) | - | - | (handled internally) |
| `"O2: " + <oxygen state>` | `(engine.WIDTH // 2, 46)`, `anchor="midtop"` | `15` | `(150, 190, 210)` |
| `f"STATUS: {alert}"` | `(engine.WIDTH // 2, 66)`, `anchor="midtop"` | `14` | the matching alert color |
| `"DOWN dive   UP rise   L light   ESC quit"` | `(16, engine.HEIGHT - 26)` | `13` | `(120, 140, 155)` |

You'll need `hull_status(sub.depth, sub.rated_depth)` for the hull line and
`oxygen_state(sub.oxygen)` for the O2 line - both from Checkpoint 3. For the
STATUS line's color, you already wrote a function for exactly this.

---

## Try it

Run `python main.py`. Everything should behave exactly like Checkpoint 4:
the countdown, the depth gauge, the sonar sweep, the HULL/O2/STATUS
readouts, the controls. If something looks different, that's a sign a
function isn't doing quite what `frame()` used to do inline - compare
against what Checkpoint 4's `frame()` did line by line.

---

## Done when

`python check.py` prints **21 / 21** (100 points). It checks:

- `current_alert()` returns the right level across several hull/oxygen
  combinations, including that `"DANGER"` wins when both are bad
- `alert_color()` returns the right tuple for each level
- `handle_controls()` sets `sub.descending` / `sub.ascending` / `sub.light_on`
  correctly for different key combinations, including that `DOWN` is
  correctly blocked when `can_descend` is `False`
- `draw_dashboard()` draws exactly the right three lines of text plus the
  hull status, with the right position, size, and color on each

Submit your `main.py` to Canvas. (Run `check.py` first to see your score -
the grader runs the same check on the file you turn in.)

---

## Hints

- `current_alert` and `alert_color` are both short - two or three lines each.
  If either is getting long, you're probably recomputing something you don't
  need to.
- `handle_controls` doesn't need `elif` - each key is its own independent
  `if`, exactly like Checkpoint 4's `frame()` had them.
- `draw_dashboard` calls four things and returns nothing. If `check.py` says
  it drew the wrong number of lines, count your `draw_hud_text` calls.
- A void function can still call other functions and use their return
  values - it just doesn't hand anything back to *its own* caller.

## If you're stuck / joining late

You don't need your Checkpoint 2, 3, or 4 files - the carried-over sections
at the bottom of `main.py` already have working versions of all three. Do
the `SETUP.md` setup if you haven't, then fill in the four function bodies
here. If you *did* do the earlier checkpoints, swap your own code into those
sections so the game stays fully yours.
