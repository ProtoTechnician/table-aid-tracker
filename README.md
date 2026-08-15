<div align="center">
  <h1>Table Aid</h1>
  <h3>A Dungeon Master's screen that lives in one browser tab</h3>
  <p>
    <b>One HTML file</b> &nbsp;·&nbsp;
    <b>No install, no account, no internet</b> &nbsp;·&nbsp;
    <b>D&amp;D 2024 rules</b>
  </p>
  <p><i>You roll the dice. It does the arithmetic.</i></p>
</div>

![The fight screen](docs/figs/initiative.png)

Open it and it works. **Save** writes one JSON file holding the entire session; **Load** brings it
back. The campaign never leaves the machine it was written on — there is no server to go down, no
account to lose, and nothing that stops working when someone else's business plan changes.

It assumes a laptop is open in front of you while four people wait. Every decision follows from
that: the fight screen is dense because you *scan* it, the arithmetic is automatic because you
shouldn't be doing it in your head, and nothing rolls unless you ask it to.

---

## Two ways to fill one in

Type it yourself — every tab has an editor and nothing is locked. Or write your adventure as plain
text, hand it to Claude with [the build spec](pack/02_BUILD_SPEC.md), and paste back the JSON it
returns.

The second route carries a **provenance layer**, which is the part that makes handing your adventure
to a model safe. Everything Claude invented is outlined in red with a sentence explaining itself,
until you sign it off. Everything *you* wrote renders plain.

![A creature Claude invented, marked and explaining itself](docs/figs/provenance.png)

**How much you write is how much you get.** The same adventure from a two-sentence brief and from a
page of proper notes — same tool, same prompt:

| | Two sentences | A page of notes |
|---|---|---|
| Items in the build | 11 | 24 |
| **Marked as invented** | **11 of 11** | **4 of 24** |
| The ending | a placeholder | the author's |
| Time to review | the whole file | about four minutes |

The thin build isn't bad — it runs, and it's balanced. But you can't tell which parts are yours,
because none of them are.

---

## What's in the tool

### Story — chapters, key beats, and images for the table

![The Story tab with a segment open](docs/figs/story.png)

Segments live in chapters, so a long campaign folds away what it has already played. The bullets at
the top of each segment are what you read in three seconds while four people look at you. A session
clock tells you which scene you *should* be in. **⇩ Story PDF** prints the whole adventure as
something you can read the day before.

### Encounters — rated against your actual party

![The difficulty bar takes the colour of the band the fight lands in](docs/figs/budget.png)

The 2024 DMG XP budget, per character × party size, with no encounter multiplier. The bar takes the
colour of the band the fight lands in. Magic items widen the budget by an editable homebrew
percentage. Every fight can carry a battle map on a 5-foot grid.

### A second screen for the players

![A handout on the players' screen](docs/figs/player_handout.png)

**Players** opens a window for your other monitor: the battle map, a scene image, or a handout full
screen. The initiative order is **hidden from them by default** and turned on deliberately — and
even then they never see hit points, AC or stat blocks. Puzzles keep their solution on your screen
while the riddle is on theirs.

### And the rest

- **Area damage** in one pass — tick who's in the blast, mark who saved, it does the arithmetic and
  queues every concentration check.
- **118 creature templates** that rescale to any CR, with a warning when you push one outside the
  band where it still reads as itself.
- **Table numbers** on every foe, so the numbered die beside the model matches the screen.
- **Round timers**, lair actions, reaction dots, automatic start-of-combat and start-of-turn pop-ups.
- **Undo** twenty deep, an unsaved-work indicator, and optional timed backups.
- **Ctrl+K** jumps to anything. **Ctrl+Z** undoes anything.

---

## Start here

| | |
|---|---|
| **[`tracker/demo.html`](tracker/demo.html)** | A complete two-hour oneshot for four level-3 characters. Opens on a panel telling you what to press. **Open this first.** |
| **[`docs/Table_Aid_Manual.pdf`](docs/Table_Aid_Manual.pdf)** | 26 illustrated pages. Every tab, the encounter maths, the Claude workflow, and a "things that will bite you" section that doesn't oversell. |
| **[`tracker/table_aid_blank.html`](tracker/table_aid_blank.html)** | The empty tracker. This is the product. |

> **Save before closing the tab.** There is no autosave — browser storage isn't available to a file
> opened this way, and pretending otherwise would be worse than saying so.

---

## Repository layout

```
tracker/    table_aid_blank.html · demo.html
docs/       the manual (PDF + source), DESIGN.md, and the screenshots above
pack/       what a DM puts in their Claude project — prompt, guide, build spec,
            template, a worked example build, and the same contract as a skill
examples/   the demo printed as a story PDF, and as a Word review copy with a
            comment on every invented passage
build/      the scripts that generate everything above
```

`docs/DESIGN.md` is the one to read before changing anything. It records *why* the tool is shaped
the way it is, including several constraints that were learned expensively:

- **One file, zero dependencies.** No build step, no CDN, no internet at runtime.
- **Never `alert()`, `confirm()` or `prompt()`.** A sandboxed frame ignores them *silently*, so the
  feature doesn't error — it just looks broken.
- **No browser storage.** Persistence is an explicit Save that downloads a file.
- **Never re-render a container while the user is typing in it.**
- **All content lives on `S.data`**, not in the constants; the constants are only the first-run seed.
- **Never reproduce official stat blocks, spell text or rules text.**

Build instructions, including the one awkward dependency, are in [`build/README.md`](build/README.md).

---

## Licence

[**PolyForm Noncommercial 1.0.0**](https://polyformproject.org/licenses/noncommercial/1.0.0) — see
[`LICENSE`](LICENSE).

Use it, change it, share it, run it at your table, hand it to your group. Do anything you like with
it that isn't commercial. **Commercial rights are reserved**, so nobody can bundle this into
something they charge for.

An unofficial fan tool with no affiliation to Wizards of the Coast, reproducing no official stat
blocks, spell text or rules text — see [`NOTICE.md`](NOTICE.md).
