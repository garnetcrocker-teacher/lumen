"""
Checkpoint 2 auto-check.   Run:  python check.py

This feeds a known dive plan into your main.py and inspects what it saved and
printed. It does NOT open a window. Paste the final score into Canvas.
"""

import json
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
PLAN = HERE / "diveplan.json"
STDIN = "Marlow\n450\n40\n100\n"

results = []


def check(label, passed):
    results.append(bool(passed))
    print(("  [PASS] " if passed else "  [FAIL] ") + label)


def main():
    if PLAN.exists():
        PLAN.unlink()

    env = dict(os.environ, LUMEN_HEADLESS="1")
    try:
        proc = subprocess.run(
            [sys.executable, str(HERE / "main.py")],
            input=STDIN, capture_output=True, text=True,
            cwd=str(HERE), env=env, timeout=30,
        )
    except subprocess.TimeoutExpired:
        print("  [FAIL] main.py did not finish within 30 seconds "
              "(are you calling input() the right number of times?)")
        _report(0, 9)
        return

    out = proc.stdout or ""
    crashed = proc.returncode != 0
    if crashed:
        print("  --- main.py error output ---")
        print("  " + (proc.stderr or "").strip().replace("\n", "\n  "))
        print("  ---------------------------")

    check("main.py runs without crashing", not crashed)

    data = {}
    try:
        data = json.loads(PLAN.read_text(encoding="utf-8"))
    except Exception:
        pass

    check("diveplan.json was written", isinstance(data, dict) and len(data) > 0)
    check("pilot is saved as the text 'Marlow'", data.get("pilot") == "Marlow")
    check("target_depth is saved as the integer 450 (you used int())",
          data.get("target_depth") == 450
          and isinstance(data.get("target_depth"), int)
          and not isinstance(data.get("target_depth"), bool))
    check("ballast_kg is saved as the float 40.0 (you used float())",
          isinstance(data.get("ballast_kg"), float) and data.get("ballast_kg") == 40.0)
    check("battery_pct is saved as the float 100.0 (you used float())",
          isinstance(data.get("battery_pct"), float) and data.get("battery_pct") == 100.0)
    check("the briefing prints the pilot name", "Marlow" in out)
    check("the briefing prints the target depth", "450" in out)
    check("the briefing prints the descent time 22.5", "22.5" in out)

    _report(sum(results), len(results))


def _report(score, total):
    points = round(score / total * 100) if total else 0
    print()
    print(f"  SCORE: {score} / {total}      POINTS: {points} / 100")
    if score == total:
        print("  All checks passed. Submit this output to Canvas.")
    else:
        print("  Some checks failed - see [FAIL] lines above, fix, and re-run.")


if __name__ == "__main__":
    main()
