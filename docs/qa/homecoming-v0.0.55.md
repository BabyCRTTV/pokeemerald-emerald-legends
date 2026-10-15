# Homecoming — v0.0.55

Status: validated locally and in [PR #70](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/70); production publication pending.

[Native preview](homecoming-v0.0.55-preview.png) · [Local/build/BPS receipt](homecoming-v0.0.55-local.json) · [Native/flash receipt](homecoming-v0.0.55-native.json)

## Authorized scope

On 15 October 2026 the owner accepted personal Mom and Norman milestone conversations and a short family welcome after the finale (pitch items 1, 2 and 4). Topic-selection menus and general everyday chatter were not selected. Use existing game assets and preserve approved artwork.

## Integration

Mom's original bedroom comments remain. New personal lines run in her normal healing branch and in the native postgame reassurance branch. Match Call registration and Amulet Coin delivery/full-Bag retry retain their original priority. The postgame reassurance branch retains its original non-healing behavior. Norman's new comments follow pending Enigma Berry/Facade handling, and occur after a successful rematch, preserving the native battle and training dialogue.

Speaking to Mom in the player's own downstairs room after Birch's final Hoenn epilogue and the original ticket/TV sequence triggers the welcome. Norman's existing object appears at the table under a fade, faces the player, and leaves under a fade after five short exchanges. Neither the player nor Mom is relocated. A failed object allocation restores the scene and leaves the welcome pending. Completion is recorded only after the final message. All artwork, maps, palettes, collision, wardrobe, follower settings and seasonal systems remain unchanged.

## Save compatibility

Reuse verified-unused Emerald `VAR_ROUTE111_STATE` 0x406A as `VAR_LEGENDS_HOMECOMING_MEMORY`; active source/scripts had no references. Existing native save structures, offsets, capacities, IDs, checksums and legacy readers remain unchanged. High byte 0xD6 validates the payload; bits 0–2 hold Mom's latest milestone (0–6), bits 3–5 Norman's (0–4), bit 6 the completed welcome, and bit 7 must be zero. Invalid/old data reads as unseen without mutation. Writes occur only after displayed personal dialogue or the completed scene. Each parent's latest milestone is independent; older speeches do not queue. Existing completed-story saves receive the current conversation/welcome on the next eligible visit. Fresh New Game uses the native variable reset.

## Verification

All 49 normal project-check blocks passed locally; PR project checks also passed with pinned Pillow 11.3.0. The focused actual-C/script suite now has nine cases, including all 65,536 legacy memory words without read-time mutation, independent parent milestones, skipped-old-speech behavior, own/rival-house isolation, native registration/gift/full-Bag priority, one-time family completion, allocation-failure retry, and won/lost rematches. All new text fits the actual normal font's 208-pixel width.

Both normal local Debug and Release/LTO builds passed. Native OPTION-card QA also passed in all four layouts, including selection and Options return, for both variants. PR build/BPS run [38716612020](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38716612020) and checks [38716612102](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38716612102) succeeded on game-source commit `a5b832c8a5fdee793c17bde1aba7896a76040bf4`. Clean Emerald rebuilt to canonical SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`. Both generated BPS files reconstructed their exact local targets using Floating IPS and independently the browser decoder. Growth over v0.0.54 was 1,635 bytes for Release and 2,474 for Debug.

Controlled mGBA 0.10.2 checks used the normal Debug ROM with a private setup callback, then normal emulated input ran the actual Mom and family scripts in both home layouts. Real flash write/clear/load preserved invalid pre-feature memory 0xFFFF until interaction, then completed memory 0xD666 and no repeat after reload. Non-default skin/outfit/hair, separate bedroom colors and gameplay Winter remained intact. Additional normal interactions displayed Champion-stage Mom and Norman conversations; memory ended at 0xD614 with scripts released. Every scene completed, and Norman's temporary family object was removed. Selected native frames were visually reviewed; the 480-pixel preview enlarges native pixels exactly 2× with captions outside the game image.

The prepared fixture uses the unchanged pre-feature save layout and current native save readers. It is not an authentic historical-release battery save. No schema migration was needed, and no claim is made for the unfinished historical-save matrix. Reproducible harness source is in `tools/legends/native_homecoming_qa/`. Private ROMs/saves are excluded.

Uninterrupted story traversal, the full historical-save matrix and Pizza Boy remain broader QA work. Private QA ROMs are never distributed.
