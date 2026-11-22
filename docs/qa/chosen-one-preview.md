# The Chosen One

Collect the nineteen gifts in any order. A monk records the gift when it fits in the Bag. Trading, storing or equipping a plate afterward preserves that visit. The Quest Log tracks the gifts and directs the player home after the last one. The elder waits by Birch’s lab in Littleroot to hand over the Azure Flute. Registering the flute lets the player play it in the field. The Arceus encounter is reserved for a future update.

## Monk locations

| Plate | Location |
| --- | --- |
| Blank | Oldale Town |
| Meadow | Verdanturf Town |
| Insect | Petalburg Woods |
| Fist | Dewford Town |
| Stone | Granite Cave, 1F |
| Iron | Rusturf Tunnel |
| Splash | Slateport Oceanic Museum, 2F |
| Zap | New Mauville, inside the power plant |
| Flame | Fiery Path |
| Earth | Fallarbor Town |
| Toxic | Route 117 |
| Sky | Fortree City |
| Mind | Mossdeep City |
| Spooky | Mt. Pyre, 1F |
| Dread | Victory Road, 1F |
| Icicle | Shoal Cave, low-tide ice room |
| Draco | Meteor Falls, first room |
| Pixie | Sootopolis City |
| Legend | Ever Grande City |

## Verification

- Built native Debug and Release targets. Visually checked all twenty NPCs in mGBA and checked their approach tiles against existing objects, events and terrain.
- An mGBA playthrough used controlled travel and inventory setup, then spoke to the NPCs through the normal A-button interaction. Collected all nineteen in mixed order, equipped one to a party member, repeated visits, saved and reloaded midway and after the finale. The elder was absent at zero and eighteen gifts and available after nineteen.
- Filled the Bag before a plate and before the flute. Both monks kept their gifts until the next conversation with room. Registering and playing the flute left it in Key Items.
- Native battle tests checked the Blank Plate against a Ghost type and the Legend Plate's Judgment against Swampert and Gyarados. The latter changes the attack to Grass and Electric respectively.
- Integrated upstream changes through rh-hideout/pokeemerald-expansion commit 22b2b010b8c11daf36262557d7de08fa65254672, following the prior sync at 7b95be15d84a053948791ce91e5dec0b168947a5. Preserved Legends’ held-item restoration on capture, its Casual move hints and project-specific contribution files.
- Four supplemental stock-engine assertions reproduced on both this build and released v0.0.94. Two expect stock save and PC storage sizes. Two flag existing food text widths for Buttered Potatoes and the egg custard description.
