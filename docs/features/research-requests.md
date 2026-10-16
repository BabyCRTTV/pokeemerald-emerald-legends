# Birch and Devon research requests — v0.0.59

Published and verified. [Release verification](../qa/research-v0.0.59-public.json).

The original six Birch requests remain available after the Pokédex, with their original IDs, objectives and rewards. Twelve additional Birch studies and twelve Devon contracts open through story progress. Early dialogue branches introduce Birch's work during his first calm lab conversation and Devon's research after the letter/PokéNav introduction; declining the explanation never blocks the main story. Players with existing saves can use the new conversations immediately when the relevant story gates are met.

Talk to Birch for **Field Requests**, or Mr. Stone on Devon's third floor for **Research Contracts**. Birch has Nearby Requests, Hoenn Surveys and Advanced Studies; Devon has Field Contracts and Special Projects. Each list keeps six request rows plus Back. `Later:` identifies locked work and selecting it explains the requirement; `Done:` identifies permanent completion. Objectives, hints and rewards appear before acceptance.

Only one research request can be active across both patrons. Main-story and other side quests continue normally. Finish/report or abandon with the request's own researcher before taking another. Abandonment requires confirmation, consumes nothing and returns the request to the list; habitat notes reset. Existing caught records still count. No Pokémon are ever removed. An existing tracked quest stays pinned; otherwise the accepted request is tracked automatically on SIDE.

All one-time rewards go to PC Item Storage. Full storage leaves the report and samples pending; the original Berry Samples request takes three Oran Berries only when the reward fits. Neither abandonment nor repeated conversation can duplicate rewards. The native Lucky Egg, Master Ball and story gifts retain priority/availability.

## Additional Birch studies

| Request | Unlock | Objective | PC reward |
| --- | --- | --- | --- |
| Granite Cave Life | Earn the STONE BADGE. | Visit GRANITE CAVE with a ROCK-type partner in your party. | 3 GREAT BALLS |
| Tidal Pool Records | Earn the KNUCKLE BADGE. | Record TENTACOOL and MAGIKARP as caught in your POKéDEX. | 3 DIVE BALLS |
| Meadow Sparks | Earn the DYNAMO BADGE. | Visit ROUTE 110 with an ELECTRIC-type partner in your party. | 3 QUICK BALLS |
| Dryland Partners | Earn the HEAT BADGE. | Visit ROUTE 111 with a GROUND-type partner in your party. | 3 NEST BALLS |
| Riverbank Survey | Earn the BALANCE BADGE. | Visit ROUTE 119 with a GRASS-type partner in your party. | 3 NET BALLS |
| Weather Partners | Help the WEATHER INSTITUTE and receive CASTFORM. | Visit ROUTE 119 with CASTFORM in your party. | 1 DAMP ROCK |
| Canopy Travelers | Earn the FEATHER BADGE. | Visit ROUTE 120 with a FLYING-type partner in your party. | 3 REPEAT BALLS |
| Quiet Mountain | Reach LILYCOVE CITY. | Visit the exterior of MT. PYRE with a GHOST-type partner. | 1 CLEANSE TAG |
| Offshore Partners | Earn the MIND BADGE. | Visit ROUTE 124 with a WATER-type partner in your party. | 3 DIVE BALLS |
| Shoal Cave Voices | Help STEVEN at the SPACE CENTER. | Visit the cave entrance with an ICE-type partner. | 3 HEAL BALLS |
| Peaceful Waters | Resolve the crisis in SOOTOPOLIS. | Visit SOOTOPOLIS CITY with a WATER-type partner. | 3 LUXURY BALLS |
| Hoenn Field Atlas | Become CHAMPION and finish the other 17 BIRCH requests. | Record at least 60 HOENN species as caught, then report to me. | 3 RARE CANDIES |

## Devon contracts

| Request | Unlock | Objective | PC reward |
| --- | --- | --- | --- |
| Tunnel Acoustics | Meet MR. STONE and receive the POKéNAV. | Visit RUSTURF TUNNEL with WHISMUR in your party. | 3 GREAT BALLS |
| Steel Under Stone | Deliver the LETTER to STEVEN. | Visit GRANITE CAVE with a STEEL-type partner. | 1 METAL COAT |
| Harbor Field Test | Deliver the DEVON GOODS to CAPT. STERN. | Visit ROUTE 109 with a WATER-type partner. | 3 NET BALLS |
| Current Conductors | Earn the DYNAMO BADGE. | Show me a party POKéMON that knows THUNDER WAVE. | 1 MAGNET |
| Heatproof Materials | Earn the HEAT BADGE. | Visit FIERY PATH with a FIRE-type partner. | 1 CHARCOAL |
| Working Waterways | Earn the BALANCE BADGE. | Visit ROUTE 118 with a WATER-type partner. | 3 DIVE BALLS |
| Rain Instruments | Help the WEATHER INSTITUTE and receive CASTFORM. | Visit ROUTE 119 with CASTFORM in your party. | 1 SMOOTH ROCK |
| Flight Recorder | Earn the FEATHER BADGE. | Show me a party POKéMON that knows FLY. | 1 SHARP BEAK |
| Power Components | Earn the FEATHER BADGE. | Record MAGNEMITE and VOLTORB as caught in your POKéDEX. | 1 THUNDER STONE |
| Orbital Telemetry | Help STEVEN at the SPACE CENTER. | Visit MOSSDEEP CITY with a PSYCHIC-type partner. | 1 PP UP |
| Pressure Recorder | Receive DIVE from STEVEN. | Visit UNDERWATER on ROUTE 124 with a WATER-type partner. | 1 PP MAX |
| Devon Master Project | Become CHAMPION and finish the other 11 DEVON contracts. | Show me at least 6 different types across your party. | 1 MASTER BALL |

Devon's twelfth contract, Devon Master Project, requires Champion status and all eleven earlier Devon completions. It asks for six distinct types across the party (both types count; Eggs do not). Reporting it successfully grants exactly one Master Ball. Birch's atlas similarly requires his seventeen earlier reports and Champion status.

## Save continuity and expansion

Request IDs 0–5 and quest IDs 33–38 preserve the original v0.0.58 work. New request IDs 6–29 append quest IDs 39–62. All older 39 quest entries and all 95 achievements retain their meaning and layout. The 36-byte journal, native save structures, sector readers and packed storage remain unchanged.

The v1 `0xB7` state remains readable without touching saves or the new words. At the first successful state write, a valid v1 selection, completion bits and habitat notes are retained, the new high completion word are initialized to zero, and the signature becomes `0xB8`. Invalid older words read as no request, with initialization only on accepting work. Full-storage submission does not migrate or consume anything. The verified-unused Route 127 var (0x407A, including its FireRed alias) stores completion bits 16–31. Because only one request is active, v2 stores its observation as a boolean in the existing note word; v1 note bits convert without losing the observation. The Seafoam entry and Safari variables remain untouched. Future expansion beyond the current 30 requests must preserve stable IDs and the bounded 32-bit format; it must add tested storage rather than shift by 32 or renumber published work.

The catalogue's engine data is in `src/legends_field_requests.c`; narrative flow is in `data/scripts/legends_field_requests.inc`. The JSON companion records the 24 new entries for documentation. Existing art, collision, map geometry, wardrobe, followers and seasonal behavior were preserved.
