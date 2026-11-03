# Bedtime Story Night

199 nights of public-domain bedtime stories for the 🌙 Bedtime Story Night Grok Bot template by Omega Games: Aesop's fables (four to a night), fairy tales from the Brothers Grimm and Hans Christian Andersen, and Kipling's Just So Stories. Every story is word for word from an edition published before 1931, tagged with reading time, a youngest age band and gentle or scary flags, so a parent can choose gentle stories only.

## Quick start

```
curl -sO https://raw.githubusercontent.com/Play-Omega-Games/bedtime-story-night/main/plans/stories.json
python3 scripts/build.py --fetch
python3 tests/test_plan.py
python3 scripts/check_links.py
```

A bot loads the plan from `https://raw.githubusercontent.com/Play-Omega-Games/bedtime-story-night/main/plans/stories.json`. If that fails, it downloads `scripts/build.py` and `scripts/curation.py` and rebuilds the plan from the public sources.

## Plan format

`plans/stories.json` has `meta` and `stories`, in reading order. Each story: `id`, `order`, `title`, `author`, `source`, `kind` (`story`, `part` or `fables`), `text`, `first_line`, `words`, `minutes` (read aloud at 150 words a minute), `min_age` (3, 6 or 9), `flags`, `level` and `edition`. Fable nights also carry `fables` (each with `title`, `text` and `flags`). Parts of a longer tale carry `series` (`id`, `title`, `part`, `of`, `part_title`).

Flags: `peril`, `scary`, `villain_dies`, `death`, `violence`, `sad`, `mature`, `dated`. Levels: `gentle` (no flags), `classic` (only peril, scary or villain_dies) and `all`.

Some tales never enter the plan at any setting, such as The Little Match Girl, The Red Shoes, The Juniper Tree and The Robber Bridegroom.

## Files

- `plans/stories.json`: the plan.
- `scripts/build.py`: `python3 scripts/build.py --fetch` downloads the sources into `./src` and rebuilds the plan (standard library only).
- `scripts/curation.py`: the age bands, flags and exclusions.
- `scripts/check_links.py`: checks every source live and finds every paragraph in it.
- `tests/test_plan.py`: offline checks, including a word-for-word check when `./src` is present.
- `scripts/make_manifest.py` and `MANIFEST.txt`: every file with its size and SHA-256, for loading by raw URL.

## License

The plan is CC0 1.0. Code is MIT. See `LICENSE`. Every story was published before 1931 and is in the public domain in the United States.

Questions or ideas? Contact Omega Games at john@playomega.games.
