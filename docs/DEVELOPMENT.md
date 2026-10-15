# Development Guide

## Repository model

Pokémon Emerald: Legends should remain a normal fork/derivative of `rh-hideout/pokeemerald-expansion` so upstream changes can be incorporated deliberately.

Start with [DEVELOPMENT-HANDOFF.md](DEVELOPMENT-HANDOFF.md), the live default branch, recent PRs/Actions and published files. The [15 October 2026 audit](qa/project-state-2026-10-15.md) records the verified v0.0.54 baseline and remaining work. Preserve accepted assets, existing save compatibility and completed systems when resuming.

Recommended remotes for local development:

```text
origin   -> BabyCRTTV/pokeemerald-emerald-legends
upstream -> rh-hideout/pokeemerald-expansion
```

## Branch strategy

- `master` - current playable development line
- `feature/<name>` - larger gameplay features when isolation is useful
- tags/releases - milestone snapshots using the current `VERSION` value

Small, well-contained changes may be committed directly to `master` during early development, but each commit should describe one logical change whenever practical.

Use the connected GitHub tools for repository writes. Inspect the current branch head before committing, and use an expected-head lease when updating it. Record important decisions, exact source/build evidence and unresolved work in the handoff; detailed QA belongs in linked records.

## Legends-specific code

Prefer these patterns:

1. Use existing expansion configuration options when they already solve the problem.
2. Add Legends-specific configuration flags for behavior that should remain optional.
3. Keep new systems modular rather than scattering unrelated logic across many engine files.
4. Document every substantial custom mechanic in `docs/features/`.
5. Note any upstream files that require invasive edits so future expansion updates can be reconciled carefully.

## Build artifacts

Do not commit generated ROMs, copyrighted ROM data, save files containing personal information, or temporary build output that upstream excludes.

## Versioning

The authoritative project version lives in the root `VERSION` file.

Read it when starting work instead of relying on a duplicated version label in this guide. Full release history is retained in the root [changelog](../CHANGELOG.md); development numbering and variant rules are defined in [VERSIONING.md](VERSIONING.md).

Every version bump must update the canonical, Release and Debug changelogs, Options, README, website and browser patcher together. Write completed changes in past tense. Documentation-only handoff maintenance does not require a new ROM version or replacement patches.

Keep the ROM release number separate from the wiki's revision and last manually reviewed game version. The wiki is updated when requested; a ROM release does not authorize automatic wiki synchronization. Game BPS files/checksums are published under `docs/downloads/`; the `wiki-desktop` prerelease is a separate companion installer.

## Quality checks

Backward save compatibility is a release requirement: previously published Legends battery saves must continue into newer updates without losing Pokémon, inventory, progress or settings. The owner's 14 October 2026 decision supersedes earlier permission to disregard older saves. Follow [SAVE-COMPATIBILITY.md](SAVE-COMPATIBILITY.md) for the current format boundaries, migration requirements and focused validation. Every PR must state its save impact; a breaking change without a verified migration blocks publication.

Use the runnable steps in [the project-check workflow](../.github/workflows/legends-checks.yml) for the current regression inventory. They cover native C modules, event progression, appearance/asset protection, save/storage compatibility, browser patching and synchronized metadata. Run checks appropriate to the change and investigate failures.

The [release workflow](../.github/workflows/build-release-patch.yml) compiles native Debug and Release ROMs, builds and verifies clean Emerald, independently applies both BPS patches and compares the results byte-for-byte before publishing. Confirm the final commit, Actions, Pages deployment and public download hashes before reporting publication. Documentation-only changes can retain the last verified ROM build when the runtime inputs are unchanged.

The [QA checklist](QA.md) and linked milestone records distinguish host checks, sprite-buffer previews, controlled emulator scenes and uninterrupted gameplay. Keep those distinctions explicit; passing CI does not complete the remaining manual playtests.
