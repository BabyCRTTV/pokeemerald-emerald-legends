# EXP System

**Status:** Planned / prior prototype work to be re-integrated

## Goal

Modernize experience distribution while retaining deliberate control over how quickly the party levels.

## Design principles

- Build on expansion-native EXP configuration where possible.
- Keep behavior configurable rather than permanently replacing upstream mechanics.
- Keep Lucky Egg behavior distinct from EXP Share behavior.
- Avoid hidden bonuses that make level progression difficult to predict.

## v0.1 implementation checklist

- [ ] Locate current expansion EXP Share implementation and configuration flags.
- [ ] Re-apply the previously tested Emerald: Legends EXP Share behavior.
- [ ] Re-apply the previously tested Lucky Egg behavior.
- [ ] Confirm behavior for fainted Pokémon, level caps if enabled, traded Pokémon, and multi-battle edge cases.
- [ ] Document final formulas and configuration switches here.
