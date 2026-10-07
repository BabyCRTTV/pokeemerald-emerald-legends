# Overworld Field Moves

**Status:** Implemented in v0.0.4 / gameplay regression testing ongoing

## Goal

Allow Emerald's required HM field actions to work without forcing a Pokémon to dedicate a moveslot to Cut, Flash, Rock Smash, Strength, Surf, Fly, Dive, or Waterfall.

Legends treats those eight actions as progression utilities earned through the same Gym Badge sequence used by Pokémon Emerald.

## Progression

The original Emerald badge order remains intact:

- Cut - Stone Badge
- Flash - Knuckle Badge
- Rock Smash - Dynamo Badge
- Strength - Heat Badge
- Surf - Balance Badge
- Fly - Feather Badge
- Dive - Mind Badge
- Waterfall - Rain Badge

Possessing or teaching the corresponding HM is no longer required for overworld use. The HM moves themselves remain normal teachable battle moves.

## How it works

The expansion's existing field-move metadata, setup functions, terrain checks, and badge gates remain the foundation.

Legends adds a shared distinction between:

- **badge utilities** - Emerald's eight HM progression actions, unlocked by badge
- **Pokémon field moves** - Dig, Teleport, Sweet Scent, Secret Power, healing moves, and expansion-specific optional field moves, which still require the Pokémon to know the move

Map scripts that call `checkfieldmove` recognize badge utilities without scanning the party for the HM. A safe non-Egg party slot is still supplied internally where legacy field-effect code expects one, but that Pokémon is not treated as the source of the ability.

## Player access

Progression actions are primarily contextual:

- interact with a cuttable tree to use Cut
- interact with a breakable rock to use Rock Smash
- interact with a Strength boulder to activate Strength
- interact with surfable water to use Surf
- use Dive and Waterfall at their existing map/terrain triggers

The party action menu also exposes one compact **FIELD** entry once the first utility is unlocked. FIELD lists the currently unlocked badge utilities and provides manual access to actions such as Flash and Fly without requiring a learned HM.

Individual HM names are no longer injected into each Pokémon's normal action list.

## Presentation

The old “{Pokémon} used HM” messages have been removed from Legends' HM interactions.

Badge utility effects preserve the familiar player pose, environmental effects, Surf/Fly movement, follower handling, and puzzle hooks, but suppress the generic Pokémon portrait/banner that would otherwise imply an arbitrary party member knew the move.

Non-HM field moves keep their normal Pokémon presentation.

## Compatibility and story rules

Legends deliberately keeps the expansion's existing restrictions where they matter:

- badge requirements
- valid terrain and map types
- Surf/Fly follower restrictions
- link and Union Room restrictions
- Regirock/Registeel field-move puzzle hooks
- Strength's per-map activation flag
- Dive/Waterfall warp and direction checks

The goal is to remove moveslot tax, not bypass Emerald's progression or map logic.

## v0.0.4 implementation checklist

- [x] Reuse Emerald's existing badge unlock metadata.
- [x] Separate HM field eligibility from learned moves.
- [x] Remove the hard-coded learned-Surf checks.
- [x] Add contextual badge-only HM interaction support.
- [x] Add the global FIELD utility submenu.
- [x] Remove Pokémon-specific HM-use text.
- [x] Suppress arbitrary Pokémon field-move banners for badge utilities.
- [x] Preserve Regi puzzle and follower hooks.
- [x] Remove the obsolete HM-based party-boxing restriction.
- [ ] Complete in-emulator regression passes at every required Emerald HM progression point.
