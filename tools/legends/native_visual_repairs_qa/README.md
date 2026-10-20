# Native visual repair QA

Requires a built Debug ROM/ELF, ARM tools, Pillow and libmGBA. Run:

```sh
python3 tools/legends/native_visual_repairs_qa/run.py --output build/visual-repairs-qa --mgba-prefix /usr
```

The optional --rom and --elf arguments target a matching baseline build. The callback prepares controlled current-save scenes; real tasks and controller inputs perform Wardrobe Apply/Cancel and Trainer Card returns, with 72 actual unfaded OBJ palette checks and real flash save/load. Native manual-clock API selects midday/night for Fallarbor. These are controlled diagnostics, not an historical save or Pizza Boy reproduction.

After building normal Release, test unmodified Release Continue and controller input:

```sh
python3 tools/legends/native_visual_repairs_qa/release.py --prefix /usr --fixtures build/visual-repairs-qa --output build/visual-repairs-release
```

Release has LTO-inlined entry points, so it uses private Debug-produced battery fixtures through normal Continue rather than injecting Debug callbacks. Only frames/logs/JSON may be uploaded. Never commit or upload private diagnostic ROMs, .sav fixtures, raw .rgba files or host/ARM binaries. Gameplay frames use actual compiled ROM pixels; scale only with nearest-neighbor sampling.

For a full second-decoder check against canonical clean Emerald and both native builds:

```sh
node tools/legends/verify_bps_with_browser.cjs clean.gba release.bps debug.bps pokeemerald-release.gba pokeemerald.gba verification.json
```

This executes the actual committed browser decoder in a Node VM and requires exact native target bytes. It does not automate a physical browser file picker or Pizza Boy. Keep all .gba/.sav inputs private.
