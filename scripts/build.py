"""Build plans/stories.json for Bedtime Story Night from public-domain editions published before 1931.

Usage (from the repo root, standard library only):
  python3 scripts/build.py --fetch   # download the source texts into ./src, then build
  python3 scripts/build.py           # build from ./src
Story text is copied word for word from the source edition. The build only removes picture
captions and footnote markers, drops italic underscores and joins hard-wrapped lines into paragraphs.
"""
import json, math, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
import curation as C

SRC = ROOT / 'src'
OUT = ROOT / 'plans' / 'stories.json'
WPM = 150  # read-aloud pace for a parent reading to a child

SOURCES = {
    'aesop':     {'edition': 'aesop-1867',    'num': 21},
    'grimm':     {'edition': 'grimm-1886',    'num': 19068},
    'andersen1': {'edition': 'andersen-1914', 'num': 32571},
    'andersen2': {'edition': 'andersen-1915', 'num': 32572},
    'andersen3': {'edition': 'andersen-1911', 'num': 17860},
    'kipling':   {'edition': 'kipling-1902',  'num': 2781},
}
AUTHOR = {'aesop': 'Aesop', 'grimm': 'the Brothers Grimm', 'andersen': 'Hans Christian Andersen', 'kipling': 'Rudyard Kipling'}

def url(num):
    return f'https://www.gutenberg.org/cache/epub/{num}/pg{num}.txt'

def fetch():
    SRC.mkdir(exist_ok=True)
    for s in SOURCES.values():
        p = SRC / f"pg{s['num']}.txt"
        if p.exists() and p.stat().st_size > 10000:
            continue
        for attempt in range(4):
            try:
                req = urllib.request.Request(url(s['num']), headers={'User-Agent': 'bedtime-story-night-build/1.0'})
                p.write_bytes(urllib.request.urlopen(req, timeout=60).read())
                break
            except Exception as e:
                print('retry', s['num'], e); time.sleep(5 * (attempt + 1))
        else:
            sys.exit(f"could not download {url(s['num'])}")

def lines_of(key):
    return (SRC / f"pg{SOURCES[key]['num']}.txt").read_text(encoding='utf-8').replace('\r\n', '\n').split('\n')

norm = lambda s: re.sub(r'[^a-z]', '', s.lower().replace('&', 'and'))
SMALL = {'a', 'an', 'and', 'the', 'of', 'in', 'on', 'to', 'by', 'with', 'his', 'her', 'at', 'for', 'from', 'is', 'who', 'that'}
KEEP_SMALL = {'his', 'her', 'is', 'who', 'that'}

def title_case(s):
    s = s.strip().rstrip(',.').strip()
    words = s.split(' ')
    out = []
    for i, w in enumerate(words):
        lw = w.lower()
        if i > 0 and lw in SMALL and lw not in KEEP_SMALL:
            out.append(lw)
        else:
            out.append('-'.join(p[:1].upper() + p[1:].lower() for p in w.split('-')))
    t = ' '.join(out)
    return t.replace('Mrs. ', 'Mrs. ').replace('Mr. ', 'Mr. ')

def clean(block):
    """block: list of raw lines -> cleaned text with paragraphs separated by blank lines."""
    out, depth = [], 0
    for l in block:
        if depth or l.lstrip().startswith('[Illustration'):
            depth += l.count('[') - l.count(']')
            if depth < 0: depth = 0
            continue
        out.append(l)
    paras, cur = [], []
    for l in out + ['']:
        if l.strip():
            cur.append(l.rstrip())
        elif cur:
            paras.append(cur); cur = []
    res = []
    for p in paras:
        if re.fullmatch(r'[_\s*]+', ''.join(p)):
            continue
        if re.match(r'\s*\[(\d+|[A-Z])\]|\s*\[Footnote', p[0]):  # footnote body
            continue
        if all(re.match(r'\s{2,}\S', l) for l in p):  # verse: keep lines
            ind = min(len(l) - len(l.lstrip()) for l in p)
            txt = '\n'.join(l[ind:] for l in p)
        else:
            txt = ' '.join(l.strip() for l in p)
        txt = re.sub(r'\[(\d+|[A-Z])\]', '', txt).replace('_', '')
        txt = re.sub(r'[ \t]+', ' ', txt) if '\n' not in txt else '\n'.join(re.sub(r'[ \t]+', ' ', x) for x in txt.split('\n'))
        res.append(txt.strip())
    return '\n\n'.join(res)

def words(t):
    return len(re.findall(r"[A-Za-z’'-]+", t))

def first_line(t):
    s = t.split('\n')[0]
    m = re.match(r'(.{20,140}?[.!?;:])(\s|$)', s)
    return (m.group(1) if m else s[:140]).strip()

def find_heads(lines, titles, start, end, prev_blank=1):
    N = {norm(t): t for t in titles}
    heads, seen = [], set()
    for i in range(start, end):
        k = norm(lines[i])
        if k in N and N[k] not in seen and all(not lines[i - j].strip() for j in range(1, prev_blank + 1)):
            heads.append((i, N[k])); seen.add(N[k])
    return heads

def segment(lines, heads, end):
    for n, (i, t) in enumerate(heads):
        j = heads[n + 1][0] if n + 1 < len(heads) else end
        yield t, lines[i + 1:j]

def idx(lines, text, after=0):
    for i in range(after, len(lines)):
        if lines[i].strip() == text:
            return i
    raise SystemExit(f'marker not found: {text}')

FLAG_WORDS = {
    'peril': r"\b(seize|seized|seizes|seizing|pounce|pounced|swoop|swooped|spring upon|sprang upon|snare|snared|trap|trapped|captured|caught|carried off|carry off|combat|fight|fighting|fought|lose (his|her|their) life|eating (him|her|them|the young)|flesh|hounds|attack|attacked|sting|stung|claw|fell into|fall into|danger|enemy|enemies|hunger|famished|wrath|rage)\b",
    'death': r"\b(kill|kills|killed|killing|slain|slay|slew|dead|death|died|dies|die|dying|devour|devoured|devours|eaten|eat (him|her|them|you|me|it|up)|ate (him|her|them|it|up)|make a meal|tore (him|her|it|them)|tore (him|her|it|them)|torn|drown|drowned|perish|perished|strangle|strangled|hang|hanged|poison|poisoned|corpse|carcass|prey|bury|buried|grave)\b",
    'violence': r"\b(blood|bloody|beat|beaten|beating|whip|whipped|stab|stabbed|cut off|throat|knife|sword|spear|arrow|wound|wounded|bite|bit|gored|claws|teeth|stone(d|s) (him|her)|flog|flogged|cudgel|punish|punished)\b",
    'mature': r"\b(drunk|drunken|drunkard|wine|harlot|courtesan|adultery|mistress|lover|sweethearts?|wives|marry|married)\b",
}

def scan_flags(text):
    t = text.lower()
    return [f for f, rx in FLAG_WORDS.items() if re.search(rx, t)]

def level(flags):
    if not flags:
        return 'gentle'
    if set(flags) <= {'peril', 'scary', 'villain_dies'}:
        return 'classic'
    return 'all'

def entry(source, key, title, text, min_age, flags, edition, **kw):
    w = words(text)
    e = {'id': f"{source}-{key}", 'title': title, 'author': AUTHOR[source], 'source': source,
         'kind': kw.pop('kind', 'story'), 'text': text, 'first_line': first_line(text),
         'words': w, 'minutes': max(1, math.ceil(w / WPM)), 'min_age': min_age,
         'flags': sorted(set(flags)), 'level': level(flags), 'edition': edition}
    e.update(kw)
    return e

def slug(t):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t.lower().replace('’', '').replace("'", ''))).strip('-')

def build_grimm():
    L = lines_of('grimm')
    titles = list(C.GRIMM) + [t for (s, t) in C.EXCLUDED if s == 'grimm']
    start = idx(L, "THE RABBIT'S BRIDE", 270)
    end = next(i for i in range(start, len(L)) if L[i].startswith('____________________'))
    heads = find_heads(L, titles + ['THE WOLF AND THE SEVEN KIDS'], start, end)
    out = []
    for t, block in segment(L, heads, end):
        if ('grimm', t) in C.EXCLUDED:
            continue
        txt = clean(block)
        if t == 'HOW MRS. FOX MARRIED AGAIN':  # keep both versions under their own headings
            txt = txt.replace('FIRST VERSION.\n\n', 'First Version.\n\n', 1).replace('SECOND VERSION.\n\n', 'Second Version.\n\n', 1)
        age, flags = C.GRIMM[t]
        tt = title_case(t)
        out.append(entry('grimm', slug(tt), tt, txt, age, flags, SOURCES['grimm']['edition']))
    return out, heads

def build_andersen():
    out, allheads = [], []
    for key in ('andersen1', 'andersen2'):
        L = lines_of(key)
        body = idx(L, "HANS ANDERSEN'S FAIRY TALES", 140 if key == 'andersen1' else 150)
        end = max(i for i, l in enumerate(L) if l.strip() == 'NOTES')
        names = list(C.ANDERSEN) + list(C.ANDERSEN_SERIES) + [t for (s, t) in C.EXCLUDED if s == 'andersen']
        heads = find_heads(L, names, body, end)
        allheads += heads
        for t, block in segment(L, heads, end):
            if ('andersen', t) in C.EXCLUDED:
                continue
            if t in C.ANDERSEN_SERIES:
                out += build_series(t, block, SOURCES[key]['edition'])
                continue
            age, flags = C.ANDERSEN[t]
            tt = title_case(t)
            out.append(entry('andersen', slug(tt), tt, clean(block), age, flags, SOURCES[key]['edition']))
    L = lines_of('andersen3')
    s = idx(L, 'THE NIGHTINGALE', 1000); e = idx(L, 'THE REAL PRINCESS', s)
    age, flags = C.ANDERSEN['THE NIGHTINGALE']
    out.append(entry('andersen', 'the-nightingale', 'The Nightingale', clean(L[s + 1:e]), age, flags, SOURCES['andersen3']['edition']))
    allheads.append((s, 'THE NIGHTINGALE'))
    return out, allheads

def build_series(t, block, edition):
    S = C.ANDERSEN_SERIES[t]
    parts = S['parts']
    pos = [next(i for i, l in enumerate(block) if l.strip() == p) for p in parts]
    stitle = title_case(t.replace('OLE-LUK-OIE THE', 'OLE-LUK-OIE, THE'))
    sid = slug(stitle)
    out = []
    intro = block[:pos[0]]
    for n, p in enumerate(parts):
        seg = block[pos[n] + 1:(pos[n + 1] if n + 1 < len(parts) else len(block))]
        sub = ''
        # Snow Queen parts carry a subtitle line right after the heading
        k = next(i for i, l in enumerate(seg) if l.strip())
        if re.fullmatch(r"[A-Z ,.'’-]+", seg[k].strip()):
            sub = title_case(seg[k].strip()); seg = seg[k + 1:]
        if n == 0 and clean(intro):
            seg = intro + [''] + [''] + seg
            text = clean(intro) + '\n\n' + clean(seg[len(intro) + 2:])
        else:
            text = clean(seg)
        ptitle = title_case(p) + (f': {sub}' if sub else '')
        age, flags = S['tags'][p]
        out.append(entry('andersen', f'{sid}-{n + 1}', f'{stitle}, {ptitle}', text, age, flags, edition,
                         kind='part', series={'id': sid, 'title': stitle, 'part': n + 1, 'of': len(parts), 'part_title': ptitle}))
    return out

def build_kipling():
    L = lines_of('kipling')
    names = list(C.KIPLING) + [t for (s, t) in C.EXCLUDED if s == 'kipling']
    start = idx(L, 'HOW THE WHALE GOT HIS THROAT', 50)
    end = next(i for i, l in enumerate(L) if 'END OF THE PROJECT GUTENBERG' in l)
    heads = find_heads(L, names, start, end)
    out = []
    for t, block in segment(L, heads, end):
        if ('kipling', t) in C.EXCLUDED:
            continue
        age, flags = C.KIPLING[t]
        tt = title_case(t)
        out.append(entry('kipling', slug(tt), tt, clean(block), age, flags, SOURCES['kipling']['edition']))
    return out, heads

def build_aesop():
    L = lines_of('aesop')
    start = idx(L, 'The Lion And The Mouse', 800)
    end = idx(L, 'FOOTNOTES', start)
    heads = [start] + [i for i in range(start + 1, end) if L[i].strip() and not L[i - 1].strip() and not L[i - 2].strip()
                       and not L[i - 3].strip() and not L[i + 1].strip()]
    fables = []
    for n, i in enumerate(heads):
        j = heads[n + 1] if n + 1 < len(heads) else end
        t = title_case(L[i].strip())
        if t in C.AESOP_EXCLUDED:
            continue
        txt = clean(L[i + 1:j])
        flags = C.AESOP_OVERRIDES.get(t, scan_flags(txt))
        fables.append({'title': t, 'text': txt, 'flags': flags})
    # group into nights of four, fables of the same level together, in book order
    sets = []
    for lv in ('gentle', 'classic', 'all'):
        pool = [f for f in fables if level(f['flags']) == lv]
        groups = [pool[k:k + 4] for k in range(0, len(pool), 4)]
        if len(groups) > 1 and len(groups[-1]) == 1:  # never leave one fable alone
            last = groups.pop()
            groups[-1] = groups[-1] + last
        for grp in groups:
            flags = sorted({x for f in grp for x in f['flags']})
            names = [f['title'] for f in grp]
            title = 'Fables: ' + (', '.join(names[:-1]) + ' and ' + names[-1] if len(names) > 1 else names[0])
            text = '\n\n'.join(f"{f['title']}\n\n{f['text']}" for f in grp)
            e = entry('aesop', f'fables-{len(sets) + 1:03d}', title, text, 3 if level(flags) != 'all' else 6, flags, SOURCES['aesop']['edition'],
                      kind='fables', fables=[{'title': f['title'], 'text': f['text'], 'flags': f['flags']} for f in grp])
            e['first_line'] = first_line(grp[0]['text'])
            sets.append(e)
    return sets, fables

def order(groups_by_source):
    """Openers first, then a steady rotation so sources alternate. Series parts stay together."""
    ordered, used = [], set()
    allg = [g for gs in groups_by_source.values() for g in gs]
    for src, t in C.OPENERS:
        g = next(g for g in groups_by_source[src] if norm(g[0]['title']) == norm(title_case(t)))
        ordered.append(g); used.add(g[0]['id'])
    queues = {s: [g for g in gs if g[0]['id'] not in used] for s, gs in groups_by_source.items()}
    pattern = ['aesop', 'grimm', 'andersen', 'aesop', 'kipling', 'grimm', 'aesop', 'andersen']
    while any(queues.values()):
        for s in pattern:
            if queues[s]:
                ordered.append(queues[s].pop(0))
    out = []
    for g in ordered:
        out += g
    for n, e in enumerate(out, 1):
        e['order'] = n
    return out

def main():
    if '--fetch' in sys.argv:
        fetch()
    grimm, _ = build_grimm()
    andersen, _ = build_andersen()
    kipling, _ = build_kipling()
    aesop, fables = build_aesop()
    groups = {'grimm': [[e] for e in grimm], 'kipling': [[e] for e in kipling], 'aesop': [[e] for e in aesop], 'andersen': []}
    for e in andersen:
        if e.get('series') and e['series']['part'] > 1:
            groups['andersen'][-1].append(e)
        else:
            groups['andersen'].append([e])
    stories = order(groups)
    meta = {
        'name': 'Bedtime Story Night', 'version': 1, 'built': time.strftime('%Y-%m-%d'),
        'stories': len(stories), 'aesop_fables': len(fables), 'read_aloud_wpm': WPM,
        'levels': {'gentle': 'no flags', 'classic': 'only peril, scary, villain_dies', 'all': 'every story in the plan'},
        'age_bands': {'3': 'ages 3 to 5', '6': 'ages 6 to 8', '9': 'ages 9 to 12'},
        'flags': ['peril', 'scary', 'villain_dies', 'death', 'violence', 'sad', 'mature', 'dated'],
        'note': 'Story text is word for word from public-domain editions published before 1931.',
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({'meta': meta, 'stories': stories}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(len(stories), 'nights written to', OUT)

if __name__ == '__main__':
    main()
