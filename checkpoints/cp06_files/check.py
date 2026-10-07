"""
Checkpoint 6 auto-check.   Run:  python check.py

Imports the three functions from main.py (save_dive_log, load_dive_stats,
save_best_dive) and exercises them directly against dedicated test files
(never your real dive_log.csv or best_dive.txt). No window opens. Paste the
final score into Canvas.
"""

import os
import sys

os.environ["LUMEN_HEADLESS"] = "1"

TOTAL_CHECKS = 19

TEST_LOG = "test_dive_log.csv"
TEST_BEST = "test_best_dive.txt"

results = []


def check(label, passed, detail=""):
    results.append(bool(passed))
    flag = "[PASS]" if passed else "[FAIL]"
    print(f"  {flag} {label}" + ("" if passed or not detail else f"   ({detail})"))


def _reset():
    for path in (TEST_LOG, TEST_BEST):
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

    needed = ("save_dive_log", "load_dive_stats", "save_best_dive")
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
    except Exception:
        pass

    try:
        count, average, minimum, maximum = student.load_dive_stats(TEST_LOG)
        check("load_dive_stats() counts all three logged dives",
              count == 3, f"got count={count!r}")
    except Exception as exc:
        check("load_dive_stats() counts all three logged dives", False, repr(exc))

    try:
        count, average, minimum, maximum = student.load_dive_stats(TEST_LOG)
        check("load_dive_stats() computes the correct average depth (283.33...)",
              abs(average - (100.0 + 500.0 + 250.0) / 3) < 0.01, f"got average={average!r}")
    except Exception as exc:
        check("load_dive_stats() computes the correct average depth (283.33...)",
              False, repr(exc))

    try:
        count, average, minimum, maximum = student.load_dive_stats(TEST_LOG)
        check("load_dive_stats() finds the correct minimum depth (100.0)",
              abs(minimum - 100.0) < 0.01, f"got minimum={minimum!r}")
    except Exception as exc:
        check("load_dive_stats() finds the correct minimum depth (100.0)", False, repr(exc))

    try:
        count, average, minimum, maximum = student.load_dive_stats(TEST_LOG)
        check("load_dive_stats() finds the correct maximum depth (500.0), "
              "not just the first or last row",
              abs(maximum - 500.0) < 0.01, f"got maximum={maximum!r}")
    except Exception as exc:
        check("load_dive_stats() finds the correct maximum depth (500.0), "
              "not just the first or last row", False, repr(exc))

    # --- load_dive_stats: skips a corrupted row instead of crashing ------------
    _reset()
    with open(TEST_LOG, "w") as f:
        f.write("pilot,depth,outcome\n")
        f.write("A,100.0,SURVIVED\n")
        f.write("Ghost,not_a_number,LOST\n")
        f.write("B,300.0,SURVIVED\n")

    try:
        count, average, minimum, maximum = student.load_dive_stats(TEST_LOG)
        check("load_dive_stats() does not crash on a row with a bad depth field",
              True)
    except Exception as exc:
        check("load_dive_stats() does not crash on a row with a bad depth field",
              False, repr(exc))

    try:
        count, average, minimum, maximum = student.load_dive_stats(TEST_LOG)
        check("load_dive_stats() skips the corrupted row, counting only the 2 valid dives",
              count == 2 and abs(average - 200.0) < 0.01 and abs(minimum - 100.0) < 0.01
              and abs(maximum - 300.0) < 0.01,
              f"got count={count!r}, average={average!r}, minimum={minimum!r}, maximum={maximum!r}")
    except Exception as exc:
        check("load_dive_stats() skips the corrupted row, counting only the 2 valid dives",
              False, repr(exc))

    # --- save_best_dive: first survived dive becomes the record ----------------
    _reset()
    try:
        student.save_best_dive("Nova", 300.0, True, TEST_BEST)
        check("save_best_dive() creates the record file on the first survived dive",
              os.path.exists(TEST_BEST), "file was not created")
    except Exception as exc:
        check("save_best_dive() creates the record file on the first survived dive",
              False, repr(exc))

    try:
        lines = _lines(TEST_BEST)
        check("the record file holds exactly 2 lines (Pilot/Depth)",
              len(lines) == 2, f"got {len(lines)} lines: {lines}")
    except Exception as exc:
        check("the record file holds exactly 2 lines (Pilot/Depth)", False, repr(exc))

    try:
        lines = _lines(TEST_BEST)
        check("the record correctly names the pilot and depth",
              lines[0] == "Pilot: Nova" and lines[1] == "Depth: 300.0 m",
              f"got {lines!r}")
    except Exception as exc:
        check("the record correctly names the pilot and depth", False, repr(exc))

    # --- save_best_dive: a shallower survived dive does NOT beat the record ----
    try:
        student.save_best_dive("Rook", 200.0, True, TEST_BEST)
        lines = _lines(TEST_BEST)
        check("a shallower survived dive does not overwrite the record "
              "(still Nova at 300.0 m)",
              lines[0] == "Pilot: Nova" and lines[1] == "Depth: 300.0 m",
              f"got {lines!r}")
    except Exception as exc:
        check("a shallower survived dive does not overwrite the record", False, repr(exc))

    # --- save_best_dive: a deeper dive that did NOT survive doesn't count ------
    try:
        student.save_best_dive("Ghost", 900.0, False, TEST_BEST)
        lines = _lines(TEST_BEST)
        check("a deeper dive that did not survive does not overwrite the record "
              "(still Nova at 300.0 m)",
              lines[0] == "Pilot: Nova" and lines[1] == "Depth: 300.0 m",
              f"got {lines!r}")
    except Exception as exc:
        check("a deeper dive that did not survive does not overwrite the record",
              False, repr(exc))

    # --- save_best_dive: a deeper survived dive DOES beat the record -----------
    try:
        student.save_best_dive("Zed", 500.0, True, TEST_BEST)
        lines = _lines(TEST_BEST)
        check("a deeper survived dive overwrites the record with the new pilot and depth",
              lines[0] == "Pilot: Zed" and lines[1] == "Depth: 500.0 m",
              f"got {lines!r}")
    except Exception as exc:
        check("a deeper survived dive overwrites the record", False, repr(exc))

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
