# Save compatibility between Legends updates

## Standing requirement

On 14 October 2026 the owner made backward save compatibility a requirement for future updates, superseding earlier permission to ignore older saves. Previously published Legends battery saves must continue into newer Legends releases, preserving Pokémon and their data, Bag/PC contents, story and map progress, gifts/reward claims, wardrobe choices, Options, clocks and seasons. Do not silently require a new game or remove a supported legacy reader. An incompatible change without a verified migration blocks publication.

This concerns the emulator's normal in-game battery save (`.sav`). Emulator save states capture the running ROM and are not the compatibility contract. The upgrade direction is older Legends → newer Legends; newer-format saves are not promised to load in older ROMs. Saves from unrelated hacks or arbitrary expansion configurations are outside this contract.

## Current verified baseline and limits

The current published baseline is v0.0.60, retaining the v0.0.59 research compatibility guarantees and adding the achievement extension detailed below. Native sectors, storage readers, the 36-byte journal and previously published identifiers remain intact. Research progress retains read-only B7 support and migrates to B8 only on successful state changes, with high completion bits in verified-unused var 0x407A. The v0.0.58/v0.0.59 sections below describe focused migration and native Continue coverage; [the current release QA](qa/research-v0.0.59.md) states its limits. The authentic historical-save matrix remains unfinished.

Historical v0.0.49 changed only front-facing cheek shading and required no save migration. The approved Side Part remains ID 2. Preserve [v0.0.49 evidence and limits](qa/front-face-v0.0.49.md) and the previous [v0.0.48 evidence](qa/side-part-v0.0.48.md).

| Area | Existing protection/evidence |
| --- | --- |
| Native sectors and appended history | `test/legends-item-descriptions.test.py` exercises shipped C across both slots/all fourteen rotations, legacy checksums, fixed history offsets, invalid sectors and failed writes. |
| Expanded storage | `test/legends-storage-codec.test.py` checks lossless compression, malformed/truncated data and capacity refusal under sanitizers. This codec test alone does not exercise migration or actual flash. |
| Journal, appearance, seasons, Adventure Log and clock | Their existing host tests cover legacy/default initialization and persistence rules using actual C logic with engine mocks. |
| Actual legacy migration and flash persistence | The [v0.0.43 native mGBA record](qa/journal-storage-v0.0.43.md) verifies the original fourteen-box layout migrating to twenty boxes with original Pokémon, names, wallpapers, fusions and inventory preserved, followed by new-format save/reload. It also records link-save paths, full boxes and recovery/refusal cases. |

The existing legacy decoder is in `src/legends_storage.c`; sector validation and slot recovery are in `src/save.c`. The expanded format was introduced in v0.0.43. Preserve both the original-format reader and the expanded-format reader. Its current packed header requires an exact `rawSize`: merely appending a field to `struct PokemonStorage` would invalidate old packed saves unless an explicit old-size decoder/migration is added.

A complete set of authentic saves from every historical release has not been replayed against the current published version. The policy is a release requirement, not a claim that this missing historical matrix is already verified. Retain existing evidence and extend a small reproducible fixture set when save-affecting work is undertaken.

## Birch request preview — v0.0.58

The six new requests reuse verified-unused native vars 0x406B–0x406D. A signed, bounded active word guards completion and habitat-note bits; invalid legacy values read as no request without writes and initialize only when accepting work. Quest IDs 33–38 are appended, while original quests, achievements, journal size/offsets, save sectors and packed-storage readers remain unchanged. The state words currently support sixteen requests; future expansion beyond that needs explicit additional-word initialization. Host tests covered every possible active-word value, legacy snapshots, one-active/abandon/retry, pin retention and atomic sample/reward behavior. Controlled native Debug flash/load and normal unmodified Release Continue with legacy/active/completed fixtures passed. [Detailed evidence and limits](qa/birch-v0.0.58.md) records the assertions; the authentic historical-release fixture matrix and Pizza Boy testing remain unfinished.

## Research expansion — v0.0.59

The extended catalogue retains v1 B7 reads and upgrades valid v0.0.58 state only at a successful mutation. One verified-unused native word 0x407A holds high completion bits; migration zeros them without reading arbitrary legacy values. Existing completion, active selection, observations, quest pins and IDs remain intact. Invalid legacy state initializes only on acceptance; full-PC failure leaves all state and inventory unchanged. The native structures, journal size/offsets, sectors and packed-storage codec are unchanged. Host tests cover v1/v2, all thirty requests, high-word bits, caps, gates and snapshots; controlled native flash and all six unmodified Release Continue fixtures passed, including the high completion word and the one-time Master Ball inventory. [QA and limits](qa/research-v0.0.59.md). [Design and migration](features/research-requests.md).

## Achievement extension — v0.0.60

The 130-achievement catalogue preserves original IDs 0–94 and all original definitions. The original 36-byte v1 journal stays at SaveBlock3 offset 652, with its checksum, earned/claimed arrays and tracked selection unchanged. A 28-byte separately signed/versioned/checksummed extension is appended at offset 688 for IDs 96–159; ID 95 uses the previously unpublished final legacy bit. Upgrading an old profile preserves its first 95 bits and pin, clears unpublished bit 95 and initializes only the absent extension. New goals backfill quietly without automatic rewards. Existing expanded-storage readers, capacities and sector geometry remain intact; no native var is reserved.

SaveBlock3 grows from 688 to 716 bytes within the existing fourteen 116-byte sector tails. Existing full/link/Hall-of-Fame/Frontier transactions copy that bounded tail and the packed inventory together. Normal and native tests must verify new high-ID claims and exact reward quantities survive flash/Continue. Continue using v0.0.60 or newer after saving new achievement progress; older versions do not know the appended achievements. [Current extension QA](qa/achievements-v0.0.60.md) records actual results and limits.

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

## Hidden grotto encounter extension — unshipped review

The owner requested persistent visitors and a per-grotto 4,500-step renewal after capture or defeat. SaveBlock3 appends 276 bytes at offset 716, growing to 992 bytes inside the existing fourteen 116-byte tails. The original prefix, native sectors, expanded storage format and all published IDs retain their positions. No persistent flag or native variable is reserved. Each room stores the exact native 80-byte BoxPokemon plus bounded species, level, season, state and remaining steps. A separate magic/version/checksum recognizes valid grotto data; absent/invalid legacy tail bytes initialize only this extension. Continue and New Game call the feature initializer.

Existing full/link/Hall-of-Fame transactions already cover every sector tail; the sector regression exercises all fourteen rotations/both slots at the larger width. The production-C grotto regression checks repeated initialization, untouched legacy prefixes, stable visitors, all battle outcomes and independent cooldown boundaries. Focused native flash/battle results and their limits are recorded in [grotto encounter QA](qa/grotto-encounters.md). The authentic historical-release save matrix remains unfinished; this extension does not claim to complete it.

## Dual Eon roamers — v0.0.75 candidate

The original single 28-byte SaveBlock1 roamer and all following native fields retain their exact width/order. A separate signed/versioned/checksummed 40-byte SaveBlock3 extension is appended at offset 992, bringing its size to 1,032 bytes within the existing fourteen sector tails. It holds the second roamer and a one-time unlock marker. The prior 992-byte prefix, flags/vars/IDs and both storage readers remain unchanged. Absent legacy data initializes only this extension; an existing post-TV first Eon that is resolved or marked seen backfills the opposite once. An active unseen first roamer waits for its first actual battle. Seen is a compatibility proxy because old saves have no exact first-encounter history. Existing original identity/HP/status and resolution are never regenerated. Valid new data retains partner capture/defeat across reload without revival. Host state and sector checks passed; focused native battle/flash/normal Release Continue verification remains pending in [QA](qa/eon-roamers-v0.0.75.md).
