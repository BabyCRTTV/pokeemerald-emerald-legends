# Seasonal Routes 109–112 — v0.0.65

**Model: GPT-6 | Approach: append native tables, preserve approved art/saves and verify native output plus both public patch decoders.**

Game status: **published and verified**. Matching wiki data/source keys are committed with this closeout; Pages/live wiki verification follows. [Roster/rules](../features/seasonal-encounters.md) · [Source receipt](seasonal-routes-v0.0.65-source.json) · [Native receipt](seasonal-routes-v0.0.65-native.json) · [Public patch receipt](seasonal-routes-v0.0.65-public.json) · [Wiki receipt](seasonal-routes-v0.0.65-wiki.json).

## Scope and preservation

Route 109 Surf and Routes 110 grass / 111 desert / 112 grass added sixteen tables and 32 visitors across Generations 1–9. All residents remain year-round. Native per-slot levels/weights and rates remain exact, including desert rate 10; species shares and species-level ranges can change when slots change. Earlier 32 tables and mappings are identical. Other methods, committed-season resolvers, native encounter priorities, art/DexNav fitting, maps, saves and persistent IDs are unchanged. No migration was needed. Related Electric/Ground surveys retain year-round resident options; Devon's coastal survey and native fishing proofs remain available.

## Code and build evidence

[PR #81](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/81) merged as `a2f494be367077246640397d7aef0a7c19980667`. Compiled source `2f9ccc8c8f42338e3755a6c776aaf12a5d1b3365` passed project checks **39219001418**, Debug/Release/canonical-base/BPS gates **39219001427** and native mGBA **39219001558**. QA commit `a7cc55de` changed no compiled inputs. Production project **39220172442**, builds/BPS **39220172592** and native **39220172611** passed. The executable shipped-C test covers all 48 tables, exact rates, all times of day, active-versus-pending seasons, fallback pointers/bounds and absent prior-season DexNav targets. CLI imports cover 48/32/16-table generations and stale-variant removal.

## Native review and previews

Native retained Quickstart and 23 prior Living Hoenn cases, then passed 102 seasonal/DexNav cases and 26,112 real wild creations. It checked table/species/level membership, current-versus-pending season, unique GUI rosters, native image pointers and VRAM frames, known/black palettes, sampled two-pose centering/containment, uniform shrink-only fitting, real unseen A-button rejection, closure and protected state. Route 111 used native passable desert terrain and rate 10. Private ROM instrumentation was removed; the normal built ROM stayed unchanged.

All **54 new frames** were visually reviewed. All **105 earlier frames** matched v0.0.64 production pixels. All **159 production frames** matched reviewed source pixels, and the normal Debug hash matched. This distinguishes fresh visual inspections from pixel regressions. Per-frame RGB hashes, artifact IDs/digests and harness hashes are in the native receipt.

The owner was shown [the actual-game preview](seasonal-routes-v0.0.65-preview.png) before merging. [All-season Route 109](route-109-seasonal-v0.0.65-preview.png) · [Route 110](route-110-seasonal-v0.0.65-preview.png) · [Route 111](route-111-seasonal-v0.0.65-preview.png) · [Route 112](route-112-seasonal-v0.0.65-preview.png) · [Two native animation states](seasonal-routes-v0.0.65-preview.gif) · [Preview provenance](seasonal-routes-v0.0.65-previews.json). Captions are outside gameplay, with exact 2x nearest-neighbor pixels. GIF timing is illustrative, not a continuous recording.

## Public verification

Patch commit `5ab989be69561f4e3d033867583d1fff9516c261` and Pages **39221335539** succeeded. Fresh Release/Debug downloads matched committed bytes and the CI manifest. Floating IPS and the downloaded browser decoder independently reconstructed exact production targets from canonical clean Emerald (SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7`). Debug SHA-256: `fb24e26d40d44e0eeaa9fef4ffdafed32c6949ef23d582ed8f98fb52b3826fbd`; Release: `be4c2ac4b57d32d7c580e31886afb29a6f0c5ce0d19354050f1cf0aa5aa919d6`. Eleven live release/preview files matched source. The public receipt retains hashes and HTTP evidence.

## Matching wiki and limits

Only the four new methods gained seasonal variants; native entries, earlier 32 variants and all 1,028 species remained intact. Actual reader JS passed all 48 seasonal views for exact species/counts, odds, badges and All day labels. The shipped walkthrough renderer passed all 409 methods, including twelve seasonal methods with actual year-round shares. Source-keyed atlas/profile URLs cover both Dex and guide pages; approved art/layout and independent companion versions/signing identities remained intact. Detailed public wiki verification follows deployment.

Controlled Debug fixtures do not establish natural full progression, a full detector hunt, Release interaction, authentic historical-save migration or Pizza Boy coverage. No fresh browser geometry pass is claimed for the focused data/key refresh. Broader playtests and the developer-site redesign remain separate backlog items. AGENTS.md was reviewed; no new durable policy was needed.
