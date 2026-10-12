# Quest Log, achievements, storage and carried-over visual fixes — v0.0.43

## Validation

- Debug and Release compile locally with GCC 13.2.1 and the established Release LTO configuration. Linked memory: Debug EWRAM 254,404 bytes / IWRAM 28,376 bytes; Release EWRAM 254,406 bytes / IWRAM 28,324 bytes. Both remain within hardware limits. ROM remains below 32 MiB. Existing upstream warnings remain.
- All 40 project regression commands pass, including browser BPS patcher tests. The journal suite executes all 33 quest completions and 80 achievement definitions, old-profile initialization, permanent unlocks after stat reset, full-PC retries, claim idempotency and link guards. The bounded codec suite runs five input patterns, tiny and full payloads, malformed/truncated tokens and capacity refusal under address/undefined-behavior sanitizers.
- The sector suite executes the shipped C item flags, checksum validator and sector writer across both slots and all fourteen rotations. It covers original field offsets, complete data/tail copies, legacy final-sector lengths, invalid sector IDs, checksum corruption and failed writes. Existing story, native field-move, weather, starter, wardrobe, appearance, Adventure Log and item-description suites continue to pass.
- mGBA **0.10.3**, isolated QA profiles and controlled native callback/flag/map setup: open the pause menu with controller input, switch to its second page, enter Quests, inspect objectives, change to Side Quests, return, enter Achievements and claim a berry reward using A. The game displays “Berries sent to PC ITEM STORAGE!” and sets exactly that claim bit.
- Actual flash save/load preserves the expanded inventory, a Pokemon in Box 20's final slot, journal claim bits and the received berries. Reclaim is refused after reload. Normal saving, direct SAVE_LINK, incremental full link saving and the formerly partial link-save entry point all reload the entire expected PC/inventory payload byte-for-byte.
- Populate all **600 slots** with distinct native generated Pokemon, random IVs, varied species/levels and personalities. Packed payload in the reviewed profile is approximately **25.5 KiB** within the 35,696-byte budget; actual flash save/load returns every byte unchanged. This sample does not establish a worst-case capacity guarantee for every possible collection.
- Damage the newest packed integrity hash while retaining a valid native sector checksum. Loading recovers the previous complete slot, reports the native recovered-save status and restores that earlier inventory byte-for-byte. Convert both slots into the authentic original fourteen-box layout and legacy inventory fields: migration preserves all 420 original Pokemon slots, names, wallpapers, fusions and original Bag/PC entries, initializes six empty boxes, and survives a subsequent new-format save/reload.
- An intentionally incompressible private QA payload is refused before flash writing. Both saved slots and all current RAM bytes stay unchanged. It is a defensive format-boundary test, not a legal Pokemon collection.
- Open the native storage UI and select **BOX20**. Enter an ordinary native wild battle with selected hair/outerwear, advance its introduction with controller input, choose RUN and return to the field. The local player cache is rebuilt after battle. These are functional entry/exit checks, not a gameplay-balance test.
- The sparse style/footwear suites cover all 212 native pose-table slots. Add a regression proving a single relative-frame descriptor and an explicit 18-frame walking table produce identical pixels with hair/color/footwear and no coat. This fixes the mixed-up frames found during live native visual review.
- Native wardrobe previews show May with NONE/GREY/BLACK leggings beneath boots, Winter outerwear and the shoulder hair-tip removal. Walking pose sheets cover both leggings choices with None/Navy/Winter coats. Female neutral gray/black uses existing palette colors; head/eyes, male art, costumes, and diving palettes remain protected by the existing checks.
- Night art checks reproduce assets, compare native daytime cells, audit free tile/palette locations and animation DMA exclusions, and run the shipped DNS mixer. Native screenshots review Petalburg, Rustboro, Fortree, Pallet and Viridian. Standard house windows include both the upper and lower panes; Center/Mart lettering uses authored pink/red emission. Town-specific window masks are included.

## Review images

- [Second pause page](pause-journal-v0.0.43.png)
- [Quest objectives](quest-detail-v0.0.43.png)
- [Claimed berry reward](achievement-reward-v0.0.43.png)
- [Box 20](box20-v0.0.43.png)
- [May: Grey leggings](leggings-grey-v0.0.43.png)
- [May: Black leggings](leggings-black-v0.0.43.png)
- [Standard night windows and Center sign](night-petalburg-v0.0.43.png)
- [Native battle return](battle-return-v0.0.43.png)

## Limits and release checks

Full playthroughs of both regions, every achievement under organic play, every wardrobe combination in every map/weather, link sessions between devices and a complete Battle Frontier/Contest run remain broader playtesting. UI/emulator checks use controlled native setup where stated; do not present them as full unassisted playthroughs.

The expanded format is forward-only: after saving in v0.0.43, use this version or newer. Compression retains the existing flash budget and both save slots; an unusually incompressible collection may be refused without changing saved data. See [save-format details](../features/quest-log-achievements.md).

Publication is complete only after GitHub's Release/Debug build workflow independently verifies the clean vanilla Emerald SHA-1, reapplies both BPS patches, byte-compares each result with its compiled ROM, and deploys Pages. Public downloads contain patches and checksums only.
