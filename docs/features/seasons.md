# Seasonal System

**Status:** Research / prototype

## Goal

Add a lightweight seasonal system inspired by modern ROM-hack quality-of-life and world-building features without replacing Emerald's core map identity.

## Potential scope

- Spring, summer, autumn, and winter state
- Seasonal encounter tables or encounter modifiers
- Optional palette/environment changes
- Seasonal NPC dialogue or small events
- Configuration to determine real-time, playtime, or story-driven season progression

## Implementation principles

- Start with data/state and encounters before attempting large visual map transformations.
- Avoid duplicating an existing expansion system if one is available.
- Make seasonal effects opt-in per map or encounter group.
- Store season state safely without destabilizing existing save data.

## v0.1 prototype checklist

- [ ] Audit expansion RTC and time-of-day systems.
- [ ] Choose season progression model.
- [ ] Define season enum/state storage.
- [ ] Prototype seasonal encounter selection.
- [ ] Decide whether palette changes belong in v0.1 or a later milestone.
