# Seasonal Routes 113–116 — v0.0.66

**Model: GPT-6 | Approach: preserve native encounter dependencies and earlier tables; verify new rosters and the season-union reader.**

Status: implementation in verification; not published. [Roster/rules](../features/seasonal-encounters.md) · [Source receipt](seasonal-routes-v0.0.66-source.json). Native slots/levels/rate20 and residents remain; previous48 tables and all unrelated methods, art, maps, saves and IDs stay unchanged. Routine user-facing previews were waived. Internal native diagnostics remain required.

Planned coverage: all64 seasonal tables through shipped-C resolver/data tests and64/48/32/16-table importer regressions;136 native cases with34,816 actual creations; both game builds, BPS gates and independent live decoders. LegendsDex All Seasons will retain per-season rates/badges, merge only identical entries and accept shared links. Results and publication receipts follow execution.

Limits: controlled native Debug fixtures do not establish full natural progression, full hunts, Release interaction, historical-save migration or Pizza Boy coverage.

## Resumption verification — 19 October 2026

**Model: GPT-6.1 | Reasoning: close the stale checkpoint against live GitHub and retained source.**

The implementation above shipped via PR #82 and patch commit `5c506a52`. Production project/builds/BPS/native/Pages gates passed; native logs confirm all 136 seasonal scenarios and 34,816 creations. Fresh public Release/Debug patch bytes match the committed hashes and pass patch CRCs. See [resumption public receipt](seasonal-routes-v0.0.66-public.json) for evidence and the unperformed fresh second-decoder limitation. The earlier implementation/planning notes are historical, not the current publication state.

Recovered LegendsDex 1.4.0 changes from `aef342e2` without its temporary workflow trigger or obsolete patch files. Prior species/art/data preserved; only Routes 113–116 land methods gained variants. Corrected exact-tuple season badges when species-wide metadata includes other seasons. Local reader (64 seasonal views/16 unions), all 409 walkthrough methods, 64/48/32/16 snapshot imports and actual-C encounter tests passed. Fresh browser CI and public web-byte verification remain the wiki closeout gate.
