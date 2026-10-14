# Family skin inheritance — v0.0.50

The owner approved all five tones on 14 October 2026 (“Flawless work. Approved.”). [Approved narrow PNG](family-skin-v0.0.50-approved.png); [preview provenance](family-skin-preview.md). The reproduced preview SHA256 is exactly `c572b60df273ac6c790c7be0ae08dab25cd5fe26a1fb8bc100b0aa8701f57722`.

## Implementation

Mom and Norman use private overworld palette tags `0x1174`/`0x1175`. Standard spawn, return-to-field, graphics-change, palette-copy and direct-patch paths resolve those tags to immutable ROM palettes using `LegendsGetSkinTone()`. Allocation, weather adjustment and reflection filtering remain native. Unrelated tags return their original palette pointer. New table entries are appended to preserve existing numerical berry palette references.

Mom's native skin slots also contain 54 hair-highlight cells across nine source frames. Generated Mom-only 4bpp data moves only those highlights from index 3 to previously unused index 12, preserving their original color in the private palette. Her PNG, outlines, transparency, exposed skin, frame geometry and animation commands are preserved. Norman's overworld image/table remain unchanged. The common trainer-front palette getter selects Norman's matching battle palette, including the approved proportional deeper contour. Every other trainer retains its original palette; Norman's battle image is unchanged.

`python3 tools/legends/build_family_skin.py` regenerates the checked-in ROM data. The study is frozen in `tools/legends/family_skin_approval.json`. This adds no sprite-cache RAM. Mom's linked image is replaced by the same-size material-separated image. No saved fields, IDs, capacities, codecs, initialization rules or legacy readers changed; no migration is required. Wardrobe Apply/Cancel uses the native field reload to derive parent colors from the committed choice. Legacy/default appearance codes use the existing first-tone fallback.

## Verification and interruption

The initial implementation passed 95 host-C asset/tone comparisons, all 44 executable workflow commands and native GCC 13.2.1 Debug/Release builds before a usage-limit interruption. Controlled mGBA 0.10.2 checks invoked actual ARM virtual-object creation and palette/reflection loaders: 190 asset/tone buffers, 20 pond/ice reflection palettes, unrelated NPC-4 isolation, full 16-slot allocation and ten wardrobe Apply/Cancel rounds passed. Those were controlled callback tests, not natural map/menu traversal or a historical-save emulator matrix.

The restored workspace did not retain that uncommitted implementation, binaries or detailed receipts. It was reconstructed against `73f9fae86de65a33a87423efeffa228cfe7df3d5`; the preview matched its original hash and the actual family C passed the 95-case comparison again. All 44 executable project-workflow commands passed again against the restored source; the already-installed Pillow dependency installation was skipped. Native builds and final publication are being reverified rather than relying only on the interrupted session.

Current source check: `python3 test/legends-family-skin.test.py` compiles the actual family palette C and existing saved-code decoder. It checks every pixel/alpha cell in all native frames and five tones, outfit/legacy code handling, unrelated pointer identity and deterministic generation. Protected appearance and fast save suites remain part of the full workflow.

## Restored-source native evidence

The restored Debug ROM passed the controlled native checks again using mGBA 0.10.2. All 190 asset/tone buffers, 20 pond/ice reflection palettes, ten Apply/Cancel rounds, unrelated NPC-4 isolation and full-slot tag-reuse checks passed. [Structured native receipt](family-skin-v0.0.50-native.json) pins its ROM, capture and harness hashes. [Reproducible harness](../../tools/legends/native_family_qa/README.md) is included as development source; its private diagnostic ROM is never distributed. The actual original Debug image is unchanged by the test runner.

Both restored-source GCC 13.2.1 builds passed. EWRAM/IWRAM were unchanged at 254468/28376 bytes (Debug) and 254470/28328 bytes (Release). ROM usage grew only 424/880 bytes respectively versus v0.0.49. [Complete local verification](family-skin-v0.0.50-verification.json) pins both final target hashes. Existing unrelated compiler warnings remained; no family build error occurred.

## Publication — GitHub and Pages verified

- Runtime source: `29e45ad535e1bd6a57e6e18f0a01939dd94740b9`; [source checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38592974123) passed. Native harness and frozen masks: `ff0b287a61cbdca1e0590255a581d7a954df7b59`; [its checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38593983229) passed.
- [Remote native Debug/Release builds, supported clean-base identity, independent BPS applications and byte comparisons](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38592973976) passed. Patch commit: `491a43c6cf6ad3d581c6ca6b57ee219ccb706a3b`. Both targets matched local native ROMs, including the actual Debug ROM tested in mGBA.
- Both pinned public GitHub BPS URLs returned HTTP 200 and matched the committed SHA256 manifest. Patch/source/target CRCs passed. Release grew only 539 BPS bytes and Debug 904 bytes. [Structured publication receipts](family-skin-v0.0.50-verification.json) contain both direct download URLs and hashes.
- On 14 October 2026, [Pages run 38597478728, attempt 2](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38597478728/attempts/2) succeeded after a targeted retry of failed jobs. The stale deployment lock no longer blocked publication. No game source, version or ROM rebuild changed for this recovery.
- Both live site BPS URLs returned HTTP 200, matched the committed SHA256 manifest and passed patch/source/target CRC checks. Their target hashes matched the native builds, including the Debug ROM tested in mGBA. Homepage, changelog, patcher HTML/JavaScript and the approved mobile PNG matched committed bytes. Sizes, hashes and failure/recovery history are preserved in the structured receipt.

### Resolved Pages incident

The original deployment timed out in `updating_pages`; immediate retries were rejected as another deployment remained active. A bounded cancellation job returned `deployment_cancelled`, but retries still encountered the stale lock. The temporary workflow was removed after use. A later retry of the failed Pages jobs completed successfully. Historical failing runs: `38594477288`, `38596593358`, `38597017926`; cancellation run: `38597018064`. Earlier v0.0.49 manifest/404 observations describe that incident, not the current live site.

For future updates, wait for the current Pages deployment before issuing additional publication commits. If a stale-lock error occurs, inspect the exact blocking deployment and retry only failed jobs once it clears. Keep verified GitHub patch downloads available, preserve deployment evidence and verify live bytes before marking publication complete. Hosting recovery requires no game version bump or duplicate ROM build.


Broader natural movement/weather/follower playtests and historical battery-save fixtures remain outstanding. Controlled callbacks do not establish normal map/menu traversal or battery save/reload. No original or private diagnostic game ROM was published.
