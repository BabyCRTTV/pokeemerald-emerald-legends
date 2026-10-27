# Mt. Ember return repair — v0.0.71 verification checkpoint

Model: GPT-6 (Codex) | Reasoning: preserve approved game inputs, distinguish host/native/decoder evidence and stop publication at the unresolved Release gate.

## Verified candidate — 27 October 2026

Native run `40445792327` completed successfully after the package-install delay. Debug created both private native battery fixtures and passed real boat interactions plus the established grotto/flash/Living Hoenn/seasonal/DexNav/bedroom/wardrobe suite. Unmodified Release booted normally through Continue and passed return decline/accept, clear-ground landing, real walking, outbound-gate retention and decline/reboarding with both gate snapshots. Existing normal Release grotto/bedroom/wardrobe Continue checks also passed. No Release ROM/RAM writes were used by the boat host. Downloaded artifact `12708703326` matched its archive digest; both actual native ROM hashes exactly matched the dual-decoder patch targets below. Verified image hashes and inspected actual Release Cinnabar return/Mt. Ember reboarding captures. [Durable native receipts](ember-return-v0.0.71-native.json).

Current project `40445792342` and build/dual-decoder patch `40445792347` passed. Downloaded its artifact `12708143740`, verified archive/patch hashes and decoder receipt. Tested source `b7a111ad`; later commits changed only documentation/changelog dates, confirmed by compare. All four v0.0.71 changelog views now use October 27, the publication date. AGENTS.md was reviewed without a new durable rule. Candidate is ready for the already-authorized merge/publication; actual merged runs, automatic patch commit, Pages and live-byte verification must be recorded separately before declaring publication complete. Controlled current fixtures do not establish authentic historical saves, uninterrupted story/balance or Pizza Boy coverage.

## Scope and compatibility

Published baseline: master `7cf9a7bfcb515ad33b4840ce38cd7d2e88008b8d`, VERSION 0.0.70. PR #90 prepares 0.0.71. Its only gameplay change moves the existing Mt. Ember boat return from blocked Cinnabar `(20,9)` to clear `(21,8)` beside the existing sailor. Maps, tilesets, approved artwork, wardrobe, seasons, flags/IDs, save layouts/readers, rewards and outbound progression gates are unchanged. No migration is required. The original geometry review remains in [the October 26 record](ember-return-2026-10-26.md).

## Verified evidence

- Reran all 57 focused Kanto/postgame tests and whitespace checks successfully.
- Candidate `3f60da69` passed project `40444532680`; native `40444532754` passed Debug Quickstart, actual boat decline/accept, return/walk/reboard with and without outbound gates, then grotto/flash/Living Hoenn/seasonal/DexNav/bedroom/wardrobe checks. Inspected the actual Cinnabar frame. Artifact `12708046192` retains frames and receipts. Debug ROM SHA256: `cf9e5925781e6f2ecd7f5b98d2b251e3b25cf290b9b86fab5c74b1f53943a000`.
- The same native job compiled Release but its injection harness stopped before gameplay with missing optimized private symbol `Task_HandleYesNoInput`. No Release boat outcome is inferred from that failure.
- `b7a111ad` replaced that Release-only path with an unchanged-ROM normal title/Continue test and two private Debug-produced current battery fixtures. Inputs are real controller presses; Release RAM observations are read-only. It checks boat decline/accept, actual map/position, walking, flag preservation and reboarding. Existing project precedent is native_visual_repairs_qa/release.py. Python syntax review passed; native fixture generation and Release execution still need actual CI results.
- Current project `40445792342` and build/patch `40445792347` passed. Patch run `40444532795` also passed both builds, canonical clean Emerald SHA1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`, Floating IPS reconstruction and the independent committed browser decoder. Downloaded artifact `12708191242`, verified its archive hash and actual patch hashes, and inspected its decoder receipt. These target hashes match the unchanged current production inputs.

| Variant | Patch SHA256 | Target ROM SHA256 |
| --- | --- | --- |
| Release | `bf915116c6c7cb848d701fe01790f88f69bff5fe78694818a34d490955a24924` | `6786a3a4d5a8ca46361aaee9db8245352d9718ef71f47fbc6b084b72b1ee6654` |
| Debug | `aca1afb419b879b264851f80f69258934bc4d7bcfd68e94279d7b2a6fd1e493b` | `cf9e5925781e6f2ecd7f5b98d2b251e3b25cf290b9b86fab5c74b1f53943a000` |

Fresh v0.0.70 live Release/Debug downloads matched the published manifest. Live homepage, changelog, patcher HTML and JS matched pinned Git blobs. No new release was published during this checkpoint.

## Earlier blocked checkpoint (superseded by verified candidate above)

At 2026-10-27 03:55 UTC (October 26 locally), native run `40445792327`, job `121996650473`, remained in compiler/mGBA package installation, which began at 03:44:05 UTC. It had not reached the new tests. The running job's logs were not yet available. Local ARM/mGBA packages are unavailable. This is an external setup delay, not an observed new game or Release harness failure.

Inspect that run's actual result first. If setup fails/times out, retry the failed job and inspect its logs. If the harness fails, investigate the specific assertion or missing data symbol; do not weaken gameplay assertions or alter production code to satisfy the test. Require Debug fixture creation, unmodified Release boat interactions and existing Release Continue checks to pass. Download native receipts/frames, compare both ROM hashes above and inspect actual Release captures. Preserve concurrent branch edits and verify the current head.

Then finalize QA/handoff, mark PR #90 ready, merge with an expected-head lease, verify merged workflows, automatic BPS publication, final Pages deployment, and actual live patch/page bytes. Do not report v0.0.71 as published before these checks. Private QA ROMs and saves must remain excluded from git and artifact globs; only frames, logs and receipts are retained.

Authentic historical saves, uninterrupted full-story/balance testing, rare outfit corruption and Pizza Boy coverage remain unresolved. Wyrmtide PR #89 has successful candidate CI but awaits visual approval; PR #56 is an older conflicting wiki proposal. Neither belongs in this repair release.
