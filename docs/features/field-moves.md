# Overworld Field Moves

**Status:** Expansion audit complete / implementation design in progress

## Goal

Allow required field actions such as Cut, Rock Smash, Strength, Surf, Waterfall, Dive, and Fly to function without forcing the player to keep the corresponding HM move on a party member solely for overworld progression.

## What pokeemerald-expansion already provides

The current expansion base already centralizes field-move metadata in `src/field_move.c` and `include/field_move.h`.

Each field move has:

- a setup function
- an unlock type
- a move ID
- a failure/message ID
- optional arguments such as the required badge

Emerald's normal badge gates are already represented cleanly through `BADGE_UNLOCK`, so Legends does **not** need to recreate the badge/progression system.

The expansion also has dedicated setup/callback functions for Cut, Flash, Rock Smash, Strength, Surf, Fly, Dive, Waterfall, and the additional supported field moves.

## What the expansion does not currently do

The party menu still builds its field-move actions by scanning the selected Pokémon's four learned moves. A field move is only offered when that Pokémon actually knows the corresponding move.

Surf also explicitly checks `PartyHasMonWithSurf()`.

This means the current expansion base does **not** natively provide the exact Legends behavior we want: using an unlocked overworld HM action without teaching the HM to a party member.

## Legends implementation direction

The cleanest approach is to preserve the expansion's existing field-move setup functions and badge checks, while separating **field-action eligibility** from **whether a party Pokémon knows the move**.

The intended architecture is:

1. Keep the existing expansion field-move definitions and badge gates.
2. Add a Legends helper that determines whether a field action is available.
3. Allow map interactions / field-action UI to call the existing setup functions without requiring a learned HM move.
4. Preserve all existing terrain checks and follower restrictions.
5. Provide a safe animation source when no Pokémon is assigned to the field move.
6. Keep the system configurable so vanilla learned-move behavior can still be restored if desired.

## Animation question

Expansion's current field effects often use the selected party slot to obtain a Pokémon species for the field-move presentation. If Legends invokes the action without a learned move, there is no naturally selected HM user.

For v0.1 we should deliberately choose one fallback policy rather than silently using an arbitrary Pokémon. Candidate policies are:

- use the first compatible non-Egg party Pokémon
- use the lead non-Egg Pokémon
- use a short player/tool-only animation with no Pokémon portrait
- suppress the Pokémon portion of the animation where appropriate

The final choice should be shared across Cut, Rock Smash, Strength, Surf, Waterfall, and Dive wherever practical, with Fly handled separately because it opens the region map.

## Intended behavior

- Preserve badge/progression requirements where Emerald expects them.
- Prefer native expansion field-move hooks rather than duplicating map logic.
- A Pokémon should not need to sacrifice a moveslot merely to provide overworld utility.
- Retain an appropriate field animation or short presentation so actions do not feel instantaneous or unfinished.
- Keep link/Union Room restrictions and map-specific restrictions intact.

## Questions to resolve during implementation

- Whether possession of the HM item remains required.
- Whether a compatible Pokémon must still be present in the party.
- Which Pokémon, if any, should be shown during the field animation when no party member knows the move.
- Whether Fly should use the same abstraction as obstacle-clearing field moves.
- How Teleport, Dig, Flash, Sweet Scent, and other non-HM field actions should interact with the system.

## v0.1 implementation checklist

- [x] Audit current `pokeemerald-expansion` field-move structure.
- [x] Confirm learned moves are still required by the stock party-menu flow.
- [x] Confirm badge unlock logic can be reused.
- [ ] Choose progression and compatibility rules.
- [ ] Implement shared Legends field-action eligibility helper.
- [ ] Preserve map scripts and badge gates.
- [ ] Implement animation fallback behavior.
- [ ] Add interaction hooks for required HM obstacles/actions.
- [ ] Regression-test every required Emerald HM progression point.
