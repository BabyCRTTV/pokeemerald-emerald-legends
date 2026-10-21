# Grotto visual cleanup and discovery review

Unshipped second review on v0.0.68. Owner requested tidier, convincing spaces and a demonstration of finding/entering a grotto. No approval to merge/publish has been given.

## Repairs and scope

- Replaced single `0x017` tree bottoms with complete four-cell native trees; regression checks every crown/trunk assembly and rejects orphan bottoms.
- Built complete native reflective shorelines with an irregular inset for Rainroot, and coherent native Scorched Slab cave banks, wall corners and a stepped northern recess for Stillwater.
- Borrowed native vines, a palette-matched Fallarbor cave opening and the complete Fortree undergrowth cluster to make three route entrances visible. Exactly ten route cells differ from published v0.0.68. A pinned patch allowlist restores all ten old words and checks the original full-file hashes, retaining every other collision/metatile. Existing route scripts, events and warps are unchanged except the explicitly added entrance background interactions.
- Rainroot's safe return is directly below its opening, `(27,106)`; the original leftover tree bottom below the replacement undergrowth was removed with native grass. Both halves of Leafshade's vine-framed trunk accept A.

## Actual bug found and repaired

The first revised native test walked Up into reused open-vine art and entered a native Secret Base before A could run the grotto script. `TryDoorWarp` normally treats every open Secret Base behavior as an auto-warp; absent a matching base background event, that path can use stale base state.

`LegendsGrottoIsEntrance` now excludes exactly four coordinate/map combinations from that auto-warp, leaving them to their Examine/Yes/No background scripts. The actual compiled C predicate was probed across all 65,536 map IDs and all 64×160 coordinates on each target route. All unrelated positions—including every existing native Secret Base location—return false and retain the original engine path. Native gameplay then passed holding/pressing toward all three openings, prompt cancellation and real reentry. No borrowed tile behavior, global Secret Base reader, tileset pointer, native door callback or save data was changed.

## Validation

- Local native Debug and Release builds completed. [ROM/frame/presentation hashes](hidden-grottos-polish.json).
- Native mGBA 0.10.2 passed twelve seasonal scenes; actual visitor graphics, active seasons and passable player positions were checked. Real input approached each Spring visitor, closed dialogue, walked out, declined an entrance and reentered all three grotto maps.
- Captured 176 original frames at ten frames per emulated second while actually walking three tiles through Petalburg Woods, examining the vines, advancing the clue, choosing Yes and fading into Leafshade. The private callback only establishes the initial approach fixture. The film's GIF coalesces identical frames and uses a shared 256-color palette; original still PNGs retain exact native RGB.
- Native Quickstart smoke passed. Five focused regressions passed, plus existing calendar/seasons, all 84 encounter tables and eight Kanto event-script checks. This is targeted review validation, not a natural uninterrupted story journey, historical-save matrix or Pizza Boy reproduction.
- [Refined interior sheet](../designs/hidden-grottos/Emerald-Legends-Grottos-Refined-Preview.png), [three native entry prompts](../designs/hidden-grottos/Emerald-Legends-Grotto-Entrances.png), [continuous native discovery clip](../designs/hidden-grottos/Emerald-Legends-Grotto-Discovery.gif), [frame hashes](../designs/hidden-grottos/verification.json) and [native assertions](../designs/hidden-grottos/emulator.log).

Capture battles, rewards, refresh timers and stable persistent contents remain unimplemented in this exploration review. No BPS application, new public release or wiki/site publication was performed. VERSION and published downloads remain v0.0.68. Keep ROMs, temporary instrumented binaries and private save fixtures out of Git/artifact uploads.
