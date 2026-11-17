---
name: lecture-notes
description: Turn a Chinese Bilibili teaching series (a 合集 collection, a multi-part video, or one long lecture, even tens of hours) into English study notes - per-lecture walkthroughs with clickable timestamps, key settings, glossary and self-check questions, a course overview with a learning path, and a .docx course book. Use for "make English notes from this Bilibili course", "help me study this series", or to read the course notes already in the kit.
---

# Chinese course → English study notes

`4-for-your-AI/tools/lecture_series.py` runs the pipeline.

**Where things go.** Every course is one folder in `2-courses/<slug>/`:
- `COURSE-BOOK.docx`: the whole course to read.
- `COURSE-OVERVIEW.md`: summary, learning path, and the list of lectures.
- `lectures/`: one notes file per lecture.

Transcripts, prompts and drafts go in `4-for-your-AI/working-files/<slug>/`, never anywhere else. If the member only wants to study a finished course, read its notes: no setup needed.

## 1. Read the course and estimate the time

```bash
PY 4-for-your-AI/tools/lecture_series.py manifest <any BV id or URL from the course> --slug <short-english-name>
```

- One page fetch lists every episode with its length, and works for a 合集, a multi-part video or a single video.
- Tell the member the episode count, total length and ETA before starting.
- **Transcription speed:** about real time per worker on a laptop. On a machine with 8 or more cores, run 2 or 3 workers with 4 threads each; they share the course safely through per-episode locks.
- **Notes speed:** about 1 minute per lecture.

## 2. Transcribe, detached (it can take hours)

Do not run a long transcription inside your own turn; most agents stop long commands. Start it detached and check back with `status`:

```powershell
# Windows (PowerShell), three workers
$env:PUBLIC_TRANSCRIBE_THREADS = "4"
1..3 | ForEach-Object { Start-Process 4-for-your-AI\.venv\Scripts\python.exe -ArgumentList '4-for-your-AI/tools/lecture_series.py','transcribe','--slug','<slug>' -WindowStyle Hidden -RedirectStandardOutput "4-for-your-AI\working-files\<slug>\worker$_.log" -RedirectStandardError "4-for-your-AI\working-files\<slug>\worker$_.err"; Start-Sleep 20 }
```
```bash
# macOS / Linux, two workers
for w in 1 2; do PUBLIC_TRANSCRIBE_THREADS=4 nohup 4-for-your-AI/.venv/bin/python 4-for-your-AI/tools/lecture_series.py transcribe --slug <slug> > 4-for-your-AI/working-files/<slug>/worker$w.log 2>&1 & sleep 20; done
```
```bash
PY 4-for-your-AI/tools/lecture_series.py status --slug <slug>     # transcribed / noted / what is missing
```

- It resumes: re-run the same command after any interruption, and finished episodes are skipped.
- `--episodes 1-10` limits a run.
- A worker that was killed leaves `4-for-your-AI/working-files/<slug>/transcripts/NNN.lock`. Delete it once no worker is running.

## 3. Write the notes: choose one way

**A. You write them (works with any model; best for a few lectures).** For each transcribed episode:
1. `PY 4-for-your-AI/tools/lecture_series.py prompt --slug <slug> --episode N > 4-for-your-AI/working-files/<slug>/epN-prompt.txt`
2. Read that file and write the notes **exactly** as it specifies, in English, into `4-for-your-AI/working-files/<slug>/epN.md`.
3. `PY 4-for-your-AI/tools/lecture_series.py save --slug <slug> --episode N --file 4-for-your-AI/working-files/<slug>/epN.md`

`save` checks every required section is present and the text is English, links the timestamps, and updates the course page. If it rejects the notes, fix what the error names and save again. Then write the overview the same way with `prompt --overview` and `save --overview --file …`.

**B. A command-line model writes them in one batch (best for a whole course).** Give `--llm-cmd` any program that reads a prompt on standard input and prints the answer:

```bash
PY 4-for-your-AI/tools/lecture_series.py notes --slug <slug> --llm-cmd "claude -p"            # Claude Code
PY 4-for-your-AI/tools/lecture_series.py notes --slug <slug> --llm-cmd "codex exec -"         # OpenAI Codex CLI
PY 4-for-your-AI/tools/lecture_series.py notes --slug <slug> --llm-cmd "ollama run --nowordwrap --hidethinking <model>"   # local, via Ollama
PY 4-for-your-AI/tools/lecture_series.py overview --slug <slug> --llm-cmd "<same>"
```

- Each lecture is one call on the member's own subscription; local Ollama models are free but slower.
- Notes that fail validation are reported and skipped, never saved half-done. Re-run to retry, or use A for that episode.
- `--force` rewrites existing notes.

**Local models:** use one with at least a 16k context window. Expect weaker notes from small (7B-class) models. In testing, one cited timestamps only from the first 35 seconds of a 6-minute lecture and copied speech-recognition errors.

Validation rejects notes like that, so failures are reported, never saved:
- missing sections;
- walkthrough timestamps that do not reach halfway through the lecture;
- leftover terminal codes;
- text that is not in English.

When an episode is rejected, switch to a stronger model or write it yourself (way A).

**Number warnings:** `notes` and `save` list any number in the notes that the lecture never said (`number_warnings`). Check each against the transcript, then fix it or flag it with `(check: …)`.

## 4. Course book and quality check

```bash
PY 4-for-your-AI/tools/lecture_series.py export --slug <slug>     # 2-courses/<slug>/COURSE-BOOK.docx
```

Before sharing anything:
- **Numbers:** every number in the notes should appear in that episode's transcript (`4-for-your-AI/working-files/<slug>/transcripts/NNN.json`). The exceptions are Chinese numerals (三万 = 30000), simple arithmetic, and `(check: …)` flags. A number with no source is invented: rewrite that episode.
- **Spot-check:** open two lectures and check three facts each against the video at the linked timestamps (a number, a part name, a step).

## What good notes contain (the prompt enforces this; keep it if you write them by hand)

- **Sections:** an English title and summary, What you will learn, Prerequisites, a Walkthrough under `[mm:ss]` headings, Key details, Pitfalls and tips, a Glossary table (中文 | English | Meaning), three self-check questions, and Transcript notes.
- **Key details:** every setting needed to reproduce the lecture (pins, baud rates, prescalers, IDs, values typed in).
- **Speaker slips are flagged, never silently fixed:** "stated as 24 V (check: a 6S LiPo is nominally 22.2 V)".
- **Your own advice** starts with "Team note:".
- **Names:** RoboMaster's English names are used (步兵 = Standard, C板 = Development Board Type C), with the Chinese on first use.

## Rules

- Public videos only; never private recordings.
- Transcripts stay on this computer. The notes credit the lecturer and link the original.
- Good finished notes: share them within your team. Ask the lecturer before posting notes of their course publicly.
