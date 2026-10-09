# Dynamic weather

v0.0.22 reuses the expansion’s native weather effects and smooth transition tasks. Most ordinary Hoenn towns and routes can be clear, rainy or occasionally stormy. Fortree and Routes 119–121 have a wetter climate. Routes 114–116 use a non-volcanic upland profile, with occasional winter flurries. Coasts and lowlands never receive random snow.

| Profile | Rain: spring / summer / autumn / winter | Thunder: spring / summer / autumn / winter | Fog | Snow |
| --- | --- | --- | --- | --- |
| Lowland/coast | 30 / 18 / 25 / 25% | 2 / 5 / 1 / 1% | None | None |
| Rainforest | 50 / 38 / 45 / 45% | 2 / 5 / 1 / 1% | 6%; 12% in autumn | None |
| Upland | 30 / 18 / 25 / 15% | 2 / 5 / 1 / 0% | 6%; 12% in autumn | 25% in winter |

Rainforest/upland fog gains 8 percentage points during the native morning and night periods. As of v0.0.25.1, clear weather fills the remainder. The former 18% cloudy share also uses clear weather: Emerald’s SUNNY CLOUDS sprites are fixed to Route 120 reflection coordinates and can show through elevated terrain on unrelated maps. Dynamic forecasts never select that effect. Each area uses its own regional forecast. These are forecast weights, not encounter probabilities.

A saved clock advances with recorded playtime, including menus and battles. Its 20-minute periods seed a local RNG using the daily seed, region and active season. Returning from buildings or continuing a save does not reroll the forecast within a period. A change in daily seed, active season or morning/night fog weighting can also change the result. Forecasts may legitimately repeat between periods. The clock wraps after 18 hours and continues independently of the native 999-hour playtime display cap.

An outdoor task checks once per second and lets the native weather task handle transitions. Dialogue, palette fades and unfinished weather transitions defer updates. Native battle weather mapping and effects are retained. Seasonal foliage still waits for a full faded map load; weather can change while walking.

Mt. Chimney, Jagged Pass, Fiery Path, Lavaridge, Fallarbor and Routes 111–113 preserve their native climate. Route 111 is protected as a whole because desert and grasslands share a map. Interiors, caves, secret bases, underwater, Frontier facilities, event islands and unconfigured regions are protected. Explicit no-weather, shade, ash, sandstorm, drought, downpour, special fog and Groudon/Kyogre weather remain native; Petalburg Woods retains its shaded canopy. The original map/script weather request is preserved separately.

The pause-menu panel identifies the active effect. Clear nights show a crescent moon with a twinkling star, using the same local day/night clock as the game palettes. Clear daytime shows the sun; rain, fog and snow keep their own icons at night. Native cloud effects and their icon remain available on protected maps. Scripted drought retains a sun icon.

Implementation: `src/legends_weather.c`, native weather task and the existing season/playtime clock. Var 0x40FF stores seconds and flag 0x26C marks initialization. Existing saves seed the clock from recorded playtime on first use; no save layout change. Saved cloudy forecasts are replaced on normal Continue/map initialization, or by the outdoor transition check after dialogue/fades finish; native cleanup destroys the old cloud sprites. Release and Debug share the same rules.

Validation: `python3 test/legends-weather.test.py` compiles the actual module and exhausts forecast rolls, checking all seasons, regional exclusions, dawn/night fog weighting, timer migration/rollover and transition guards. Pause-panel tests cover moon/day/effect selection and both animation frames. Emulator QA: explore ordinary towns, Fortree, Routes 114–116 and ocean routes across seasons; wait across a forecast boundary; enter/exit buildings and save/continue; check battle weather, native story weather, desert/ash, and moon appearance around the native night boundary.

Cloud regression QA: revisit Oldale and other towns with elevated door tiles; confirm no moving cloud/reflection sprites appear through the ground. Test a pre-0.0.25.1 cloudy save on Continue and after a normal map reload, and retain native cloud reflections on protected maps such as Faraway Island.
