# Versioning Policy

Pokémon Emerald: Legends uses a deliberately fine-grained version sequence during active pre-1.0 development.

## Source of truth

The root `VERSION` file is the authoritative project version.

All player-facing locations should match it, including:

- the in-game Options menu
- the project website
- the browser patcher
- release patch and generated ROM filenames
- the README
- the changelog

## Pre-1.0 cadence

The current baseline is `0.0.1`.

Each meaningful shipped change normally advances the final development revision by one:

- `0.0.1`
- `0.0.2`
- `0.0.3`
- `0.0.4`

A fourth segment such as `0.0.3.1` may be used for a very small follow-up build or correction when that communicates the relationship more clearly than advancing the normal revision.

Larger milestone numbering can be introduced later as the project approaches a stable 1.0 release.

## Changelog rule

Every version bump must update `CHANGELOG.md` in the same development change.

A changelog entry should describe player-visible changes first, followed by notable technical, site, tooling, or maintenance changes when relevant.

## Release rule

Public BPS patches are generated from the current `VERSION` value. The automated release workflow verifies that applying the patch to the supported clean Emerald base reproduces the compiled Legends ROM byte-for-byte before publishing it to the site.
