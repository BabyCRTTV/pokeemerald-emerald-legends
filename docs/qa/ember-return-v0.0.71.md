# Mt. Ember return repair — v0.0.71 published

Model: GPT-6 (Codex) | Reasoning: verify the approved landing repair through real Debug/Release interactions and exact live-patch identity while preserving existing game inputs.

Published 27 October 2026. [PR #90](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/90) merged as `ab52786d11e709014240520451c05d9d2cef5f24`; its tree exactly matched the reviewed head. Automatic patch commit `15e147a4a3c2d4969285fdee42188a4bceafe790` and [patch Pages 40449056949](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/40449056949) succeeded. **Publication is complete; no publication blocker remains.**

## Change and compatibility

The existing Mt. Ember return boat now lands on clear Cinnabar ground `(21,8)`, beside the expedition sailor, instead of the blocked closed-door/self-warp tile `(20,9)`. The original script/geometry regression failed before this repair and passed afterward. Outbound story gates, unrestricted expedition return, flags/reports and decline behavior retain their meanings. Maps, tilesets, approved artwork, wardrobe, seasons, save layouts/readers, persistent IDs and reward behavior are unchanged. No migration was required. Only the return coordinate and synchronized version labels changed game inputs. All three changelogs, Options/title labels, README, site and browser patcher/cache key show v0.0.71, dated October 27. AGENTS.md was reviewed; no new durable rule was needed.

## Verification

All 57 focused Kanto/postgame host tests passed. Candidate project `40445792342`, builds/canonical-base/two independent decoders `40445792347`, and native `40445792327` passed. Actual Debug boat decline/accept, return, collision-enabled walking and reboarding passed with/without outbound gates. Private current native battery fixtures then booted through **normal Continue on the unmodified Release ROM**, with real controller buttons and read-only RAM observations. The same affected interactions and progression preservation passed there. Existing grotto/battle/flash/Living Hoenn/seasonal/DexNav/bedroom/wardrobe checks and normal Release Continue checks passed. [Durable candidate native receipts](ember-return-v0.0.71-native.json).

Production [project 40448115913](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/40448115913), [builds/BPS/dual-decoder 40448115841](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/40448115841) and [native Debug/Release 40448115945](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/40448115945) all passed. Both builds' native hashes matched the exact independently decoded targets below. Downloaded production artifact `12709552687`, verified its archive digest, native target and retained boat image hashes, and inspected the actual Release Cinnabar return frame. Candidate Release return/reboarding frames were also inspected. Private ROMs and saves remain excluded from git/artifact uploads; only frames, logs, metadata and receipts were retained.

The first private test needed adequate turn/walk input and native Yes/No readiness/event waits. Release optimization removed an assumed private function name; the final Release checker uses the established normal-Continue approach instead of injecting code or changing production compilation. These harness repairs changed no game inputs. Earlier blocked-state details remain in git history and [the original geometry record](ember-return-2026-10-26.md); they are superseded by the passed results above.

## Live publication

Fresh public HTTP downloads returned 200 for both BPS files, manifest, homepage, changelog, patcher HTML and JavaScript. Page/manifest Git blob hashes matched committed bytes. Both actual patch hashes and patch CRCs passed and matched the independently dual-decoded candidate bytes; native production target hashes matched those decoder targets. Clean-base applications used canonical Emerald SHA1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7` in CI. Fresh live byte/CRC checks are distinguished from those independent CI applications; no additional local clean-base application is claimed. [Exact public/production receipts](ember-return-v0.0.71-public.json).

| Variant | Live patch SHA256 | Native and decoded target SHA256 |
| --- | --- | --- |
| Release | `bf915116c6c7cb848d701fe01790f88f69bff5fe78694818a34d490955a24924` | `6786a3a4d5a8ca46361aaee9db8245352d9718ef71f47fbc6b084b72b1ee6654` |
| Debug | `aca1afb419b879b264851f80f69258934bc4d7bcfd68e94279d7b2a6fd1e493b` | `cf9e5925781e6f2ecd7f5b98d2b251e3b25cf290b9b86fab5c74b1f53943a000` |

## Limits and remaining work

Controlled current-save fixtures do not establish authentic historical-owner saves, a full uninterrupted story/balance playthrough or Pizza Boy coverage. Broader historical fixtures, rare outfit corruption and those playtests remain unfinished. Wyrmtide PR #89 still needs visual approval; older wiki PR #56 must be reconciled without overwriting the current wiki. None of that work was included in this repair release.
