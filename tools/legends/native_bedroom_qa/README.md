# Native bedroom review harness

After building Debug, run `python3 tools/legends/native_bedroom_qa/run.py --output /tmp/bedroom-qa --mgba-prefix /path/to/extracted/usr`.

Requires GCC ARM tools, Pillow and mGBA 0.10.2. The ARM callback lives in unused FF ROM padding and uses a private EWRAM mailbox. Never distribute the generated private ROM. Screenshots show native rendering and tasks, with controlled story setup; the real player-input path selects/cancels independent colors. Flash round-trip verifies the prepared save, not an authentic historical release fixture. Runtime art comes exclusively from existing game assets.
