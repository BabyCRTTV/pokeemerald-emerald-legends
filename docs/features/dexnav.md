# DexNav approach changes

v0.0.31, shared by Release and Debug.

Selecting DexNav without nearby eligible wild-encounter terrain displays a small top-left instruction window. Press A/B/START to dismiss it and remain in the pause menu. Grass, cave floors and water require matching native map encounter tables; terrain alone is not enough. The check reuses the native search rectangle, without consuming random numbers or creating a search.

Pokémon do not flee because you walk, run or cycle toward them. The native search timeout is now 45 seconds (15 + 30). Moving out of signal range, manually cancelling, warping away and timing out still end searches normally. Reaching the target starts the usual battle. Hidden encounters use the same forgiving approach rules.
