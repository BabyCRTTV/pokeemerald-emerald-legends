# Overworld Pokémon Followers

**Status:** Implemented in 0.0.13. Release and Debug share identical follower behavior.

## Player controls

On Legends Options (L/R from General), choose FOLLOWER and press Left/Right for ON/OFF. ON is the default for new and existing saves. Leaving Options applies it through the normal faded field reload; an ordinary game save persists it. Title-screen Options choices carry into New Game, including OFF.

The native system selects the first conscious non-egg Pokémon in party order. Reorder the party to change your follower. No follower appears before obtaining a Pokémon or when every party member is fainted/an egg. Native Pokémon graphics, shiny/female handling, walking, Poké Ball emergence and talking interactions are retained. Species lacking supplied overworld art use the expansion’s configured Substitute fallback.

## Native restrictions

Followers use the expansion’s existing movement/visibility rules, including travel and forced movement. Oversized sprites are suppressed indoors. Temporary script hiding and active NPC companions take precedence over the player preference. The permanent ON/OFF flag is separate from these temporary conditions, so enabling the option never overrides story hiding. If a map has no free object-event slot, native spawning safely defers the follower.

Seasons affect map palettes; follower/player/NPC object palettes keep their native colors. Existing badge-earned HM utility rules remain in place.

## Maintenance

`include/config/overworld.h` enables `OW_FOLLOWERS_ENABLED` and maps `B_FLAG_FOLLOWERS_DISABLED` to the unused permanent `FLAG_LEGENDS_FOLLOWERS_DISABLED` (0x26A). A cleared disable flag means ON, allowing old saves to initialize without changing their layout or resetting other settings. `src/legends_settings.c` owns the saved preference and title-screen staging; `src/option_menu.c` owns the UI. Native `UpdateFollowingPokemon` in `src/event_object_movement.c` remains responsible for selection, spawning/removal and exclusions. The existing faded field reload refreshes the follower after Options, party/battle screens and map loads.

Run `python3 test/legends-followers.test.py` for native selection/spawn host regressions and `python3 test/legends-new-game-options.test.py` for preference and title-screen lifecycle regressions. See [QA](../QA.md) for emulator playtesting, which is separate from host tests and verified native builds.
