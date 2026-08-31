"""
Copy the canonical engine.py (repo root) into every checkpoints/cpNN/ folder.

Run this whenever you edit engine.py:

    python tools/sync_engine.py

Each checkpoint folder ships to students as a self-contained zip, so each needs
its own copy of engine.py. This keeps them identical to the root one.
"""

import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "engine.py"


def engine_version(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("ENGINE_VERSION"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return "?"


def main():
    checkpoints = sorted((ROOT / "checkpoints").glob("cp*"))
    if not SRC.exists():
        raise SystemExit(f"no engine.py at {SRC}")
    for folder in checkpoints:
        if folder.is_dir():
            shutil.copy2(SRC, folder / "engine.py")
            print(f"  updated {folder.name}/engine.py")
    print(f"\nsynced engine {engine_version(SRC)} to {len(checkpoints)} checkpoint(s)")


if __name__ == "__main__":
    main()
