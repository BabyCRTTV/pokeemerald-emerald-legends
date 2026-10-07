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
- tags/releases - milestone snapshots such as `v0.1.0`

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

Development begins at `0.1.0-dev`.

Milestone releases use semantic-style project versions:

- `0.1.0-dev` - active development
- `0.1.0` - first completed milestone
- `0.1.1` - fixes to the milestone
- `0.2.0` - next feature milestone
