# v0.0.63 seasonal encounters / DexNav preview QA

**Model: GPT-6 | Approach: dependency-focused encounter review, executable shipped-C checks and actual native mGBA GUI captures.**

Historical pre-correction record. The owner subsequently approved the roster/style and requested icon fitting corrections; [final geometry/capture evidence](dexnav-layout-v0.0.63.md) supersedes its visual-readiness status. The encounter proposal is unchanged.

Original status: preview ready on [draft PR #78](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/78). Owner approval, merge and game publication are pending. The public game remains v0.0.62. No ROM, private diagnostic ROM, ELF or save is included in these preview files.

## Design and dependency review

[The complete roster and rules](../features/seasonal-encounters.md) preserve every original grass resident year-round at a combined 70% base share, with two seasonal visitors at 20% and 10%. The sixteen tables retain native twelve-slot weights, per-slot levels and rate 20. Routes 101–104 only; both Route 104 halves share the table. The 32 visitors span Generations 1–9. This pilot is all-day, consistent with disabled time-of-day encounters.

The shared land resolver reads the committed active world season, so a pending season cannot change encounter data before the existing safe transition. Walking, Sweet Scent, local helpers, optional overworld encounters, DexNav list/levels/completion/hunts, Match Call hints and habitat maps use that resolver. Unrelated maps retain their baseline pointers. Water, fishing, Rock Smash, hidden-only data and native outbreak/roamer/Frontier priority remain intact. Original Birch research targets remain available year-round; Wally's forced Ralts tutorial and scripted starter/rescue battles are unchanged.

DexNav creates the real species' native two-frame party icon for unseen entries, then assigns a separately allocated black palette. Transparency, icon geometry and native callbacks remain intact. Known icons keep their shared original palettes. Empty X slots, name/type/search locks, detector selection and seen/caught data retain their behavior. Native map return frees sprite palettes. No approved artwork, wardrobe, sprite asset, serialized layout, saved field, variable allocation or persistent ID changed; no migration is required.

## Verified source and CI

Game implementation: `0808935e083010aef9daaf52ba934dff78357949`. Final executable QA source: `0a33a336a8211764bb87a34fc68a8e49fc8a5955`; later resumption changes only reconcile existing wiki work and add documentation/captures. The game source remains identical to the tested source.

| Gate | Verified result |
|---|---|
| [Project checks 39095843915](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39095843915) | Success, including new resolver/data and silhouette regressions |
| [Native builds / BPS 39095843909](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39095843909) | Debug and Release builds, canonical Emerald identity and both independent patch round trips passed |
| [mGBA 39095843918](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39095843918) | Unmodified Debug Quickstart, existing 23 Living Hoenn cases and all 19 seasonal/DexNav cases passed |

The source/C regressions cover all sixteen tables at all time-of-day values; exact native weights and 70/20/10 shares; resident preservation; 32 distinct visitors; levels/rates; committed versus pending season; bounds/fallbacks; unrelated-map pointer equality; and current versus absent prior-season DexNav target levels. Compiled icon-helper checks cover native species/callback selection, palette isolation, forms, empty/bounds/allocation guards and retained locks. These complement the actual-game checks rather than stand in for gameplay captures.

## Native captures

The ordinary Debug ROM SHA-256 was `185bb9dc9cd81d75c18775f968f93967896ffb8c22de3fa80e39d7eb1ecfd7cc`. mGBA native core 0.10.2 ran the actual compiled Legends GUI, sprite animation and wild generator. A private callback in a disposable copy established controlled route/season/seen fixtures. The unmodified base ROM hash was checked; only PNG/JSON/logs were uploaded in artifact `12124647019` (`legends-mgba-gameplay`).

Nineteen cases cover each route in all four seasons, all-unseen Route 101, all-land-seen Route 104 and southern Route 104. Each case created 256 actual wild Pokémon: 4,864 total, all in the active table and its level ranges, with both seasonal visitors sampled. Exact table checks establish rare resident availability; the random sample does not claim every 1% resident appeared. Checks also verified native icon image pointers and VRAM frames, both distinct animation frames, black silhouette colors, unchanged known palettes, real A-button rejection of an unseen target, closure, passable fixture placement and protected-state hashes after fixture setup.

All 38 native frames were visually inspected. The five phone-friendly PNGs retain original 240×160 gameplay pixels at 2× nearest-neighbor scale, with captions outside the captured image. The GIF loops two genuine captured states at an illustrative 500 ms interval; it is not a continuous recording. In the all-land-seen panel the unseen water Pelipper correctly remains black.

- [DexNav silhouette PNG](dexnav-silhouettes-v0.0.63-preview.png) · [native-frame GIF](dexnav-silhouettes-v0.0.63-preview.gif)
- [Route 101](route-101-seasonal-v0.0.63-preview.png) · [Route 102](route-102-seasonal-v0.0.63-preview.png) · [Route 103](route-103-seasonal-v0.0.63-preview.png) · [Route 104](route-104-seasonal-v0.0.63-preview.png)
- [Native receipt and harness hashes](seasonal-encounters-v0.0.63-native.json) · [capture provenance](seasonal-encounters-v0.0.63-previews.json)

Two early native runs stopped in the private checker before new captures: an inlined private level helper had no linker symbol, then a standalone `memcmp` was unavailable. QA-only follow-ups removed those assumptions and used a local comparator; game code did not change. The final run above supersedes those failures. Sampling no longer requires a rare 1% resident in 256 creations.

## Continuity and limits

Master advanced independently with wiki 1.7.0 and companion publication through `ced449c6e148310c021f70896840d37893c0185f`. Preserve all of that work when integrating this preview. Its preserved trial header matches this proposal, and its public Preview notice must stay until game approval/publication. No additional wiki redesign is part of this task.

These are controlled Debug cases, not a natural route/story playthrough, complete detector hunt, native Release interaction, authentic historical-save migration matrix or Pizza Boy coverage. Those broader playtests remain separate backlog items. Both build variants and BPS targets passed CI, but no v0.0.63 public download or Pages update has been published. After owner approval, recheck the live branch, run the normal merged release gates, publish both BPS files and verify live bytes/decoding. Then reconcile the wiki's preview status with the actual released game source without discarding its approved design.
