# Overworld Field Moves

**Status:** Planned for v0.1

## Goal

Allow required field actions such as Cut, Rock Smash, Strength, Surf, Waterfall, Dive, and Fly to function without forcing the player to keep the corresponding HM move on a party member solely for overworld progression.

## Intended behavior

- Preserve badge/progression requirements where Emerald expects them.
- Prefer native expansion field-move hooks when available.
- A Pokémon should not need to sacrifice a moveslot merely to provide overworld utility.
- When possible, retain an appropriate field animation or short presentation so actions do not feel instantaneous or unfinished.

## Questions to resolve during implementation

- Whether possession of the HM item remains required.
- Whether a compatible Pokémon must still be present in the party.
- Which Pokémon, if any, should be shown during the field animation when no party member knows the move.
- Whether Fly should use the same abstraction as obstacle-clearing field moves.
- How Teleport, Dig, Flash, Sweet Scent, and other non-HM field actions should interact with the system.

## v0.1 implementation checklist

- [ ] Audit current `pokeemerald-expansion` field-move options.
- [ ] Choose progression and compatibility rules.
- [ ] Implement shared field-action eligibility helper.
- [ ] Preserve map scripts and badge gates.
- [ ] Implement animation fallback behavior.
- [ ] Regression-test every required Emerald HM progression point.
