# Controlled native family palette QA

After building the normal Debug `pokeemerald.elf`/`.gba`, run:

```sh
python3 tools/legends/native_family_qa/run.py --output /tmp/legends-family-qa
```

Requires `arm-none-eabi-gcc`, `arm-none-eabi-objcopy`, `arm-none-eabi-nm`, a host C compiler, Pillow and libmgba development headers/library (tested with mGBA 0.10.2). `--mgba-prefix /path/to/usr` supports extracted development packages; ARM tools follow `PATH`.

The runner checks unused ROM padding before inserting its callback into a private copy. After boot, it isolates callback1 and invokes actual ARM virtual-object, palette, reflection and wardrobe functions. Five tones × pond/ice yield 190 sprite/palette cases and 20 reflection palettes. It verifies unrelated NPC-4 isolation, wardrobe Apply/Cancel, and cached parent tag reuse with all 16 slots occupied. Original linked files are never modified.

`verification.json` records the tested Debug ROM/capture/harness hashes. The output also contains a modified private ROM and diagnostic binaries: **do not commit or distribute that output**. Only these reproducible source files belong in git. This fixture does not test normal map traversal, menu clicks, follower/weather transitions or battery save/load. Retain the broader QA and save-compatibility requirements.
