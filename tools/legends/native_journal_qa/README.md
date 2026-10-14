# Native journal selection QA

Requires a built Debug `pokeemerald.elf`/`pokeemerald.gba`, ARM GCC/binutils, Pillow and mGBA 0.10.2 development headers/library.

```sh
python3 tools/legends/native_journal_qa/run.py --output /tmp/journal-qa
```

For an extracted mGBA package, add `--mgba-prefix /path/to/usr`; put ARM tools on PATH. The harness links a diagnostic callback into verified unused padding of a **private ROM copy**, sets quest flags, then opens the actual journal. The host sends emulated GBA keys and waits for rendering/DMA before capturing eight native screens. It asserts selected/scroll/detail state and pixel contrast, saves PNGs, a narrow two-screen preview and SHA256 receipts.

Only Debug symbols are supported. Captures are controlled UI tests, not natural overworld traversal or historical-save loading. Never commit or distribute the private ROM/ELF/output directory. Commit only selected PNG previews and structured receipts. Use a fresh output directory when extending the capture set.
