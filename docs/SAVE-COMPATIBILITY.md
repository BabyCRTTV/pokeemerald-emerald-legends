# Save compatibility between Legends updates

## Standing requirement

On 14 October 2026 the owner made backward save compatibility a requirement for future updates, superseding earlier permission to ignore older saves. Previously published Legends battery saves must continue into newer Legends releases, preserving Pokémon and their data, Bag/PC contents, story and map progress, gifts/reward claims, wardrobe choices, Options, clocks and seasons. Do not silently require a new game or remove a supported legacy reader. An incompatible change without a verified migration blocks publication.

This concerns the emulator's normal in-game battery save (`.sav`). Emulator save states capture the running ROM and are not the compatibility contract. The upgrade direction is older Legends → newer Legends; newer-format saves are not promised to load in older ROMs. Saves from unrelated hacks or arbitrary expansion configurations are outside this contract.

## Current verified baseline and limits

v0.0.49 changes only front-facing cheek shading and does not change save fields, the storage format or saved IDs. No save migration is needed. The approved Side Part remains ID 2. Existing compatibility checks passed; see [v0.0.49 evidence and verification limits](qa/front-face-v0.0.49.md) and the previous [v0.0.48 evidence](qa/side-part-v0.0.48.md).

| Area | Existing protection/evidence |
| --- | --- |
| Native sectors and appended history | `test/legends-item-descriptions.test.py` exercises shipped C across both slots/all fourteen rotations, legacy checksums, fixed history offsets, invalid sectors and failed writes. |
| Expanded storage | `test/legends-storage-codec.test.py` checks lossless compression, malformed/truncated data and capacity refusal under sanitizers. This codec test alone does not exercise migration or actual flash. |
| Journal, appearance, seasons, Adventure Log and clock | Their existing host tests cover legacy/default initialization and persistence rules using actual C logic with engine mocks. |
| Actual legacy migration and flash persistence | The [v0.0.43 native mGBA record](qa/journal-storage-v0.0.43.md) verifies the original fourteen-box layout migrating to twenty boxes with original Pokémon, names, wallpapers, fusions and inventory preserved, followed by new-format save/reload. It also records link-save paths, full boxes and recovery/refusal cases. |

The existing legacy decoder is in `src/legends_storage.c`; sector validation and slot recovery are in `src/save.c`. The expanded format was introduced in v0.0.43. Preserve both the original-format reader and the expanded-format reader. Its current packed header requires an exact `rawSize`: merely appending a field to `struct PokemonStorage` would invalidate old packed saves unless an explicit old-size decoder/migration is added.

A complete set of authentic saves from every historical release has not been replayed against v0.0.48. The policy is a release requirement, not a claim that this missing historical matrix is already verified. Retain existing evidence and extend a small reproducible fixture set when save-affecting work is undertaken.

## Review every update

State the save impact in the PR/handoff, including “none” when appropriate. Check for changes to:

- Serialized structures, field offsets/widths/alignment, bitfields, capacities, checksums, encryption, codec/header formats and configuration switches that alter any of them.
- Saved identifiers: species/forms/moves/items, flags/vars, graphics and wardrobe choices, map groups/numbers/warps, quests/achievement indices and reward-claim bits. Preserve their meanings; do not renumber or reuse published IDs without migration.
- Continue/new-game initialization, one-time grants and progression gates. New features must initialize missing data once, retain the player's existing choices and avoid duplicate rewards or story softlocks.

Prefer stable layouts and unused reserved space when that preserves the serialized contract. Validate legacy signatures/versions rather than assuming unused bytes are zero. Where a format must change, recognize the old format explicitly, convert without discarding data, initialize only new fields and retain supported readers. Test repeated initialization and save/reload so a migration cannot reapply gifts or reset settings. Preserve the last valid save if conversion or writing fails; do not turn an unsupported/corrupt payload into a silent empty profile.

Upstream merges and expansion configuration changes receive the same review as Legends features. Passing a build or creating a valid BPS patch does not establish save compatibility.

## Keep routine patch time small

The existing [project-check workflow](../.github/workflows/legends-checks.yml) already runs the relevant host tests. Reuse those steps; do not add a second full suite, another native build, or a full historical emulator matrix to each artwork/text update. Seven focused existing suites (item history/sectors, storage codec, journal, appearance, seasons, Adventure Log and clock) passed during adoption of this policy; they take seconds locally, excluding setup. The policy adds no ROM data, migration executed per frame, patch-format change or client-side patching step.

When saved data or progression semantics change, add the smallest regression that catches the actual risk. Use deterministic synthetic fixtures where possible. Keep fixtures/provenance tied to their source version; avoid personal saves and never commit full ROMs. For a schema/codec/sector migration, also validate an older-format battery save in the new native build, then save, reset and Continue again. Compare affected Pokémon/inventory/progress/settings before and after; cover non-default wardrobe and season values, repeated initialization, and relevant failure/recovery paths. Exercise Release and Debug when their behavior differs, reusing the normal builds.

Record source version, fixture provenance, target commit, build/emulator, assertions and limits in a linked QA note. Reuse established format fixtures instead of retesting every art-only version. Build out the historical matrix incrementally: original fourteen-box saves, v0.0.43 expanded saves and a current pre-update save, with mid-story/postgame coverage. Do not mark an upgrade path verified until its load → migrate → save → reload result is observed.

## Updating a player's ROM

Keep a backup of the in-game battery save before updating. Apply the new BPS to the supported clean Emerald base, then have the emulator use that existing battery save with the new ROM (matching its save filename or importing the save as required). Use Continue and make an in-game save. v0.0.43 and newer use the expanded storage format, so retain the backup if returning to an older ROM.
