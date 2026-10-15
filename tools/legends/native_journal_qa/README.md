# Native journal selection QA

Requires built `pokeemerald.elf`/`pokeemerald.gba` (Debug) or `pokeemerald-release.elf`/`pokeemerald-release.gba` (Release), ARM GCC/binutils, Pillow and mGBA 0.10.2 development headers/library.

```sh
python3 tools/legends/native_journal_qa/run.py --output /tmp/journal-qa
```

For an extracted mGBA package, add `--mgba-prefix /path/to/usr`; put ARM tools on PATH. The harness links a diagnostic callback into verified unused padding of a **private ROM copy**, sets quest flags, then opens the actual journal. The host sends emulated GBA keys and waits for rendering/DMA before capturing fourteen native screens. It asserts selected/scroll/detail state, complete row contrast, manual reward claim confirmation/timeout and exact quest detail-return pixels, saves PNGs, a narrow two-screen preview and SHA256 receipts.

Pass `--variant Release` for Release symbols; Debug is the default. Captures are controlled UI tests, not natural overworld traversal or historical-save loading. Never commit or distribute the private ROM/ELF/output directory. Commit only selected PNG previews and structured receipts. Use a fresh output directory when extending the capture set.

Release uses `arm_release.c` to seed quest flags/journal/one claimed rendering fixture directly, because LTO removes Debug setup helpers. Both variants then drive the real menu, manual second reward claim, PC confirmation/timeout and filters with emulated keys. First-open footer pixels are checked before any redraw. No diagnostic code enters published ROMs.
