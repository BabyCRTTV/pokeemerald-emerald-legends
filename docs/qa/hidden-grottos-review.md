# Hidden grotto first-review evidence

Unshipped prototype based on published `a3eea770` / v0.0.68. This is a review checkpoint, not a release candidate.

- Both local native builds completed with GCC ARM 13.2.1: Debug `pokeemerald.gba`, Release `pokeemerald-release.gba`. Hashes: [receipt](hidden-grottos-review.json). Neither ROM is committed or distributed.
- `tools/legends/native_grotto_review/run.py` executed the built Debug review ROM under native mGBA 0.10.2. Private callback setup selected each of three maps and four seasons. Actual native objects matched their selected species graphics and committed season; player placement was passable.
- Real input approached each Spring visitor, played its cry/text and closed the dialogue. Real walking left each shelter, returned to its safe native route approach, declined an entrance and then reentered it. All twelve seasonal scenes and all three return/decline/reentry paths passed.
- The native Quickstart smoke also passed. Focused host checks passed map reachability, safe approaches, absent event collisions, unchanged existing route art/scripts/events and append-only map/layout IDs. Baseline hashes are pinned to `a3eea770` in [the regression fixture](hidden-grottos-baseline.json), so shallow CI checkouts need no historic Git fetch.
- Existing season/calendar tests, all 84 seasonal encounter tables and the eight Kanto event-script checks passed. These checks are focused regressions, not proof of uninterrupted story progression or all historical battery saves.
- `tools/legends/present_grotto_review.py` copied verified native 240×160 captures and enlarged them with nearest-neighbor scaling. Captions sit outside the frames. [Preview sheet](../designs/hidden-grottos/Emerald-Legends-Hidden-Grottos-Preview.png), [season GIF](../designs/hidden-grottos/Emerald-Legends-Grotto-Seasons.gif), [native frame hashes](../designs/hidden-grottos/verification.json) and [native assertions](../designs/hidden-grottos/emulator.log).

Limits: reward collection, captures/battles, cooldowns and their persistent save state are intentionally not implemented in this exploration review. No BPS files were created or independently applied, and no release/wiki/site/version change was made. Broader Release interactions, historical saves and Pizza Boy were not exercised. Preserve these limits when reporting status.

The diagnostic mailbox occupies 64 bytes above the game's EWRAM heap, and the host retries callback injection at frame boundaries if native field callbacks replace it before execution. Instrumentation only prepares scenes and queries their state; it does not replace movement, dialogue, sprite rendering, seasonal logic or entrance scripts. Do not commit the private ROM, temporary ELF, raw buffers or fixtures.
