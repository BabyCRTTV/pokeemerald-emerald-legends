# Living Hoenn independent review — v0.0.62

**Model: GPT-6 | Approach: trace affected event dependencies, execute source/C branches, then verify exact native dialogue and protected state.**

The owner asked for an independent review of the other model's in-game progress/Weather Institute edits. Reviewed v0.0.61 against the v0.0.60 baseline, AGENTS.md, the handoff, source and CI/private-preview evidence. The existing Research Notes, seasonal bulletin and four-NPC milestone reactions are preserved.

## Findings and repair

1. Fortree's new OldManBadge speech placed three unscrolled lines in the native two-line field window (`src/menu.c` uses four tile rows; `CHAR_NEWLINE` in `src/text.c` advances without scrolling). A new field-text regression failed on that exact string before repair. Changed only the second newline to the native scroll prompt `\l`; wording, speaker, flags and map geometry stayed unchanged.
2. Successful private preview run 39059912905 captured the research request lists, not the new Research Notes. Its host pressed A through six screens before moving Down twice, so the caption implied coverage it did not provide. Source game content was unchanged in that private branch. The replacement checker waits for the exact patron root menu, asserts cursor 2 before A, matches the expected original encoded dialogue, and requires return/closure and unchanged protected state. The old preview is not evidence that Research Notes ran.

## Dependency review

- Notes only count the selected patron's authenticated completion bits; neither accepted work nor the other patron's reports count. Both B7 and B8 reads remain supported without mutation or migration by the presentation helper. Existing first-meeting, Pokédex/rating/registration, letter/PokéNav/Lucky Egg and request claim/abandonment paths are preserved.
- The bulletin stays on the first-floor second worker, gated after Aqua rescue, with Yes/No and all four committed visual seasons. A pending next season is not displayed early. The two-floor scientist/Castform and abnormal-weather scripts are unchanged.
- The four ambient NPCs use existing badges/Champion state. Rustboro gives Champion precedence over Stone Badge; earlier dialogue is retained. All branch exits release control; no new gift, quest, achievement or saved field is introduced.
- No graphics, wardrobe, battle data, map objects/warps, storage codec, save structures or persistent identifiers changed. This repair has no save migration.

## Verification checkpoint

Fresh local checks passed: 24 executable weather state/choice/season paths, nine executable town-NPC milestone paths, native font widths/two-line control geometry for all 18 new texts, every patron completion count and threshold, old B7 state/other-patron isolation/read-only snapshots, deferred season results and unchanged active-season writes. Existing request/season suites passed.

PR #77 passed [project checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39071368910), [native Debug/Release builds and both BPS round trips](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39071368738), and [unmodified Debug Quickstart plus all 23 targeted mGBA scenarios](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39071368730). Reviewed all 92 targeted native frames, including actual Research Notes, all four bulletin seasons and the repaired Fortree scroll. [Native receipt](living-hoenn-v0.0.62-native.json) · [Phone preview](living-hoenn-v0.0.62-preview.png).

The checker runs original compiled scripts/text with temporary state in a private diagnostic ROM copy, verifies passable placement and checks journal/claims, PC rewards, request words and active season. It does not establish natural progression, authentic historical saves or Pizza Boy coverage; Release dialogue was not separately played through. Product ROMs and saves are never included in screenshots or CI artifacts. Original gift/first-meeting priorities received source/guard review; these controlled scenarios enter the research menu directly.

Merged as `512acf964dba395551070cd59e83b0b59b19ba1e`. Production project checks passed; production native/build/BPS jobs and live download verification remain pending at this checkpoint. Two final test-only refinements explicitly cover accepted-but-uncompleted work and make the Living Hoenn metadata guard follow the authoritative release version rather than pinning a minor version; their focused suites passed locally. AGENTS.md was reviewed; no new durable rule was needed.
