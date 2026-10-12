"""
Checkpoint 7 auto-check.   Run:  python check.py

Imports the six functions from main.py (spawn_creatures, distance_to_creature,
update_creatures, cull_creatures, sonar_contacts, draw_creatures) and exercises
them directly. No window opens. Paste the final score into Canvas.
"""

import os
import sys

os.environ["LUMEN_HEADLESS"] = "1"

TOTAL_CHECKS = 22

results = []


def check(label, passed, detail=""):
    results.append(bool(passed))
    flag = "[PASS]" if passed else "[FAIL]"
    print(f"  {flag} {label}" + ("" if passed or not detail else f"   ({detail})"))


def attempt(label, test):
    """Run one check. test() returns (passed, detail); a crash counts as a fail."""
    try:
        passed, detail = test()
    except Exception as exc:
        check(label, False, repr(exc))
    else:
        check(label, passed, detail)


def close(a, b, tol=1e-6):
    return abs(a - b) <= tol


def main():
    try:
        import main as student
    except Exception as exc:
        print(f"  [FAIL] could not import main.py: {exc!r}")
        return _report(0, TOTAL_CHECKS)

    needed = ("spawn_creatures", "distance_to_creature", "update_creatures",
              "cull_creatures", "sonar_contacts", "draw_creatures")
    for fn in needed:
        if not hasattr(student, fn):
            print(f"  [FAIL] main.py has no function called {fn}()")
            return _report(0, TOTAL_CHECKS)

    import engine

    min_dx = getattr(student, "SPAWN_MIN_DX", 130.0)
    max_dx = getattr(student, "SPAWN_MAX_DX", 240.0)
    spread = getattr(student, "SPAWN_DEPTH_SPREAD", 100.0)
    min_depth = getattr(student, "MIN_CREATURE_DEPTH", 30.0)
    max_speed = getattr(student, "MAX_CREATURE_SPEED", 6.0)
    cull_limit = getattr(student, "CULL_DISTANCE", 300.0)
    sonar_m = getattr(student, "SONAR_RANGE_M", 120.0)

    def make_sub(x=0.0, depth=0.0, power=100.0):
        sub = engine.Submarine(engine.DEFAULT_DIVEPLAN)
        sub.x = x
        sub.depth = depth
        sub.power = power
        return sub

    def spawn(sub, count):
        batch = student.spawn_creatures(sub, count)
        if not isinstance(batch, list) or len(batch) != count:
            raise ValueError(f"expected a list of {count} creatures, got {batch!r}")
        return batch

    # --- spawn_creatures -------------------------------------------------------
    def t_count():
        batch = student.spawn_creatures(make_sub(), 5)
        return isinstance(batch, list) and len(batch) == 5, f"got {batch!r}"
    attempt("spawn_creatures(sub, 5) returns a list of 5 creatures", t_count)

    def t_tuples():
        batch = spawn(make_sub(), 10)
        ok = all(isinstance(c, tuple) and len(c) == 3
                 and all(isinstance(v, (int, float)) for v in c) for c in batch)
        return ok, f"got {batch[:2]!r}"
    attempt("each creature is a tuple of three numbers (x, depth, speed)", t_tuples)

    def t_x_band():
        sub = make_sub(x=250.0, depth=500.0)
        batch = spawn(sub, 60)
        bad = [c for c in batch
               if not (min_dx - 1e-6 <= abs(c[0] - sub.x) <= max_dx + 1e-6)]
        return not bad, f"x should be {min_dx} to {max_dx} from sub.x (250), got {bad[:2]!r}"
    attempt("x is SPAWN_MIN_DX to SPAWN_MAX_DX meters from sub.x", t_x_band)

    def t_both_sides():
        sub = make_sub(x=250.0, depth=500.0)
        batch = spawn(sub, 60)
        left = any(c[0] < sub.x for c in batch)
        right = any(c[0] > sub.x for c in batch)
        return left and right, f"left={left} right={right}"
    attempt("creatures spawn on both the left and the right of the sub", t_both_sides)

    def t_depth_band():
        sub = make_sub(x=0.0, depth=500.0)
        batch = spawn(sub, 60)
        bad = [c for c in batch if not (500.0 - spread - 1e-6 <= c[1] <= 500.0 + spread + 1e-6)]
        return not bad, f"depth should be within {spread} of 500, got {bad[:2]!r}"
    attempt("depth is within SPAWN_DEPTH_SPREAD of the sub (sub at 500 m)", t_depth_band)

    def t_depth_floor():
        sub = make_sub(x=0.0, depth=0.0)
        batch = spawn(sub, 60)
        bad = [c for c in batch if not (min_depth - 1e-6 <= c[1] <= spread + 1e-6)]
        return not bad, f"depth should be {min_depth} to {spread}, got {bad[:2]!r}"
    attempt("depth is never shallower than MIN_CREATURE_DEPTH (sub at the surface)",
            t_depth_floor)

    def t_speed():
        batch = spawn(make_sub(), 60)
        bad = [c for c in batch if abs(c[2]) > max_speed + 1e-6]
        return not bad, f"speed should be within +/-{max_speed}, got {bad[:2]!r}"
    attempt("speed is between -MAX_CREATURE_SPEED and MAX_CREATURE_SPEED", t_speed)

    def t_random():
        batch = spawn(make_sub(x=250.0, depth=500.0), 20)
        return len(set(batch)) > 1, f"all 20 creatures were identical: {batch[0]!r}"
    attempt("spawned creatures are random, not all the same", t_random)

    # --- distance_to_creature ----------------------------------------------------
    def t_distance():
        sub = make_sub(x=100.0, depth=400.0)
        result = student.distance_to_creature(sub, (160.0, 480.0, -4.0))
        return close(result, 100.0, 0.01), f"sideways 60, depth 80 -> 100.0, got {result!r}"
    attempt("distance_to_creature measures straight-line distance (60 across, 80 down -> 100)",
            t_distance)

    def t_distance_neg():
        sub = make_sub(x=100.0, depth=400.0)
        result = student.distance_to_creature(sub, (40.0, 320.0, 2.0))
        return close(result, 100.0, 0.01), f"creature up and to the left, got {result!r}"
    attempt("distance_to_creature works for a creature above and to the left of the sub",
            t_distance_neg)

    # --- update_creatures --------------------------------------------------------
    def t_update():
        creatures = [(0.0, 100.0, 5.0), (50.0, 200.0, -2.0)]
        student.update_creatures(creatures, 0.5)
        expected = [(2.5, 100.0, 5.0), (49.0, 200.0, -2.0)]
        ok = (len(creatures) == 2 and all(
            len(c) == 3 and close(c[0], e[0]) and close(c[1], e[1]) and close(c[2], e[2])
            for c, e in zip(creatures, expected)))
        return ok, f"expected {expected}, got {creatures}"
    attempt("update_creatures moves each creature by speed x seconds (in the list itself)",
            t_update)

    def t_update_neg():
        creatures = [(10.0, 50.0, -4.0)]
        student.update_creatures(creatures, 2.0)
        ok = len(creatures) == 1 and close(creatures[0][0], 2.0) and close(creatures[0][1], 50.0)
        return ok, f"expected x=2.0, depth=50.0, got {creatures}"
    attempt("update_creatures moves a left-swimming creature left and keeps its depth",
            t_update_neg)

    def t_update_twice():
        creatures = [(0.0, 100.0, 3.0)]
        student.update_creatures(creatures, 1.0)
        student.update_creatures(creatures, 1.0)
        ok = len(creatures) == 1 and close(creatures[0][0], 6.0) and close(creatures[0][2], 3.0)
        return ok, f"expected x=6.0, speed=3.0, got {creatures}"
    attempt("update_creatures keeps each creature's speed, so updates add up", t_update_twice)

    # --- cull_creatures ----------------------------------------------------------
    def t_cull_basic():
        sub = make_sub()
        near = (cull_limit - 20.0, 0.0, 1.0)
        far = (cull_limit + 20.0, 0.0, 1.0)
        result = student.cull_creatures(sub, [far, near])
        return result == [near], f"expected {[near]}, got {result!r}"
    attempt("cull_creatures keeps creatures inside CULL_DISTANCE and drops the ones outside",
            t_cull_basic)

    def t_cull_diag():
        sub = make_sub()
        kept = (0.6 * cull_limit, 0.6 * cull_limit, 0.0)
        dropped = (0.8 * cull_limit, 0.8 * cull_limit, 0.0)
        result = student.cull_creatures(sub, [dropped, kept])
        return result == [kept], (f"diagonal gaps use straight-line distance; "
                                  f"expected {[kept]}, got {result!r}")
    attempt("cull_creatures uses straight-line distance, depth included", t_cull_diag)

    def t_cull_runs():
        sub = make_sub()
        far = [(cull_limit + 50.0 + i, 0.0, 1.0) for i in range(4)]
        n1 = (10.0, 0.0, 1.0)
        n2 = (-20.0, 40.0, -1.0)
        result = student.cull_creatures(sub, far[:3] + [n1] + far[3:] + [n2])
        return result == [n1, n2], f"expected {[n1, n2]} in order, got {result!r}"
    attempt("cull_creatures drops every far creature, even several in a row", t_cull_runs)

    # --- sonar_contacts ----------------------------------------------------------
    def t_sonar_full():
        sub = make_sub(power=100.0)
        creatures = [(0.75 * sonar_m, 0.0, 1.0), (1.7 * sonar_m, 0.0, 1.0),
                     (-0.25 * sonar_m, 0.0, 1.0), (0.0, 0.5 * sonar_m, 1.0)]
        result = student.sonar_contacts(sub, creatures)
        expected = [0.25 * sonar_m, 0.5 * sonar_m, 0.75 * sonar_m]
        ok = (isinstance(result, list) and len(result) == 3
              and all(close(r, e, 0.01) for r, e in zip(result, expected)))
        return ok, f"expected {expected}, got {result!r}"
    attempt("sonar_contacts returns the distances in range, nearest first", t_sonar_full)

    def t_sonar_power():
        sub = make_sub(power=50.0)
        creatures = [(0.45 * sonar_m, 0.0, 1.0), (0.75 * sonar_m, 0.0, 1.0),
                     (0.0, -0.25 * sonar_m, 1.0), (0.55 * sonar_m, 0.0, 1.0)]
        result = student.sonar_contacts(sub, creatures)
        expected = [0.25 * sonar_m, 0.45 * sonar_m]
        ok = (isinstance(result, list) and len(result) == 2
              and all(close(r, e, 0.01) for r, e in zip(result, expected)))
        return ok, f"at 50% power, expected {expected}, got {result!r}"
    attempt("sonar_contacts range shrinks with sub.power (50% power hears half as far)",
            t_sonar_power)

    def t_sonar_depth():
        sub = make_sub(power=50.0)
        creatures = [(0.3 * sonar_m, 0.3 * sonar_m, 1.0)]
        result = student.sonar_contacts(sub, creatures)
        expected = [(0.18 ** 0.5) * sonar_m]
        ok = (isinstance(result, list) and len(result) == 1
              and close(result[0], expected[0], 0.01))
        return ok, f"expected {expected}, got {result!r}"
    attempt("sonar_contacts counts depth as well as sideways distance", t_sonar_depth)

    # --- draw_creatures ----------------------------------------------------------
    real_draw = engine.draw_creature

    def run_draw(sub, creatures, screen):
        calls = []
        engine.draw_creature = lambda surface, pos, facing=1: calls.append(
            (surface, tuple(pos), facing))
        try:
            student.draw_creatures(screen, sub, creatures)
        finally:
            engine.draw_creature = real_draw
        return calls

    draw_sub = make_sub(x=100.0, depth=300.0)
    draw_list = [(110.0, 320.0, 3.0), (80.0, 290.0, -1.5), (95.0, 310.0, 0.0)]
    screen_marker = object()

    def t_draw_pos():
        calls = run_draw(draw_sub, draw_list, screen_marker)
        expected = [(engine.world_x_to_screen(draw_sub, x), engine.world_y_to_screen(draw_sub, d))
                    for x, d, s in draw_list]
        got = [c[1] for c in calls]
        return got == expected, f"expected {expected}, got {got}"
    attempt("draw_creatures calls engine.draw_creature once per creature at its screen position",
            t_draw_pos)

    def t_draw_screen():
        calls = run_draw(draw_sub, draw_list, screen_marker)
        return len(calls) > 0 and all(c[0] is screen_marker for c in calls), \
            "pass the screen you were given as the first argument"
    attempt("draw_creatures passes the screen through to engine.draw_creature", t_draw_screen)

    def t_draw_facing():
        calls = run_draw(draw_sub, draw_list, screen_marker)
        got = [c[2] for c in calls]
        return got == [1, -1, 1], f"expected facing [1, -1, 1] (right, left, speed 0), got {got}"
    attempt("draw_creatures faces right for speed 0 or more and left for negative speed",
            t_draw_facing)

    _report(sum(results), len(results))


def _report(score, total):
    points = round(score / total * 100) if total else 0
    print()
    print(f"  SCORE: {score} / {total}      POINTS: {points} / 100")
    if score == total:
        print("  All checks passed. Submit this output to Canvas.")
    else:
        print("  Some checks failed - see the [FAIL] lines above.")


if __name__ == "__main__":
    main()
