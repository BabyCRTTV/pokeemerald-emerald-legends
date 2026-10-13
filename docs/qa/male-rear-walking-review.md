# Male rear walking hairstyle review

Status: visual review draft based on published v0.0.45. These changes are staged for review and are not a new published release.

Replace the generic tapered rear mask with ten individually authored 16-pixel-wide crowns in `tools/legends/male_overworld_back_hair.py`. Crew Cut, Side Part, Spiky, Side Sweep, Tousled, Quiff, Shag, Curls, Man Bun and Undercut have their own outlines and texture. The bun uses a visible tie; the undercut uses the selected skin ramp for its shaved lower section.

Anchor each crown to the native ear row and finish directly above the neck. Preserve the actual ears, their outside rims, and the body. Clear the full native cap region, including its pale lower band, rather than treating cap pixels between the ears as a face. Fill both lower skull rows completely between the native ears; tapering these rows leaves transparent gaps beside the ears. A regression check verifies that coverage in every rear walking/running pose under all coat combinations.

The existing sparse layer generator and runtime compositor remain in use. The Normal sprite bank includes both walking and running: only male north-facing poses 1, 5, 6, 10, 14 and 15 receive the revised cuts. This changes 60 hair layers; all other 3,332 layers are byte-identical to v0.0.45, including every female layer, male front/side views, coats and other activities. Both approved battle frame banks are unchanged.

Validation: the Debug ROM builds; `python3 test/legends-style-layers.test.py` passes all 212 native pose tables, art reproduction, actual skin/ear protection, coat order, complete skull interiors and unique rear cuts. The rear-view test now protects real ears/neck instead of incorrectly protecting the retired cap as eye pixels.

Review exports are decoded from the rebuilt ROM in mGBA with Light skin and the default outfit. The front/back still sheet uses Natural hair; the walking GIF cycles all eight hair colors and contains an Original Emerald reference.

After visual approval, finalize a fine-grained version bump, the three changelog entries and site metadata, then run the normal Release/Debug verified BPS publishing workflow.

