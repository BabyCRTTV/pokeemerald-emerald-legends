# Quest Log, achievements and expanded storage (v0.0.56)

Press **Right or Left** in the pause menu to reach its second page. Choose **QUEST LOG** or **ACHIEVEMENTS**; the Adventure Log remains on the first page. Linked-room menus retain their native restrictions.

## Interface

The owner-approved A layout keeps six entries visible. MAIN / SIDE / DONE quest tabs and ALL / READY / CLAIMED achievement tabs show the active view. READY means unlocked rewards that have not been claimed; DONE shows completed quests. The top-right counter shows the selected entry and view total. Alternating paper rows, a plum selection band, cream selected text and a separate pointer distinguish selection from the completion checkbox. C remains the claimed-reward marker. Both control lines fit within the screen. Details retain all existing objectives, progress, rewards and claim messages.

## Quests

There are 33 entries: 26 main quests and seven basic side quests. Main quests cover Hoenn's introductory journey, all eight badges and major story errands, the Pokemon League, the nine current Wing Survey chapters and the Sleeping Continent intermission. Side quests cover the remaining visiting Leaders, a bicycle, Secret Power/base registration, the Scanner, ancient Regi doors, catching the three birds and catching Regigigas. These entries document existing gameplay; they do not add new story events.

- **Up/Down:** select an entry.
- **A:** open its objectives.
- **Left/Right or SELECT:** Main Story / Side Quests / Completed.
- **L/R:** move six entries at a time.
- **B:** back, then close. **START:** close directly.

Checks come from the same native flags used by the story. Later main-story completion flags also recognize earlier mandatory objectives on older saves. Future chapters stay hidden until relevant progress opens them. Completed entries remain readable. Optional bird captures and the titan capture remain side quests, separate from observation/report completion.

The initial catalogue is in `data/legends/quests.json`, with the shipped C table in `src/data/legends/journal.h`. Keep both synchronized when authoring more quests. No player-managed checkbox or fabricated completion state is used.

## Achievements and rewards

There are **95 achievements**, listed in `data/legends/achievements.json`. Each has a title, explicit requirement, progress target and a bundle of three or five berries. Rewards cycle through 45 berry varieties, including healing, condition, EV-reducing, type-resistance and rare stat berries. No full-party or random-item reward is substituted.

Open a detail page and press **A** to claim. Berries are added directly to **PC ITEM STORAGE** through the native atomic item API. The claim bit is set only after that addition succeeds. If storage is full, the reward remains pending. Claims cannot be repeated after a successful save/load. A successful claim shows a temporary **REWARD CLAIMED! / Sent to PC ITEM STORAGE.** confirmation. Unlocking an achievement alone never grants its reward. Save your game normally to keep the reward; loading an earlier save rolls both the berries and claim state back together.

All / Ready to Claim / Claimed views are available. An achievement stays unlocked after a streak resets. Stat milestones are captured by the native `SetGameStat` hook, story milestones by flag transitions, and collection milestones by newly caught Pokédex entries. The journal also refreshes on returning to the field, opening the journal and saving. A compact upper-left notice names new unlocks for about three seconds without consuming input; simultaneous unlocks queue. Notices wait through scripts, fades, menus, battles and location banners. Existing profiles recover achievements quietly from their retained flags, statistics and caught-species records, without replaying old banners or auto-claiming new rewards. Feats absent from those records cannot be reconstructed.

IDs are stable array positions. Append new achievements; do not reorder existing IDs. The reserved bitset supports 96 entries. Journal data is appended after the existing item-history field in SaveBlock3 with its own version/magic/checksum; existing field offsets remain unchanged.

## Storage capacities

| Storage | Before | v0.0.43 |
| --- | ---: | ---: |
| Pokemon boxes | 14 / 420 Pokemon | 20 / 600 Pokemon |
| PC item storage | 50 slots | 150 slots |
| Bag Items | 30 slots | 150 slots |
| Bag Key Items | 30 slots | 60 slots |
| Bag Poke Balls | 16 slots | 32 slots |
| Bag TMs/HMs | 64 slots | 128 slots |
| Bag Berries | 46 slots | 80 slots |

Native per-stack quantities, pocket rules, registration and field-move progression remain in use. The Battle Pyramid's challenge bag keeps its separate native limits. Boxes retain the native 30-slot layout, naming and wallpapers.

## Save format and compatibility

Emerald uses a 128 KiB flash save with two rotating fourteen-sector slots. A larger raw PokemonStorage does not fit the original nine PC payload sectors. Legends therefore packs the expanded PC plus Bag/PC item inventories into a **bounded lossless stream** in those same sectors. It reversibly normalizes each boxed Pokemon's encryption before packing and restores the original encrypted bytes immediately afterward. No Pokemon fields, nicknames, OT data, IVs, EVs, ribbons, fusions or inventory entries are intentionally dropped.

A packed header records the format marker, exact raw size, payload length and FNV-1a integrity hash. The reader checks token bounds and integrity before accepting a packed save. Each physical sector also retains its native checksum/signature/counter. An invalid packed payload can recover from the previous intact slot. Normal, link, Hall of Fame and Frontier transactions include the complete packed inventory payload so berry rewards and claim bits remain consistent.

Earlier Legends saves are recognized by the original 14-box sector format. The reader preserves all original boxed Pokemon, box names/wallpapers, fusion slots, and all original Bag/PC slots, then initializes six empty boxes and expanded inventory space. Subsequent saves use the new format. **After saving in v0.0.43, use v0.0.43 or newer; earlier versions cannot read the expanded format.** The normal 128 KiB `.sav` file and standard mGBA/Pizza Boy flash emulation are used; no enlarged emulator save setting is required.

Compression has a fixed 35,696-byte payload budget. Typical populated storage compresses well, but an unusually incompressible collection is not guaranteed to fit merely because it uses fewer than 600 slots. Packing checks the limit before any flash erase/write and reports a failed save if it cannot fit; both prior flash slots and current RAM remain intact. This defensive limit is preferable to silently losing Pokemon or removing the backup slot. Future work can improve compression without changing achievement IDs or story flags.

EWRAM holds the expanded native box arrays. The general heap is 96 KiB; native Contest scratch buffers are located relative to its end instead of the original hardcoded heap offsets. No Hall of Fame, Trainer Hill or recorded-battle sectors are repurposed.

## Tracked quest (v0.0.57)

A on an unfinished visible quest's Details tracks or stops it. One saved choice is marked T in the list and TRACKED in Details. Both ordinary pause pages show the next objective in the native card above clock/weather, with a 16-pixel gap from the right menu. Long wrapped text pauses at each end, scrolls by single pixels and smoothly returns; the heading stays fixed and short text stays still. Competing screens remove the card; special counter/link layouts suppress it. Quest completion clears the choice.

Selection reuses the existing version-1 journal reserved u16 at offset 10 with signature 0xA700 and low byte quest ID + 1 (zero means off). Invalid/unsigned legacy values read as off without writes; the layout, checksum, storage codec, readers and achievement bits stay unchanged. Quest indices 0–32 are persistent and future quests must append. [Design and native evidence](../qa/quest-tracking-preview.md) · [Overflow verification](../qa/quest-tracking-scroll.md).
