# Legends Wiki — Windows companion

This is a standalone, browser-based desktop reader for the public wiki and LegendsDex. It does not include or modify a Pokémon ROM, save file, emulator, or game code.

The installer is the public `Legends-Wiki-Setup.exe` attached to the repository's separate **wiki-desktop** release. It uses a wizard to choose the installation location, optionally create a desktop shortcut, and run the program after installation. Reinstalling over an older version retains the same application ID.

The wiki website and app's **Update Wiki** button check `docs/wiki/windows-version.json`. A matching installed version receives the message that it is current; older versions offer the newer installer in the browser. Windows still asks the user to run and approve the setup. The site itself receives article updates on reload.

Builds happen independently on Windows GitHub Actions whenever owner-edited wiki content or desktop app source changes. The app shows Happiny's real, single-frame transparent sprite, generated locally from `graphics/pokemon/happiny/icon.png`. Large desktop binaries are published as release assets rather than Git blobs.

The program uses Electron with sandboxed renderer, context isolation, disabled Node integration and external-browser handling for off-site URLs. It requires network access, no account, and no invasive permissions. It is currently **unsigned**, so Windows SmartScreen may warn about the unknown publisher.
