# Dual Eon roamers — v0.0.75 candidate

Model: GPT-6 (Codex) | Reasoning: preserve the original serialized roamer and add an independent one-time partner.

Baseline: published v0.0.74 `7a0f61c885984b15adacd322ea6346ac2726499f`. [Behavior and compatibility](../features/eon-roamers.md).

Host production-C state tests passed both TV choices, blocked-roll isolation, unlock on battle return, preserved enemy/first-roamer state, independent HP/status/identities/removal, legacy active/unseen/seen/resolved backfill, repeated initialization and no revival. Existing save-sector checks passed at 1,032 bytes, with all old field offsets and both slots/all fourteen rotations intact.

Native Debug/Release actual-battle and flash round-trip fixtures are committed but not yet verified. Builds, full project/browser checks, independent BPS reconstruction, merged production runs and actual public bytes remain required before publication. No native test or publication claim is made yet.

No artwork, seasonal tables, maps/tilesets, wardrobe or persistent IDs changed. New signed extension initializes absent legacy data once. Legacy seen-flag backfill is a documented proxy, not an exact record of roaming encounters. Authentic historical-owner saves, uninterrupted story/balance and Pizza Boy remain broader limits.


Native checkpoint: Debug run 40623148581/artifact 12788705640 confirmed Red-first escape, independent opposite capture, both Eons caught in one save and exact actual flash round-trips. The first knockout case remains blocked; do not call native QA complete or publish. Fixture corrections already made: compare prefix after normal save journal/clock updates; restore field callback before scheduling the battle; use native Shadow Tag/legal Shadow Ball and explicit Fight inputs. Diagnostic candidate 1c3e3415/run 40623933002 now retains failure-frame, callback and symbol evidence to distinguish test control from battle logic. Game code is unchanged since 238436e7; seen-flag backfill is limited to absent/invalid extension initialization. Native Blue-first/KO and normal Release Continue gates remain unverified. Resume this candidate/PR #94, inspect the diagnostic artifact and resolve the failure; do not redo v0.0.74 or publish while blocked.
