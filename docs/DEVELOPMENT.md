# Development Guide

## Repository model

Pokémon Emerald: Legends should remain a normal fork/derivative of `rh-hideout/pokeemerald-expansion` so upstream changes can be incorporated deliberately.

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

Current version: `0.0.3`.

During active pre-1.0 development, each meaningful shipped change increments the development revision:

- `0.0.1` - initial baseline
- `0.0.2` - Release/Debug distribution split
- `0.0.3` - separate variant changelogs
- a fourth segment such as `0.0.3.1` may be used for a very small follow-up build when that is clearer than consuming the next normal revision

Every version bump must update the canonical, Release, and Debug changelogs and be mirrored in player-facing version text. See [VERSIONING.md](VERSIONING.md).
