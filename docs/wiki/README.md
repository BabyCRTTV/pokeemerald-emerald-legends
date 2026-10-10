# Pokémon Emerald: Legends — Player Wiki

This is a **manually maintained snapshot**, not a live mirror of the game's latest source files. The owner chooses when to update wiki content. New ROM releases are not supposed to change `articles.json` automatically.

## Reader URLs

- Site: `https://babycrttv.github.io/pokeemerald-emerald-legends/wiki/`
- Deep link: `/wiki/?page=kanto-gyms`
- Android companion: `../downloads/Emerald-Legends-Wiki.apk`, built by the separate wiki Android workflow.

The wiki is static HTML, CSS, JavaScript and JSON, runs without a login or backend, and uses no external CDNs or trackers. Readers can search the current article snapshot locally in their browsers. The companion Android app loads this same live site instead of embedding a permanently stale copy.

## Updating intentionally

1. Read `VERSION`, the changelogs, and the relevant actual source/documentation in the live repository.
2. Edit only affected articles in `docs/wiki/articles.json`, **including previously written articles** whose facts have changed. Remove obsolete statements, distinguish shipped vs planned, and preserve article IDs when possible.
3. Change `wikiRevision` / `reviewedAgainstGameVersion` below as part of an owner-requested content refresh, independently of the game release.
4. Validate JSON parsing, article IDs, links, mobile behavior, search, and rendering; deploy Pages.
5. A content-only wiki update never requires rebuilding the Android APK. A change to native Android UI/security behavior does.

## Wiki scope

The articles summarize documented mechanics, and distinguish current Kanto gameplay from design plans. For engineering details consult `docs/features/` and `docs/QA.md`. Do not distribute ROMs here.

## Accessibility and privacy

No account or tracking is present. The interface uses system fonts, keyboard navigation, semantic heading levels, focus indications, readable contrast, and responsive layouts. APK permission is internet access only. Device-file access and JavaScript-to-native bridges are not enabled in the Android WebView.

## Interactive route encounters and National Pokédex

The independent `dex.html` guide uses `dex-data.json`: a manually reviewed snapshot of the active Legends wild encounters and National Pokédex species metadata. It provides mobile-friendly route cards, encounter methods, source sprites, combined per-method slot weights, level ranges, type/stats where parsed, and searchable Pokémon profile locations.

**Correct probability interpretation:** the displayed rate is the species' *relative share of encounters for the selected method*, **not** the chance of finding it per step. The `encounter_rate` engine values are separate. Old/Good/Super Rod tables are evaluated independently.

`dex-data.json` was built directly from `src/data/wild_encounters.json`, `include/constants/pokedex.h`, and `src/data/pokemon/species_info/*_families.h`. Only active Emerald encounter tables and the explicitly imported Legends Kanto tables are indexed. The old upstream FireRed/LeafGreen encounter tables for routes that aren't playable in Legends are excluded. Altering Cave's extra special rotation sets are not all presented as simultaneously active.

No game update automatically rebuilds this snapshot. On an owner-requested wiki update, regenerate and verify against the new source game revision, check aliases and new scripted encounters, and only then advance the wiki's documentation revision. The game version in `VERSION` is never changed by the wiki.

Sprites load from the project's own public GitHub source art at the snapshot commit (HTTPS), and the UI uses graceful fallbacks if an image is missing. There is no requirement to download additional ROM content.
