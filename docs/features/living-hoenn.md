# A Living Hoenn — v0.0.61

**Model: GPT-6 (High) | Logic: read-only milestones and narrowly scoped story-flag branches; preserve verified progression.**

## Gameplay

- **Research Notes:** Birch and Mr. Stone now offer a third optional menu action, after their established Requests/Rating or Contracts/Business actions. The text reflects their own **completed reports**, not the current acceptance. Birch: 0–2, 3–8, 9–17, and all 18 reports. Devon: 0–2, 3–5, 6–11, and all 12 contracts. Notes may be revisited without rewards or progress.
- **Weather Institute:** After the Aqua rescue, talk to the **first-floor second worker** and choose to read the field bulletin. The message observes Spring, Summer, Autumn or Winter using the currently committed outdoor visual season. This does not predict specific daily weather or change encounter tables. The scientist upstairs, Castform gift and abnormal-weather story remain unchanged.
- **The World Remembers (first phase):** Littleroot's PC-advice resident recognizes the Champion; a Rustboro Devon worker acknowledges Roxanne's badge or Championship; Fortree's older resident notes Winona's badge; Lilycove's contest enthusiast recognizes a Champion. These are repeatable ambient lines; original dialogue is retained for the player's earlier story states.

## Dependency and save impact

Existing first meetings, native Birch Pokédex gifts, Mr. Stone's letter/PokéNav/Lucky Egg, Team Aqua's Weather Institute invasion, scientist Castform reward, abnormal-weather triggers, gym events, trainers, movement/map geometry, and save initialization are unchanged. The implementation reads existing `FLAG_BADGE01_GET`, `FLAG_BADGE06_GET`, `FLAG_SYS_GAME_CLEAR`, `VAR_WEATHER_INSTITUTE_STATE`, signed research completion bits, and the active seasonal display. It introduces **no new saved variables, flags, IDs, persistent structures, rewards, map NPCs, or art**. The two additional read-only specials only return current information for dialogue choices. Release and Debug receive the same content.

## Validation plan and limitations

`test/legends-living-hoenn.test.py` checks connected dialogue entry points, four seasonal branches, menu ordering, original gift/story branches, read-only specials, save-sensitive invariants and old 0.0.60 history. Existing field-request and season suites continue to run. Native Release/Debug compilation, BPS round-trip validation and Pages deployment are release requirements; those outcomes belong in the [QA record](../qa/living-hoenn-v0.0.61.md) after real CI completes. Expanded old-save and uninterrupted emulator playthrough coverage remain separate tasks.

## Publication and QA

**Model: GPT-6 (High) | Logic: real mGBA startup proof plus targeted source branch testing; keep unexercised scenarios explicit.** [v0.0.61 production release, patch hashes, mGBA screenshot evidence and remaining manual scenarios](../qa/living-hoenn-v0.0.61.md). The shipped update makes no saved-state or artwork changes.
