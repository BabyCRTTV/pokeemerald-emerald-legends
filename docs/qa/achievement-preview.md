# Achievement expansion and notices — unpublished preview

Production remains **v0.0.51**. The owner explicitly requested a preview before publication. This branch is a review checkpoint; do not merge, update Pages/downloads or publish patches until the owner approves the appearance. The intended next release is v0.0.52, with normal version/site/changelog synchronization and native clean-base BPS verification still required at publication.

## Implemented

- Appended fifteen definitions as stable IDs **80–94**, bringing the catalogue to **95**. Added Rydel’s Rider, Weather Watch, See the Unseen, Deep-Sea Salvage, Thunderwing Witness, Frostwing Witness, Emberwing Witness, Sleeping Giant, Island Explorer, A Familiar Shadow, Homeward Bound, Trailblazer (100000 steps), Hatchery Master (50 eggs), Evolution Master (50 evolutions), and Dex Collection 300. Existing IDs 0–79 and their rewards are pinned unchanged.
- Kept the existing manual claim flow: open Achievements, select an unlocked entry, open Details, then press A to claim. No reward is deposited on unlock. Native AddPCItem success commits the claim once; full storage retains it for retry. Added a three-second detail-panel popup saying **REWARD CLAIMED! / Sent to PC ITEM STORAGE.** before returning to the claimed status text.
- Added a compact 144×32 native-font panel at screen (8,8), with the unlock heading and exact achievement title. It lasts 180 field frames, clears itself, and leaves a twenty-frame gap between queued notices. The player keeps moving; the feature changes no input, script locks, field scrolling, weather palettes or player sprites.
- Flag transitions, stat thresholds and newly caught Pokédex flags queue unlocks. Return-to-field refresh includes milestones earned in link/trade screens. Notices wait through fades, scripts, locked controls, menus, battles, Union Room/link sessions and location banners. Interrupted notices resume; window-allocation failure retries. Field-window cleanup and location-popup creation remove the transient panel safely.

## Compatibility and performance

The serialized journal remains version 1 and exactly **36 bytes**, with earned/claimed offsets 12/24 and the existing 96-bit capacity. No capacity, layout, persistent IDs, old readers or initialization signatures changed. Older saves preserve the first eighty earned/claimed bits. New goals use existing flags/stats/Dex data; already completed goals backfill quietly, remain unclaimed, and never auto-grant berries or flood Continue with old unlock banners. Reserved slot 95 remains available; exceeding 96 requires a separate compatibility design.

Only 24 bytes of static EWRAM were added. The panel allocates 2304 bytes temporarily while visible. Its BG0 tiles occupy 0x2C0–0x307, above the existing field help window (ending before 0x2C0), pause windows and standard text/frame tiles. It reuses field palette 15; no new per-frame progress scan, palette, task, save migration or client patching step was introduced.

## Verification and preview

- Native GCC 13.2.1 Debug and Release builds passed. Debug EWRAM/IWRAM: 254492/28376 bytes. Release: 254494/28328. [Native receipts and hashes](achievement-preview-native.json).
- All **46 executable project checks passed locally**, including the existing approved-art, animation, parent-palette, season and save suites. [Check receipts](achievement-preview-checks.json).
- Backend tests pinned the original eighty definitions and journal layout; exercised all fifteen new thresholds, one-time notices, old-save quiet backfill, repeated initialization, manual claims, full-PC retries and duplicate-claim prevention. Renderer tests covered all 95 titles, selected-row colors/navigation and success-popup expiration. All titles fit the compact field panel with native font widths.
- Notice lifecycle tests compiled the actual C and checked every deferral gate, allocation failure, interruption/resume, all queued notices, lifetime/gap and cleanup. They provide no lock/input setters, ensuring the notice cannot consume gameplay controls.
- Controlled **mGBA 0.10.2** setup entered an actual Oldale Town field scene. The real FlagSet hook unlocked new ID 80; the new native field code displayed its title while emulated movement changed the saved player position. Native window-state assertions verified visibility and automatic dismissal. Actual journal tasks navigated all 95 entries and manually claimed ID 80; the claimed save bit changed only after the claim. The three-second confirmation and later claimed status were captured.
- [Phone-friendly PNG](achievement-preview.png) and [animated native field preview](achievement-unlock-preview.gif) were rendered from actual emulator video; scene setup was diagnostic, not an ordinary story playthrough. No full ROM or BPS was distributed. General story playtests and historical battery-save matrices remain outside this preview.

## Approval and next steps

Await owner feedback on the unlock notice and claim popup. On approval, apply any requested refinements, advance VERSION and all matching release locations to v0.0.52, move the three Unreleased entries into the dated release sections, verify remote checks and both native/BPS round trips, then publish and verify Pages/downloads. Keep v0.0.51 available until that release passes its gates.
