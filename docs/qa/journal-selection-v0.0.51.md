# Pause-menu and journal selection — v0.0.51

The owner requested one Adventure Log on the first pause-menu page, removal of its duplicate from the second, and an obvious hovered quest. The second-page builder now adds only Quest Log, Achievements and Exit. The first-page builders and action enum/callback IDs remain intact.

The shared journal list uses the existing dark plum palette entry 8, cream foreground 1 and shadow 0 for the selected row. Its text background matches the band so text printing cannot erase the selection. A four-column cream pointer occupies x=8–11, distinct from the existing checkbox at x=13–20. The band fits x=7–235 and the existing sixteen-pixel row spacing. Titles and claimed markers share the correct selected colors. No new palette, tile, window or persistent RAM allocation was added.

## Verification

- All **45 executable project-check blocks passed** locally, including existing save-compatibility, approved art, animation, family palettes and seasonal checks. [Local check/build receipts](journal-selection-v0.0.51-local.json).
- The compiled real pause-menu builders were tested across all sixteen unlock combinations: exactly one Adventure Log on page one; exactly Quest Log, Achievements and Exit on page two. Wrapping, scrolling, both page-arrow directions, one-through-eight-row footer clearance and tile allocations passed.
- A new host harness compiled the actual journal backend/catalogue, renderer and input task. It measured actual native font widths, checked all visible title bounds, one selected band/pointer, matching text backgrounds, checkboxes and claimed markers. It exercised quest/achievement scrolling and wrapping, L/R paging, all filters and empty views, details/back selection, full-PC failure/retry, reward claims, fade/input guards and allocation failure/close lifecycle.
- GCC 13.2.1 native Debug and Release builds passed. Static EWRAM/IWRAM stayed at 254468/28376 bytes (Debug) and 254470/28328 (Release). ROM usage increased only 68/84 bytes from v0.0.50. Existing unrelated toolchain warnings remained.
- mGBA 0.10.2 captured **eight actual 240×160 screens** after controlled quest-flag setup. Emulated button input verified selected indices 0→1→7, scrolling top 2, details/back retaining index 7, side-filter reset, and Achievements with a claimed reward. Native pixel assertions verified band contrast, pointer separation and checkbox visibility. [Native receipts](journal-selection-v0.0.51-native.json), [reproducible harness](../../tools/legends/native_journal_qa/README.md), [phone-friendly lossless preview](journal-selection-v0.0.51.png).
- These controlled captures exercised actual native UI tasks, not natural overworld menu opening or historical battery-save reloads. Full historical-save fixtures and broader field playtests remain separate unfinished work.

## Save and asset review

Only menu composition, journal drawing, version text and documentation changed in game source. No serialized layouts, persistent action/quest/achievement IDs, catalogue ordering, save readers, initialization or migrations changed. Existing older-save paths remain intact, requiring no migration or extra release builds. No player/parent graphics, wardrobe, animation commands, seasons or reward rules changed.

## Publication

Local verification completed. Source CI, independent clean-base BPS round trips, patch commit and live Pages/download verification were pending at this source milestone; record their actual outcomes before claiming publication.
