# Player appearance

Introduced in v0.0.15, shared by Release and Debug.

After choosing Boy or Girl in Birch's introduction, choose **Fair, Light, Medium,
Brown or Deep**, then **Emerald, Trail or Sport**. Both genders have three designs:
the original Emerald clothing, a trail jacket with trousers, and a striped sport
top with shorts. A bordered 64px trainer preview sits at the bottom right above
the dialogue and updates when the cursor moves. A confirms; B returns to the
previous choice. Naming follows outfit confirmation.

The saved choice applies to walking/running, both bikes, Surf, field moves,
fishing/watering, the local player's battle front/back portraits, Safari and
Frontier player scenes, and the local Trainer Card. The diving suit retains its
native covered silhouette. Hair and facial pixels are retained; NPCs and rivals
use their original assets. Native pond/ice filters generate reflections from the
selected player palette; high bridges retain their dark-blue reflection rule.

Existing saves retain their exact original Emerald appearance. This version adds
choices at New Game only; it does not add an appearance editor for existing saves.
Debug Quickstart uses the original appearance. Link/remote appearance is not
synchronized; remote Trainer Cards and native link-player scenes keep native art.

## Implementation

`VAR_LEGENDS_APPEARANCE` uses the previously unused permanent variable `0x404E`:
zero means legacy appearance; values 1–15 encode `1 + skin + 5 * outfit`.
Invalid values fall back to legacy. No save-block layout or link protocol changes.

`legends_appearance.c` stages intro choices separately from saved variables so
they survive `InitEventData`, then consumes them once during New Game. A fresh
title entry discards staging. This is independent of the existing title Options
bridge. Three dedicated palette pairs cover overworld, trainer and underwater
art; only skin slots 1–3 and outfit accent slots 10–11 change. Other slots keep
their native colors. Palette caches rebuild when the appearance changes.

`legends_appearance_graphics.c` supplies eighteen player-only graphics IDs
(two genders × nine native avatar states) in the reserved `0x0F00–0x0F11` range.
The native graphics count and dynamic template IDs remain unchanged so old saved
map templates keep their meaning. Graphics/state checks normalize these
IDs to native IDs. Cloned graphics info retains native dimensions, animation,
tracks and OAM; clothing swaps only the frame images and palette tag. Original
NPC graphics and trainer IDs remain untouched. Six local trainer IDs select
front pictures and all four native back-animation frames.

The intro reuses the native choice window and trainer sprites. The popup uses
non-overlapping BG tiles `0x110–0x14F`; two persistent 2KiB EWRAM buffers keep
preview copies alive through VBlank. No sprite allocation occurs when browsing.

## Assets and validation

`tools/legends/build_appearance.py` authors the clothing masks from the native
indexed PNG pose sheets without changing transparency or animation geometry.
`appearance_frames.json` records native frame order, including repeated Surf and
Dive frames. Generated 4bpp C headers and the frame manifest are checked in; ROM
builds do not require Pillow. To regenerate, install Pillow 11.3.0, then run
`python3 tools/legends/build_appearance.py`.

Host regressions compile the actual settings/graphics modules and check all 30
combinations, save staging, legacy defaults, all avatar states and NPC isolation.
Asset regressions check all 368 edited poses for reproducibility, native facial
pixels, held-ball colors outside the torso, transparency and LZ77 roundtrip.
The Legends workflow must also compile both variants and verify both BPS patches.

### Emulator QA

- Start a new game for both genders; browse every tone/outfit. Confirm the popup
  is above the text, changes immediately, and leaves no tiles after confirmation.
- Use B to revisit skin/gender, change gender, then revisit outfits. Finish naming
  and verify the final choice in Littleroot before setting the clock.
- Save, reset and Continue; check the chosen appearance remains. Load a pre-0.0.15
  save and verify the original appearance and story progress remain intact.
- Check all directions while walking/running, both bikes, Surf/Dive, fishing,
  watering and field moves; test pond/ice and high-bridge reflections.
- Enter a wild and trainer battle, reopen after the Bag/Pokémon screen, check
  every throw-animation frame, then Safari, Frontier and the local Trainer Card.
- Verify the rival and other NPCs remain unchanged; check a native link session
  uses its existing appearance behavior. Repeat in Release and Debug.
