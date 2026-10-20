# Seasonal encounters — Routes 101–116

**Model: GPT-6 | Approach: preserve native residents/levels and resolve every dependent land-table consumer through the committed season.**

Status: Routes 101–104 grass shipped in v0.0.63; Routes 105–108 Surf in v0.0.64; Route 109 Surf and Routes 110–112 land in v0.0.65. Both live v0.0.65 patches were independently decoded and verified against production ROM hashes. Approved native DexNav sizing/centering and silhouettes were preserved.

## Grass pilot — Routes 101–104 (v0.0.63)

- Grass encounters on Routes 101, 102, 103 and 104 (both halves). Water, fishing, Rock Smash, hidden-only tables and other maps retain their published data.
- Original resident species stay available in every season and collectively occupy 70% of normal grass encounters. Two visitors occupy 20% and 10%; the existing twelve-slot weights, per-slot levels and encounter rate 20 are retained. These are base odds before native Lures or attraction abilities apply.
- Selections span Generations 1–9, including native seasonal/regional forms. Early routes use unevolved, ordinary species; no legendary, mythical, paradox or Da Bug encounters were added.
- This pilot applies all day; native time-of-day encounter support is currently disabled. No new nocturnal restrictions were introduced.
- Read the committed active season used by the world. A pending clock/playtime change waits for the existing safe transition. No new option, variable, save field, encounter roll, quest or achievement ID was added.
- Ordinary walking, Sweet Scent, local-mon helpers, optional overworld encounters, DexNav lists/levels/completion/hunts, Match Call hints and Pokédex habitat maps use the same land resolver. Outbreaks, roamers and Frontier tables retain native priority.

## Seasonal visitors

### Route 101 — levels 2–3

Year-round residents: Poochyena, Wurmple, Zigzagoon.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Scatterbug | Fletchling |
| Summer | Sunkern | Hoppip |
| Autumn | Sentret | Tarountula |
| Winter | Skwovet | Rookidee |

### Route 102 — levels 3–4

Year-round residents: Lotad, Poochyena, Ralts, Seedot, Wurmple, Zigzagoon.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Budew | Azurill |
| Summer | Surskit | Tympole |
| Autumn | Sewaddle | Smoliv |
| Winter | Wooper | Ducklett |

### Route 103 — levels 2–4

Year-round residents: Poochyena, Wingull, Zigzagoon.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Pidove | Bunnelby |
| Summer | Buizel | Wattrel |
| Autumn | Nidoran♀ | Nickit |
| Winter | Spheal | Lillipup |

### Route 104 — levels 3–5

Year-round residents: Marill, Poochyena, Taillow, Wingull, Wurmple.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Caterpie | Cutiefly |
| Summer | Fomantis | Ledyba |
| Autumn | Autumn Deerling | Shroomish |
| Winter | Snorunt | Alolan Sandshrew |

## Surf extension — Routes 105–108 (v0.0.64)

The owner chose the next four numbered sea routes. Their seasonal Surf extension shipped in v0.0.64 after PR/production builds, native mGBA, BPS round trips and both live patch decoders passed. These routes have no grass tables.

The native five Surf slots retain weights **60/30/5/4/1**, their exact level ranges **5–35 / 10–30 / 15–25 / 25–30 / 25–30**, and encounter rate **4**. Tentacool occupies 60%, Wingull 4% and Pelipper 1% in every season; the two visitors occupy 30% and 5%. This intentionally makes 65% original residents and 35% seasonal visitors. Existing level ranges stay attached to slots; resident Wingull now uses the original fourth slot's levels 25–30. Native Lures and attraction abilities retain their usual modifiers.

Fishing remains the original Old/Good/Super Rod data, including Magikarp, Tentacool and Wailmer. The Abandoned Ship, Island Cave, neighboring routes, Dive encounters, hidden-only data and the existing Routes 101–104 grass implementation are unchanged. Surf visitors use the committed active season, all day. The shared resolver covers normal Surf, Sweet Scent, DexNav lists/levels/completion/hunts, habitat maps, local helpers, Match Call and optional overworld encounters. Native roamers, suppression gates, encounter checks and scripted battles retain priority. No new saved field, flag/variable, option, persistent ID or migration was added.

### Route 105 — Surf

| Season | 30% visitor (levels 10–30) | 5% visitor (levels 15–25) |
|---|---|---|
| Spring | Finneon | Mantyke |
| Summer | Finizen | Alomomola |
| Autumn | Remoraid | Frillish |
| Winter | Chinchou | Spheal |

### Route 106 — Surf

| Season | 30% visitor (levels 10–30) | 5% visitor (levels 15–25) |
|---|---|---|
| Spring | Krabby | Binacle |
| Summer | Clauncher | Corsola |
| Autumn | Skrelp | Mareanie |
| Winter | Shellder | Pincurchin |

### Route 107 — Surf

| Season | 30% visitor (levels 10–30) | 5% visitor (levels 15–25) |
|---|---|---|
| Spring | Buizel | Wishiwashi |
| Summer | Arrokuda | Bruxish |
| Autumn | Basculin (red-striped) | Inkay |
| Winter | Seel | Qwilfish |

### Route 108 — Surf

| Season | 30% visitor (levels 10–30) | 5% visitor (levels 15–25) |
|---|---|---|
| Spring | Horsea | Shellos (west) |
| Summer | Wiglett | Pyukumuku |
| Autumn | Corphish | Clamperl |
| Winter | Slowpoke | Relicanth |

[Surf QA and release status](../qa/seasonal-surf-v0.0.64.md).

## Next numbered routes — v0.0.65 (published and verified)

**Model: GPT-6 | Approach: append native-method tables; retain every resident, committed-season behavior and approved icon geometry.**

The next four numbered routes add sixteen tables and 32 distinct visitors across Generations 1–9. Route 109 uses Surf (65% residents, 30%/5% visitors); Routes 110–112 use native land encounters (70% residents, 20%/10% visitors). Route 111 applies to desert sand encounters, not its southern paths. Native per-slot levels, slot weights and encounter rates remain exact; species shares and species-level ranges can change when their slots change. Route 111 retains encounter rate 10; Routes 110/112 retain 20; Route 109 Surf retains 4. All use the committed active season, all day.

Fishing, Rock Smash, Routes 110/111 Surf, hidden-only tables, neighboring caves and Routes 101–108 remain unchanged. No maps, art, options, saved fields, variables, persistent IDs or migrations were added. Native desert access, weather, encounter priorities, attraction abilities and DexNav seen/search gates remain intact.

### Route 109 — Surf

Year-round residents: Tentacool, Wingull, Pelipper.

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Staryu | Dewpider |
| Summer | Luvdisc | Chewtle |
| Autumn | Cramorant | Veluza |
| Winter | Sealeo | Eiscue |

### Route 110 — grass

Year-round residents: Poochyena, Electrike, Gulpin, Minun, Oddish, Wingull, Plusle.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Combee | Petilil |
| Summer | Yamper | Blitzle |
| Autumn | Trubbish | Shroodle |
| Winter | Pachirisu | Emolga |

### Route 111 — desert

Year-round residents: Sandshrew, Trapinch, Baltoy, Cacnea.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Sandile | Helioptile |
| Summer | Silicobra | Hippopotas |
| Autumn | Dwebble | Skorupi |
| Winter | Phanpy | Gible |

### Route 112 — grass

Year-round residents: Numel, Marill.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Ponyta | Deerling |
| Summer | Litleo | Sizzlipede |
| Autumn | Houndour | Rolycoly |
| Winter | Vulpix | Rockruff |

## Routes 113–116 — v0.0.66 (shipped; production CI verified)

**Model: GPT-6 | Approach: append native land tables and retain the approved encounter, art and save baseline.**

Sixteen tables add 32 distinct visitors across Generations 1–9. Original residents occupy 70% in every season, with two visitors at 20% and 10%. Native twelve-slot levels/weights and encounter rate 20 stay exact; species shares and species-level ranges can change with reassigned slots. Route 113 uses its existing ash-grass encounters; the ash/weather, flute collection, maps and tile behavior are unchanged. Route 115 uses its existing northern grass, retaining normal access requirements. Water, fishing, Rock Smash, cave encounters and all earlier seasonal tables remain unchanged. All visitors use the committed active season, all day. No saved fields, IDs or migrations were added. Routine user-facing DexNav previews were waived; focused native QA remains required.

### Route 113

Year-round residents: Spinda, Slugma, Skarmory.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Growlithe | Rufflet |
| Summer | Salandit | Charcadet |
| Autumn | Vullaby | Klink |
| Winter | Sneasel | Bronzor |

### Route 114

Year-round residents: Swablu, Lotad, Lombre, Seviper, Nuzleaf.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Bounsweet | Applin |
| Summer | Skiddo | Pancham |
| Autumn | Teddiursa | Morelull |
| Winter | Snover | Cetoddle |

### Route 115

Year-round residents: Swablu, Taillow, Swellow, Jigglypuff, Wingull.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Mienfoo | Farfetchd |
| Summer | Hawlucha | Passimian |
| Autumn | Zangoose | Murkrow |
| Winter | Minccino | Absol |

### Route 116

Year-round residents: Poochyena, Whismur, Nincada, Abra, Taillow, Skitty.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Pichu | Buneary |
| Summer | Kricketot | Blipbug |
| Autumn | Nymble | Patrat |
| Winter | Wooloo | Espurr |

## DexNav silhouettes

Unseen route entries use the actual native animated party icon with all nontransparent colors mapped to a separate black OBJ palette. Known icons retain their original shared palettes and animation. Empty slots retain the native X. Names, types, search eligibility, seen/caught flags and detector-mode selection stay unchanged. Locked hidden-only entries also show silhouettes rather than question marks. No icon artwork is replaced. A DexNav-only presentation helper centers the combined bounds of both native poses and uniformly shrinks oversized icons to fit the existing columns. It never enlarges small species or edits shared party/battle/follower assets; both discovered and silhouette states use identical placement.

## Verification / approval

The owner approved the roster and silhouette approach, with a request to correct DexNav sizing/centering. Final source `4660dc53` passed project checks, 4,096 geometry cases, a shipped-C audit of all 1,809 native icon sheets and 35 controlled native mGBA cases (8,960 wild creations). All 54 captures were visually reviewed and panel containment was asserted. [Final correction evidence and release gate](../qa/dexnav-layout-v0.0.63.md) · [Native receipt](../qa/dexnav-layout-v0.0.63-native.json) · [Corrected preview](../qa/dexnav-layout-v0.0.63-preview.png).

PR and production Debug/Release builds, project checks, both BPS validations and native mGBA checks passed. [Live publication receipt](../qa/dexnav-layout-v0.0.63-public.json). Controlled Debug fixtures do not establish natural progression, a full DexNav hunt, historical-save migration, native Release interaction or Pizza Boy coverage. Original pre-correction evidence remains in the [first trial QA record](../qa/seasonal-encounters-v0.0.63.md).
