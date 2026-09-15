# PSOBB Quest Generator

Separate quest-authoring project using a pinned snapshot of the [PSOBB Quest Database](https://github.com/DarkChas1DR/PSOBB-Quest-Database).

## Current release: planning prototype

Episode 1 area/map/room selection, numbered map links, wave type/count entries, NPC positions/dialogue/handler planning, compatibility warnings, browser autosave and JSON plan import/export.

**This is not yet a client-validated playable-quest generator.** It does not compile BIN/DAT/QST. Enemy coordinates, event chains, door/completion logic, full appearance editing, boss presets and native tests are unfinished. A local AI adapter is implemented; real-model validation is pending. It does not invent capacity limits or certify source-documented placements as client-tested.

Open the site through any static HTTP server. For example, run `python -m http.server 8080` here and visit localhost:8080. There are no package dependencies. GitHub Pages deployment is provided by the workflow; repository Pages must allow GitHub Actions.

## Development sequence

1. Structured authoring plan and pinned research data (initial implementation).
2. Deterministic compiler/packager with an independently checked small encounter fixture.
3. QEdit save/reopen and solo/four-player client tests.
4. Backend AI planning with schema validation and server-side credentials.
5. Broader encounters and episodes as verification grows.

The database remains a separate research site. Reference snapshot: f901e1f. Source data retains its original ownership; this repository adds no blanket licence over game or upstream reference material. Saved plans stay in the browser unless explicitly exported. No AI key is requested or stored.

## Local AI integration (in development)

Run `python server.py`, then open http://127.0.0.1:8088. Install Ollama and an appropriate model separately, start Ollama, and use **Find local models**. Enter a prompt, generate, review, apply or undo. Local models have no per-request API fee, but require suitable hardware. Model quality and speed vary.

The Python server calls Ollama on loopback only and never asks for an API key. It validates entity IDs, exact map variants and room references. Coordinates, wave activation and runtime compatibility remain unverified. GitHub Pages supports manual planning; AI requires this local backend. Do not expose the development server publicly.

Adapter/validation tests: `python -m unittest test_server.py`. Editor smoke test: `node smoke.cjs`. The adapter test uses a mocked response; a real local-model run is pending because Ollama is not installed in the development environment.

API reference: https://docs.ollama.com/api/chat
