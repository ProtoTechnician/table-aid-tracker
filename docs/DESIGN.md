# DM AID — BUILD SPEC & PREFERENCES
### Mejdy's table tooling · v2.2 · derived from *The Ninth Step* (Abyss Table) and the Table Aid generalisation

> **How to use this file.** Hand it to Claude at the start of any new oneshot or campaign prep,
> with a line like *"build me the DM aid the way this spec describes, for <campaign>."*
> Everything below is a decision already made and tested at the table — it does not need
> re-litigating. Only the **§9 Content slots** change from campaign to campaign.
>
> **v2 changes:** the tool is now fully editable in the browser, ships with 118 scalable creature
> templates, six colour themes and a light mode, and carries a **provenance layer** (§13) so anything
> Claude invented is visibly marked. The run sheet became **Story**, with chapters and key beats.
> The campaign-mechanic tab became **Tools** and gained a full dice roller.
>
> **v2.1 adds:** undo, an unsaved-work indicator and optional auto-backups (§7); area damage,
> round timers, lair actions and reaction dots on the fight screen (§4); a **player-facing second
> window** driven by handouts and puzzles kept in Tools (§14); Ctrl+K jump-to-anything; a markdown
> recap export; and a segment can carry the fight that happens in it.
> **Table mode was tried and dropped** — Ctrl+scroll already does it better.
>
> **v2.2 adds:** a **table number** on every foe so a numbered die can stand next to any model (§4);
> the player screen's initiative order is **hidden by default** and toggled on deliberately (§14);
> **images per story segment**, thrown onto the player screen from the segment itself (§14);
> and handout text expands in place rather than truncating.

---

## 1. WHAT THE DELIVERABLE IS

Two artefacts per campaign, always:

| Artefact | Format | Purpose |
|---|---|---|
| **The tool** | One self-contained `.html` file | Live use at the table, open in a browser tab |
| **The run sheet** | `.pdf` (built from a `.md` source) | Read-ahead prep, one scene per page |

The `.md` source of the run sheet is kept too, because it is the thing that gets edited;
the PDF is regenerated from it. **Deliver the PDF, not just the markdown** — markdown is
awkward to read in a second tab.

A third artefact exists for other people's campaigns: a **build JSON** (`{"tableAidBuild":1,"data":{…}}`)
that pastes into a blank tracker. See §13 and `11_Table_Aid_Build_Spec_Provenance.md`.

Two more exist for reading and reviewing away from the screen: the **story PDF** (Story → ⇩ Story PDF
in the tracker) and a **Word review copy** with a comment on every invented passage, which the author
marks up and hands back for a fresh build.

> **The marketing website is finished and frozen.** `site/` and `table-aid-website.zip` were built
> once and are no longer maintained. Do not regenerate, re-link or re-zip them when the tracker,
> the manual or the demo changes — Mejdy asked for this explicitly. The live deliverables are the
> tracker, the blank, the demo, the manual PDF and the authoring pack.

---

## 2. HARD CONSTRAINTS *(these were learned the painful way — do not skip)*

1. **One file, zero dependencies.** No build step, no npm, no CDN, no internet at runtime.
   Everything inline in a single `.html`. It has to work in a hotel with no wifi.
2. **NEVER use `alert()`, `confirm()`, or `prompt()`.** The preview frame is sandboxed
   without `allow-modals`, so the browser *silently ignores* them — `confirm()` returns
   `false` and the feature just looks broken. Use the toast + two-step arm patterns in §6.
3. **No `localStorage` / `sessionStorage`.** Not available. Persistence is an explicit
   **Save** button that downloads a JSON of the whole state object, and a **Load** button
   that restores it. Everything the DM types must live on that one state object.
4. **Never re-render a container while the user is typing inside it.** Rebuilding
   `innerHTML` destroys the focused input and eats the keystroke. Build once, then patch
   only the readout nodes. Use `oninput` → patch; use `onchange` → full re-render is fine.
5. **Everything is keyboard-reachable for the common case.** Typing a number and pressing
   Enter must be enough; the mouse is for the rare case.
6. **All content lives on `S.data`, not in constants.** The constants at the top of the file are
   only the first-run seed. Every tab reads through the accessors (`MON()`, `ENC()`, `SC()`,
   `CH()`, `TOOLS()`) so everything stays editable and saveable.

---

## 3. TAB STRUCTURE

Six tabs, in this order, never merged. The split *is* the design — resist adding a seventh.

| Tab | Holds | Notes |
|---|---|---|
| **Initiative** | The live combat list | The only screen open during a fight |
| **Party** | One card per PC | Sheet-adjacent; HP, slots, ability uses, conditions |
| **Bestiary** | Stat blocks, foes red and NPCs green | Searchable, editable, `+ Initiative` per block |
| **Encounters** | Preset fights | One-click load into initiative, live XP budget bar, battle map |
| **Story** | Chapters of scene segments | Key beats, notes, session-clock pacing |
| **Tools** | Dice roller + campaign-wide mechanics + handouts and puzzles | See §8 and §14 |

Header bar (always visible): brand (name · subtitle · LV/party badge) · tabs · **session clock** ·
Start/Pause · Reset · Dice · **Undo** · Save · Load · **save-age pill** · **Players** ·
provenance pill · dark/light/system · **⋮ options**.

---

## 4. LAYOUT RULES

### The golden rule
**One visible control per concept per row. Everything else goes in a dropdown tray.**
When a feature needs more than one new button on the initiative row, it belongs in the tray
instead. Row density is the whole point of the initiative tab.

### Initiative row grid
```
60px            init (editable)
minmax(160,1fr) ▶ chevron + name + meta line
136px           damage input flanked by − / + , HP number, HP bar
minmax(160,.62) active condition chips + "+ condition…" select
132px           CONCENTRATING toggle
60px            TEMP HP
42px            ✕ remove
```
- Row colour-coded by a 3px left border: PC = teal, ally = green, foe = red.
- Active turn: amber border + lighter background.
- At 0 HP: 42% opacity.
- Meta line under the name carries the low-priority numbers as text, never buttons:
  `AC 17 · CR 5 · +9 temp · LEG 3/3 · RES 1/3 · reaction used · Bless 3r`.
- A **reaction dot** sits next to the name: click when the creature spends its reaction, and it
  clears itself automatically at the start of that creature's turn.
- **Lair actions** are a slim row pinned at initiative 20 with an editable description and no HP.
- **Area damage** (initiative bar, or the `a` key) opens one pass over every combatant: tick who is
  in it, mark failed / saved / no effect per creature, and it applies full, half or none, eats
  temporary hit points first, and queues one concentration check per concentrating creature hit.
- **Round timers** sit above the list as chips. They count down at the top of each round and announce
  themselves when they expire. Optionally tied to a creature, in which case they also show on its row.
- **Table numbers.** Every foe gets `#1`, `#2`, `#3`… in the order it entered the fight, shown as an amber
  chip beside its name and click-to-edit. This exists because the models on the table are whatever is in
  the box, not what the stat block says: the DM puts a numbered die next to each model and reads the number
  off the screen. **Numbers are never reused when a creature dies or is removed** — the die on the table
  does not move. Numbering restarts at 1 when an encounter is loaded, because the foes are all replaced.

### The tray (the `▶` expander)
Appears only for creatures that have something to track. Sections in this fixed order:

1. **Spell slots** — pips per level, click to burn, click again to refund
2. **Spells** — name · level tag · casting meta · one-line paraphrased effect · `cast` button
3. **Legendary** — Legendary Resistance pips, Legendary Actions pips + `refill` button,
   with that creature's legendary action menu written out underneath
4. **Limited uses** — anything finite: X/day pips, once-per-fight ticks, `roll d6` for recharge

---

## 5. VISUAL SYSTEM

```css
--bg:#0c0f13   --surface:#141a21  --surface2:#1b232c  --line:#27313c
--ink:#e9edf2  --muted:#8b98a6    --dim:#5d6a78
--teal:#5fb3c4 --teal-d:#25505c   /* structure, PCs, "safe" */
--amber:#d99a4e --amber-d:#5c421d /* the active thing, the clock, legendary */
--red:#d4636c  --red-d:#5a2429    /* foes, danger, destructive, Claude's additions */
--green:#6dbd8a                   /* allies, success, HP healthy */
--violet:#9a83d6                  /* temp HP */
```
- **Dark by default** — it is read in a dim room. Light and system modes exist and are selected
  from the header segment; every colour must go through a CSS custom property so they work.
- Six themes ship: `abyss` (teal/amber), `ember`, `verdant`, `violet`, `slate`, `ash`.
  Background colour, accent and highlight are individually overridable, plus a background image
  with an opacity slider (downscaled to 1600px and stored in the save file).
- All numbers in a mono face; all prose in the system sans.
- Section labels: 9–10px, uppercase, `letter-spacing:.13em`, colour `--dim`.
- Border radius 6–8px. Cards get 1px `--line`; accented cards get a 3px coloured left border.
- **Big things are the things you scan for**: HP totals, the clock, the save DC, the dice total.
  Small things are labels.
- **Editable fields must be visibly editable.** Inputs get `--field2` backgrounds, a real border
  and a teal focus ring — never near-invisible text on near-identical background.

---

## 6. INTERACTION PATTERNS *(reuse these verbatim)*

| Pattern | Where it's used | Behaviour |
|---|---|---|
| **Toast** | Every confirmation | Bottom-centre, fades after ~2.8s, accepts inline HTML |
| **Two-step arm** | Reset, Clear, Delete anything | 1st click → button turns red and reads *Sure?*; 2nd click fires; auto-disarms after 3s |
| **Inline number entry** | Damage/heal, both tabs | Small input between − / + ; **Enter = damage, Shift+Enter = heal**; focus restored after the re-render |
| **Hover stat card** | Initiative rows, bestiary, template picker | Full block on hover, anchored *below or above the row so it never covers it*; click to pin; Esc releases; hides when the cursor moves onto a tray |
| **Accordion** | Story chapters and segments, initiative trays | Chevron ▶/▼; expanding never loses typed notes; tick-boxes are independent of the expander |
| **Pips** | Slots, uses, legendary, death saves | Round = spell slot / resistance, square = ability use; click index *i* sets used to *i+1*, clicking an already-used pip refunds down to *i* |
| **Modal** | HP roll sheet, concentration check, every editor | Centred, backdrop click closes, Esc closes, built once then patched |
| **⋯ dots menu** | Every card — creature, encounter, segment, chapter, mechanic | Edit · Duplicate · Move up · Move down · Delete. Parent must be `overflow:visible` or the menu clips |
| **⋮ library & syntax** | Every freeform field in an editor | Opens a picker of common entries plus an in-depth syntax guide; inserts by appending, never by replacing |
| **Trigger pop-up** | Start of combat, start of a creature's turn | Fires automatically; `auto` kind gets an Apply button, `roll` prompts a roll, `rem` is a reminder |

---

## 7. UTILITIES THAT MUST BE PRESENT

- **Session clock** — H:MM:SS. Start/Pause, **±5 min nudges**, **Reset (two-step)**, and
  **click the readout to type a time**. Accepted formats: `1:23:45` = h:m:s, `2:15` = 2h15m
  (matches how the run sheet writes times), bare `90` = 90 minutes. Pauses while editing.
- **Pace readout** — compares the clock to the story segment times and says which scene
  you *should* be in and how many you're ahead/behind. This is the single most useful thing
  in the tool for a timed oneshot.
- **Dice roller, two of them.** A floating quick panel (header **Dice** button, or press **R**),
  and a full roller at the top of Tools: `2d6+1d4+3`, `4d6kh3`, advantage/disadvantage over the whole
  expression, every die shown individually with max faces green / natural 1s red / dropped dice
  struck through, and a log of the last sixteen rolls. Physical dice are still the default at this
  table, so **any tool that needs a roll must also accept a typed value**.
- **Concentration checker** — fires automatically when a creature flagged CONCENTRATING
  takes damage. Shows **Damage · Save DC (= max(10, ⌊dmg÷2⌋)) · Needs a X+**, takes the
  DM's physical d20 as typed input, adds the creature's stored CON save modifier, prints
  `roll + mod = total vs DC`, and sets or clears the CONCENTRATING light on Apply.
  Force hold / Force break overrides. Drops to 0 HP end it with no save.
- **Condition hover cards** — hovering any condition chip shows what it does, what saves against it
  and when, in 2024 wording.
- **HP roll sheet** — opened by clicking a PC's HP bar. One row per level, level 1 = max die
  by default, per-row roll button, bulk *roll all empty / reroll / average / clear*,
  bonus-per-level and flat-bonus fields, running total column, grand total, and a
  "the average build would be N — you're X up/down" line. Applies the minimum 1 HP per level,
  and the number of filled rows drives the character's displayed level.
- **Creature template library** — `+ New creature` opens 118 archetypes in 15 categories with a
  CR scaling engine: AC, HP, hit dice, attack bonus, save DC and damage all rescale to a target CR,
  and creatures gain extra attacks as CR rises so the dice stay readable. Each template carries a
  **CR band** and warns when you push it outside the range where it still reads as itself.
  Hovering a template shows the finished block before committing.
- **Encounter builder** — add creatures from a dropdown, difficulty recalculates live.
- **Save / Load / Paste** — one JSON containing state for every tab, including story notes,
  segment time stamps, and the clock. Paste-a-build in Options offers **Replace everything** or
  **Merge into what I have** (creature names are the join key; a name that already exists is kept,
  not overwritten; chapter ids are remapped).
- **Undo, 20 deep** — Ctrl+Z, a header button, and an Undo button on the toast that follows anything
  destructive. Snapshots go in before deletes, clears, damage, rests, loads and merges — not on
  keystrokes. The background image is stripped from snapshots and carried across, or the stack eats
  megabytes. The session clock is never rolled back by an undo.
- **Save-age pill** next to Load: "saved 3m ago" green, "unsaved 7m" amber, red past fifteen, plus a
  `beforeunload` guard. Optional auto-backup writes a timestamped JSON to downloads every 10/15/30
  minutes; off by default because the browser prompts about repeated downloads.
- **Ctrl+K palette** — one search across creatures, fights, segments, mechanics, conditions, spells,
  anything currently in the initiative order, and handouts. Enter jumps there; for a handout, Enter
  puts it straight on the players' screen.
- **Recap export** — Story tab → *⇩ Recap* writes the session as markdown: chapters, segments, what
  time each actually ran, the notes typed during play, and where the party ended. This is the input
  the Session Log doc wants.
- **Encounter XP budget bars** — every fight shows its XP against the party's Low / Moderate / High
  thresholds. **Solid fill in the band's colour** — blue (below Low) → green (Moderate) → amber →
  red (High) — not a gradient; the whole bar takes the tier's colour so it reads at a glance.

---

## 8. THE TOOLS TAB

Formerly the campaign-mechanic tab. It holds the dice roller and **any number of** campaign-wide
mechanics — the homebrew rules that make it that campaign. In *The Ninth Step* that was the Curse
of Ascension. The shape is reusable and fully editable in the browser:

1. A one-line statement of the rule in a coloured callout at the top
2. A **quick resolver** — dropdowns/inputs for the situation → it prints the DC, how many
   saves, and what success/failure does, with a button to roll it
3. The full rules table (pipe-separated in the editor, headers on the first line)
4. Any associated random table with a roll button
5. Free-text note panels beside it — including the legitimate ways to cheat the rule

If a campaign has no such mechanic, leave it empty rather than inventing one, or use it as a
**Rulings** log: a running list of ad-hoc calls made at the table, so future rulings stay consistent.

---

## 9. CONTENT SLOTS *(the only part that changes per campaign)*

Fill these; everything else is already decided. Field-by-field detail lives in
`11_Table_Aid_Build_Spec_Provenance.md`.

```js
MONSTERS   [{ n, t, cr, xp, ac, hp, hd, dex, sp, ab:[6], conSv, grp, side, legRes, legAct, lines:[] }]
CARDS      [{ id, name, img, text, dm }]   // handouts & puzzles — text is player-facing, dm never is
SCENES     [{ ch, a, b, t, note, keys:[], imgs:[{n,u}], enc }]
KITS       { "<monster name>": { dc, slots:{lvl:count},
               spells:[{ n, lv, per?, t, d }],
               uses:[{ n, max, note }] } }
TRIG       { "<monster name>": { combat:[{n,w,k}], turn:[{n,w,k,heal}] } }
ENCOUNTERS [{ n, loc, note, m:[["<monster name>", qty]] }]
MAPS       { <enc index>: { t, scale, draw, rows:[], tok:[{x,y,l,s,n}] } }
CHAPTERS   [{ id, name, sub, open }]
SCENES     [{ ch, a:"0:00", b:"0:30", t:"Title", note:"…", keys:["…"] }]
TOOLS      the §8 table + resolver, one entry per mechanic
PARTY      { size, level, items:{rarity:count} }
```

### Content rules
- **2024 rules by default.** Where 2014 and 2024 differ in a way that matters, say so.
- **Never reproduce official text verbatim.** Spell and rule effects are one-line
  paraphrases with a note to check the PHB for exact dice and ranges.
- **Homebrew is labelled homebrew**, always.
- Spells chosen for a stat block must be *characterful first* — the spell should explain
  something about who the creature is, not just add damage. (Silence for the Silence-Warden;
  Detect Thoughts as the in-world reason the Auger predicts you; Divine Word for the woman
  called the First Silence.)
- Every creature's `conSv` must be filled in, because the concentration checker uses it.
- Every creature needs a `side` — `foe` or `ally`. Rescuable NPCs are `ally` and get green cards.
- Signature homebrew attacks get an explicit spell-slot cost where sensible
  (Closing Verse = a 3rd-level slot).
- **Key beats on every segment.** 4–8 fragments about what actually happens: the interaction,
  the decision, the line to say out loud, the thing to plant now that pays off later. `★` marks
  the pivotal ones. These are read in three seconds mid-scene — they are not a prose summary.

### Encounter maths
2024 DMG XP budget: per-character threshold × party size, **no encounter multiplier**.
For four level-10 characters: Low 6,400 · Moderate 9,200 · High 12,400.
Magic items add a homebrew uplift per item (common 2% · uncommon 5% · rare 10% · very rare 18% ·
legendary 30% · artifact 50%, capped at +200%), editable in Options. XP is entered **per creature**,
never per encounter.

---

## 10. RUN SHEET (PDF) SPEC

Built by: markdown → styled HTML → Chromium print-to-PDF. A4, 16/15/18mm margins.

- **Cover page**: kicker, huge title, rule, subtitle, party/level/depth line, and the
  one-sentence premise in an italic bordered block.
- `page-break-before: always` on every `h2` → **one scene per page**. The wasted whitespace
  is worth it; you never flip pages mid-encounter.
- **Read-aloud blocks** are tinted, left-bordered, italic; the "READ ALOUD:" cue renders as
  small-caps uppercase inside them.
- Stat-block headers get an amber left border and a tinted background.
- Tables: dark header band, striped rows, `page-break-inside: avoid`.
- Running header (title left, campaign meta right) and centred `page / total` footer.
- Serif body at ~9.9pt — it is read, not skimmed.

### Run sheet document structure
`Six-hour spine table` → `the campaign mechanic` → one `##` section per scene, each with
read-aloud text, stat blocks, and a **DM notes / contingencies** section → a final
one-page quick reference with every DC and XP total in the session.

---

## 11. NEW-BUILD CHECKLIST

- [ ] Ask: party size, level, session length, ruleset, magic items, and the one homebrew mechanic
- [ ] Write the run sheet markdown first — the tool's content comes out of it
- [ ] Verify encounter XP against the **2024** DMG budget for the real party
- [ ] Fill MONSTERS + KITS + TRIG (with `conSv` and `side` on every entry)
- [ ] Write key beats for every segment, and group segments into chapters
- [ ] Build the HTML, then **test it inside a sandboxed iframe**, not just a plain file open
- [ ] Confirm: no native dialogs, no storage APIs, no focus loss while typing, no console errors
- [ ] Regenerate the blank template from the campaign build so the two stay in sync
- [ ] Generate the PDF, eyeball pages 1, middle, and last
- [ ] Deliver both, and save the spec + run sheet to the project

---

## 12. DECISION LOG *(why things are the way they are)*

| Decision | Reason |
|---|---|
| Six separate tabs, never merged | The split is what keeps the fight screen usable |
| Trays instead of more row buttons | Row density; the fight screen must stay scannable |
| Two-step confirms instead of dialogs | Native dialogs are silently blocked in the frame |
| Typed d20 input everywhere a roll happens | This table rolls physical dice; the tool does the arithmetic, not the randomness |
| Stat card anchors to the row, not the cursor | It kept covering the HP controls of the creature being looked up |
| Legendary counters moved off the row into the tray | Two fewer buttons; the counts survive as text in the meta line |
| Level 1 = max hit die, rolls typed in | This table rolls HP per level and wants the running total visible |
| Pace readout instead of a plain timer | A 6-hour oneshot fails on pacing, not on content |
| Scene notes live per-segment, not in one blob | Notes are written mid-scene and read back per scene |
| Chapters above segments | A campaign needs to fold away what it has already played; a oneshot just has one |
| Key beats separate from the prep note | The prep note is one line you hold; the beats are the scan-in-three-seconds summary |
| Solid tier colour on the XP bar, not a gradient | You read the band, not the position |
| Content moved out of constants into `S.data` | Everything had to become editable without a rebuild |
| Templates carry a CR band | A dragon cannot be CR 2 and stay a dragon; warn rather than silently obey |
| Build JSON rather than a whole HTML file | 250 KB does not travel through a chat; JSON does, and it survives tool updates |
| Undo instead of confirmation dialogs everywhere | Confirmations slow down the ninety-nine correct clicks to protect the one wrong one |
| The player window is a pop-up, never the default | It is a second monitor feature; it must cost nothing when there is only one screen |
| Handouts hold the solution next to the player text | The DM reads the answer off their screen while the table reads the puzzle off theirs |
| Table mode built, then removed | Ctrl+scroll already does it, and better |
| Foes carry a table number, not just a name suffix | The miniatures at this table are whatever is in the box; a numbered die is the join between model and stat block |
| Table numbers are never recycled | Recycling would mean walking round the table moving dice mid-fight |
| The player screen hides initiative unless told otherwise | Turn order is the DM's to give away |
| Long handout text expands in place | Truncating it forced a trip through the editor to read the solution |

---

## 13. PROVENANCE — marking what Claude added

Any creature, encounter, segment or mechanic may carry:

```js
ai: true,        // Claude invented this entry
aiOk: false,     // the author has not accepted it yet
aiNote: "Statted at CR 5 — you named them and said 'tough but not elite', so every number here is mine."
```

Marked entries render with a red rail, the note, and a **✓ That's fine** button that clears that one.
A global switch in Options hides every mark at once; a header pill counts what is still unreviewed.
Notes are one sentence and start with a verb: **Invented · Statted · Scaled · Filled in · Balanced ·
Guessed · Split · Added.**

Two failure modes, both worse than a rough stat block:
- **Unmarked invention** — putting words in the author's mouth.
- **Marking their own writing** — insulting, and it makes the whole layer noise.

The full contract, including what does and does not get marked, is
`11_Table_Aid_Build_Spec_Provenance.md`. The author-facing explanation is
`10_Table_Aid_Authoring_Guide.md`, and `12_Adventure_Intake_Template.md` is the form to hand
someone who has an idea but no notes.

---

---

## 14. THE PLAYERS' SCREEN

**Players** in the header opens a second browser window (a pop-up — fail gracefully with a toast if it
is blocked) that the DM drags onto the other monitor. Closing it costs nothing; the main tool behaves
identically whether it is open or not. It shows exactly one of three things, chosen from the main window:

1. **The battle map** of the last-loaded encounter, full width.
2. **A handout** — full screen: image, text, nothing else. Serif, large, centred.
3. **A scene image** — anything attached to a story segment.
4. **Blank** — for when they should be looking at the DM.

**The initiative order is hidden by default** and appears beside the map only when the DM ticks
*show them the initiative order*. When shown it carries names, table numbers, conditions and whose turn
it is — never hit points, AC or stat blocks. Default-secret is the correct default: knowing the turn
order is information the DM chooses to give away, not the tool's to leak.

**Images live on the segment, not in a separate library.** A scene carries `imgs: [{n, u}]` where `u` is a
URL or an uploaded data URL (downscaled to 1600px). They render as thumbnails inside the open segment and
one click throws one onto the player window, with the live one ringed in green. Ctrl+K finds them by name.

Handouts live at the bottom of Tools as `CARDS`. Each holds `name` (DM label), `img` (URL or an
uploaded image downscaled to 1600px), `text` (what the players read) and `dm` (the solution, never
displayed). **Every puzzle in a campaign should exist as a card** — the split between the riddle and
its answer is the whole point.

Repaints are signature-guarded: the order-of-battle view redraws on every initiative render, a static
handout does not.

---

*Generated from the Abyss Table build for **The Ninth Step**, generalised into Table Aid. If a future
build contradicts something here, the newer table experience wins — update this file rather than
working around it.*
