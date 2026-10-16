# Quest tracking — v0.0.57 release

Status: **published and verified**, through [PR #72](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/72). [Approved layout](quest-tracking-preview.png) · [Approved scrolling GIF](quest-tracking-scroll.gif) · [Build/native/public receipts](quest-tracking-v0.0.57-public.json).

## Approved result and compatibility

The owner approved publication on 15 October 2026: “Excellent, apply and publish if all is bug free.” Details A tracks/stops one visible unfinished quest; T and TRACKED identify it. Both ordinary pause pages show its next objective above clock/weather, with a 16-pixel right-menu gap. Long text pauses at each end, scrolls by single pixels and smoothly returns; the heading stays fixed, short text stays still and reopening resets the cycle. Existing menu/popup/special-layout exclusions remain intact.

Selection reuses reserved u16 offset 10 with signature 0xA700 and low-byte quest ID + 1 in the unchanged 36-byte version-1 journal. Zero payload means off; unsigned/invalid legacy values read as off without mutation. Existing readers, checksum, codec and achievement bits remain unchanged, and completion clears a recognized selection. Preserve quest IDs 0–32 and append future entries. No migration, approved artwork, wardrobe, season, story or reward changes were introduced. [Original design/save contract](quest-tracking-preview.md) · [Scroll implementation](quest-tracking-scroll.md).

Final review corrected the optional cache to `AllocZeroedUnchecked`: the checked allocator could stop the game before the intended NULL fallback. Focused actual-C failure/cleanup tests passed against the recoverable API. Cached wrapping and clipped whole-word 4bpp copies update only the 96×60 body. The RAM-only scratch window never installs a tilemap or uploads graphics, and resources are freed on close/failure.

## Verification and recovery

All 49 local project-check blocks passed, with focused pause-card/menu checks repeated after the allocator correction. PR and merged Actions passed all project checks, both builds and clean-base BPS round trips. Eleven test-reencoded PNGs had identical indexed pixels/palettes/geometry and were restored to original bytes. AGENTS.md was reviewed; no new durable rule was required.

Before interruption, final-version native Debug tests passed actual tracking, both pages, brief close/reopen input, help/Save exclusion and return, real flash persistence, next objective, completion and Safari suppression, preserving non-default appearance, bedroom colors and Winter on walkable floor. Unmodified Release loaded the controlled battery fixture through normal title/Continue and passed both pages, Details and stop without host RAM/callback writes; its short-card pixels matched Debug.

Oversized private fixtures also passed in both variants. Debug used the controlled callback fixture; a separate Release copy substituted only the objective pointer/text and used normal Continue/input without host RAM/callback writes. Each recorded 1,316 native frames/439 images and 264 one-pixel moves through 132 pixels and back. Heading/frame/menu pixels stayed fixed; the final card matched the opening card and decoded GIF image/timing checks passed. All 133 distinct card states matched across variants. Two corresponding captures differed in queued VRAM upload phase; offset arrays and complete cycles matched. This is not frame-for-frame temporal identity. Synthetic objective text is never shipped.

Workspace maintenance removed the temporary final-version native logs/captures/private fixtures and the uncommitted publication workspace before resumption. The receipt explicitly records these native outcomes as retained executed session results, not fresh reruns or recovered raw files. Approved preview receipts/captures and the original reproducible Debug/Release harnesses remain committed. On resumption the repository was recovered directly, both focused pause tests passed again, all relevant live Actions were verified, and a fresh canonical base plus both downloaded patches were independently decoded. Their exact target hashes match the already native-tested normal ROMs, so the game builds/native suite were not needlessly repeated.

## Publication

PR #72 merged as `7c34eaf147adcfab2d4078963439c6ee831f5bad` from tested head `ee8082ef9d3b751a5d52c22c571a43a55459ebe9`. PR checks/builds: 38811281429 / 38811281310. Merged checks/production builds: 38812493553 / 38812493630. Patch commit `1859f4925272fe9bd9b08afaafeed3eb9b719607` and [patch Pages 38813694630](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38813694630) succeeded before this publication record was updated.

Both live patches, SHA256 manifest, homepage, changelog, patcher, guide and approved previews returned HTTP 200 and matched committed bytes. A freshly rebuilt clean Emerald matched canonical SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`. Floating IPS and independently the downloaded browser decoder applied both live patches and reconstructed the exact tested normal ROMs: Release `06eb7a663b27e063a7bb4351509d4e9be8b3ae06979d79f5381cad747ae1ec0b`; Debug `d594664b57c50574d894cebf60e9d9c7fecf696cacc9bfb545a4e4c2c9969844`. Source/target/patch CRCs and manifest SHA256 values matched. Patch growth was 2,669/2,031 bytes (Release/Debug). VERSION, all three changelogs, title/Options labels, README, site, patcher and player guide are synchronized.

No publication blocker remains. The authentic historical-save matrix, uninterrupted story traversal and Pizza Boy remain unfinished; controlled fixtures do not establish those outcomes. Private diagnostic ROMs, ELFs and saves are excluded. The developer-site refresh stays deferred.
