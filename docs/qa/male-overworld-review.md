# Male overworld reference review

Status: unpublished visual-review draft on v0.0.45. Finalize a fine-grained version
bump and publish verified Release/Debug BPS patches only after visual approval.

Import the user's ten four-view sheets for Crew Cut, Side Part, Spiky, Side Sweep,
Tousled, Quiff, Shag, Curls, Man Bun and Undercut. Update the complete male overworld
set, including forward, rear and profile views; east uses native west mirroring.
The indexed head atlas and source hash/grid records are checked in. All fitting
runs at authoring time through the existing sparse layer pipeline. The 83 source
poses map to 92 native runtime descriptors through repeated Surf/watering frames:
920 male hair layers change; the other 2,472 layers remain byte-identical to v0.0.45.

Fit all 83 non-diving male source poses across walking/running, Mach Bike, Acro
Bike tricks, Surf, field moves, fishing and watering. Preserve original frame
tables, dimensions, body movement, lower faces/pupils, skin, ears and props.
Register heads to native pupils or rear ears, including three-quarter field-move
faces. Fill the tiny background gaps under Side Part's separate fringe locks.
Use the selected skin shade for the undercut's shaved temple. The supplied rear
contours can include a straight dark nape outline; every nape pixel is owned by
the imported layer, rather than accidentally retaining native cap pixels.

Male custom overworld hair uses 4/7/8 for midtone/highlight/shadow and 15 for the
outline. Move original navy 8 into stable 5 before painting hair. Slot 5 retains
that exact navy RGB, protecting native pupils through hair-color changes. Coats,
scarves and footwear retain their separate materials; footwear remapping excludes
all three reserved hair shades. Trainer/battle palettes and female art are outside
this change. Original hair, native costume overlays and the diving suit retain
their existing treatment and saved option IDs.

Validation:

- Reproduce sparse assets and exercise all 212 native pose tables through the
  actual C compositor, including face/ear/hand/rod protection, skull coverage,
  distinct cuts and coat order.
- Run actual footwear/cache regressions under all shoes, hairstyles, coats,
  hair colors and native activity states, including costume and dive isolation.
- Run the actual appearance settings/palette regression across genders, all
  tones/outfits, saved settings, staged choices and legacy defaults.
- Decode the rebuilt ROM's live graphics selectors and native animation commands
  in mGBA. Check all 400 cut/color/skin combinations and 200 live combinations of
  outfits, coats, scarves, shoes/boots, colors and skin tones. Verify stable pupil
  RGB, all three hair shades and the selected skin ramp.
- Export ten individual four-view character sheets, a walking/running montage,
  native activity animation panels, and a color/skin-tone animation for approval.

Release and Debug share this art. Keep root VERSION and the published downloads
at v0.0.45 until approval; all three changelogs record the draft as Unreleased.
