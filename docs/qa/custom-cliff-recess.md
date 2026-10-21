# Custom recessed cliff entrance

Owner selected A as the starting point and explicitly requested a high-quality custom asset. This review replaces only Stillwater's two mouth metatiles, keeping the existing landing, collision, inspection script, return coordinate, other exteriors and all interiors.

## Art and integration

The authored overlay is 16×32 native pixels, with an asymmetric near rock cheek, offset overhang, deep cavity, dim far inner wall and diagonal threshold. Existing Fallarbor palette 11 supplies every color. The surrounding native cliff texture is retained outside the aperture. Source authoring is reproducible in `tools/legends/build_custom_cliff.py`; the indexed overlay export is `data/tilesets/legends_grotto/cliff_recess_overlay.png`.

Eight previously unreferenced 8×8 cells in a sibling atlas hold the custom overlay. Allocation excludes every original metatile reference and all secondary animation DMA ranges found in the engine. Every other indexed pixel and the complete original palette are checked against the active Fallarbor base atlas. Two metatiles append at `0x375–0x376`; existing definitions/attributes remain exact prefixes. Only Route 114 `(13,39–40)` references the new art. Existing map/layout IDs, save layouts and original collisions remain intact; the mouth stays solid and the landing `(14,40)` remains passable.

The active header now points to the sibling custom atlas/metatiles/attributes. The existing lighting generator builds its accepted Fallarbor assets first, calls the custom builder, then records these three redirects in the normal manifest. This preserves the original native and lighting sources and makes full lighting regeneration reproducible. Regenerate using `build_cliff_entrance_options.py`, `build_night_lights.py` (includes custom builder), then `build_grotto_review.py`. No palette changes or emissions were added. Other routes using Fallarbor retain identical referenced pixels/definitions.

## Verification

- Debug and Release built successfully; hashes are in the accompanying JSON.
- Ten focused grotto tests passed, covering the map exception allowlist, approved scenery, native guard, actual landing adjacency and new free-tile/prefix/palette invariants.
- Existing night-light source reproducibility and real DNS color mixer checks passed after the custom pipeline integration.
- Native mGBA checked the full active compiled metatile array against ROM bytes, then passed twelve seasonal scenes and three production exit/decline/reentry paths. The real cliff walk film now uses the custom asset mapped in the production review source. Three historical alternatives also passed their private landing/inspect/decline/entry fixtures.
- Inspected the actual custom exterior, native A/custom comparison and enlarged detail. User-facing previews contain actual compiled Debug ROM frames; crops/enlargement are nearest-neighbor and text is outside the game image. The clip records 165 original frames through approach, prompt, decline and entry. Native original frames/assertions/receipt are retained in `docs/designs/hidden-grottos/custom-cliff/`.

This remains draft PR #87 visual review, not publication or a claim of full story/old-save/Release-emulator/Pizza Boy testing. Capture rewards and persistent refresh contents remain unfinished. VERSION, public BPS, wiki and site are unchanged.
