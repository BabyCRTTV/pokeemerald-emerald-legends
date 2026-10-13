# Male overworld repair — review draft

The owner reported distorted male heads and outfits in the new-game, wardrobe and Trainer Card screens, then supplied a field screenshot with a cone-shaped blond head and beard-like face shading. The subsequent request explicitly authorizes generating all ten male field cuts for review and tuning. Published v0.0.46 and its approved predecessor artwork remain preserved on master. PR #64 is a draft, not a release or visual approval.

## Authoring and native integration

The built-in image generator produced `graphics/legends/male_overworld/generated-reference-draft.png` using the native Brendan field reference. The interface does not expose a selectable model ID. The prompt calls for youthful clean-shaven native Emerald proportions, recognizable ten cuts, consistent front/rear/profile identity, connected pixel clusters and the existing white/green Curls cap. The generated face/body is a design reference only.

`import_generated_world.py` samples hair and cap materials onto the existing 48×320 indexed head atlas. Pupil anchors are calibrated against the immutable reference; rear placement uses the native ears. The fourth source view actually faces west, despite its label. East continues to use native west mirroring. Sampling retains diagonal outline connections, removes disconnected label/neck artifacts and fills enclosed crown gaps. `male_overworld_sheets.json` records reference SHA256, exact grid/anchors and pending-review status. The previously pending Side Part is now included in this explicitly requested ten-cut draft.

`male_overworld_hair.py` places the heads in every native walking/running, Mach/Acro bike/trick, surfing, field-move, fishing and watering frame. Native pupils, lower faces, skin tone, hands, rod and props remain authoritative; gaps around the native ear/neck landmarks are filled. Hair never replaces the body, animation table or runtime facing flags. The native covered diving suit retains its existing path.

Field hair uses slots 4/7 and the existing black outline. Native blue slots 5/8 stay fixed. Protected brown skin contours are retagged to skin shadow 3, and native brown/blue body shades move to stable navy before hair painting, including Natural hair. This prevents blond hair from tinting the chin or outfit. Footwear still reserves its established slots 6/11. Curls reserves slot 13 for fixed green; native red-shadow details use red 12. Its cap white moves from 14 to white 9 when a scarf uses 14. Neither coat, scarf, outfit nor shoes changes cap identity.

The authored sparse ROM bank grows by about 20 KiB. Runtime still uses the existing shared 13.5 KiB field/back frame bank; no additional frame buffers or heap allocations are introduced. Saved wardrobe IDs and every native animation command remain unchanged. Fingerprints in `appearance-preservation.json` prove that all female field layers and every front/back sparse style layer remain byte-identical to portrait checkpoint `6ad7161`. Approved prepared battle bitmaps are untouched.

## Validation and review files

`legends-male-world.test.py` compiles the actual footwear/style compositor with the actual outfit/accessory banks and palette update function. It exercises 1,010 male native pose/style combinations, every hair color, 2,160 outfit/coat/scarf/shoe combinations and all 440 hair/color/skin choices, checks body RGB independence and native pupils/lower faces, repeats cached consumers and checks diving. The existing sparse geometry and footwear suites cover both trainers, all native table poses, anatomy/prop protection, relative frame descriptors and the shared field/battle cache. The imported atlas and source metadata must reproduce byte-for-byte.

The PNG/GIF below decode real compiled host-C field buffers at nearest-neighbor zoom. They are not emulator screenshots. GIF frame IDs, durations and east mirroring come directly from the native animation commands. `--preview` also exports 80 indexed native PNG sheets (ten cuts × eight movement states), with transparent slot 0 and 16-color RGB palettes. The ZIP contains runtime image-table order; walking sheets include all 18 walking/running frames. ROM integration consumes the atlas and sparse bank, rather than these review exports.

- [Ten cuts, four direction views](male-overworld-repair-preview.png)
- [Native walking cycles and all five outfits](male-overworld-walk-preview.gif)
- [Native sprite sheets](male-overworld-native-draft.zip)
- [Trainer Card / wardrobe / new-game front repair](male-front-repair-preview.png)

Debug and Release share these repairs. Native builds, vanilla input SHA1 and byte-exact BPS reapplication are verified by the PR build workflow. No exhaustive emulator playthrough is claimed. Artwork awaits owner review and tuning; VERSION, published downloads and Pages are unchanged.
