# Validation status

## Completed

- 24 Python checks, including actual newserv compilation when NEWSERV_PATH is set.
- QST extraction reproduces compressed BIN/DAT payloads byte-for-byte.
- Independent decoder verifies script metadata and expected object/enemy counts.
- Named variant tests verify Savage Wolf parameter 2 and Gobooma parameter 6.
- Browser-independent editor smoke test: area mapping, wave addition, NPC placement and autosave.
- Real Qwen3 4B generation of Lost Research Team with six Savage Wolves and eight Goboomas; successful compilation.
- Real model revision changes the requested first-wave count while preserving the second wave.
- Common unsupported boss requests rejected before generation; model-only rejection was found unreliable and is not relied on alone.

- Public GitHub Pages deployment succeeded; editor returned HTTP 200.
- Browser interaction: local model discovery, prompt generation, proposal application (14 enemy records), QST package response and Undo restoring the prior eight-record plan.
- Negated feature lists such as “no boss or rewards” are accepted; separate positive requests remain rejected.
- Revision requests include existing NPC dialogue in the model context. Exact preservation still depends on the model and proposal review.
- Publishing now runs Python checks and the editor smoke check first. Hosted checks skip the native newserv test when the executable is unavailable; local native compilation remains a separate check.

- HTTP boundary checks cover invalid requests, rejected external origins, concurrent AI requests, provider failure recovery, compiler configuration errors and private source paths.

## Pending

- Generated quest QEdit open/save/reopen comparison. The database's original TTF baseline is not proof for this generated quest.
- Solo and four-player client tests: NPC, spawns, waves, door, finish, disconnect/failure paths.
- Broader prompt fidelity tests and support for additional maps, features and complete quest-building workflows.

Static decoding proves file structure, not playable behavior. Model success on one prompt is not a guarantee for all requests.
