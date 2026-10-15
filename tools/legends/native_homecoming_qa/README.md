# Controlled native homecoming QA

Build Debug, then run `python3 tools/legends/native_homecoming_qa/run.py --output /tmp/homecoming-qa --prefix /path/to/usr` with ARM tools on PATH and libmgba development files at the prefix. Requires Pillow and mGBA 0.10.2.

The runner adds a controlled setup callback only to a private ROM copy. It prepares both home layouts with completed native and finale gates, an invalid legacy conversation word, and non-default wardrobe/bedroom/season settings. The player starts on wood floor and approaches Mom with normal emulated input. Assertions require a passable stationary player throughout the shipped scene and no-clip disabled, then try to enter blocked table tiles after reload in both houses. Never warp the player beside Mom on table tiles (the original fixture mistake). Assertions cover actual flash write/clear/load before and after, successful object cleanup, completed memory, retained settings and no repeat after reload. Native frame captures and verification JSON are emitted only after success.

This is a reproducible format-identical pre-feature fixture, not an authentic historical-release save or uninterrupted playthrough. Never publish the private ROM, save or full output directory. Commit only the harness source, selected captures and verification receipt.
