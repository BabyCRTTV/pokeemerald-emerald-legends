# Native achievement preview

Requires a built Debug ELF/ROM, ARM tools on PATH, Pillow and mGBA 0.10.2 headers/library. Run from any directory:

```sh
python3 tools/legends/native_achievement_qa/run.py --output /tmp/achievement-preview
```

Add `--mgba-prefix /path/to/usr` for an extracted development package. The harness links a private callback into checked unused ROM padding, prepares a new Oldale Town scene, triggers appended achievement 80 through actual FlagSet, and drives real field/journal tasks using emulated GBA keys. It asserts earned/unclaimed state, movement during the banner, visible/expired window state, selected indices and the manual claimed bit. Pixel checks reject a blank banner and require every panel pixel to remain identical on every visible frame during four-direction movement. The GIF is decoded/composited and its banner pixels must also match the native reference. This catches the original screen-block overlap that corrupted the first preview when the camera moved. Output includes full-screen PNGs, an animated native field preview, a narrow three-screen PNG and structured hashes.

Use a fresh output directory when extending captures. Private ROMs/ELFs/raw buffers/logs must never be committed or distributed. Only the reviewed PNG/GIF and JSON receipts belong in docs/qa. These controlled scenes are not normal story progression or historical save reload tests.
