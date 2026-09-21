# Validation status

## Completed

- 15 Python checks, including actual newserv compilation when NEWSERV_PATH is set.
- QST extraction reproduces compressed BIN/DAT payloads byte-for-byte.
- Independent decoder verifies script metadata and expected object/enemy counts.
- Named variant tests verify Savage Wolf parameter 2 and Gobooma parameter 6.
- Browser-independent editor smoke test: area mapping, wave addition, NPC placement and autosave.
- Real Qwen3 4B generation of Lost Research Team with six Savage Wolves and eight Goboomas; successful compilation.
- Real model revision changes the requested first-wave count while preserving the second wave.
- Common unsupported boss requests rejected before generation; model-only rejection was found unreliable and is not relied on alone.

## Pending

- Visual browser interaction verification (earlier tool attempt blocked by usage review).
- Generated quest QEdit open/save/reopen comparison. The database's original TTF baseline is not proof for this generated quest.
- Solo and four-player client tests: NPC, spawns, waves, door, finish, disconnect/failure paths.
- Broader prompt fidelity tests and support for additional maps, features and complete quest-building workflows.
- Public Pages deployment verification after initial enablement.

Static decoding proves file structure, not playable behavior. Model success on one prompt is not a guarantee for all requests.
