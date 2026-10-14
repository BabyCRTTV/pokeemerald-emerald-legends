# Approved front-face shading — v0.0.49

## Approval and exact scope

On 14 October 2026 the owner requested slightly softer face shadows, clarified **front-facing only**, then approved the five-tone comparison for both characters. [Retained approved comparison](front-face-v0.0.49-approved.png), SHA256 `64a25725dca1f1c2b1809085bb4047b18563d5d7315f3d2685395eed18ac6348`. Its source was the v0.0.48 C compositor at `4f5b07ad45ddfc93ce66835ed94c11c81b6956c0`; only the selected cheek pixels were edited for that review.

The implemented standing face matches those twelve male/four female shade changes. Existing skin shade 3 becomes shade 2 at authored interior cheek cells. Jaw outlines, eyes, smile, ears, hair and non-face pixels remain intact. The five skin ramps themselves are unchanged; hands and other views do not become lighter. Native running faces have a shorter jaw than the standing pose, so their own contours are retained rather than copying a standing rectangle over them.

Masks are authored from the original native source poses, then stored alongside the sparse ROM data. All 202 native field descriptors are represented; only the 62 front-facing entries contain edits. The original sixteen hair/coat/leggings layers and their offsets are unchanged; new pixels are appended and deduplicated (404 bytes). Small additional ROM descriptors reuse the existing compositor; no new runtime cache, heap bank or direction-dependent palette was introduced. The final pass accepts skin-shadow 3 only, preserving composed hair/accessories. Native cap/ear contours using other materials remain protected.

## Validation

- All 44 runnable project-check commands passed locally, including the existing sector/legacy initialization/codec/save rules, approved Side Part, wardrobe, story and appearance tests.
- `test/legends-front-face.test.py` executes the real integrated C renderer in pre-shading/current modes: 2,866 comparisons cover every field descriptor, original plus all ten custom cuts, coats/accessories, five skin tones, eight hair colors and front portraits. Exactly 886 compared front results changed; every changed cell stayed within its authored mask and used existing skin shade 2. Palettes and pixels outside those masks matched exactly; side/rear views, portraits and diving were unchanged.
- The v0.0.48 Side Part suite independently freezes its original head/art and native frame hashes with this new shading disabled in the host comparison. The new suite verifies the combined pipeline; this preserves the old hair approval without silently replacing its reference.
- Local GCC 13.2.1 Debug and Release builds passed. Debug/Release EWRAM remained 254,468/254,470 bytes; linked ROM grew only 2,156/2,164 bytes. mGBA 0.10.2 executed the actual ARM compositor after boot through a private controlled callback: all 1,010 native descriptors across both genders and all five skin tones matched the host C pixels and palettes exactly. Callback1 was disabled to isolate this harness from the title flow; the private QA ROM/callback is not distributed. This is not a natural field traversal or save-persistence test. [Structured proof](front-face-v0.0.49-verification.json).
- Save impact: no serialized structures, capacities, flags/vars, persistent graphics/wardrobe/story IDs, storage codec or initialization rules changed. The existing older-save upgrade path is retained without migration. This is a source/layout invariance finding; no new historical-save emulator matrix is claimed.

## Downloadable previews

- [Current native-C standing comparison, 360 pixels wide](front-face-v0.0.49-mobile.png)
- [Current native-command walking/running comparison GIF](front-face-v0.0.49-motion.gif)

Reproduce with `python3 tools/legends/preview_front_face.py`. These are exact nearest-neighbor C sprite-buffer exports, not emulator screenshots. The before column reproduces the pre-shading pipeline; the after column uses the current compositor. Native South walking/running commands and durations drive the GIF. Both sides preserve the native head bob and shorter running jaw.

Publication requires successful native Debug/Release Actions, independent clean-base BPS round trips, Pages deployment and live download verification. Until then this record describes a validated candidate.
