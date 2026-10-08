# Pokémon Emerald: Legends

**Version:** 0.0.13  
**Base:** [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion)

Pokémon Emerald: Legends is an unofficial, non-commercial Pokémon Emerald ROM-hack project built on the open-source `pokeemerald-expansion` decompilation/expansion base.

The project is intended to preserve the feel and structure of Pokémon Emerald while layering in modern quality-of-life improvements, configurable mechanics, expanded systems, and new features developed incrementally.

## Try the current v0.0.13 build

The project site provides two builds from the same source:

- **Release (recommended):** https://babycrttv.github.io/pokeemerald-emerald-legends/patcher.html
- **Debug / developer:** https://babycrttv.github.io/pokeemerald-emerald-legends/patcher.html?build=debug
- **Release BPS:** https://babycrttv.github.io/pokeemerald-emerald-legends/downloads/Pokemon-Emerald-Legends-v0.0.13.bps
- **Debug BPS:** https://babycrttv.github.io/pokeemerald-emerald-legends/downloads/Pokemon-Emerald-Legends-v0.0.13-debug.bps

The Release and Debug builds contain the same Legends gameplay/content changes. Release disables developer entry points for a cleaner casual-player build. Debug retains the expansion's overworld/battle/sprite debug tools and title-screen Quickstart.

**EXP Share:** The physical Gen 6-style Exp. Share is now a Key Item given at new-game start and restored on existing saves. The Key Item and Legends Options control the same ON/OFF setting, defaulting to ON. Participants earn full EXP and eligible benched Pokémon earn the modern half share when enabled.

**DexNav:** Unlocked with Birch's first Pokédex gift, including detector mode. DexNav appears in the Start menu, and older saves with a Pokédex receive it automatically on continue.

**FOLLOWERS (v0.0.13):** The first conscious non-egg Pokémon in party order follows you using the expansion’s native system. FOLLOWER ON/OFF on Legends Options saves with your game, defaults to ON, and applies on leaving Options. Title-screen choices carry into New Game. See [follower documentation](docs/features/followers.md).

**SEASONS:** Title-screen Legends choices now carry into New Game, including the chosen gameplay season, EXP Share and shiny rate. Legends Options offers REAL TIME (default; Northern Hemisphere calendar months) or 7H PLAY (seven recorded gameplay hours per season). CURRENT shows the active environment; SET SEASON lets gameplay-mode players choose Spring, Summer, Autumn or Winter and restart that season's timer. Changes apply on a faded map transition, such as entering or leaving a building, or on save reload. Seasonal foliage and weather preserve volcanic areas and special/story effects. See [season documentation](docs/features/seasons.md).

**SHINY RATE (v0.0.10):** Use L/R to select the Legends Options page, then Left/Right on SHINY RATE to choose 1/8192 (default), 1/5680, or 1/1226. The chosen base rate is stored in an unused permanent save variable; it affects newly generated wild Pokémon, including fishing and DexNav. Shiny Charm, chain-fishing and DexNav bonus rolls still apply. Gift Pokémon, eggs, scripted encounters and already-owned Pokémon use their previous logic.

**Maintenance QA (0.0.8.1):** Browser patching now ignores stale ROM validation and download operations; automated BPS decoding tests have been added. Gameplay mechanics are unchanged from 0.0.8.

**Paged Options:** Options now has General and Legends pages. Use L/R to switch pages. The original Emerald window dimensions are preserved so future Legends settings can be added without squeezing or corrupting the menu.

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
