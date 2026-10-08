# Da Bug

Added in v0.0.20 to both Release and Debug. Da Bug is the Leafhopper Pokémon, a single-stage Bug/Grass species, 0.3 m tall and 1.2 kg. Its green leaf-veined wings and red eyes become autumn amber wings, a cream body and teal eyes when shiny. The approved Pokédex entry is unchanged:

> It sways in the breeze to mimic a fallen leaf. If its disguise fails, it flashes its red eyes and springs away.

## One-time PC gift

New Game places one level-5 Da Bug in Box 1, first slot, after initializing storage. Existing saves receive it on continue in the first empty slot across boxes, starting with Box 1. No existing Pokémon is overwritten. If every box is full, make space, save and continue again to retry.

The four initial moves are Tackle, Leer, Mean Look and Absorb with their normal PP. Player name/ID are the original trainer. The gift registers Da Bug as seen/caught; its entry becomes accessible when the National Pokédex is unlocked through normal Legends progression.

`FLAG_LEGENDS_DA_BUG_RECEIVED` reserves unused flag 0x26B. Once stored, withdrawal, release, trade, PC access and continued play never replace or reroll it. Save after receiving it to retain that Pokémon; resetting an unsaved game follows normal save behavior. Debug's explicitly destructive Clear Boxes command does not restore the gift.

An inclusive uniform roll of 0–9 makes only outcome 0 shiny. The native stored shiny bit is explicitly set for both outcomes after creation, so ordinary personality odds, SHINY RATE Options, Charm and encounter bonuses cannot increase the gift's chance. This exception applies only to this one-time placed Pokémon, not ordinary Da Bug obtained through breeding/debug tools. No wild encounter tables change. Because Da Bug has no evolution, it is excluded by the native Legends Random starter eligibility rule.

## Species and learnset

Base stats: HP 65 / Attack 70 / Defense 75 / Special Attack 80 / Special Defense 75 / Speed 85 (450 total). Abilities: Swarm, Leaf Guard; hidden ability Chlorophyll. Medium Fast growth; Bug egg group. No evolution, egg moves or TM/tutor learnset are introduced in this version.

| Level | Move |
|---|---|
| 1 | Tackle, Leer, Mean Look, Absorb |
| 8 | Bug Bite |
| 12 | Leech Seed |
| 16 | Mega Drain |
| 20 | Struggle Bug |
| 24 | Protect |
| 28 | Giga Drain |
| 32 | Agility |
| 36 | Leech Life |
| 40 | Synthesis |
| 44 | Energy Ball |
| 48 | Bug Buzz |

## Native implementation

`src/legends_da_bug.c` handles the gift only; metadata and learnsets live in the separate Legends species/learnset headers. Custom species ID 1573 and National Dex 1026 append after existing species/dex entries. Existing species IDs are unchanged. Adding entry 1026 leaves the rounded dex bitfields at 129 bytes, preserving the SaveBlock layout.

Art in `graphics/pokemon/da_bug` converts the approved concept into indexed 16-color native assets: 64x128 front (two 64x64 frames), 64x64 rear, six 32x32 follower frames, two 32x32 shared-palette icons and 16x16 footprint. Shared palette indices supply the normal/shiny forms. The icon uses the expansion's existing green/red palette 1 to preserve UI palette limits. Follower directions use the native symmetric frame layout. The intro uses `ANIM_ROTATE_TO_SIDES` and an eye-only glimmer frame, with a dedicated red palette index in both forms. The player-side send-out uses a separate 48-frame sway with an eye-only red palette blend, restoring the original normal/shiny eye colors at completion. The Debug visualizer exposes this back animation too. No whole-sprite color flash.

The original cry is two soft rising chirps, 0.34 seconds of unsigned 8-bit mono PCM at the native 13379 Hz, converted by the existing compressed cry pipeline. Both forward and reverse cry tables include the new cry.

## Validation and emulator QA

`test/legends-da-bug.test.py` compiles the actual gift module against storage/RNG fixtures, exercises all ten roll outcomes with ordinary shiny on and off, duplicate guard, full-box retry, moves/level and dex registration. It also checks asset dimensions, eye-only frame changes, shared red glimmer, PCM bounds, exact dex text, unchanged dex bitfield size and no wild placement.

Before judging presentation, test in an emulator: new save Box 1 and all four move PP; v0.0.19 save migration without replacement; full boxes followed by space/save/continue; withdraw/save/reload with no duplicates; normal/shiny Summary, storage icon, follower facing/walking/reflection, battle rear and Pokédex front sway/glimmer; play the cry and inspect all four dex lines. Automated compilation/patch verification does not replace this visual/audio gameplay QA.
