# TABLE AID — AUTHORING GUIDE
### Write your adventure in plain text. Get back a tracker with the boring parts already done.

> **The short version.** Start a Claude chat. Attach `02_BUILD_SPEC.md`. Paste the prompt from
> `00_PROMPT.md`, then your adventure. Claude hands you a block of JSON. Open the tracker,
> **⋮ top right → Paste a build from Claude → Load this build.** Everything Claude invented is
> outlined in red with a note saying why. Tick off what you're happy with. Save.
>
> You can also just open the tracker and type it all in yourself — every tab has an editor.
> This is the shortcut, not the requirement.

---

## 1. WHAT THE TOOL IS

One self-contained HTML file. No install, no account, no internet. Open it in a browser tab and it
works. **Save** downloads one JSON file holding everything; **Load** brings it back. Your campaign
never leaves your machine.

| Tab | What lives there |
|---|---|
| **Initiative** | The live combat screen. Pulls everything from the other tabs. |
| **Party** | One card per PC — HP, spell slots, ability uses, conditions, death saves |
| **Bestiary** | Every creature. Foes get red cards, NPCs get green ones. |
| **Encounters** | Preset fights that load into initiative in one click, with a live difficulty rating and a battle map |
| **Story** | Chapters of segments, with key beats, a session clock and a pacing readout |
| **Tools** | A dice roller, your campaign's homebrew mechanics, and the handouts and puzzles you put on the players' screen |

---

## 2. WRITE IT HOWEVER YOU LIKE

You do **not** need to format your adventure. Prose is fine. A messy outline is fine.
`03_ADVENTURE_TEMPLATE.md` is a form you can fill in if a blank page is worse than a questionnaire.

### The minimum

1. **Party** — how many players, what level, which ruleset.
2. **Your scenes in order**, with rough times if you care about pacing.
3. **Who they fight**, and roughly how tough each thing is.

### What makes a great build

**Key beats.** The single highest-value thing you can write. For each scene, three to eight
fragments about what actually *happens* — who they talk to, the decision they face, the line you
must remember to say, the thing you're planting now that pays off in two hours. These become
bullets you read in three seconds while four people stare at you. Write them yourself and they go
in as yours; leave them out and Claude writes them from your prose and marks them red.

**Constitution saves.** The one number people forget. The tracker runs concentration checks off it,
so every creature that can concentrate needs one.

**Flag your NPCs.** Anything the party might rescue, hire, escort or talk to. They get green cards
and are treated as allies everywhere.

**Say what fires automatically.** "Regenerates at the start of its turn." "The aura applies before
initiative." "Recharges on 5–6." Those become pop-ups at the right moment, which is the whole
difference between remembering regeneration and not.

**Describe your battlefields in a sentence.** "A ledge with a chasm down the middle and a rope
bridge at the north end" becomes a grid map you can copy onto the table.

**Name your homebrew rule** and give its table. Curses, madness, corruption, heat, supply, doom
clocks — anything with tiers and a save becomes a resolver that does the arithmetic mid-session.

**Say what you haven't decided.** Claude asks about those instead of guessing, which is what you
want: a wrong guess about your ending is far worse than a question.

---

## 2b. A NOTE ON SETTING CLAUDE UP

Put `02_BUILD_SPEC.md` in a Claude **Project**, and put the non-negotiable rules in the
**Project instructions** as well — instructions are always in context, whereas project documents get
*searched* rather than read once a project outgrows the context window, and that behaviour cannot be
switched off. The manual's §11 has the exact block to paste.

**Keep the Claude project lean.** The authoring pack is about eleven thousand tokens and will never
trigger that on its own; a project stuffed with campaign bibles and session logs will. Those belong
in a different project.

If you are unsure the spec landed, ask before you build: *"what are the three provenance fields, and
what does each one mean?"* If the answer is not `ai`, `aiOk` and `aiNote`, paste the spec into the
chat directly.

---

## 3. THE PROVENANCE SYSTEM — seeing Claude's work

This is the part that makes handing your adventure to a model safe.

Every creature, encounter, segment and mechanic that **Claude invented** carries a red rail, a short
note saying what it did and why, and a **✓ That's fine** button. Everything **you** wrote renders
plain. So the first thing you see when a build loads is exactly where the machine put its hands.

- **⋮ top right → What Claude added** — a global switch. Turn the marks off and you have a clean
  tracker; turn them back on any time, even mid-session.
- **✓ That's fine** on any card clears that one mark.
- **Accept everything** clears the lot when you've read them.
- **Flag it all again** brings them back, which is useful after Claude edits your file a second time.
- **The header pill is a walk, not a counter.** Click it and it takes you to the next unreviewed
  item — switching tab, opening the right chapter, scrolling to the card. Click again for the next.

The notes are meant to be argued with. `"Statted at CR 5 — you named the Zealots and said 'tough but
not elite', so every number here is mine"` is an invitation to change the numbers, not a disclaimer.

---

## 4. CHAPTERS, KEY BEATS AND THE COMBAT SCREEN

**Chapters** group segments in the Story tab. A oneshot has one. A campaign gets one per session or
one per act, and you fold the finished ones away so tonight's material isn't buried under six months
of history.

- **+ New chapter** to add one; the **⋮** on a chapter renames, duplicates, reorders or deletes it.
  Deleting a chapter moves its segments into the neighbouring one rather than binning them.
- Click a chapter header to fold it. **Fold finished** collapses every chapter you've fully ticked off.
- Move a segment up or down past a chapter boundary and it changes chapter — that's how you move
  things between them, along with the Chapter dropdown in the segment editor.

A segment can also carry **the fight that happens in it** — pick an encounter in the segment editor and a
**⚔ Run** button appears on the segment, so you start the fight from the story rather than hunting for it.

On the **Initiative** tab: **◉ Area damage** hits several creatures in one pass (tick who's in it, mark who
saved, it does the arithmetic and queues every concentration check); **round timers** count spell durations
down at the top of each round and tell you when they end; **+ Lair action** puts a slot in the order at
initiative 20; and every row has a **reaction dot** that clears itself at the start of that creature's turn.

Every foe also carries a **table number** — `#1`, `#2`, `#3` — assigned in the order it entered the fight
and shown next to its name. Put the matching numbered die beside whichever model is standing in for it and
the miniature never has to look like the stat block. Click the number to change it; numbers are not reused
when something dies, because the die on the table doesn't move.

**Key beats** are the bullets inside each segment: the summary you read at a glance. Lead the pivotal
ones with ★. Under them sits the prep note — the one line you need in your hand — and under that, the
runtime notes box you type into during play. The head of each segment shows a beat count, so you can
see at a glance which scenes you've actually prepped.

---

## 4b. GETTING IT OUT AGAIN

- **Story → ⇩ Story PDF** prints the whole adventure — every segment with its beats, the fights,
  the handouts with their solutions, the mechanics and every stat block. Choose *Save as PDF* in the
  print dialog. This is what you read the day before, and the easiest thing to mark up when you want
  changes made.
- **Story → ⇩ Recap** writes the session out as markdown after you've played it.
- Ask Claude for the story **as a Word document with a comment on everything it invented**, mark it
  up, and hand it back — you get an updated build with your changes made.

---

## 5. THE PLAYERS' SCREEN

**Players** in the header opens a second browser window you drag onto your other monitor. Press it again
to close it; nothing about the main tracker changes either way. It shows one of three things, and you
choose which:

- **The battle map** for the fight you last loaded. **⧉ To players** on any encounter card puts that
  fight's map up.
- **A handout** — full screen, image and text, nothing else.
- **A scene image** — anything you attached to a story segment.
- **Blank** — for when they should be looking at you.

**The initiative order is hidden from them by default.** There's a *show them the initiative order*
tick in the Player screen bar at the top of the handouts section; leave it off and the order of battle
stays yours. Turn it on and they see names, table numbers, conditions and whose turn it is — never hit
points, AC or stat blocks.

**Images per scene.** Open a segment's editor and there's an *Images for the players' screen* section:
paste links or upload files, name them, reorder them. They show as thumbnails on the open segment and
one click throws one onto the player window. Ctrl+K finds them by name too.

**Handouts and puzzles** live at the bottom of the Tools tab. Each one has a player-facing side — an
image, some text, or both — and a solution that never leaves your screen. Write the riddle in the top
half, the answer and the DCs in the bottom half, and you can put the puzzle in front of the table while
reading how it works off your own laptop. Images can be a pasted link or an uploaded file (downscaled to
1600px and stored in the save file, so keep them modest).

Fastest route mid-session: **Ctrl+K**, type the handout's or the image's name, Enter. It goes straight
onto their screen.

---

## 6. IF SOMETHING GOES WRONG

- **Undo** — Ctrl+Z anywhere, or the Undo button in the header, or the Undo that appears on the toast right
  after something destructive. Twenty steps deep, covering deletes, clears, damage, rests, and loading a
  build. It does not undo typing in a notes box.
- **The save pill** next to Load says how long it has been since you saved properly, and goes amber then
  red as it ages. The browser will also stop you closing a tab with unsaved changes.
- **Automatic backups** are off by default. Turn them on in **⋮ → Not losing your evening** and it writes a
  timestamped JSON to your downloads every 10, 15 or 30 minutes. The first one makes the browser ask
  whether to allow multiple downloads — say yes once.

---

## 7. THE DICE ROLLER

Tools tab, top. There if you want it; the tool never rolls anything behind your back.

- Type `2d6+1d4+3`, `4d6kh3`, `1d20+7`. `kh`/`kl` keeps the highest or lowest N.
- Tap the die buttons to build the expression; **+1**/**−1** nudge the modifier.
- **advantage**/**disadvantage** rolls the whole expression twice and keeps the better or worse total —
  and shows you the one it dropped.
- Every die is shown individually. Maximum faces go green, natural 1s on a d20 go red, dice dropped
  by `kh`/`kl` are struck through.
- The roll log keeps the last sixteen, so "what did I actually roll for that" has an answer.

There's also a floating quick-roller on every tab — the **Dice** button in the header, or press **R**.

---

## 8. HOUSE RULES THE TOOL ASSUMES

- **2024 rules by default.** Say so if you're on 2014 and the condition text changes.
- **You roll the dice.** Every check says **roll a die** and takes your number, then does the
  arithmetic. If your table would rather the screen rolled, **⋮ → Dice → let the tracker roll the dice**
  puts a Roll button beside each of them. The dice rollers and **Roll foe initiative** are always
  available either way.
- **Difficulty uses the 2024 DMG XP budget** × party size, with no encounter multiplier. Those budgets
  are considerably tighter than the 2014 ones, so fights that felt "medium" under the old maths rate
  above High. That's the new table, not a bug.
- **Magic items widen the budget** by a homebrew percentage per item (2/5/10/18/30/50% for
  common → artifact, capped at +200%). Editable in Options; set them all to 0 to switch it off.
- **Minimum 1 hit point per level** in the HP roller.
- Official spell and rules text is never reproduced verbatim — effects are one-line paraphrases.
  Check your book for exact dice and ranges.

---

## 9. EDITING IT YOURSELF

Every card has a **⋯** menu: Edit, Duplicate, Move up, Move down, Delete. Delete asks twice.

- **Bestiary → + New creature.** A library of **118 templates** across 15 categories. Pick a target CR
  and the template rebuilds itself against it — AC, hit points, hit dice, attack bonus, save DC and
  damage all rescale, and bigger creatures gain extra attacks so the dice stay readable. Hover a card
  to read the finished block before committing. Each template carries the CR band where it still reads
  as itself; push a kobold to CR 20 and it says so rather than silently obeying.
  Traits go one per line. Spells are `name | level | perDay | casting note | effect` — level 0 is a
  cantrip, and a number in perDay makes it innate instead of spending a slot. Triggers are
  `name | kind | healAmount | text`, where kind is `auto`, `roll` or `rem`. Every one of those fields
  has a **⋮ library** button with common entries to click in.
- **Encounters → + New encounter.** Add creatures from a dropdown and watch the difficulty update live.
  The map is a text grid: `#` rock, `.` floor, `~` open air, `^` rubble, `s` stair, `=` ledge edge,
  `o` pillar, `T` plinth, `C` chimney up, `X` crack down, `D` door. Keep every row the same length.
  Tokens are `x | y | letter | side | name`.
- **Story → + New chapter / + Add segment.** Times are h:mm from session start; the pacing readout uses
  the end time. Key beats are one per line.
- **Tools → + New mechanic.** The rules table is pipe-separated with headers on the first line. Tell it
  which column holds the DC. Set "one save per" to 0 if it's always a single save.
- **Tools → + New handout.** A puzzle, riddle, inscription or picture. Top half is what the players read;
  bottom half is the solution and never leaves your screen.
- **⋮ top right** — campaign name, party size and level, six themes, dark/light/system, a background
  image, the magic-item percentages, the provenance switch, and the paste-a-build box.

---

## 10. THINGS THAT WILL BITE YOU

- **Save before you close the tab.** There is no autosave — browser storage isn't available to a file
  opened this way. Keep the JSON next to the HTML, or in whatever cloud drive you already use.
- **Pasting a build replaces the whole campaign.** Save first if you want the old one.
- **Map rows must all be the same length**, or the grid looks wrong. Short rows get padded with floor.
- **Every creature needs a CON save** or its concentration checks default to +0.
- **XP is per creature, not per encounter.** Enter the single-creature XP and set the quantity.
- **The app assumes a laptop.** It works on a tablet in landscape. It is not a phone tool. Ctrl+scroll
  zooms if you're reading it from across the table.
- **The player window is a pop-up.** If nothing happens when you press Players, allow pop-ups for the page.

---

*If you improve on any of this, the newer build wins — update the guide rather than working around it.*
