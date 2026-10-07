# Pokémon Emerald: Legends — Quality Assurance

Baseline: v0.0.8. Maintenance checks added in v0.0.8.1.

## Automated checks

- VERSION, canonical/Release/Debug changelogs, homepage, patcher, and in-game version labels stay synchronized.
- Source-level checks cover the Options page allocation, Legends EXP Share flags/save initialization, Rustboro Lucky Egg, and Birch National Dex / Champion rewards.
- Node regression tests cover browser BPS SourceRead, TargetRead, TargetCopy overlaps, source and patch CRC rejection, target CRC rejection, and stale ROM selection.
- Build workflow compiles both Debug and Release ROMs, verifies a freshly built clean Emerald base SHA-1, reapplies generated BPS patches, and byte-compares both results with compiled ROMs.
- No copyrighted full .gba images are committed or distributed.

## Manual emulator regression checklist (not yet verified)

- [ ] Start new Release and Debug saves and confirm only Debug exposes developer utilities.
- [ ] Open Options; switch General/Legends using L/R with normal controls and L=A mode, modify settings, save/reload, inspect borders and CANCEL.
- [ ] Continue an older save and confirm EXP Share initializes only once. Toggle OFF, save/reload, and confirm it stays OFF.
- [ ] Battle with participants, benched Pokémon, fainted Pokémon and Eggs with EXP Share ON/OFF and Lucky Egg; check resulting EXP.
- [ ] Use each of the eight badge-earned HM utilities without taught HMs, preserving terrain, story, follower and Regi-puzzle gates.
- [ ] Receive the Rustboro Lucky Egg exactly once after Steven's letter.
- [ ] Receive early National Pokédex; test Champion Rare Candy delivery to Bag, PC, and deferred state when both are full, including postgame saves.
- [ ] Patch Release and Debug on Android and desktop using a clean Emerald ROM; try switching files midway and rejecting wrong ROMs.

CI passing does not establish emulator gameplay correctness. Record emulator version, save state and observed outcome before checking a manual item off.

## v0.0.9 manual regressions (not yet verified)

- [ ] New game: Exp. Share is a Key Item immediately and USE changes Legends Options.
- [ ] Existing save with EXP SHARE OFF: receive item on continue without altering setting; no duplicate Key Items on reload.
- [ ] Before Birch's Pokédex: DexNav is hidden from Start menu.
- [ ] After Birch's Pokédex: DexNav appears and searches wild encounter slots.
- [ ] Existing save with Pokédex: DexNav appears immediately upon continue, detector mode works.
- [ ] Battle Pyramid temporary Bag is not modified by missing-item restoration.
