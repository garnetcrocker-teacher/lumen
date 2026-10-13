# Checkpoint 7 - Creatures

**Module 7: Lists & Tuples**
**Concepts:** building a list in a loop, looping over a list by item and by index, indexing and unpacking, tuples (and why you rebuild them), filtering into a new list, sorting

---

> **Heads up:** this checkpoint is a little longer and more involved than usual. You write six functions instead of the usual three or four, so start early and don't save it for the last day.

## The story so far

You're not alone down here. This week the ocean gets creatures, and one list holds all of them.

Each creature is a tuple: `(x, depth, speed)`. That's its sideways position in meters, its depth in meters, and how fast it swims sideways in meters per second (negative swims left). A tuple can't be changed once it's made.

The world is endless, so the game only keeps a small crowd near you. Every frame it moves the creatures, drops the ones that fell too far behind, and spawns new ones off screen to replace them. Your light only reaches about 40 meters, so most creatures sit in the dark. Sonar hears much farther: the dashboard now has a **CONTACTS** line showing how many creatures sonar hears and how far away the nearest one is.

The `def` lines are given again this week, same as Checkpoints 4 and 6.

---

## What to do

Open `main.py`. Fill in the bodies of the six functions between `BEGIN YOUR CODE (Checkpoint 7)` and `END YOUR CODE`. Don't change any `def` line or the constants above them.

> `creatures = []` and `frame()` are provided. Each frame, `frame()` calls your functions in this order: `update_creatures`, `cull_creatures`, `spawn_creatures` (when the crowd is short), `draw_creatures`, then `sonar_contacts` for the CONTACTS line. You don't need to add any of those calls yourself.
>
> Below `frame()` is a **Checkpoint 6 (carried over)** section with reference versions of last week's three functions, then Checkpoints 5, 4, 3, and 2 the same way. If you did those checkpoints, paste your own versions in over the references.

### 1. `spawn_creatures(sub, count)` - returns a list

Returns `count` new creatures placed around the sub. Each one is a `(x, depth, speed)` tuple:

- `x`: `SPAWN_MIN_DX` to `SPAWN_MAX_DX` meters away from `sub.x`, on a randomly chosen side (left or right). That keeps new creatures off screen.
- `depth`: random, within `SPAWN_DEPTH_SPREAD` meters above or below `sub.depth`, but never shallower than `MIN_CREATURE_DEPTH`.
- `speed`: random, from `-MAX_CREATURE_SPEED` to `MAX_CREATURE_SPEED`.

### 2. `distance_to_creature(sub, creature)` - returns a number

The straight-line distance in meters from the sub to one creature. This is the same Pythagorean idea as `distance_to_base` in Checkpoint 5, except the creature is a tuple. Its speed doesn't matter here.

### 3. `update_creatures(creatures, seconds)` - void

Moves every creature sideways for `seconds` of swimming. Its `x` changes by its speed times `seconds`; its depth and speed stay the same.

You can't change a tuple, so each creature has to be replaced by a new tuple in the same spot in the list. Change the list itself. There's nothing to return.

### 4. `cull_creatures(sub, creatures)` - returns a list

Returns a new list with only the creatures within `CULL_DISTANCE` meters of the sub, in their original order. Call `distance_to_creature` for the distance.

### 5. `sonar_contacts(sub, creatures)` - returns a list

Returns the distance in meters to every creature sonar can hear, nearest first. Sonar hears a creature within `SONAR_RANGE_M` meters at full power, and the range shrinks in proportion to `sub.power` (50% power hears half as far). Return the distances, not the creatures. If nothing is in range, return an empty list.

### 6. `draw_creatures(screen, sub, creatures)` - void

Draws every creature. For each one, convert its world position to a screen position with `engine.world_x_to_screen` and `engine.world_y_to_screen`, then call `engine.draw_creature(screen, (screen_x, screen_y), facing)`. `facing` is `1` for a creature swimming right (speed 0 or more) and `-1` for one swimming left. `engine.draw_creature` skips anything that is off screen for you.

---

## Try it

Run `python main.py`. After the countdown, dive past 100 meters and creatures should drift in from the sides. The CONTACTS line should climb as you drift toward them, and a creature only shows up on screen once it's inside your light (or if you're shallow enough for daylight). Turn the light off with `L` and watch the CONTACTS number stay the same while the creatures vanish.

---

## Done when

`python check.py` prints **22 / 22** (100 points). It checks:

- `spawn_creatures()` returns the right number of `(x, depth, speed)` tuples, with `x`, `depth`, and `speed` inside their ranges, on both sides of the sub, and random
- `distance_to_creature()` gives the straight-line distance in every direction
- `update_creatures()` moves each creature by its speed times the time, in the list itself
- `cull_creatures()` keeps only the creatures inside `CULL_DISTANCE`, even when several far ones are in a row
- `sonar_contacts()` returns sorted distances, shrinks its range with power, and counts depth as well as sideways distance
- `draw_creatures()` draws each creature once at the right screen position, facing the right way

Submit `main.py` to Canvas. `check.py` runs the same checks the grader uses.

---

## Hints

- A list that grows one item at a time starts as `[]` and uses `.append()`.
- `random.uniform(a, b)` gives a random float between `a` and `b`. `random.choice(sequence)` picks one item from a sequence.
- Take a tuple apart with an index (`creature[0]`) or by unpacking (`x, depth, speed = creature`).
- `creature[0] = 5` is an error because tuples can't change. Build a new tuple and store it with `creatures[i] = ...`.
- `for creature in creatures` gives you each item. `for i in range(len(creatures))` gives you each position. You need the second one when you're replacing items.
- Removing items from a list while looping over it skips items. Build a new list of the keepers instead.
- `.sort()` sorts a list in place, and `sorted()` returns a new sorted list.

## If you're stuck / joining late

The carried-over sections at the bottom of `main.py` already have working versions of Checkpoints 2 through 6, so you don't need those files. Do the `SETUP.md` setup if you haven't, then write the six functions here. If you did the earlier checkpoints, swap your own code into those sections.
