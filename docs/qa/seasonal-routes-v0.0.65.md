# Seasonal Routes 109–112 — v0.0.65

**Model: GPT-6 | Approach: append native encounter tables and extend focused regression coverage.**

Status: implementation in verification; not published. Source baseline: `5ad991d66944ceb7d6a60afef8dfedd1862017fd` (verified live master). [Roster/rules](../features/seasonal-encounters.md) · [Source receipt](seasonal-routes-v0.0.65-source.json).

Route109 Surf and Routes110 grass/111 desert/112 grass add sixteen tables and 32 visitors across Generations1–9. All original residents remain year-round. Native per-slot levels/weights and encounter rates are exact, including desert rate10. Species distributions and species-level ranges can change with their slots. Earlier32 seasonal tables/mappings are identical. Core committed-season resolvers, native method tables, art, save layouts and IDs are unchanged.

The executable shipped-C regression checks all48 tables, every time of day, current-vs-pending seasons, invalid bounds/fallback pointers, and absent prior-season DexNav targets. The importer CLI checks all48 tables and historical16-table reimport, preserving native entries and removing stale future variants. Native harness preserves previous68 scenes and appends34: mixed/seen states for each new route/season and two unseen locks (102 total;26,112 real creations when passed). Route111 uses native passable desert terrain and rate10. Actual native captures, build results and public receipts will be recorded after execution.

No natural story playthrough, full detector hunt, historical-save migration, Release interaction or Pizza Boy verification is claimed. No new saved state requires migration.
