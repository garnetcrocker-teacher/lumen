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

You can now drift sideways with `LEFT`/`RIGHT`. The sub stays centered on
screen either way - the water and the drifting specks scroll past it
instead, the same way the world already scrolls vertically as you dive.
There's no limit to how far you can go in either direction, and the game
now keeps an odometer of how far you've drifted in total, in either
direction - it's on the dashboard, bottom right.

There's also an actual destination now: the dive site you're descending
toward isn't directly below where you started (`sub.target_x` holds its
horizontal position - real launch points rarely land you exactly on top of
the thing you're diving to find). Your own `POSITION` reading (in the
top-left corner, under `DEPTH`) tells you where you are; this week you
build the piece that tells you which way the site is and how far, so you
can actually steer toward it.

Most of `draw_dashboard` and `handle_controls` should be quick - you're not
writing new logic for them, nearly every line you need is already sitting
almost word-for-word inside your own Checkpoint 4 `main.py`'s `frame()`.
Open it side by side with this one. The sideways movement flags, the
odometer readout, and the heading-to-site readout are the pieces that are
genuinely new - and the two new readouts need two new functions,
`format_distance` and `heading_to_target`, to decide how to show them.

---

## What to do

Open `main.py`. Write FOUR functions between `BEGIN YOUR CODE (Checkpoint
5)` and `END YOUR CODE`. Unlike every checkpoint before this, there's no
`def` line waiting for you - you're deciding the name and parameters
yourself and writing the whole thing.

> Below your code: `frame()` is provided, now much shorter, then a
> **Checkpoint 4 (carried over)** section with reference versions of last
> week's four functions, then **Checkpoint 3 (carried over)** with reference
> versions of all five of that week's functions - your functions this
> week call several of those directly - then **Checkpoint 2 (carried over)**
> with the pre-dive intake. If you did those checkpoints, paste your own
> versions in over the references.

### 1. `format_distance(meters)` - returns a string

The engine now keeps `sub.total_drift`, a running total in meters of how
far you've drifted sideways, counting both directions. Write a function
that turns that number into a display string:

- below 1000, show it in meters, no decimal place: `"340 m"`
- 1000 or above, show it in kilometers, one decimal place instead:
  `"1.2 km"`

There's nothing to copy for this one anywhere in your old checkpoints - the
logic is new, but the shape (an `if`/`else` that picks one of two return
values) is the same idea as `hull_status` or `oxygen_state` from
Checkpoint 3. Unlike those two functions, though, this one hands back a
string, not a status word.

### 2. `heading_to_target(offset_m)` - returns a string

`sub.target_x` is the dive site's horizontal position; `sub.x` is yours.
Whoever calls this works out `offset_m` as `sub.target_x - sub.x` and
hands it to you - positive means the site is to your RIGHT, negative means
LEFT. Turn that into a string like `"340 m RIGHT"` or `"1.2 km LEFT"`:

- work out the direction from the sign of `offset_m`
- call your own `format_distance()` on the *size* of the offset (its
  absolute value, not the sign) to get the `"340 m"` / `"1.2 km"` part
- put the direction word after it

Nothing to copy here either - it's new, same as `format_distance`. Notice
this one calls that one: a function you wrote calling another function you
wrote, which is exactly the kind of thing this module is about.

### 3. `draw_dashboard(screen, sub, alert)` - void

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

Then add two more lines, using the functions you just wrote.

Call `format_distance(sub.total_drift)` and draw the result as
`"DRIFTED: " + format_distance(sub.total_drift)`, in the bottom-right
corner - mirroring the hint line's spot in the bottom-left. Same size (13)
and color (`(120, 140, 155)`) as the hint line, position
`(engine.WIDTH - 16, engine.HEIGHT - 26)`, anchor `"topright"`.

Call `heading_to_target(sub.target_x - sub.x)` and draw the result as
`"SITE: " + heading_to_target(sub.target_x - sub.x)`, at
`(engine.WIDTH // 2, 86)`, anchor `"midtop"`, same size and color as the
other two.

### 4. `handle_controls(sub)` - void

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

`draw_dashboard` and `handle_controls` change things (drawing to the
screen, or changing `sub`) and hand nothing back - that's what makes them
void instead of value-returning. `format_distance` and `heading_to_target`
are the opposite: neither draws or changes anything, they just hand a
string back to whoever called them. Inside `draw_dashboard`, you're
calling both of them - one of your own functions calling another - plus
`hull_status`, `oxygen_state`, and `can_descend`, all from Checkpoint 3,
and `heading_to_target` itself calls `format_distance`. A void function
can absolutely use another function's return value; it just doesn't pass
anything back to *its own* caller.

---

## Try it

Because nothing is pre-written this week, running `python main.py` before
all four functions exist will crash with a `NameError` - that's expected,
not a bug. Get them written, then run it: the countdown, the depth gauge,
the sonar sweep, and the HULL/O2/STATUS readouts should all behave exactly
like Checkpoint 4. If something there looks different, compare against what
Checkpoint 4's `frame()` did line by line - you likely dropped or changed
something in the copy.

Then try `LEFT` and `RIGHT`. The sub stays put in the middle of the screen;
the drifting specks in the water should visibly slide the other way, same
idea as watching the water shift as you dive, just sideways. There's no
wall - hold one direction long enough and you'll just keep going. Watch the
bottom-right corner: the DRIFTED readout should climb the whole time, and
flip from meters to kilometers once it passes 1000. Watch the SITE readout
too - drift the direction it names and the distance should shrink; keep
going past the site and it should flip to the other direction.

---

## Done when

`python check.py` prints **21 / 21** (100 points). It checks:

- `format_distance()` formats both a sub-1000 and an over-1000 value
  correctly
- `heading_to_target()` picks the right direction word for a positive and
  a negative offset, using `format_distance()` correctly for the size
- `handle_controls()` sets `sub.descending` / `sub.ascending` /
  `sub.moving_left` / `sub.moving_right` / `sub.light_on` correctly for
  different key combinations, including that `DOWN` is correctly blocked
  when `can_descend` is `False`
- `draw_dashboard()` draws exactly the right five lines of text plus the
  hull status, with the right position, size, and color on each - checked
  across all three alert levels, so the color logic has to be complete

Submit your `main.py` to Canvas. (Run `check.py` first to see your score -
the grader runs the same check on the file you turn in.)

---

## Hints

- Go copy the lines from your own Checkpoint 4 `frame()` first, then figure
  out the `def` line. Don't try to write `draw_dashboard` or
  `handle_controls` from memory - `format_distance` and `heading_to_target`
  are the two functions here with no source to copy from.
- A function's parameters are just "whatever the lines inside it need from
  outside." If a line uses `screen`, `sub`, or `alert`, that's a parameter.
- `heading_to_target` doesn't need `sub` as a parameter at all - it only
  needs the one number (`offset_m`) that whoever calls it already worked
  out. Compare that to `draw_dashboard`, which does need `sub`.
- `handle_controls` doesn't need `elif` - each key is its own independent
  `if`, exactly like before. `LEFT`/`RIGHT` are two more independent `if`s
  in the exact same style, not a special case.
- If `check.py` says `draw_dashboard` drew the wrong number of lines, count
  your `draw_hud_text` calls against the six things it's supposed to draw
  (hull status, O2, STATUS, the hint line, DRIFTED, and SITE).

## If you're stuck / joining late

You don't need your Checkpoint 2, 3, or 4 files - the carried-over sections
at the bottom of `main.py` already have working versions of all three. Do
the `SETUP.md` setup if you haven't, then write the four functions here,
copying from the reference `frame()`-style logic in those carried-over
sections the same way you would from your own Checkpoint 4 file. If you
*did* do the earlier checkpoints, swap your own code into those sections so
the game stays fully yours.
