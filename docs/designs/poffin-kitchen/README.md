# Poffin Kitchen and Treat Case review

## Separate case and feeding display — 12 November 2026

The first interaction with any machine gives the player a distinct TREAT CASE key item (appended item ID 876). It holds 40 Poffins independently of Pokéblocks, shows their pastry colors, flavor values, level and feel, and opens from the Bag, the machine or registered SELECT. The gift checks ownership and handles a full key-item pocket without starting cooking.

Feeding uses a new native screen with the selected Pokémon, a plated pastry, three bite stages and a nature-dependent reaction. The existing condition selector and condition gains remain. Only Poffins use the new animation; ordinary Pokéblocks retain their original scene.

These are actual mGBA 0.10.5 Debug captures, enlarged exactly 3×:

| Scene | Capture |
| --- | --- |
| First interaction gift | [Receive the case](08-Treat-Case-Gift.png) |
| One cooked Poffin | [Treat Case](10-Treat-Case.png) |
| New feeding display | [Feeding still](12-Poffin-Feeding.png) · [Actual animation](13-Poffin-Feeding.gif) |
| Full case, scrolled | [40-treat fixture](18-Full-Treat-Case.png) |

Both Debug and Release builds passed. Native controller tests covered the one-time gift, cooking, independent storage, feeding exactly one treat with condition gains, Bag return, registered SELECT, full-case refusal without berry loss, scrolling and flash persistence. The sector-tail regression passed both slots/all fourteen rotations at the new 1,316-byte SaveBlock3 size; storage codec sanitizer checks passed. [Verification receipt](verification.json).

An earlier preview ROM generated a controlled older-format battery save. The new ROM’s normal Continue migrated the exact Poffin flavors while retaining a normal Pokéblock, party, berries, hairstyle and season; saving, resetting and Continue passed again. [Migration receipt](legacy-verification.json). This is a synthetic fixture, not the authentic historical-owner-save matrix.

The signed Poffin section starts at SaveBlock3 offset 1,032 and appends 284 bytes, leaving the old prefix, sectors and packed storage unchanged. Missing signatures initialize the extension and move preview Poffins once from native records. Full release patch/CI/publication gates remain pending; this is a review branch, not a published release.

Run `python tools/legends/native_poffin_qa/run.py` after building Debug. The optional `legacy.py` checks migration when the private baseline build pair from commit `714669411aa84f1d2efbcd37599854d95e693c14` is present at `build/poffin-native/legacy/pokeemerald.{gba,elf}`. Do not commit ROMs, ELFs or battery saves.

## Original kitchen preview


These are mGBA 0.10.2 captures from a private debug build of Emerald: Legends based on 0.0.77, enlarged exactly 3×. A fresh fixture placed a trainer, Torchic, three Cheri Berries and two Chesto Berries in Oldale. Controller input then opened the machine, selected berries, stirred the batter and fed the result.

| Scene | Capture |
| --- | --- |
| Interact in Oldale | [Poffin Maker](01-Poffin-Maker.png) |
| Roll the D-pad clockwise | [Stirring](02-Stirring.png) |
| Reverse and respond to heat | [Burn warning](03-Burn-Warning.png) |
| Cheri first, Chesto second | [Spicy Poffin with dry sprinkles](04-Baked-Poffin.png) |
| Retrieve the batch | [Treat case](05-Treat-Case.png) |
| Chesto first, Cheri second | [Dry Poffin with spicy sprinkles](06-Dry-Poffin.png) |

A clockwise, counterclockwise, then clockwise sequence fits the GBA D-pad. Single-direction holds and opposite-direction taps earn no stirring credit. Speed matters while the batter is thin, and pauses can burn thick batter. Cooking accepts one or two berries. Each batch makes one treat and commits its ingredients on completion. B cancels during cooking.

Primary flavor sets the crust color. The strongest remaining flavor sets the sprinkle color. Berry order breaks a tie between flavors. This original preview used Emerald's seven-byte contest-treat records and feeding scene. The independent case and custom feeding implementation above supersede that storage/UI; sheen and nature rules remain.

## Verification

Run from the repository root after building Debug:

```sh
python tools/legends/native_poffin_qa/run.py
```

Tested the full Oldale interaction, the two-berry recipe in both orders, a burn warning, case storage, save/reload, and feeding a mixed batch to Torchic. The case held one level 23 treat after cooking. Quantities fell from 3/2 to 2/1. Torchic gained 23 Cool and 23 Beauty and the treat was consumed. Canceling in the Bag or during stirring preserved both ingredients. All 47 machine approaches were checked against map collision and fixed map objects. Oldale was exercised in the emulator. This preview did not replay an authentic historical player save or exercise every Center in-game.

Verified Debug ROM SHA-256: `d623b958ec4be0c328726810376c6e1da917fc2ac4793b7dc3dbc615387b2137`.
