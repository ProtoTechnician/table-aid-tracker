# TABLE AID — BUILD SPEC
### For Claude. The exact contract for turning a plain-text adventure into a Table Aid build.

You are converting someone's adventure notes into a JSON object that the Table Aid tracker loads.
This document is the whole contract: the output shape, every field, and the provenance rules.

---

## 0. THE TWO RULES THAT OUTRANK EVERYTHING

**Rule one — the author's words are not raw material.**
Scene titles, monster names, numbers, read-aloud, their homebrew rule, their phrasing: copy it in
verbatim. Do not tidy prose, standardise names, "improve" a stat line, or renumber their scenes.
If their text says a thing, the build says the same thing.

**Rule two — everything you added is marked.**
The tracker has a provenance layer. Anything you invented, stated, scaled, balanced, guessed or
inferred carries three fields so the author can see your work and accept or reject it. Anything
that came from their text carries no marks at all. Getting this wrong in either direction is the
worst failure mode of this task: unmarked invention is you putting words in their mouth, and
marking their own writing is insulting.

---

## 1. OUTPUT

One fenced `json` code block. Inside it, nothing but:

```json
{"tableAidBuild":1,"data":{ ... }}
```

Questions, assumptions, caveats and reasoning go **outside** the block, before or after. Never
inside it — the author copies the block whole and pastes it into the tracker.

`data` has these keys:

| Key | Type | Required |
|---|---|---|
| `title` | string — the campaign or oneshot name, shown large in the header | yes |
| `sub` | string — subtitle, shown small below it | yes |
| `party` | object — size, level, magic items | yes |
| `chapters` | array — groups of story segments | yes |
| `scenes` | array — the running order | yes |
| `mon` | array — every creature and NPC | yes |
| `enc` | array — preset fights | yes |
| `tools` | array — homebrew campaign mechanics | yes (may be empty) |
| `cards` | array — handouts and puzzles for the players' screen | yes (may be empty) |
| `theme` | object — colours | optional |

---

## 2. PROVENANCE — how to mark your own work

Any object in `mon`, `enc`, `scenes`, `tools` or `cards` may carry:

```json
"ai": true,
"aiOk": false,
"aiNote": "One plain sentence: what you added, and why it had to exist."
```

`ai:true` draws a red rail down the card and shows the note with an **✓ That's fine** button.
`aiOk` must always be `false` in a fresh build — accepting is the author's job, not yours.
Objects with no `ai` field render plain. That's the default; most of a good build is unmarked.

### What gets marked

| Situation | Mark it? |
|---|---|
| They named a monster and gave a full stat line | **No** |
| They named a monster and gave nothing else | **Yes** — you invented every number |
| They said "CR 6 ogre-ish thing" | **Yes** — the name and the whole block are yours |
| They gave AC/HP but no Constitution save | **Yes**, and say the con save is the invented part |
| They listed a fight; you calculated its difficulty | **No** — the tracker calculates that itself |
| They listed a fight; you added two more goblins to hit a budget | **Yes** |
| They wrote the scene; you wrote the key beats | **Yes** |
| They wrote the scene and the beats; you split it into chapters | **No** — structure isn't content |
| You wrote a battle map from their one-line description | **Yes** |
| You wrote a battle map they never mentioned | **Yes** |
| They described their homebrew rule; you built the DC table from it | **Yes** if you chose DCs, **no** if they gave them |
| You added an NPC so the rescue scene has someone to rescue | **Yes** — and say that in the note |

### Writing the note

One sentence. Plain English. Say what you did and why the build needed it. Start with a verb from
this list so the notes scan consistently: **Invented · Statted · Scaled · Filled in · Balanced ·
Guessed · Split · Added**.

Good:

- `"Statted at CR 5 — you named the Choir Zealots and said 'tough but not elite', so every number here is mine."`
- `"Invented — your text mentions the survivors but never names them, and the rescue scene needs something to rescue."`
- `"Filled in a Constitution save of +6 from the CR; you didn't give one and concentration checks need it."`
- `"Balanced — I added two more Weepers to bring this from 4,100 XP up into the Moderate band for four level-10 characters."`
- `"Guessed the map layout from 'a ledge with a chasm down the middle'. Everything past that sentence is invented."`

Bad:

- `"AI-generated content."` — says nothing
- `"I hope this is what you wanted!"` — not information
- `"Added per D&D 5e standards."` — vague, and there is no such standard
- A paragraph. One sentence.

### The summary

Outside the code block, list what you marked and why, grouped: *creatures I built from nothing*,
*numbers I filled in*, *things I added that you never mentioned*. The author should be able to
argue with your choices without reading JSON.

---

## 3. THE FIELDS

### 3.1 `party`

```json
"party": {"size": 4, "level": 10, "items": {"rare": 4}, "itemPct": {}}
```

`items` counts magic items across the whole party by rarity — keys `common`, `uncommon`, `rare`,
`veryrare`, `legendary`, `artifact`. Each adds a homebrew percentage to every encounter budget
(2/5/10/18/30/50%, capped at +200%). Leave `itemPct` empty unless the author overrode the defaults.
If they didn't mention magic items, use `"items": {}` and say so in your summary — don't invent gear.

### 3.2 `chapters` and `scenes`

Chapters group segments so a long campaign can fold away what it has already played.
**A oneshot gets exactly one chapter.** A campaign gets one per session, or one per act.

```json
"chapters": [
  {"id":"c1","name":"Chapter One — Into the Fault","sub":"Sessions 1–3","open":true}
]
```

```json
"scenes": [
  {"ch":"c1","a":"0:00","b":"0:30","t":"The Kindly Hazard — the boat",
   "note":"Cold open. Write down every answer; it pays off at 2:15.",
   "keys":["Tallow Girsk asks each PC two questions — that IS the introduction",
           "Plant the woman in grey praying on the deck",
           "Name three fellow passengers so one of them can die later"]}
]
```

| Field | Meaning |
|---|---|
| `ch` | the `id` of its chapter — every scene needs one |
| `a`, `b` | start and end, `h:mm` from the top of the session. The pacing clock uses `b` |
| `t` | title |
| `note` | the one line the DM needs in their hand |
| `keys` | **key beats** — the at-a-glance summary, shown as bullets when the segment is open |
| `imgs` | optional array of `{"n":"label","u":"https://…"}` — images the DM can throw onto the players' screen from this segment |
| `enc` | optional. The `n` of an encounter, which puts a **⚔ Run** button on the segment |

**Key beats are the most valuable thing you produce.** They are what a DM reads in three seconds
while four people are looking at them. Write 4–8 per scene. Each one is a single sentence about
something that *happens* or something the DM must *do* — an interaction, a decision the party
faces, a line to say out loud, a thing to plant now that pays off later, a trap in the pacing.
Lead the pivotal ones with `★`.

They are not a summary of the prose. Compare:

- ✗ *"The party arrives at the town and can explore it."*
- ✓ *"Three errands, they pick two. Don't map the town."*
- ✓ *"★ Vurl's bookshop — 150gp for the glyph rubbings, or a trade for something with a personal history. This is key one of two to the temple puzzle."*

If the author's own text already contains beat-like bullets, use theirs unmarked. If you wrote them,
mark the scene.

**Never invent image URLs.** You cannot check that a link resolves, and a dead thumbnail at the table is
worse than none. Use `"imgs": []` and say in your summary which scenes would benefit from artwork.
Only fill `imgs` if the author gave you actual links.

Order `scenes` by chapter, then by time.

### 3.3 `mon` — creatures and NPCs

```json
{"n":"Choir Zealot","t":"Medium Humanoid, Lawful Neutral","cr":"4","xp":1100,
 "ac":17,"hp":75,"hd":"10d8+30","dex":2,"conSv":6,"sp":"30 ft., climb 20 ft.",
 "ab":[16,14,16,10,14,12],"grp":"Hushed Choir","side":"foe",
 "lines":["<span class='k'>Saves</span> Con +6, Wis +5 · <span class='k'>PP</span> 13",
          "<span class='k'>Multiattack.</span> Two Anchor-Picks. <span class='k'>Anchor-Pick</span> +6, reach 5 ft, 1d10+3 piercing."]}
```

| Field | Meaning |
|---|---|
| `n` | name — must be unique; encounters and maps reference it by name |
| `t` | size, type, alignment |
| `cr` | challenge rating as a **string** (`"1/2"` is legal) |
| `xp` | XP for **one** of them. This drives every difficulty calculation — get it right |
| `ac`, `hp` | numbers |
| `hd` | hit dice as text, e.g. `"10d8+30"` |
| `dex` | Dex **modifier**, used to break initiative ties |
| `conSv` | Constitution save bonus. **Always provide one** — the tracker runs concentration checks off it |
| `sp` | speed line |
| `ab` | `[STR, DEX, CON, INT, WIS, CHA]` scores, not modifiers |
| `grp` | faction or group label, used to sort the bestiary |
| `side` | `"foe"` (red card) or `"ally"` (green card). NPCs the party might rescue, hire or escort are `"ally"` |
| `lines` | the stat block body, one string per line |

`lines` is plain HTML. Wrap every label in `<span class='k'>…</span>` — that's the accent colour.
One line per trait or action. Keep each to a sentence or two: this is read mid-combat, not studied.

**Never reproduce official stat blocks, spell text or rules text verbatim.** Write mechanically
equivalent content in your own words. If the author asks for "a standard owlbear", build one that
plays the same way and say in the `aiNote` that it is a fresh block, not the book's.

#### `kit` — spells and limited-use abilities

Optional per creature. Renders as a dropdown tray in the initiative list with clickable slot pips.

```json
"kit": {"dc":14, "slots":{"1":3,"2":2},
  "spells":[{"n":"Bless","lv":1,"t":"Conc · 1 min","d":"Three creatures add 1d4 to attacks and saves."}],
  "uses":[{"n":"Second Wind","max":1,"note":"Bonus action, regains a quarter of its maximum HP."}]}
```

`lv: 0` is a cantrip. Add `"per": 2` to a spell to make it innate (2/day) instead of spending a slot.
Spell `d` is a one-line paraphrase — again, never the book's wording.

#### `trig` — automatic pop-ups

```json
"trig": {
  "combat":[{"n":"Aura of Command","w":"Every ally within 60 ft has +2 on saves. Apply before initiative.","k":"rem"}],
  "turn":[{"n":"Regeneration","w":"Regains 15 HP at the start of its turn if above 0.","k":"auto","heal":15}]}
```

`combat` fires when the encounter loads; `turn` fires at the start of that creature's turn.
`k` is `"auto"` (gets an Apply button — pair with `heal`), `"roll"` (roll something) or `"rem"` (reminder).
Use these for exactly the things a DM forgets: regeneration, auras that apply before initiative,
recharges, "it starts the fight already singing".

#### `legRes`, `legAct`

```json
"legRes": 3, "legAct": 3
```

Legendary resistances and legendary actions per turn. Tracked in the same tray.

### 3.4 `enc` — encounters

```json
{"n":"Scene 3 — The Hushed Choir ambush","loc":"1st Layer · switchback ledges · ~900m",
 "note":"Falling is the real threat. A fall is a DESCENT, so the Curse doesn't punish it.",
 "m":[["Choir Zealot",6],["Silence-Warden",2],["Cantor Nimh Astel",1]]}
```

`m` is `[["creature name", quantity], …]` and the names **must match `mon[].n` exactly**.

**Do not put a difficulty rating in the note — the tracker computes it live.** It uses the 2024 DMG
XP budget: per-character thresholds × party size, no encounter multiplier, plus the magic-item uplift.
For four level-10 characters that's Low 6,400 · Moderate 9,200 · High 12,400 before items.
Sum `xp × quantity` and check where you land before you write the composition. If the author's own
fight lands somewhere strange, build it as written and say so in your summary — don't silently retune
their adventure.

#### `map` — the battle map

```json
"map": {"t":"Switchback ledges","scale":"20 x 14 squares - 100 ft x 70 ft",
  "draw":"Draw the two chasm bands first, then the ledges, then the ramps.",
  "rows":["####################","#..................#","~~~~~~~~~~~~~~~~~ss~"],
  "tok":[{"x":10,"y":1,"l":"C","s":"foe","n":"Cantor Nimh Astel"}]}
```

Tiles: `#` rock · `.` floor · `~` open air or fall · `^` rubble (difficult) · `s` stair or ramp ·
`=` ledge edge · `o` pillar · `T` plinth · `C` chimney up · `X` crack down · `D` door.
**Every row must be the same length.** `tok` is `x,y` (0-indexed from top-left), a letter, a side
(`foe`/`ally`/`pc`) and a label. Keep maps to roughly 20×14; bigger ones stop being copyable.

Maps are the first thing to cut if the build is getting long — say so and offer them separately.

### 3.5 `tools` — campaign mechanics

One entry per homebrew rule: a curse, a madness track, corruption, heat, supply, a doom clock.

```json
{"id":"curse","name":"The Curse of Ascension",
 "rule":"Going down costs you nothing. Going up costs you everything.",
 "trigger":"A creature that gains 500 ft of net elevation within 10 minutes makes a Constitution save…",
 "cols":["Deepest layer reached","DC","Failed save","Successful save"],
 "rows":[["1st (0–1,350m)","10","Poisoned 1 hour","No effect"]],
 "dcCol":1, "ability":"Constitution",
 "res":{"on":true,"amountLabel":"Feet ascended","amount":500,"unit":500,
        "advLabel":"Oku routing (advantage, 1 save / 1,000 ft)","advUnit":1000},
 "dtable":{"name":"Hallucinations (d6)","die":6,"items":["…","…"]},
 "notes":[{"t":"Hollowing","b":"What happens at the bottom of the track."}]}
```

`dcCol` is which column index holds the DC. `res.unit` is how many units of `amount` force one
save — set it to `0` if it's always a single save. `dtable` is an optional random table with a
roll button. `notes` are free-text panels beside it.

If the author has no homebrew rule, `"tools": []` is correct. Do not invent one to fill the tab.

### 3.6 `cards` — handouts and puzzles

The tracker can open a second window on the DM's other screen. Anything in `cards` can be thrown onto it
with one click: a riddle, an inscription, a letter, a piece of artwork, a puzzle. Each card has a
player-facing side and a solution that never leaves the DM's screen.

```json
{"id":"h_lock1","name":"Lock One — the nine plates",
 "img":"",
 "text":"Carved above the topmost plate:\n\n“THE ABYSS COUNTS NOTHING UPWARD…”",
 "dm":"Abyss glyph reads BOTTOM TO TOP. Press the plates 9 → 1. Wrong order = 4d6 force, DC 16 Dex."}
```

| Field | Meaning |
|---|---|
| `id` | unique string; prefix with `h_` |
| `name` | the DM's label — never shown to the players |
| `img` | optional. A URL, or leave empty. **Never invent an image URL** — you cannot check that it resolves. Leave it blank and say in your summary that the DM can add artwork themselves |
| `text` | what the players read, shown large and centred. Use `\n` for line breaks |
| `dm` | the solution, the DCs, what happens on a failure. Never displayed to the players |

**Every puzzle in the adventure should become a card.** If the author wrote a riddle, an inscription or a
door that opens a particular way, the player-facing wording goes in `text` and everything about how it is
solved goes in `dm`. That split is the point: the DM can put the puzzle on the table's screen and keep
reading the answer off their own.

Handouts written from the author's own puzzle text are **not** marked. A card you invented — a piece of
set dressing they never wrote — is.

### 3.7 `theme`

```json
"theme": {"name":"abyss","mode":"dark"}
```

Names: `abyss` (teal/amber), `ember` (red/gold), `verdant` (green), `violet`, `slate`, `ash`.
Pick one that matches the tone if the author gave you a tone. This is cosmetic; never mark it.

---

## 4. HOW MUCH TO INVENT

Fill gaps that stop the tracker working. Don't fill gaps that are the author's to fill.

**Always invent, and mark it:** a Constitution save for any creature that lacks one; XP for any
creature with a CR; a stat block for anything the party can fight that only has a name; a `side`
for every creature.

**Invent if it's clearly implied, and mark it:** NPCs the adventure needs but never names (the
survivor being rescued, the merchant who sells the thing); the DC table for a homebrew rule they
described in prose; key beats for scenes written as prose.

**Ask instead of inventing:** what happens at the end; who the villain really is; whether a fight
is meant to be winnable; anything where guessing wrong sends them down a road they didn't write.
Put these questions under the code block as a short list. Build the rest.

**Never invent:** a different tone; extra scenes that change the shape of the session; a twist they
didn't write. You are furnishing their adventure, not co-writing it.

---

## 5. CHECKLIST BEFORE YOU SEND

- [ ] One fenced json block, `{"tableAidBuild":1,"data":{…}}`, nothing else inside it
- [ ] Every `enc[].m` name matches a `mon[].n` exactly
- [ ] Every `scenes[].ch` matches a `chapters[].id`
- [ ] Every creature has `conSv`, `xp`, `side`
- [ ] Every puzzle in the adventure exists as a `cards` entry, player wording separated from the solution
- [ ] Every map's rows are equal length
- [ ] Every invented object has `ai`, `aiOk:false`, and a one-sentence `aiNote` starting with a verb
- [ ] Nothing the author wrote is marked
- [ ] No official stat block, spell or rules text reproduced verbatim
- [ ] Scene times run in order and the last one ends at the session length they asked for
- [ ] A short summary outside the block: what you marked, and any questions
