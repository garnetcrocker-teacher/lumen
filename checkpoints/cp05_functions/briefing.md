# Checkpoint 5 - Breaking frame() Apart

**Module 5: Functions**
**Concepts:** defining and calling functions, void functions, parameters, calling a function from inside another function

---

## The story so far

`frame()` has really only ever done two jobs: draw the dashboard, and read
the keyboard. Until now both jobs sat inline, mixed into one function. This
week you pull each job out into its own function. Almost nothing you write
changes what the game looks like when it runs - if you do it right, it
should look and play just like Checkpoint 4 did for the depth gauge, sonar,
and HUD, just organized better.

The one real addition: you can now drift sideways with `LEFT`/`RIGHT`. The
sub stays centered on screen either way - the water and the drifting specks
scroll past it instead, the same way the world already scrolls vertically
as you dive. There's no limit to how far you can go in either direction.

Most of this should be quick. You're not writing new logic for
`draw_dashboard` or most of `handle_controls` - nearly every line you need
there is already sitting almost word-for-word inside your own Checkpoint 4
`main.py`'s `frame()`. Open it side by side with this one. The sideways
movement is the one piece that's genuinely new.

---

## What to do

Open `main.py`. Write TWO functions between `BEGIN YOUR CODE (Checkpoint 5)`
and `END YOUR CODE`. Unlike every checkpoint before this, there's no `def`
line waiting for you - you're deciding the name and parameters yourself and
writing the whole thing.

> Below your code: `frame()` is provided, now much shorter, then a
> **Checkpoint 4 (carried over)** section with reference versions of last
> week's four functions, then **Checkpoint 3 (carried over)** with reference
> versions of all five of that week's functions - your two functions this
> week call several of those directly - then **Checkpoint 2 (carried over)**
> with the pre-dive intake. If you did those checkpoints, paste your own
> versions in over the references.

### 1. `draw_dashboard(screen, sub, alert)` - void

Everything Checkpoint 4's `frame()` did with `draw_hull_status` /
`draw_hud_text` - the hull line, the O2 line, the STATUS line (including
the `if`/`elif`/`else` that picks its color), and the controls-hint line at
the bottom. `frame()` hands you `alert` already worked out, same as before.
Copy those lines in, decide what the function needs as parameters to run
them, and write the `def` line. One small update to the controls-hint text
itself, since it needs to mention the new keys - it should now read exactly:

```
DOWN dive   UP rise   LEFT/RIGHT drift   L light   ESC quit
```

### 2. `handle_controls(sub)` - void

Everything Checkpoint 4's `frame()` did with `DOWN` / `UP` / `L`. Same
three `if` statements, same `can_descend(...)` gate on `DOWN` - copy them
in as they were.

Then add two more `if` statements, matching the exact shape of the
`DOWN`/`UP` ones - there's nothing to copy for these, since they're new
this week:

| Condition | Effect |
|---|---|
| `LEFT` held | `sub.moving_left = True` |
| `RIGHT` held | `sub.moving_right = True` |

That's it - you're just setting a flag, the same as `sub.descending` or
`sub.ascending`. The engine applies the actual sideways movement every
frame and resets both flags afterward, exactly like it already does for
diving and rising.

Both functions change things (drawing to the screen, or changing `sub`) and
hand nothing back - that's what makes them void instead of value-returning.
Inside each one, though, you're still calling functions that *do* return a
value - `hull_status`, `oxygen_state`, and `can_descend`, all from
Checkpoint 3. A void function can absolutely use another function's return
value; it just doesn't pass anything back to *its own* caller.

---

## Try it

Because nothing is pre-written this week, running `python main.py` before
either function exists will crash with a `NameError` - that's expected, not
a bug. Get both written, then run it: the countdown, the depth gauge, the
sonar sweep, and the HULL/O2/STATUS readouts should all behave exactly like
Checkpoint 4. If something there looks different, compare against what
Checkpoint 4's `frame()` did line by line - you likely dropped or changed
something in the copy.

Then try `LEFT` and `RIGHT`. The sub stays put in the middle of the screen;
the drifting specks in the water should visibly slide the other way, same
idea as watching the water shift as you dive, just sideways. There's no
wall - hold one direction long enough and you'll just keep going.

---

## Done when

`python check.py` prints **15 / 15** (100 points). It checks:

- `handle_controls()` sets `sub.descending` / `sub.ascending` /
  `sub.moving_left` / `sub.moving_right` / `sub.light_on` correctly for
  different key combinations, including that `DOWN` is correctly blocked
  when `can_descend` is `False`
- `draw_dashboard()` draws exactly the right three lines of text plus the
  hull status, with the right position, size, and color on each - checked
  across all three alert levels, so the color logic has to be complete

Submit your `main.py` to Canvas. (Run `check.py` first to see your score -
the grader runs the same check on the file you turn in.)

---

## Hints

- Go copy the lines from your own Checkpoint 4 `frame()` first, then figure
  out the `def` line. Don't try to write either function from memory.
- A function's parameters are just "whatever the lines inside it need from
  outside." If a line uses `screen`, `sub`, or `alert`, that's a parameter.
- `handle_controls` doesn't need `elif` - each key is its own independent
  `if`, exactly like before. `LEFT`/`RIGHT` are two more independent `if`s
  in the exact same style, not a special case.
- If `check.py` says `draw_dashboard` drew the wrong number of lines, count
  your `draw_hud_text` calls against the four things it's supposed to draw.

## If you're stuck / joining late

You don't need your Checkpoint 2, 3, or 4 files - the carried-over sections
at the bottom of `main.py` already have working versions of all three. Do
the `SETUP.md` setup if you haven't, then write the two functions here,
copying from the reference `frame()`-style logic in those carried-over
sections the same way you would from your own Checkpoint 4 file. If you
*did* do the earlier checkpoints, swap your own code into those sections so
the game stays fully yours.
