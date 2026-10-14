# Evolving bedroom — v0.0.53 verification

The owner approved publication on 14 October 2026 after requesting removal of alternate chair styles in favor of color changes to the original chair: “You can publish after the removal of chair changes other than color.” The corrected poster was explicitly accepted. The alternate native chair shapes from the prior unpublished preview were removed before release. Publication results are recorded separately; this document describes the verified implementation.

## Native captures

- [Rooms and independent rug/bed colors](bedroom-native-room.png)
- [Original chair color choices](bedroom-native-chair-colors.png)
- [Decoration/color menu and off-rug doll](bedroom-native-menu.png)
- [Actual wood-floor placement confirmation](place-on-wood-prompt.png)
- [Decoration reached through the actual bedroom PC](decorate-from-bedroom-pc.png)
- [mGBA receipt](bedroom-preview-native.json)
- [Local builds/checks/save impact](bedroom-preview-local.json)

These are actual mGBA 0.10.2 frames, enlarged 2× nearest neighbor. Controlled callbacks prepared normal bedroom maps and story progress; real emulated button inputs used the decoration tasks. Captions are outside the game image. All runtime artwork comes from existing game assets. No generated furniture or replaced player assets were introduced.

## Resulting behavior

- The original wall map, bed, clock, GameCube, PC and wardrobe stay in place. One Ball Poster appears beside the map after the first filed Wing Survey report. Each lower poster half shares the original console metatile; the female poster sits left of the map so the books remain intact. The rug widens one tile toward the bed in each mirrored layout.
- Flowers appear after the first Hoenn badge, silver after Norman, gold after Hall of Fame. Home memories continue through bird reports, Regigigas, northern research, eight visiting Gym records, Faraway Island and Birch's closing letter. Captures are not required. Native notebook rules remain; additional memories may be declined. Mom's new comment is only in her ordinary healing branch, preserving native story/gift priority.
- The bedroom **PC → DECORATION** menu offers **RUG COLOR**, **BED COLOR** and **CHAIR COLOR**, each with Default, Blue, Rose, Mint, Gold, Plum and Coral. A applies only the selected material; B/Cancel preserves choices. Default keeps original colors. Original chair geometry, white bedding and furniture supports stay intact. No alternate chair styles, decoration inventory grants or extra doll slots remain.
- Existing dolls/cushions can use clear floor beyond the rug. Furniture, fixed keepsakes, saved decorations and functional approaches are protected. Flood-fill rejects placements that isolate previously reachable furniture/exit approaches. Full doll footprints cannot overlap existing objects. Saved dolls suppress conflicting new keepsakes without being moved/deleted. Off-rug dolls restore on entry. Secret Base controls/placement and rival room defaults remain unchanged.

## Save and palette design

No serialized structure, size, map/warp ID, item/decor ID, journal bitset, capacity or legacy reader changed. Verified-unreferenced native state variable 0x405C stores rug/bed choices with signature 0xB400. Variable 0x405F stores chair color with signature 0xCA00 and a validated 0–6 index. The unpublished style signature 0xC900 is rejected as Default, without writes; it was never a published save contract. Invalid/legacy values initialize visually to Default without mutation. Only explicit selections write choices. There is no migration or client patch-time step.

The generator copies native art into free cells of a private bedroom extension; shared source art is unchanged. Palette slots 1/2 isolate rug and bedding; 12 isolates the original chair. Desk support pixels that shared upholstery indices are remapped to fixed entries with identical original colors. Slots 3/4/5/11 retain native prop colors. Menu palettes 13–15 are untouched. Loading is limited to bedroom maps, honors unfaded-only reloads, and uses defaults in the rival's room. Existing native chair collision/elevation and PC interaction remain intact.

## Verification

- The first PR check failed because Pillow 11.3 encoded the generated PNG differently from local Pillow. Reproduced with the pinned CI package: exact indices, palette, dimensions and mode matched, while encoded PNG bytes differed. The determinism check now compares those exact art properties for PNGs and byte hashes for binary metatiles/metadata. Both local and pinned-Pillow focused checks passed; no ROM/art changes were needed.
- Actual-C host tests cover validated defaults, no implicit writes, independent materials, all seven chair colors in both layouts, invalid selections, rival/away isolation, repeated setup, map preservation, wider rugs, doll footprints, protected access and generator determinism.
- A native-tile compositor regression compares both Default chairs against their original native pixels, including PC supports. The emulator Default scenes also matched the prior native baseline byte-for-byte. Chair color changes affected only the upholstery rectangle in both rooms. Rug/bed comparisons changed no pixels outside those materials.
- Poster-on/off captures changed only the wall rectangle in both rooms, preserving both consoles and the female books. A metatile-word regression checks each original console. Keep this check: the earlier color-only comparison missed the poster bug.
- Actual emulated input selected Rose/Mint original-chair colors, canceled without mutation and restored Mint through real flash write/clear/load. Both save/load statuses were SAVE_STATUS_OK. PC interaction worked from both chairs, and the actual PC menu reached Decoration.
- Native input selected independent rug/bed colors, canceled, re-entered, and placed Pikachu Doll (77) on wood at (0,7). Color/doll records survived real flash write/clear/load. Female off-rug restoration was also captured.
- Debug and Release builds, project checks and BPS verification are pinned in the local/public receipts. All new notebook/family dialogue fits the actual normal font's 208-pixel width. Existing wardrobe, journal, save-sector, storage, appearance and seasonal checks are retained.

The prepared flash fixture is not an authentic historical-release battery save. A full historical save matrix, uninterrupted natural story/family traversal and Pizza Boy playtests remain broader QA work. Private ROMs are never committed or distributed.
