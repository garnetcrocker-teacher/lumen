"""
Checkpoint 6 auto-check.   Run:  python check.py

Imports the two functions from main.py (save_dive_log, load_best_depth) and
exercises them directly against a dedicated test file (never your real
dive_log.csv). No window opens. Paste the final score into Canvas.
"""

import os
import sys

os.environ["LUMEN_HEADLESS"] = "1"

TOTAL_CHECKS = 10

TEST_LOG = "test_dive_log.csv"

results = []


def check(label, passed, detail=""):
    results.append(bool(passed))
    flag = "[PASS]" if passed else "[FAIL]"
    print(f"  {flag} {label}" + ("" if passed or not detail else f"   ({detail})"))


def _reset():
    if os.path.exists(TEST_LOG):
        os.remove(TEST_LOG)


def _lines():
    with open(TEST_LOG, "r") as f:
        return [line.strip() for line in f.readlines()]


def main():
    try:
        import main as student
    except Exception as exc:
        print(f"  [FAIL] could not import main.py: {exc!r}")
        return _report(0, TOTAL_CHECKS)

    needed = ("save_dive_log", "load_best_depth")
    for fn in needed:
        if not hasattr(student, fn):
            print(f"  [FAIL] main.py has no function called {fn}()")
            return _report(0, TOTAL_CHECKS)

    # --- load_best_depth on a missing file --------------------------------------
    _reset()
    try:
        result = student.load_best_depth(TEST_LOG)
        check("load_best_depth() on a missing file returns 0.0 (no crash)",
              result == 0.0, f"got {result!r}")
    except Exception as exc:
        check("load_best_depth() on a missing file returns 0.0 (no crash)",
              False, repr(exc))

    try:
        result = student.load_best_depth(TEST_LOG)
        check("load_best_depth() on a missing file returns a float, not an int/str",
              isinstance(result, float), f"got {type(result).__name__} {result!r}")
    except Exception as exc:
        check("load_best_depth() on a missing file returns a float", False, repr(exc))

    # --- save_dive_log: first call creates the file with a header --------------
    _reset()
    try:
        student.save_dive_log("Nova", 340.0, True, TEST_LOG)
        check("save_dive_log() creates the log file if it doesn't exist",
              os.path.exists(TEST_LOG), "file was not created")
    except Exception as exc:
        check("save_dive_log() creates the log file if it doesn't exist", False, repr(exc))

    try:
        lines = _lines()
        check("save_dive_log() writes the header line first",
              lines[0] == "pilot,depth,outcome", f"got {lines[0]!r}" if lines else "file is empty")
    except Exception as exc:
        check("save_dive_log() writes the header line first", False, repr(exc))

    try:
        lines = _lines()
        check("after one save_dive_log() call, the file has exactly 2 lines (header + 1 row)",
              len(lines) == 2, f"got {len(lines)} lines: {lines}")
    except Exception as exc:
        check("after one save_dive_log() call, the file has exactly 2 lines", False, repr(exc))

    try:
        lines = _lines()
        row = lines[1].split(",")
        check("the saved row records the pilot's name and \"SURVIVED\" when alive is True",
              row[0] == "Nova" and row[2] == "SURVIVED", f"got {lines[1]!r}")
    except Exception as exc:
        check("the saved row records the pilot's name and outcome correctly", False, repr(exc))

    # --- save_dive_log: second call appends, doesn't duplicate the header ------
    try:
        student.save_dive_log("Rook", 90.0, False, TEST_LOG)
        lines = _lines()
        check("a second save_dive_log() call appends a row without rewriting the header "
              "(3 lines total: header + 2 rows)",
              len(lines) == 3 and lines.count("pilot,depth,outcome") == 1,
              f"got {len(lines)} lines: {lines}")
    except Exception as exc:
        check("a second save_dive_log() call appends without duplicating the header",
              False, repr(exc))

    try:
        lines = _lines()
        row = lines[2].split(",")
        check("the second row records \"LOST\" when alive is False",
              row[2] == "LOST", f"got {lines[2]!r}")
    except Exception as exc:
        check("the second row records \"LOST\" when alive is False", False, repr(exc))

    # --- load_best_depth: the maximum, not the first or last logged dive -------
    _reset()
    try:
        student.save_dive_log("A", 100.0, True, TEST_LOG)
        student.save_dive_log("B", 500.0, False, TEST_LOG)
        student.save_dive_log("C", 250.0, True, TEST_LOG)
        result = student.load_best_depth(TEST_LOG)
        check("load_best_depth() returns the deepest of several logged dives (500.0), "
              "not just the first or last",
              result == 500.0, f"got {result!r}")
    except Exception as exc:
        check("load_best_depth() returns the deepest of several logged dives", False, repr(exc))

    try:
        result = student.load_best_depth(TEST_LOG)
        check("load_best_depth() still returns a float once the file has real rows in it",
              isinstance(result, float), f"got {type(result).__name__} {result!r}")
    except Exception as exc:
        check("load_best_depth() still returns a float once the file has real rows",
              False, repr(exc))

    _reset()
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
