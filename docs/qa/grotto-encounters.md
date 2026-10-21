# Hidden grotto encounters — unshipped review

**Model: GPT-6 (Codex) | Reasoning: append isolated visitor state, exercise native battle outcomes and test real flash/Continue rather than infer persistence from compilation.**

Implemented the owner’s requested rare visitors, independent 4,500-step renewal after capture/defeat, compact LegendsDex labels and Grotto filter. Only Route 119 cells `(26,103)` and `(27,103)` changed visually: both now use the plain cliff immediately to their right. All approved interiors, other entrances, landing/collision, map IDs and original encounter tables remain protected by the existing regressions. [Roster/rules](../features/hidden-grottos.md), [machine evidence](grotto-encounters.json), [actual Route 119 capture](../designs/hidden-grottos/encounter-update/Route-119-Cliff.png), [mobile reader](../designs/hidden-grottos/encounter-update/LegendsDex-Grotto-Filter.png).

## Passed

- Native Debug and LTO Release builds. mGBA Quickstart smoke on the unmodified Debug ROM.
- Production-C state tests: all twelve weighted seasonal pools, 768 room/outcome combinations, stable full visitor data through 5,001 active steps/season changes/reinitialization, unrelated battle guards, exact cooldown boundary, independent rooms, invalid legacy tails, untouched original 716-byte prefix and occupied-square spawn deferral.
- Native mGBA Debug: actual challenge/escape preserving identity, KO removing the visitor and starting at 4,500, one physical step reducing it to 4,499, fast-forward to the exact renewal boundary with visible respawn, Master Ball capture awarding the Pokémon and starting the next cooldown. Actual native save/clear/load transactions preserved active/cooldown/capture states and the existing prefix, Pokémon, Bag and season fixture.
- Unmodified Release boot and normal Continue, with controller input and read-only assertions: synthetic absent-tail migration, exact active visitor checksum, exact 4,500-step cooldown, and caught-party count. The resume map hook also refreshes a restored instance’s resolved graphics ID before sprites are recreated.
- All twelve seasonal world scenes and the three production exit/decline/reentry paths, real cliff landing/discovery walks and historical entrance-option checks. Actual compiled-ROM mGBA frames; Route 119 preview is exact 3× nearest-neighbor pixels.
- Existing all-slot/all-fourteen-rotation save-sector regression at the new 992-byte width, plus journal, Adventure Log, seasons and ten grotto geometry/art checks.
- LegendsDex browser checks at 360/412/768/1280px: labels, equal-height chips, no old tag, Grotto region/method filtering, four exact seasonal shares, All Seasons, National Dex filtering, species details, no overflow or page errors. Reader/audio, 84 ordinary season views, 21 ordinary unions, 412 walkthrough methods and pinned seasonal-import regressions passed. All 157 ordinary maps, species and artwork stayed exact.
- Map/engine/wiki/profile generators reproduced the final checked source, including the resume scripts, without drift. CI runs the new production-C, native battery and browser checks.

## Save contract and limits

The separate signed/versioned/checksummed grotto extension appends at SaveBlock3 offset 716. Total size grows from 716 to 992 bytes inside the existing fourteen 116-byte sector tails. No persistent flag/var is reserved, no published IDs move, and expanded storage/native sectors retain their format. Each visitor stores the exact 80-byte native BoxPokemon; species, level, IVs, personality, ability and shiny identity are not rerolled on revisit. Native temp flag 5 only controls the visible object on these three appended maps.

The old-format fixture is synthetic absent-extension data written through real flash, not an authentic historical owner battery. Loss and other unusual outcomes were exercised through production C with engine mocks; interactive native battles cover escape, KO and capture. Native fixtures use a controlled all-badge level-100 player and animations off. The final 4,499 steps are accelerated through the production step function after one physical step. Natural full progression, every historical release, full-PC capture refusal and Pizza Boy were not independently played through here. Existing native capture/storage handling remains in use.

This work remains on draft PR #87. Public VERSION/downloads/BPS were not changed or published. Independent patch application, release metadata and publication verification remain required before shipping; passing these checks is not a claim that publication happened. Item-ball scenery remains its existing inspectable prop, with no new item award.

Remote CI follow-up: the initial project job stopped at the grotto art check because Pillow was installed later in the workflow. Moved the existing pinned Pillow install before the first image-dependent test. Local checks passed; remote reruns must be assessed from the current PR rather than inferred from local results.
