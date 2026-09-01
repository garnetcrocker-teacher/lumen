# LUMEN - one-time setup

You need **Python 3.10 or newer** and the **pygame-ce** library. We install the
library into a *virtual environment* ("venv") - a private box of libraries that
lives in this project folder and can't break anything else on the computer.

You do this **once**. There are two ways: with VS Code (easiest), or in a
terminal.

---

## The easy way: VS Code (recommended)

With this route you set the environment up once and **never activate anything
again** - VS Code uses the venv automatically for the Run button and for every
terminal it opens.

1. Install the **Python** extension from Microsoft (Extensions sidebar, search
   "Python", Install) if you don't already have it.
2. **File > Open Folder** and open the `lumen` project folder.
3. Press `Ctrl+Shift+P`, type **Python: Create Environment**, press Enter, then:
   - choose **Venv**
   - choose a Python 3.10+ interpreter when asked
   - tick **`requirements.txt`** so it installs the libraries too
4. Wait for the notification in the bottom-right to finish. That's it - VS Code
   made a `.venv` folder and installed pygame-ce into it.

From now on:

- The **Run button** (the ▶ triangle, top-right of an open file) runs your code
  with the venv.
- Any terminal you open with **Terminal > New Terminal** is already switched to
  the venv - you'll see `(.venv)` at the start of the prompt. You do **not** type
  an activate command.

To run a checkpoint: open its `main.py` and click ▶, or in the VS Code terminal:

```
cd checkpoints\cp02_io
python main.py
python check.py
```

> Already made a `.venv` some other way? Skip step 3. Instead press
> `Ctrl+Shift+P` > **Python: Select Interpreter** > pick the one whose path
> contains `.venv`.

---

## Reading the briefing files (`.md`)

Every checkpoint has a `briefing.md`. Markdown (`.md`) files are just text with
light formatting - readable in any editor, but nicer when rendered:

- **VS Code** (already installed): open the `.md` file and press `Ctrl+Shift+V`
  (`Cmd+Shift+V` on Mac) for a formatted preview. Or click the little
  *Open Preview to the Side* book icon at the top-right of the editor.
- **No VS Code:** paste the text into a free web viewer - [stackedit.io](https://stackedit.io)
  or [dillinger.io](https://dillinger.io) - or install a free reader like
  [MarkText](https://www.marktext.cc).
- On GitHub, `.md` files render automatically - if a link is shared with you,
  just read it in the browser.

---

## The manual way: a terminal

Use this if you're not using VS Code. The catch: you must **activate the venv
again every time you open a new terminal** (see "Every session" below).

### Windows - PowerShell

```powershell
cd "$HOME\Documents\lumen"        # wherever you unzipped the project

python -m venv .venv              # make the venv (creates a .venv folder)
.\.venv\Scripts\Activate.ps1      # turn it on - prompt now shows (.venv)
python -m pip install -r requirements.txt
```

If step 2 gives a red *"running scripts is disabled on this system"* error,
Windows is blocking the activate script. Run this once, answer `Y`, and try
again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Still blocked (locked-down lab machine)? Don't activate at all - call the venv's
Python directly every time instead:

```powershell
.\.venv\Scripts\python.exe main.py
.\.venv\Scripts\python.exe check.py
```

### Windows - Command Prompt (cmd)

```bat
cd "%USERPROFILE%\Documents\lumen"
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

### macOS / Linux

```bash
cd ~/Documents/lumen
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Every session (manual way only)

Each time you open a new terminal to work, turn the venv on first:

| Shell | Command |
|---|---|
| PowerShell | `.\.venv\Scripts\Activate.ps1` |
| cmd | `.venv\Scripts\activate.bat` |
| macOS / Linux | `source .venv/bin/activate` |

You should see `(.venv)` in the prompt. Then `cd` into the checkpoint folder and
run `python main.py` / `python check.py`. When you're done, `deactivate` or just
close the terminal.

---

## Check it worked

With the venv active (or via the VS Code Run button), run:

```
python -c "import pygame; print('pygame', pygame.version.ver, 'OK')"
```

You should see something like `pygame 2.5.8 OK`. A short pygame line above it is
normal.

If you see `ModuleNotFoundError: No module named 'pygame'`, the libraries didn't
install into the environment you're using - see the table below.

---

## Common problems

| What you see | What it means | Fix |
|---|---|---|
| `python` is not recognized | Python isn't on PATH | Reinstall Python from python.org, tick **"Add python.exe to PATH"** |
| `(.venv)` never appears in the terminal | activation didn't run | Re-run the activate line for your shell; on PowerShell see the ExecutionPolicy note above. Or use VS Code, which does it for you. |
| `ModuleNotFoundError: pygame` | you're running a Python that isn't the venv | VS Code: `Ctrl+Shift+P` > *Python: Select Interpreter* > pick `.venv`. Terminal: activate the venv, then re-run `python -m pip install -r requirements.txt` |
| pip tries to "build wheel" then fails | your Python is too new/old for this pygame-ce | Use Python 3.10-3.13, or ask the instructor for an updated `requirements.txt` |
| window opens then closes instantly | that was `check.py` or headless mode | run `python main.py` instead; press ESC to close the game window |
| `.venv` folder got huge / synced to OneDrive | it's ~60 MB of libraries | it's fine to delete `.venv` and rebuild it any time |
