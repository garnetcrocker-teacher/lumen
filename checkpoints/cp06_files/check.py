"""
Checkpoint 6 auto-check.   Run:  python check.py

Imports the three functions from main.py (save_dive_log, load_dive_stats,
save_last_summary) and exercises them directly against dedicated test files
(never your real dive_log.csv or last_dive.txt). No window opens. Paste the
final score into Canvas.
"""

import os
import sys

os.environ["LUMEN_HEADLESS"] = "1"

TOTAL_CHECKS = 15

TEST_LOG = "test_dive_log.csv"
TEST_SUMMARY = "test_last_dive.txt"

results = []


def check(label, passed, detail=""):
    results.append(bool(passed))
    flag = "[PASS]" if passed else "[FAIL]"
    print(f"  {flag} {label}" + ("" if passed or not detail else f"   ({detail})"))


def _reset():
    for path in (TEST_LOG, TEST_SUMMARY):
        if os.path.exists(path):
            os.remove(path)


def _lines(path):
    with open(path, "r") as f:
        return [line.strip() for line in f.readlines()]


def main():
    try:
        import main as student
    except Exception as exc:
        print(f"  [FAIL] could not import main.py: {exc!r}")
        return _report(0, TOTAL_CHECKS)

    needed = ("save_dive_log", "load_dive_stats", "save_last_summary")
    for fn in needed:
        if not hasattr(student, fn):
            print(f"  [FAIL] main.py has no function called {fn}()")
            return _report(0, TOTAL_CHECKS)

    # --- load_dive_stats on a missing file --------------------------------------
    _reset()
    try:
        result = student.load_dive_stats(TEST_LOG)
        check("load_dive_stats() on a missing file returns (0, 0.0, 0.0, 0.0)",
              tuple(result) == (0, 0.0, 0.0, 0.0), f"got {result!r}")
    except Exception as exc:
        check("load_dive_stats() on a missing file returns (0, 0.0, 0.0, 0.0)",
              False, repr(exc))

    # --- save_dive_log: first call creates the file with a header --------------
    _reset()
    try:
        student.save_dive_log("Nova", 340.0, True, TEST_LOG)
        check("save_dive_log() creates the log file if it doesn't exist",
              os.path.exists(TEST_LOG), "file was not created")
    except Exception as exc:
        check("save_dive_log() creates the log file if it doesn't exist", False, repr(exc))

    try:
        lines = _lines(TEST_LOG)
        check("save_dive_log() writes the header line first",
              lines[0] == "pilot,depth,outcome", f"got {lines[0]!r}" if lines else "file is empty")
    except Exception as exc:
        check("save_dive_log() writes the header line first", False, repr(exc))

    try:
        lines = _lines(TEST_LOG)
        check("after one save_dive_log() call, the file has exactly 2 lines (header + 1 row)",
              len(lines) == 2, f"got {len(lines)} lines: {lines}")
    except Exception as exc:
        check("after one save_dive_log() call, the file has exactly 2 lines", False, repr(exc))

    try:
        lines = _lines(TEST_LOG)
        row = lines[1].split(",")
        check("the saved row records the pilot's name and \"SURVIVED\" when alive is True",
              row[0] == "Nova" and row[2] == "SURVIVED", f"got {lines[1]!r}")
    except Exception as exc:
        check("the saved row records the pilot's name and outcome correctly", False, repr(exc))

    # --- save_dive_log: second call appends, doesn't duplicate the header ------
    try:
        student.save_dive_log("Rook", 90.0, False, TEST_LOG)
        lines = _lines(TEST_LOG)
        check("a second save_dive_log() call appends a row without rewriting the header "
              "(3 lines total: header + 2 rows)",
              len(lines) == 3 and lines.count("pilot,depth,outcome") == 1,
              f"got {len(lines)} lines: {lines}")
    except Exception as exc:
        check("a second save_dive_log() call appends without duplicating the header",
              False, repr(exc))

    try:
        lines = _lines(TEST_LOG)
        row = lines[2].split(",")
        check("the second row records \"LOST\" when alive is False",
              row[2] == "LOST", f"got {lines[2]!r}")
    except Exception as exc:
        check("the second row records \"LOST\" when alive is False", False, repr(exc))

    # --- load_dive_stats: count/average/min/max over several dives -------------
    _reset()
    try:
        student.save_dive_log("A", 100.0, True, TEST_LOG)
        student.save_dive_log("B", 500.0, False, TEST_LOG)
        student.save_dive_log("C", 250.0, True, TEST_LOG)
        count, average, minimum, maximum = student.load_dive_stats(TEST_LOG)
        check("load_dive_stats() counts all three logged dives",
              count == 3, f"got count={count!r}")
        check("load_dive_stats() computes the correct average depth (283.33...)",
              abs(average - (100.0 + 500.0 + 250.0) / 3) < 0.01, f"got average={average!r}")
        check("load_dive_stats() finds the correct minimum depth (100.0)",
              abs(minimum - 100.0) < 0.01, f"got minimum={minimum!r}")
        check("load_dive_stats() finds the correct maximum depth (500.0), "
              "not just the first or last row",
              abs(maximum - 500.0) < 0.01, f"got maximum={maximum!r}")
    except Exception as exc:
        check("load_dive_stats() computes count/average/min/max correctly", False, repr(exc))

    # --- save_last_summary: overwrites instead of appending --------------------
    _reset()
    try:
        student.save_last_summary("Nova", 340.0, True, TEST_SUMMARY)
    except Exception:
        pass

    try:
        lines = _lines(TEST_SUMMARY)
        check("save_last_summary() writes exactly 3 lines (Pilot/Depth/Outcome)",
              len(lines) == 3, f"got {len(lines)} lines: {lines}")
    except Exception as exc:
        check("save_last_summary() writes exactly 3 lines (Pilot/Depth/Outcome)", False, repr(exc))

    try:
        lines = _lines(TEST_SUMMARY)
        check("save_last_summary() records the pilot's name",
              lines[0] == "Pilot: Nova", f"got {lines[0]!r}")
    except Exception as exc:
        check("save_last_summary() records the pilot's name", False, repr(exc))

    try:
        lines = _lines(TEST_SUMMARY)
        check("save_last_summary() records \"SURVIVED\" when alive is True",
              lines[2] == "Outcome: SURVIVED", f"got {lines[2]!r}")
    except Exception as exc:
        check("save_last_summary() records \"SURVIVED\" when alive is True", False, repr(exc))

    try:
        student.save_last_summary("Rook", 90.0, False, TEST_SUMMARY)
        lines = _lines(TEST_SUMMARY)
        check("a second save_last_summary() call replaces the file instead of appending "
              "(still 3 lines, showing the new dive only)",
              len(lines) == 3 and lines[0] == "Pilot: Rook" and lines[2] == "Outcome: LOST",
              f"got {len(lines)} lines: {lines}")
    except Exception as exc:
        check("a second save_last_summary() call replaces the file instead of appending",
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
