# Parent skin-tone preview — awaiting visual review

On 14 October 2026 the owner requested Mom and Norman's overworld skin and Norman's battle portrait to match the player's selected skin tone, and asked to see all five existing tones. This is a review study against published v0.0.49 (`4dd6a65d32c7daf2c326df35a1898a71d6281670`); family-tone inheritance is **not integrated into the ROM** yet. Do not describe it as shipped or bump the game version for this preview.

The narrow `Family-Skin-Tones-Preview.png` shows the actual v0.0.49 player reference, both parents from the front/back/side and Norman's full battle portrait at each of the five tones. SHA256: `c572b60df273ac6c790c7be0ae08dab25cd5fe26a1fb8bc100b0aa8701f57722`. The native parent pixels, poses, hair and clothing are retained. All skin highlights/midtones/shadows use `sSkinPalettes`; Norman's extra battle-skin outline preserves its native darker shade ratio. The preview is a precise native-asset recolor with a host-C player reference, not an emulator capture or runtime integration test.

Reproduce with `python3 tools/legends/preview_family_skin.py --output /tmp/family-skin-review`. The tool validates all nine source frames for each parent plus the battle portrait at all five tones (95 cases), checking unchanged alpha/silhouette and every pixel outside the skin masks. Source hashes and the three RGB555 skin colors per tone are written to the output's `proposal.json`.

## Important integration constraints

- Both overworld actors currently use the shared `OBJ_EVENT_PAL_TAG_NPC_4` / `PALSLOT_NPC_4`. Recoloring that bank globally would also affect unrelated NPCs. Isolate parent materials/palettes when integrating; exercise reflections, lighting, palette-slot pressure and maps containing other NPCs.
- Mom's native indices 1–3 also include disconnected peach/brown hair highlights. The study isolates the actual face, ears and hands and leaves those highlights unchanged, including in the rear view. A future private palette alone is insufficient unless those shared hair materials are separated too.
- Norman's battle material 4 is a skin contour near the face/hands. His slate hair and clothing use other materials and stay unchanged. Keep the original trainer portrait/silhouette; do not regenerate or replace him.
- Inherit from the existing player skin selection (including after wardrobe changes and on older saves). Do not add separate saved parent choices, renumber persistent IDs or change the save format for this feature. Legacy appearance defaults must stay valid.
- Wire and test the proposed inheritance only after visual review. The current skin-mask checks establish the preview's scope; they do not establish native palette allocation, battle loading or save/continue behavior.
