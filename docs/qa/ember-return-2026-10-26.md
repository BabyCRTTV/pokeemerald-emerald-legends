# Mt. Ember return landing — 26 October 2026

Model: GPT-6 (Codex) | Reasoning: script destination, map collision, native warp and sailor interaction review.

Baseline: master `7cf9a7bfcb515ad33b4840ce38cd7d2e88008b8d`, VERSION 0.0.70.

The production `LegendsStory_EmberReturn` warped to Cinnabar `(20,9)`. Its current layout word is `0x0433`: collision 1, elevation 0, and the coordinate also hosts a self-targeting closed-door warp. The old event test asserted those coordinates without examining the map. This establishes an invalid landing; it does not establish a reproduced emulator softlock.

Changed only the return script destination to `(21,8)`, directly east of the existing expedition sailor at `(20,8)`. The new word is `0x30D0`, collision 0, elevation 3, matching the sailor; primary metatile D0 has normal behavior. It has no object or warp at that coordinate. North `(21,7)` is clear at the same elevation, leading to the town path. Existing maps, tilesets, object placement and owner edits are untouched. Outbound requirements, decline behavior, report gates, inventory and saved IDs/layouts are unchanged. Returning requires no progression flags, so it remains available throughout the expedition.

Added an existing-suite regression that executes the actual return script for three progression snapshots, declines then accepts, checks unchanged flags, resolves the actual destination against the current map/layout, checks collision, object/warp overlap, adjacency/elevation to the sailor and the north path. It failed against the original script (`1024 != 0`, blocked landing) and passed after the change.

Validation: all 57 tests across `legends-story-expeditions`, `legends-kanto-finale`, `legends-kanto`, `legends-kanto-foundation`, `legends-kanto-challenge`, `legends-kanto-chapter2` and `legends-kanto-chapter3` passed; `git diff --check` passed.

Limits: these are source-level event/geometry checks. Native compiler and mGBA dependencies are absent locally. Candidate CI must verify both ROM builds, clean-base BPS reconstruction and native smoke. A focused emulator boat-return/movement/reboarding check remains required; the existing native smoke does not cover it. No publication, version bump or new downloadable patch is claimed. Historical saves, uninterrupted story traversal and Pizza Boy coverage remain outstanding.
