# Wardrobe customization

Introduced in v0.0.23, refined in v0.0.24, costumes added in v0.0.25; shared by Release and Debug.

A small clothes box using Emerald’s native moving-box artwork stands directly beneath the bed in your Littleroot bedroom. Face it from an adjacent tile and press A. Your rival’s wardrobe remains private. Interaction opens customization directly.

Use Up/Down to scroll through OUTFIT, COSTUMES, SCARF, JACKET, SHOES, TRAINER CARD, APPLY and CANCEL. Six rows are visible at once; the cursor wraps and follows the viewport. Left/Right cycles a setting; A also cycles the selected setting. The native trainer portrait updates immediately. APPLY keeps all pending changes; CANCEL or B discards them. Closing restores the field through the native map reload, so player graphics and reflections rebuild together. Your skin tone is retained.

| Setting | Choices |
| --- | --- |
| Outfit | Emerald, Trail, Sport, Yellow, Lavender |
| Costumes | None, Team Magma, Team Aqua |
| Added scarf | None, Crimson, Ocean, Emerald, Lavender, Cream |
| Jacket | None, Navy |
| Shoes | Original, Red, Blue, Green, White, Purple, Light-brown boots, Black boots |
| Trainer Card | Original, Emerald, Ocean, Crimson, Lavender, Gold, Rose, Slate |

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

## Complete costumes (v0.0.25)

COSTUMES chooses the native male/female Team Magma or Team Aqua grunt uniform. Walking and wardrobe/Trainer Card portraits use the exact original grunt pixel assets, with the selected skin ramp applied. Running uses the matching native walking motions at player speed. Bikes, Surf and field-action sheets adapt those uniforms to native player frame dimensions, while back battle art keeps all four player throwing motions under the matching hood or bandana. Diving remains in the covered native suit.

SCARF and JACKET display FIXED while a costume is active to preserve the full uniform. Their saved choices are kept. Choose NONE to restore them, or change OUTFIT to switch back to normal clothes. Apply saves; Cancel/B discards costume edits too. Var 0x40A8 stores 0/1/2 without changing SaveBlock sizes; invalid values use None and New Game resets the var. Existing NPCs/rivals and link protocol are unchanged.

`build_costumes.py` compiles independent 4bpp packs, frame tables and palettes. Its native uniform/front fidelity and frame/face/held-object checks run in project CI. Male Sport shorts now have explicit cloth hem stripes rather than recoloring entire trouser sections into skin.

Emulator QA: test every costume for each gender/tone, all directions and action states, mirrors/reflections, all battle throws and Trainer Cards; save/reset/continue, costume/normal switching, accessories restored from costume mode, Cancel and new-game reset. Host tests/build verification do not replace visual playtesting.

## Footwear and card colors (v0.0.31)

Boots use taller cuffed shafts and shaped toes/soles, rather than the shoe silhouette with a brown/black tint. Shoes preserve native rounded toes. The live trainer portrait previews both genders and all ordinary outfits; footwear follows native movement poses. Boots/shoes stay hidden under the native Surf/diving presentation where feet are covered. Throw portraits keep their normal crop, with palette shadow remapping to prevent footwear colors leaking into hair or clothing. Team costumes retain fixed native footwear; switch back to an outfit to customize shoes.

Trainer Card colors show a small live swatch below the portrait. They recolor the local card’s paper/frame accents without changing text, badges or achievement stars. Link cards remain native. APPLY saves shoes/card colors alongside the existing choices; B/CANCEL discards pending edits. Old saves default to Original.

Authoring uses `tools/legends/build_footwear.py`; generated masks live in `graphics/legends/footwear/masks.bin`. The runtime compositor caches native frames without expanding the 16-color player palettes; two shadow shades map to their nearest existing colors before dedicated footwear colors are applied. Skin and red Poké Balls retain separate palette slots. Actual-C checks exercise all native pose tables and protected pixels.

The overworld compositor uses one 13.5 KiB bank sized by the generated native pose metadata. Only the local player uses custom overworld graphics; NPC/link art remains separate. This covers the largest 27-frame Acro Bike sequence within the GBA RAM budget.

## Underwater color preservation (v0.0.36.1)

Choosing colored shoes or boots no longer remaps native diving-suit palette indices or modifies underwater sprite frames. Diving shoes are not visible, so the existing unmodified art is used. This focused compatibility fix is not the full requested wardrobe redesign; dry-land palette sharing, improved boot/coating silhouettes, a gender-tailored shearling winter coat, and ten working hairstyles need further artwork and playtests.

## Hairstyles and winter outerwear (v0.0.37)

The opening customization now goes from gender to skin tone, then hairstyle, then outfit. The hairstyle step uses Left/Right for a live one-row portrait preview rather than squeezing all eleven choices into a five-row window. The original Emerald hat is still available, plus Crop, Side Part, Spikes, Side Sweep, Tousled, Pixie, Bob, Curls, Ponytail and Twin Tails. The wardrobe HAIR row lets existing characters change the same choice without restarting. Team Magma and Aqua grunt costumes retain the native hood/bandana, leaving the underlying hairstyle saved for ordinary outfits.

The JACKET row now offers None, Navy and Winter. Winter adds an ivory shearling collar over dark tailored panels with small buttons; the female silhouette narrows at the waist. Existing scarves, outfits and card/footwear settings are preserved. Old accessory values 0-11 remain valid; winter codes occupy 12-17 using the same existing wardrobe variable. Existing saves default to original hair through the verified-unreferenced native Mauville state var; New Game resets it to zero. No saved structure size or link protocol changes.

### Replacement artwork (v0.0.38)

The first procedural art pass in v0.0.37 was replaced. `tools/legends/build_style_layers.py` authors discrete pixel contours against every native animation-table pose. Its checked-in ROM edits cover the front portrait, all four throw frames and walking/running/bike/field-action tables. `src/legends_style_layers.c` only applies those edits; it does not estimate face positions or draw geometric hairstyles at runtime. Regenerate with Pillow 11.3.0 and `python3 tools/legends/build_style_layers.py`.

Coats are composed before hair, with selected scarf pixels kept in front. Thick shearling lapels, shoulder/sleeve contours, a front fastening and fitted female hems give outerwear its own silhouette. Boot cuffs and soles are authored in the footwear masks rather than scanned from shared colors. Footwear uses slots 6 and 11, retaining May's hair/eye slot 7; jacket shading uses 5 and 8. Accessory templates move native white from 14 to 9, whose exact white value is restored for both scarves and jacket-only templates.

The existing 13.5 KiB overworld bank and portrait buffers are reused. Save variables and selection IDs are unchanged. Diving suits and team costumes retain their native artwork. Tests compile the actual sparse compositor and integrated footwear cache, exercise all 212 native animation-table poses, and check face/hand/ball protection and independent hair/shoe choices. Authoring renders are available in `docs/qa/wardrobe-v0.0.38.png` and `docs/qa/wardrobe-actions-v0.0.38.png`; regenerate them with `python3 tools/legends/preview_style_layers.py`. These are sprite renders, not emulator screenshots. Full emulator traversal remains a follow-up visual playtest.

Native mGBA 0.10.2 review uses controlled wardrobe callback entry. Both genders, all eleven hairstyle selections, Winter/brown-boot portraits and scarf changes render through the game's real UI. The head/face crop is unchanged across the tested scarf colors. Emulator captures: `docs/qa/wardrobe-female-mgba-v0.0.38.png`, `docs/qa/wardrobe-male-mgba-v0.0.38.png` and `docs/qa/wardrobe-scarf-mgba-v0.0.38.png`. Full field traversal and save/load remain separate playtests.

### Gender-specific hairstyles (v0.0.38.1)

All ten custom choices use separate male and female contours. Female cuts have their own layered fringes, rounded bob/curl silhouettes and higher, longer tied hair; male cuts retain independent cropped and angular contours. Names and saved IDs are shared, while their actual artwork differs. The existing v0.0.38 QA filenames now show this follow-up artwork.

### Vertical hairstyle lists and native-grid art (v0.0.39)

The intro now displays five choices at once. Use Up/Down to scroll, A to select and B to return to skin tone. In the wardrobe, highlight HAIR and press A to open a six-row list. A stages that choice for APPLY; B restores the hairstyle selected before opening the list. The original hats and ten hairstyle IDs remain unchanged.

`tools/legends/hair_pixels.py` contains separate male/female portrait and overworld pixel clusters. Front and overworld patterns are placed without scaling; back portraits use their own corrected head proportions. Coats now cover exposed arms through the protected hand boundaries. All palettes are unchanged. Authoring sheets: `docs/qa/wardrobe-v0.0.39.png` and `docs/qa/wardrobe-actions-v0.0.39.png`. These are source-art renders, not emulator captures.
