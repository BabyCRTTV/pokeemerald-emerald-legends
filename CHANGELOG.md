# Changelog

All notable Pokémon Emerald: Legends project changes are documented here.

For build-specific player views, see [CHANGELOG-RELEASE.md](CHANGELOG-RELEASE.md) and [CHANGELOG-DEBUG.md](CHANGELOG-DEBUG.md). The canonical history below records the project as a whole.

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
- Release and Debug share the appearance feature; no variant-specific gameplay differences.

## [0.0.14.1] - 2026-10-08

### Changed
- Colored the pause-panel weather icons using Emerald’s existing text palette: warm sunshine/sand, blue rain/water and pale blue snow.
- Added gentle two-frame weather animation twice per second: sun shimmer, falling rain/ash, drifting snow/fog/sand, a softly dimming lightning bolt and water shimmer. Indoor and cloud icons stay still.
- Redrew the clock hands as a clear L shape, removing the previous U-like appearance.
- Animation updates only the weather icon pixels, reads no RTC data and uses no additional sprite or palette slots. Menu closure retains the existing cleanup.

### Validation
- Extended the actual-module host C regressions for both animation frames, native colors, pixel bounds and RTC read limits.
- Release and Debug share the visual changes; no variant-specific gameplay differences.

## [0.0.14] - 2026-10-08

### Added
- Added a bottom-left Start-menu panel using Emerald’s native border, small text and pixel clock/weather icons.
- Shows the local RTC clock in 12-hour format, live weather and the active season. Refreshes once per second and redraws only when values change; unavailable RTC displays --:--.
- Indoors/caves show a shelter icon; underwater shows a water icon. Opening the menu does not advance the active season or change weather.
- Handles save/retire dialogs, submenu transitions, returning to the menu and allocation failure without leaking a window.

### Validation
- Added host C regressions for panel lifecycle, time rollover, invalid RTC, weather categories, season display and tile/pixel bounds. Both native ROM builds and BPS round-trip verification run in Actions; emulator visual QA remains separate.
- Release and Debug share the panel; no variant-specific gameplay differences.

## [0.0.13.1] - 2026-10-08

### Changed
- Changed the New Game / Continue / Options main menu backdrop to a soft light lavender, preserving the existing menu cards, text, borders and fades.

- Release and Debug share the same visual change; no gameplay changes.

## [0.0.13] - 2026-10-08

### Added
- Enabled the expansion’s native overworld Pokémon follower system with a saved FOLLOWER ON/OFF setting on Legends Options (default ON for new and existing saves).
- The first conscious non-egg Pokémon in party order follows the player, using native walking, Poké Ball, graphics and interaction behavior. Reorder the party to change the follower.
- Reused native hiding rules for travel/forced movement, oversized indoor sprites, temporary script hiding and NPC companions; missing overworld graphics keep the configured native substitute fallback.
- Leaving Options applies the follower choice through the normal faded field reload. The selection persists across save/reload and title-screen New Game setup.
- Used an unused permanent disable flag without changing the SaveBlock layout; kept both Options pages within seven rows and the existing VRAM allocation.

### Validation
- Added host C regressions for native party selection, follower spawn/removal, script/NPC hiding, indoor limits and full object slots. Extended saved-setting and title-screen New Game regressions for the follower toggle. Emulator visual/playtesting remains separate.
- Updated the roadmap’s gameplay-season timing to the current seven-hour cycle.
- No variant-specific gameplay changes; Release disables developer tools and Debug retains them.

## [0.0.12.1] - 2026-10-08

### Fixed
- Preserved title-screen Legends Options choices when starting New Game: season mode, selected gameplay season, EXP Share and shiny rate now survive the new save reset.
- Initialized the active season before the opening maps load; 7H PLAY and manual season selection work independently of the bedroom clock event.
- New saves start with a fresh seven-hour timer for the selected gameplay season; previous save progress and story flags are not carried over.
- Cleared temporary title choices after applying them and on fresh title entry, preserving standard defaults when New Game is started without title-screen Options.

### Validation
- Added host C regressions for title choices across save reset, pre-clock season initialization, replacement/consumption of staged choices, default new saves and native lifecycle hook ordering. Emulator visual/playtesting remains separate.
- No variant-specific gameplay changes; Release disables developer tools and Debug retains them.

## [0.0.12] - 2026-10-08

### Changed
- Changed gameplay seasons to seven recorded play hours each (28 hours for a full Spring → Summer → Autumn → Winter cycle).
- Held seasonal colors and ambient weather until a faded map transition, such as entering/leaving a building, a faded warp, or save reload; seamless route crossings and menu/battle returns preserve the active environment.
- Added SET SEASON in gameplay mode. Left/Right selects the next season to apply and restarts its seven-hour timer; REAL TIME remains calendar-controlled.
- CURRENT now shows the active environment, including while a new season is pending.
- Fixed corrupted season labels by providing native color prefixes, checking those prefixes before recoloring, and clearing old choice text before redraw.
- Preserved seasonal progression in existing saves without changing the SaveBlock layout; volcanic exclusions and special weather remain intact.

### Validation
- Added host regressions for seven-hour boundaries, deferred transitions, old-cycle normalization, manual season selection and native Options text rendering. Emulator visual/playtesting remains separate.
- No variant-specific gameplay changes; Release disables developer tools and Debug retains them.

## [0.0.11] - 2026-10-08

### Added
- Added REAL TIME / 28H PLAY seasonal modes to Legends Options, plus a CURRENT season preview.
- Real time follows Northern Hemisphere calendar seasons using the native RTC; the gameplay mode cycles Spring, Summer, Autumn and Winter every 28 saved gameplay hours.
- Added seasonal outdoor vegetation colors and region-aware ambient rain, fog, thunderstorms and winter snowfall using native weather effects.
- Preserved Mt. Chimney, Jagged Pass, Fiery Path, Lavaridge, Fallarbor, Routes 112/113, and Route 111's desert corridor; oceans and mild island towns do not receive seasonal snowfall.
- Preserved indoor/underground/underwater maps, special weather, and Groudon/Kyogre story effects.
- Reused unused permanent save variables, migrated older saves from recorded playtime, and kept seasonal time running beyond the native 999-hour playtime display limit.
- Refreshed seasons safely on return to the field and during outdoor play, composing foliage palettes with existing day/night and weather processing.

### Technical
- Added host C regression coverage for calendar/timing boundaries, save migration, weather exclusions, palette bounds and safe refresh; emulator visual/play testing remains separate.

## [0.0.10] - 2026-10-07

### Added
- Added a persistent SHINY RATE setting to the Legends Options page (Left/Right: 1/8192, 1/5680, 1/1226; default 1/8192).
- Selected odds govern the base per-roll shiny chance for newly generated wild Pokémon, including fishing and DexNav encounters.
- Kept bonus rolls from Shiny Charm, chain fishing and DexNav; eggs, gifts, special/scripted Pokémon and previously caught Pokémon are unchanged.
- Used an existing unused permanent event variable, so earlier saves retain 1/8192 and a new choice survives save/load.

### Technical
- Used unbiased 16-bit rejection sampling so the three selected base probabilities are mathematically exact before modifier rerolls.
- Reused the existing paged Options UI without increasing window tile usage or the seven-row General page.
- Added static project checks for the new save variable and wild-only shiny calculation; emulator playtesting remains separate.

## [0.0.9] - 2026-10-07

### Added
- Enabled expansion DexNav using dedicated persistent search flags and variables. It appears in the Start menu after Birch's first Pokédex gift, including detector mode.
- Existing saves that already received the Pokédex automatically unlock DexNav when continued.
- Added the Gen 6-style physical Exp. Share to Key Items in new games; existing saves receive one if missing.

### Fixed
- Using the Exp. Share Key Item and changing Legends Options now affect the same persistent ON/OFF flag.
- Existing-save item restoration avoids the temporary Battle Pyramid bag; if the Key Items pocket is full it retries on a future ordinary continue.

### Quality
- Expanded repository checks to verify DexNav configuration and Exp. Share item/unlock migration.
- Release and Debug retain identical gameplay changes and separate changelogs.

## [0.0.8.1] - 2026-10-07

### Fixed
- Browser patcher now ignores stale checksum results when the selected ROM changes during verification.
- Cancels in-flight local patching when the selected ROM changes, avoiding accidental output from an older selection.
- Prevents longer version text from overlapping the Options page-navigation hint.

### Quality and maintenance
- Reviewed the Options, EXP Share settings, HM field utilities, Birch Champion reward, and Rustboro Lucky Egg paths at source level.
- Added automated BPS decoder tests for copy behavior, integrity checks, and rapid ROM selection changes.
- Documented verified automated coverage and remaining manual emulator scenarios in docs/QA.md.
- No gameplay or content changes from v0.0.8; Release and Debug retain identical Legends mechanics.

## [0.0.8] - 2026-10-07

### Added
- Added a reusable paged Options framework with separate **General** and **Legends** pages.
- Added L/R shoulder-button page switching with the active page shown in the Options header.
- Moved the Legends EXP Share toggle onto the Legends page, leaving room for additional project-specific settings later.

### Fixed
- Restored the Options menu's safe upstream window dimensions so its text tile buffer ends before the window-frame graphics begin.
- Fixed the corrupted/repeating Options window borders seen in mGBA and Pizza Boy after the 0.0.5 single-page layout expansion.
- Restored full visibility of the CANCEL row instead of allowing it to clip below the Options window.

### Changed
- The General page now contains Text Speed, Battle Scene, Battle Style, Sound, Button Mode, Frame, and Cancel.
- Each page uses the original 16-pixel row spacing; new Legends settings can be added by extending the page table rather than enlarging the window.

## [0.0.7] - 2026-10-07

### Added
- Professor Birch's initial Pokédex handoff now enables National Mode immediately.
- Birch now gives 25 Rare Candies after the player becomes Champion, replacing the old post-Elite Four National Dex upgrade reward.

### Changed
- The Champion reward first tries the Bag and falls back to the PC if the Bag cannot hold all 25 Rare Candies.
- Added a one-time reward flag so existing postgame saves that already passed the old National Dex scene can still claim the 25 Rare Candies from Birch.
- Preserved the existing postgame state progression, including the later Hoenn Pokédex completion / Johto starter reward.

## [0.0.6] - 2026-10-07

### Changed
- Replaced Mr. Stone's post-Steven-Letter Rustboro reward from the now-redundant held Exp. Share to a Lucky Egg.
- Updated Mr. Stone's reward explanation to describe the Lucky Egg's held-item EXP bonus.
- Preserved the expansion-native Lucky Egg multiplier behavior; this release changes acquisition, not the multiplier formula.
- Retained Emerald's existing `FLAG_RECEIVED_EXP_SHARE` as the one-time Devon reward completion state for save compatibility.

## [0.0.5] - 2026-10-07

### Added
- Added Gen 6-style party-wide EXP Share from the start of the game.
- Added an `EXP SHARE` ON/OFF setting to the normal Options menu.
- Added a one-time settings migration so saves created before 0.0.5 start with the new EXP Share enabled.

### Changed
- When EXP Share is ON, battle participants receive full EXP while eligible non-participating party Pokémon receive the Gen 6-style half share.
- The system reuses pokeemerald-expansion's native EXP pipeline, preserving existing Lucky Egg, traded-Pokémon, scaled EXP, catch EXP, and level-cap handling.
- The Options menu layout was tightened vertically by one tile row so the additional setting fits without reducing normal row spacing.
- Lucky Egg behavior remains unchanged and is tracked separately from EXP Share tuning.

## [0.0.4.2] - 2026-10-07

### Fixed
- Corrected homepage release wording so badge-earned HM field utilities are accurately credited to 0.0.4 rather than the 0.0.4.1 maintenance build.

### Changed
- Added direct Release and Debug changelog links beside their corresponding download options.
- Strengthened changelog consistency checks so the current version must be the newest entry in the canonical, Release, and Debug histories and must appear in both website changelog tabs.
- Published this changelog/site housekeeping as micro-build 0.0.4.2 with no gameplay or content divergence between Release and Debug.

## [0.0.4.1] - 2026-10-07

### Fixed
- Corrected the website changelog so the historical 0.0.3 entries are labeled 0.0.3 instead of 0.0.4.
- Synchronized the current version display across the site, browser patcher, README, and both build variants.

### Changed
- Published this documentation/maintenance correction as micro-build 0.0.4.1 without gameplay or content divergence between Release and Debug.

## [0.0.4] - 2026-10-07

### Added
- Added a global `FIELD` utility submenu to the party action menu for badge-unlocked Emerald field moves.
- Added pull-request verification for both Release and Debug ROM builds before major gameplay changes can merge.

### Changed
- Cut, Flash, Rock Smash, Strength, Surf, Fly, Dive, and Waterfall are now unlocked for overworld use by Emerald's original badge progression rather than by a Pokémon knowing the corresponding HM move.
- Preserved the original Stone, Knuckle, Dynamo, Heat, Balance, Feather, Mind, and Rain Badge progression for the eight field utilities.
- Preserved terrain, map, follower, link, and story-puzzle restrictions while removing the HM moveslot requirement.
- Contextual interactions such as Cut trees, breakable rocks, Strength boulders, Surf water, Dive spots, and Waterfalls now work after the appropriate badge without an HM user.
- Field-move prompts and success text no longer identify a Pokémon as the HM user.
- Badge utility effects suppress the old arbitrary Pokémon portrait/banner while retaining player and environment animations.
- Learned non-HM field moves such as Dig, Teleport, Sweet Scent, and similar utilities remain tied to the Pokémon that knows them.

## [0.0.3] - 2026-10-07

### Added
- Added separate, permanently maintained Release and Debug changelog files alongside the canonical project changelog.
- Added a dedicated website changelog page with one-click Release and Debug tabs.
- Added variant-aware changelog validation so every version must appear in the canonical, Release, and Debug histories.

### Changed
- Advanced both build variants to version 0.0.3.
- Added a compact Changelog link to the main project site instead of placing long update histories on the landing page.
- Clarified project documentation so the normal player build is consistently called Release, reserving “vanilla” for the untouched Pokémon Emerald base ROM.

## [0.0.2] - 2026-10-07

### Added
- Added separate Release and Debug distributions built from the same Pokémon Emerald: Legends source.
- Added a Debug download directly below the recommended Release download on the project website.
- Added browser-patcher support for both Release and Debug builds.
- Added distinct in-game version identification for Debug builds as `LEGENDS v0.0.2-D`.

### Changed
- The recommended player build now uses the expansion's native release configuration, disabling developer/debug entry points while preserving all Legends gameplay and content changes.
- The Debug build retains the overworld debug menu, battle debug menu, Pokémon sprite visualizer, and title-screen Quickstart tools supplied by the expansion base.
- The automated release pipeline now builds, patches, reapplies, and byte-for-byte verifies both Release and Debug variants before publishing them.
- Release filenames now use `Pokemon-Emerald-Legends-v0.0.2.bps` and `Pokemon-Emerald-Legends-v0.0.2-debug.bps`.

## [0.0.1] - 2026-10-07

### Added
- Added a centered `LEGENDS` subtitle to the Emerald title screen while preserving the original Pokémon Emerald logo artwork.
- Added `LEGENDS v0.0.1` identification to the in-game Options menu header.
- Added a release/download section to the project website in preparation for patch distributions.
- Added an in-browser BPS patcher that verifies a clean Emerald ROM and creates the playable `.gba` locally without uploading the source ROM.
- Added a reproducible CI workflow that builds and verifies the v0.0.1 BPS patch from decompiled source.
- Established Pokémon Emerald: Legends project identity.
- Adopted `pokeemerald-expansion` as the upstream base.
- Added project roadmap and development documentation.
- Added feature design documents for EXP changes, overworld field moves, and seasons.
- Added an initial GitHub Pages landing site.
- Added repository contribution and feature-request structure.

### Changed
- Established `0.0.1` as the authoritative current development baseline.
- Added an explicit versioning policy: each meaningful shipped change increments the development revision and receives a matching changelog entry.
- Updated release tooling so BPS filenames are derived from the root `VERSION` file.

### Planned during 0.0.x development
- Implement the revised EXP Share behavior already designed during development.
- Implement HM/field-move use from the overworld without requiring a dedicated HM move slot.
- Research and prototype a configurable seasonal system.
