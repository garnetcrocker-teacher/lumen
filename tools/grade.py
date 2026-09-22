"""
Batch-grade a folder of student submissions for one checkpoint.

For each student's .py file, copies it in as main.py next to a FRESH copy
of that checkpoint's check.py and engine.py (so grading always uses the
current, canonical checker - never a possibly-stale copy sitting in the
submissions folder), runs check.py as a subprocess, and collects the score.
Each run happens in its own temp directory, so one student's main.py can
never leak into another's run.

Usage:
    python tools/grade.py cp02_io path/to/downloaded/submissions

The submissions folder can hold any mix of .py files, named however Canvas
or you named them (main_gerald.py, Doe_Jane_late_12345_main.py, whatever) -
anything that isn't literally main.py, check.py, or engine.py is treated as
one student's submission.

Writes, inside the submissions folder:
    grades.csv        one row per student: name, file, status, score, points
    logs/<name>.txt   that student's full check.py output, for FAIL detail

Never touches anything outside a temp dir and the submissions folder itself.
"""

import csv
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TIMEOUT_SECONDS = 15
SCORE_RE = re.compile(r"SCORE:\s*(\d+)\s*/\s*(\d+)\s*POINTS:\s*(\d+)\s*/\s*100")
SKIP_NAMES = {"main.py", "check.py", "engine.py"}


def student_label(path):
    name = path.stem
    for prefix in ("main_", "main-"):
        if name.startswith(prefix):
            name = name[len(prefix):]
            break
    name = name.replace("_", " ").replace("-", " ").strip()
    return name or path.stem


def grade_one(checkpoint_dir, submission_path):
    with tempfile.TemporaryDirectory(prefix="lumen_grade_") as tmp:
        tmp = pathlib.Path(tmp)
        shutil.copy(checkpoint_dir / "check.py", tmp / "check.py")
        shutil.copy(checkpoint_dir / "engine.py", tmp / "engine.py")
        shutil.copy(submission_path, tmp / "main.py")

        try:
            result = subprocess.run(
                [sys.executable, "check.py"],
                cwd=tmp,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                stdin=subprocess.DEVNULL,
            )
            output = result.stdout + result.stderr
        except subprocess.TimeoutExpired as exc:
            output = (exc.stdout or "") + (exc.stderr or "")
            output += f"\n\n[grade.py] Timed out after {TIMEOUT_SECONDS}s - killed."
            return {"status": "TIMEOUT", "score": "", "total": "", "points": "0", "output": output}

        match = SCORE_RE.search(output)
        if match:
            score, total, points = match.groups()
            return {"status": "OK", "score": score, "total": total, "points": points, "output": output}
        return {"status": "ERROR", "score": "", "total": "", "points": "0", "output": output}


def main():
    if len(sys.argv) != 3:
        print("Usage: python tools/grade.py <checkpoint_folder_name> <submissions_folder>")
        print("Example: python tools/grade.py cp02_io Student_Grading/cp02_io")
        sys.exit(1)

    checkpoint_dir = ROOT / "checkpoints" / sys.argv[1]
    if not (checkpoint_dir / "check.py").exists():
        raise SystemExit(f"No check.py found at {checkpoint_dir}")

    submissions_dir = pathlib.Path(sys.argv[2])
    if not submissions_dir.is_dir():
        raise SystemExit(f"No submissions folder at {submissions_dir}")

    submissions = sorted(p for p in submissions_dir.glob("*.py") if p.name not in SKIP_NAMES)
    if not submissions:
        raise SystemExit(
            f"No student .py files found in {submissions_dir} "
            f"(looked for *.py, excluding main.py/check.py/engine.py)"
        )

    logs_dir = submissions_dir / "logs"
    logs_dir.mkdir(exist_ok=True)

    rows = []
    print(f"Grading {len(submissions)} submission(s) against "
          f"{checkpoint_dir.relative_to(ROOT)}/check.py ...\n")
    for path in submissions:
        label = student_label(path)
        result = grade_one(checkpoint_dir, path)
        rows.append({
            "student": label, "file": path.name,
            "status": result["status"], "score": result["score"],
            "total": result["total"], "points": result["points"],
        })
        (logs_dir / f"{label}.txt").write_text(result["output"], encoding="utf-8")

        if result["status"] == "OK":
            print(f"  {label:20s}  {result['score']}/{result['total']}  ({result['points']}/100)")
        else:
            print(f"  {label:20s}  {result['status']}")

    csv_path = submissions_dir / "grades.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["student", "file", "status", "score", "total", "points"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {csv_path}")
    print(f"Full check.py output for each student is in {logs_dir}/<name>.txt")


if __name__ == "__main__":
    main()
