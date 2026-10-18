# Seasonal encounters — Routes 101–108

**Model: GPT-6 | Approach: preserve native residents/levels and resolve every dependent land-table consumer through the committed season.**

Status: published in v0.0.63. The reported DexNav icon sizing/centering issues were corrected and verified in actual mGBA captures; both live patches independently reconstructed the production ROMs.

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

The owner chose the next four numbered sea routes. Implementation is on the development branch; production and live patch verification must finish before declaring v0.0.64 published. These routes have no grass tables.

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

## DexNav silhouettes

Unseen route entries use the actual native animated party icon with all nontransparent colors mapped to a separate black OBJ palette. Known icons retain their original shared palettes and animation. Empty slots retain the native X. Names, types, search eligibility, seen/caught flags and detector-mode selection stay unchanged. Locked hidden-only entries also show silhouettes rather than question marks. No icon artwork is replaced. A DexNav-only presentation helper centers the combined bounds of both native poses and uniformly shrinks oversized icons to fit the existing columns. It never enlarges small species or edits shared party/battle/follower assets; both discovered and silhouette states use identical placement.

## Verification / approval

The owner approved the roster and silhouette approach, with a request to correct DexNav sizing/centering. Final source `4660dc53` passed project checks, 4,096 geometry cases, a shipped-C audit of all 1,809 native icon sheets and 35 controlled native mGBA cases (8,960 wild creations). All 54 captures were visually reviewed and panel containment was asserted. [Final correction evidence and release gate](../qa/dexnav-layout-v0.0.63.md) · [Native receipt](../qa/dexnav-layout-v0.0.63-native.json) · [Corrected preview](../qa/dexnav-layout-v0.0.63-preview.png).

PR and production Debug/Release builds, project checks, both BPS validations and native mGBA checks passed. [Live publication receipt](../qa/dexnav-layout-v0.0.63-public.json). Controlled Debug fixtures do not establish natural progression, a full DexNav hunt, historical-save migration, native Release interaction or Pizza Boy coverage. Original pre-correction evidence remains in the [first trial QA record](../qa/seasonal-encounters-v0.0.63.md).
