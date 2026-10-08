# EXP System

**Status:** Implemented in 0.0.5; Rustboro reward in 0.0.6; physical Key Item added in 0.0.9

## Goal

Modernize experience distribution while preserving player control over party-wide leveling.

## 0.0.5 behavior

Pokémon Emerald: Legends uses the expansion's native Gen 6-style EXP Share path rather than maintaining a separate EXP calculation.

- EXP Share is available immediately and defaults to **ON**.
- A new **EXP SHARE** option switches the global effect ON or OFF. As of 0.0.8 it lives on the dedicated **Legends** Options page.
- When ON, Pokémon that participated in the battle receive the normal full EXP reward.
- Eligible non-participating party Pokémon receive the Gen 6-style half share.
- Eggs do not receive EXP.
- When OFF, non-participating Pokémon do not receive the global party share. Normal participant EXP and held-item behavior remain expansion-native.
- Catch EXP, scaled EXP, level-cap behavior, traded-Pokémon bonuses, and other modifiers continue to use the expansion battle pipeline.

The global behavior is backed by `I_EXP_SHARE_FLAG`, assigned to the Legends-specific saved flag `FLAG_LEGENDS_EXP_SHARE`.

## Defaults and save migration

New games enable the Legends EXP Share flag immediately after event data is initialized.

Existing saves created before 0.0.5 receive a one-time settings migration on continue: EXP Share is enabled and a separate initialization flag is set. After that migration, the player's ON/OFF choice is preserved normally and is not overwritten on later loads.

## Physical Exp. Share Key Item (v0.0.9)

The expansion's `I_EXP_SHARE_ITEM` setting is `GEN_6`: the Exp. Share is a Key Item. The initial Bag gets one and the global EXP Share flag remains ON by default. Continuing an older save attempts to backfill it without changing the saved ON/OFF choice; the temporary Battle Pyramid inventory is excluded. An item-space failure retries on a later ordinary continue. The Key Item and Options toggle both operate the same saved `FLAG_LEGENDS_EXP_SHARE`. The Rustboro reward continues to be a Lucky Egg.

## Options menu

The setting is saved when leaving the Options menu. Version 0.0.8 replaced the temporary single-page layout with General and Legends pages. EXP SHARE now lives on the Legends page, selected with L/R, while the menu uses Emerald's original safe window dimensions and 16-pixel row spacing.

## Lucky Egg

Lucky Egg remains distinct from the global EXP Share. Its multiplier continues to be handled by the expansion's normal experience multiplier path.

### 0.0.6 Rustboro reward

After the player delivers Mr. Stone's Letter to Steven and returns to Devon Corp. in Rustboro, Mr. Stone now gives a **Lucky Egg** instead of the original held Exp. Share. The global EXP Share introduced in 0.0.5 made the original reward redundant.

This changes Lucky Egg acquisition only. Its native 1.5× held-item EXP multiplier is unchanged. Emerald's existing `FLAG_RECEIVED_EXP_SHARE` is deliberately retained as the one-time Devon reward completion flag so existing save/event state remains compatible.

Any further Legends-specific Lucky Egg tuning will be treated as a separate future change.

## Implementation checklist

- [x] Locate and reuse the expansion-native Gen 6 EXP Share implementation.
- [x] Assign a persistent Legends flag for global EXP Share state.
- [x] Default new games to EXP Share ON.
- [x] Migrate existing pre-0.0.5 saves to the new default once.
- [x] Add an EXP SHARE ON/OFF setting to Options.
- [x] Preserve native Lucky Egg, traded Pokémon, scaled EXP, catch EXP, and level-cap handling.
- [x] Complete Release and Debug build verification for 0.0.5.
