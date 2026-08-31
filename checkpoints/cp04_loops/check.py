"""
Checkpoint 4 auto-check.   Run:  python check.py

Imports the three functions from main.py and exercises their loops.
No window opens. Paste the final score into Canvas.
"""

import builtins
import contextlib
import io
import os
import sys

os.environ["LUMEN_HEADLESS"] = "1"

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


def main():
    try:
        import main as student
    except Exception as exc:
        print(f"  [FAIL] could not import main.py: {exc!r}")
        return _report(0, 13)

    for fn in ("read_valid_depth", "max_safe_depth", "draw_depth_ticks"):
        if not hasattr(student, fn):
            print(f"  [FAIL] main.py has no function called {fn}()")
            return _report(0, 13)

    import engine

    # --- read_valid_depth -------------------------------------------------
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

    # --- max_safe_depth -------------------------------------------------
    for arg, expected in [(100, 2000), (50, 1000), (2, 40), (1, 20), (0, 0)]:
        try:
            got = student.max_safe_depth(arg)
            check(f"max_safe_depth({arg}) -> {expected}",
                  got == expected and type(got) is int, f"got {got!r}")
        except Exception as exc:
            check(f"max_safe_depth({arg})", False, repr(exc))

    # --- draw_depth_ticks -------------------------------------------------
    seen = []
    real_tick = engine.draw_tick
    engine.draw_tick = lambda screen, y, d: seen.append((d, y))
    try:
        sub = engine.Submarine(engine.DEFAULT_DIVEPLAN)
        sub.depth = 250.0
        student.draw_depth_ticks(None, sub)
    except Exception as exc:
        check("draw_depth_ticks runs without error", False, repr(exc))
    finally:
        engine.draw_tick = real_tick

    depths = [d for d, _ in seen]
    expected_depths = list(range(0, 2001, 100))
    check("draw_depth_ticks calls engine.draw_tick for every marker 0..2000",
          depths == expected_depths, f"got {depths}")

    sub_ref = engine.Submarine(engine.DEFAULT_DIVEPLAN)
    sub_ref.depth = 250.0
    y_ok = len(seen) > 0 and all(y == engine.world_y_to_screen(sub_ref, d) for d, y in seen)
    check("draw_depth_ticks converts each depth with engine.world_y_to_screen",
          y_ok, "y values did not match world_y_to_screen(sub, d)")

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
