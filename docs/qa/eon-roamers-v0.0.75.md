# Dual Eon roamers — v0.0.75 candidate

Model: GPT-6 (Codex) | Reasoning: preserve the original serialized roamer and add an independent one-time partner.

Baseline: published v0.0.74 `7a0f61c885984b15adacd322ea6346ac2726499f`. [Behavior and compatibility](../features/eon-roamers.md).

Host production-C state tests passed both TV choices, blocked-roll isolation, unlock on battle return, preserved enemy/first-roamer state, independent HP/status/identities/removal, legacy active/unseen/seen/resolved backfill, repeated initialization and no revival. Existing save-sector checks passed at 1,032 bytes, with all old field offsets and both slots/all fourteen rotations intact.

Native Debug/Release actual-battle and flash round-trip fixtures are committed but not yet verified. Builds, full project/browser checks, independent BPS reconstruction, merged production runs and actual public bytes remain required before publication. No native test or publication claim is made yet.

No artwork, seasonal tables, maps/tilesets, wardrobe or persistent IDs changed. New signed extension initializes absent legacy data once. Legacy seen-flag backfill is a documented proxy, not an exact record of roaming encounters. Authentic historical-owner saves, uninterrupted story/balance and Pizza Boy remain broader limits.
