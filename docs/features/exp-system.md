# EXP System

**Status:** Implemented in 0.0.5

## Goal

Modernize experience distribution while preserving player control over party-wide leveling.

## 0.0.5 behavior

Pokémon Emerald: Legends uses the expansion's native Gen 6-style EXP Share path rather than maintaining a separate EXP calculation.

- EXP Share is available immediately and defaults to **ON**.
- A new **EXP SHARE** option in the normal Options menu switches the global effect ON or OFF.
- When ON, Pokémon that participated in the battle receive the normal full EXP reward.
- Eligible non-participating party Pokémon receive the Gen 6-style half share.
- Eggs do not receive EXP.
- When OFF, non-participating Pokémon do not receive the global party share. Normal participant EXP and held-item behavior remain expansion-native.
- Catch EXP, scaled EXP, level-cap behavior, traded-Pokémon bonuses, and other modifiers continue to use the expansion battle pipeline.

The global behavior is backed by `I_EXP_SHARE_FLAG`, assigned to the Legends-specific saved flag `FLAG_LEGENDS_EXP_SHARE`.

## Defaults and save migration

New games enable the Legends EXP Share flag immediately after event data is initialized.

Existing saves created before 0.0.5 receive a one-time settings migration on continue: EXP Share is enabled and a separate initialization flag is set. After that migration, the player's ON/OFF choice is preserved normally and is not overwritten on later loads.

## Options menu

The setting is saved when leaving the Options menu. The Options screen was tightened vertically by one tile row so the additional EXP SHARE row fits while retaining the original 16-pixel spacing between settings.

## Lucky Egg

Lucky Egg remains distinct from the global EXP Share and is **unchanged in 0.0.5**. Its multiplier continues to be handled by the expansion's normal experience multiplier path. Any Legends-specific Lucky Egg tuning will be treated as a separate future change.

## Implementation checklist

- [x] Locate and reuse the expansion-native Gen 6 EXP Share implementation.
- [x] Assign a persistent Legends flag for global EXP Share state.
- [x] Default new games to EXP Share ON.
- [x] Migrate existing pre-0.0.5 saves to the new default once.
- [x] Add an EXP SHARE ON/OFF setting to Options.
- [x] Preserve native Lucky Egg, traded Pokémon, scaled EXP, catch EXP, and level-cap handling.
- [x] Complete Release and Debug build verification for 0.0.5.
