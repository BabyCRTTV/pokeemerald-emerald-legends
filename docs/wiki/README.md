# Pokémon Emerald: Legends — Player Wiki

This is a **manually maintained snapshot**, not a live mirror of the game's latest source files. The owner chooses when to update wiki content. New ROM releases are not supposed to change `articles.json` automatically.

## Reader URLs

- Site: `https://babycrttv.github.io/pokeemerald-emerald-legends/wiki/`
- Deep link: `/wiki/?page=kanto-gyms`
- Android companion: `../downloads/Emerald-Legends-Wiki.apk`, built by the separate wiki Android workflow.
- Windows installer: `https://github.com/BabyCRTTV/pokeemerald-emerald-legends/releases/download/wiki-desktop/Legends-Wiki-Setup.exe`, published as an independent public installer release.
- App update manifests: `android-version.json` and `windows-version.json`. The header's **Update Wiki** control compares the installed companion app version where available and informs users when already up to date.

The wiki is static HTML, CSS, JavaScript and JSON, runs without a login or backend, and uses no external CDNs or trackers. Readers can search the current article snapshot locally in their browsers. The companion Android app loads this same live site instead of embedding a permanently stale copy.

## Updating intentionally

1. Read `VERSION`, the changelogs, and the relevant actual source/documentation in the live repository.
2. Edit only affected articles in `docs/wiki/articles.json`, **including previously written articles** whose facts have changed. Remove obsolete statements, distinguish shipped vs planned, and preserve article IDs when possible.
3. Change `wikiRevision` / `reviewedAgainstGameVersion` below as part of an owner-requested content refresh, independently of the game release.
4. Validate JSON parsing, article IDs, links, mobile behavior, search, and rendering; deploy Pages.
5. Every owner-requested wiki revision triggers **new Android APK and Windows installer builds**. Their independent workflows version and publish the packages and their platform manifests after validation; the articles themselves are immediately readable online.

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

## Update and app-icon conventions

- The website shows **Update Wiki**, **LegendsDex** and a right-aligned search button instead of multiple install banners. The version checker uses a published manifest; ordinary browsers cannot reliably detect installed native applications.
- Each Android and Windows companion advertises its installed version to the wiki site. The app prompts users to download newer installers only when a greater published version is found. Installations remain user-approved.
- A transparent single-frame **Happiny** source sprite is used as the launcher and installer icon for both platforms. This does not alter the sprites shown *within* the LegendsDex.
- Android release signing requires private GitHub Actions secrets for seamless install-over-install behavior; without them the builder uses a temporary debug signature, and Android may require uninstalling the previous version. See `android/wiki/README.md`.
- Windows installers are built with the same stable NSIS application ID, optional desktop shortcut and launch-after-install choice. They are not code-signed yet; Windows SmartScreen may warn.

## Foldable and tablet display support

The companion pages use `fold-layout.css` after the original lavender styles. Navigation persists in folded and unfolded states. The Android wiki home presents direct Routes and Pokédex access, which links into the selected LegendsDex view. CSS uses viewport width and near-square aspect-ratio media queries; Android WebView uses the responsive viewport without forcing portrait orientation. No ROM files are modified.

## Reader polish and sprite audio (10 Oct 2026)

Home now presents seven topic sections; each section leads to its article list, with breadcrumbs back to the topic and home. Search still covers every article. Topic and article URLs support browser and Android Back/Forward navigation. LegendsDex's bottom navigation contains only Routes and Pokédex. The visible header shortcut opens LegendsDex from the wiki and changes to Back to guide inside LegendsDex. Native companions open LegendsDex first.

LegendsDex sprites are separate accessible audio buttons. Tapping a sprite plays the source game cry; the adjacent name/details button opens the profile. Only one cry plays at a time; leaving the page or closing the profile stops audio. Playback failures announce retry guidance. `tools/build_wiki_cries.py` verifies the 1,026 documented species' WAV files and generates default-form aliases. Audio loads only on tap from the project's own GitHub source at the same pinned snapshot commit as the sprites, including Da Bug; no third-party audio service is used.

The Android activity preserves its current page and filters while the window changes size, including folding/unfolding. The native application still loads the live reader, so existing installations receive these page improvements on reopening.


LegendsDex renders all matching Pokémon and routes at once. Bottom-tab switches preserve the current scroll offset. A fading, accessible up-arrow returns to the search field rather than the hero/header; reduced-motion settings disable animation. These behaviors are shared by browser, Android and Windows readers.

`tools/build_wiki_sprite_atlas.py` generates one lossless transparent sprite atlas and index from the manually pinned `dex-data.json.sourceCommit`. All 1,026 sprites preload and decode before results appear; scrolling does not fetch additional images or Pokémon. Regenerate the atlas only when the owner requests a data snapshot revision. Cries remain tap-to-load.

## Owner-requested review — 13 October 2026

Wiki 1.6.0 is reviewed against game v0.0.46 at `e542033cf4fcb8378c68fdd5ffbc4f5b5933fb64`. Chapters 19–25 finish the shipped Wing Survey, with its Hoenn intermission. Quest Log, achievements, storage, wardrobe and all eight visiting records are documented. The current encounter snapshot has 157 locations. ROM VERSION is unchanged. Both wiki and LegendsDex footers link to the project site; reader styles remain unchanged.

For an intentional encounter refresh, pin `dex-data.json.sourceCommit`, run `python3 tools/build_wiki_encounters.py`, and review the added maps and species metadata against that commit. Regenerate profiles, portraits and the sprite atlas using their existing tools. Mt. Ember tables use the Sevii expedition filter and deliberately have no mainland-map coordinates. Walkthrough blocks without an available regional marker use `showMap: false` while retaining their encounter panels and explanatory notes. Historical town counts retain their separate pinned provenance.

## Owner-requested preview — 17 October 2026

Wiki 1.7.0 content was refreshed against published game v0.0.62 at `7c9b80a68ae67688b705dd0c63d8759573b01601`. Documented 63 quests, 130 achievements, thirty Birch/Devon requests, tracked objectives, bedroom/family changes and Living Hoenn conversations. The original theme/layout and the 25-chapter structure were preserved. Article-level review fields retain earlier provenance for unchanged content. Historical town counts remain pinned independently.

LegendsDex 1.3.0 adds centered season/time badges and a season selector when seasonal variants exist. Published ordinary encounters currently have no time-of-day restriction (`OW_TIME_OF_DAY_ENCOUNTERS FALSE`); they are labeled All day. All seasons is used where no seasonal restriction exists. Profiles include the same availability metadata and do not duplicate year-round residents across seasons.

The current encounter snapshot is pinned to game v0.0.67 source `0d13f23794686525203fcfe3f8c6496e6921d2f2`. It includes seasonal land on Routes 101–104 and 110–121, plus Surf on 105–109: all 84 native tables. Native entries, earlier variants and all species/art remain preserved. Original residents occupy 70% of seasonal land encounters or 65% of Surf; visitors occupy 20%/10% on land or 30%/5% on Surf. Other methods remain unchanged; each individual season/method totals 100% and is All day.

Original map/species/icon/portrait inputs were checked unchanged from the prior v0.0.66 snapshot before advancing their matching source pins; no approved artwork was regenerated. Atlas/profile script URL keys match the new source pin so newly loaded pages request matching metadata alongside the no-store encounter JSON. The reader regression enforces this dependency on both Dex and guide pages and checks all eighty-four seasonal route/method views and twenty-one All Seasons unions. Walkthrough panels show actual invariant year-round resident shares (65% Surf / 70% grass on seasonal routes) and direct readers to LegendsDex for full seasonal rosters/rates. A shipped-JS regression covers all 409 methods; existing layouts, styles and approved artwork were preserved. Historical article/town-stat review provenance and independent wiki/app versions remain separate. The preserved `preview-inputs/seasonal-encounters.h` remains historical input, not game source.

The owner approved this wiki preview on 18 October 2026. After gameplay PR #78 merged and both live v0.0.63 patches were independently verified, the matching snapshot was intentionally promoted to Published. Reader navigation/audio checks and the published-preview-notice assertion passed. This metadata/status promotion preserved the approved reader layout, art, wiki/app versions and existing Android/Windows signing identities; it did not rebuild companion binaries or modify ROM code/patches. [Promotion receipt](../qa/wiki-seasonal-v0.0.63-promotion.json).

## LegendsDex 1.4.0 — All Seasons

The season filter includes **All Seasons**, shareable with `dex.html?season=all`. It shows the union of seasonal entries rather than the older native fallback table. Identical species/level/rate/time rows appear once with combined availability; differing tuples stay separate. Each displayed share belongs to its listed seasons and is never summed or averaged. Route headings explain this. Individual-season views still total 100%; All Seasons is an availability view, not a combined probability distribution. Route rows and species profiles use the same union helper, including safe native fallbacks for absent/empty variants. The changed reader script has its own revision cache key. Existing wrappers load the live feature; the existing companion workflows handle any resulting package builds and publication independently.

## LegendsDex 1.5.0 — grotto review

The owner requested compact **Sevii** and **Grotto** region chips and removal of the “Updated on request” hero tag. The dedicated Grotto filter indexes Leafshade Hollow, Stillwater Nook and Rainroot Hollow, with four seasonal pools, levels and exact visitor-selection shares. These are visible single encounters, rather than random grass encounters; capture or defeat starts a separate 4,500-step cooldown. An active visitor persists through fleeing, losing and season changes.

The three supplementary tables are generated from `src/data/legends/grotto_encounters.json` by `tools/legends/build_grotto_encounters.py`, with a separate `grottoSource` manifest hash and review status. The ordinary 157-location v0.0.67 source pin and matching approved atlas remain unchanged. This supplement is unshipped on the grotto review branch; it does not assert that grotto encounters are available in the current public ROM. The ordinary encounter importer preserves this supplement, and the profile generator records grotto entrances without inventing mainland-map coordinates.
