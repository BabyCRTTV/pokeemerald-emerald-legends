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

The current version is `0.0.4.2`.

Each meaningful shipped change normally advances the final development revision by one:

- `0.0.1`
- `0.0.2`
- `0.0.3`
- `0.0.4`
- `0.0.4.1`
- `0.0.4.2`

A fourth segment such as `0.0.3.1` may be used for a very small follow-up build or correction when that communicates the relationship more clearly than advancing the normal revision.

Larger milestone numbering can be introduced later as the project approaches a stable 1.0 release.

## Build variants

A project version can publish two variants without consuming separate version numbers:

- **Release** - recommended player build. Built with the expansion's release configuration so developer/debug entry points are disabled.
- **Debug** - developer/testing build from the same source revision. It retains the expansion's debug menus, Pokémon sprite visualizer, and title-screen Quickstart.

The Debug filename receives a `-debug` suffix, and its in-game Options version receives a `-D` suffix. Gameplay/content changes remain synchronized between the two variants.

## Changelog rule

Every version bump must update all three changelog records in the same development change:

- `CHANGELOG.md` - canonical full project history
- `CHANGELOG-RELEASE.md` - player-facing Release history
- `CHANGELOG-DEBUG.md` - developer-facing Debug history

The website changelog mirrors the Release and Debug views behind separate tabs. Shared changes appear in both variant logs; build-specific differences are called out explicitly. If a version has no variant-specific divergence, that should be stated rather than omitted.

A changelog entry should describe player-visible changes first, followed by notable technical, site, tooling, or maintenance changes when relevant.

## Release rule

Both public BPS patches are generated from the current `VERSION` value. The automated release workflow independently applies each patch to the supported clean Emerald base and verifies that it reproduces its corresponding compiled Legends ROM byte-for-byte before publishing it to the site.
