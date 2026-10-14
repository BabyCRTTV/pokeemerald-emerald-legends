# Native bedroom QA harness

After building Debug, run `python3 tools/legends/native_bedroom_qa/run.py --output /tmp/bedroom-qa --mgba-prefix /path/to/extracted/usr`. Optional `--baseline-output` compares both Default scenes with existing native captures.

Requires GCC ARM tools, Pillow and mGBA 0.10.2. The ARM callback uses unused FF ROM padding and a private EWRAM mailbox. Never distribute the private ROM. Controlled story setup uses real maps and native artwork. Actual emulated input selects/cancels separate rug/bed/original-chair colors and places a doll on wood floor. Real flash write/clear/load restores the color and decoration records; this is a prepared current fixture, not an authentic historical-release save.

Pixel comparisons isolate rug/bed/chair changes and the poster wall rectangle. Default native chair geometry/support colors must match baseline exactly. PC interaction is captured from both seats; the final capture reaches Decoration through the real PC menu. The direct-menu callback only sets up other QA cases. No alternate chair shapes remain in runtime assets or controls.
