# Pokémon Emerald: Legends

**Version:** 0.0.57<br>
**Base:** [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion)

Pokémon Emerald: Legends is an unofficial, non-commercial Pokémon Emerald ROM-hack project built on the open-source `pokeemerald-expansion` decompilation/expansion base.

The project is intended to preserve the feel and structure of Pokémon Emerald while layering in modern quality-of-life improvements, configurable mechanics, expanded systems, and new features developed incrementally.

The New Game / Continue / Options menu uses a soft lavender backdrop as of v0.0.13.1. v0.0.54 displays the current version at the right edge of its OPTION card, matching the native text; Debug includes the -D suffix.

v0.0.57 adds a saved tracked quest and a pause-menu reminder of its next objective. Press A on an unfinished quest's Details page to track or stop it. Long reminder text scrolls automatically and smoothly returns to the top; other menus retain their space.

v0.0.56 refines Quest Log and Achievements with filter tabs, alternating paper rows, clear selection, a top-right entry counter and fully visible controls. Manual rewards and older Legends save support remain intact.

v0.0.55 adds personal Mom/Norman milestone conversations and a one-time family welcome after the finale. Speak to Mom at home or Norman at the Gym; native story events, rewards and battles retain priority.

Kanto has eight playable visiting Gyms, each offering a difficulty choice with one victory per save. The Borrowed Voice adds two field surveys and an updated progress journal. The Trainer Card switches between Hoenn and Kanto badge collections. SELECT switches the postgame PokeNav between Hoenn and Kanto. [Postgame design and current scope](docs/features/kanto-postgame.md).

v0.0.53 adds evolving bedroom keepsakes and memories through the current Kanto finale. The bedroom PC offers separate rug, bed and original chair colors, and existing dolls/cushions can use safe clear floor beyond the widened rug. See the [bedroom guide](docs/bedroom-guide.html).

Quest Log and Achievements are on the second pause-menu page (Left/Right). The journal tracks 33 quests and 95 achievements, with one-time berry rewards manually claimed into PC item storage. Nonblocking unlock notices name each earned achievement; a temporary confirmation appears after a successful claim. Storage now offers 20 Pokemon boxes and larger Bag/PC inventories. See [journal and storage documentation](docs/features/quest-log-achievements.md).

## Adventure notebook

The pause menu includes ADVENTURE LOG: turn pages, filter by played day or story, and review milestones, locations and one recent catch. DAY above the clock counts dates actually played; skipped dates add none, while play hours carry across sessions. Existing saves start their notebook at Day 1. [Player guide](https://babycrttv.github.io/pokeemerald-emerald-legends/adventure-guide.html) · [Implementation and validation](docs/features/adventure-log.md).

## Try the current build

The project site provides two builds from the same source:

- **Release (recommended):** https://babycrttv.github.io/pokeemerald-emerald-legends/patcher.html
- **Debug / developer:** https://babycrttv.github.io/pokeemerald-emerald-legends/patcher.html?build=debug
- **Release BPS:** https://babycrttv.github.io/pokeemerald-emerald-legends/downloads/Pokemon-Emerald-Legends-v0.0.44.bps
- **Debug BPS:** https://babycrttv.github.io/pokeemerald-emerald-legends/downloads/Pokemon-Emerald-Legends-v0.0.44-debug.bps

The Release and Debug builds contain the same Legends gameplay/content changes. Release disables developer entry points for a cleaner casual-player build. Debug retains the expansion's overworld/battle/sprite debug tools and title-screen Quickstart.

**PLAYER APPEARANCE:** After choosing gender in Birch’s introduction, choose one of five skin tones and one of five outfits: Emerald, Trail (jacket/trousers), Sport (striped shirt/shorts), Yellow, or Lavender (cream scarf). The bottom-right preview updates as you browse. Custom outfits use bare hands; the default Emerald outfit retains its gloves. Choices save with your game and apply to overworld poses, local battle portraits and your Trainer Card. Existing saves retain the original appearance. Mom and Norman now inherit your selected skin tone in their overworld sprites and Norman’s battle portrait. Their hair, clothing and animations remain unchanged. The approved front-facing cheek shading and hairstyles are preserved. See [appearance documentation](docs/features/player-appearance.md).

**EXP Share:** The physical Gen 6-style Exp. Share is now a Key Item given at new-game start and restored on existing saves. The Key Item and Legends Options control the same ON/OFF setting, defaulting to ON. Participants earn full EXP and eligible benched Pokémon earn the modern half share when enabled.

**DexNav:** Unlocked with Birch's first Pokédex gift, including detector mode. DexNav appears in the Start menu, and older saves with a Pokédex receive it automatically on continue.

**KANTO (v0.0.43):** The nine-chapter Wing Survey is complete. Eight visiting Gyms include Blue in Viridian; Oak's Pallet investigation opens the native Faraway Island/Mew voyage. All three bird habitats and the central-Hoenn Regigigas intermission are playable. Observation advances each survey without requiring capture. Existing Mew captures receive an alternate scene. Night windows/Center signs illuminate, and custom-hair walking/running directions are corrected. [Player and Debug guide](https://babycrttv.github.io/pokeemerald-emerald-legends/kanto-guide.html).

**FOLLOWERS (v0.0.13):** The first conscious non-egg Pokémon in party order follows you using the expansion’s native system. FOLLOWER ON/OFF on Legends Options saves with your game, defaults to ON, and applies on leaving Options. Title-screen choices carry into New Game. See [follower documentation](docs/features/followers.md).

**SEASONS:** Title-screen Legends choices now carry into New Game, including the chosen gameplay season, EXP Share and shiny rate. Legends Options offers REAL TIME (default; Northern Hemisphere calendar months) or 7H PLAY (seven recorded gameplay hours per season). CURRENT shows the active environment; SET SEASON lets gameplay-mode players choose Spring, Summer, Autumn or Winter and restart that season's timer. Changes apply on a faded map transition, such as entering or leaving a building, or on save reload. Seasonal foliage and weather preserve volcanic areas and special/story effects. Kanto uses its own seasonal regional forecasts, and grass/long-grass/plain outdoor battle backgrounds in both regions follow the visible season. See [season documentation](docs/features/seasons.md).

**SHINY RATE (v0.0.10):** Use NEXT PAGE + A (or L/R) to select the Legends Options page, then Left/Right on SHINY RATE to choose 1/8192 (default), 1/5680, or 1/1226. The chosen base rate is stored in an unused permanent save variable; it affects newly generated wild Pokémon, including fishing and DexNav. Shiny Charm, chain-fishing and DexNav bonus rolls still apply. Gift Pokémon, eggs, scripted encounters and already-owned Pokémon use their previous logic.

**Maintenance QA (0.0.8.1):** Browser patching now ignores stale ROM validation and download operations; automated BPS decoding tests have been added. Gameplay mechanics are unchanged from 0.0.8.

**HAIR AND WARDROBE (v0.0.43):** Choose a gender-specific hairstyle and one of eight hair colors in the intro or your home/secret-base wardrobe. Open HAIRSTYLE or HAIR COLOR with A or Left/Right, scroll with Up/Down, confirm with A, then APPLY. Both jackets have full sleeves: Navy and dark-green Winter with ivory shearling. Existing saves keep their hairstyles and Natural color. See [wardrobe details](docs/features/wardrobe.md).

**STARTERS (v0.0.19):** Adventure Options offers Gen 1–9, Special (Happiny/Wattrel/Mankey), and Random (three distinct unevolved Pokémon that can evolve). The rescue screen follows your setting; your rival uses the generation counter or Zorua/Zoroark for Special/Random. Choose before opening the rescue bag; later edits apply to your next New Game. See [starter documentation](docs/features/starters.md).

**DA BUG (v0.0.20):** A single-stage Bug/Grass leafhopper awaits in your PC at level 5, with Tackle, Leer, Mean Look and Absorb. This one-time gift has its own 1-in-10 shiny roll; no wild encounters are added. Existing saves receive it in the first free box slot on continue. v0.0.21 refines its follower/menu sprite scale and lowers its battle back view. See [Da Bug documentation](docs/features/da-bug.md).

**Paged Options:** Options now has General, Legends and Adventure pages. Select NEXT PAGE and press A to switch pages, or use L/R. The visible A: NEXT / B: SAVE hint explains navigation; B saves and exits from any row. The original Emerald window dimensions are preserved so future Legends settings can be added without squeezing or corrupting the menu.

**Rustboro reward:** After delivering Mr. Stone's Letter to Steven, the Devon Corp. reward is now a Lucky Egg instead of the redundant held Exp. Share.

**Pokédex progression:** Professor Birch enables National Mode as soon as he gives the Pokédex. After becoming Champion, his former National Dex upgrade scene instead awards 25 Rare Candies, with PC fallback if the Bag is too full.

**Badge-earned field moves:** Cut, Flash, Rock Smash, Strength, Surf, Fly, Dive, and Waterfall no longer require an HM moveslot for overworld use. Emerald's original badge progression and map restrictions remain in place.

The browser patcher verifies a clean U.S./Europe Pokémon Emerald ROM (SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`) and creates the selected `.gba` locally. The source ROM is never uploaded.

## Development philosophy

- Preserve the recognizable Emerald adventure as the foundation.
- Prefer configurable features over hard-coded behavior where practical.
- Reuse `pokeemerald-expansion` systems before introducing duplicate implementations.
- Keep custom mechanics documented and isolated so upstream updates remain manageable.
- Never commit or distribute a commercial Pokémon ROM.

## Initial 0.0.x focus

The first development milestone establishes the project structure and prepares the first custom systems:

- Gen 6-style party EXP Share with an Options toggle
- Overworld field moves / HM quality-of-life system
- Seasonal world and encounter framework
- Project configuration documentation
- Reproducible build workflow
- GitHub Pages project site

See [ROADMAP.md](ROADMAP.md) and the documentation in [`docs/features`](docs/features).

## Building

This repository is a fork of `rh-hideout/pokeemerald-expansion`. Follow the current upstream installation and build instructions in [INSTALL.md](INSTALL.md).

- `make release` produces the normal player build with release-disabled developer features removed.
- `make` produces the development/debug-capable build used for the public Debug variant.

Generated ROMs and other copyrighted binary material must not be committed to this repository.

## Upstream

Pokémon Emerald: Legends is built on the work of the `pokeemerald-expansion` community.

- Upstream project: https://github.com/rh-hideout/pokeemerald-expansion
- Upstream documentation: https://rh-hideout.github.io/pokeemerald-expansion/
- Existing upstream credits: [CREDITS.md](CREDITS.md)

The existing upstream license, credits, and notices remain part of this fork.

## Interactive Pokédex & encounter guide

[Browse the Legends Pokédex and wild encounters](https://babycrttv.github.io/pokeemerald-emerald-legends/wiki/dex.html) for searchable Hoenn/Kanto routes, in-game Pokémon sprites, level ranges and verified per-method encounter shares. This is a separate, manually refreshed website feature also accessible from the wiki Android APK; it does not touch the game build or release number.

## Player Wiki

The [free Pokémon Emerald: Legends Wiki](https://babycrttv.github.io/pokeemerald-emerald-legends/wiki/) is a searchable, no-login, lavender-themed player encyclopedia. It documents game systems, customization, and the currently playable Kanto postgame. Wiki content is refreshed **only when specifically requested**, not on every ROM release. The companion [Android wiki APK](https://babycrttv.github.io/pokeemerald-emerald-legends/downloads/Emerald-Legends-Wiki.apk) loads that same site and receives its intentionally published article updates without needing a new APK.

## Project documentation

- [Roadmap](ROADMAP.md)
- [Full project changelog](CHANGELOG.md)
- [Release changelog](CHANGELOG-RELEASE.md)
- [Debug changelog](CHANGELOG-DEBUG.md)
- [Website changelog](https://babycrttv.github.io/pokeemerald-emerald-legends/changelog.html)
- [Versioning policy](docs/VERSIONING.md)
- [Development guide](docs/DEVELOPMENT.md)
- [QA and regression checklist](docs/QA.md)
- [Legal / distribution notes](docs/LEGAL.md)
- [EXP system design](docs/features/exp-system.md)
- [Paged Options menu](docs/features/options-menu.md)
- [Pokédex and Champion reward](docs/features/pokedex-progression.md)
- [Overworld field moves](docs/features/field-moves.md)
- [Seasonal system](docs/features/seasons.md)

## Legal

This is an unofficial fan project and is not affiliated with, endorsed by, or sponsored by Nintendo, Creatures, GAME FREAK, The Pokémon Company, or other rights holders. Pokémon and related properties belong to their respective owners.

No commercial Pokémon ROM is included in this repository.

**DYNAMIC WEATHER (v0.0.22):** Regional forecasts bring rain, occasional storms, rainforest/upland fog and winter upland flurries. Clear nights show a moon in the pause panel. See [weather documentation](docs/features/weather.md).

**WARDROBE (v0.0.23, refined v0.0.24):** Change outfits and add colored scarves or a navy jacket at home, or wear complete Team Magma/Aqua grunt costumes. Buy a placeable secret-base wardrobe from Pretty Petal. Accessories appear on your avatar, battle portraits and local Trainer Card. See [wardrobe documentation](docs/features/wardrobe.md).
