# THE PROMPT — copy this into Claude

Start a new chat. Attach `02_BUILD_SPEC.md` (and this file, if you like). Paste the text below,
then paste or attach your adventure underneath it.

---

```
Build my adventure into a Table Aid tracker.

Follow 02_BUILD_SPEC.md exactly. Two things matter more than anything else:

1. KEEP MY WORDS. Anything I wrote — scene titles, monster names, numbers, notes,
   read-aloud, my homebrew rule — goes in as I wrote it. Don't tidy it, don't
   improve it, don't rename anything.

2. MARK EVERYTHING YOU ADD. Every creature, encounter, story segment and mechanic
   you invent, stat, scale, balance or guess at gets  "ai": true, "aiOk": false,
   and an "aiNote" saying in one plain sentence what you did and why. Anything that
   came from my text gets no mark at all. If you're halfway — I gave a name and a
   vibe, you built the numbers — mark it and say so in the note.

Return ONE fenced json code block containing {"tableAidBuild":1,"data":{...}} and
nothing else inside the block. Put your questions and your reasoning outside it.

My party: [4 players, level 10, D&D 2024 rules, one rare magic item each]
Session length: [about 6 hours]
Tone: [heroic fantasy with grim stakes]

My adventure follows.
```

---

## Want to see one first?

`04_EXAMPLE_BUILD.json` is a complete small build — two chapters, five segments with key beats,
three creatures, two fights with a map, one homebrew mechanic, correctly marked. Paste it straight
into the tracker before you write anything and you'll know what you're aiming at.

## Then

1. Copy the JSON block Claude gives you.
2. Open the tracker → **⋮ top right** → **Paste a build from Claude** → **Load this build**.
3. Everything Claude invented is outlined in **red** with a note explaining why.
   Read them, and tick off the ones you're happy with. The red goes away.
4. **Save.** That downloads one JSON file holding your whole session.

## If the build is too big for one message

Ask for it in two:

```
Give me the build in two parts. Part one: title, sub, party, chapters, scenes, tools.
Part two: mon and enc only, as {"tableAidBuild":1,"data":{"mon":[...],"enc":[...]}}.
```

Paste part one, then part two — the second paste merges creatures and encounters into
what's already loaded rather than replacing it, as long as you don't reload the page in between.
Ask Claude to drop the `map` fields first if you need to save space; you can draw those later.

## Going back for more

The chat still has your adventure in it. Useful follow-ups:

- *"Add three more key beats to segment 4 — the ones I'd forget mid-scene."*
- *"The second fight is too hard for a party with no magic items. Rebalance it and re-mark what you changed."*
- *"Give me a battle map for encounter 2."*
- *"Split the story into three chapters: the town, the descent, the temple."*
- *"Stat the innkeeper as a CR 2 NPC in case they fight him."*

Every time, remind it: **return the whole `data` object, and keep the provenance marks.**
