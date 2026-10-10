# Pokémon Emerald: Legends Wiki — Android companion

A minimal Android WebView companion for the manually maintained wiki:

https://babycrttv.github.io/pokeemerald-emerald-legends/wiki/

This is a **separate Android app**, not an emulator, patcher, game modification or part of the ROM build. It has no connection to game saves, assets, or gameplay. Its only requested Android permission is INTERNET.

## Updates

The app loads the live GitHub Pages wiki over HTTPS, including the articles JSON. **Wiki content changes only when the project owner explicitly requests a refresh**. Content-only changes appear in the already installed app whenever it reloads the site. No native APK rebuild is needed for content updates.

APK builds are independently versioned from the game. The default GitHub workflow creates a signed development APK for sideloading. Android may require uninstalling the previous app before installing a future native rebuild because GitHub runner debug-signing keys are not persistent. This does not affect the live article update behavior. For seamless signed native APK upgrades, configure a privately held persistent signing keystore in GitHub Actions and switch to a signed release artifact. Do not commit private signing keys to the repository.

## Building

Requires Java 17, Android SDK Platform 35, Build Tools 35.0.0 and Gradle 8.10.2.

```bash
gradle --project-dir android/wiki :app:assembleDebug --no-daemon
```

The independent workflow builds, verifies and publishes the app to `docs/downloads/Emerald-Legends-Wiki.apk`. It triggers only for the wiki's Android source/workflow changes or a manual dispatch, **not** on ROM releases or article changes.

The WebView disables file/content access and mixed HTTP content and opens out-of-wiki links in the system browser. There is no JavaScript bridge, no app accounts, and no analytics SDK.
