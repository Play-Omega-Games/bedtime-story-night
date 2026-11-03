"""Offline checks on plans/stories.json. Run from the repo root: python3 tests/test_plan.py
If ./src holds the source texts (python3 scripts/build.py --fetch), it also checks every story word for word."""
import collections, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import build, curation as C

PLAN = json.load(open(os.path.join(ROOT, 'plans', 'stories.json'), encoding='utf-8'))
S = PLAN['stories']
EM = '\u2014'
SLURS = re.compile(r"\b(nigger\w*|chinam[ae]n|negro(es)?|squaws?|coolies?|blackamoors?|hottentots?|darkies|savages?|gipsy|gypsy|gipsies|gypsies|bitch)\b", re.I)
EXCLUDED_TITLES = ['the little match girl', 'the red shoes', 'the almond tree', 'the juniper tree', 'the robber bridegroom',
                   'the metal pig', 'how the leopard got his spots', 'the æthiop', 'the bitch and her whelps']

def test_count_ids_order():
    assert len(S) >= 190
    assert len({s['id'] for s in S}) == len(S)
    assert [s['order'] for s in S] == list(range(1, len(S) + 1))

def test_fields():
    for s in S:
        for k in ('id', 'title', 'author', 'source', 'kind', 'text', 'first_line', 'words', 'minutes', 'min_age', 'flags', 'level', 'edition'):
            assert s.get(k) not in (None, ''), (s['id'], k) if k != 'flags' else None
        assert s['min_age'] in (3, 6, 9), s['id']
        assert s['minutes'] == max(1, math.ceil(s['words'] / build.WPM)), s['id']
        assert set(s['flags']) <= set(PLAN['meta']['flags']), s['id']
        assert s['level'] == build.level(s['flags']), s['id']
        assert s['text'].startswith(s['first_line'][:20]) or s['kind'] == 'fables', s['id']

def test_editions_before_1931():
    for s in S:
        assert int(re.search(r'(\d{4})', s['edition']).group(1)) < 1931, s['id']

def test_excluded_never_present():
    titles = {s['title'].lower() for s in S} | {f['title'].lower() for s in S for f in s.get('fables', [])}
    for t in EXCLUDED_TITLES:
        assert t not in titles, t
    for s in S:
        assert 'match girl' not in s['title'].lower() and 'red shoes' not in s['title'].lower()

def test_no_slurs_or_dated_words_outside_flagged():
    for s in S:
        m = SLURS.search(s['text'])
        if m:
            assert 'dated' in s['flags'], (s['id'], m.group(0))

def test_gentle_means_gentle():
    for s in S:
        if s['level'] != 'gentle':
            continue
        if s['source'] == 'aesop':
            for f in s['fables']:
                assert build.scan_flags(f['text']) == [] or f['title'] in C.AESOP_OVERRIDES, f['title']
                assert f['flags'] == [], f['title']
        else:
            hits = [m.group(0) for k in ('death', 'violence') for m in re.finditer(build.FLAG_WORDS[k], s['text'], re.I)]
            assert not hits or s['id'] in C.REVIEWED_GENTLE, (s['id'], hits[:5])

def test_series_in_order_and_together():
    by = collections.defaultdict(list)
    for s in S:
        if s.get('series'):
            by[s['series']['id']].append(s)
    assert by, 'expected the two series'
    for sid, parts in by.items():
        assert [p['series']['part'] for p in parts] == list(range(1, len(parts) + 1)), sid
        orders = [p['order'] for p in parts]
        assert orders == list(range(orders[0], orders[0] + len(parts))), sid

def test_every_fable_used_once():
    names = [f['title'] for s in S for f in s.get('fables', [])]
    assert len(names) == PLAN['meta']['aesop_fables'], (len(names), PLAN['meta']['aesop_fables'])

def test_fable_sets():
    for s in S:
        if s['kind'] == 'fables':
            assert 2 <= len(s['fables']) <= 5, s['id']
            assert s['text'] == '\n\n'.join(f"{f['title']}\n\n{f['text']}" for f in s['fables']), s['id']
            assert sorted({x for f in s['fables'] for x in f['flags']}) == s['flags'], s['id']

def test_no_editorial_junk():
    junk = re.compile(r'Project Gutenberg|\[Illustration|Illustration:|\bFootnote|CONTENTS|\bINDEX\b|\[Pg|\{\d+\}|\[\d+\]|_|Transcriber', re.M)
    for s in S:
        m = junk.search(s['text'])
        assert not m, (s['id'], m.group(0))

def test_no_third_party_names_in_owner_facing_fields():
    names = re.compile(r'\b(Gutenberg|Townsend|Lucy Crane|Walter Crane|Stickney|Dulac|Rackham|Margaret Hunt|Hersholt|Ginn|Macmillan|Dover|Routledge)\b', re.I)
    for s in S:
        for k in ('title', 'author', 'first_line'):
            assert not names.search(s[k]), (s['id'], k)
    assert not names.search(json.dumps(PLAN['meta']))

def test_no_em_dash_in_our_words():
    assert EM not in json.dumps(PLAN['meta'], ensure_ascii=False)
    for s in S:
        assert EM not in s['title'], s['id']

def test_spread():
    c = collections.Counter(s['source'] for s in S)
    assert set(c) == {'aesop', 'grimm', 'andersen', 'kipling'}
    for a, b in zip(S, S[1:]):
        if not (a.get('series') and b.get('series')):
            assert not (a['source'] == b['source'] == 'kipling'), a['id']

def test_verbatim_against_sources():
    src = os.path.join(ROOT, 'src')
    if not os.path.isdir(src):
        print('     (skipped: no ./src; run python3 scripts/build.py --fetch)'); return
    squash = lambda t: re.sub(r'\s+', ' ', t.replace('_', '')).strip()
    raw = {}
    for k, v in build.SOURCES.items():
        raw[v['edition']] = squash(open(os.path.join(src, f"pg{v['num']}.txt"), encoding='utf-8').read())
    n = 0
    for s in S:
        parts = [f['text'] for f in s['fables']] if s['kind'] == 'fables' else [s['text']]
        for p in parts:
            for para in p.split('\n\n'):
                if s['source'] == 'grimm' and para in ('First Version.', 'Second Version.'):
                    continue
                assert squash(para) in raw[s['edition']], (s['id'], para[:80])
                n += 1
    print(f'     {n} paragraphs matched word for word')

if __name__ == '__main__':
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            try:
                fn(); print('ok  ', name)
            except AssertionError as ex:
                fails += 1; print('FAIL', name, str(ex)[:300])
    print(f"{len(S)} nights; {'ALL PASS' if not fails else str(fails) + ' FAILED'}")
    sys.exit(1 if fails else 0)
