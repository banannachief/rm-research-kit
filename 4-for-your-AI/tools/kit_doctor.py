#!/usr/bin/env python3
"""RoboMaster Research Kit - setup doctor.

    python 4-for-your-AI/tools/kit_doctor.py            local checks + one live request each to the
                                            RoboMaster forum, GitHub and Bilibili
    python 4-for-your-AI/tools/kit_doctor.py --offline  local checks only
    python 4-for-your-AI/tools/kit_doctor.py --json     machine-readable report

Every check prints ok / warn / optional / FAIL, and every FAIL or warn carries the fix.
Exit code 1 when anything FAILs.
"""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

SETUP = 'see 4-for-your-AI/skills/kit-setup/SKILL.md'
# yt-dlp is not a package check: the tools run the yt-dlp executable, so a standalone yt-dlp.exe is fine.
REQUIRED = {'faster_whisper': 'faster-whisper', 'docx': 'python-docx', 'pypdf': 'pypdf'}


def check_python():
    v = sys.version_info
    detail = 'Python %d.%d.%d at %s' % (v.major, v.minor, v.micro, sys.executable)
    if v < (3, 10):
        return 'FAIL', detail, 'install Python 3.12 and recreate 4-for-your-AI/.venv (%s)' % SETUP
    if v >= (3, 14):
        return 'warn', detail, 'speech-model packages may lack 3.14 wheels; use Python 3.12 if installs fail'
    if sys.prefix == sys.base_prefix:
        return 'warn', detail, ('this is not the kit environment; run tools with 4-for-your-AI\\.venv\\Scripts\\python.exe '
                                '(Windows) or 4-for-your-AI/.venv/bin/python')
    return 'ok', detail, ''


def check_packages():
    missing = [pip for mod, pip in REQUIRED.items() if importlib.util.find_spec(mod) is None]
    if missing:
        return 'FAIL', 'missing: ' + ', '.join(missing), \
            'PY -m pip install -r 4-for-your-AI/requirements.txt (PY = the kit environment python)'
    return 'ok', 'faster-whisper, python-docx, pypdf installed', ''


KIT_ROOT = os.path.dirname(os.path.dirname(HERE))
SHORT_PATH_FIX = ('Windows limits paths to 260 characters: move the kit folder somewhere short such as '
                  'C:\\rm-kit, delete 4-for-your-AI\\.venv, and run setup again')


def check_kit_path():
    if os.name == 'nt' and len(KIT_ROOT) > 100:
        return 'warn', 'kit path is %d characters long: %s' % (len(KIT_ROOT), KIT_ROOT), SHORT_PATH_FIX
    return 'ok', KIT_ROOT, ''


def check_speech_engine():
    """Actually load what transcription needs: a package can be installed yet fail to load."""
    for module in ('ctranslate2', 'onnxruntime', 'av'):
        try:
            importlib.import_module(module)
        except ImportError as exc:
            detail = '%s will not load: %s' % (module, str(exc)[:160])
            if 'too long' in str(exc).lower():
                return 'FAIL', detail, SHORT_PATH_FIX
            return 'FAIL', detail, 'PY -m pip install --force-reinstall -r 4-for-your-AI/requirements.txt'
    return 'ok', 'speech engine loads (ctranslate2, onnxruntime, av)', ''


def check_ytdlp():
    import public_media_transcribe as pmt
    exe = pmt.ytdlp_bin()
    out = subprocess.run([exe, '--version'], capture_output=True, text=True, timeout=60, env=pmt.ytdlp_env())
    if out.returncode != 0:
        return 'FAIL', 'yt-dlp did not run: %s' % (out.stderr or out.stdout)[:120], \
            'PY -m pip install -U "yt-dlp[default,deno]"'
    return 'ok', 'yt-dlp %s at %s' % (out.stdout.strip(), exe), ''


def check_js_runtime():
    import public_media_transcribe as pmt
    found = shutil.which('deno', path=pmt.ytdlp_env()['PATH']) or shutil.which('node')
    if not found:
        return 'warn', 'no JavaScript runtime: YouTube downloads will fail (Bilibili still works)', \
            'PY -m pip install -U "yt-dlp[default,deno]"'
    return 'ok', found, ''


def check_speech_model():
    try:
        from faster_whisper.utils import download_model
        download_model('small', local_files_only=True)
        return 'ok', 'whisper "small" is downloaded', ''
    except Exception:  # noqa: BLE001 - absent, or faster-whisper itself missing (reported above)
        return 'optional', 'whisper "small" downloads on the first transcription (~0.5 GB)', ''


def check_tool(name, purpose, fix):
    path = shutil.which(name)
    return ('ok', '%s at %s' % (name, path), '') if path else ('optional', '%s not installed (%s)' % (name, purpose), fix)


# The research freshness checks: how old the offline forum index and the sources playbook are.
MAX_AGE_DAYS = 30
RESEARCH = '3-club-research'
INDEX_FILE = '2026-09-08-rm-bbs-source-index.json'
PLAYBOOK_DATE = re.compile(r'(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)')


def today():
    return datetime.date.today()


def check_index_age():
    try:
        with open(os.path.join(KIT_ROOT, RESEARCH, INDEX_FILE), encoding='utf-8') as handle:
            index = json.load(handle)
        checked = datetime.datetime.fromisoformat(index['checked_at']).date()
    except (OSError, ValueError, KeyError, TypeError):
        return 'warn', 'forum index not found or unreadable', \
            'rebuild it: PY 4-for-your-AI/tools/rm_public_research.py bbs-index'
    age = (today() - checked).days
    articles = index.get('articles')
    count = len(articles) if isinstance(articles, list) else 0
    if age <= MAX_AGE_DAYS:
        return 'ok', 'forum index checked %s (%d days ago, %d articles)' % (checked.isoformat(), age, count), ''
    return 'warn', 'forum index last checked %s, %d days ago' % (checked.isoformat(), age), \
        'refresh it: PY 4-for-your-AI/tools/rm_public_research.py bbs-index'


def check_playbook_age():
    try:
        with open(os.path.join(KIT_ROOT, RESEARCH, 'sources-playbook.md'), encoding='utf-8') as handle:
            text = handle.read()
    except (OSError, ValueError):
        text = ''
    now = today()
    dates = []
    for found in PLAYBOOK_DATE.findall(text):
        try:
            day = datetime.date.fromisoformat(found)
        except ValueError:
            continue
        # A competition date written in the future says nothing about when the routes were checked.
        if day <= now:
            dates.append(day)
    if not dates:
        return 'warn', 'sources playbook not found or undated', 're-unzip the kit, or ask for a newer kit'
    last = max(dates)
    age = (now - last).days
    if age <= MAX_AGE_DAYS:
        return 'ok', 'sources playbook last verified %s (%d days ago)' % (last.isoformat(), age), ''
    return 'warn', 'sources playbook last verified %s, %d days ago' % (last.isoformat(), age), \
        'routes may have changed: re-check a route before calling a source broken, and ask for a newer kit ' \
        '(START-HERE.md, "Share back")'


def live_forum():
    import rm_public_research as rpr
    r = rpr.bbs_search('超级电容', page_size=1)
    return 'ok' if (r.get('total_hits') or 0) > 0 else 'FAIL', '%s forum posts match 超级电容' % r.get('total_hits')


def live_github():
    import rm_public_research as rpr
    r = rpr.github('HNUYueLuRM/basic_framework')
    return 'ok', 'GitHub API answered (basic_framework tip %s)' % r['tip_sha'][:7]


def live_bilibili():
    # Members read Bilibili with this tool, so the doctor checks the reader they will actually run.
    import rm_public_research as rpr
    video = rpr.bili_video('BV1E24y1C7ER')
    season = video.get('season') or {}
    episode_count = season.get('episode_count') or 0
    return 'ok', 'Bilibili video page readable (%d-episode course)' % episode_count


LIVE = [('live: RoboMaster forum search', live_forum, 'check the internet connection; the forum may be down'),
        ('live: GitHub API', live_github, 'check the connection; GitHub allows 60 anonymous requests an hour'),
        ('live: Bilibili', live_bilibili, 'check the connection; if HTTP 412, wait a few minutes (anti-bot)')]


def run(offline, report=None, starting=None):
    checks = []

    def add(name, fn, fix_on_error=SETUP, slow=False):
        if slow and starting is not None:
            starting(name)
        try:
            status, detail, *fix = fn()
            fix = fix[0] if fix else ''
        except Exception as exc:  # noqa: BLE001 - a check that crashes is a failed check, with its reason
            status, detail, fix = 'FAIL', '%s: %s' % (type(exc).__name__, str(exc)[:160]), fix_on_error
        if status == 'FAIL' and not fix:
            fix = fix_on_error
        checks.append({'name': name, 'status': status, 'detail': detail, 'fix': fix})
        if report is not None:
            report(checks[-1])

    add('python', check_python)
    add('kit location', check_kit_path)
    add('packages', check_packages)
    add('speech engine', check_speech_engine, slow=True)
    add('yt-dlp', check_ytdlp, 'PY -m pip install -r 4-for-your-AI/requirements.txt', slow=True)
    add('javascript runtime', check_js_runtime)
    add('speech model', check_speech_model)
    add('freshness: forum index', check_index_age)
    add('freshness: playbook', check_playbook_age)
    add('optional: gh', lambda: check_tool('gh', 'code search inside repositories', 'see the setup skill, step 4'))
    add('optional: bili', lambda: check_tool('bili', 'Bilibili search from the shell', 'PY -m pip install bilibili-cli'))
    add('optional: ffmpeg', lambda: check_tool('ffmpeg', 'start transcription mid-video', 'see the setup skill, step 4'))
    if not offline:
        for name, fn, fix in LIVE:
            add(name, lambda fn=fn: (*fn(), ''), fix, slow=True)
    return checks


def line(check):
    return '%-9s %-32s %s%s' % (check['status'], check['name'], check['detail'],
                                ('   -> fix: ' + check['fix']) if check['fix'] else '')


def heads_up(name):
    # A slow check says so before it starts, so a quiet minute is not mistaken for a hang.
    if name == 'speech engine':
        wait = 'loading the speech engine (can take a minute or more)'
    elif name == 'yt-dlp':
        wait = 'starting yt-dlp (a few seconds)'
    else:
        wait = 'asking the live source (can take a moment)'
    return line({'status': '...', 'name': name, 'detail': wait, 'fix': ''})


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--offline', action='store_true', help='skip the live source checks')
    ap.add_argument('--json', action='store_true', help='print a JSON report')
    args = ap.parse_args(argv)
    if args.json:
        checks = run(args.offline)
    else:
        scope = 'offline checks only' if args.offline else 'local checks, then one live request per source'
        print('RoboMaster Research Kit doctor (%s)' % scope, flush=True)

        def show(check):
            print(line(check), flush=True)

        def starting(name):
            print(heads_up(name), flush=True)
        checks = run(args.offline, report=show, starting=starting)
    failed = any(c['status'] == 'FAIL' for c in checks)
    if args.json:
        print(json.dumps({'ok': not failed, 'checks': checks}, ensure_ascii=False, indent=1))
    else:
        print('\nAll required checks passed.' if not failed else '\nSome checks FAILED: apply the fixes above, then run this again.')
    return 1 if failed else 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    raise SystemExit(main())
