# Kanto postgame — Wing Survey

## Playable in v0.0.28

Become Hoenn Champion, get the Invite Ticket in Lilycove Harbor, and use the existing Kanto ferry or northern Route 124 Surf passage. Both passages retain the established return routes and Emerald field-move requirements.

Visit Oak's field aide in Vermilion Fan Club. The aide introduces the Wing Survey: investigate reports of lightning, frost and fiery wings, comparing Kanto's observations with Birch's records of Hoenn's resolved weather crisis. This is an investigation, not proof that the Hoenn crisis caused the sightings. No new evil team replaces Emerald's story.

Complete Lt. Surge and Koga's visiting challenges in either order. Surge reports unusual readings near the Power Plant; Koga reports cold winds at Seafoam and a third bird sighting. Return to the aide to complete the first report and hear the tentative Mew lead. The aide explicitly identifies the next expedition as future development content. There are no new legendary battles in this version.

The new road loop is Vermilion → Route 6 → Saffron → Route 7 → Celadon → Routes 16–18 → Fuchsia → Routes 15–11 via Lavender → Vermilion, with Route 8 connecting Lavender and Saffron. Walking and normal Emerald bikes work on the western road; the old FRLG forced Cycling Road state is not imported. Wild species distributions reuse the upstream FireRed tables with postgame levels (47–54), on Routes 6–8 and 11–19. Six optional trainers occupy Routes 6–8 and 16–18. Native Cut obstacles retain ordinary Emerald progression.

Lavender, Fuchsia, Saffron and Celadon Centers have nurses. Their upper floors and unused city interiors retain the existing development closures. The remaining Gyms and unbuilt northern/western regions are not implied to be complete.

## Gym contract

An entrance guide explains the choice at each entry before the Leader fight. YES chooses Champion; NO chooses Standard. Talking to the guide changes it until victory. The Leader separately asks whether to battle, so declining is safe. The player party is never scaled or replaced.

| Leader | Current state | Standard | Champion | Record |
| --- | --- | --- | --- | --- |
| Lt. Surge | Playable, Vermilion | 4 Pokemon, 52–56 | 6 Pokemon, 72–76 | `FLAG_LEGENDS_KANTO_SURGE_WON` |
| Koga | Playable, Fuchsia | 4 Pokemon, 56–60 | 6 Pokemon, 76–80 | `FLAG_LEGENDS_KANTO_KOGA_WON` |
| Brock | Planned, Pewter | Target 50–54 | Target 70–74 | Reserved independent flag |
| Misty | Planned, Cerulean | Target 52–56 | Target 72–76 | Reserved independent flag |
| Erika | Planned, Celadon | Target 54–58 | Target 74–78 | Reserved independent flag |
| Sabrina | Planned, Saffron | Target 58–62 | Target 78–82 | Reserved independent flag |
| Blaine | Planned, Cinnabar | Target 60–64 | Target 80–84 | Reserved independent flag |
| Viridian Leader | Planned; Blue as acting Leader | Target 62–66 | Target 82–86 | Reserved independent flag |

Targets for unimplemented teams are design notes, not shipped balance promises. Blue's proposed acting role avoids reversing the original Rocket/Giovanni outcome; establish it with dialogue when Viridian is implemented. Kanto's chronology is this hack's original continuation, not a claim that game and anime timelines are identical.

**Only one victory per Leader, per save.** Winning either mode completes both permanently. Standard and Champion teams have different trainer IDs but share the Gym completion flag. Losing blackouts out of the native trainer script before the victory command; retry and reselection remain available. No mode grants extra story progress, rewards or permission to fight a second team. Hoenn's badges and their field permissions are untouched. A future eighth-record check will use all eight dedicated flags, not trainer ID counts or Emerald badges.

Surge's electrical barrier is opened by an on-load script for this visiting challenge; the familiar room and trash cans remain. Koga keeps the native invisible-wall geometry. Neither Gym imports FRLG badge, TM, Fame Checker or NPC story state.

## Chapter plan

### 1. A Champion abroad — implemented opening

Oak's aide asks for observations, not capture trophies. Introduce the survey at the Fan Club, where local Pokemon enthusiasts naturally share sightings. Surge and Koga demonstrate that both difficulty choices count equally and that the player's Hoenn experience matters. First report: three habitats, tentative bird identifications, an unexplained mimic cry and a tiny pink hair. The final detail is a clue rather than proof of Mew.

### 2. The Kanto circuit — next playable expansion

Populate Celadon and Saffron beyond their Centers, implement Erika/Sabrina using the same per-Gym contract, and extend northern routes toward Cerulean/Pewter for Misty/Brock. Trainers, habitat encounters, services and travel signs should arrive with each road, rather than adding more empty territory indefinitely.

Each Leader offers a distinct observation: Misty notes changes in currents, Brock checks rockfalls without attributing every disturbance to a legend, Erika finds stressed vegetation near roosts, Sabrina senses an unfamiliar but curious presence. Birch and Oak compare measurements; their conclusions remain tentative until the player surveys the sites. Use established characters and brief local conversations, rather than a new named rival or villain cast.

Collecting the early records earns access to the first habitat expedition; completing Standard is as valid as Champion. The eventual quest should let a player reach the sites in a clear order while the Gym circuit remains flexible. Provide a journal/status NPC summarizing missing records before increasing complexity.

### 3. Three habitats — future encounters

- **Zapdos, Power Plant:** restore safe access and inspect damaged equipment. Route trainers and workers connect Surge's reading to a bird protecting its roost. Use native Power Plant maps, electricity-themed puzzles and a single native legendary encounter. Gym difficulty must not silently scale the wild encounter.
- **Articuno, Seafoam Islands:** a stranded survey boat and changing currents lead to the caves. Keep recognizable boulder/current puzzles and native Surf/Strength logic. Articuno's presence should explain the frost without casting it as malicious.
- **Moltres, Mt. Ember:** Blaine's volcanic observations unlock a later Sevii expedition, reusing the upstream FireRed habitat. The inland sighting in the opening can be a migrating bird rather than a contradictory permanent Kanto roost. Add Sevii map browsing only when that expedition is playable.

The anime's sense of awe around powerful elemental birds can inform tone; do not import its Orange Islands catastrophe, Ash's role, or film-specific artifacts as established game events. The survey is a new game story, not an adaptation. Hoenn's Rayquaza resolution remains intact, and the birds need not be responsible for another global disaster.

For each encounter, plan a dedicated approach scene and native caught/defeated outcome handling. Defeated-but-uncaught legends need an explicit recovery policy and clear player guidance. Survey completion should record observing/protecting the habitat; do not force capture to understand the story. Inspect existing upstream legendary respawn logic before allocating new states.

### 4. The elusive visitor — future Mew conclusion

After the eight-Gym circuit and bird surveys, Oak recognizes that one set of observations does not belong to any bird. The mimic cry and pink hair recur in small optional scenes. Mew is curious about the player's Pokemon, not an antagonist, a laboratory weapon or a guaranteed reward for choosing harder teams.

Birch and an old maritime record connect the visitor to **Faraway Island**, retaining Emerald's existing Mew habitat. Audit the existing Old Sea Map, Mew encounter/capture flags, puzzle and event-island travel before granting story access. Reuse that encounter instead of adding a second catchable Mew. Existing saves that already caught Mew must receive a completed/alternate scene rather than a duplicate spawn. The final voyage resolves the survey and connects the Kanto journey back to Hoenn.

Finish with a concise acknowledgement from Oak, Birch and the League. Preserve ordinary Emerald exploration, Battle Frontier and other postgame content. Any new final reward must be one-time and recover gracefully from a full Bag, using the existing project reward conventions.

## Implementation and saves

- `data/scripts/legends_kanto_challenge.inc`: self-contained Gym and survey scripts, included explicitly for Emerald from `data/event_scripts.s`.
- `src/data/trainers.party`: distinct Standard/Champion parties and six optional route trainers; uses the expansion's party parser and native Leader artwork.
- `data/legends_kanto_chapter1.json`: the 18 appended native-map imports and two active Gyms. The old foundation manifest remains a record of the earlier 30 imports.
- Gym completion bits `0x26E–0x275`: reserved once per named Leader, separate from all Hoenn badge and native FRLG states. Only Surge/Koga are set now.
- Survey started/report bits `0x276/0x277`. Reports check both Gym completion flags, so doing a Gym before meeting the aide still works.
- Saved choice vars `0x40B8`/`0x40BB`: 0 unset, 1 Standard, 2 Champion. Old saves default to unset. `VAR_TEMP_0` prevents the entrance trigger from repeating during that map visit; every doorway lane is covered. No SaveBlock resizing.
- PokeNav `displayRegion`: transient map-screen state. SELECT toggles Hoenn/Kanto after `FLAG_SYS_GAME_CLEAR`, including from zoomed views. Fade, native zoom reset and graphics reload run as a looped task. Cursor lookup follows the displayed map; player marker and Fly only apply to the actual region. Fly/wall/Pokedex screens initialize independently. Browsing the full Kanto map does not assert that every location is implemented.
- Connections back into Saffron point at the real Legends city with its proper offsets, replacing the FRLG dummy connection map. Gate warp slots are preserved; old Legends map IDs are append-only.

## Validation and manual playtest

Automated checks exercise actual event branches for both modes, decline/loss/retry, common victory records and reporting in either order; the map graph, NPC/entrance collision positions, encounters, trainer levels and native graphics are also checked. The C map-switch task is exercised with host stubs for its asynchronous services. CI separately compiles Debug/Release and verifies both BPS patches against an independently built, SHA-1-verified vanilla Emerald.

Static native layout renders were inspected for the two Gym rooms, Route 7 and the newly linked city approaches. This is not an emulator playtest. Before calling the chapter playtested:

1. On an existing Champion save, SELECT-switch from both zoom states in both regions. Move the cursor, zoom, switch repeatedly and return; verify names, city previews, help bar, player marker, exit/re-entry and current-region Fly. Check pre-Champion map behavior remains unchanged.
2. Walk each route/gate in both directions, including Route 6/Saffron, Route 7/Saffron, Route 8/Saffron, Route 16 gate and Route 18 gate. Enter/leave all four working Centers and heal an injured party. Check no inherited Cycling Road state leaks into Hoenn.
3. Enter each Gym through all three door lanes. Choose each mode on separate save copies, decline the battle, change modes, lose and retry. Win, leave/reload, and verify the other team remains unavailable. Check the other Gym's choice is independent.
4. Check Surge's barrier opens every load and Koga's maze leads to his original position. Battle teams need human balance testing; listed levels and script-path tests alone do not establish difficulty quality.
5. Start the survey before and after one/both victories. Complete them in both orders. Verify the report occurs once and the development endpoint is clearly stated.
6. Confirm existing ferry and Surf travel, invitation retention, respawn and return travel still work. Keep all commercial base ROMs and compiled ROMs private; publish only verified BPS patches/checksums.
