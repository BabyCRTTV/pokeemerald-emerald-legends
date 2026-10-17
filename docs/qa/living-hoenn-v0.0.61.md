# A Living Hoenn — v0.0.61 QA

**Model: GPT-6 (High) | Logic: dependency-scoped branch reviews, existing signed research/season/story flags, then real ROM compilation and native mGBA emulator startup.**

## Implementation / protected state

Birch and Mr. Stone gained optional `RESEARCH NOTES`, without changing their two original menu actions, research claims or the Lucky Egg/Pokédex priorities. The Weather Institute first-floor second worker gained seasonal bulletin dialogue after the Aqua rescue, without changing Castform or unusual-weather events. Four ambient NPCs in Littleroot, Rustboro, Fortree and Lilycove acknowledge badge or Champion milestones. No serialized save layouts, new persistent variables, story flags, quest IDs, rewards, graphics, movement or approved art changed.

## Verified tests and publication

- [PR #76](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/76) merged as `b3782b54c912d864fae4df4e85896b693b265a52`. [PR project checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39050448266), [Debug/Release native builds plus BPS reconstruction](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39050448291) and [mGBA native smoke](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39050448294) passed.
- Production [project checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39050991111), [native compilation and BPS verification](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39050991073), and [mGBA native run](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39050991044) all passed at the merged commit.
- The actual unmodified v0.0.61 Debug ROM was loaded into the native mGBA 0.10.2 core. Its SELECT Quickstart reached the live `CB2_Overworld` callback, with two native 240×160 frame captures. [Production screenshot/receipt artifact](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39050991044/artifacts/12106824203) includes PNGs and metadata, never ROMs/saves. Debug ROM SHA-256 `9c061d1526966b20e2fc2755f4bcf88451227ef9dd0da1704103f4825d26777e`, identical to the published manifest.
- Production patch commit `74de564aa6d30366d708dbb6bb9f9a23316d0c44` contains Release `Pokemon-Emerald-Legends-v0.0.61.bps` (SHA-256 `0697715ebe3202b4ffd03937705e68fcfc2d4722f5e5d5722c86c14f0adfad7a`) and Debug `Pokemon-Emerald-Legends-v0.0.61-debug.bps` (SHA-256 `3968b98615e222c29d79f33a1a290a5fa42c911f3373e08e848ed0d400bf4f4e`). Release output ROM hash `c438da5812ed8a82c71acf72208ca51d207b4dc4611d33578caecdfa1232cc5f`. [Pages deployment](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39051565870) succeeded after patch commit.

## Limits and future QA

This validates source branches, both builds, BPS reconstruction, normal Debug emulator startup and in-game rendered frame capture. **It does not validate the four new NPC interactions, all patrons' milestone conversation states, or bulletin seasons by walking to each NPC in a real mGBA save.** Nor does it prove full-playthrough stability, true historical battery-save compatibility or Pizza Boy behavior; those remain to be tested with targeted fixtures. The GitHub commit, manifest and successful Pages deployment were confirmed, but the public Pages host could not be independently fetched to compare binary download bytes in this session.

**Preview provenance:** Any screenshot presented as actual gameplay is from the compiled v0.0.61 Debug ROM's mGBA native video buffer, not a stock Emerald screenshot, other media or generated substitute. Nearest-neighbor scaling preserves source pixels.
