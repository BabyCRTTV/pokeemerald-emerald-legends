# Controlled native quest-tracking QA

Requires normal Debug/Release ROMs and ELFs, ARM GCC/binutils on PATH, Pillow and mGBA 0.10.2 development files. For extracted dependencies:

```
python3 tools/legends/native_quest_tracking_qa/run.py --output /tmp/tracking-debug --prefix /path/to/usr
python3 tools/legends/native_quest_tracking_qa/release.py --output /tmp/tracking-release --prefix /path/to/usr --fixture /tmp/tracking-debug/private-tracked.sav
```

Debug injects a setup callback only into verified unused padding of a private ROM copy. It prepares a walkable home-floor position, version-1 journal with reserved=0, non-default appearance/bedroom/Winter and a partially completed Devon Delivery. Emulated input tracks through Details, visits both pause pages, DexNav help and Save/cancel. Controlled flags advance/complete the quest and enable the Safari counter. Real flash write/clear/load checks the old-format default, tracked selection and completed state, retaining settings. A mailbox completion handshake prevents a later diagnostic request from interrupting an unfinished callback.

The runner verifies unchanged menu-content/clock pixels and changed next-objective pixels. Host tests separately cover every legacy word, all catalogue text with native font widths, resource bounds, allocation failure, map-popup exclusion and all 64 combinations of special-menu restrictions.

Release loads a **private writable copy** of the Debug battery fixture through normal title/Continue input. mGBA's save mapping requires a writable file; the source fixture is preserved. This host changes neither ROM bytes nor RAM/callbacks. It checks both pause pages, tracked Details and stop tracking; the reminder pixels must match Debug exactly.

These are controlled fixtures in the unchanged save layout, not authentic historical-release saves or uninterrupted traversal. Use fresh output directories. Never commit/distribute diagnostic ROMs, ELFs, full output directories or battery saves. Only selected previews, source and structured receipts belong in GitHub.
