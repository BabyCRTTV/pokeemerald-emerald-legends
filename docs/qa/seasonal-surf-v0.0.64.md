# Seasonal Surf — v0.0.64

**Model: GPT-6 | Approach: preserve native encounter dependencies, execute shared C and inspect real compiled Legends in mGBA.**

Status: implementation prepared on a development branch; native, build/BPS and publication checks pending. Baseline: published v0.0.63 master `4e6000ca35dbbaeb92b7a45296993a1de10a5f4e`.

The owner explicitly chose Routes 105–108 Surf. [Roster/rules](../features/seasonal-encounters.md). Sixteen seasonal tables add 32 visitors, with original residents at 65%, visitors 30%/5%, original five-slot levels/rate and committed-season behavior. Land pilot tables, fishing/native data, map layouts, art, icon fitting, save structures/readers and identifiers remain intact. No migration was needed.

`test/legends-seasonal-encounters.test.py` passed exact table/odds/levels/resident checks, all TOD values, active-vs-pending season, bounds/invalid season, unrelated native pointer parity, dependent readers and absent previous-season DexNav targets for both methods. DexNav proximity passed. The expanded native harness retains all 35 original grass cases and adds sixteen Surf mixed-seen rosters, sixteen all-seen rosters and one all-unseen lock case (68 total; 17,408 native wild creations if execution passes).

Do not treat planned coverage as executed. Builds, mGBA captures, production results and both live BPS decoders must be recorded before publication is claimed. Controlled Debug fixtures do not establish a full uninterrupted playthrough, detector hunt, historical-save migration, Release interaction or Pizza Boy coverage. Existing historical receipts remain protected.
