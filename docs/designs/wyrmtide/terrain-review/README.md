# Wyrmtide terrain review, 5 November 2026

Actual compiled Legends Debug v0.0.70 plus unshipped Wyrmtide, running in mGBA 0.10.2. Public v0.0.75 is unchanged. Visual approval of the new shore/descent remains pending; the earlier Regidrago Heart was approved and remains byte- and capture-exact.

## Visual audit and changes

| Inconsistency | Corrected composition |
| --- | --- |
| Tree and boulder metatiles overwrote shoreline caps, leaving square land bases in the surf | Restored the complete native shore cells and placed native sand-backed trees/rocks wholly inland |
| Cliff caps and faces were stretched into a large rectangular entrance wall | Used the original vanilla Desert Ruins 5-by-4 rock geometry, native sand feet and existing two-cell seal opening |
| Free-standing columns introduced another material and scale at the entrance | Removed those columns and used matching coastal rocks and grouped vegetation |
| Long repeated stair strips extended beyond their stone ledges | Used short two-cell flights meeting complete ledge tops and feet |
| The final landing had oversized water rectangles and floating wall strips | Used a dry stone procession toward the approved dry Heart |
| A return-stair surround isolated a depth-tablet approach during development | Opened its side approach, retained the intended stair entry and added a source reachability assertion |

The four descending walking routes cross 6/4/6/6 native stair cells. The tidal gallery has one short flight plus its exit; the other landings have two short flights plus their exits. Native walking is verified with controller input, not a map render.

## References

- Vanilla Emerald: complete Route 111 Desert Ruins/Regi facade, Route 105 coastal entry, Dewford/Route 106 shore setbacks, and Sealed Chamber rock ledges. The upstream [Route 111 map blob](https://github.com/pret/pokeemerald/blob/master/data/layouts/Route111/map.bin) `4ce11a8a9a7b63ca3c0b2cdb4bddc9a35b32f9d8` is byte-identical to the protected local native layout. Its rock geometry is reused with the existing beach surround and closed-seal state.
- [Emerald Crest official gallery](https://thatsimpledev.itch.io/emerald-crest): reviewed the outdoor forest/town screenshots for vegetation grouping, consistent ground transitions and coherent material use. This is a visual reference, not imported Crest artwork or a claim of inspecting its paid source/tileset files.
- [Gaia creator gallery](https://www.sphericalice.com/romhacking/hacks/gaia/screenshots/): catalogued shrine/tunnel references, but its direct image fetches were unavailable in this runtime; no Gaia pixel-level verification or asset reuse is claimed.

AGENTS.md now records the owner's standing preference to reference vanilla and polished hacks, especially Emerald Crest, during map and tileset work. Existing shared artwork and palettes remain unchanged.

## Verification and limits

Debug compilation, existing production-C flag/gate/ID/art/topology checks, the native full Wyrmtide call/voyage/clues/seal/stairs/battle/retry/capture/flash/report/return suite and normal unmodified Debug Quickstart all passed for the final exact ROM. All four maps were walked both ways; both depth inscriptions and the final inscription were read. The approved Heart's source and native chamber capture remain exact. [Receipt](../../../qa/wyrmtide-terrain-review.json).

This is a review branch, not a release. It still requires reconciliation with current master, Release/current candidate patch gates and owner visual approval. No authentic historical-owner-save, natural full-story, Release gameplay or Pizza Boy claim. The old visual-repair receipts remain historical.
