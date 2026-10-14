# C2 bedroom — native implementation preview

Status: **implemented on the review branch; not merged or published**. The owner selected C2, requested a Ball Poster, a wider rug, separate rug/bed colors in the bedroom decorate menu, and clear-floor decoration outside the rug. The original request retained review before publication. Production remains verified v0.0.52 at `ed88772110e0952c9e9c3887f1345ecabd4429c0`; no new BPS or website deployment is claimed.

## Review files

- [Native room/color examples](bedroom-native-room.png)
- [Native decoration/color menu and off-rug doll](bedroom-native-menu.png)
- [Native PC chair styles](bedroom-native-chairs.png)
- [Decoration reached through the actual bedroom PC](decorate-from-bedroom-pc.png)
- [Actual wood-floor placement confirmation](place-on-wood-prompt.png)
- [mGBA receipt](bedroom-preview-native.json)
- [Local builds/checks/save impact](bedroom-preview-local.json)

These are actual mGBA 0.10.2 frames, enlarged 2× nearest neighbor. Controlled callbacks prepared normal bedroom maps and story progress; real emulated button inputs used the decoration tasks. Captions are outside the game image. Native source artwork is retained; new private assets copy the required bedroom/Secret Base tiles, metatiles and palettes. No AI imagery or newly drawn furniture was used.

## Resulting behavior

- The original wall map, bed, clock, GameCube, PC and wardrobe stay in place. The single native Ball Poster appears beside the map after the first filed Wing Survey report. The rug widens one tile toward the bed in each mirrored layout.
- Flowers appear after the first Hoenn badge, silver after Norman, gold after Hall of Fame. Home memories continue through bird reports, the Regigigas intermission, northern research, eight visiting Gym records, Faraway Island and Birch's closing letter. Catching the birds/Regigigas/Mew is not required by the memory displays. Native notebook rules remain; the player can decline the additional memory pages. Mom's new comment is inserted only into her ordinary healing branch, preserving Match Call registration, Amulet Coin and story priority.
- The bedroom decoration menu, still accessed through the **bedroom PC**, gains **RUG COLOR**, **BED COLOR**, and **PC CHAIR**. Each has Default, Blue, Rose, Mint, Gold, Plum and Coral. A commits only the selected material; B/Cancel leaves choices intact. Default preserves the room's original blue/pink rug and original bed colors. White bedding and existing bed geometry remain intact.
- PC CHAIR offers Default plus all nine native one-tile chair styles: Small, Pokémon, Heavy, Pretty, Comfort, Ragged, Brick, Camp and Hard. These are cosmetic choices for the existing seat, available without consuming or granting decoration inventory. They preserve the PC desk supports, seat position and access, and use no doll slots. The list scrolls; A applies and B/Cancel preserves the saved style. The main menu uses 14-pixel rows so all seven actions fit above the description.
- Fixed the first preview's poster composition: each lower poster half now shares the original GameCube metatile rather than replacing it with blank wall. In May's layout the poster moved to the map's left, above the GameCube; the original books to its right are intact. The full map remains at its native location.
- Existing doll/cushion categories and twelve placement slots remain. They can use clear floor beyond the rug, including floor bordering the newly expanded carpet. Furniture, fixed keepsakes, existing saved decorations, the clock/wardrobe approaches and paths through the room are protected. A flood-fill rejects a new placement if it isolates a previously reachable furniture/exit approach. Large doll footprints cannot overlap existing saved dolls or furnishings.
- A saved doll suppresses an overlapping new keepsake; its record is never moved/deleted. The same floor eligibility is used during room re-entry so off-rug dolls return. Secret Bases and the rival's room do not gain bedroom-only controls or player-selected colors.

## Save and resource design

No SaveBlock structure, size, journal bitset, map/warp ID, item/decor ID, capacity or legacy reader changed. The formerly unreferenced Emerald native variable `VAR_LILYCOVE_CITY_STATE` (0x405C) is aliased as `VAR_LEGENDS_BEDROOM_COLORS`. No existing Emerald source/script references that state variable. The value has signature 0xB400 and separate 4-bit choices; bad signatures/out-of-range choices read as Default without writes. Only an explicit color selection writes it. Chair style uses the likewise unreferenced `VAR_EVER_GRANDE_CITY_STATE` (0x405F), signature 0xC900 plus a validated 0–9 style. Invalid/legacy values read as Default without writes. No existing script/source references either original variable outside the aliases. Only explicit chair selection writes it. This avoids a save format migration and any client patch-time step.

`tools/legends/build_bedroom.py` generates a private room tileset and uses tile cells unreferenced by the original room metatiles. Shared art and palettes remain unchanged. Unused bedroom BG palette slots 1/2 isolate rug/blanket colors; slots 3/4/5/11/12 hold native prop/chair colors. Palette 11 retains the original award colors and fills its unused indices with exact native floor/desk-support colors. The color hook runs only for the two bedroom maps. The rival uses native defaults. Palette loading honors unfaded-only reloads. Menu palettes 13–15 are retained.

## Verification

- Both Debug and Release compiled successfully. Full local project runner passed **48 executable blocks**; the final workflow included rival/away, raised-bed elevation, saved-overlap, blocked-access and native font-width cases. Build hashes/memory usage are in the local receipt.
- Focused tests execute the actual bedroom C with native map/palette data: signed legacy defaults, no implicit writes, independent choices, map/furniture coordinates, wider rug, invalid/border/furniture placement refusal, connectivity, old decoration suppression, rival/outside-map isolation, repeated setup and generator determinism.
- mGBA opened both actual maps, selected Rose rug/Mint bed and Plum rug/Gold bed through the real menu, canceled without changing the choices, and re-entered the room with the chosen appearance.
- A new poster-on/off native pixel comparison changed only its wall rectangle in both rooms, preserving the entire consoles and female books. The host regression also checks the lower metatile words against each original console. The earlier color-only comparison did not detect the poster bug; retain both checks.
- All ten chair choices passed actual-C tests in both layouts, including signed legacy defaults, collision/elevation preservation, invalid choices, rival isolation and repeated room setup. Native UI input selected Pokémon/Hard chairs, scrolled and canceled without mutation; Hard survived real flash write/clear/load. Actual PC interaction worked from both seats, and real PC -> Decoration navigation displayed the new controls.
- Pixel comparison found no changed scene pixels outside the rug/bed regions for either layout. Existing map/furniture/player art was unchanged across those color selections.
- The native menu placed Pikachu Doll (77) on wood floor at (0,7), then re-entry restored it. Real flash write -> clear color/doll RAM fields -> load returned SAVE_STATUS_OK and restored profile 0xB423 and the doll's item/position. The female off-rug restoration scene was also checked.
- All new notebook/family dialogue lines fit the actual normal font's 208-pixel width. Existing wardrobe/journal/save-sector/storage/appearance/season tests passed in the project runner.

The real flash fixture was prepared by the current private harness. It is not an authentic historical-release battery save, and no full historical matrix or Pizza Boy playtest is claimed. Natural story traversal of all notebook/family branches remains broader playtest work. Private ROMs remain outside the repository and are never distributed.

## Next step

Review these native visuals with the owner. After approval, prepare the next version and synchronized site/patcher/release notes, repeat only checks justified by further changes, and complete the ordinary native/BPS/Actions/Pages publication gates. Do not merge the design branch or replace public patches before approval.
