# Pause-menu world panel

The overworld Start menu shows a small native Emerald window at the bottom left.

- Clock: local RTC time, using the bedroom clock offset, in 12-hour AM/PM format. This is real time in both seasonal modes, not accumulated playtime. Before setting the bedroom clock, the default local offset applies. Invalid/unavailable RTC shows `--:--`.
- Weather: a pixel silhouette for sun, cloud, rain, thunderstorm, snow, fog, ash, sand or water. Uses the active native weather, preserving volcanic and story weather. Indoor/cave/secret-base maps show a shelter icon; underwater shows a droplet.
- Season: the active displayed season, including in gameplay mode. This panel does not commit pending seasonal changes.

Implementation lives in `src/legends_start_menu.c`, with show/update/hide hooks in the native Start menu. The 12×4-tile window uses BG0/palette15 and tiles 0xC0–0xEF, below the map-name popup and away from action, save, counter and dialog graphics. Icons reuse the native text palette (gray, warm gold, blue and light blue) and require no sprites or palette changes. The clock has a static L-shaped pair of hands. RTC sampling is limited to once per 60 menu frames; unchanged snapshots do not redraw text. Weather animation alternates two frames every 30 menu frames: sun shimmer, falling rain/ash, drifting snow/fog/sand, a dimming lightning bolt and water shimmer. Clouds and shelter icons stay still. Animation clears only the 12×12 weather icon, copies the window graphics and performs no RTC reads.

Save and retire dialogs hide the panel before presenting confirmation text. Submenus, DexNav, link Trainer Card and menu closure release it; returning to the menu recreates it. Window allocation failure leaves the normal menu usable.

Regression: `python3 test/legends-start-menu.test.py` compiles the actual module against engine mocks. Emulator QA should cover indoor/outdoor weather, minute rollover, both animation frames/colors, all four seasons, Safari/Pyramid counters, Debug/DexNav, Save cancel/success, and returning from each submenu.
