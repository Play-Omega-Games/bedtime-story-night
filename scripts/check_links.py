#!/usr/bin/env python3
"""Live checks for Bedtime Story Night.

1. Every source edition the build uses returns HTTP 200, and every story's paragraphs are found in the live text.
2. With --raw: the plan and build files load from raw.githubusercontent.com main (after the repo is public).
Usage, from the repo root: python3 scripts/check_links.py [--raw]
"""
import json, re, sys, time, urllib.request
sys.path.insert(0, 'scripts')
import build

UA = {'User-Agent': 'Mozilla/5.0 (bedtime-story-night link check)'}
RAW = 'https://raw.githubusercontent.com/Play-Omega-Games/bedtime-story-night/main/'

def get(url, tries=4):
    err = None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.status, r.read().decode('utf-8', 'replace')
        except Exception as e:
            err = e; time.sleep(3 * (i + 1))
    return getattr(err, 'code', 0) or 0, ''

squash = lambda t: re.sub(r'\s+', ' ', t.replace('_', '').replace('\r', '')).strip()
stories = json.load(open('plans/stories.json', encoding='utf-8'))['stories']
bad, live = [], {}
for key, s in build.SOURCES.items():
    u = build.url(s['num'])
    st, body = get(u)
    print(f'{st} {u}', flush=True)
    if st != 200:
        bad.append((u, f'HTTP {st}')); continue
    live[s['edition']] = squash(body)
    time.sleep(1)
n = 0
for s in stories:
    txt = live.get(s['edition'])
    if txt is None:
        continue
    parts = [f['text'] for f in s['fables']] if s['kind'] == 'fables' else [s['text']]
    for p in parts:
        for para in p.split('\n\n'):
            if para in ('First Version.', 'Second Version.'):
                continue
            n += 1
            if squash(para) not in txt:
                bad.append((s['id'], 'paragraph not found live: ' + para[:60]))
print(f'{len(stories)} nights, {n} paragraphs checked against the live sources')
if '--raw' in sys.argv:
    for f in ('plans/stories.json', 'scripts/build.py', 'scripts/curation.py', 'MANIFEST.txt'):
        st, _ = get(RAW + f, tries=2)
        print(f'{st} {RAW + f}')
        if st != 200:
            bad.append((RAW + f, f'HTTP {st}'))
if bad:
    print(f'{len(bad)} PROBLEMS'); [print(' ', a, b) for a, b in bad[:40]]; sys.exit(1)
print('ALL LINKS OK')
