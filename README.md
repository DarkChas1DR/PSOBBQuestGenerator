# PSOBB Quest Generator

Separate quest-authoring project using a pinned snapshot of the [PSOBB Quest Database](https://github.com/DarkChas1DR/PSOBB-Quest-Database).

## Current release: planning prototype

Episode 1 area/map/room selection, numbered map links, wave type/count entries, NPC positions/dialogue/handler planning, compatibility warnings, browser autosave and JSON plan import/export.

**This is not yet an AI-powered or playable-quest generator.** It does not compile BIN/DAT/QST. Enemy coordinates, event chains, door/completion logic, full appearance editing, boss presets, AI backend and native tests are unfinished. It does not invent capacity limits or certify source-documented placements as client-tested.

Open the site through any static HTTP server. For example, run `python -m http.server 8080` here and visit localhost:8080. There are no package dependencies. GitHub Pages deployment is provided by the workflow; repository Pages must allow GitHub Actions.

## Development sequence

1. Structured authoring plan and pinned research data (initial implementation).
2. Deterministic compiler/packager with an independently checked small encounter fixture.
3. QEdit save/reopen and solo/four-player client tests.
4. Backend AI planning with schema validation and server-side credentials.
5. Broader encounters and episodes as verification grows.

The database remains a separate research site. Reference snapshot: f901e1f. Source data retains its original ownership; this repository adds no blanket licence over game or upstream reference material. Saved plans stay in the browser unless explicitly exported. No AI key is requested or stored.
