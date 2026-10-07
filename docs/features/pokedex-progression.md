# Pokédex and Champion Reward

**Status:** National Dex in 0.0.7; DexNav unlock in 0.0.9.

Pokémon Emerald: Legends unlocks the National Pokédex during Professor Birch's initial Pokédex handoff instead of waiting until after the Elite Four.

## Initial Pokédex handoff

When Birch gives the player the Pokédex after the Route 103 rival battle, Legends now enables National Mode immediately. The normal Pokédex acquisition flags and tutorial progression remain intact. DexNav and hidden Pokémon detector mode now unlock in the Start menu alongside this gift, with dedicated persistent flags/variables. Existing saves with a Pokédex automatically unlock DexNav when continued.

## Post-Champion reward

The original Emerald post-Elite Four National Dex upgrade event is no longer needed because National Mode is already active. Birch now gives the player **25 Rare Candies** at that point instead.

- Birch first tries to place all 25 Rare Candies in the Bag.
- If the Bag cannot hold the full stack, all 25 are sent to the PC instead.
- If neither location has room, the reward remains unclaimed and Birch offers it again when spoken to later.
- A dedicated one-time reward flag prevents duplicate claims.
- Existing postgame saves that already passed the old National Dex scene can still receive the Rare Candy reward once by speaking to Birch.

## Postgame continuity

The existing `VAR_DEX_UPGRADE_JOHTO_STARTER_STATE` progression is preserved so later Emerald postgame behavior, including the Hoenn Pokédex completion reward and Johto starter selection, continues to use the original state flow.
