# Player appearance

Introduced in v0.0.15, shared by Release and Debug.

After choosing Boy or Girl in Birch's introduction, choose **Fair, Light, Medium,
Brown or Deep**, then a gender-specific hairstyle and hair color from separate Up/Down scrolling lists, then **Emerald, Trail, Sport, Yellow or Lavender**. Both genders have five designs:
the original Emerald clothing, a trail jacket with trousers, and a striped sport
top with shorts, a yellow top, and a lavender top with plum shading and a cream scarf. Custom designs use bare hands; Emerald retains its original gloves. A bordered 64px trainer preview sits at the bottom right above
the dialogue and updates when the cursor moves. A confirms; B returns to the
previous choice. Naming follows outfit confirmation.

The saved choice applies to walking/running, both bikes, Surf, field moves,
fishing/watering, the local player's battle front/back portraits, Safari and
Frontier player scenes, and the local Trainer Card and naming-screen icon. The diving suit retains its
native covered silhouette. Hair and facial pixels are retained; NPCs and rivals
use their original assets. Native pond/ice filters generate reflections from the
selected player palette; high bridges retain their dark-blue reflection rule.

Existing saves retain their original Emerald appearance. Since v0.0.23, the
[wardrobe](wardrobe.md) edits outfits, hairstyles, hair colors and accessories at home or in your own secret base, retaining skin tone.
Debug Quickstart uses the original appearance. Link/remote appearance is not
synchronized; remote Trainer Cards and native link-player scenes keep native art.

## Implementation

`VAR_LEGENDS_APPEARANCE` uses the previously unused permanent variable `0x404E`:
zero means legacy appearance; values 1–25 encode `1 + skin + 5 * outfit`.
Codes 26–30 retain native skin with a selected outfit for wardrobe edits on legacy saves.
Accessory var 0x40A1 stores scarf/jacket settings. Invalid values fall back to legacy. No save-block layout or link protocol changes.

`legends_appearance.c` stages intro choices separately from saved variables so
they survive `InitEventData`, then consumes them once during New Game. A fresh
title entry discards staging. This is independent of the existing title Options
bridge. Three dedicated palette pairs cover overworld, trainer and underwater
art; skin uses slots 1–3 and outfit accents use 10–11. Hair colors reserve 4/7 and coats reserve 10 through pose-specific masks; eye, skin and footwear roles stay separate. In the male overworld review, custom cuts also reserve 8 for a third hair shade. The compositor transfers native navy pixels to slot 5, which retains the original navy RGB value; footwear cannot choose 4/7/8 as replacement body colors. This is confined to custom male overworld art. Trainer/battle palettes, female art, Original and the diving suit retain their existing roles. Palette caches rebuild when the appearance changes.

`legends_appearance_graphics.c` supplies eighteen player-only graphics IDs
(two genders × nine native avatar states) in the reserved `0x0F00–0x0F11` range.
The native graphics count and dynamic template IDs remain unchanged so old saved
map templates keep their meaning. Graphics/state checks normalize these
IDs to native IDs. Cloned graphics info retains native dimensions, animation,
tracks and OAM; clothing swaps only the frame images and palette tag. Original
NPC graphics and trainer IDs remain untouched. Ten local trainer IDs select
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

Host regressions compile the actual settings/graphics modules and check all 50
combinations, save staging, legacy defaults, all avatar states and NPC isolation.
Asset regressions check all 736 edited poses for reproducibility, native facial
pixels, held-ball colors outside the torso, transparency and LZ77 roundtrip.
The Legends workflow must also compile both variants and verify both BPS patches.

### Male overworld reference import (review draft)

`graphics/legends/male_overworld/heads.png` contains ten indexed native-grid
head sets (front, rear and west). `male_overworld_sheets.json` records the supplied
reference names, SHA-256 hashes and sampled eye/ear grid registration.
`import_male_overworld_sheets.py` can reimport the original four-view sheets with
Pillow and NumPy; ordinary builds consume the checked-in atlas and sparse masks.
Native east-facing animations mirror the west image, matching the original engine.

`male_overworld_hair.py` fits the atlas to all 83 male walking/running, bike,
Surf, field-move, fishing and watering source poses before generating ROM edits.
Pupils register forward/profile heads; actual ears register rear heads. Field-move
poses with two visible eyes use the forward view even when the body turns sideways.
Skin underneath separated fringe locks stays filled. Preserve lower faces, hands,
real ears and fishing rods. The undercut's shaved temple uses the selected skin ramp.
The native diving suit is checked through its existing animation table.

Validation combines the real C compositor/cache tests with decoded mGBA frames,
all eight hair colors and five skin tones, and outfit/coat/scarf/shoe combinations.
Review details: [male overworld QA](../qa/male-overworld-review.md).

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
  every throw-animation frame, then Safari, Frontier and the local Trainer Card and naming-screen icon.
- Verify the rival and other NPCs remain unchanged; check a native link session
  uses its existing appearance behavior. Repeat in Release and Debug.
