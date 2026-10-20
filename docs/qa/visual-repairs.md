# Visual repair candidate after v0.0.67

Unpublished; four visual repairs prepared for owner review. The rare outfit report remains open. No version, public patch or Pages publication is claimed.

## Causes and scope

- **Badges:** native Hoenn front-card tiles contain numbered white slot boxes. Transparent Kanto badge pixels expose those boxes. The local non-link Hoenn card now continues the adjacent native stripes beneath its badge row; badge bitmap pixels/palettes, region controls, back and link layouts stay intact.
- **Bedroom surround:** twelve source cells use palette 11's black index 15, but the private decoration loader reuses slot 11 and makes the void lavender. Those twelve cells now reference the identical black index 15 in decoration slot 5. Source pixels, flips, attributes, ceiling trim, original chairs, furniture and rug/bed colors stay intact. The thin native light ceiling highlight is intentional source art and is retained.
- **Center sign:** the emissive generator made both the pale face and red lettering pink. Only the generated night colors change: warm-white face, red lettering. Daytime colors, source signs, window glows, borders and palette/tile allocations are retained for Hoenn and Kanto.
- **Pause footer:** independent tiny page/list triangles crowded the bottom right. The page hint now reads LEFT/RIGHT 1/2 or 2/2 in native FONT_SMALL at visibleRows*16+4, x=8. Native glyph ink occupies +7 through +15, inside the existing 16-pixel footer, leaving a blank row below the last action. Up/down list indicators, menu actions, frame, controller handling and Link/Union exclusions remain intact.

## Verification

Baseline: master e019d5f85e550bc1e69bfa7c38eea710c85ec916. Local baseline Debug SHA256 87680bf3bee6e5a953562858fd096923af45b82420894081caa0da46da2d9cd8 exactly matched the verified public v0.0.67 Debug ROM.

Passed local focused tests: legends-bedroom, legends-night-lights, legends-start-menu, legends-adventure-menu, legends-trainer-card-badges, legends-wardrobe, legends-appearance, legends-appearance-colors, legends-footwear, legends-family-skin. They exercise actual C rendering/input and generated assets, not mocked replacement implementations. The appearance checks preserve approved art across 1,440 combinations and 400 smile/color/skin cases.

Both normal Debug and LTO Release builds passed. Controlled Debug mGBA checks covered 72 gender/movement-state palettes, sixteen repeated Wardrobe Apply/Cancel/Trainer Card cycles, and actual flash reload of nine saved appearance/bedroom fields per gender. The rare outfit corruption did not occur. Both bedroom layouts and native manual-clock day/night Fallarbor were captured from compiled ROMs. Private setup callbacks only exist in emulator ROM copies. The separate Release harness boots the unmodified production-format ROM through normal Continue and controller input from controlled current battery fixtures.

Normal unmodified Release Continue, both pause pages, both badge regions and natural floor approach to each bedroom wardrobe passed. Both Release bedroom frames and all four Kanto badge rows matched Debug exactly. Daytime Fallarbor and the wardrobe preview matched the original baseline frame exactly; bedroom differences were exclusively the old lavender void becoming black. Card changes were confined to its badge row. Moving outdoor NPCs are not a whole-frame regression target. [Local machine receipts](visual-repairs-local.json) include exact ROM/image hashes. [Native UI review](visual-repairs-ui.png) and [native world review](visual-repairs-world.png) show before/after at 2× nearest-neighbor scale. CI/BPS results remain pending and are not implied by local build success. Original screenshot files and private ROM/save fixtures are excluded from commits and CI uploads.

## Remaining work

- Owner review of the proposed native menu/sign appearance; publish only after that review.
- Complete next-version metadata, all three changelogs/site, Debug/Release BPS application and live publication verification when promoting the candidate.
- Reproduce rare outfit oversaturation, retaining the exact appearance settings, preceding menu/field action, weather/time, follower and whether a map reload restores it. Keep the issue open; successful controlled tests are not proof it is fixed on Pizza Boy.
- Continue hidden grottos after the visual work. No grotto mechanics or assets were implemented here.
