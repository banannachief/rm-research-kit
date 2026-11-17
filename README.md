# RoboMaster Research Kit

Most RoboMaster engineering knowledge is written in Chinese: the official forum, team
repositories, Bilibili lectures. This kit lets an English-speaking team use it.

Open the folder in your own AI agent (Claude Code, Codex, Gemini CLI, Cursor) and ask in
English. The agent searches the Chinese sources in Chinese, reads them, and answers with
links. It can also turn a Chinese video course into English study notes.

Built by a university RoboMaster team for its members; published for other teams.

- **See it work:** [EXAMPLE.md](EXAMPLE.md) finds eight teams' open-source sentry navigation in one command.
- **Just want the map?** [The sources playbook](3-club-research/sources-playbook.md) lists which RoboMaster sources an AI agent can read, which ones block it, and the tested way around each. It is useful without installing anything.
- **Set it up:** [START-HERE.md](START-HERE.md). About 10 minutes.

## What is inside

- **Four skills** in `4-for-your-AI/skills/`: kit setup, RoboMaster research, public video
  transcription, and course notes.
- **Three tools** in `4-for-your-AI/tools/`:
  - `rm_public_research.py`: search and read the official forum, read its PDFs, find
    Bilibili videos, inspect GitHub repositories.
  - `public_media_transcribe.py`: transcribe a public Bilibili or YouTube video on your own
    computer, with a RoboMaster glossary.
  - `lecture_series.py`: turn a whole course into notes with timestamps, a glossary and
    self-check questions.
- **`kit_doctor.py`** checks the setup.

Everything is read-only against public sources: no accounts, no cookies, no posting.
Transcription runs on your own computer, and the AI runs on your own subscription.

## What is not inside

Finished course notes and transcripts. Those are the lecturers' work: make your own copy
for study, and ask the lecturer before publishing notes of their course.

## Help keep it accurate

Each route in the playbook carries the date it was last tested. Sites change. If a route
stops working, or you find a better one, please open an issue.

## Licence

MIT for the kit's own files.
The tools it installs (faster-whisper, yt-dlp, python-docx, pypdf) keep their own licences.
