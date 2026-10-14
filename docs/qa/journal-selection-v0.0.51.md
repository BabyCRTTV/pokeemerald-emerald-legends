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

- Source commit: [`da2a9572eecd3b9989a6f00f54bc514549e46de0`](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/commit/da2a9572eecd3b9989a6f00f54bc514549e46de0). [Project checks 38604169624](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38604169624) passed.
- [Native builds and independent BPS round trips 38604169555](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38604169555) passed. The vanilla base matched SHA1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`; Floating IPS independently applied both patches and compared each result byte-for-byte to its compiled ROM. Both CI target SHA256 values exactly matched the local builds in the receipts.
- Patch commit: [`ff8533bcee9ec19068eabb091ae89fd83bd4a7bc`](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/commit/ff8533bcee9ec19068eabb091ae89fd83bd4a7bc). [Pages 38605550314](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38605550314) succeeded; no stale deployment lock recurred. Active Pages completed before this evidence update was prepared.
- Both live public BPS URLs returned HTTP 200, matched the pinned manifest and local committed patch SHA256 values, passed supported source/target/patch CRC checks, and matched local native target hashes. The homepage, both changelog tabs, patcher HTML/JS and preview matched committed bytes. [Structured public receipts](journal-selection-v0.0.51-public.json).
- Release BPS: **17,428,639 bytes**, SHA256 `fe04fac104afdf9397a25e5c002eade133af3011b35256af91437cdff8489e23`. Debug BPS: **17,261,391 bytes**, SHA256 `398789aea9f6ec3213c73cad69f803865560f15354a9c5d5335761378fe6cf32`. They were 906/504 bytes smaller than v0.0.50; no material patch-size or routine verification-time increase was introduced.
