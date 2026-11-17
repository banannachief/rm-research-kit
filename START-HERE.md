# RoboMaster Research Kit: start here

This folder turns your AI (Claude, ChatGPT/Codex, Gemini, Cursor and others) into a RoboMaster research assistant. It can read the official RoboMaster forum, team code on GitHub and Gitee, and Bilibili videos, and it can turn Chinese video courses into English notes. It runs on **your** AI subscription.

It was built by a university RoboMaster team for its own members and is published so other English-speaking teams can use it.

## What is in this folder

```
rm-research-kit/
├── START-HERE.md                   ← you are here
├── 2-courses/                      ← every course YOU make appears here
├── 3-club-research/                ← the sources playbook, and the research notes your AI saves
├── 4-for-your-AI/                  ← your AI's toolbox: you never need to open this
└── AGENTS.md  CLAUDE.md  GEMINI.md ← instructions your AI reads by itself (leave these here)
```

## Start in three steps

1. **Download** this folder (clone it, or use GitHub's "Download ZIP") somewhere you will keep it, with a **short path**: on Windows, `C:\rm-kit`; on Mac, `Documents/rm-kit`. Windows breaks with very long folder paths, such as deep inside Downloads.
2. **Open the folder in an AI agent that can run commands:**
   - **Claude Code:** `cd` into the folder, then run `claude`.
   - **OpenAI Codex:** `cd` into the folder, then run `codex`.
   - **Cursor, Windsurf, or VS Code with Copilot:** Open Folder, then use the agent chat.
   - **Gemini CLI:** `cd` into the folder, then run `gemini`.
3. **Type:** `Set up the research kit.` It takes about 10 minutes and installs everything inside `4-for-your-AI/`. It asks before touching anything else on your computer.

## Then just ask

- *Make English notes from this Bilibili course: <link>* → your notes appear in `2-courses/`.
- *What does this video teach? <link>*
- *How do top teams do sentry navigation? Use the RoboMaster forum and GitHub.*

## Good to know

- **No terminal-capable AI?** You can still read `3-club-research/sources-playbook.md` yourself, or upload it to a chat AI. The tools need an agent that can run commands.
- **Speed and cost:** a video is transcribed on your computer at about its own length; a 5-hour course takes an evening. Writing the notes uses about one AI request per lecture.
- **Stay private:** searches go to the internet. Keep your team's private details (names, unreleased designs, sponsors) out of them.
- **Share back:** found a better source or a broken route? Open an issue or a pull request on this repository.

## Sharing rules

- **Course notes credit the lecturer and link the original video.** Keep those credits when you share notes, and ask the lecturer before publishing notes of their course.
- **Transcripts** (in `4-for-your-AI/working-files/`) are the lecturers' own words. Keep them on your computer.
- **Other teams' code and designs belong to them.** Read the licence before reusing anything (many RoboMaster projects are GPL), credit the team, and do not re-host their files.
- **The tools** (faster-whisper, yt-dlp, python-docx, pypdf) keep their own licences.
