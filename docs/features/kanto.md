# Kanto: the Champion's arrival

Implemented in v0.0.26 in both Release and Debug. This first chapter opens **Vermilion City**, rather than restarting FireRed's adventure. The rest of Kanto and a possible later Johto expansion remain future work.

After becoming Hoenn Champion, speak to the gentleman in **Lilycove Harbor**. Kanto's Pokémon League has invited the new Champion to visit. He gives you an **Invite Ticket**. Speak to the sailor near the entrance to sail to Vermilion Port. The native attendant still handles Emerald's original destinations.

Two Fan Club members give you a small welcome on your first arrival. Explore the three homes, Fan Club, Mart and Pokémon Center. The Center heals, provides PC access and has the native link-service floor. Its heal point also handles blackouts. The Mart stocks Ultra Balls, Hyper/Max Potions, Full Restores, Revives, Full Heals, Escape Ropes and Max Repels.

Cooltrainer **ALEX**, on the city waterfront, offers an optional six-Pokémon battle. His Kanto team is Raichu (60), Arcanine (61), Exeggutor (61), Nidoking (62), Lapras (62) and Dragonite (64). He explains the challenge before asking permission. Declining leaves the battle available; winning records native trainer victory. Losing uses the native blackout and healing flow. Neither fighting nor winning is required for travel.

The sailor aboard the Vermilion gangway offers passage back to Lilycove. Keep your ticket: it is required on every crossing and is never consumed. The ship remains available; there is no S.S. Anne departure event. Returning to Hoenn restores Lilycove as your blackout destination. Roads to Routes 6 and 11 have visible repair barriers, and Lt. Surge is away helping the crews. These are future chapter boundaries, with no countdown or unlock quest in this version.

## Debug testing tutorial

Use the **Debug** patch. In the overworld, **hold R and press START**. On numeric selectors, **Left/Right selects the digit**, **Up/Down changes it**, **A confirms**, and **B backs out**. The IDs below are **decimal** and apply to v0.0.26. Use a separate testing save: changing Game clear sets only a flag, not all completed Emerald story events.

1. On a Champion save, leave Game clear alone. On a new testing save, open **Flags & Vars… → Toggle Game clear** and enable it. If starting from the title in Debug, **SELECT** activates native Quickstart. For battle testing, **Give X… → Pokémon (Basic)** can provide a suitable team around levels 60–65.
2. Choose **Utilities… → Warp to map warp…**. Enter **Group 13 → Map 10 → Warp 0** for Lilycove Harbor. Walk up from the exit and speak to the gentleman, then the sailor near the entrance. This tests the actual invitation and boarding flow, rather than bypassing it.
3. A fresh Debug setup may have Emerald's native ship hidden. Under **Flags & Vars… → Set Flag XYZ…**, enter **861** (`0x35D`, `FLAG_HIDE_LILYCOVE_HARBOR_SSTIDAL`). If it reads **TRUE**, press A once to make it **FALSE**, then exit and re-enter the harbor. Normal postgame saves have the native ship setup already.
4. Decline the first sailing and confirm you remain in Lilycove. Accept the next sailing; confirm the welcome plays and the ticket remains in Key Items.
5. Walk north off the gangway into Vermilion City. Visit the Center and Mart, then find ALEX on the city waterfront. Decline his offer, prepare/heal, then accept. Check victory dialogue and a second conversation. Test losing on a separate attempt; you should recover at Vermilion's Center.
6. Return south to the port and speak to the sailor at the end of the gangway. Decline, then accept passage home. Board again from Lilycove: the ship and ticket remain usable and the welcome does not repeat. Save/reload in both regions and test this again.

For direct area inspection, use the following **Utilities → Warp to map warp** values. Direct warps intentionally bypass boarding; prepare Game clear and the ticket first when testing the complete ferry route.

| Location | Group | Map | Warp |
|---|---:|---:|---:|
| Lilycove Harbor | 13 | 10 | 0 |
| Vermilion City waterfront | 75 | 0 | 0 |
| Vermilion Port, city entrance | 75 | 1 | 1 |
| Pokémon Center, ground floor | 75 | 2 | 0 |
| Pokémon Center, link floor | 75 | 3 | 0 |
| Mart | 75 | 4 | 0 |
| Fan Club | 75 | 5 | 0 |
| Houses 1 / 2 / 3 | 75 | 6 / 7 / 8 | 0 |

**Give the ticket directly:** **Give X… → Give item XYZ… → Item 874 → Quantity 1**. The normal invitation is the preferred progression test.

**Replay the welcome:** **Flags & Vars… → Set Flag XYZ… → 621** (`0x26D`, `FLAG_LEGENDS_KANTO_WELCOMED`). This menu toggles the selected flag when A is pressed. If TRUE, press A once to make it FALSE; if already FALSE, leave it alone. Exit and re-enter Vermilion Port.

**Reset ALEX's victory:** use the same menu with **2135** (`0x857`, `TRAINER_FLAGS_START + TRAINER_LEGENDS_KANTO_ALEX`). Make it FALSE, then speak to him again. This resets only that optional trainer, not the rest of the game.

## Implementation

- Modular events: `data/scripts/legends_kanto.inc`; dedicated maps in appended **group 75**. Existing Hoenn and FRLG map IDs are unchanged. Map `region` is the build filter, so the imported maps use `REGION_HOENN` for Emerald inclusion; `region_map_section: MAPSEC_VERMILION_CITY` supplies the actual Kanto name/map geography.
- Two appended outdoor layouts reuse the original FRLG tiles/metatiles/palettes. Upstream FRLG attributes already use Emerald behavior semantics. `tileset_format: frlg` activates the engine's existing 640-primary tile/metatile counts, seven primary palettes, 32-bit attributes and explicit border dimensions while `layout_version: emerald` selects the build. Legacy layouts are unchanged. Selected door animations are registered against the new tileset pointers. Native FRLG water animations remain intact.
- Interior maps reuse compatible Emerald layouts, nurse animation, shops, PCs and link services. They do not run FireRed's early-game gifts, S.S. Anne departure, original trainer teams or story flags.
- Item 874, trainer 855 and the final heal location are appended. The welcome uses previously unused flag `0x26D`. Existing SaveBlock sizes, item IDs, map/layout IDs and trainer-flag allocation remain unchanged.
- Native S.S. Tidal route state and event-ticket handling are untouched. Ferry events use independent fades/ship sound and explicit safe arrival coordinates; the return restores the Lilycove heal point.
- `python3 test/legends-kanto.test.py` exercises actual script branching for invitation/ticket gates, declined journeys, retained-ticket round trips, welcome persistence and optional battle victory. It audits warp bounds/destinations, map sizes, spectator land placement and the blackout nurse destination. These checks do not replace emulator playtesting.

## Emulator checklist

- [ ] Release and Debug: normal Champion invitation, no invitation before Game clear; declined sailing; repeat-ticket use.
- [ ] Inspect first arrival, dialogue line widths, actor positions, ship layering, water animation and both costume/gender/follower states.
- [ ] Walk through every open door and back; inspect door animation, collisions/elevations and both harbor boundaries. Repair barriers must be visible and impassable.
- [ ] Center healing/PC/link-floor return, Mart purchases, optional battle decline/win/loss and correct regional blackout destination.
- [ ] Return/revisit, save/reload in each map, welcome persistence, ticket persistence, and ALEX's native victory flag.
- [ ] Native Hoenn sailings to Slateport/Frontier and event islands continue to work independently.
- [ ] Region map displays Kanto while visiting Vermilion; unsupported Kanto Fly destinations stay unavailable.
- [ ] Test on mGBA and Pizza Boy, including an existing Champion save.
