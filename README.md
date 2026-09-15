# PSOBB Quest Generator

Separate quest-authoring project using a pinned snapshot of the [PSOBB Quest Database](https://github.com/DarkChas1DR/PSOBB-Quest-Database).

## Current release: planning prototype

Episode 1 area/map/room selection, numbered map links, wave type/count entries, NPC positions/dialogue/handler planning, compatibility warnings, browser autosave and JSON plan import/export.

**This is not yet a client-validated playable-quest generator.** Experimental single-floor BIN/DAT/QST compilation is implemented through a locally configured newserv tool. General placement authoring, full appearance editing, boss presets and native tests are unfinished. The compiler provides an explicit sequential event chain and completion handler for its test encounter. A local AI adapter is implemented; real-model validation is pending. It does not invent capacity limits or certify source-documented placements as client-tested.

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

## Experimental BB quest export

Set `NEWSERV_PATH` to your newserv executable before starting `python server.py`. The tested development executable is newserv 1f7faff9+; the build report records its SHA-256. Obtain/build newserv from https://github.com/fuzziqersoftware/newserv; it is not bundled here.

In the editor, **Load two-wave test encounter**, then **Build QST package**. The ZIP contains QST, compressed BIN/DAT, assembly, independent decoder outputs and a build report. The example combines source-derived Forest 2 placement anchors with newly generated logic; it is **not yet client-playtested**. NPC accessibility, door behavior, completion and multiplayer need native tests. Do not replace an existing server quest with this test without choosing a separate server entry and checking its quest number.

AI encounter scope uses this placement template when starting an empty plan. Matching positions are retained; unsupported spatial changes remain uncompiled. General planning can cover more maps than the experimental compiler.

Run `python -m unittest test_server.py test_compiler.py` with `NEWSERV_PATH` set to include real compilation and QST extraction tests. One test also checks that joining stays disabled: newserv's `.joinable` directive is enabled by presence, even if followed by `false`.
