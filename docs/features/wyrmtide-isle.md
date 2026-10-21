# Wyrmtide Isle — story review

Unshipped addition to the v0.0.70 source, authored for visual review. Uses only existing native Emerald: Legends art. Public Release/Debug downloads are unchanged.

## Story and progression

After calming Regigigas and completing the existing Weather Institute report, eight safe outdoor steps trigger an unknown-number Pokenav call. Mr. Briney reveals himself and invites the player to a newly found island just west of Dewford. The call yields to existing higher-priority step events and never interrupts indoor/Safari/forced movement.

Briney's Dewford menu offers Wyrmtide Isle and keeps his native coastal routes when they are available. After his original NPC has left, a local expedition contact and boat appear at the same dock without changing any original travel-state flag. On S.S. Tidal he directs the player to Dewford. Briney always offers the return voyage from the island, including before its puzzle is solved.

Three weathered tablets refer to the hand that shaped the original three titans, the continent's mover standing among six companions, and a last heart hidden from the sun. The sealed entrance opens only with a non-egg Regigigas in the actual party; a fainted companion qualifies. Opening is permanent, so storing it afterward cannot strand the player.

Four switchback stair landings lead to the Heart. Their native stair warps work in both directions. There are no random encounters or forced Flash requirement. The last inscription describes dragon power sealed in an unfinished body. A sleeping Lv75 Regidrago waits on the dais; interaction asks whether to awaken it. Escaping/loss leaves it available, defeating it calms it and permits another challenge, and capture hides it permanently. Reporting to Briney after defeat or capture completes the appended journal quest, The Maker's Last Dream.

## Identity and save handling

- Appended six maps/layouts, a new map section after preserved MAPSEC_NONE, two menu IDs, two specials and quest ID 63. All published IDs keep their values.
- Seven audited native flags occupy 0x493–0x499, retaining their unused aliases. No native variable, serialized structure, sector, inventory or storage format changes.
- On older Dewford Continue saves, refresh only the two appended source NPC templates. Preserve all existing cached NPC templates/permanent movements. Defer spawning a contact or boat while the player's tile is occupied.
- Original maps/tileset binaries are untouched. One sibling Cave tileset copies the native prefix exactly and appends existing stair artwork with the native ladder behavior. The region-map sea cell west of Dewford gains a label without changing world-map pixel artwork.

`tools/legends/build_wyrmtide_maps.py` authored the new maps. Existing files are preserved by default. `--refresh-review` is an explicit authoring operation for this unshipped draft, never part of routine builds or releases. Later owner Porymap changes must be retained.

## Verification

`test/legends-wyrmtide.test.py` checks alias allocation, original IDs, old geometry, source collision/warp pairs and production C gates. `tools/legends/native_wyrmtide_qa/run.py` runs controlled fixtures in the compiled ROM through native mGBA, records real gameplay PNGs and tests affected interactions. The setup payload is private and deleted, never included in published ROMs. Controlled fixtures are not an authentic historical owner save or a full natural story playthrough.

Local Debug/Release compilation, full native interaction and controlled old-Dewford-cache flash repair passed; see [receipt and limits](../qa/wyrmtide-native.json). Project, full native mGBA and Release/Debug candidate patch workflows passed for source `7279100bcaed27904e83dcb8da69dba0c5ed6373` in [PR #89](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/89). Both candidate BPS patches independently decode against the supported clean base to ROMs exactly matching the local builds. [Patch receipt](../qa/wyrmtide-patches.json). New artwork is not generated for this quest; all gameplay preview frames must be actual native captures.
