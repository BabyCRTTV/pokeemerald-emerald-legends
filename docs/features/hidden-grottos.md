# Hidden grotto encounters (unshipped review)

Each room holds one visible Pokémon. Inspect it to hear its cry and choose whether to battle. Capture or defeat empties that room and starts its own 4,500-step cooldown. The native overworld step counter is used, including running, cycling and Surf travel. Leaving, fleeing, losing, changing seasons or saving/loading keeps the active Pokémon’s full identity. Steps taken before resolving it do not bank toward a replacement.

A new visitor is selected once the cooldown has expired and the room is visited (or immediately while already inside, when its square is unoccupied). The current season is sampled then; it never rerolls an existing visitor. Each seasonal pool has weights 30/25/20/15/10%. Levels are uniformly selected within the listed range. Existing wild shiny settings apply once at generation.

| Grotto | Entrance | Levels |
| --- | --- | --- |
| Leafshade Hollow | Petalburg Woods | 8–12 |
| Stillwater Nook | Route 114 | 18–22 |
| Rainroot Hollow | Route 119 | 25–30 |

| Season | Leafshade | Stillwater | Rainroot |
| --- | --- | --- | --- |
| Spring | Riolu, Ralts, Eevee, Zorua, Bulbasaur | Gible, Carbink, Beldum, Deino, Mudkip | Goomy, Applin, Bagon, Dreepy, Chikorita |
| Summer | Larvesta, Fennekin, Eevee, Zorua, Snivy | Axew, Charcadet, Beldum, Dratini, Totodile | Jangmo O, Duraludon, Bagon, Goomy, Froakie |
| Autumn | Zorua, Phantump, Eevee, Riolu, Chespin | Dreepy, Sableye, Beldum, Deino, Fuecoco | Dreepy, Mimikyu, Bagon, Goomy, Rowlet |
| Winter | Vulpix, Snom, Eevee, Riolu, Piplup | Frigibax, Amaura, Beldum, Gible, Piplup | Frigibax, Duraludon, Bagon, Dratini, Popplio |

The canonical roster is `src/data/legends/grotto_encounters.json`. Its generator produces the engine C table and LegendsDex supplement together. The Grotto filter is available in both route and species views; the Encounter type selector also supports Grotto visitor. Item-ball scenery remains the approved inspectable prop; no item reward was added in this task.

Approved interiors and entrances are preserved. The sole requested scenery change replaces Route 119 cells `(26,103)` and `(27,103)` with the same plain cliff metatile `0x079` used immediately to their right. Collision and the access/return coordinates are unchanged.

Save design and compatibility: [save policy](../SAVE-COMPATIBILITY.md). Validation and remaining release gates: [QA](../qa/grotto-encounters.md).
