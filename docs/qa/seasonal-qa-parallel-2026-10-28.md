# Isolated seasonal QA workers — 28 October 2026

Model: GPT-6 (Codex) | Reasoning: run independent native scenarios concurrently while retaining exact coverage, diagnostics and a measured serial reference.

Baseline: published v0.0.75 and completed process maintenance at `94afb7d6fff5183a316fdec226f131042b4a5191`. Owner authorized the first optimization only: parallel seasonal QA. Build sharing and publisher redesign remain separate work.

## Scope and invariants

The original 288-scenario list, private ARM callback, 256 real creations per case, RNG seeding, per-case emulator reset, frame waits, input sequence and every native icon/palette/geometry/animation/protected-state assertion remain unchanged. The C host adds optional start/end indices while preserving its original full-range command. Contiguous disjoint ranges run in separate mGBA processes, with a separate output directory for each. The parent shares only the read-only private diagnostic ROM; mutable emulator state is process-local.

The default is at most four workers, capped by available CPU affinity. Each worker has a ten-minute timeout. The parent requires exact ordered PASS IDs for its range and a native GUI capture for every case, rejects unexpected/failure captures and retains all sibling outcomes after a failure. Global logs merge in original scenario order; accepted PNGs and verification.json remain in their existing locations. Worker logs, execution receipts and optional serial captures are retained by Actions; no ROM or battery save is exported. Old success receipts/captures are invalidated before a local rerun.

Game source, route/season tables, maps, approved sprites/artwork, wardrobe, serialized saves, VERSION and published patches are unchanged. Existing Debug/Release builds, Eon/boat/grotto/wardrobe checks and ordinary project checks remain. The existing v0.0.75 build/patch evidence applies to identical game inputs; this change creates no new game release.

## Validation and operation

- Nine local host-independent tests passed: partition boundaries, CPU cap/serial override, actual overlapping processes with distinct PIDs, global log order, missing/duplicate/out-of-range cases, missing/unexpected captures, failure diagnostics and sibling completion, timeout rejection, exact serial/parallel captures/logs and stale-output rejection.
- Python syntax, YAML and diff whitespace passed. Reviewed the native per-case C body and ARM callback against the baseline; no assertions or scenarios were removed.
- The initial implementation commit opts into a full same-runner serial reference through `[benchmark seasonal QA]` in its message. CI must require all 288 cases / 73,728 creations in each mode, exact merged native logs and byte-identical raw captures, then record serial/parallel execution times and the actual speedup. This benchmark remains pending until its native receipt is inspected.
- Future normal runs use only parallel execution. Run `python3 tools/legends/native_seasonal_encounters_qa/run.py --jobs 1` for serial troubleshooting, or add `--compare-serial` for full parity/timing validation. The native workflow also exposes a manual boolean `compare_serial` input. The benchmark commit-message marker is only a validation opt-in, never a waiver of tests.

See [the machine evidence and current status](seasonal-qa-parallel-2026-10-28.json) and [development handoff](../DEVELOPMENT-HANDOFF.md). Do not report a measured runtime improvement or completed native parity until the actual CI results are verified. This retains controlled Debug seasonal/DexNav coverage; it does not add native Release seasonal hunts, authentic historical-save testing, a full story playthrough or Pizza Boy validation.
