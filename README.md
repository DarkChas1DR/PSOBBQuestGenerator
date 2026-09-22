# PSOBB Quest Generator

[Public editor](https://darkchas1dr.github.io/PSOBBQuestGenerator/) · [Research database](https://github.com/DarkChas1DR/PSOBB-Quest-Database)

Describe a quest, review the AI proposal, edit its plan, and build a Blue Burst test package. **Generated quests still require QEdit and client validation.**

## What works now

- Episode 1 area/map/room browsing, wave and NPC planning, plan import/export and browser autosave.
- Local Ollama prompt generation, proposal review and undo.
- A Forest 2 room 12 encounter preset with source-derived placement anchors, researcher dialogue, sequential waves, a door and a finish interaction.
- Explicit Savage/Barbarous Wolf and Booma/Gobooma/Gigobooma variants, including their required parameters.
- Experimental BB BIN/DAT/QST compilation through newserv, independent decoding and a build report.

The **public website is a planning editor**. AI and compilation run on your own computer; GitHub Pages cannot host Ollama. No API key or paid AI account is required for a local model. Hardware and electricity are still needed.

## Run locally

1. Install Python 3.10+ and [Ollama](https://ollama.com/). Download a model, for example `ollama pull qwen3:4b`.
2. Download/clone this repository. In its folder run `python server.py` and open http://127.0.0.1:8088.
3. For compilation, set `NEWSERV_PATH` to your [newserv](https://github.com/fuzziqersoftware/newserv) executable before starting the server. It is not bundled. The development compiler is build 1f7faff9+; every build report records its hash.
4. Choose a local model and enter a prompt. Review the proposal, apply it, then build the QST package.

Example prompt:

> Build Lost Research Team for four players in Ultimate. Two waves: six Savage Wolves then eight Goboomas. Include a missing researcher briefing and dialogue.

In PowerShell, configure compilation with:

```powershell
$env:NEWSERV_PATH = 'C:\path\to\newserv-windows.exe'
python server.py
```

The server listens only on loopback. Do not expose this development server publicly. The browser sends quest prompts only to that local server; it calls Ollama on loopback. Source files and environment settings are not served by the app.

## Supported scope and limits

The buildable AI preset currently targets **Forest 2 room 12**. The 16-wave and 24-record budgets are application limits, not proven PSOBB capacity limits. General Episode 1 planning supports more maps but requires explicit placements before compiling. Bosses, item rewards, additional episodes, full appearance editing and multi-floor compilation remain unfinished. General full-plan model generation has timed out in testing; the compact encounter recipe is the tested path.

Difficulty is design intent: choose the matching server mode. Completion sets the success register and the researcher interaction exits the test quest; no rewards are awarded. NPC accessibility, door operation, starting-floor drop behavior, progression and four-player synchronization remain unverified in the client. Do not install over an existing production quest; the test uses quest number 65000.

## Evidence and tests

Run `python -m unittest discover` and `node smoke.cjs`. Setting `NEWSERV_PATH` includes real compiler/QST round-trip tests; otherwise that test is explicitly skipped. The local model has produced a recipe matching six Savage Wolves and eight Goboomas and compiled successfully. Source-derived coordinates are not a substitute for gameplay tests.

[Current validation record](VALIDATION.md) tracks completed checks and outstanding work. No 100% compatibility claim is made.

## Reference provenance

Pinned database snapshot: f901e1f. Spatial anchors come from TTF and Monster Bash 1: Encore; source quest IDs are retained per position. Model decisions cannot invent anchor coordinates. Upstream data and game materials retain their original ownership; this repository adds no blanket licence over them.

Ollama protocol: [structured outputs](https://docs.ollama.com/capabilities/structured-outputs).
