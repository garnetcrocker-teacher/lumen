"""
Checkpoint 4 auto-check.   Run:  python check.py

Imports the four functions from main.py and exercises their loops.
No window opens. Paste the final score into Canvas.
"""

import builtins
import contextlib
import io
import os
import sys

os.environ["LUMEN_HEADLESS"] = "1"

TOTAL_CHECKS = 19

results = []


def check(label, passed, detail=""):
    results.append(bool(passed))
    flag = "[PASS]" if passed else "[FAIL]"
    print(f"  {flag} {label}" + ("" if passed or not detail else f"   ({detail})"))


def feed_input(answers):
    """Replace input() with one that returns the given answers in order."""
    it = iter(answers)
    calls = {"n": 0}

    def fake(prompt=""):
        calls["n"] += 1
        return next(it)

    builtins.input = fake
    return calls


def call_valid_depth(student, answers):
    real_input = builtins.input
    calls = feed_input(answers)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            value = student.read_valid_depth()
    finally:
        builtins.input = real_input
    return value, calls["n"]


def _expected_status(depth_m, rated_m):
    """Independent copy of the Checkpoint 3 rule - doesn't rely on the
    student's own (possibly broken) carried-over hull_status()."""
    if depth_m < rated_m:
        return "OK"
    elif depth_m < 1.5 * rated_m:
        return "CAUTION"
    return "BREACH"


_EXPECTED_COLOR = {"OK": (90, 200, 150), "CAUTION": (230, 190, 90), "BREACH": (230, 90, 80)}


def main():
    try:
        import main as student
    except Exception as exc:
        print(f"  [FAIL] could not import main.py: {exc!r}")
        return _report(0, TOTAL_CHECKS)

    needed = ("read_valid_depth", "max_safe_depth", "draw_depth_ticks", "draw_sonar_rings")
    for fn in needed:
        if not hasattr(student, fn):
            print(f"  [FAIL] main.py has no function called {fn}()")
            return _report(0, TOTAL_CHECKS)

    import engine

    # --- read_valid_depth ---------------------------------------------------
    try:
        v, n = call_valid_depth(student, ["-5", "70000", "0", "450"])
        check("read_valid_depth rejects -5, 70000, 0 then returns 450",
              v == 450, f"returned {v!r}")
        check("read_valid_depth returns an int", type(v) is int, f"type {type(v).__name__}")
        check("read_valid_depth asked again after each bad value (4 prompts)",
              n == 4, f"called input() {n} time(s)")
    except Exception as exc:
        for lbl in ("rejects bad values", "returns an int", "re-prompts"):
            check(f"read_valid_depth {lbl}", False, repr(exc))

    try:
        v1, _ = call_valid_depth(student, ["1"])
        v2, _ = call_valid_depth(student, ["6000"])
        check("read_valid_depth accepts the low boundary 1", v1 == 1, f"returned {v1!r}")
        check("read_valid_depth accepts the high boundary 6000", v2 == 6000, f"returned {v2!r}")
        v3, n3 = call_valid_depth(student, ["6001", "500"])
        check("read_valid_depth rejects 6001 then accepts 500",
              v3 == 500 and n3 == 2, f"returned {v3!r} after {n3} prompt(s)")
    except Exception as exc:
        for lbl in ("low boundary", "high boundary", "just over the top"):
            check(f"read_valid_depth {lbl}", False, repr(exc))

    # --- max_safe_depth ------------------------------------------------------
    for arg, expected in [(100, 2000), (50, 1000), (2, 40), (1, 20), (0, 0)]:
        try:
            got = student.max_safe_depth(arg)
            check(f"max_safe_depth({arg}) -> {expected}",
                  got == expected and type(got) is int, f"got {got!r}")
        except Exception as exc:
            check(f"max_safe_depth({arg})", False, repr(exc))

    # --- draw_depth_ticks ------------------------------------------------------
    seen = []
    real_tick = engine.draw_tick
    engine.draw_tick = lambda screen, y, d, color=None: seen.append((d, y, color))
    try:
        sub = engine.Submarine(engine.DEFAULT_DIVEPLAN)   # rated_depth = 1000.0
        sub.depth = 250.0
        student.draw_depth_ticks(None, sub)
    except Exception as exc:
        check("draw_depth_ticks runs without error", False, repr(exc))
    finally:
        engine.draw_tick = real_tick

    depths = [d for d, _, _ in seen]
    expected_depths = list(range(0, 2001, 100))
    check("draw_depth_ticks calls engine.draw_tick for every marker 0..2000",
          depths == expected_depths, f"got {depths}")

    sub_ref = engine.Submarine(engine.DEFAULT_DIVEPLAN)
    sub_ref.depth = 250.0
    y_ok = len(seen) > 0 and all(y == engine.world_y_to_screen(sub_ref, d) for d, y, _ in seen)
    check("draw_depth_ticks converts each depth with engine.world_y_to_screen",
          y_ok, "y values did not match world_y_to_screen(sub, d)")

    expected_colors = [_EXPECTED_COLOR[_expected_status(d, sub_ref.rated_depth)]
                       for d in expected_depths]
    got_colors = [c for _, _, c in seen]
    check("draw_depth_ticks colors each marker by hull_status (OK/CAUTION/BREACH)",
          got_colors == expected_colors,
          f"first few colors: {got_colors[:3]} (did you pass color to draw_tick?)")

    # --- draw_sonar_rings ------------------------------------------------------
    # Independent copy of the expected formula - freezes engine.now() to a known
    # value so the animation is fully deterministic for testing.
    SONAR_RANGE_MAX = 400
    SWEEP_SECONDS = 2.5
    PULSE_COUNT = 4

    def expected_radii(power, t):
        sonar_range = power * (SONAR_RANGE_MAX / 100)
        out = []
        for i in range(PULSE_COUNT):
            offset = i / PULSE_COUNT
            fraction = (t / SWEEP_SECONDS + offset) % 1.0
            out.append(fraction * sonar_range)
        return out

    expected_center = (engine.WIDTH // 2, engine.SUB_SCREEN_Y)
    real_ring = engine.draw_ring
    real_t = engine._state.t

    def rings_for(power, t):
        calls = []
        engine.draw_ring = lambda screen, pos, radius, *a, **kw: calls.append((tuple(pos), radius))
        engine._state.t = t
        try:
            sub2 = engine.Submarine(engine.DEFAULT_DIVEPLAN)
            sub2.power = power
            student.draw_sonar_rings(None, sub2)
        finally:
            engine.draw_ring = real_ring
            engine._state.t = real_t
        return calls

    def radii_match(got, expected):
        return len(got) == len(expected) and all(abs(g - e) < 0.5 for g, e in zip(got, expected))

    try:
        calls0 = rings_for(100, 0.0)
    except Exception as exc:
        check("draw_sonar_rings runs without error", False, repr(exc))
        calls0 = []

    exp0 = expected_radii(100, 0.0)
    got0 = [r for _, r in calls0]
    check(f"draw_sonar_rings at 100% power, t=0s draws radii ~{[round(r) for r in exp0]}",
          radii_match(got0, exp0), f"got {got0}")
    centers_ok = len(calls0) > 0 and all(p == expected_center for p, _ in calls0)
    check("draw_sonar_rings centers every pulse on the sub",
          centers_ok, f"expected center {expected_center}")

    for power, t in [(50, 1.25), (0, 0.6), (100, 2.5)]:
        try:
            exp = expected_radii(power, t)
            got = [r for _, r in rings_for(power, t)]
            check(f"draw_sonar_rings at {power}% power, t={t}s draws radii ~{[round(r) for r in exp]}",
                  radii_match(got, exp), f"got {got}")
        except Exception as exc:
            check(f"draw_sonar_rings at {power}% power, t={t}s", False, repr(exc))

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
