# A Living Hoenn — v0.0.61 QA

**Model: GPT-6 (High) | Logic: reuse signed research, active season and already-set story/badge flags, with focused dependent-script checks.**

## Scope

- Birch and Mr. Stone: optional **RESEARCH NOTES** action; preserve first two actions and exit, claims, abandon/retry, Pokédex and Devon's Lucky Egg priority.
- Weather Institute: first-floor second worker after rescue, four-season bulletin. Second-floor native Castform and unusual postgame weather are untouched.
- Ambient talk: Littleroot (Champion), Rustboro (Stone Badge/Champion), Fortree (Feather Badge), Lilycove (Champion). No player movement, new flags, sprites or map layout changes.

## Validation evidence / gates

- Focused Python source regression: `test/legends-living-hoenn.test.py` (to be checked in CI).
- Existing `test/legends-field-requests.test.py` and `test/legends-seasons.test.py` retained without alteration.
- Required before publishing: successful PR project checks, native Release and Debug builds, independent BPS reconstruction, merged production checks and builds, committed release patches and successful Pages deployment.
- A passing build cannot substitute for uninterrupted emulator gameplay, historic genuine battery-save fixtures, or optional QA checks on Pizza Boy. These are not claimed by this work.

**Save compatibility:** no serialized or persistent IDs, layout, variables or readers changed; existing values are read without mutation. The first two research choices retain their original indices, the optional notes action is index 2, and the original exit moves from index 2 to 3.

**Artwork:** unchanged; all previously approved sprites, palettes, weather visuals and wardrobe remain intact.

## Publication state

Implementation was staged on a feature branch for CI. Record checked run IDs, merged SHA and patch deployment only after verified.
