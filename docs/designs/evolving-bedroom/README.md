# Evolving bedroom — owner review

Status: **C2 selected with Ball Poster; native implementation preview awaits review.** Prepared from verified v0.0.52 master `ed88772110e0952c9e9c3887f1345ecabd4429c0`. The owner selected evolving bedrooms and requested designs/stages before implementation, extending through the current Kanto storyline. On 14 October 2026 the owner explicitly reiterated using existing game assets for world building; any newly designed artwork must be previewed separately first.

## Current implementation preview — C2 with Ball Poster

The owner selected C2, requested the native Ball Poster, a rug extending to the bed, separate rug/bed color controls in the bedroom decoration menu, and placement across clear floor where safe. These changes are implemented on the review branch. [Native screenshots, verification, save impact and limits](../../qa/bedroom-preview.md). The public v0.0.52 ROM/patches have not changed.

The wall map remains at its original position. C2 now uses the same Ball Poster throughout; Kanto reports and the finale also update home notebook memories and Mom's dialogue. Silver remains after gold is added. The original furniture, native color defaults, saved doll placements and reserved access tiles are protected. The color choices are Default, Blue, Rose, Mint, Gold, Plum and Coral. Placement supports the bedroom's existing dolls/cushions on available floor; it does not enable Secret Base-only furniture categories in bedrooms.

The following earlier design material is historical. In particular, prior C1/poster colors, three-poster/map replacement, glass ornament and A recommendation are superseded. Await review of the native implementation before merge/publication.

## Current review — revised C

The owner preferred **C — Champion display**, but identified that the posters covered the existing wall map and explicitly requested that the map remain displayed. This supersedes the initial A recommendation and the initial proposal to remove the map. Do not implement or republish those earlier overlapping poster arrangements.

- **C1 (recommended):** the original map stays exactly where it is. Two native posters flank it, one on each side. Gold and silver awards occupy the outer edge above Mom's flowers.
- **C2:** retain the same awards and map, but use only one native poster beside the map; it changes from green to blue at the finale.
- Norman's silver display remains after the Champion gold display is added. No glass ornament is proposed for revised C.
- C1 progression: first Gym victory adds flowers; Norman adds silver; Hall of Fame adds gold; the first filed Wing Survey report adds the green poster; Oak's final report plus Birch's closing letter adds the blue poster. Individual bird reports, Regigigas, northern research, all eight visiting Gym records and Faraway Island continue to add notebook/family memories in between. Bird captures are not required.
- Both layouts preserve the original map's full 16×32 native-pixel region. The generator asserts exact pixel equality for stages 0–6, both bedroom layouts and both variants (28 combinations). Existing furniture and original source assets remain unchanged. No collision, palette capacity, save-compatibility or gameplay verification is claimed by these static assertions.

[Revised C layouts](bedroom-c-revised-layouts.png), [revised stages through Kanto](bedroom-c-revised-stages.png), [revised C in both bedrooms](bedroom-c-revised-both.png).

## Historical first-round directions (superseded)

The following initial images remain as review history. Their three-poster layout removed the map and was rejected by the owner's follow-up. Use the revised C images above for current work.

## Original visual directions

- **A — Home with memories (recommended):** flowers, a small Hoenn award, three native research-themed posters and a native glass ornament. Staged additions retain the familiar room layout, colors, furniture, GameCube, clock, bed and wardrobe positions. The original small picture gives way to the completed report display; its memory stays in the notebook.
- **B — Cozy home:** flowers and the original picture; most changes appear in notebook entries and family dialogue. Least floor clutter.
- **C — Champion display:** gold/silver native shields instead of the glass ornament, with the research posters. More emphasis on awards.

[Directions](bedroom-directions.png), [Hoenn stages](bedroom-hoenn-stages.png), [Kanto stages](bedroom-kanto-stages.png), [both bedroom layouts](bedroom-both-layouts.png).

These are **static native-asset compositions, not emulator captures or verified gameplay**. They contain no AI imagery, new pixel art or invented furniture. Native source tiles, their flips and native palettes are composed with transparency and enlarged by exactly 3× nearest neighbor. The presentation captions are outside the game scene. Existing decorations stand in for story mementos; their proposed role does not grant the original Battle Tower/Contest achievement or withdraw an owned item. The posters are report displays, not bird feathers or capture trophies.

## Original proposed progression (superseded where revised above)

| Milestone in the existing game | Room / notebook / family change |
| --- | --- |
| Starting adventure | Original room. The existing notebook becomes the place to revisit home memories after the opening scenes. |
| First Hoenn Gym victory | Native flowers from Mom; first proud-parent line. Visual stage 1. |
| Defeat Norman | Silver display and a family note recognizing your growth. Visual stage 2. |
| Resolve Hoenn's weather crisis | Notebook entry about returning to a peaceful home; Mom's dialogue acknowledges it. |
| Enter the Hall of Fame | Gold replaces silver; earlier memories remain readable. Visual stage 3. |
| First Kanto arrival | A travel letter in the notebook and a new Mom response. No repeat arrival celebration. |
| First filed Wing Survey report | First native research poster. Visual stage 4. |
| File Power Plant, Seafoam and Mt. Ember reports | Three posters fill independently as reports are filed. Visual stage 5 shows all three. Observation/reporting suffices; catching a bird is not required. |
| File Hoenn Regigigas report | Birch/Steven expedition entry. No need to capture Regigigas. |
| File northern report; obtain all eight visiting Gym records | Separate northern-travel and eight-record notebook pages; both Gym difficulty modes count equally. |
| Visit Faraway Island | Voyage page, without claiming Mew was caught. |
| Final Oak report and Birch closing letter | Native glass ornament and a final family message. Visual stage 6. The completed room remains a place to return to. |

These are presentation stages, not a replacement story progression variable. Completed milestones should appear independently and out-of-order optional content must not regress other displays. No extra travel requirements, story gates or forced return-home scenes are proposed.

## Implementation constraints after approval

Apply these constraints to revised C; the original map must remain fully visible and pixel-identical in its original position.

- Derive keepsakes from existing badge/story flags. Kanto sources include `FLAG_LEGENDS_KANTO_WELCOMED`, `FLAG_LEGENDS_KANTO_SURVEY_REPORT`, `FLAG_LEGENDS_KANTO_SURVEY_POWER_REPORT`, `FLAG_LEGENDS_STORY_SEAFOAM_REPORT`, `FLAG_LEGENDS_STORY_WEATHER_REPORT`, `FLAG_LEGENDS_STORY_NORTH_REPORT`, `FLAG_LEGENDS_STORY_EMBER_REPORT`, `FLAG_LEGENDS_FINAL_EIGHT_RECORDS`, `FLAG_LEGENDS_FINAL_ISLAND_VISITED`, `FLAG_LEGENDS_FINAL_REPORT` and `FLAG_LEGENDS_FINAL_HOENN_EPILOGUE`. Verify each actual script contract when implementing.
- Keep saved structures, map/warp IDs, item/decor IDs, existing wardrobe choices and player decoration records unchanged. An existing progressed save should derive its earned displays on room entry, without item grants or migrations. This is a design objective, not a verified compatibility claim.
- The 9×8 bedroom layouts and existing furniture coordinates remain intact in these concepts. Display props use the outer right column in Brendan's home and outer left column in May's home. Do not alter the rival's bedroom or opening/moving-in scenes.
- **Player-placed decoration conflicts remain an implementation detail to resolve:** never move, delete or overwrite saved dolls/cushions. If a proposed prop overlaps an existing decoration, suppress that fixed prop and retain its notebook entry; placement-preview rules must agree. Native collision, event reachability, follower behavior and both genders require gameplay verification.
- Import only the required native decoration tiles/palettes into a private bedroom extension. Do not replace the room's tileset wholesale, recolor existing furniture or change shared Secret Base palettes. Palette/tile capacity must be checked before promising the exact composition.
- Preserve the existing notebook's beginner text and context; add readable memory pages without breaking the PC, wardrobe, clock or decoration menu. Family dialogue must respect higher-priority native story scenes and existing skin-tone logic.
- No new achievement IDs are proposed. The current 95-achievement catalogue has only one remaining reserved slot; do not grow its saved bitsets for this feature.
- After design approval: implement incrementally, check old-save backfill and idempotency, protect decorations, verify both bedrooms and collisions in mGBA, then provide actual native in-game previews before publication. Follow ordinary Debug/Release/build/BPS/site release gates at that point.

## Reproduction and review evidence

`python3 tools/legends/preview_evolving_bedroom.py` regenerates the four historical PNGs and three revised C PNGs and a source/output SHA256 manifest. Inspected the staged compositions, both bedroom variants and all three design options. Preview-only files do not enter ROM builds; VERSION stays 0.0.52. No new game build or BPS patch is claimed for this design milestone.

Next step: obtain the owner's review of revised C1/C2, then implement the approved design. The owner selected C as inspiration; that is not approval of this newly revised layout. No design or implementation publication approval has been inferred from the earlier v0.0.52 approval.
