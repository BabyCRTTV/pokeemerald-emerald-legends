# Pokémon Emerald: Legends - Release Changelog

This is the player-facing history for the recommended **Release** build. Shared Legends changes are repeated here so this file stands on its own; Release-only behavior is called out separately.

## [0.0.47] - 2026-10-14

- Preserve the existing v0.0.46 trainer sprites, approved hairstyles and native animations as the baseline for further improvements.
- Fix male smile, chin, ear and bare-skin contours taking the selected hair color in the new-game selection, wardrobe, Trainer Card and overworld sprites.
- Keep clothing/body colors stable across hair colors, including Natural, and prevent footwear recoloring from borrowing reserved hair colors.
- Preserve saved wardrobe choices, female sprites, approved battle art, fixed costumes, diving and untouched Original. Shared by Release and Debug; no variant-specific gameplay differences. Validation: `docs/qa/appearance-color-fix.md`.

## Wiki 1.6.0 - 2026-10-13

- Owner-requested documentation refresh against game v0.0.46. Preserve the wiki design and walkthrough layout; extend Chapters 19–25 through Seafoam, the Hoenn intermission, northern/western Kanto and Faraway Island.
- Review all eight visiting Gyms, story gates and legendary observation/capture rules. Add Quest Log, achievements/rewards and expanded-storage guides; update wardrobe, leggings and fixed battle-uniform details.
- Refresh the pinned encounter catalogue to 157 locations, including the limited Mt. Ember expedition. Keep Sevii encounter locations separate from mainland map markers; add footer links to the project site.
- Documentation applies equally to Release and Debug; no variant-specific differences. ROM VERSION and verified BPS patches remain v0.0.46. Native wiki companions rebuild through their existing independent workflows.

## [0.0.46] - 2026-10-13

- Publish the nine approved male overworld hairstyles: Crew Cut, Spiky, Side Sweep, Tousled, Quiff, Shag, Curls, Man Bun and Undercut. Fit front, rear and profile views to native walking/running, both bikes and tricks, Surf, field moves, fishing and watering. Retain native east mirroring and the covered diving suit.
- Anchor each head to native pupils or ears, preserve lower faces, hands and props, and let the undercut temple follow the selected skin tone. Three independent hair shades preserve native pupil RGB through hair-color, coat, scarf and footwear changes.
- Keep male Side Part on its published v0.0.45 art and palette while its separate revision awaits visual approval. Preserve all approved battle art and female overworld art unchanged.
- Validate the native sparse compositor, saved settings and footwear caches. Prepare a complete labeled PNG/GIF review archive covering both trainers, field activities, colors, skin tones, battle throws and front/wardrobe portraits.
- Shared by Release and Debug; no variant-specific gameplay differences. See `docs/qa/male-overworld-review.md`.

## [0.0.45] - 2026-10-13

- Add ten prepared male battle hairstyles: Crew Cut, Side Part, Spiky, Side Sweep, Tousled, Quiff, Shag, Curls, Man Bun and Undercut. Match the existing male wardrobe IDs and refresh the cut/color/skin tone on the next battle after APPLY.
- Fit supplied hair to Brendan's native face, hands, body and all four throw poses. Preserve the red gloves, green cuffs/backpack and original animated Ball.
- Use independent male hair slots and all eight existing hair colors/five skin tones in the fixed native battle uniform. Keep the Original option's native hat and preserve all forty approved female bitmaps unchanged.
- Remove native cap-edge remnants beside the raised glove and use hair-shadow colors for interior strands instead of fixed black specks. Preserve native fingers, cuff, face, collar and body geometry.
- Retain the reference's small white-and-green cap on Curls, above its exposed ringlets. Join its white crown into one clean panel, remove isolated white brim/edge fragments, and soften the border with native slate outlines and pale gray shading. Fixed cap colors remain independent of all eight hair colors and five skin tones; the other nine male cuts are unchanged.
- Extend prepared-battle validation to twenty cuts/eighty frames, native anatomy, silhouette connectivity, fixed clothing and current wardrobe choices.
- Shared by Release and Debug; no variant-specific gameplay differences. Authoring and validation: `docs/features/male-battle-appearance.md`.

## [0.0.44] - 2026-10-13

- Import the ten supplied female battle hairstyles into fixed-outfit, four-frame Emerald battle sprites: Pixie, Side Part, Soft Layers, Side Sweep, Wavy Bob, Short Bob, Long Bob, Curls, Ponytail and Twin Braids. Use the matching saved hairstyle and hair color when entering a battle; wardrobe changes take effect on the next battle.
- Give battle art an independent palette with five dedicated skin-tone ramps. Preserve hair, red uniform, gloves and outlines when skin tone changes. Keep all eight existing in-game hair-color choices, including Dark Brown.
- Use a fixed battle uniform instead of layering wardrobe outfits, coats, scarves, footwear, leggings or costumes onto battle backs. Overworld customization and front/wardrobe portraits continue normally. Male and Original-hair female battles use native Emerald art with the selected skin tone until corresponding prepared sheets are available.
- Fit the supplied hair to native May's original face, body proportions and four throwing poses, using clean three-shade Emerald hair palettes. Keep the native 64x64 frames and moving Ball animation; omit the detached illustration Ball from the supplied sheets.
- Align battle hair to native eyes in every pose. Preserve full glove cuffs and collar boundaries, restore the arm hidden under May's original hair, and remove leftover forelock/nape pixels; check all 40 frames for detached anatomy or stray pixels.
- Add a visible red Ponytail tie in every pose and let Twin Braids drape behind the shoulder with a small throw sway. Preserve the other eight approved cuts unchanged.
- Remove the approved three leftover shoulder cells from May's custom front portraits, including geometry added by legacy jacket assets. Preserve the connected collar and sleeve.
- Shared by Release and Debug; no variant-specific gameplay differences. Prepared-sprite pipeline and validation: `docs/features/battle-appearance.md`.

## [0.0.43.1] - 2026-10-12

- Center every Text Speed value (SLOW, MID, FAST and INSTANT) between its Options-menu arrows using the native font-width helper.
- Shared by Release and Debug; no variant-specific differences.

## [0.0.43] - 2026-10-12

- Add a second pause-menu page with QUEST LOG, ACHIEVEMENTS, ADVENTURE LOG and EXIT. Left/Right switches pages; small directional arrows show the extra page. Keep linked-room menus and native activity controls available.
- Track 33 quests: Hoenn's main adventure, every shipped Wing Survey chapter, the central-Hoenn Regigigas intermission, and seven basic side quests. Main/Side/Completed views show automatic objective checkmarks from native story flags; earlier saves recover their progress without replaying the story.
- Add 80 permanent gameplay/progression achievements covering badges, visiting Leaders, expedition reports, collecting, battles, exploration, breeding, evolution, berries, fishing, contests, DexNav and the Battle Tower. Record stat thresholds as they happen, including streaks that later reset. Each achievement grants a varied berry bundle once, claimed from its detail screen into PC ITEM STORAGE; a full PC retains the pending claim for a retry.
- Expand Pokemon storage from 14 to 20 boxes (420 to 600 slots), PC item storage from 50 to 150 slots, and Bag pockets to 150 Items / 60 Key Items / 32 Balls / 128 TMs-HMs / 80 Berries. Preserve original save-field offsets and migrate earlier Legends profiles automatically, including boxed Pokemon, box names/wallpapers, fusions, and every original inventory entry.
- Store expanded PC/inventory data in a bounded, lossless compressed payload across the existing nine PC save sectors. Retain both alternating 128 KiB save slots, native Hall of Fame/Trainer Hill/recorded battles, sector checksums and an additional packed-payload integrity check. Normal, link and Frontier save paths include claimed rewards and expanded inventories. Check capacity before writing any flash; reject an oversized payload without replacing either existing save. Technical details and limits: `docs/features/quest-log-achievements.md`.
- Correct nighttime window/sign colors to authored warm glass and pink-red Center signage with smooth native dusk/dawn palette swaps. Add previously missing town-specific windows while keeping daytime artwork and unlit roofs, walls, water and paths intact.
- Fix bike/fishing direction and crown placement, preserve fishing rods, and apply selected hair/coats/footwear to ordinary battle back sprites and all four throw poses. Remove May's detached native shoulder hair triangle for custom cuts. Add female-only Grey/Black leggings in the wardrobe, with native neutral colors and shoes/boots drawn above them; preserve outfit/hair/eye colors, costumes and diving suits.
- Shared by Release and Debug; no variant-specific gameplay differences. Both variants retain their established developer-feature separation and verified-BPS pipeline. Validation evidence and limitations: `docs/qa/journal-storage-v0.0.43.md`. Wiki content updates remain manual.

## [0.0.42] - 2026-10-12

- Continue the Wing Survey with **The Last Record**, **A Familiar Shadow**, and **Beyond the Horizon**. Open the native western Kanto circuit through Route 2/Viridian Forest, Viridian City, Route 1, Pallet/Oak's lab, and the Route 21 Surf connection from Cinnabar.
- BLUE serves as Viridian's visiting acting Leader. Standard uses four Pokemon at Lv. 64-68; Champion uses six at Lv. 84-88. Either grants the same permanent eighth record. Native trainer-save capacity and all existing map/layout IDs remain unchanged.
- OAK compares the birds' habitats and the Hoenn investigation with an old voyage record. After the full survey and eight Gyms, grant one OLD SEA MAP and unlock the original Lilycove/Faraway Island ferry. Reuse the existing map/item/ship flags; existing maps are recognized and a full Bag delays issuance safely.
- Preserve Emerald's single overworld MEW and native deep-grass puzzle/Lv. 30 encounter. Observation completes the story without capture; on the survey, fainting/fleeing allows forest-reentry retry. Existing MEW captures receive an alternate weathered-sign/sailor scene without another spawn. Native capture state is retained permanently.
- Add OAK's final report, a one-time MASTER BALL (Bag, then PC fallback, with retry if both are full), a healing assistant, Adventure Log milestones and BIRCH's closing letter at the Weather Institute. All original Hoenn postgame and return travel remain available.
- Enable native day/night lighting for standard Hoenn and Kanto house windows and illuminated Center/Mart signs. Dedicated tile/palette copies keep daytime RGB and unlit roofs, walls, ground and water unchanged; lights fade smoothly with dusk/dawn.
- Fix custom hairstyle walking/running direction jumps. Match every step, bike and field-action hair mask to its actual native source-sheet direction; keep native faces and selected colors/accessories intact.
- Shared by Release/Debug. Verify event gates, all eight records, mode/decline/loss/retry, map connections/closures, old-map/full-inventory cases, MEW observation/capture/reentry/legacy profiles and reward idempotency. Native build and BPS verification use the established workflow. Targeted emulator evidence and limits: `docs/qa/finale-v0.0.42.md`. Wiki updates remain manual.

## [0.0.41] - 2026-10-12

- Add Wing Survey chapters four through six: **Stillwater Wings** (Seafoam/Articuno), **Stone and Tide** (Cerulean/Pewter readings and visiting Misty/Brock challenges), and **Ember's Passage** (Blaine's Cinnabar record and a returnable Mt. Ember/Moltres expedition). Native FireRed habitat layouts and wild levels are retained; bird observation advances without capture. Articuno and Moltres are optional Lv. 50 encounters with reentry retries when uncaught.
- Add the central-Hoenn intermission **The Sleeping Continent** after the Seafoam report. Investigate the Weather Institute's field readings in either order, enter the fault beside Fiery Path's southern doorway, restore three buried regulators, and face Lv. 70 Regigigas with native Slow Start and Regi battle music. Victory or capture settles the anomaly; flee/loss permits retry, and a defeated titan remains available for later capture. The Institute report returns the player to the Kanto survey.
- Add thirty native Kanto/Sevii map imports and a Hoenn vault with append-only map/layout IDs, active Centers/Marts, clear development closures, reciprocal roads, an explicit Route 4 return trail around native one-way ledges, and a permanent expedition return boat. The rest of Sevii, Viridian's challenge and the final Mew voyage remain future content.
- Give Misty, Brock and Blaine separate Standard/Champion teams with one permanent victory per Leader across both difficulties. Keep native trainer-save capacity at 864 and map the six appended trainer IDs to existing dedicated Gym records; preserve all Hoenn badge/progression flags.
- Port Seafoam's native Strength/boulder/current puzzle to independently allocated Emerald flags and a separate saved current-entry variable. Persist both the upper-floor removal and lower-floor reveal when a boulder falls. Retain native field-move requirements and all existing maps/records/save-structure offsets.
- Add Adventure Log milestones and a current journal path for all new reports. Hoenn's temporary storm/fog override is limited to Routes 119/120 during the intermission; protected weather, sandstorms, indoor maps and the original Rayquaza resolution remain native. Normal forecasts resume when Regigigas is calmed.
- Shared by Release and Debug; no variant-specific gameplay differences. Regression checks execute observation/capture/retry, report and travel gates, both Gym modes, both field-reading orders, all regulator orders, native dialogue widths, warp geometry, flag allocation, and actual-C weather/Seafoam boundaries. Emulator review and limits are recorded in `docs/qa/story-v0.0.41.md`. Both builds and verified BPS publication use the established workflow. Wiki updates remain manual.

## [0.0.40] - 2026-10-12

- Repair incomplete skull/nape coverage on all ten custom hairstyles across the 212 native animation-table poses, including facing away, cycling, field actions and throw portraits. Separate touching cheek/forearm pixels in raised-arm poses.
- Give Boy and Girl distinct named hairstyle lists. Boy choices include Crew Cut, Quiff, Shag, Man Bun and Undercut; Girl choices include Pixie, Soft Layers, Wavy/Short/Long Bob, Ponytail and Twin Braids. Original and existing saved IDs remain supported.
- Add a separate vertical hair-color list to the intro and wardrobe: Natural, Black, Dark Brown, Chestnut, Auburn, Honey, Blond and Silver. Hair colors keep native eyes, skin, shoe colors and costume/diving palettes separate. Existing hairstyle saves retain Natural color; no SaveBlock layout changes.
- Make wardrobe HAIRSTYLE and HAIR COLOR lists accessible with A or Left/Right, with explicit on-screen controls. Up/Down scrolls the list; A keeps the pending selection, B restores its entry value, and APPLY saves both choices for the field.
- Extend both jackets fully to the cuffs. Navy uses fixed navy fabric; Winter uses dark green fabric with ivory shearling, independent of the outfit or hair color. Preserve gloves, held balls, scarf layering and tailored hems.
- Shared by Release and Debug; no variant-specific differences. Regression checks cover complete head coverage, forearm coverage, all 88 saved hair/color codes, intro/wardrobe lifecycle, protected palettes and the integrated footwear cache. Native mGBA evidence and playtest scope: `docs/qa/appearance-v0.0.40.md`. Both variants use the established verified-BPS release workflow.

## [0.0.39] - 2026-10-11

- Replace the intro's single Left/Right hairstyle row with a five-row Up/Down scrolling list, scroll indicators and live preview. Widen the existing choice window within its allocated tiles so long names and arrows do not overlap. A selects; B returns to skin tone; revisiting restores the chosen hairstyle.
- Open a six-row vertical hairstyle list with A on the wardrobe HAIR row. A keeps the previewed selection for APPLY; B restores the hairstyle from before opening that list. Sideways input no longer changes hair. Team costumes remain fixed.
- Redraw all ten custom hairstyles from the supplied Brendan/May reference direction: connected shaded locks, rounded crowns, readable cropped/parted/swept fringes, spikes, fuller bobs/curls and tied silhouettes. Author separate male/female portrait and overworld grids, retain Original and all saved hairstyle IDs, and anchor back portraits to each native throw pose.
- Give custom male hair a warm highlight in slot 7, moving the original blue clothing shade to stable slot 5 before footwear overlays. Preserve native eye/face indices and colors, female hair shades, native underwater palettes and fixed costumes. Scarf, coat and footwear changes cannot tint the hair. Extend Navy/Winter sleeves and refine hems; no save-layout changes.
- Shared by Release and Debug; no variant-specific differences. Actual-C regressions cover intro/wardrobe scrolling, preview/apply/cancel, all 212 native sprite poses, exact eye-border pixels, 900 hair/scarf/coat/skin palette combinations and footwear caches. mGBA 0.10.2 reviews both genders, all eleven intro choices, A/B re-entry, wardrobe scrolling and Winter/brown-boot previews; rendered head RGB stays byte-identical across tested scarf colors. Evidence and playtest limits: `docs/qa/appearance-v0.0.39.md`. Both builds and byte-for-byte BPS verification use the established release workflow.

## [0.0.38.1] - 2026-10-11

- Give each of the ten hairstyles separate male and female pixel contours, with distinct fringes, crown shapes, bob/curl lengths and higher/longer female tied styles. Retain the original Emerald hat and all saved hairstyle IDs.
- Clear the native hat tip above replacement walking crowns. Regenerate all 212 pose masks and review both genders in authoring renders and the native mGBA wardrobe UI. Sparse-compositor and footwear/cache checks pass; full field traversal and save/load remain follow-up playtests.
- Shared by Release and Debug; no variant-specific differences. Both variants and verified BPS patches use the established release workflow.

## [0.0.38] - 2026-10-11

- Replace v0.0.37's procedural head/coat painter with authored, pose-specific sparse pixel art. Ten hairstyle choices retain their saved IDs, with smaller shaded crowns, partings, curls, sideburns and tied tails. Resolve each native animation pose at authoring time instead of guessing the face/torso coordinates on the GBA.
- Redraw Navy and Winter outerwear with shoulder/sleeve contours, front fastening and coat hems. Winter has thick turned shearling lapels; the female coat has a fitted waist and flared hem. Scarves remain in front of coats, and native backpack/hand/held-ball details remain protected.
- Refine leather boot cuffs, tapered shafts, shaded toes and continuous soles in the pose masks. Remove the shared-color boot finishing scan. Move footwear's shadow slot from 7 to clothing slot 11 so May's native hair/eye shade is retained. Restore exact white for eyes moved into slot 9 by scarf/jacket templates; Navy shading avoids footwear slots.
- Store sparse art in ROM and reuse the existing pose and portrait buffers; no extra animation bank or saved-data changes. Preserve native underwater suits, team uniforms, selection/apply/cancel controls and old hairstyle/accessory codes.
- Shared by Release and Debug; no variant-specific differences. Actual-C checks cover 212 native animation-table poses, all hairstyle/coat combinations, face/hand/ball protection, ROM-mask reproducibility, palette isolation and integrated footwear cache rebuilds under address/undefined-behavior sanitizers. Authoring renders reviewed; full emulator traversal remains a follow-up visual playtest. Both compiled variants and BPS byte-for-byte verification use the established release workflow.
- mGBA 0.10.2 checks both genders' live wardrobe previews, all eleven hair selections, Winter coats with brown boots, and Crimson/Ocean scarf changes. The same hair/face crop stays byte-identical across scarf changes. Controlled native wardrobe callback entry was used; full overworld traversal and save/load remain follow-up playtests. Remove detached coat-outline marks found during this emulator review.

## [0.0.37] - 2026-10-11

- Expand the trainer wardrobe to include 11 hairstyle choices (the untouched original hat and 10 distinct pixel-silhouette styles: crop, side part, spikes, side sweep, tousled, pixie, bob, curls, ponytail and twin tails). Birch's introductory customization now progresses skin tone -> hairstyle -> outfit with a compact Left/Right hair selector and immediate trainer preview. Wardrobe HAIR is scrollable and supports Apply/Cancel.
- Add distinct rolled boot cuffs and dark continuous outsole finishing over the existing tall-shaft boot masks; leave the original native sneaker choices intact.
- Add a WINTER jacket with an ivory shearling collar, overlaid coat panels, decorative buttons and narrower female tailoring, alongside NONE and the existing NAVY jacket. The 6 scarf colors remain selectable and Team Magma/Aqua uniforms remain fixed.
- Paint haircut and winter-clothing differences into the existing local 4bpp player pose / trainer portrait cache without allocating a second overworld frame bank. Preserve native face skin and eye pixels, hands and red ball indices. Original hair and outerwear remain the default; hairstyles and coats apply to the native player, not NPCs or linked remote cards.
- Preserve old wardrobe accessory codes 0-11 and allocate 12-17 for winter coats. Save the hairstyle in the unused Mauville state var, with zero retaining original graphics; no SaveBlock or link-protocol changes. v0.0.36.1's diving palette/pixel preservation remains included.
- Shared in Release and Debug; no variant-specific content changes. Regression tests cover hair silhouette independence, palette/eye protections, staged selections and winter coat behavior. Pixel-art appearance still warrants hands-on emulator review across every pose.

## [0.0.36.1] - 2026-10-11

- Wardrobe footwear compatibility: preserve the native underwater suit sprites and palette byte-for-byte when any shoes or boots are selected. The diving state has no visible footwear; its unnecessary shadow remapping could tint other suit/head details.
- The dry-land footwear, scarves, jackets and trainer portraits remain unchanged. The larger requested sprite/art redesign, shearling coats and ten hairstyles still require their own animation and visual QA; they are not included in this fix.
- Shared in Release and Debug; no variant-specific differences. Strengthen actual-C regression coverage for underwater palette and native sprite identity. No changes to saves, Kanto progression or the wiki.

## [0.0.36] - 2026-10-11

- Enable the expansion's native first-time obtained-item descriptions for supported gifts, field pickups, hidden items and harvest scripts. The top window explains the item while the normal receipt dialogue and icon remain native; subsequent receipts retain the small icon without repeating the description.
- Append item-history bits after the existing Adventure Log in reserved SaveBlock3 sector space. Preserve all previous save-field offsets and saved PC contents, including native partial/link saves; validate sector identity/checksum and reuse the existing verified flash writer. Existing profiles begin tracking discoveries after this upgrade; historical receipts cannot be reconstructed.
- Add compact Left/Right arrows around the selected Text Speed value, including INSTANT, within the existing Options window.
- Shared in Release and Debug; no variant-specific differences. Wiki files/workflows are unchanged. Host checks cover every item ID, invalid IDs, legacy profiles and all 28 save-slot/rotation layouts, partial-save PC preservation and flash failures. mGBA 0.10.2 verifies all four text-speed labels/arrows, native first/repeat Potion receipts, two-line Escape Rope and TM descriptions, dismissal, full save/load and both partial-save paths. Controlled native reward-script entry was used. EWRAM grows by 112 bytes; the existing sector buffer is reused. Native builds and verified BPS publication use the established workflow.

## [0.0.35] - 2026-10-11

- Add five understated native window frames: TYPE 21 Leaf, TYPE 22 Ocean, TYPE 23 Lavender Stitch, TYPE 24 Amber Circuit and TYPE 25 Poké Ball. Select them in General Options → FRAME; the native live preview and Left/Right wrap now cover 25 types.
- Append indexed nine-tile art and palettes to the existing frame table. Preserve the original 20 frame IDs, white text interiors, native text palette slots, window dimensions and tile allocation. The existing five-bit saved selection holds all 25 types without a save-layout change.
- Same frames in Release and Debug; no variant-specific differences. Wiki files/workflows and fixed native dialogue/battle graphics are unchanged. Add repeatable pixel-art generation and asset/selection checks for palette, tile and save limits. mGBA 0.10.2 checks all five live Options previews, TYPE 1↔25 wrap, saved TYPE 25 after field reload, and its native Yes/No menu plus dismissal. Controlled map entry was used; RAM usage is unchanged.

## [0.0.34] - 2026-10-11

- Add **INSTANT** to General Options → Text Speed, alongside Slow, Mid and Fast. Reuse pokeemerald-expansion's existing instant renderer; text appears immediately while page confirmations, scripted pauses and choices retain their native behavior.
- Display the selected speed alone and clear its previous label before redraw, keeping the existing safe Options window dimensions. Left/Right cycles all four speeds; B saves as usual. Existing saves retain their chosen speed and the New Game default remains Mid; no save-layout changes.
- Shared feature in Release and Debug; no variant-specific differences. Wiki files and wiki workflows are unchanged. Options navigation/redraw regressions cover all four speeds; mGBA 0.10.2 checks the selected label, saving back to the field, immediate text, a page waiting without input, and A advancing to the next page.

## [0.0.33] - 2026-10-11

- Add Wing Survey chapter three, **The Quiet Current**: north from Lavender through native Rock Tunnel to Route 10's Center and the Surf approach to the Power Plant. Isolate two unused electrical feeds in either order, observe Zapdos, then file Oak's aide's report. Zapdos can optionally be challenged at native FireRed level 50; observation alone advances the story. Capture persists, while fainting or fleeing allows a later visit to retry. Seafoam is the next lead; no new Gyms, Articuno, Moltres or Mew battles in this version.
- Restore every populated Kanto area's wild encounter slot levels to its original FireRed table, including land, Surf, fishing and Rock Smash. Preserve species distributions and encounter rates; visiting Gym challenge teams retain their chosen difficulty.
- Move the Trainer Card's compact L/R badge-region hint to the right of the existing BADGES heading, clear of the Time stat and badge icons. Add survey milestones to the Adventure Log using append-only event IDs.
- Preserve SaveBlock sizes, existing map/trainer IDs and saved system-flag addresses. Allocate five previously unused flags for the new survey and optional capture. Wiki files and wiki workflows are unchanged.
- Same gameplay and fixes in Release and Debug; no variant-specific differences. Developer conveniences remain Debug-only. Automated checks exercise progression gates, either-order console work, observation without battle, capture/retry outcomes, native wild levels, map warps and badge-heading bounds. Full builds and verified BPS publication use the established workflow.
- mGBA review checks all four seasonal Route 10 scenes, Power Plant console/roost art, native cave/Center rendering, real west-console acceptance, and Trainer Card Hoenn/Kanto switching plus front/back/front with all stats visible. Controlled native map entry was used; full story traversal and manually played capture/blackout remain follow-up playtests.

## [0.0.32.1] - 2026-10-11

- Fix bright horizontal stripes and the cyan top ramp in seasonal outdoor plain battle backgrounds, including scripted Stunky and ordinary trainer encounters. Normalize only their shared stripe/sky palette indices to native tall-grass colors before seasonal tinting; preserve plain platforms, battle terrain mechanics, sprites, UI and special/indoor backgrounds.
- Exercise all four seasons, all 20 native weather IDs and wild/scripted-first/trainer flags, including repeated palette restoration and sand/ash exclusions. Shared fix in Release and Debug; no variant-specific differences or save-layout changes.
- mGBA 0.10.2 rendered 240 native battle scenes across four seasons, twenty map-weather inputs and Poochyena/first-battle Stunky/May configurations. Eligible stripe/sky palette slots match; ash and sand retain native backgrounds, including dynamic weather resolving to sandstorm. Controlled native battle entry was used; this is not a full story walkthrough.

## [0.0.32] - 2026-10-11

### Added
- Celadon and Saffron visiting Gyms, retaining native FireRed garden/Cut and teleport-room geometry. Erika offers Standard Lv. 54–58 / Champion Lv. 74–78; Sabrina offers Standard Lv. 58–62 / Champion Lv. 78–82. Standard teams have four Pokemon and Champion teams have six. The entrance guide explains that winning either mode permanently completes that Gym; losses and declined battles allow retry/reselection.
- WING SURVEY chapter two, **The Borrowed Voice**. After filing Surge/Koga's opening report, win Erika/Sabrina's challenges in either order and examine leaves with Route 16's birdwatcher and listen to copied calls with Route 8's researcher. Oak's aide lists missing tasks, files the field report once, and distinguishes a migrating bright bird from an unidentified smaller imitator. The Power Plant expedition and bird/Mew battles remain future chapters.
- Trainer Card supports eight Hoenn and eight Kanto badge slots in separate collections. On the local card front, Left/Right, L/R or SELECT switches the badge strip; unearned Kanto badges are dimmed. Existing Surge/Koga victories display immediately. Kanto victories play the native badge fanfare; Hoenn field permissions, card stars and linked-card format are unchanged.

### Compatibility and visual checks
- Separate trainer-table capacity from native saved trainer-flag capacity. New Erika/Sabrina teams resolve to their existing dedicated Gym victory bits. Preserve MAX_TRAINERS_COUNT_EMERALD=864, system-flag addresses, old trainer IDs and SaveBlock layouts; move transient partner IDs above the enlarged trainer table and update Debug/slide indexing and route Debug trainer toggles through the same safe flag mapping.
- Restore native Cut trees on Celadon's Gym approach. Reopen only the two Gym doors; retain append-only map IDs and every Saffron teleport slot. Enable native Erika/Sabrina/tree sprite data, frame tables and graphics pointers for Emerald. Place residents/researchers on ground beside paths; guides/staff look around without walking into maze lanes.
- Event checks cover both modes, one-win locks, loss/decline/retry, site prerequisites, either-order fieldwork, journal missing tasks and repeated visits. Actual-C tests check trainer-flag addresses and 1,024 badge-rendering combinations, palettes, tile bounds and linked-card isolation. Native map/sprite renders and dialogue font widths reviewed. Manual emulator traversal, card flips and team balance remain playtest work; full Debug/Release builds and BPS byte comparisons run in the established workflow.

### Build variants
- Shared gameplay, maps, story and Trainer Card behavior in Release and Debug; no variant-specific gameplay differences. Debug retains native developer conveniences and the corrected partner-trainer selector.

## [0.0.31.1] - 2026-10-10

- Keep a stable calendar origin when switching between real and manual bedroom clocks, preventing native hour borrowing from shifting the day count. Preserve existing clock counters and legacy calendar timestamps.
- Test actual native RTC subtraction across midnight, mode changes and restored RTC support.
- Shared in Release and Debug; no variant-specific differences.

## [0.0.31] - 2026-10-10

### Added
- Scrolling wardrobe categories with SHOES and TRAINER CARD. Footwear adds red, blue, green, white and purple shoes plus light-brown and black boots; Original remains available. Boots have separate tall shafts, cuffs, toes and soles in the live portrait and pose-local overworld overlays.
- Seven custom Trainer Card colors: Emerald, Ocean, Crimson, Lavender, Gold, Rose and Slate, plus Original. A small live color swatch appears below the wardrobe portrait. Star counts, badges and link cards retain native behavior.
- A dismissible top-left DexNav instruction window when there is no nearby wild-encounter terrain with matching map encounters.
- REAL TIME (default) and MANUAL clock choices at the bedroom clock, available on the first visit and later visits. Real time follows the emulator/device RTC without the old introductory offset. If a valid RTC is unavailable, the clock starts at 9 AM plus saved accumulated playtime; fallback continues past the native 999-hour timer cap.

### Changed and fixed
- DexNav Pokémon no longer flee when approached by walking, running or cycling; search timeout increases from 15 to 45 seconds. Cancellation, out-of-range signal loss and battle initiation retain native behavior.
- The pause clock continues polling once per second and redraws on minute rollover, including the fallback clock. Opening the pause menu does not stop the underlying RTC or playtime clock.
- The introductory bedroom clock confirms the current time instead of resetting it. Manual adjustment is confined to your own bedroom clock in normal gameplay; the rival’s clock remains view-only. Invalid RTC months and out-of-range hours/minutes/seconds are rejected safely.

### Compatibility and validation
- Existing saves keep their original footwear/card color until changed; outfits, skin tones, scarves and jackets remain supported. Native Team Magma/Aqua costumes keep fixed footwear, as they do fixed accessories. No save layout or link-protocol changes; settings use verified-unreferenced native variable slots.
- Actual-C host checks cover wardrobe scrolling/wrap/apply/cancel, cosmetic save defaults, native footwear poses and palette protection, card colors, nearby DexNav terrain, RTC/manual/fallback priority, minute rollover and saved fallback ticking. Native-art footwear contact sheet reviewed. Full Debug/Release compilation and byte-for-byte BPS verification run in GitHub Actions; manual emulator playtesting remains outstanding.

### Build variants
- All gameplay, clock, wardrobe and interface changes are shared by Release and Debug; there are no variant-specific differences in this version. Native developer conveniences remain Debug-only.

## [0.0.30] - 2026-10-10

### Added
- Dynamic Kanto outdoor weather using the existing 20-minute playtime forecast clock and native rain, storm, fog and snow transitions. Inland, coast and upland profiles vary by active season; morning/night have more fog. Coastal Kanto never receives random snow.

### Fixed
- Hoenn and Kanto grass, long-grass and ordinary outdoor plain battle backgrounds now follow the visible overworld season, including intro foliage and background restoration after move animations. Autumn uses amber foliage and winter uses frosted tones.
- Kanto overworld grass and trees now receive seasonal colors in their native FRLG palette slot zero. Day/night rebuilds retain the seasonal treatment; Hoenn's slot zero, transparent colors, blue water, character and UI palettes remain protected.

### Compatibility and validation
- Reuses existing saved season/weather state and native battle environments; no save layout, battle terrain, move effects or progression changes. Caves, water, sand, special backgrounds, facilities, linked/recorded and legendary battles retain native art. Explicit story weather and indoor maps remain protected.
- Actual-C checks cover all seasonal forecast weights, Kanto route coverage, weather transition guards, battle palette loading/reloading, special exclusions and Kanto slot-zero/day-night rebuilding. Native-art battle preview inspected; manual emulator testing remains outstanding. Debug/Release builds and verified BPS publishing use the established workflow.

### Build variants
- Shared weather, foliage and battle-scene changes in Release and Debug. No variant-specific gameplay differences; Debug retains developer conveniences.

## [0.0.29] - 2026-10-10

### Added
- ADVENTURE LOG in the pause menu: a cozy cream-and-lavender notebook with older/newer pages, All/Day/Story filters, played-day browsing, dates, locations, story notes, cumulative play time and one recent caught Pokemon with its level per entry.
- Automatically records key Hoenn milestones and the existing Kanto/Wing Survey story. Future Kanto victory records use the same modular registry. Captures and repeated save checkpoints refresh a field note between milestones; the latest 32 notes are retained.
- DAY counter above the clock/weather/season rows: counts dates actually played, including across sessions and midnight; skipped dates add nothing. Four hours on one date plus three on a later date remain seven play hours and two played days. Invalid RTC pauses counting; backward clock changes do not duplicate days.
- Scrollable pause menu with directional hints, retaining existing actions without extending beyond the screen. The notebook closes back to the pause menu; Continue has no forced replay scene.

### Compatibility and validation
- Existing saves begin a new Day 1 notebook with their known progress; historical dates/catches are not invented. Original SaveBlock1/2 and prior SaveBlock3 fields/IDs retain their offsets. The checked, versioned extension fits the native partial-save sector boundary; a bad extension resets only the log.
- Actual-C host checks cover persistence/migration, played dates, story hooks, catches, retention, filters, notebook lifecycle/font/pixel bounds, menu scrolling and the expanded clock panel. Native-font static preview inspected; manual emulator testing remains outstanding.
- Debug/Release compilation and verified BPS publishing use the established release workflow.

### Build variants
- Shared Adventure Log, day counter and gameplay in Release and Debug. No variant-specific gameplay differences; Debug retains developer conveniences.

## [0.0.28.1] - 2026-10-10

### Added
- Wing Survey journal at Oak's field aide in Vermilion Fan Club: shows 0/2, 1/2 or 2/2 opening records, names the missing Leader and their city, and offers optional review of only the clues already collected.
- Completed reports remain reviewable; the aide distinguishes tentative bird/Mew evidence from confirmed sightings. First introductions and report filing still occur only once, including on existing saves.

### Compatibility and validation
- Reuses the existing Gym victory and survey flags; no new save fields, trainer slots, rewards or encounter changes. Declined/lost battles never count as records.
- Event-path checks cover all four progress states, reviewing/declining clues, repeat visits, existing report flags and loss/decline behavior. Debug/Release compile and verified BPS publishing use the established workflow.
- Shared content in Release and Debug; no variant-specific gameplay differences. Debug retains developer conveniences.

## [0.0.28] - 2026-10-10

### Added
- Postgame PokeNav map browsing: SELECT switches between Hoenn and Kanto after becoming Champion, from full or zoomed views. Native region graphics, region banner and cursor sections reload together; browsing cannot change location, show a false player marker, or enable cross-region Fly.
- Kanto road loop: Routes 6–8 and 16–18, Saffron and Celadon, five connecting gate ground floors and two gate upstairs maps, two city Centers and Vermilion Gym (18 new maps). Existing map IDs remain stable. Unbuilt destinations remain sealed and labeled.
- Native Kanto wild distributions on Routes 6–8, 11–19 (excluding unopened Route 10), adjusted to Lv. 47–54; four optional, one-time route trainers and two birdwatching NPCs at Lv. 53–59. Routes 16–18 support walking and ordinary Emerald bikes; no forced FRLG Cycling Road state.
- Working nurses in Lavender, Fuchsia, Saffron and Celadon Centers, using Emerald's existing healing routine.
- First two visiting Gym challenges: Lt. Surge (Standard Lv. 52–56 / Champion Lv. 72–76) and Koga (Standard Lv. 56–60 / Champion Lv. 76–80). A guide stops entrants and explains the per-Gym choice. Talk to the guide to change it before winning. Standard has four Pokemon; Champion has six with stronger training. Player levels are never rescaled.
- Each Leader can be defeated only once per save: either difficulty permanently completes both. Losses allow retry/reselection; declining the Leader's confirmation leaves the challenge available. Dedicated Kanto records do not change Hoenn badges. Surge's visiting arena opens its native electrical barrier; Koga retains the native invisible-wall layout.
- Original WING SURVEY opening: Oak's field aide at Vermilion Fan Club follows up Hoenn's resolved weather crisis, gathers Surge and Koga's reports in either order, and introduces the three birds and a possible Mew lead. This build ends after the first report; legendary encounters and the other six Gyms are future chapters.
- Detailed staged postgame design and implementation/save-state documentation in `docs/features/kanto-postgame.md`, with the eight-Leader plan, habitat expeditions, story beats, and a manual playtest checklist.

### Validation
- Script-path tests cover both difficulties, the shared permanent victory, loss/retry, decline, independent Gym records and either-order survey reporting. Map geometry, route encounters, trainer teams, native graphics, and map-switch task checks are included in project CI.
- Release completion requires the existing Debug/Release compile, independent vanilla SHA-1, and BPS reapplication/byte comparison workflow. Manual emulator traversal and battle balance remain playtest work; static layout inspection is not emulator validation.

### Build variants
- Shared gameplay, maps, story and map browsing are identical in Release and Debug. No variant-specific feature differences; Debug retains the expansion's development conveniences.

## [0.0.27] - 2026-10-09

### Added
- Unpopulated Kanto foundation: FireRed-native Routes 11–15, Lavender Town, Fuchsia City and Route 19, with 22 empty gate/town interiors. Geography, dimensions, route offsets and tileset assets come from the expansion's native FireRed data.
- Opened Vermilion's eastern road. Walk the connected Route 11–15 loop between Vermilion, Lavender and Fuchsia, then reach Route 19.
- Two-way Surf passage: northern Route 124 (x20–24, y1) to southern Route 19; return from Route 19 (x10–16, y56). Outbound travel requires Champion status and the retained Invite Ticket. Native Surf/badge requirements still apply. A fade separates incompatible regional tileset formats; the permanent ferry remains available.

### Scope and compatibility
- New maps contain no NPCs, trainers, item gifts, wild encounters or FireRed story scripts. Centers and Marts in these new areas are empty shells; Vermilion services remain available. Tower, Safari Zone, Diglett's Cave and roads beyond this foundation remain closed.
- Appended map/layout IDs; no save-layout changes or existing IDs renumbered. Regional blackout handling retains Vermilion in Kanto and restores Lilycove on Surf return.
- Release and Debug share these additions with no variant-specific gameplay differences; developer tools remain Debug-only.

## [0.0.26.1] - 2026-10-09

### Fixed and polished
- Vermilion's construction-site Machop now uses native species overworld graphics. Older residents use native Emerald sprites, fixing invisible legacy FRLG-only entries.
- Fan Club visitors stand on the floor beside the sofas; the Gym attendant stands outside the doorway instead of overlapping its artwork.
- Invite Ticket text fits Emerald's Bag description window and clearly explains return travel.
- Residents look around, with small bounded walking routes for selected town/facility visitors. Nurse, shop and link-service attendants retain their required facing; the docked ship remains stationary. Welcome actors face the arriving Champion during their scene.
- Lilycove's Kanto sailor now waits beside the main ferry attendant. The shareable beginner guide describes the new boarding location.

### Compatibility
- Release and Debug share all fixes with no variant-specific gameplay differences; developer tools remain Debug-only. Existing tickets, saves, map IDs, welcome progress and trainer victories are retained.

## [0.0.26] - 2026-10-09

### Added
- The first Kanto postgame chapter: Hoenn's Champion receives a League Invite Ticket from a representative at Lilycove Harbor. The nearby sailor offers permanent two-way passage to Vermilion Port; the ticket is retained and required on every crossing.
- Vermilion City and its permanently docked passenger ship, with original Kanto outdoor art/music, a modest one-time welcome from Fan Club members, new clean dialogue, three homes, a Fan Club, a fully functioning Pokémon Center/link floor and a postgame-stocked Mart.
- An optional Cooltrainer ALEX battle on the waterfront with six Kanto Pokémon at levels 60–64. Players can decline and return later; victory is saved using native trainer flags. Travel never requires winning.
- A dedicated Kanto heal/blackout destination and return-to-Hoenn respawn handling. Existing Hoenn transport/event-island scripts remain separate.
- A player/Debug tutorial with exact map, item and flag IDs, repeat-visit and battle reset instructions, and a manual emulator checklist. Expanded for beginner playtesters with emulator button explanations, a worked number-selector example, a complete ferry walkthrough, troubleshooting and bug-report guidance; advanced shortcuts are separate.

### Scope and compatibility
- This is the Vermilion arrival chapter, not the complete Kanto region. Roads to Routes 6/11 are visibly closed for storm repairs, and Lt. Surge is away assisting the crews. Later chapters can open these paths without transplanting FireRed's new-game story.
- Reuses the expansion's native FRLG tile/palette counts, attribute packing, water animations and selected door animations. Mapjson now separates build selection (`layout_version`) from optional `tileset_format`; existing layouts retain their previous behavior.
- Appended map/layout/item/heal/trainer IDs; no SaveBlock enlargement or renumbering of existing IDs. Existing Champion saves can obtain the invitation immediately.
- Release and Debug share all new content with no variant-specific gameplay differences. Developer tools and title Quickstart remain Debug-only.

## [0.0.25.1] - 2026-10-09

### Fixed
- Removed SUNNY CLOUDS from dynamic regional forecasts. Emerald's cloud sprites use fixed Route 120 reflection coordinates and could show through elevated tiles/doorways on unrelated maps. Former cloudy forecast periods now use clear weather, with rain/thunder/fog/snow weights and timing unchanged.
- Existing saved cloud forecasts resolve through the native map-load or weather-transition cleanup; no new save or clock reset is required. Native effects on protected maps remain intact.

### Compatibility and validation
- Exhausted all forecast rolls across seasons, times, configured climate profiles and ordinary weather inputs; checked old-cloud cleanup and native protected-map behavior.
- Release and Debug share this fix with no variant-specific differences; developer tools remain Debug-only. No save-layout changes.

## [0.0.25] - 2026-10-09

### Added
- A COSTUMES wardrobe category with NONE, TEAM MAGMA and TEAM AQUA for both genders. Uses the exact native grunt walking sprites and front portraits, including Magma hoods, Aqua bandanas, uniform details and team symbols.
- Matching compiled costume action poses for running, bikes, Surf, field moves, fishing/watering, plus all four native battle throw frames and the local Trainer Card. Costume art is independent from NPC grunt graphics; the covered Dive suit stays native.
- Saved costume selection in unused var 0x40A8. The selected skin tone is retained; normal outfit/scarf/jacket choices remain stored when a costume is worn. Accessory rows show FIXED for complete uniforms. Selecting a normal outfit exits costume mode; NONE restores stored clothes.

### Fixed
- Male Sport shorts now retain fabric above the knees with two light hem stripes; overworld shorts also have a light hem instead of a large skin-colored trouser section.

### Compatibility and validation
- No save-layout changes or existing appearance/decoration/species ID renumbering. New Game resets costumes; invalid saved values safely use NONE. Apply/Cancel stage costumes alongside clothes.
- Added native-asset fidelity, action frame dimensions, skin/held-object protection, costume save/palette/graphics selection and wardrobe navigation regressions.
- Release and Debug share these changes with no variant-specific differences; developer tools remain Debug-only.

## [0.0.24] - 2026-10-08

### Updated
- Integrated the two upstream expansion updates through commit 7b95be15: held-item restoration after wild battles/captures, and missing/corrected overworld sprites and palettes for Pokémon forms. Retained Legends gameplay, follower controls, custom species, appearance and weather systems.
- Replaced the tall custom wardrobe with Emerald’s native closed storage-box artwork beneath each bedroom’s bed. The secret-base WARDROBE now occupies one tile; its existing decoration ID and purchase/inventory state are retained.
- Interacting with your wardrobe now opens customization directly. Removed the repeated shop advertisement and Yes/No prompt.
- Compiled pose-local scarf tails and jacket outlines/hem layers for both genders, including overworld states, battle portraits/throws and Trainer Cards. Faces, hands, held objects and native frame sizes are preserved.

### Compatibility and validation
- No save-layout or accessory encoding changes. Added focused tests of upstream held-item restoration, captured items, bag routing, berries and partner slots; retained all Legends regressions and layered-asset validation.
- Release and Debug share all changes with no variant-specific differences; native developer tools remain Debug-only.

## [0.0.23] - 2026-10-08

### Added
- A wooden wardrobe in each Littleroot bedroom, usable only in the player’s own home. Browse all five outfits, five additional scarf colors (Crimson, Ocean, Emerald, Lavender, Cream) or no added scarf, and an optional navy jacket with short sleeves.
- A dedicated native wardrobe screen with a live trainer portrait, Apply and Cancel. Scarf and jacket selections combine independently with every outfit; skin tone is retained.
- A placeable 1x2 WARDROBE ornament sold for ₽3,000 at Route 104’s Pretty Petal Flower Shop. Uses the native decoration inventory, placement/removal and save system; customization is available only in your own secret base.
- Matching accessory art for both genders across walking/running, bikes, Surf, field moves, fishing/watering, battle front/back throw frames and the local Trainer Card. The diving suit remains covered; rivals/NPCs and remote link art remain native.

### Compatibility and validation
- Accessory choices use unused var 0x40A1 without changing save layouts. Legacy saves retain native skin colors when editing clothes; new games start with no added accessories.
- Added pose-aligned native 4bpp asset generation, separate scarf coloring, safe cabinet tile reuse, actual UI access/navigation/apply/cancel tests, and all-combination appearance/asset regressions.
- Documented wardrobe controls, shopping/placement, save migration and emulator QA. Release and Debug share these changes with no variant-specific differences; developer tools remain disabled in Release and enabled in Debug.

## [0.0.22] - 2026-10-08

### Added
- Regional dynamic forecasts in most ordinary Hoenn towns and routes: rain, clouds and occasional thunderstorms; wetter conditions around Fortree and Routes 119–121.
- Fog in rainforest/upland areas, more likely in autumn and during native morning/night hours; winter flurries on non-volcanic upland Routes 114–116. Tropical coasts and lowlands never receive random snow.
- A saved 20-minute playtime forecast period, with smooth native transitions while outdoors. Local seeded randomness avoids consuming battle RNG or rerolling every time a building is entered.
- A moon and subtle star twinkle for clear nights in the pause weather indicator, using the existing game day/night clock. Drought retains its sun indicator.

### Compatibility and validation
- Preserved indoor, cave, underwater, desert, volcanic, special-map and scripted story weather; weather transitions wait for dialogue, fades and existing effects to finish.
- Existing saves initialize the weather timer from recorded playtime. One unused var and flag are reserved without changing save layouts.
- Documented climates, forecast weights and emulator QA; added actual-module checks for probabilities, exclusions, timer migration/rollover and transition guards.
- Release and Debug share all weather changes with no variant-specific differences; developer tools remain disabled in Release and enabled in Debug.

## [0.0.21] - 2026-10-08

### Changed
- Halved Da Bug’s follower art inside its existing 32x32 frames, keeping it centered and grounded; visible silhouettes now fit within 14x14 pixels.
- Reduced its shared PC/party icon to roughly 20x16 pixels, comparable to native small Pokémon icons, with padding around every frame.
- Reduced the front sprite used by the large PC/Pokédex preview from 60x48 to 48x40 pixels; preserved the normal/shiny colors and eye-only glimmer frames.
- Lowered Da Bug’s battle back sprite by 8 pixels using its native species Y offset.
- Updated sprite bounds checks and art documentation. The existing PC gift, save compatibility, moves, cry and shiny roll are unchanged.
- Release and Debug share these adjustments with no variant-specific differences; developer tools remain disabled in Release and enabled in Debug.

## [0.0.20] - 2026-10-08

### Added
- Added Da Bug, the original single-stage Bug/Grass Leafhopper Pokémon: 0.3 m, 1.2 kg, with the approved green leaf-wing design, red eyes and amber-wing/teal-eye shiny.
- Native front/back battle art, PC icon, footprint and walking follower sprites; a gentle swaying front animation with localized red eye glimmers and a short, original two-note chirp.
- One level-5 Da Bug is placed in Box 1 on New Game, with Tackle, Leer, Mean Look and Absorb. Existing saves receive it in their first free PC box slot on continue. Full storage retries on a later continue without overwriting Pokémon.
- This gift alone has exactly a 1-in-10 shiny roll, independent of Options/Charm. A permanent receipt flag prevents replacement or rerolls after withdrawal, release or later continues. No wild encounters or Random starter inclusion.
- A relevant level-up progression introduces Bug Bite, Leech Seed, Mega Drain, Struggle Bug, Protect, Giga Drain, Agility, Leech Life, Synthesis, Energy Ball and Bug Buzz. No evolution.
- Preserved the approved Pokédex entry verbatim: “It sways in the breeze to mimic a fallen leaf. If its disguise fails, it flashes its red eyes and springs away.”

### Compatibility and validation
- Added custom species/National Dex entries without renumbering existing Pokémon. Dex save bitfields remain 129 bytes; the gift uses an unused permanent flag rather than enlarging save blocks.
- Added actual-module regressions for every shiny outcome, both ordinary shiny states, level/moves, duplicate prevention, occupied/full storage, retry and Pokédex registration; asset/cry/dex integration checks.
- Documented species data, learnset, gift migration and emulator QA in docs/features/da-bug.md.
- Release and Debug share the gameplay changes. Debug’s sprite visualizer adds a labeled Da Bug sway/eye-glimmer animation; developer tools remain disabled in Release.
- Both variants compiled successfully; both BPS patches passed byte-for-byte reapplication verification against the independently built, SHA-1-verified clean Emerald reference.

## [0.0.19] - 2026-10-08

### Added
- Added Lavender for both genders: a lavender/plum outfit with cream scarf details, bare hands, matching overworld poses, intro/naming previews, battle front/back art and Trainer Card.
- Added Adventure 3/3 Options with STARTERS: Gen 1–9, Special (Happiny/Wattrel/Mankey), and Random. Gen 3 remains the default; title Options carry into New Game.
- Random selects three distinct, enabled, unevolved canonical Pokédex species with evolutions, including babies. The lineup rolls once at the rescue bag and remains saved/stable.
- Generation rivals use their corresponding counter starter and native level evolutions. Special/Random rivals use Unovan Zorua, evolving to Zoroark at level 30. Both genders and all 30 native starter-dependent teams are covered.

### Compatibility and validation
- Lock the rescue lineup separately from future-game preferences. Existing saves retain Gen 3 rival lineage; default Gen 3 preserves exact Emerald teams. No save-block or Options-window enlargement.
- Keep starter levels, Stunky rescue, other rival team members and progression scripts. The Petalburg type tutorial now uses general examples rather than calling a Hoenn species your own starter.
- Added actual-module starter/rival tests using native evolution metadata; checked stable Random selection and all 30 teams in 11 modes. Extended title staging and three-page navigation tests.
- Appearance checks cover all 50 gender/skin/outfit combinations and 736 custom poses.
- Release and Debug share these changes with no variant-specific differences. Developer tools remain disabled in Release and enabled in Debug.

## [0.0.18] - 2026-10-08

### Changed
- Replaced the bottom CANCEL row on both Options pages with NEXT PAGE. Press A there to cycle pages; L/R remain page shortcuts.
- Added a permanent A: NEXT / B: SAVE hint on the bottom row, independent of the version label. B saves all settings and exits from any row.
- Kept the original seven-row windows and VRAM allocation. Page changes preserve pending settings, and L/R retains priority with L=A controls.
- Release and Debug share these changes with no variant-specific differences. Developer tools remain disabled in Release and enabled in Debug.

### Validation
- Added an actual-function navigation regression covering A/L/R paging, pending settings, row wrap and B save/exit on every row in both pages.

## [0.0.17] - 2026-10-08

### Changed
- Stunky replaces Zigzagoon in the opening Route 101 professor rescue, both in the level-2 battle and as the Pokémon chasing the professor. Uses the expansion’s native Stunky overworld sprites and palette.
- The rescue movement, starter choices and story progression are unchanged; existing saves remain compatible.
- Release and Debug share this change with no variant-specific differences. Developer tools remain disabled in Release and enabled in Debug.

## [0.0.16] - 2026-10-08

### Fixed
- The player naming-screen icon now uses the selected outfit and skin tone.
- Clear the entire intro text window so longer appearance prompts leave no stray letters/arrows. Active text printers restore their own glyph colors after menu text.
- Grass rustle/jump/short/long/shaking animations use a separate seasonal vegetation palette; water, ash, NPCs and player palettes retain their own colors.
- Refined custom front/back outfit panels across all four battle animation poses, kept bags distinct from shirts, protected held Poké Balls and corrected May’s colored mouth detail.

### Added
- Added a fourth, yellow outfit for both genders. All custom outfits use bare hands; the default Emerald outfit retains its original gloves.
- Walking through standard winter grass clears the snow-covered tuft until a full map reload, inspired by ash grass. This is a temporary visual change: encounters, collision and terrain behavior are preserved. Tree-edge, long-grass and volcanic-ash tiles retain native terrain rendering.

### Validation
- Expanded actual-module appearance checks to all 40 combinations and asset coverage to all 552 custom poses.
- Added regressions for printer color isolation, seasonal grass palettes and snow clearing/reset/bounds.
- Release and Debug share these changes; developer tools remain disabled in Release and enabled in Debug.

## [0.0.15] - 2026-10-08

### Added
- Added skin tone and outfit selection immediately after gender in Birch’s New Game introduction.
- Five realistic skin tones (Fair, Light, Medium, Brown, Deep) and three clothing designs per gender: Emerald, Trail (jacket/trousers), Sport (striped shirt/shorts).
- Added a live 64px sprite preview in a bordered popup at the bottom right, above the dialogue box. B returns to the previous choice.
- Saved appearance applies to walking/running, bikes, Surf, field moves, fishing/watering, local battle front/back poses, Safari scenes and the local Trainer Card; Dive retains the native diving-suit silhouette.
- Existing saves and Debug Quickstart keep the original Emerald appearance. Player colors and graphics use separate IDs/palettes so NPCs and rivals retain their native appearance.
- Documented appearance data, native pose reuse, asset authoring and emulator QA. Remote/link appearance synchronization is not added.

### Validation
- Added exhaustive actual-module host regressions for all 30 gender/skin/outfit combinations, intro-to-save handoff, legacy saves, graphics states and NPC isolation.
- Added generated-art reproducibility, face/held-ball protection, silhouette and LZ77 roundtrip checks across all 368 custom outfit poses.
- No Release-only gameplay differences; developer tools remain disabled.

## [0.0.14.1] - 2026-10-08

### Changed
- Colored the pause-panel weather icons using Emerald’s existing text palette: warm sunshine/sand, blue rain/water and pale blue snow.
- Added gentle two-frame weather animation twice per second: sun shimmer, falling rain/ash, drifting snow/fog/sand, a softly dimming lightning bolt and water shimmer. Indoor and cloud icons stay still.
- Redrew the clock hands as a clear L shape, removing the previous U-like appearance.
- Animation updates only the weather icon pixels, reads no RTC data and uses no additional sprite or palette slots. Menu closure retains the existing cleanup.

### Validation
- Extended the actual-module host C regressions for both animation frames, native colors, pixel bounds and RTC read limits.
- No Release-only visual/gameplay differences; developer tools remain disabled.

## [0.0.14] - 2026-10-08

### Added
- Added a bottom-left Start-menu panel using Emerald’s native border, small text and pixel clock/weather icons.
- Shows the local RTC clock in 12-hour format, live weather and the active season. Refreshes once per second and redraws only when values change; unavailable RTC displays --:--.
- Indoors/caves show a shelter icon; underwater shows a water icon. Opening the menu does not advance the active season or change weather.
- Handles save/retire dialogs, submenu transitions, returning to the menu and allocation failure without leaking a window.

### Validation
- Added host C regressions for panel lifecycle, time rollover, invalid RTC, weather categories, season display and tile/pixel bounds. Both native ROM builds and BPS round-trip verification run in Actions; emulator visual QA remains separate.
- No Release-only gameplay differences; developer tools remain disabled.

## [0.0.13.1] - 2026-10-08

### Shared changes
- Changed the New Game / Continue / Options main menu backdrop to a soft light lavender, preserving the existing menu cards, text, borders and fades.

### Release-specific
- No Release-only visual/gameplay divergence; developer tools remain disabled.

## [0.0.13] - 2026-10-08

### Shared changes
- Enabled the expansion’s native overworld Pokémon follower system with a saved FOLLOWER ON/OFF setting on Legends Options (default ON for new and existing saves).
- The first conscious non-egg Pokémon in party order follows the player, using native walking, Poké Ball, graphics and interaction behavior. Reorder the party to change the follower.
- Reused native hiding rules for travel/forced movement, oversized indoor sprites, temporary script hiding and NPC companions; missing overworld graphics keep the configured native substitute fallback.
- Leaving Options applies the follower choice through the normal faded field reload. The selection persists across save/reload and title-screen New Game setup.
- Used an unused permanent disable flag without changing the SaveBlock layout; kept both Options pages within seven rows and the existing VRAM allocation.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.12.1] - 2026-10-08

### Shared changes
- Preserved title-screen Legends Options choices when starting New Game: season mode, selected gameplay season, EXP Share and shiny rate now survive the new save reset.
- Initialized the active season before the opening maps load; 7H PLAY and manual season selection work independently of the bedroom clock event.
- New saves start with a fresh seven-hour timer for the selected gameplay season; previous save progress and story flags are not carried over.
- Cleared temporary title choices after applying them and on fresh title entry, preserving standard defaults when New Game is started without title-screen Options.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.12] - 2026-10-08

### Shared changes
- Changed gameplay seasons to seven recorded play hours each (28 hours for a full Spring → Summer → Autumn → Winter cycle).
- Held seasonal colors and ambient weather until a faded map transition, such as entering/leaving a building, a faded warp, or save reload; seamless route crossings and menu/battle returns preserve the active environment.
- Added SET SEASON in gameplay mode. Left/Right selects the next season to apply and restarts its seven-hour timer; REAL TIME remains calendar-controlled.
- CURRENT now shows the active environment, including while a new season is pending.
- Fixed corrupted season labels by providing native color prefixes, checking those prefixes before recoloring, and clearing old choice text before redraw.
- Preserved seasonal progression in existing saves without changing the SaveBlock layout; volcanic exclusions and special weather remain intact.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.11] - 2026-10-08

### Shared changes
- Added REAL TIME / 28H PLAY seasonal modes to Legends Options, plus a CURRENT season preview.
- Real time follows Northern Hemisphere calendar seasons using the native RTC; the gameplay mode cycles Spring, Summer, Autumn and Winter every 28 saved gameplay hours.
- Added seasonal outdoor vegetation colors and region-aware ambient rain, fog, thunderstorms and winter snowfall using native weather effects.
- Preserved Mt. Chimney, Jagged Pass, Fiery Path, Lavaridge, Fallarbor, Routes 112/113, and Route 111's desert corridor; oceans and mild island towns do not receive seasonal snowfall.
- Preserved indoor/underground/underwater maps, special weather, and Groudon/Kyogre story effects.
- Reused unused permanent save variables, migrated older saves from recorded playtime, and kept seasonal time running beyond the native 999-hour playtime display limit.
- Refreshed seasons safely on return to the field and during outdoor play, composing foliage palettes with existing day/night and weather processing.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.10] - 2026-10-07

### Shared changes
- Added a persistent SHINY RATE setting to the Legends Options page (Left/Right: 1/8192, 1/5680, 1/1226; default 1/8192).
- Selected odds govern the base per-roll shiny chance for newly generated wild Pokémon, including fishing and DexNav encounters.
- Kept bonus rolls from Shiny Charm, chain fishing and DexNav; eggs, gifts, special/scripted Pokémon and previously caught Pokémon are unchanged.
- Used an existing unused permanent event variable, so earlier saves retain 1/8192 and a new choice survives save/load.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.9] - 2026-10-07

### Shared changes
- Enabled DexNav at Birch's first Pokédex gift and on existing saves that already have the Pokédex.
- Added the physical Gen 6-style Exp. Share Key Item at new-game start and restored it for eligible existing saves.
- The Exp. Share item and Legends Options share the same persistent ON/OFF flag.
- Rustboro's Lucky Egg and the Champion Rare Candy reward are unchanged.

### Release-specific
- No Release-only gameplay divergence; developer tools are disabled.

## [0.0.8.1] - 2026-10-07

### Shared changes
- Fixed browser patcher handling of rapid ROM changes, discarding obsolete validation and download results.
- Ensured version text cannot overlap the Options header's L/R hint.
- Added automated BPS parser/checksum tests and a manual emulator regression checklist.
- Core Legends gameplay and content remain unchanged from 0.0.8.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.8] - 2026-10-07

### Shared changes
- Reworked Options into two pages: General and Legends.
- Use L/R in Options to switch pages; the current page is shown in the header.
- Moved EXP SHARE to the Legends page to reserve clean space for future Legends-specific settings.
- Restored the original safe Options window dimensions, fixing corrupted/repeating frame graphics and the clipped CANCEL row.

### Release-specific
- No Release-only gameplay divergence in this version.

## [0.0.7] - 2026-10-07

### Shared changes
- Professor Birch now enables the National Pokédex during the initial Pokédex handoff.
- Birch's post-Elite Four National Dex upgrade reward is now 25 Rare Candies.
- If the Bag cannot hold all 25, the reward is sent to the PC; if neither has room, Birch keeps the reward pending for a later conversation.
- Existing postgame saves can claim the new Rare Candy reward once without disrupting later Johto starter progression.

### Release-specific
- No Release-only gameplay divergence in this version.

## [0.0.6] - 2026-10-07

### Shared changes
- Mr. Stone now gives a Lucky Egg after the Steven Letter delivery instead of the redundant held Exp. Share.
- His reward dialogue now explains the Lucky Egg's EXP bonus.
- Lucky Egg's native multiplier behavior is unchanged; only the Rustboro reward source changed.

### Release-specific
- No Release-only gameplay divergence in this version.

## [0.0.5] - 2026-10-07

### Shared changes
- Added default-on Gen 6-style party EXP Share from the beginning of the game.
- Added an `EXP SHARE` ON/OFF setting to Options.
- Added one-time migration for pre-0.0.5 saves so the new setting starts enabled.
- Reused the expansion-native EXP pipeline so existing multipliers and level-cap behavior remain intact.

### Release-specific
- No Release-only gameplay divergence in this version.
- Release includes the full EXP Share setting with developer/debug entry points disabled.

## [0.0.4.2] - 2026-10-07

### Shared changes
- Corrected homepage wording so the field-move feature is accurately attributed to 0.0.4.
- Added a direct Release changelog link beside the Release download.
- Tightened changelog/version consistency checks.

### Release-specific
- No Release-only gameplay or content changes in this micro-build.

## [0.0.4.1] - 2026-10-07

### Shared changes
- Corrected mislabeled 0.0.3 headings on the website changelog.
- Synchronized current version labels and download targets to 0.0.4.1.

### Release-specific
- No Release-only gameplay or content changes in this micro-build.

## [0.0.4] - 2026-10-07

### Shared changes
- Cut, Flash, Rock Smash, Strength, Surf, Fly, Dive, and Waterfall are now badge-earned overworld utilities and no longer require a Pokémon to know the HM.
- Added a compact `FIELD` submenu for manually invoking unlocked utilities.
- Preserved Emerald's original badge order, map restrictions, follower restrictions, and Regi puzzle hooks.
- Removed Pokémon-specific HM-use text and suppressed arbitrary Pokémon field-move banners.
- Kept non-HM field moves such as Dig, Teleport, and Sweet Scent move-dependent.

### Release-specific
- No Release-only gameplay divergence in this version.
- Release contains the full badge-field-move system with developer/debug entry points still disabled.

## [0.0.3] - 2026-10-07

### Shared changes
- Added dedicated Release and Debug changelog tracking.
- Added a website changelog page with tabs for switching between build histories.
- Improved version/changelog consistency checks.

### Release-specific
- No Release-only gameplay or content changes in this version.
- Release remains the recommended casual-player build with developer/debug entry points disabled.

## [0.0.2] - 2026-10-07

### Shared changes
- Introduced separate Release and Debug downloads built from the same Legends source.
- Added browser patcher support for both build variants.
- Added automated byte-for-byte verification for both published patches.

### Release-specific
- Release is built using the expansion's native release configuration.
- Overworld debug menu, battle debug menu, Pokémon sprite visualizer, and title-screen Quickstart are disabled.
- All Pokémon Emerald: Legends gameplay/content changes remain present.

## [0.0.1] - 2026-10-07

### Pre-split baseline
- Added the `LEGENDS` title-screen subtitle.
- Added the initial in-game Legends version label.
- Added the project website, browser patcher, reproducible patch workflow, roadmap, and initial feature design documentation.
- Formal Release/Debug variants had not yet been separated.
