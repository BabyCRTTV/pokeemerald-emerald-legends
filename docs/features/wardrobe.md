# Wardrobe customization

Introduced in v0.0.23, refined in v0.0.24; shared by Release and Debug.

A small clothes box using Emerald’s native moving-box artwork stands directly beneath the bed in your Littleroot bedroom. Face it from an adjacent tile and press A. Your rival’s wardrobe remains private. Interaction opens customization directly.

Use Up/Down to select OUTFIT, SCARF, JACKET, APPLY or CANCEL. Left/Right cycles a setting; A also cycles the selected setting. The native trainer portrait updates immediately. APPLY keeps all pending changes; CANCEL or B discards them. Closing restores the field through the native map reload, so player graphics and reflections rebuild together. Your skin tone is retained.

| Setting | Choices |
| --- | --- |
| Outfit | Emerald, Trail, Sport, Yellow, Lavender |
| Added scarf | None, Crimson, Ocean, Emerald, Lavender, Cream |
| Jacket | None, Navy |

Scarf and jacket settings combine independently with all five outfits, both genders and the five existing skin tones. The Lavender outfit’s original cream neck trim remains part of that design when no added accessory is chosen; added scarves override its collar. The navy jacket has short sleeves and a visible center seam. Original Emerald gloves remain; custom outfits keep bare hands.

Accessories are visible on walking/running, both bikes, Surf, field moves, fishing/watering, local trainer front portraits, all four throw frames and the local Trainer Card. The diving suit keeps its native covered appearance. NPCs/rivals and remote Trainer Cards/link art remain native; this does not change the link protocol.

## Secret-base wardrobe

Buy WARDROBE for ₽3,000 at the Pretty Petal Flower Shop on Route 104, from the decoration seller (after the usual initial shop conversation). The native shop handles payment and full ornament storage normally. Place the 1x1 ornament through your secret-base PC’s Decorate menu under ORNAMENTS. Its placement, collision, removal and inventory persistence use the existing engine. Press A facing the box to customize in your own base. Other trainers’ wardrobes are private. Buying one does not create a base or bypass Secret Power progression.

## Implementation and assets

`src/legends_wardrobe.c` owns the screen and location checks; `legends_appearance.c` owns staged/saved choices. Pending wardrobe choices never write permanent vars until Apply. The original skin/outfit variable 0x404E still reads codes 0–25; new codes 26–30 preserve native skin with each outfit for legacy saves. Accessory var 0x40A1 encodes `scarf + 6 * jacket`, with zero meaning no added accessories. Invalid settings fall back safely. New Game resets accessories. No SaveBlock size changes.

`tools/legends/build_accessories.py` compiles pose-aligned layers into two binary asset packs with generated frame tables. The three accessory layers (scarf, jacket, both) add visible scarf tails and jacket silhouette/hem pixels while retaining native dimensions, frame ordering, faces, hands and held Poké Balls. Scarves reserve palette index 14; native white highlights consolidate into near-white slot 9 in accessory art, keeping red Poké Balls, skin colors and black outlines distinct. Covered diving palettes are unchanged. Builds use checked-in binary assets and need no art tools.

`tools/legends/build_wardrobe_furniture.py` copies Emerald’s native closed moving-box tiles into reserved Secret Base primary tiles (464–471), remapping their colors into the existing base palette, appends two shared secret-base metatiles (0x344/0x345), and appends two house metatiles (0x2C4/0x2C5). Existing metatile and decoration IDs are never renumbered. Decoration ID 121 is retained in the native ornament category, leaving inventory/save array sizes intact. The single-tile decoration replaces the previous 1x2 shape on normal map reload. No new sprite object consumes a room’s object-event budget.

To regenerate, install Pillow 11.3.0, run both authoring scripts, then the appearance, wardrobe and accessory asset regression tests. The Legends workflow compiles both variants and verifies both BPS patches.

## Emulator QA

- Test both home layouts and genders, including initial moving-in/clock/rival scenes; approach the storage box and confirm the rival’s wardrobe is private.
- Preview every scarf/jacket combination with each outfit and tone; Apply, Cancel and B; save/reset/continue; check a legacy save retains native skin.
- Check walking/running, bikes, Surf/Dive, fishing, watering, field moves and reflections; all battle throw frames, Safari/Frontier and the local Trainer Card.
- Buy the ornament with normal/full storage and insufficient funds. Place/remove/reposition it in tree, shrub and all cave bases; check collision, save/continue and own/friend base access.
- Confirm NPC/rival and native remote-link art are unchanged. Inspect menu borders/text/portrait after returning to the field. Compiled builds and host tests do not replace visual playtesting.
