# Checkpoint 3 - Hull, Air, and the Decision to Dive

**Module 3: Decision Structures and Boolean Logic**
**Concepts:** `if` / `elif` / `else`, comparison operators, `and` / `or` / `not`, returning a value

---

## The story so far

The submarine now reads the dive plan you built in Checkpoint 2 and actually
descends. But the deep is dangerous: too deep and the hull fails, the air runs
down the whole time, and you should not be able to dive when you're out of
ballast or power. The engine tracks all those numbers - it just needs **you** to
make the judgement calls.

---

## What to do

Open `main.py`. Fill in the bodies of the three functions between
`BEGIN YOUR CODE` and `END YOUR CODE`. Don't change the `def` lines.

### 1. `hull_status(depth_m, rated_m)`

| Condition | Return |
|---|---|
| `depth_m` less than `rated_m` | `"OK"` |
| `depth_m` at least `rated_m`, but less than `1.5 * rated_m` | `"CAUTION"` |
| `depth_m` at least `1.5 * rated_m` | `"BREACH"` |

### 2. `oxygen_state(oxygen_pct)`

| Condition | Return |
|---|---|
| greater than 50 | `"GOOD"` |
| greater than 15, up to and including 50 | `"LOW"` |
| 15 or less | `"CRITICAL"` |

### 3. `can_descend(ballast_kg, power_pct)`

Return `True` only when **both** `ballast_kg > 0` **and** `power_pct > 0`.
Otherwise return `False`. Use the `and` keyword.

---

## Try it

Run `python main.py`. Hold **DOWN** to dive. Watch the `HULL:` readout at the top
center change from `OK` to `CAUTION` to `BREACH` as you pass 1000 m and 1500 m.
Let the battery run down (or watch over time) and confirm that once `PWR` hits 0
you can no longer descend.

---

## Done when

`python check.py` prints **16 / 16** (100 points). It imports your three
functions and calls them with these values:

```
hull_status(500, 1000)   -> "OK"          oxygen_state(80) -> "GOOD"
hull_status(999, 1000)   -> "OK"          oxygen_state(51) -> "GOOD"
hull_status(1000, 1000)  -> "CAUTION"     oxygen_state(50) -> "LOW"
hull_status(1499, 1000)  -> "CAUTION"     oxygen_state(16) -> "LOW"
hull_status(1500, 1000)  -> "BREACH"      oxygen_state(15) -> "CRITICAL"
hull_status(4000, 1000)  -> "BREACH"      oxygen_state(0)  -> "CRITICAL"

can_descend(40, 100) -> True     can_descend(0, 100) -> False
can_descend(40, 0)   -> False    can_descend(0, 0)   -> False
```

Paste the check.py output into the Canvas submission.

---

## Hints

- The boundary cases (`1000, 1000` and `oxygen 50`) are where most points are
  lost. Decide whether each comparison is `<` or `<=` and test it.
- `elif` handles "the previous condition was false, now check this one".
- The last function needs no `if` at all - `return ballast_kg > 0 and power_pct > 0`
  is a complete answer once you understand why.
- Return the string, don't `print()` it. The game and the checker both need the
  returned value.

## If you're stuck / joining late

This checkpoint's `main.py` already contains a correct Checkpoint 2. You do **not**
need your own Checkpoint 2 files. Do the `SETUP.md` venv steps if you haven't,
then edit only the three function bodies here.
