# Seasonal encounters in Hoenn and Kanto

**Model: GPT-6 | Approach: preserve native residents/levels and resolve every dependent land-table consumer through the committed season.**

Hoenn Routes 101–134 shipped across v0.0.63–v0.0.74. Version 0.0.86 adds seasonal grass encounters to Kanto Routes 1–4. Version 0.0.87 expands Kanto seasonal grass and Surf encounters across 17 additional maps.

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

## Routes 117–121 — v0.0.67 (published and verified)

**Model: GPT-6.1 | Reasoning: extend native land rosters while preserving habitat, encounter dependencies, approved assets and save compatibility.**

Twenty new seasonal land tables add 40 distinct visitors not present in the previous seasonal roster. Original residents remain available year-round at a combined 70%; seasonal visitors occupy 20% and 10%. Native twelve-slot levels/weights stay exact. Encounter rate stays 20 except Route 119, which retains 15. Routes 119–120 retain native long grass and their existing field-move/weather behavior. Surf, fishing, Feebas fishing tiles, Kecleon events, Weather Institute/rival/story gates, Day Care, Safari access and all prior tables are unchanged. Birch/Devon survey types retain their original resident/gift options. No saved data or identifiers changed; no migration is needed. Availability is all day and uses the existing committed active season.

### Route 117

Year-round residents: Poochyena, Oddish, Marill, Illumise, Volbeat, Seedot.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Cherubi | Flabebe |
| Summer | Venonat | Roselia |
| Autumn | Foongus | Swirlix |
| Winter | Snubbull | Drowzee |

### Route 118

Year-round residents: Zigzagoon, Electrike, Linoone, Manectric, Wingull, Kecleon.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Doduo | Nidoran M |
| Summer | Tauros | Girafarig |
| Autumn | Miltank | Stantler |
| Winter | Bouffalant | Shinx |

### Route 119

Year-round residents: Zigzagoon, Linoone, Oddish, Tropius, Kecleon.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Bellsprout | Bonsly |
| Summer | Yanma | Carnivine |
| Autumn | Paras | Croagunk |
| Winter | Tangela | Oranguru |

### Route 120

Year-round residents: Poochyena, Mightyena, Oddish, Marill, Absol, Kecleon, Seedot.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Exeggcute | Natu |
| Summer | Aipom | Heracross |
| Autumn | Pineco | Bramblin |
| Winter | Snom | Hatenna |

### Route 121

Year-round residents: Poochyena, Shuppet, Mightyena, Oddish, Gloom, Wingull, Kecleon.

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Duskull | Gothita |
| Summer | Scraggy | Venipede |
| Autumn | Phantump | Pumpkaboo |
| Winter | Misdreavus | Greavard |

## Routes 122–126 — v0.0.72 (published and verified)

**Model: GPT-6 (Codex) | Reasoning: append native-method data, preserve every original resident/slot and related field-survey/story access.**

Twenty appended tables add 40 distinct visitors spanning Generations 1–9, without repeating earlier seasonal visitors or grotto pools. Route 123 grass keeps residents at 70% and visitors at 20%/10%; Surf on Routes 122/124/125/126 keeps residents at 65% and visitors at 30%/5%. Slot levels and native rates (20 grass; 4 Surf) remain exact. Grass visitors use levels 28 and 26; Surf visitors retain levels 10–30 and 15–25. All use the existing committed season, all day.

Native residents remain year-round: Poochyena, Shuppet, Mightyena, Oddish, Gloom, Wingull and Kecleon on Route 123; Tentacool, Wingull and Pelipper on the sea routes. Fishing, Route 123 Surf, Dive encounters, shards, berries, Mt. Pyre/Shoal Cave, Sootopolis/story/HM access, weather and all existing maps/scripts/artwork are unchanged. Birch’s Route 124 Water-partner and underwater studies retain native partners and gates. No save fields, identifiers, options or migrations were introduced.

### Route 122 — Surf

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Psyduck | Goldeen |
| Summer | Poliwag | Seaking |
| Autumn | Barboach | Quagsire |
| Winter | Palpitoad | Dewgong |

### Route 123 — grass

| Season | 20% visitor | 10% visitor |
|---|---|---|
| Spring | Toedscool | Chingling |
| Summer | Dunsparce | Stunky |
| Autumn | Yamask | Litwick |
| Winter | Golett | Elgyem |

### Route 124 — Surf

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Lumineon | Mantine |
| Summer | Floatzel | Octillery |
| Autumn | Lanturn | Seadra |
| Winter | Golduck | Cloyster |

### Route 125 — Surf

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Wimpod | Kingler |
| Summer | Carvanha | Sharpedo |
| Autumn | Wugtrio | Crawdaunt |
| Winter | Wailmer | Walrein |

### Route 126 — Surf

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Araquanid | Swanna |
| Summer | Drednaw | Clawitzer |
| Autumn | Jellicent | Barbaracle |
| Winter | Tentacruel | Kingdra |

[Source/compatibility receipt](../qa/seasonal-routes-v0.0.72-source.json). Candidate and production native checks passed all 220 scenarios / 56,320 actual creations, with all 279 prior encounter frames pixel-identical. Both public patches match the independently decoded candidates and native-tested ROM targets. [Production/public receipt](../qa/seasonal-routes-v0.0.72-public.json).

## Routes 127–131 — v0.0.73 (published and verified)

**Model: GPT-6 (Codex) | Reasoning: retain native slot capacity, rare Wailord and special island/story layouts while extending ordinary Surf only.**

Twenty new Surf tables add 36 distinct seasonal visitors spanning Generations 1–9, with no earlier seasonal/grotto species repeated. Routes 127/128/130/131 retain Tentacool 60%, Wingull 4% and Pelipper 1%, with visitors 30%/5%. Route 129 has four native residents: Tentacool 60%, Wingull 5%, Pelipper 4% and **Wailord 1%**. It therefore receives one seasonal visitor at 30%, preserving every resident and the rare Wailord slot without expanding/reweighting the native five slots. Exact native per-slot levels and rate 4 remain unchanged; common visitors use 10–30 and rare visitors 15–25. All use the committed active season, all day.

Fishing/Dive, Mirage Island’s Wynaut grass/appearance/Liechi Berry, Sky Pillar layout/access, Route127/129 abnormal weather/Marine Cave, Route 128 Seafloor Cavern/story actors and existing grotto scenery remain unchanged. No maps, tilesets, scripts, artwork, sprites, saves, readers, flags/variables or persistent IDs changed. Earlier 104 tables are protected by exact hashes. No migration is needed.

### Route 127 — Surf

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Poliwhirl | Politoed |
| Summer | Azumarill | Poliwrath |
| Autumn | Whiscash | Seismitoad |
| Winter | Slowbro | Slowking |

### Route 128 — Surf

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Croconaw | Starmie |
| Summer | Feraligatr | Toxapex |
| Autumn | Huntail | Gorebyss |
| Winter | Dragalge | Golisopod |

### Route 129 — Surf

| Season | 30% visitor | Native rare resident |
|---|---|---|
| Spring | Gastrodon | Wailord (1%, all seasons) |
| Summer | Dondozo | Wailord (1%, all seasons) |
| Autumn | Carracosta | Wailord (1%, all seasons) |
| Winter | Empoleon | Wailord (1%, all seasons) |

### Route 130 — Surf

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Marshtomp | Swampert |
| Summer | Brionne | Primarina |
| Autumn | Dewott | Samurott |
| Winter | Prinplup | Inteleon |

### Route 131 — Surf

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Overqwil | Barraskewda |
| Summer | Quaxwell | Quaquaval |
| Autumn | Frogadier | Greninja |
| Winter | Drizzile | Gyarados |

[Source/compatibility receipt](../qa/seasonal-routes-v0.0.73-source.json). Candidate and production project/browser/native/build/dual-decoder gates passed. Candidate captures retained identical pixels across all 345 prior encounter frames. Both actual public patches match independently decoded candidates and their native-tested ROM targets; LegendsDex 1.6.1 is synchronized. [Production/public receipt and limits](../qa/seasonal-routes-v0.0.73-public.json).

## Routes 132–134 — v0.0.74

**Model: GPT-6 (Codex) | Reasoning: append native Surf variety while preserving the current maze, underwater access and ancient puzzle requirements.**

Twelve new Surf tables add 24 distinct aquatic visitors, repeating no earlier seasonal/grotto species. Tentacool remains60%, Wingull 4% and Pelipper 1% in every season; visitors use 30%/5%. Native five-slot weights, per-slot levels and encounter rate 4 remain exact. Visitors retain levels 10–30 and 15–25, all day, using the existing committed active season.

Currents, map/collision geometry, Route 134’s Dive warp, underwater encounters, Sealed Chamber Dig/first-Wailord/last-Relicanth checks and one-time doors remain unchanged. New wild rosters do not include Wailord, Relicanth or Feebas. Fishing/Feebas tiles, earlier tables, approved artwork/wardrobe and save layouts/IDs remain unchanged; no migration is needed.

### Route 132 — Surf

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Panpour | Simipour |
| Summer | Wartortle | Blastoise |
| Autumn | Bibarel | Ludicolo |
| Winter | Clobbopus | Grapploct |

### Route 133 — Surf

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Tynamo | Eelektrik |
| Summer | Eelektross | Malamar |
| Autumn | Stunfisk | Vaporeon |
| Winter | Flamigo | Cursola |

### Route 134 — Surf

| Season | 30% visitor | 5% visitor |
|---|---|---|
| Spring | Omanyte | Omastar |
| Summer | Kabuto | Kabutops |
| Autumn | Magikarp | Milotic |
| Winter | Dracovish | Arctovish |

[Source/compatibility receipt](../qa/seasonal-routes-v0.0.74-source.json). Host and candidate project/browser/native/both-build/dual-decoder checks passed; all 288 native scenarios completed. The four native animation-phase differences in older Route 130 captures are recorded in QA; no artwork/layout changed. Production project/browser/native/both-build/dual-decoder gates passed. Both actual public patches match independently decoded candidates and native-tested production ROMs; LegendsDex 1.6.2 is live. [Production/public receipt and limits](../qa/seasonal-routes-v0.0.74-public.json).

## DexNav silhouettes

Unseen route entries use the actual native animated party icon with all nontransparent colors mapped to a separate black OBJ palette. Known icons retain their original shared palettes and animation. Empty slots retain the native X. Names, types, search eligibility, seen/caught flags and detector-mode selection stay unchanged. Locked hidden-only entries also show silhouettes rather than question marks. No icon artwork is replaced. A DexNav-only presentation helper centers the combined bounds of both native poses and uniformly shrinks oversized icons to fit the existing columns. It never enlarges small species or edits shared party/battle/follower assets; both discovered and silhouette states use identical placement.

## Verification / approval

The owner approved the roster and silhouette approach, with a request to correct DexNav sizing/centering. Final source `4660dc53` passed project checks, 4,096 geometry cases, a shipped-C audit of all 1,809 native icon sheets and 35 controlled native mGBA cases (8,960 wild creations). All 54 captures were visually reviewed and panel containment was asserted. [Final correction evidence and release gate](../qa/dexnav-layout-v0.0.63.md) · [Native receipt](../qa/dexnav-layout-v0.0.63-native.json) · [Corrected preview](../qa/dexnav-layout-v0.0.63-preview.png).

PR and production Debug/Release builds, project checks, both BPS validations and native mGBA checks passed. [Live publication receipt](../qa/dexnav-layout-v0.0.63-public.json). Controlled Debug fixtures do not establish natural progression, a full DexNav hunt, historical-save migration, native Release interaction or Pizza Boy coverage. Original pre-correction evidence remains in the [first trial QA record](../qa/seasonal-encounters-v0.0.63.md).

## Kanto Routes 1–4 (v0.0.86)

The first Kanto batch uses grass encounter tables on Routes 1–4. Every original resident stays available in all seasons and retains at least one original slot. Native slot levels and the encounter rate of 21 remain in place. Original residents account for 70% of ordinary grass encounters, with two all-day visitors at 20% and 10%. Fishing, Surf, and neighboring areas retain their existing tables.

| Route | Season | 20% visitor | 10% visitor |
|---|---|---|---|
| 1 | Spring | Pawmi | Hoothoot |
| 1 | Summer | Pikipek | Yungoos |
| 1 | Autumn | Purrloin | Glameow |
| 1 | Winter | Cubchoo | Munchlax |
| 2 | Spring | Spinarak | Cottonee |
| 2 | Summer | Grubbin | Burmy |
| 2 | Autumn | Karrablast | Shelmet |
| 2 | Winter | Silcoon | Joltik |
| 3 | Spring | Mareep | Tandemaus |
| 3 | Summer | Stufful | Cubone |
| 3 | Autumn | Spoink | Munna |
| 3 | Winter | Swinub | Vanillite |
| 4 | Spring | Diglett | Roggenrola |
| 4 | Summer | Nacli | Nosepass |
| 4 | Autumn | Mudbray | Drilbur |
| 4 | Winter | Geodude | Onix |

## Kanto grass and coastal expansion (v0.0.87)

Grass on Routes 6–18 and Route 21 North gains two visitors per season, for 112 distinct additions. Every original grass resident stays available at its native slot levels and encounter rate. The residents occupy 70% of each seasonal table, with visitors at 20% and 10%. Route 21 North retains Tangela at 70%. Route 17 uses the Cycling Road’s existing encounter grass. Route 21 South has Surf encounters.

Surf on Routes 19–20 and both halves of Route 21 gains 32 distinct visitors. Tentacool stays available at 65%, and the visitors occupy 30% and 5%. Native levels and encounter rate 2 remain in place. The grass and Surf encounter lists use the committed season and apply all day.

### Grass

| Route | Season | 20% visitor | 10% visitor |
|---|---|---|---|
| 6 | Spring | Starly | Happiny |
| 6 | Summer | Bidoof | Dedenne |
| 6 | Autumn | Furret | Purugly |
| 6 | Winter | Dubwool | Smoochum |
| 7 | Spring | Fidough | Spritzee |
| 7 | Summer | Skitty | Komala |
| 7 | Autumn | Perrserker | Thievul |
| 7 | Winter | Cinccino | Slurpuff |
| 8 | Spring | Maschiff | Mime Jr. |
| 8 | Summer | Litleo | Chatot |
| 8 | Autumn | Liepard | Murkrow |
| 8 | Winter | Persian | Jynx |
| 9 | Spring | Rhyhorn | Gligar |
| 9 | Summer | Aron | Klawf |
| 9 | Autumn | Tinkatink | Durant |
| 9 | Winter | Boldore | Glalie |
| 10 | Spring | Magnemite | Charjabug |
| 10 | Summer | Luxio | Togedemaru |
| 10 | Autumn | Klink | Klang |
| 10 | Winter | Elekid | Magneton |
| 11 | Spring | Makuhita | Nidorino |
| 11 | Summer | Grafaiai | Zebstrika |
| 11 | Autumn | Hypno | Stunky |
| 11 | Winter | Delibird | Granbull |
| 12 | Spring | Gossifleur | Flabebe |
| 12 | Summer | Tadbulb | Masquerain |
| 12 | Autumn | Amoonguss | Toedscruel |
| 12 | Winter | Skiploom | Piloswine |
| 13 | Spring | Dolliv | Butterfree |
| 13 | Summer | Leavanny | Ribombee |
| 13 | Autumn | Weepinbell | Ariados |
| 13 | Winter | Eldegoss | Frosmoth |
| 14 | Spring | Breloom | Ledian |
| 14 | Summer | Venomoth | Galvantula |
| 14 | Autumn | Shiinotic | Hattrem |
| 14 | Winter | Forretress | Ferroseed |
| 15 | Spring | Swadloon | Comfey |
| 15 | Summer | Sunflora | Vileplume |
| 15 | Autumn | Scyther | Pinsir |
| 15 | Winter | Lilligant | Whimsicott |
| 16 | Spring | Tranquill | Heliolisk |
| 16 | Summer | Cyclizar | Fletchinder |
| 16 | Autumn | Corvisquire | Pawniard |
| 16 | Winter | Linoone | Weavile |
| 17 | Spring | Herdier | Gogoat |
| 17 | Summer | Krokorok | Scrafty |
| 17 | Autumn | Sandaconda | Varoom |
| 17 | Winter | Dodrio | Orthworm |
| 18 | Spring | Swablu | Audino |
| 18 | Summer | Staravia | Talonflame |
| 18 | Autumn | Slakoth | Bewear |
| 18 | Winter | Greedent | Noctowl |
| 21 North | Spring | Budew | Roselia |
| 21 North | Summer | Bellossom | Lurantis |
| 21 North | Autumn | Tangrowth | Maractus |
| 21 North | Winter | Abomasnow | Glaceon |

### Surf

| Route | Season | 30% visitor | 5% visitor |
|---|---|---|---|
| 19 | Spring | Mantyke | Staryu |
| 19 | Summer | Alomomola | Corsola |
| 19 | Autumn | Clamperl | Remoraid |
| 19 | Winter | Seel | Chinchou |
| 20 | Spring | Shellder | Horsea |
| 20 | Summer | Clauncher | Binacle |
| 20 | Autumn | Inkay | Frillish |
| 20 | Winter | Spheal | Pincurchin |
| 21 North | Spring | Wingull | Finneon |
| 21 North | Summer | Buizel | Chewtle |
| 21 North | Autumn | Shellos | Cramorant |
| 21 North | Winter | Slowpoke | Qwilfish |
| 21 South | Spring | Wailmer | Dewpider |
| 21 South | Summer | Mantine | Bruxish |
| 21 South | Autumn | Corphish | Mareanie |
| 21 South | Winter | Relicanth | Dewgong |
