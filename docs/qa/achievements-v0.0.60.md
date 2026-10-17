# Thirty-five additional achievements — v0.0.60

The owner requested another 35 achievements on 16 October 2026. Implementation appends IDs 95–129 (130 total): ten research milestones, twenty native activity/stat goals, three caught-species goals and two optional native gifts. Original IDs 0–94, goals and rewards remain byte-for-byte identical in the catalogue. Existing artwork, wardrobe, maps, seasons, journal rendering and native animation are unchanged.

## Save impact

The 36-byte v1 journal remains at offset 652. A separately signed 28-byte extension at offset 688 holds earned/claimed bits for IDs 96–159. Legacy migration keeps all original 95 bits and the tracked quest, clears unpublished bit 95 and initializes the new tail; no native variables, storage reader, packed header, sector geometry or inventory capacity changes. Current SaveBlock3 size is 716 bytes within existing sector tails. New eligible goals backfill quietly and remain manually claimable. PC deposits remain atomic and once-only.

## Completed local verification

All 50 project workflow blocks passed locally, including the original 95-entry fingerprint, JSON/C parity, every new threshold/manual claim/full-PC retry, bit boundaries 95/96/127/128/129, retained low bits/pins, repeated initialization, native-font UI/details/navigation, full sector rotations and protected artwork/wardrobe/season tests. The threshold refinement also passed focused journal/UI/research retests.

Both normal native GCC 13.2.1 Debug and LTO Release builds passed. Existing unrelated Release LTO warnings remained. Private Debug/Release patches reconstructed the exact tested ROMs with Floating IPS and the browser decoder against canonical Emerald SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`.

mGBA 0.10.2 ran a controlled v0.0.59-layout journal with original claims/pin, arbitrary unused tail/bit 95, completed research, non-default wardrobe and Winter. Quiet migration retained original claims and the pin, rejected legacy garbage and backfilled all ten research goals unclaimed. Actual flash save/clear/load retained both bit arrays, settings, party/inventory and request progress. The actual native flag hook unlocked ID 129; real menu input scrolled to entry 130/130 and opened its full details. Full-PC failure retained the reward; freeing space and manually claiming added exactly three Charti Berries once. Another actual flash save/clear/load retained the claimed high bit and exact PC quantity.

Four normal title/Continue runs used the unmodified Debug and Release ROMs, each with migrated-unclaimed and high-ID-claimed battery fixtures. Hosts only sent buttons and read RAM. Original claims/pin, extension bits including 129, research, bedroom colors and exact PC quantities survived. [Machine receipts](achievements-v0.0.60.json) · [Actual-game phone preview](achievements-v0.0.60-preview.png).

## Publication and limits

PR #75 merged as `046eeba758cda44a09a875b0b6fd912ed95dcd3d`. The production [project checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38988995474) and [Release/Debug native build plus BPS verification](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38988995495) passed. The patch update landed as `c9d5a3e090588dc4c734ab4ae29b226d4f066656`, and the [Pages deployment](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38989753116) succeeded. Both v0.0.60 BPS files and SHA256SUMS.txt are committed. This audit checked the CI/commit evidence, not an independent downloaded live Pages byte comparison. See [17 October resumption audit](resume-2026-10-17.md).

`tools/legends/native_achievement_expansion_qa/` reproduces the controlled extension migration and high-ID native UI/reward/flash tests. Fixtures are format-identical synthetic saves, not authentic historical user saves. An authentic historical-release matrix, Pizza Boy and a full uninterrupted playthrough remain outside this milestone. Private ROMs, saves and raw data are excluded. AGENTS.md was reviewed; no new durable rule was needed.
