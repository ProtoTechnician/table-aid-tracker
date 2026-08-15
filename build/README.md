# Build

Everything in `tracker/` and `docs/` is generated. Run in this order.

| Script | Reads | Writes |
|---|---|---|
| `make_blank.py` | `$TABLE_AID_SOURCE` (a filled tracker) | `tracker/table_aid_blank.html` |
| `demo_art.py` | nothing | `build/art/*.svg` — the demo's scene plates |
| `demo_build.py` | the blank + `demo_art` | `tracker/demo.html` |
| `manual_shots.py` | `tracker/demo.html` | `docs/figs/*.png` |
| `thin_shots.py` | the blank | `docs/figs/thin_story.png` |
| `build_manual.py` | `docs/Table_Aid_Manual.md` + `docs/figs/` | `docs/Table_Aid_Manual.pdf` |
| `check.sh <file>` | any tracker HTML | pass/fail on its script blocks |

## Requirements

```
python3.11+
pip install playwright markdown --break-system-packages
playwright install chromium     # or set PLAYWRIGHT_BROWSERS_PATH if you already have one
```

## `make_blank.py` needs a source

It empties a **filled** tracker rather than building an empty one from nothing — the layout, the
creature templates and all the behaviour live in that file. The source is a personal campaign build
kept outside this repository:

```bash
TABLE_AID_SOURCE=/path/to/abyss_tracker.html python3 build/make_blank.py
```

If the script reports misses, one of its anchor strings has drifted — the tracker's HTML changed
under it. Fix the anchor rather than the output; the whole point is that the two files stay in step.

## Testing

There is no test suite. What there is:

- `check.sh` extracts every `<script>` block and runs `node --check` over it. Run it after any edit.
- The tracker must be tested **inside a sandboxed iframe**, not just opened as a file — native
  dialogs and pop-ups fail silently there and that is where the bugs hide. See `docs/DESIGN.md` §2.
- After changing the tracker, regenerate the blank and the demo and click through every tab. Console
  errors are the signal; the UI often looks fine while something is broken underneath.
