# Pokémon Emerald: Legends

**Version:** 0.0.6  
**Base:** [pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion)

Pokémon Emerald: Legends is an unofficial, non-commercial Pokémon Emerald ROM-hack project built on the open-source `pokeemerald-expansion` decompilation/expansion base.

The project is intended to preserve the feel and structure of Pokémon Emerald while layering in modern quality-of-life improvements, configurable mechanics, expanded systems, and new features developed incrementally.

## Try the current v0.0.6 build

The project site provides two builds from the same source:

- **Release (recommended):** https://babycrttv.github.io/pokeemerald-emerald-legends/patcher.html
- **Debug / developer:** https://babycrttv.github.io/pokeemerald-emerald-legends/patcher.html?build=debug
- **Release BPS:** https://babycrttv.github.io/pokeemerald-emerald-legends/downloads/Pokemon-Emerald-Legends-v0.0.6.bps
- **Debug BPS:** https://babycrttv.github.io/pokeemerald-emerald-legends/downloads/Pokemon-Emerald-Legends-v0.0.6-debug.bps

The Release and Debug builds contain the same Legends gameplay/content changes. Release disables developer entry points for a cleaner casual-player build. Debug retains the expansion's overworld/battle/sprite debug tools and title-screen Quickstart.

**EXP Share:** Gen 6-style party EXP is available from the start and defaults to ON. Battle participants receive full EXP while eligible non-participating party members receive the modern half share. It can be switched ON or OFF at any time from Options.

**Rustboro reward:** After delivering Mr. Stone's Letter to Steven, the Devon Corp. reward is now a Lucky Egg instead of the redundant held Exp. Share.

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
- [Legal / distribution notes](docs/LEGAL.md)
- [EXP system design](docs/features/exp-system.md)
- [Overworld field moves](docs/features/field-moves.md)
- [Seasonal system](docs/features/seasons.md)

## Legal

This is an unofficial fan project and is not affiliated with, endorsed by, or sponsored by Nintendo, Creatures, GAME FREAK, The Pokémon Company, or other rights holders. Pokémon and related properties belong to their respective owners.

No commercial Pokémon ROM is included in this repository.
