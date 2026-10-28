# Development process audit — 28 October 2026

Model: GPT-6 (Codex) | Reasoning: measure the critical path, remove discarded work and preserve verification strength.

Baseline: published v0.0.75 at `7819b69eecdc3f8cafdae9018f0891ea59baa597`. Reviewed live history, Actions, workflows, VERSION, releases, AGENTS, handoff, save policy, native fixtures and companion packaging. This is process maintenance; game version, source, maps, approved artwork and published patches are unchanged.

## Measured delays

These are observed job/step times from GitHub's run/jobs API, not forecasts. See [machine timing evidence](development-process-2026-10-28.json).

| Stage | v0.0.75 production observation | Implication |
| --- | --- | --- |
| Native QA [40628689606](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/40628689606) | 14m52s job; Debug build 4m30s, Release 2m36s | Repeated failed fixtures pay compilation cost again. Inspect failures and run cheap checks before another remote checkpoint. |
| Seasonal/DexNav within that job | 5m04s; 288 scenarios / 73,728 creations | Main gameplay sweep; not the Eon feature itself. Keep coverage and approved animation checks. |
| Actual Eon Debug battles / normal Release Continue | 26s / 10s | New feature checks were a small part of final runtime. |
| Patch job [40628689473](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/40628689473) | 9m56s; another 4m28s Debug + 2m33s Release, clean base 1m48s | Duplicate compilation exists across native/patch jobs. They overlap in wall time; do not sum them as a 25-minute wait. |
| Project checks [40628689748](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/40628689748) | 55s | Keep the broad inexpensive safety net. |
| Wiki [40628689620](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/40628689620) | 3m15s; browser setup 25s, layout 68s, seasons 83s | Dependency setup is not the dominant cost in this sample. |
| Windows [40628689486](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/40628689486) | 2m11s | Unchanged remote-content wrappers rebuild on wiki data edits by established policy. |

Successful candidate native QA took another 15m34s. Nine failed Eon-development native runs precede that success in the recent 100-run sample; their run windows total roughly 50 minutes before successful candidate/production gates. Some failures were fixture problems, and one exposed a real graphics allocation defect. They are not all game regressions, and those run durations do not measure total chat/developer time. Current evidence does not prove the app caused or stopped these jobs.

## Changes applied

- Added PR-only cancellation to native, project and wiki checks. Workflow-specific groups prevent cross-workflow cancellation; master groups include commit SHA and retain every production gate. Existing test commands and coverage remain intact. [GitHub concurrency semantics](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency).
- Added a standard-library live-release verifier and focused HTTP regression tests. Replaces repeated disposable download/hash scripts, checks all expected files concurrently, retries transient network failures once, rejects stale/corrupt/missing bytes and writes a machine receipt even on failure. It deliberately does not replace native tests or either clean-base decoder.
- Added [the start-to-finish procedure](../DEVELOPMENT-PROCESS.md) and durable AGENTS guidance: targeted history reads, immutable evidence reuse, fixture-first diagnosis, bounded status polling, persistent checkpoints and one release closeout.
- Updated stale “current” QA/save-policy pointers (previously v0.0.57/v0.0.60) to verified v0.0.75 and corrected the grotto extension's obsolete unshipped heading. Historical evidence and unverified playtest limits remain.

The handoff is about 124 KB: rereading it in full on every resumption recreates investigation. Keep history intact, start at the latest entry and follow only affected links. The previous closeout also had to reconstruct scripts lost from `/tmp`; checked-in tooling and durable provenance avoid that recovery cost.

## Further improvements to stage separately

| Opportunity | Expected benefit | Required proof before adoption |
| --- | --- | --- |
| Reuse one build within native and patch verification | Remove about seven duplicate runner-minutes per candidate/production phase in this sample; wall-time gain depends on job layout | Keep game binaries on the same ephemeral runner; do not upload/cache full ROMs publicly. Preserve Debug/Release distinctions, exact hashes, both decoders, provenance, failure artifacts and native coverage. Rework the workflow dependency graph in a focused follow-up. |
| Parallelize independent native scenario groups | Shorter five-minute seasonal sweep | Preserve all 288 cases, independent emulator state and deterministic seeds, approved icon geometry/animation assertions, complete receipts and CPU/memory bounds. Measure first; do not just reduce cases or frame waits. |
| Reuse candidate evidence for unchanged merged inputs | Avoid an identical second sweep in carefully proven cases | Requires an enforced manifest of all ROM/build/harness inputs, merge-tree checks, artifact integrity and clear trust/publication gates. Current automatic production gates were retained. Matching VERSION alone is insufficient. |
| Rebuild companion installers only for native wrapper/icon changes | Avoid new installers for remote-content-only edits | Android/Windows READMEs explicitly prescribe content-triggered rebuilds. This is a policy option, not applied by this audit; preserve package/signing/update checks. |
| Stage the site and matching patches behind completed release gates | Reduce manual coordination and the interval where frontend version labels and downloads differ | On v0.0.75, patch Pages finished at 03:58:08 UTC and production native at 04:02:32; candidate QA had already passed. Publish matching frontend/manifest/patches together after required gates, preserve old downloads until promotion, and test interrupted/retry paths. This audit retained the existing publisher. |
| Pin/cache build and browser dependencies | More consistent setup and fewer upstream surprises | Use measured misses, complete source/compiler/OS keys and a reproducible dependency lock. Do not cache copyrighted ROMs, bypass clean-base identity or adopt floating dependency upgrades as “optimization.” |

No percentage or guaranteed future session-time reduction is claimed. The immediate improvements prevent obsolete work, stale-state rediscovery and repeated manual closeout; the largest build/sweep reductions need separately verified engineering.

## Verification

Focused verifier tests cover exact bytes, stale equal-length data, truncation/oversize, transient retry, permanent 404, all-file reporting, BPS CRC failures, invalid/duplicate paths and replacing stale success with a failed CLI report. All eight tests passed locally and in project CI; the helper also verified all 18 actual live v0.0.75 files against the reviewed receipt. Maintenance commit `4b8eaa7a` passed project `40635448507`, full native Debug/Release `40635448486`, wiki/browser `40635448307` and Pages `40635448150`. Existing trigger filters/builds/test/upload commands were compared byte-for-byte after removing the scheduling block and new test step; no prior check was removed. [Current handoff](../DEVELOPMENT-HANDOFF.md). PR cancellation expressions are reviewed against GitHub's documented semantics; deliberately racing test PRs was not performed.
