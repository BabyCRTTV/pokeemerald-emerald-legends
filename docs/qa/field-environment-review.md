# Field environment review

The field preview builds on the Dewford bottle preview at d19240a7. It uses the existing map, warp and save IDs.

## Map coverage

All 124 added maps were checked against their active layout. These comprise 107 Kanto and Sevii maps, 14 Hoenn quest maps and three rental maps. The review counted 465 warp events, 160 objects, 133 background interactions and 44 coordinate events. The checks covered map bounds, destination warp indices, solid object tiles, and adjacent walkable ground. A separate flood-fill from ordinary map entries highlighted interactions that rely on scripts, counters or gym teleports.

Run `python3 test/legends-field-environments.test.py` for the repeatable layout and event checks. The Cerulean closed rear door, Vermilion counter and sleeping Mira have intentional positioning exceptions. The script checks the currently registered map groups. It does not simulate a full story playthrough.

## Native gameplay checks

A private mGBA fixture selected each starting map and party. Walks, button presses, scripts and transitions used the compiled game.

- Cerulean, Cinnabar, Pewter, Route 4 and Viridian each healed a 1 HP party member to 255 HP from the public side of the counter.
- Both lanes of the new stairs in waking and dreaming Lilycove admitted the player. The adjoining ledge blocked movement. Walking into Mira’s front door loaded the home and dream bedroom respectively.
- Both Route 10 signs started their intended interaction. Lavender’s upper floor now uses the Fuchsia second-floor layout with the matching upstairs events.
- The Continental Vault encounter faced the southern approach. Walking up to the Route 114 cliff and interacting from its east side entered Stillwater Grotto.
- With Regigigas in the party the Wyrmtide seal opened and transferred the player into the first descent. Re-entering the island in its opened state and walking north through the doorway loaded the same descent.

Focused checks include the Kanto foundation, Kanto chapter 3, grottos, grotto review, Nightmare, story expeditions and Wyrmtide suites. The 170-frame atlas includes both states of Wyrmtide’s cave mouth.
