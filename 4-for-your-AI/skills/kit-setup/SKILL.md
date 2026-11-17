---
name: kit-setup
description: Set up, check or repair the RoboMaster Research Kit on this computer - Python environment, transcription and video tools, and a live check of the RoboMaster sources. Use when the kit is new (no .venv folder), when the member says "set up the research kit", or when any kit tool fails to start.
---

# Set up the RoboMaster Research Kit

Setup takes about 10 minutes and roughly 1 GB of disk: Python packages, plus a 0.5 GB speech model that downloads the first time a video is transcribed. Run everything from the kit folder, the one containing `AGENTS.md`. Tell the member what you are doing at each step; ask before installing anything system-wide (steps 1 and 4).

## 0. Check where the kit is (Windows)

Windows limits file paths to 260 characters, and the speech engine's files sit deep inside `4-for-your-AI\.venv\`. If the kit folder's own path is longer than about 100 characters (for example `Downloads\rm-research-kit-main\rm-research-kit-main`), ask the member to move it somewhere short, such as `C:\rm-kit`, **before** step 2. Otherwise transcription fails later with "The filename or extension is too long".

## 1. Find a suitable Python (3.10 to 3.13)

Try `python --version`, `python3 --version`, and on Windows `py -3.12 --version`. Use the first that reports 3.10, 3.11, 3.12 or 3.13; 3.11 and 3.12 are the most tested. On Windows, a `python` that opens the Microsoft Store is not a real install: use `py` instead.

If none qualifies, ask the member before installing one:
- **Windows:** `winget install Python.Python.3.12`
- **macOS:** `brew install python@3.12`
- **Linux:** the distribution's `python3.12` and `python3.12-venv` packages

Python 3.14 may lack the speech-model packages; use 3.12.

## 2. Create the kit's own environment

```bash
# Windows (PowerShell)
py -3.12 -m venv 4-for-your-AI\.venv            # or: python -m venv 4-for-your-AI\.venv
4-for-your-AI\.venv\Scripts\python.exe -m pip install --upgrade pip
4-for-your-AI\.venv\Scripts\python.exe -m pip install -r 4-for-your-AI/requirements.txt

# macOS / Linux
python3 -m venv 4-for-your-AI/.venv
4-for-your-AI/.venv/bin/python -m pip install --upgrade pip
4-for-your-AI/.venv/bin/python -m pip install -r 4-for-your-AI/requirements.txt
```

This installs four things:
- `faster-whisper`: local speech-to-text.
- `yt-dlp`, with a bundled JavaScript runtime that YouTube needs: video and audio access.
- `python-docx`: the course books.
- `pypdf`: the text of PDF reports and rules manuals (`pdf-text`).

There is no need to activate the environment: from now on, run everything with `PY` (`4-for-your-AI\.venv\Scripts\python.exe` or `4-for-your-AI/.venv/bin/python`).

## 3. Check everything

```bash
PY 4-for-your-AI/tools/kit_doctor.py
```

It checks Python, the packages, yt-dlp and its JavaScript runtime, the speech model, and whether the forum index and the sources playbook are less than 30 days old. It also makes one live request each to the RoboMaster forum, GitHub and Bilibili. Each line prints as its check finishes. Loading the speech engine can take a minute or more (several minutes with a system Python that also has large AI libraries installed), so wait for it. Every line should read `ok` or `optional`. For any `FAIL` or `warn`, apply the fix printed beside it, then run the doctor again. Use `--offline` to skip the live checks.

## 4. Optional extras (ask the member first)

| Extra | Adds | Install |
|---|---|---|
| GitHub CLI `gh`, logged in | code search inside repositories (`gh search code`) | winget `GitHub.cli` / brew `gh` / apt `gh`, then `gh auth login` |
| `bili` (bilibili-cli) | channel listings from the shell (the kit's `bili-search` and `bili-video` already cover search and video pages) | `PY -m pip install bilibili-cli`. On Windows, set `PYTHONUTF8=1` before running it (PowerShell: `$env:PYTHONUTF8 = "1"`), or it crashes with `UnicodeEncodeError` whenever its output is piped |
| `ffmpeg` | transcribing from the middle of a long video (`--start`/`--end`) | winget `Gyan.FFmpeg` / brew `ffmpeg` / apt `ffmpeg` |
| speech model `medium` (1.5 GB) | better accuracy on clean lecture audio; 3 to 7 times slower | downloads itself on first `--model medium` |

## 5. Tell the member it is ready

Report which checks passed, which optional extras are present, and three things to try:
- "How do top teams do sentry navigation? Use the RoboMaster forum and GitHub."
- "What does this Bilibili video teach? <link>"

## If something breaks later

| Symptom | Fix |
|---|---|
| `No module named faster_whisper` / `docx` | You ran the system Python; use `PY`. Or re-run step 2. |
| "The filename or extension is too long", or "VAD filter requires the onnxruntime package" | The Windows path limit. Move the kit to `C:\rm-kit`, delete `4-for-your-AI\.venv`, and re-run step 2. |
| `yt-dlp is not installed` | Re-run step 2; check `4-for-your-AI/.venv` contains `yt-dlp` (`Scripts\yt-dlp.exe` on Windows, `bin/yt-dlp` elsewhere). A standalone `yt-dlp` on the PATH also works; the doctor's `yt-dlp` line names the one it found. |
| The doctor sits on `speech engine` for minutes | It is loading the speech engine. With a system Python that has other large AI libraries (such as `transformers` or `torch`), this alone can take minutes. Wait, and make sure you ran the doctor with `PY`, the kit's own Python. |
| The doctor warns `freshness: forum index` | Refresh it: `PY 4-for-your-AI/tools/rm_public_research.py bbs-index`. |
| The doctor warns `freshness: playbook` | The routes were last verified over 30 days ago. Re-check a route before calling a source broken, and pull the latest version of the kit's repository. |
| `pdf-text` says `pypdf` is not installed | Re-run step 2. |
| `pdf-text` returns `too-large` | Tell the member the size. Re-run with `--max-mib N` (at most 200) only if the file is really needed. |
| `bili` crashes with `UnicodeEncodeError` (Windows) | Set `PYTHONUTF8=1` (PowerShell: `$env:PYTHONUTF8 = "1"`; cmd: `set PYTHONUTF8=1`) and run it again. |
| YouTube fails with "Sign in to confirm" or a JS challenge error | Update: `PY -m pip install -U "yt-dlp[default,deno]"`. |
| Bilibili returns HTTP 412 | Their anti-bot block. Space requests at least 5 s apart and use the routes in the playbook, not the `view` API. |
| `oshwhub.com` does not resolve | Some campus networks block it. Use the Jina route in the playbook, or another network. |
| BBS search returns 0 hits | Use Chinese keywords; English rarely matches. |
