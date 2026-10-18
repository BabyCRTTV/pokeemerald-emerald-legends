# Seasonal encounters — Routes 101–104 preview

**Model: GPT-6 | Approach: preserve native residents/levels and resolve every dependent land-table consumer through the committed season.**

Status: proposed v0.0.63 on a draft preview branch. The owner requested an actual-game preview before publication; approval and merge remain pending. The public release stays v0.0.62.

## Pilot rules

- Grass encounters on Routes 101, 102, 103 and 104 (both halves). Water, fishing, Rock Smash, hidden-only tables and other maps retain their published data.
- Original resident species stay available in every season and collectively occupy 70% of normal grass encounters. Two visitors occupy 20% and 10%; the existing twelve-slot weights, per-slot levels and encounter rate 20 are retained. These are base odds before native Lures or attraction abilities apply.
- Selections span Generations 1–9, including native seasonal/regional forms. Early routes use unevolved, ordinary species; no legendary, mythical, paradox or Da Bug encounters were added.
- This pilot applies all day; native time-of-day encounter support is currently disabled. No new nocturnal restrictions were introduced.
- Read the committed active season used by the world. A pending clock/playtime change waits for the existing safe transition. No new option, variable, save field, encounter roll, quest or achievement ID was added.
- Ordinary walking, Sweet Scent, local-mon helpers, optional overworld encounters, DexNav lists/levels/completion/hunts, Match Call hints and Pokédex habitat maps use the same land resolver. Outbreaks, roamers and Frontier tables retain native priority.

## Proposed visitors

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

## DexNav silhouettes

Unseen route entries use the actual native animated party icon with all nontransparent colors mapped to a separate black OBJ palette. Known icons retain their original shared palettes and animation. Empty slots retain the native X. Names, types, search eligibility, seen/caught flags and detector-mode selection stay unchanged. Locked hidden-only entries also show silhouettes rather than question marks. No icon artwork is replaced.

## Verification / approval

Project checks, both native Debug/Release builds and independent clean-base BPS round trips passed. Nineteen controlled native mGBA cases passed, covering all sixteen route/season tables, both halves of Route 104, 4,864 wild creations, native icon frames/palettes, unseen selection rejection and protected-state checks. All 38 native captures were visually reviewed. [Evidence and limits](../qa/seasonal-encounters-v0.0.63.md) · [Native receipt](../qa/seasonal-encounters-v0.0.63-native.json) · [Silhouette preview](../qa/dexnav-silhouettes-v0.0.63-preview.png).

These controlled Debug fixtures do not establish natural progression, a full DexNav hunt, historical-save migration, Release interaction or Pizza Boy coverage. Publication remains pending the owner's preview approval; the public game stays v0.0.62.
