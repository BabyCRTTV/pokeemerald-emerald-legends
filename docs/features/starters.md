# Starter sets and rival progression

Added in v0.0.19; shared by Release and Debug.

Open Options, use NEXT PAGE + A (or L/R) to reach **Adventure 3/3**, and edit
**STARTERS** with Left/Right. GEN 3 is the default. B saves and exits.
Title-screen choices carry into New Game. You can also change this setting before
opening the Route 101 rescue bag. Once the bag opens, that save's trio and rival
lineage are fixed; subsequent Options edits are preferences for a future New Game.

| Choice | Left ball | Middle ball | Right ball |
| --- | --- | --- | --- |
| GEN 1 | Bulbasaur | Charmander | Squirtle |
| GEN 2 | Chikorita | Cyndaquil | Totodile |
| GEN 3 | Treecko | Torchic | Mudkip |
| GEN 4 | Turtwig | Chimchar | Piplup |
| GEN 5 | Snivy | Tepig | Oshawott |
| GEN 6 | Chespin | Fennekin | Froakie |
| GEN 7 | Rowlet | Litten | Popplio |
| GEN 8 | Grookey | Scorbunny | Sobble |
| GEN 9 | Sprigatito | Fuecoco | Quaxly |
| SPECIAL | Happiny | Wattrel | Mankey |
| RANDOM | Random base Pokémon | Random base Pokémon | Random base Pokémon |

Random selects three distinct, enabled, unevolved Pokémon with an enabled evolution
from across the National Pokédex. Baby Pokémon qualify; evolved Pokémon,
single-stage species, eggs and alternate forms are excluded. Each eligible species
has equal inclusion odds. This does not impose a type triangle or strength balance.
The three species are rolled once when the bag opens, saved immediately, and stay
stable when moving the cursor, declining confirmation, or saving/reloading.
Starting another New Game clears the old trio and rolls again.

For generation sets, the native grass/fire/water slot determines the rival's
counter: grass faces fire, fire faces water, and water faces grass, all from the
selected generation. Special and Random give the rival normal Unovan **Zorua**
regardless of your selected ball, evolving into **Zoroark at level 30** (Route 119
and Lilycove). Generation starters evolve at their native level thresholds, so
some reach their final stage earlier than others. Default Gen 3 retains exact
native Emerald teams, including their original evolutionary stages.

Both May and Brendan are covered in all 30 native starter-dependent teams,
including the optional Rustboro battle. Levels, IVs, other team members, rewards
and story scripts are preserved. Replacements use the selected species' native
current-level learnset and ability rather than inheriting Hoenn-starter moves.
The opening rescue still uses level-2 Stunky; the player receives a level-5 starter.
Existing saves retain their Gen 3 starter/rival lineage and party.

## Implementation

`legends_starters.c` owns generation tables, reservoir sampling, rescue locking and
rival substitutions. The native starter screen still draws previews, names,
categories and cries; `GetStarterPokemon` resolves each slot through this module.
`VAR_STARTER_MON` keeps its existing 0/1/2 slot meaning, preserving all story branches.
The locked set is separate from the next-game preference.

Unused permanent vars store preference (`0x4083`), locked mode (`0x408B`) and
random species (`0x4091`, `0x409B`, `0x409D`). Modes are encoded as setting + 1;
zero/invalid preferences default to Gen 3. An existing rescued save with no locked
mode also uses Gen 3. The title Options bridge stages only the preference, never
an old game's trio or progress. Save-block layouts remain unchanged.

Random eligibility marks incoming evolution edges once in a temporary species
bitset and uses the expansion's native species/form/evolution metadata and RNG.
There is no repeated full-dex pre-evolution scan or Pokémon-art duplication.
Rival generation copies each TrainerMon template, substitutes only the native
Hoenn starter member in May/Brendan Rival teams, and then uses the expansion's
normal trainer generator. Trainer definitions are not modified in place.

Host tests exercise all modes, save locking, invalid indices, stable distinct
random trios and all 30 rival teams against source evolution metadata. Actions
also compiles both distributions and verifies BPS reconstruction.

## Emulator QA

- Choose each generation in title Options, start New Game, and inspect all three
  balls' names, previews and cries. Confirm level 5 and the selected species.
- Choose Special; inspect Happiny/Wattrel/Mankey and Zorua in the first rival battle.
- Choose Random; browse, decline confirmation and return. Verify no reroll or
  duplicates, save/reload after the rescue, and check the same rival lineage.
- Confirm Zorua before level 30 and Zoroark at Route 119/Lilycove for both genders.
- Change the Options preference after the rescue; the established rival must stay
  unchanged. Then start New Game and confirm the newly chosen setting applies.
- Load a pre-v0.0.19 save and verify original party and Gen 3 rival teams.
