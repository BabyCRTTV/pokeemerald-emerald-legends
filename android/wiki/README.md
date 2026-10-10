# Pokémon Emerald: Legends Wiki — Android companion

A minimal Android WebView companion for the manually maintained wiki:

https://babycrttv.github.io/pokeemerald-emerald-legends/wiki/

This is a **separate Android app**, not an emulator, patcher, game modification or part of the ROM build. It has no connection to game saves, assets, or gameplay. Its only requested Android permission is INTERNET.

## Updates

The app loads the live GitHub Pages wiki over HTTPS, including the articles JSON. **Wiki content changes only when the project owner explicitly requests a refresh**. Content-only changes appear in the already installed app whenever it reloads the site. The Android APK is rebuilt and versioned whenever the owner revises wiki content, even though the live site itself already reflects the new articles.

APK builds are independently versioned from the game. The default GitHub workflow creates a signed development APK for sideloading. Android may require uninstalling the previous app before installing a future native rebuild because GitHub runner debug-signing keys are not persistent. This does not affect the live article update behavior. For seamless signed native APK upgrades, configure a privately held persistent signing keystore in GitHub Actions and switch to a signed release artifact. Do not commit private signing keys to the repository.

## Building

Requires Java 17, Android SDK Platform 35, Build Tools 35.0.0 and Gradle 8.10.2.

```bash
gradle --project-dir android/wiki :app:assembleDebug --no-daemon
```

The independent workflow builds, verifies and publishes the app to `docs/downloads/Emerald-Legends-Wiki.apk`. It triggers on owner-edited wiki files and Android source changes, **not** on ROM releases. Published installer and version-manifest commits from github-actions[bot] are skipped.

The WebView disables file/content access and mixed HTTP content and opens out-of-wiki links in the system browser. There is no JavaScript bridge, no app accounts, and no analytics SDK.

## Installing and updating

The app's **Update** header action checks the published `docs/wiki/android-version.json`, compares numeric build versions, and says when you already have the newest release. The website's **Update Wiki** menu performs the same check when it can identify this app by its user-agent suffix. Android always requires approval before installing an APK.

**Signing warning:** the initial builds use ephemeral runner debug signatures. Android cannot install a different-signed APK over an existing app of the same package name. Configure a persistent private release-signing keystore once for seamless future in-place updates. Required GitHub Actions secrets: `WIKI_ANDROID_KEYSTORE_BASE64` (base64 of the keystore), `WIKI_ANDROID_STORE_PASSWORD`, `WIKI_ANDROID_KEY_ALIAS`, and `WIKI_ANDROID_KEY_PASSWORD`. Never put the keystore or password in the public repository. Until configured, the update prompt explicitly warns that an uninstall might be necessary.

The application icon is extracted from the project Happiny icon sheet by `tools/build_wiki_icons.py`; the generated asset is transparent and contains exactly one sprite. Only INTERNET permission is requested.
