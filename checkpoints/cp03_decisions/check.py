"""
Checkpoint 3 auto-check.   Run:  python check.py

Imports your four functions from main.py and calls them with known values.
No window opens. Paste the final score into Canvas.
"""

import os
import sys

os.environ["LUMEN_HEADLESS"] = "1"      # stop main.py from opening a window

TOTAL_CHECKS = 21

results = []


def check(call_text, got, expected):
    ok = got == expected and type(got) is type(expected)
    results.append(ok)
    flag = "[PASS]" if ok else "[FAIL]"
    extra = "" if ok else f"   (got {got!r}, expected {expected!r})"
    print(f"  {flag} {call_text}{extra}")


def check_value(call_text, got, expected):
    """Like check(), but only compares the value, not the type - an int or a
    float answer is equally correct here."""
    ok = got == expected
    results.append(ok)
    flag = "[PASS]" if ok else "[FAIL]"
    extra = "" if ok else f"   (got {got!r}, expected {expected!r})"
    print(f"  {flag} {call_text}{extra}")


def main():
    try:
        import main as student
    except Exception as exc:
        print(f"  [FAIL] could not import main.py: {exc!r}")
        _report(0, TOTAL_CHECKS)
        return

    for fn in ("clamp_battery", "hull_status", "oxygen_state", "can_descend"):
        if not hasattr(student, fn):
            print(f"  [FAIL] main.py has no function called {fn}()")
            _report(0, TOTAL_CHECKS)
            return

    cb = student.clamp_battery
    hs, ox, cd = student.hull_status, student.oxygen_state, student.can_descend

    check_value("clamp_battery(150)", cb(150), 100)
    check_value("clamp_battery(101)", cb(101), 100)
    check_value("clamp_battery(100)", cb(100), 100)
    check_value("clamp_battery(99.5)", cb(99.5), 99.5)
    check_value("clamp_battery(0)", cb(0), 0)

    check("hull_status(500, 1000)", hs(500, 1000), "OK")
    check("hull_status(999, 1000)", hs(999, 1000), "OK")
    check("hull_status(1000, 1000)", hs(1000, 1000), "CAUTION")
    check("hull_status(1499, 1000)", hs(1499, 1000), "CAUTION")
    check("hull_status(1500, 1000)", hs(1500, 1000), "BREACH")
    check("hull_status(4000, 1000)", hs(4000, 1000), "BREACH")

    check("oxygen_state(80)", ox(80), "GOOD")
    check("oxygen_state(51)", ox(51), "GOOD")
    check("oxygen_state(50)", ox(50), "LOW")
    check("oxygen_state(16)", ox(16), "LOW")
    check("oxygen_state(15)", ox(15), "CRITICAL")
    check("oxygen_state(0)", ox(0), "CRITICAL")

    check("can_descend(40, 100)", cd(40, 100), True)
    check("can_descend(0, 100)", cd(0, 100), False)
    check("can_descend(40, 0)", cd(40, 0), False)
    check("can_descend(0, 0)", cd(0, 0), False)

    _report(sum(results), len(results))


def _report(score, total):
    points = round(score / total * 100) if total else 0
    print()
    print(f"  SCORE: {score} / {total}      POINTS: {points} / 100")
    if score == total:
        print("  All checks passed. Submit this output to Canvas.")
    else:
        print("  Some checks failed - check your < vs <= at the boundaries.")


if __name__ == "__main__":
    main()
