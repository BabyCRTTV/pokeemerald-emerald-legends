# Birch field requests — v0.0.58 preview QA

**Approval:** implementation complete for review; do not merge master, deploy Pages or publish patches before owner preview approval. Production remains v0.0.57 at `9af3087528bc06bd754587b83dc2d291f1362fd9`.

[Preview PNG](birch-v0.0.58-preview.png) · [Animated actual-game capture](birch-v0.0.58-preview.gif) · [Machine receipts](birch-v0.0.58.json) · [Feature design and request table](../features/birch-field-requests.md)

## Verified

- All 50 project check blocks passed, including the new shipped-C field-request suite and existing journal/UI, story, wardrobe, map, seasons, patcher and metadata checks. Text fits native dialogue widths. The first 33 quest entries retain their exact hash; all 95 achievement IDs and the 36-byte journal remain intact.
- Debug and native LTO Release builds passed with GCC 13.2.1/binutils 2.42/newlib 4.4. The restored local toolchain needed its ARM assembler path repaired; no game workaround was introduced. Existing unrelated LTO warnings remain. EWRAM is 254808/254814 bytes, below 262144.
- Shipped-C tests exercised all six proofs/rewards, one active request, a preserved existing tracked quest, abandonment/cancel/reaccept, completed-request rejection, Egg exclusion, link guards, invalid legacy words and full-storage retry. Samples are consumed only by successful berry submission; no Pokémon are removed.
- Debug mGBA 0.10.2 ran actual native dialogue/menu input through selection, acceptance, canceling/confirming abandonment, reacceptance, full PC storage and successful one-time berry reward. Real flash save/clear/load retained invalid pre-feature words, active/completed work, habitat observations and non-default wardrobe/bedroom/Winter settings.
- Actual Petalburg Woods/Route 104 arrivals recorded qualifying party observations. The real Pokédex handoff displayed the invitation immediately after its explanation and continued to the rival's normal Poké Ball gift. Collision stayed enabled and the player remained on passable floor throughout. No maps, collision data or art changed.
- Unmodified Release booted normally and used Continue with three private Debug-produced fixtures: arbitrary legacy words, active Berry Samples, and completed Berry Samples. The host only read memory and sent buttons. Request words persisted; the active fixture exercised both pause pages, SIDE Details and stopping tracking. Reminder pixels matched Debug exactly.
- Private Release/Debug BPS files independently reconstructed the exact tested ROMs using both Floating IPS and the site's browser decoder against canonical clean Emerald SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`. No private ROMs, saves or patch files were committed or published.

## Reproduction

`tools/legends/native_field_requests_qa/run.py --prefix <mGBA/GBA-toolchain prefix> --output <private output>` builds a private Debug payload and fixtures. `release.py --prefix <prefix> --output <private output> --fixture <Debug fixture.sav> --state <word> --done <word>` checks normal Release Continue. Use `(0xffff,0xffff)`, `(0xb703,0)` and `(0xb700,4)` for the legacy, active and completed fixtures. Keep all fixtures and payload ROMs private. The preview uses unaltered captures, enlarged with nearest-neighbor scaling; the vertical PNG adds labels outside the game frame.

## Limits and next steps

These are controlled format-identical save fixtures, not authentic historical user saves. An uninterrupted six-request playthrough, wider authentic-save matrix and Pizza Boy testing remain outstanding. Local verification does not imply remote CI passed.

After owner approval: inspect live master for changes, commit any requested revisions, open/merge the feature PR after checks and both native/BPS CI passes, then verify published Release/Debug patches, Pages bytes and downloads. Keep appended request/journal IDs stable. The existing signed words have room for 16 requests; expansion beyond that requires a tested additional-word migration.
