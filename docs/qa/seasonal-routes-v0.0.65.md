# Seasonal Routes 109–112 — v0.0.65

**Model: GPT-6 | Approach: append native encounter tables and extend focused regression coverage.**

Status: merged after all PR gates passed; production/native/public verification pending. Source baseline: `5ad991d66944ceb7d6a60afef8dfedd1862017fd` (verified live master). [Roster/rules](../features/seasonal-encounters.md) · [Source receipt](seasonal-routes-v0.0.65-source.json).

Route109 Surf and Routes110 grass/111 desert/112 grass add sixteen tables and 32 visitors across Generations1–9. All original residents remain year-round. Native per-slot levels/weights and encounter rates are exact, including desert rate10. Species distributions and species-level ranges can change with their slots. Earlier32 seasonal tables/mappings are identical. Core committed-season resolvers, native method tables, art, save layouts and IDs are unchanged.

The executable shipped-C regression checks all48 tables, every time of day, current-vs-pending seasons, invalid bounds/fallback pointers, and absent prior-season DexNav targets. The importer CLI checks all48 tables and historical32/16-table reimports, preserving native entries and removing stale future variants. Native harness preserves previous68 scenes and appends34: mixed/seen states for each new route/season and two unseen locks (102 total;26,112 real creations when passed). Route111 uses native passable desert terrain and rate10. Actual native captures, build results and public receipts will be recorded after execution.

No natural story playthrough, full detector hunt, historical-save migration, Release interaction or Pizza Boy verification is claimed. No new saved state requires migration.

## Source and native evidence

[PR #81](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/81), final compiled source `2f9ccc8c8f42338e3755a6c776aaf12a5d1b3365`. Full project checks **39219001418** and native mGBA **39219001558** succeeded. Native retained Quickstart and23 previous Living Hoenn scenarios, and passed all102 seasonal/DexNav scenarios (26,112 actual wild creations). Screenshot artifact12170119379 ZIP SHA-256: `ea8a61507c8c4c63cf136d09115ebe04a1ceda853e18a08a516c28fe9410e350`. Normal Debug ROM SHA-256: `fb24e26d40d44e0eeaa9fef4ffdafed32c6949ef23d582ed8f98fb52b3826fbd`.

All54 new captures were visually reviewed; all105 previous captures matched v0.0.64 production pixels exactly. This is105 pixel regressions plus54 fresh visual inspections, not159 fresh visual inspections. Hardware-sampled icon checks covered the entire visible grid. New UI modes/methods are passed through the private mailbox rather than inferred from scene numbers. [Native receipt](seasonal-routes-v0.0.65-native.json) · [Preview provenance](seasonal-routes-v0.0.65-previews.json) · [Phone preview](seasonal-routes-v0.0.65-preview.png) · [Two native animation states](seasonal-routes-v0.0.65-preview.gif). The owner was shown the actual-game preview before publication.

[Route109](route-109-seasonal-v0.0.65-preview.png) · [Route110](route-110-seasonal-v0.0.65-preview.png) · [Route111](route-111-seasonal-v0.0.65-preview.png) · [Route112](route-112-seasonal-v0.0.65-preview.png). Captions are outside gameplay; images preserve exact2x nearest-neighbor native pixels. GIF timing is illustrative, not a continuous recording.

## Merge checkpoint

PR #81 merged as `a2f494be367077246640397d7aef0a7c19980667`. Both PR builds, canonical-base identity and independent BPS round trips passed in **39219001427**. Production project checks **39220172442** passed, including the stronger 48/32/16-table importer regression. Production build/publication **39220172592** and native **39220172611** remain in progress at this checkpoint. The related Birch Route110 Electric and Route111 Ground surveys retain native resident options in every season; Devon's Route109 water survey and native fishing proofs remain available. No quest/script priority, reward, ID or saved-state changes were made.
