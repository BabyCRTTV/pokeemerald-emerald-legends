# Wing Survey chapters 4–6 and The Sleeping Continent — v0.0.41

## Verified

- Both native variants compiled with GCC 13.2.1. Release uses the established LTO configuration. Debug uses 254,100 bytes EWRAM; Release uses 254,094 bytes, so these new scripts/maps do not allocate another runtime sprite bank. Existing upstream LTO warnings remain present.
- All 35 recovered Legends Python regression suites passed. The new 12-test expedition suite executes the shipped script branches for optional observations/captures, caught/won/fled/lost handling, both survey orders, all six regulator orders, reports, travel refusal/returns and Gym Standard/Champion decline/loss/retry/one-win behavior. It also checks saved-bit allocation, dialogue widths, imported warps/NPC floors, and the actual C weather/Seafoam boundaries. Five browser patcher tests passed.
- mGBA 0.10.2: controlled Quickstart profile and native warp/script entry. Loaded Cerulean, Pewter and Cinnabar Gyms, Seafoam 1F/B4F, Mt. Ember summit and the Continental Vault. Verified actual save-block map group/number after each warp; inspected the rendered rooms and sprites.
- Executed all three regulator scripts in the native engine. Verified their flags become set and the sealed-door opening scene runs. Inspected the vault and Regigigas roost. Executed the native awakening script and verified its saved awakened flag; the battle starts with Regigigas displayed at Lv. 70 and native Regi battle presentation. A generated Lv. 100 Rayquaza was provided only to this private QA profile so the encounter could be inspected.
- Native flash persistence: TrySavingData(SAVE_NORMAL) and LoadGameSave(SAVE_NORMAL) both returned SAVE_STATUS_OK. Cleared the new Articuno/report/weather/regulator/Regigigas/current flags and Seafoam-entry variable in RAM between them; confirmed all ten selected flags and variable 0x4077 were restored from flash.

## Evidence and scope

The adjacent `story-*-v0.0.41.png` screenshots show native mGBA output. These checks use controlled map/script entry and flags; they do not establish a complete six-chapter playthrough, every boulder permutation, natural ferry/ledge traversal, battle balance, or every live capture/blackout outcome. Outcome combinations are covered by event regression execution; the awakening/battle entry and flash save/load are additionally verified in mGBA. Human balance and uninterrupted traversal remain useful follow-up playtests.

Only BPS patches are published by the existing release workflow. Its independently built vanilla reference must match SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`; both patch reapplications must match the respective compiled ROM byte-for-byte before deployment.
