# LUMEN - one-time setup

You need **Python 3.10 or newer** and the **pygame-ce** library. We install the
library into a *virtual environment* ("venv") - a private box of libraries that
lives in this project folder and can't break anything else on the computer.

Do this once. It takes about two minutes.

---

## Windows - PowerShell (the blue terminal, and the one in VS Code)

```powershell
# 1. Go into the project folder (change the path to wherever you unzipped it)
cd "$HOME\Documents\lumen"

# 2. Create the venv (this makes a .venv folder)
python -m venv .venv

# 3. Turn it on
.\.venv\Scripts\Activate.ps1

# 4. Install the libraries
python -m pip install -r requirements.txt
```

After step 3 your prompt shows `(.venv)` at the start of the line. That means the
venv is on.

### If step 3 gives a red "running scripts is disabled on this system" error

Windows is blocking the activate script. Run this one line, answer `Y`, then try
step 3 again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Still blocked (locked-down lab machine)? Skip activation entirely and call the
venv's Python directly every time:

```powershell
.\.venv\Scripts\python.exe main.py
.\.venv\Scripts\python.exe check.py
```

---

## Windows - Command Prompt (cmd)

```bat
cd "%USERPROFILE%\Documents\lumen"
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

---

## macOS / Linux

```bash
cd ~/Documents/lumen
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

---

## Every time you sit down to work

1. Open a terminal in the project folder.
2. Turn the venv on:
   - PowerShell: `.\.venv\Scripts\Activate.ps1`
   - cmd: `.venv\Scripts\activate.bat`
   - macOS/Linux: `source .venv/bin/activate`
3. You should see `(.venv)` in the prompt. Now run your checkpoint:
   ```
   cd checkpoints\cp02_io
   python main.py
   python check.py
   ```
4. When you're done, `deactivate` (or just close the terminal).

---

## Using VS Code

1. Open the `lumen` folder in VS Code (`File > Open Folder`).
2. Press `Ctrl+Shift+P`, type **Python: Select Interpreter**, and pick the one
   that says `.venv` (it will end in `.venv\Scripts\python.exe`).
3. Now the "Run" button (the triangle, top right) and any new terminal
   (`Terminal > New Terminal`) use the venv automatically.

---

## Check it worked

With the venv on, run:

```
python -c "import pygame; print('pygame', pygame.version.ver, 'OK')"
```

You should see something like `pygame 2.5.8 OK`. A small pygame banner line above
it is normal.

If you see `ModuleNotFoundError: No module named 'pygame'`, the venv is not on, or
step 4 didn't finish - turn the venv on and re-run
`python -m pip install -r requirements.txt`.

---

## Common problems

| What you see | What it means | Fix |
|---|---|---|
| `python` is not recognized | Python isn't on PATH | Reinstall Python from python.org, tick **"Add python.exe to PATH"** |
| `(.venv)` never appears | activation didn't run | Re-run the activate line for your shell; on PowerShell see the ExecutionPolicy note above |
| `ModuleNotFoundError: pygame` | wrong Python / venv off | Turn the venv on; confirm VS Code interpreter is `.venv` |
| pip tries to "build wheel" then fails | your Python is too new/old for this pygame-ce | Use Python 3.10-3.13, or ask the instructor for an updated `requirements.txt` |
| window opens then closes instantly | that's `check.py` or headless mode | run `python main.py` instead; press ESC to close the game window |
| `.venv` folder got huge / synced to OneDrive | it's ~60 MB of libraries | it's fine to delete `.venv` and rebuild it any time; never commit it |
