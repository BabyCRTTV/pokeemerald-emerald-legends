# Refined Quest Log and Achievements — v0.0.56

The owner chose native concept A: “I like A the most! Let's implement it.” Implementation and publication are authorized after verification. Native fonts, existing palette/window, filter tabs, alternating paper rows, header counter and plum selection are retained. Six rows remain visible. Production spacing leaves both help lines within 240×160. Details retain all objectives, descriptions, progress, rewards and claim/full-PC messages. Exploratory B/C and truncated A details are excluded.

No save structures, catalogue order, persistent IDs, readers, artwork, wardrobe, seasons, bedroom or homecoming scripts changed. No migration or added save-time work is needed. Historical-save fixtures and broader Pizza Boy playtests remain unfinished.

The interruption cleared temporary preview/build files before a release commit. Restored the selected design from captured code instructions; focused real-renderer/input and backend checks passed again. Fresh builds, native screenshots, full checks and publication verification are pending. Earlier preview claims are historical; fresh evidence will be pinned separately. Never distribute private QA ROMs.

Final native comparison exposed an opening DMA race: Draw queued the tilemap before PutWindowTilemap finished populating it. Initial footer rows could remain blank until input. Populating the map before Draw fixes the ordering with no extra buffer or saved state. Added host ordering and native first-open footer checks; final builds and captures are being rerun.
