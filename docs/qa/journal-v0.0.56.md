# Refined Quest Log and Achievements — v0.0.56

Status: **published and verified**, through [PR #71](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/71). [Native preview](journal-v0.0.56-preview.png) · [Build/native/public receipts](journal-v0.0.56-public.json).

## Approved result

The owner chose A: “I like A the most! Let's implement it.” The shipped design retained six visible rows, filter tabs, alternating paper rows, plum selection, cream text, the separate pointer and claimed markers. MAIN / SIDE / DONE and ALL / READY / CLAIMED retained the existing filters. The entry counter moved to the header, and both help lines fitted within 240×160. Details retained every objective, description, progress, reward and claim/full-PC message. Exploratory B/C variants and truncated details were excluded.

Manual one-time berry claims, PC Item Storage confirmations, atomic full-PC retry, field unlock overlays and catalogue order stayed intact. No serialized fields, capacities, persistent IDs, readers, artwork, wardrobe, seasons, bedroom, homecoming scripts or gameplay rules changed. No migration or added save-time work was needed. AGENTS.md was reviewed; its standing rules remained applicable without a new policy change.

## Opening repair and verification

The final native comparison exposed an opening DMA race: Draw queued the tilemap before PutWindowTilemap finished populating it. Initial footer rows could remain blank until input. Populating the map before Draw fixed the ordering without another buffer or saved state. Host ordering and native first-open footer checks cover this repair.

All 49 merged project-check blocks passed, including the renderer/input, backend/claims, save compatibility, wardrobe, appearance and seasonal regressions. Final PR checks/builds and production Debug/Release builds/BPS checks passed. The PR recorded earlier local checks, but temporary captures/structured receipts were not committed before interruption. This follow-up regenerated both normal ROMs from the unchanged merged source and verified exact equality with the production target hashes before recapturing native evidence.

Fresh controlled mGBA 0.10.2 checks passed for both variants. Fourteen screens matched exactly between Debug and Release: first-open, selection, scrolling, complete Details/back, filters, claimed markers, a real second manual reward claim, PC confirmation and timeout. The first claim is a prepared rendering fixture; Release seeds that fixture directly because LTO removes Debug setup helpers. The next claim uses actual native input. Selected images were visually reviewed and enlarged exactly 2× without changing native pixels. Private diagnostic ROMs, ELFs and saves were excluded.

## Publication

PR #71 merged as `8d7a8d56ad60064cf6fb8a3e16bc2e487353d61f`; tested head `52d234fe9c0d9f589c06935a77601d65f9cac022` has the same runtime tree. Production [38796200927](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38796200927) built both variants, verified canonical clean Emerald, reapplied both generated patches and committed them as `ee20772873a7073d636fa331790b4cc798c33e5f`. Patch [Pages 38797205338](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38797205338) succeeded. An earlier merged build was superseded/cancelled; it was not a compiler failure.

Both live patches, checksum manifest, homepage, changelog and patcher returned HTTP 200 and matched committed bytes. A freshly rebuilt clean Emerald matched canonical SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`. Floating IPS and independently the downloaded browser decoder reconstructed the exact normal ROM hashes: Release `f180616dd87f21b0a8148e019c164a8c2697fd633f3a13ca5d7806c6e77d3a1e`; Debug `8f14e84fe0ec0f3c6c421ec941e5889acae8c7afd640f3bca4a55e280a703bb0`. Relative to v0.0.55, the Release patch grew 451 bytes and Debug shrank 232 bytes. VERSION, three changelogs, Options/title labels and site/patcher stayed synchronized.

Broader natural traversal, historical-save fixtures and Pizza Boy remain unfinished. No publication blocker remains for this approved menu update. The developer-site visual refresh stays deferred.
