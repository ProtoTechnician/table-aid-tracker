# Changelog

Versions are the tracker's, recorded in `docs/DESIGN.md`.

## 2.2.1

- A hairline seam under the header bar, so at table distance the bar reads as the edge of the
  screen rather than as a floating panel.
- Numbers arriving from text fields go through one clamp, instead of each field guarding itself.
- Save files carry a `schema` field naming the format and the build that wrote them, so a file
  from an older build can be recognised as one rather than half-loaded.

## 2.2

- **Table numbers on every foe** — `#1`, `#2`, `#3` in entry order, click to edit, never recycled
  when something dies, so the numbered die beside the model never has to move.
- **The players' screen hides the initiative order by default**, and says so; it is turned on
  deliberately rather than leaked.
- **Images per story segment** — thumbnails inside the open segment, one click to the second screen.
- **Handout text expands in place** instead of truncating into the editor.
- **A dice toggle.** Every check says *roll a die* and takes a typed number; a global option adds a
  Roll button beside each instead. Roll foe initiative and the two rollers are always available.
- **The review pill is a walk** — each click jumps to the next unreviewed item, opening the right
  tab and chapter on the way.
- **Story PDF** — the whole adventure printed as a read-through, with anything still unreviewed
  flagged in red.
- Bestiary field buttons read *library* rather than *library & syntax*.

## 2.1

- **Undo**, twenty deep, on Ctrl+Z, a header button and the toast after anything destructive.
- **Save-age pill** and a `beforeunload` guard; optional timed backup downloads.
- **Area damage** in one pass, with per-creature save results and a queue of concentration checks.
- **Round timers** that tick at the top of each round, **lair actions** at initiative 20, and a
  **reaction dot** that clears itself on that creature's turn.
- **A player-facing second window** driven by handouts and puzzles kept in Tools.
- **Ctrl+K** jump-to-anything; a markdown recap export; a segment can carry its own fight.
- Table mode was built and then removed — Ctrl+scroll already does it better.

## 2.0

- Everything became editable in the browser; content moved from constants onto `S.data`.
- **118 creature templates** with a CR scaling engine and archetype bands.
- Six themes, light/dark/system, background images.
- **The provenance layer** — `ai` / `aiOk` / `aiNote`, marks, the accept flow and the global switch.
- The run sheet became **Story**, with chapters and key beats.
- The campaign-mechanic tab became **Tools**, and gained a full dice roller.

## 1.0

- Initiative, party sheets, bestiary, encounters with the 2024 XP budget, campaign mechanic tab,
  run sheet with a session clock and pacing readout.
