# Pokémon Emerald: Legends Roadmap

Reviewed against **v0.0.55** on 15 October 2026. The root `VERSION`, current source and [development handoff](docs/DEVELOPMENT-HANDOFF.md) take precedence over older milestone notes. [Verification and remaining playtests](docs/qa/project-state-2026-10-15.md).

## 0.0.x - Foundation

Goal: establish a stable `pokeemerald-expansion` project and implement the first quality-of-life systems without changing the core Emerald identity.

### Project foundation
- [x] Project name and versioning established
- [x] Documentation structure established
- [x] GitHub Pages site scaffolded
- [x] Fork/import current stable `pokeemerald-expansion` base
- [x] Confirm clean build through automated release verification
- [x] Add automated build and BPS verification

### Gameplay systems
- [x] Gen 6-style party EXP Share with Options toggle
- [x] Replace Rustboro's redundant held Exp. Share reward with Lucky Egg
- [x] Unlock National Pokédex at Professor Birch's initial Pokédex handoff
- [x] Replace the post-Elite Four National Dex upgrade reward with 25 Rare Candies
- [ ] Lucky Egg behavior review / tuning
- [x] Overworld HM / field move system
- [x] Field move animation and usability rules
- [x] Seasonal framework: native RTC calendar / seven saved gameplay hours
- [x] Seasonal outdoor foliage and ambient weather
- [x] Native overworld Pokémon followers with saved Options toggle
- [x] Seasonal grass effects, winter scuffs and Hoenn/Kanto battle palettes
- [x] Regional dynamic forecasts and animated day/night weather indicators
- [x] Early DexNav, saved shiny-rate choices and starter-generation selection
- [x] Quest Log, 95 achievements and expanded Bag/PC storage
- [x] Deferred achievement notices and corrected journal selection rendering
- [x] Evolving bedroom keepsakes, independent furnishing colors and safe floor decoration
- [x] Personal Mom/Norman milestones and a one-time family welcome after the finale (v0.0.55)
- [x] Six selectable Birch field requests with one-active, abandon/retry and native Quest Log integration (v0.0.58 preview; owner approval pending)
- [ ] Seasonal encounter hooks

### Trainer appearance
- [x] Home/secret-base wardrobe, outfits, accessories, footwear and Trainer Card colors
- [x] Gender-specific hairstyles, independent hair colors and five skin tones
- [x] Fixed Team Magma/Aqua costumes, striped Sport shorts and female leggings
- [x] Prepared male/female battle hairstyles with fixed native battle uniforms
- [x] Approved v0.0.46 male overworld artwork and v0.0.47 smile/body-color isolation
- [x] Approved Side Part head, single transparent-cell repair and native animation checks (v0.0.48)
- [x] Approved front-face shading and inherited Mom/Norman skin tones (v0.0.49–0.0.50)
- [ ] Further visual tuning from specific owner feedback

### Kanto postgame
- [x] Champion invitation and permanent Lilycove–Vermilion ferry
- [x] Vermilion arrival, residents, facilities and optional spectator challenge
- [x] Routes 6–8 / 11–19 road loop, regional map browsing and Surf passage
- [x] First four visiting Gyms, three Wing Survey reports and regional Trainer Card badges
- [x] Route 10, Rock Tunnel and Power Plant: Quiet Current survey and optional Lv. 50 Zapdos
- [x] Native FireRed wild encounter levels and unobstructed Trainer Card region navigation
- [x] Northern/western circuit and all eight visiting Gyms, including Blue in Viridian
- [x] Seafoam/Articuno, Cinnabar and the limited Mt. Ember/Moltres expedition
- [x] Hoenn Weather Institute/Regigigas intermission
- [x] Oak's analysis, Old Sea Map voyage and native Faraway Island/Mew conclusion
- [x] Return travel, optional bird/Mew captures and legacy caught-Mew handling
- [ ] Research Johto assets and geography after Kanto is established

The complete Wing Survey is playable. Route 22's League approach, unrelated interiors and the rest of Sevii remain closed; the completed survey does not imply a complete Kanto League or Sevii region.

### Quality and maintenance
- [x] Add paged General / Legends Options framework for future settings
- [ ] Centralize Legends-specific configuration flags
- [x] Establish feature documentation and an emulator regression checklist
- [x] Retain release provenance, approved-asset checks and a model-independent handoff
- [ ] Complete uninterrupted story/return-travel, battle-balance and mGBA/Pizza Boy compatibility playtests
- [ ] Establish a reusable test-save matrix without publishing ROMs or private saves
- [ ] Reconcile the conflicting older wiki PR #56 with the published v1.6.0 snapshot
- [ ] Establish upstream update procedure

## Later milestones

### 0.1.x
- Additional quality-of-life mechanics
- Expanded configuration menu ideas
- Encounter and Pokédex tuning
- Seasonal polish

### 0.2.x and beyond
- New events, side content, maps, trainers, and postgame ideas as the design develops
- Additional optional difficulty and gameplay settings

The roadmap is intentionally flexible. Features should move between milestones when implementation or upstream changes make that sensible.
