# Developing Legends without repeating completed work

Quality gates protect the game; repeated investigation and discarded evidence do not. This procedure preserves current candidate/production builds, native gameplay, save compatibility, approved artwork and independent BPS reconstruction. [Measured audit and deferred improvements](qa/development-process-2026-10-28.md).

## Resume and scope

1. Read AGENTS.md, VERSION, the newest handoff entry and its linked QA receipts. Batch live head/recent commits, relevant PR, releases and Actions reads through the GitHub connector. Pin source reads to that head. Read older entries only for an affected dependency, approval or outstanding issue; historical headings in QA/roadmap files are not the current release state.
2. Preserve an existing checkout's edits. Fetch once and use an isolated checkout when needed; do not repeatedly reclone the asset-heavy repository or reset work from another session. Inspect current head again before a remote write and use an expected-head lease.
3. Write a small impact list: entry conditions, shared state/IDs, event priorities, save/Continue, rewards and retry paths materially connected to the change. Preserve owner maps, art, wardrobe and seasonal systems. Do not turn a route addition into an unrelated project redesign.

## Implement and check

| Change | First checks | Release evidence |
| --- | --- | --- |
| Handoff, QA or process documentation | Links, claims and focused script/workflow checks | Existing unchanged game evidence remains valid; no game-version bump or new BPS solely for documentation. |
| Encounters or ordinary game logic | Affected production-C tests and related event/save/UI checks | Both builds, focused native interactions, existing automatic regressions and both independent patch decoders. Sync relevant wiki rosters. |
| Persistent data or progression | Layout/ID and legacy-reader review; deterministic old/current/repeated-initialization tests | Actual focused load/migrate/save/reload and normal Release Continue with provenance and explicit historical-save limits. |
| Art, wardrobe or rendering | Exact source/geometry/palette protection and affected compositor checks | Genuine compiled-game captures and affected interactions; obtain visual approval when required. Do not regenerate unchanged assets. |
| Companion website/app | Source/reader or platform checks for the changed component | Keep established content-triggered app rebuild policy until explicitly revised; ROM gameplay is not an app-only gate. |

Keep the inexpensive full host suite: the measured production run took 55 seconds. Before a remote checkpoint, run the affected cheap checks and inspect the diff. Batch related fixes into a coherent checkpoint instead of committing each speculative fixture adjustment and starting another native build. Existing required automatic gates still run; this procedure does not authorize skipping them.

When a native test fails, inspect its first failure, frame, log and runtime diagnostics before editing. Identify whether setup, fixture controls/obedience, game behavior or publication failed. Use established legal parties, trapping and cursor inputs. Re-run only a transient failed job; a deterministic failure needs a correction. Never change approved game behavior to accommodate a faulty test.

## Wait, retain and resume

- Poll relevant runs together roughly every 30–60 seconds with cache-busting API reads; request failing-job details only when needed. Compare progress to measured stage times before calling a long stage hung. Continue independent review/documentation while CI runs; do not silently disappear during setup.
- Superseded PR runs of native, project and wiki checks cancel within their own workflow. Master uses a per-commit concurrency group, so a later master commit does not cancel that verification gate. Never infer a pass from cancellation.
- Keep evidence tied to source/tree, build configuration, harness, artifact digest and ROM hashes. Download and verify a needed archive once, retain its extracted receipts/capture hashes locally and link the durable repository QA record. Re-extract only if absent, corrupt or a new comparison is needed. Do not publish ROMs or personal saves.
- Persist resumable scripts and costly evidence under the workspace's ignored build directory, with the immutable provenance in the repository QA record. `/tmp` alone is not a checkpoint. After workspace loss, recover only the artifacts needed for the next unverified step.
- Use one per-release evidence record plus a short handoff link. Record commit, run ID, last verified stage, blocker and exact next step at meaningful milestones. Do not append a new historical handoff section for every poll or copy full logs into it. Reuse completed evidence only when its relevant inputs are identical; document why it remains applicable. Harness edits invalidate harness evidence even if game code is unchanged.

## Seasonal native QA execution

The seasonal runner supports up to four isolated mGBA processes, capped by CPU affinity, with unchanged cases/assertions and strict complete coverage. Worker logs and receipts retain failures. Use `--jobs 1` for serial troubleshooting or `--compare-serial` for the complete serial/parallel log, pixel and timing comparison. Normal runs do not repeat a serial reference. The native workflow supports manual `compare_serial` input; `[benchmark seasonal QA]` in a push commit message also explicitly opts into that validation. [Implementation status and measured evidence](qa/seasonal-qa-parallel-2026-10-28.md).

## Publish and close

1. Inspect completed candidate gates and their actual receipts; compare native ROM hashes with both independently reconstructed BPS targets. Confirm that the merged tree preserves the reviewed inputs. Current production gates remain required; do not treat documentation differences as new game changes.
2. Wait for production gates, automatic patch commit, required companion publication and the corresponding Pages deployment. Batch status reads. App build success without the required signing identity is not published-APK success.
3. Prepare expected public file hashes from the reviewed Git blobs and verified patch/native receipts. For the v0.0.75 receipt format, run:

   ```sh
   python3 tools/legends/verify_public_release.py \
     --receipt docs/qa/eon-roamers-v0.0.75-public.json \
     --output build/qa/v0.0.75-live-recheck.json
   ```

   For a new release, first prepare its own expected receipt from that release's verified inputs. Never copy old expected hashes or derive expectations from the unverified live site. The helper checks every listed live file, exact SHA256/Git blob, size and BPS footer CRC; it bounds concurrency, network retries and timeouts, retains failures and exits nonzero. It does **not** apply patches, validate gameplay or decide whether CI passed. A CRC/receipt check cannot replace independent clean-base reconstruction.
4. Check the actual deployed bytes once after the relevant deployment. Recheck when publication changes those bytes or deployment is uncertain; avoid repeated full downloads during an unchanged deployment. Final documentation may add a receipt: verify its new public bytes after Pages, while retaining the already verified unchanged game/patch evidence.
5. Commit concise closeout evidence and report the released behavior, download link, checks and material limits. No new release version is needed for maintenance that leaves the game and download bytes unchanged.
