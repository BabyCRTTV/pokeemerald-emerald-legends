# Adventure Log and played-day counter

## Player guide — v0.0.29

Choose **ADVENTURE LOG** in the pause menu to open a cream-paper notebook with a lavender cover strip, ruled pages and Emerald's native font. It opens on the newest note. The pause menu scrolls when needed, with small arrows showing additional rows; all existing actions remain available.

- **Left/right or L/R:** older/newer pages. Stops at the oldest/newest page.
- **Up/down:** switch to the Day filter and select an older/newer played day that has retained notes.
- **SELECT:** cycle All, Day and Story filters.
- **A:** newest page in the selected filter; the Day filter returns to the current played day.
- **B or START:** close the notebook and return to the pause menu.

Entries show a played-day number, the RTC calendar date when available, location, a story note or latest known milestone, total accumulated play time, and up to one recent Pokemon catch with its level. Captures, checkpoint saves and day resumes refresh the current field note until another story milestone or played day begins, so repeated catches/saves do not crowd out the story. The book keeps the **32 newest notes**; the oldest rolls away when it fills. Story filtering does not change the saved notes.

Opening the notebook is a manual recap similar in purpose to FireRed's adventure reminders. It does not replay animations or force a scene on Continue. Old pages describe recorded observations and victories; they do not repeat battles or advance quests.

## What a day means

**Day 1 is the first date recorded by this system. Each later RTC date on which the game is played adds one day, regardless of its distance from the previous date.** A week away adds no skipped days. Four hours on one date and three hours on another mean Day 2 and seven accumulated play hours. Multiple sessions on the same date stay on the same day. Playing through midnight adds the next date when observed, within a minute or immediately at the next recorded activity/menu refresh.

Uses the RTC calendar, independently of the bedroom clock's hour adjustment, seasonal colors, or the 7H PLAY season setting. Backward clock changes never add duplicate days; counting resumes once the date advances beyond the previously recorded high-water date. An unavailable/invalid RTC pauses the date counter instead of inventing calendar dates; play time still accumulates normally. Only saved history survives a reset, as with ordinary game progress.

On an older save, previous played dates and captures cannot be reconstructed reliably. Its notebook begins at Day 1 where Continue loads the player, with a clearly labelled latest known milestone derived from existing progress. Existing badges, Pokemon and story flags are retained; historical victories are not fabricated as freshly dated entries.

## Story coverage and extension

Current registry records the National Pokedex handoff, Steven's letter, the Mossdeep Space Center resolution, Rayquaza resolving Sootopolis's weather crisis, all eight Hoenn badges, becoming Champion, arriving in Kanto, starting the Wing Survey, Lt. Surge/Koga victories, and filing the first survey report. The other six Kanto victory flags are already registered for their future chapters; notes are generated only when those flags are actually set. Bird and Mew notes remain tentative leads in the current story.

Future chapters can add an `ADV_*` event to `include/legends_adventure.h`, text to `src/legends_adventure_ui.c`, and a final progress flag mapping in `sMilestones` in `src/legends_adventure.c`. Native `FlagSet` records only a real unset-to-set transition. `LegendsAdventureRecord(event)` also supports explicit completed events without a flag. Add a test when introducing a new story event. Do not register construction flags, transient scene states or fake encounter victories.

Captures are recorded at the native captured-mon handoff. They are captures, not gifts, trades, party selections, Dex sightings or battle transformations. Only one recent species is included per entry; the pending recent catch resets on a later played date.

## Saves and safety

`LegendsAdventureSave` is appended to the existing SaveBlock3 reserved sector chunks. SaveBlock1, SaveBlock2, original SaveBlock3 fields, species/trainer/map/flag/var IDs and their existing save offsets do not move. The current full SaveBlock3 is 540 bytes, inside the first five 116-byte chunks written by native partial/link saves. A compile-time assertion enforces that boundary as future features change configuration.

The extension has its own magic, schema version, bounds checks and checksum because these reserved bytes are outside the native sector data checksum. Old reserved bytes or a torn/corrupt log reset only the notebook. Full and partial saves keep the entire journal together. Native game saves remain native; no commercial ROM or player save is uploaded.

The counter and log persist with normal saving, including the save checkpoint. There is no independent autosave. Unsaved notes are lost on reset. Older builds ignore the added extension, and resaving there may discard it; other existing fields are preserved.

## Validation

Focused host checks run the actual C implementations for migration, save/reload, checksum recovery, all story hooks, same-date and skipped-date counting, midnight observation, clock rollback/invalid dates, one recent capture, alternating capture/checkpoint coalescing, 32-note retention, filters and adjacent-day selection. Notebook tests exercise the real render and input callbacks, palette/window bounds, native font widths, empty filters, fade locking, close/return and allocation failure. Pause-menu tests exercise all normal/Debug action combinations and wrapping through the scrolling viewport. The clock-panel test includes the new day row and tile/pixel boundaries.

A local preview rendered from the actual notebook drawing commands and native font glyphs was visually inspected. It is static renderer QA, not an emulator playtest. Release completion requires the existing Debug/Release compile and independent vanilla SHA-1/BPS reconstruction workflow.

Manual emulator checklist:

1. Continue a v0.0.28.1 save and verify player location, party, bag, badges and story progress remain intact. Open the notebook, check Day 1, then save/reload.
2. Capture a Pokemon, save twice, capture another, and verify one refreshed recent catch in the field note. Verify a new story victory creates a separate page and does not repeat on revisits.
3. Use every filter and both paging directions, reach the ends, and close during normal use. Check the empty Story filter early in a new game.
4. On disposable save copies, test repeated sessions on one date, a later date, a several-day gap, a backward clock change, a missing RTC and midnight while the menu is open. Hours accumulate separately from played-day count.
5. Scroll the full Release pause menu with DexNav/PokeNav unlocked and the Debug menu. Reach SAVE, OPTIONS and EXIT where provided; verify the clock/weather panel, Safari counter and Pyramid floor panel remain clear. B/START still close the menu.
6. Verify a native partial/link or Frontier save retains the whole log, and note that a deliberately corrupt extension resets only the notebook.
