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

## Publication

Pending rerun regression/native-build/BPS verification and live Pages/download checks. The latest verified public build remains v0.0.49 until these receipts are recorded. Broader natural movement/weather/follower playtests and historical battery-save fixtures remain outstanding; this palette-only change does not claim those tests.
