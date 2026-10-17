# Achievement extension native QA

Requires built Debug/Release ROMs and ELFs, ARM tools on PATH, Pillow, and an mGBA 0.10.2 development prefix.

Run `run.py --prefix <prefix> --output <private-output>` to check a controlled v0.0.59-layout journal (including garbage unused bytes), quiet backfill, retained old claims/pin/settings/inventory, ID 129's real notice/list/details, manual full-PC retry/once-only claim and actual flash save/clear/load. The callback is linked only into a private Debug ROM copy. `continue.py --prefix <prefix> --output <private-output> --variant Debug|Release --fixture <private-migrated.sav|private-claimed.sav> --claimed 0|1` loads those fixtures via normal title/Continue in the unmodified game; it only sends buttons and reads memory.

Private ROMs, battery saves and raw output must never be committed or distributed. These are controlled format-identical fixtures, not authentic historical user saves, a full playthrough or Pizza Boy coverage.
