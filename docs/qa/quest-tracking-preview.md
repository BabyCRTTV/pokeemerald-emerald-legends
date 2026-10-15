# Quest tracking — review preview

Status: **implemented on `feature/quest-tracking-preview`, awaiting owner approval before publication**. Published master remains v0.0.56. [Native preview](quest-tracking-preview.png) · [Competing-menu examples](quest-tracking-menu-safety.png) · [Verification receipt](quest-tracking-preview.json).

## Interaction and placement

On 15 October 2026 the owner accepted Track a Quest and requested a preview before publishing, explicitly requiring the reminder to avoid other menus. Press A on an unfinished visible quest's Details page to track it; press A again to stop. A T marker identifies the list entry and Details shows TRACKED. Completed/undiscovered quests cannot be selected. Existing filters, six rows, objectives and achievement rewards stay intact.

The pause card uses the native frame, font and text palette. Its framed footprint is x=0..111, y=0..87: a 16-pixel gap separates it from the right menu, whose frame starts at x=128. The unchanged clock/weather frame starts at y=88. It appears on both ordinary pause pages, with no field HUD or input capture. The next unfinished objective comes from Quest Log's flags; completing the quest clears tracking. Only quests already visible in the log are eligible.

DexNav help removes the card before allocating its window and restores it on closing. Save and other screens use the established pause-panel cleanup. Safari, Pyramid, Pike, partner rooms, link and Union Room layouts suppress it. Map-name popups defer creation; queued achievement notices are hidden before allocation. Allocation failure leaves the menu functional. BG0 tiles 0x250..0x2BB stay below physical map blocks at VRAM 0xE000 and outside menu/clock/frame allocations. DexNav help reuses this range only after the card is removed.

## Save contract

The existing 36-byte version-1 journal's reserved u16 at offset 10 stores 0xA700 | (quest ID + 1), with 0xA700 explicitly off. No size, offset, reader, codec, save version, achievement ID or reward bit changed. Zero/unsigned/invalid values read as no selection without writes. Explicit track/stop and clearing a recognized completed/obsolete selection use the existing checksum/refresh/save path. No schema migration is needed. Quest IDs 0..32 now have a persistence contract: retain their array order and append future quests.

## Verification

All 49 normal project-check blocks passed. Extended actual-C checks cover all 65,536 possible legacy words without read-time mutation, initialization/persistence, track/switch/stop, hidden/completed/link guards, progression, real Details A controls, complete catalogue text using native font widths, allocation/map-popup handling and resource bounds. The final geometry/exclusion additions passed again, including all 64 combinations of special-menu restrictions. Test-generated PNGs had identical indexed pixels/palettes and were restored to their original encoding; no approved artwork changed.

Both normal Debug and Release builds passed. Controlled Debug mGBA input tracked Devon Delivery through actual menus, displayed both pause pages, removed/restored the card around DexNav help and Save/cancel, and suppressed it for the Safari counter. Real flash write/clear/load retained the pre-feature-format default, tracked selection and completion, preserving non-default wardrobe, bedroom colours and Winter. The player remained on a verified walkable floor tile. Controlled flags advanced/completed the quest; this was not uninterrupted story traversal.

An unmodified Release ROM loaded a private copy of that battery fixture with normal title/Continue input. Both pause pages, tracked Details and stop tracking passed without host RAM/callback writes. Reminder pixels matched Debug exactly. Debug captures retained exact menu-content and clock/weather pixels when the card appeared. Selected native frames were visually reviewed; previews enlarge pixels exactly 2× with captions outside the game image.

These are prepared fixtures in the unchanged v0.0.56 save layout, not authentic historical-release saves. The historical matrix and Pizza Boy remain unfinished. Private diagnostic ROMs, ELFs and battery saves are excluded.

## Overflow scrolling follow-up

The owner requested automatic smooth scrolling after reviewing the card. [Native long-text animation](quest-tracking-scroll.gif), [implementation and scope](quest-tracking-scroll.md), and [fresh verification](quest-tracking-scroll.json) supersede the static-body behavior. The original evidence above remains historical.

## Approval and publication

VERSION and public downloads remain v0.0.56 during review. Following owner layout approval: coordinate the next version/changelogs/title/Options/site labels, run final PR CI/build/BPS checks, merge and verify both live downloads through independent decoders and Pages. Do not merge or update Pages/downloads before approval. The developer-site refresh remains deferred.
