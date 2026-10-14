# Development handoff

## Working preference

The owner switches between models such as Astra and Sol. Use the selected model's strengths, retain the same quality standard, and communicate project decisions, approvals, validation and unfinished work through this file and the linked records. Live repository activity supersedes this snapshot. Inspect it before resuming; do not infer publication from a commit alone.

## Accepted baseline

- Root version: **0.0.47**, shared by Release and Debug.
- The owner approved the minimal smile/body-color repair and requested publication. Preserve the existing v0.0.46 sprites and approved hairstyle artwork. Generated replacement sprites were rejected and are absent from the released tree.
- Male native mouth/chin/ear and exposed-skin contours now use skin shadow instead of hair color. Natural custom hair receives body isolation; footwear remapping reserves both hair slots. Clothes and shoes retain their selected colors across hair-color changes.
- Existing save choices, female sprites, approved battle art, fixed costumes, diving and untouched Original retain their established behavior. Side Part still uses its published art; its separate redesign has not received approval.

## Confirmed implementation and validation

- [PR #64](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/64) merged as `f6e4cd519c654865267f47e4cbcde48a233179bf`.
- Versioned PR checks and native Debug/Release/BPS verification passed before merge. Merged-source [project checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38495112804) and [publication workflow](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38495112683) passed.
- Both patches independently reproduced their corresponding compiled ROMs byte-for-byte against the verified clean Emerald base. Patch commit: `818792a92ad8623b099b6486fa4413006bd5d246`. [SHA256 manifest](downloads/SHA256SUMS.txt).
- Live Pages index, changelog and browser patcher agree on v0.0.47. Both public BPS downloads returned HTTP 200, matched the verified SHA256 manifest and passed patch CRC checks. The simplified PNG also returned HTTP 200. QA/preview commit `12211c565f772bb6f6dde77eb77c1fd3b27dc275` passed project checks and Pages deployment.
- Relevant checks cover frozen artwork fingerprints, 212 native poses, 400 smile/color/skin cases, 1,440 front/field wardrobe combinations, footwear caches, intro, wardrobe and prepared battle sprites. [Detailed QA](qa/appearance-color-fix.md).
- [Simplified matching wardrobe/overworld PNG](qa/v0.0.47-sprite-sheet.png) shows Natural/Blond Crew Cut with identical Emerald clothing and red shoes, plus Silver Tousled with Trail/navy/Ocean scarf/black boots. It uses actual compiled-C buffers, not generated replacements or emulator captures. Reproduce with `python tools/legends/preview_appearance_baseline.py`.

## Next work

The owner intends to improve from this approved baseline. Await specific visual tuning feedback before redesigning or publishing further artwork. Preserve the color repair and existing protected-asset checks. No new sprite redesign is approved by this handoff.
