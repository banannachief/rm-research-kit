---
name: video-transcribe
description: Transcribe a public Bilibili or YouTube video on this computer (Chinese or English) and report what it actually says, with timestamps - for RoboMaster tutorials, match commentary, rule briefings and team technical talks. Use when the member shares a video link or BV id and asks what it teaches or says.
---

# Transcribe a public video

`4-for-your-AI/tools/public_media_transcribe.py` downloads only the audio, with no login and no cookies, and transcribes it on this computer with faster-whisper and a RoboMaster glossary. Nothing is uploaded, and the audio is deleted afterwards.

```bash
PY 4-for-your-AI/tools/public_media_transcribe.py BV1E24y1C7ER                          # Bilibili (Chinese by default)
PY 4-for-your-AI/tools/public_media_transcribe.py "https://youtu.be/VRL-xmK0nvw"         # YouTube (language detected)
PY 4-for-your-AI/tools/public_media_transcribe.py BV1E24y1C7ER --start 600               # the next 10 minutes of a long video
PY 4-for-your-AI/tools/public_media_transcribe.py BV1E24y1C7ER --model medium --end 240  # clean lecture audio, more accurate
```

- **Output:** JSON with the title, uploader, window, detected language, timestamped `segments`, the full `text`, and `quality_warnings`.
- **Windows:** one call covers 10 minutes (4 with `medium`). A long video returns `truncated: true` and a `next_start` value to continue from. Starting mid-video needs `ffmpeg` (see the setup skill).
- **Speed:** about real time with the default `small` model on a typical laptop; `medium` is 3 to 7 times slower. Tell the member before starting anything long.
- **First run:** it downloads the speech model (0.5 GB for `small`, 1.5 GB for `medium`).
- **Before transcribing,** `PY 4-for-your-AI/tools/rm_public_research.py bili-video <BV id>` reads the title, uploader, date and description links in one quick request; the links (lesson code, documents) often answer the question without any transcription. `bili-search "<中文关键词>"` finds videos.

## Which model

| Model | Use for | Measured on RoboMaster audio |
|---|---|---|
| `small` (default) | anything, especially noisy match or stream audio | 9 of 12 jargon terms right; keeps all speech |
| `medium` | clean, single-speaker lectures | 11 of 12 terms; dropped up to 38% of speech on a noisy talk |

## Report what it says, honestly

- Summarise in English and cite moments as Bilibili `?t=<seconds>` links (YouTube: `&t=`).
- Speech recognition mishears jargon: 电条 for 电调 (ESC), 涂船 for 图传 (video transmission), "C-BAR" or "Saber" for C板 (Development Board Type C), 看 for CAN. Correct these from context and say you did.
- It cannot see the screen. When the speaker says "this line here", say the detail is on screen and not in the audio.
- `quality_warnings` mark hallucinated repetition loops (already collapsed) and dropped segments; mention them.
- Check exact numbers, code and wiring against the video before anyone builds from them.

## Rules

- Public videos only. Never put private recordings (meetings, calls) through this tool.
- Transcripts are the speaker's words: keep them on this computer. Do not post or upload them.
- For a whole course or series, use `4-for-your-AI/skills/lecture-notes/SKILL.md` instead.
