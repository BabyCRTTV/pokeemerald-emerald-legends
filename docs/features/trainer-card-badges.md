# Regional Trainer Card badges — v0.0.32

The local Trainer Card contains two eight-slot collections: Hoenn and Kanto. On the front, press Left/Right, L/R or SELECT to switch the existing badge strip. A small region label explains the controls. A still flips to the card's normal back; B closes it. Unearned Kanto badges use dimmed native Kanto artwork, while earned badges show full color.

Kanto order is Boulder, Cascade, Thunder, Rainbow, Soul, Marsh, Volcano, Earth. Each slot reads its dedicated permanent Leader victory flag. Current content supports Surge, Erika, Koga and Sabrina; other slots remain unearned until their Gyms are implemented. Existing Surge/Koga wins appear without revisiting their Leaders. Either difficulty earns the same badge, and the other team cannot then be fought.

This is an additional League record display. It does not grant Hoenn HM permissions, change card stars, or add an inventory item. All Hoenn badges and existing save offsets are preserved. No field is added to the public `TrainerCard` struct or the link packet, and link cards do not offer this local-only region selector.

The display reuses its original 1 KiB decompression buffer and 32 badge tiles in VRAM when switching regions. Only eight transient badge-state bytes and the selector byte are added to its allocated screen state. Palette 3 holds earned badge colors; palette 6 holds dimmed Kanto colors. Card colors, trainer portrait, star palette and front/back statistics keep their existing regions.

`test/legends-trainer-card-badges.test.py` runs the actual drawing functions across all 256 earned combinations, both regions and linked/local cards (1,024 cases). It checks tile bounds, four tiles per displayed badge, palette choices, label bounds and native font widths. `test/legends-kanto-chapter2.test.py` compiles the actual trainer flag resolver and checks save address/partner separation. Full builds verify integration. Manual emulator review of card switching/flips remains a separate playtest item.
