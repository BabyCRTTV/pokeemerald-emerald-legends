# Wyrmtide Isle

Unshipped addition to the v0.0.70 source. The owner requested another design review on 22 October; public downloads are unchanged. Uses existing native Emerald: Legends artwork. Preserve subsequent owner Porymap edits.

## Story and progression

After calming Regigigas and completing the existing Weather Institute report, eight safe outdoor steps trigger an unknown-number Pokenav call. Mr. Briney reveals himself and invites the player to a newly found island just west of Dewford. The call yields to existing higher-priority step events and never interrupts indoor/Safari/forced movement.

Briney's Dewford menu offers Wyrmtide Isle and keeps his native coastal routes when they are available. After his original NPC has left, a local expedition contact and boat appear at the same dock without changing any original travel-state flag. On S.S. Tidal he directs the player to Dewford. Briney always offers the return voyage from the island, including before its puzzle is solved.

Three weathered tablets refer to the hand that shaped the original three titans, the continent's mover standing among six companions, and a last heart hidden from the sun. The sealed entrance opens only with a non-egg Regigigas in the actual party; a fainted companion qualifies. Opening is permanent, so storing it afterward cannot strand the player.

Four distinct stair landings lead to the Heart: the Maker's Hall, a tidal stair, a memorial switchback and a final procession between sea-water basins. Their native stair warps work in both directions. There are no random encounters or forced Flash requirement. The last inscription describes dragon power sealed in an unfinished body. A sleeping Lv75 Regidrago waits on the dais; interaction asks whether to awaken it. Escaping/loss leaves it available, defeating it calms it and permits another challenge, and capture hides it permanently. Reporting to Briney after defeat or capture completes the appended journal quest, The Maker's Last Dream.

## Identity and save handling

- Appended six maps/layouts, a new map section after preserved MAPSEC_NONE, two menu IDs, two specials and quest ID 63. All published IDs keep their values.
- Seven audited native flags occupy 0x493–0x499, retaining their unused aliases. No native variable, serialized structure, sector, inventory or storage format changes.
- On older Dewford Continue saves, refresh only the two appended source NPC templates. Preserve all existing cached NPC templates/permanent movements. Defer spawning a contact or boat while the player's tile is occupied.
- Original shared map/tileset artwork is untouched. The shore sibling retains Dewford’s metatile prefix, every referenced pixel, native palm animation and day/night wiring. Eight cells add exact Cave inscription/column pixels in unused sibling slots and Cave’s native palette 6 in Dewford’s unused palette 6.
- The underground sibling retains all 414 original Cave definitions and reuses native Cave 0x396 for ordinary/warp stairs at 0x39F/0x39E. The exterior entrance uses the same pink-rock cells as Hoenn’s original Regi islands. No palette colors were authored or changed.
- The region-map sea cell west of Dewford gains a label without changing world-map pixel artwork.

`tools/legends/build_wyrmtide_maps.py` authored the new maps. Existing files are preserved by default. `--refresh-review` is an explicit map-authoring operation, never part of routine builds or releases. Later owner Porymap changes must be retained.

## Current environment review

The 22 October pass uses a single pink-rock headland, two slender native columns and a sheltered sandy landing with Dewford palms. Three low inscription ledges form short clue spurs. Proper three-cell-deep Sealed Chamber walls enclose four stair landings. Retaining banks guide actual movement through the stairs; the tidal gallery and last procession carry the sea beneath the island. A single final inscription, paired columns and seven worn stones frame the sleeping dragon.

[Current native gallery](../designs/wyrmtide/hoenn-review/Wyrmtide-Redesign.png), [source-tile island overview](../designs/wyrmtide/hoenn-review/Island-Layout.png), and [verification/limits](../qa/wyrmtide-hoenn-review.json). The earlier [Astra gallery](../designs/wyrmtide/astra-redesign/Wyrmtide-Redesign.png) remains as design history. This revision is pending owner visual review.

Source inspiration: [wally-217’s Hoenn map remake](https://www.reddit.com/r/PokemonROMhacks/comments/10ul67l/hoenn_now_with_more_water/) and [redscarewiggler’s Emerald EXP map discussion](https://www.reddit.com/r/PokemonROMhacks/comments/utl9aj/some_beta_maps_for_our_emerald_exp_project/). These informed coherent terrain and small coastal discoveries; no external art or map data was imported. [Porymap’s metatile documentation](https://huderlem.github.io/porymap/manual/tileset-editor.html) describes the layered tile/behavior model used for the local cells.

For manual editing, the island uses `gTileset_LegendsWyrmtideShore` (new cells 0x37B–0x382); all underground maps use `gTileset_LegendsWyrmtideCave` (warp 0x39E, ordinary stair 0x39F). Existing files are preserved by the generator unless the explicit authoring override is supplied. Do not regenerate over future owner edits.
