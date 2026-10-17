# Thirty-five additional achievements — v0.0.60

The owner requested another 35 achievements on 16 October 2026. Implementation appends IDs 95–129 (130 total): ten research milestones, twenty native activity/stat goals, three caught-species goals and two optional native gifts. Original IDs 0–94, goals and rewards remain byte-for-byte identical in the catalogue. Existing artwork, wardrobe, maps, seasons, journal rendering and native animation are unchanged.

## Save impact

The 36-byte v1 journal remains at offset 652. A separately signed 28-byte extension at offset 688 holds earned/claimed bits for IDs 96–159. Legacy migration keeps all original 95 bits and the tracked quest, clears unpublished bit 95 and initializes the new tail; no native variables, storage reader, packed header, sector geometry or inventory capacity changes. Current SaveBlock3 size is 716 bytes within existing sector tails. New eligible goals backfill quietly and remain manually claimable. PC deposits remain atomic and once-only.

## Verification in progress

All 50 project workflow blocks passed locally, including the append-only catalogue fingerprint, JSON/C parity, all new thresholds/claims/full-PC retries, bit boundaries 95/96/127/128/129, retained low bits/pins, repeated initialization, UI/details/navigation, full sector rotations and protected artwork/wardrobe/season tests. Native Debug/Release builds, controlled flash/Continue and publication are still in progress; this record does not claim them yet.

`tools/legends/native_achievement_expansion_qa/` reproduces the controlled extension migration and high-ID native UI/reward/flash tests. Fixtures are format-identical synthetic saves, not authentic historical user saves. An authentic historical-release matrix, Pizza Boy and a full uninterrupted playthrough remain outside this milestone.
