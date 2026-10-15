# Homecoming — v0.0.55

Status: implementation and verification in progress; not yet published.

## Authorized scope

On 15 October 2026 the owner accepted personal Mom and Norman milestone conversations and a short family welcome after the finale (pitch items 1, 2 and 4). Topic-selection menus and general everyday chatter were not selected. Use existing game assets and preserve approved artwork.

## Integration

Mom's original bedroom comments remain. New personal lines run in her normal healing branch and in the native postgame reassurance branch. Match Call registration and Amulet Coin delivery/full-Bag retry retain their original priority. The postgame reassurance branch retains its original non-healing behavior. Norman's new comments follow pending Enigma Berry/Facade handling, and occur after a successful rematch, preserving the native battle and training dialogue.

Speaking to Mom in the player's own downstairs room after Birch's final Hoenn epilogue and the original ticket/TV sequence triggers the welcome. Norman's existing object appears at the table under a fade, faces the player, and leaves under a fade after five short exchanges. Neither the player nor Mom is relocated. A failed object allocation restores the scene and leaves the welcome pending. Completion is recorded only after the final message. All artwork, maps, palettes, collision, wardrobe, follower settings and seasonal systems remain unchanged.

## Save compatibility

Reuse verified-unused Emerald `VAR_ROUTE111_STATE` 0x406A as `VAR_LEGENDS_HOMECOMING_MEMORY`; active source/scripts had no references. Existing native save structures, offsets, capacities, IDs, checksums and legacy readers remain unchanged. High byte 0xD6 validates the payload; bits 0–2 hold Mom's latest milestone (0–6), bits 3–5 Norman's (0–4), bit 6 the completed welcome, and bit 7 must be zero. Invalid/old data reads as unseen without mutation. Writes occur only after displayed personal dialogue or the completed scene. Each parent's latest milestone is independent; older speeches do not queue. Existing completed-story saves receive the current conversation/welcome on the next eligible visit. Fresh New Game uses the native variable reset.

## Verification

Pending final receipts. The focused test compiles the actual C module and exercises script routing, legacy/default values, independent parents, one-time completion, gift priority/full-Bag retry, rematches, both houses/rival isolation and native-font width. Native builds, full project checks, controlled emulator/flash evidence and independent BPS/publication verification must be recorded before readiness is claimed.

Uninterrupted story traversal, the full historical-save matrix and Pizza Boy remain broader QA work. Private QA ROMs are never distributed.
