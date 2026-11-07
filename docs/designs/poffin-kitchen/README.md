# Poffin Kitchen review

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

Primary flavor sets the crust color. The strongest remaining flavor sets the sprinkle color. Berry order breaks a tie between flavors. The stored treat uses Emerald's seven-byte contest-treat record and existing feeding, sheen and nature systems. The station also opens the case before the player obtains the portable case.

## Verification

Run from the repository root after building Debug:

```sh
python tools/legends/native_poffin_qa/run.py
```

Tested the full Oldale interaction, the two-berry recipe in both orders, a burn warning, case storage, save/reload, and feeding a mixed batch to Torchic. The case held one level 23 treat after cooking. Quantities fell from 3/2 to 2/1. Torchic gained 23 Cool and 23 Beauty and the treat was consumed. Canceling in the Bag or during stirring preserved both ingredients. All 47 machine approaches were checked against map collision and fixed map objects. Oldale was exercised in the emulator. This preview did not replay an authentic historical player save or exercise every Center in-game.

Verified Debug ROM SHA-256: `d623b958ec4be0c328726810376c6e1da917fc2ac4793b7dc3dbc615387b2137`.
