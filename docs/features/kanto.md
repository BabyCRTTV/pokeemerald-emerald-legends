# Current chapter (v0.0.28.1)

The original arrival and map foundation below remain historical documentation. Routes 6–8 and 16–18, Saffron and Celadon are now connected; two visiting Gyms, route encounters and the Wing Survey opening are playable. See [Kanto postgame](kanto-postgame.md) for the authoritative current scope, permanent victory rules and planned chapters.

# Kanto: arrival and regional foundation

Version **0.0.27** adds an intentionally empty eastern/southern Kanto foundation to the existing Vermilion arrival chapter. Walk east from Vermilion through Routes 11, 12, 13, 14 and 15 to Lavender and Fuchsia, then south to Route 19. The new towns, routes and 22 gate/town interiors use native FireRed layout dimensions, blockdata, border data and tileset art. No new NPCs, trainers, gifts, wild encounters or FireRed story events are imported. The new Centers/Marts are empty shells; return to Vermilion for healing and supplies.

**Surf connection:** on Route 124, Surf north through the water lane at **x20–24, y1** and accept the crossing to Route 19. Champion status and the retained Invite Ticket are required outbound. At Route 19's south end, cross **x10–16, y56** to return; no ticket gate can strand a traveler on the Kanto side. Arrival tiles are water, separated from the triggers to prevent immediate return loops. Native Surf and badge checks remain intact. The short fade reloads each region's tilesets instead of displaying incompatible Hoenn/FRLG borders. The two-way Lilycove ferry remains available.

**Boundaries:** Route 6, Routes 8/10/18/20, Pokémon Tower, Safari Zone and Diglett's Cave remain outside this revision. Unsupported entrances are solid and display a development notice. Unimplemented route edges are sealed. Appended map/layout IDs preserve the existing save structure and the original group-75 maps. See `data/legends_kanto_foundation.json` for the exact map/source manifest. Imported maps set Vermilion's heal destination; Surf return restores Lilycove's destination.

**Validation limits:** automated geometry, reciprocal connections, event gates, source fidelity and encounter exclusion are checked. A green build and BPS round-trip verification establish compilation and patch integrity; emulator traversal of every new map and Pizza Boy testing remain necessary. This revision does not claim those playtests.

## Recorded foundation validation (v0.0.27)

[PR build/verification run](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38011963384) completed successfully for revision `e089ae2`: Debug and Release compilation, independently built clean Emerald SHA-1 verification, and both BPS reapplications with byte-for-byte ROM comparisons. All Legends Python suites and all five browser patcher tests pass. Four foundation checks cover native layout dimensions/borders and allowed boundary edits, explicit event-script registration, absence of new objects/encounters, connected reciprocal map/warp graph, Champion/ticket gating, unrestricted return travel and clear water arrivals outside trigger lanes. Native mapjson generated the map groups, layouts and imported headers/events. Static renders of Lavender, Fuchsia and Route 19 were inspected; the unfinished western sea exit now uses native rocks rather than an ocean fence. These renders do not exercise the game engine. Emulator traversal, new-map save/reload checks and Pizza Boy testing remain outstanding.

## Original arrival chapter

Implemented in v0.0.26 in both Release and Debug. This first chapter opens **Vermilion City**, rather than restarting FireRed's adventure. The rest of Kanto and a possible later Johto expansion remain future work.

After becoming Hoenn Champion, speak to the gentleman in **Lilycove Harbor**. Kanto's Pokémon League has invited the new Champion to visit. He gives you an **Invite Ticket**. Speak to the sailor beside the main ferry attendant to sail to Vermilion Port. The native attendant still handles Emerald's original destinations.

Two Fan Club members give you a small welcome on your first arrival. Explore the three homes, Fan Club, Mart and Pokémon Center. The Center heals, provides PC access and has the native link-service floor. Its heal point also handles blackouts. The Mart stocks Ultra Balls, Hyper/Max Potions, Full Restores, Revives, Full Heals, Escape Ropes and Max Repels.

Cooltrainer **ALEX**, on the city waterfront, offers an optional six-Pokémon battle. His Kanto team is Raichu (60), Arcanine (61), Exeggutor (61), Nidoking (62), Lapras (62) and Dragonite (64). He explains the challenge before asking permission. Declining leaves the battle available; winning records native trainer victory. Losing uses the native blackout and healing flow. Neither fighting nor winning is required for travel.

The sailor aboard the Vermilion gangway offers passage back to Lilycove. Keep your ticket: it is required on every crossing and is never consumed. The ship remains available; there is no S.S. Anne departure event. Returning to Hoenn restores Lilycove as your blackout destination. The road to Route 6 has visible repair barriers, and Lt. Surge is away helping the crews. These are future chapter boundaries, with no countdown or unlock quest in this version.

## Beginner playtest walkthrough

This walkthrough is for **v0.0.27 Debug**. You do not need programming knowledge. “Debug” is the testing edition; its special menu can move you to an area and prepare a test save.

### 1. Open the Debug edition

Use the [Debug browser patcher](https://babycrttv.github.io/pokeemerald-emerald-legends/patcher.html?build=debug). Select your own clean, unmodified Pokémon Emerald ROM and create the patched game. Your original ROM stays on your device and is never uploaded. Open the resulting **Debug .gba** in your emulator. Do not apply this patch to an already patched Legends ROM.

Use a separate testing save, or back up your existing Champion save before copying it for testing. Emulator save states are snapshots; the game's **START → Save** option writes the normal save. Keep your main adventure's save separate from this experiment.

On a new game, finish the opening scene until you can walk around freely. Optional shortcut: press **SELECT on the Debug title screen** for Quickstart, then leave the truck and finish Mom's dialogue. Quickstart is not required.

### 2. Learn the buttons and open the menu

These names mean the **GBA buttons in your emulator**, not particular keyboard keys. On a phone, use its on-screen controls. On a computer, check your emulator's input settings for the keys assigned to R and START.

- **Up/Down:** move through a menu.
- **A:** choose the highlighted option; talk to a person you are facing; advance dialogue.
- **B:** go back or close a menu.
- **R:** the right shoulder button, not Right on the direction pad.
- **START:** the GBA Start button.

Stand somewhere you can walk freely, with no dialogue or menu open. **Hold R, press START while still holding R, then release both buttons.** The Debug menu should appear. Use Up/Down to highlight an option, then press A. Press B to return to the previous menu; repeat until you are back in the game.

If you see the ordinary Pokémon/Bag/Save menu, close it and check that you loaded the Debug game and held R while pressing START.

### 3. Make your test save count as Champion

If your copied save has already beaten the Pokémon League, skip this step.

Otherwise, open Debug and choose **Flags & Vars…**. Highlight **Toggle Game clear**. A “flag” is simply a saved yes/no setting; Game clear tells this feature that you are Hoenn Champion. If it is OFF, press A once to switch it ON. If it is already ON, leave it alone. Press B until you return to the game.

This shortcut opens the Kanto invitation for testing. It does not finish all of Emerald's other story events.

### 4. Travel instantly to Lilycove Harbor

Open Debug again. Choose **Utilities…**, then **Warp to map warp…**. A “warp” moves your character to a map entrance.

You will see **three number screens in order: Group, Map, then Warp**. Enter one number per screen and press A to continue. For Lilycove Harbor, the numbers are **Group 13, Map 10, Warp 0**.

The number selector uses different controls from a normal menu:

- **Up** adds to the number; **Down** subtracts.
- **Right** selects the next larger place: ones → tens → hundreds. **Left** moves back toward ones.
- The indicator **+1** means each Up press adds 1; **+10** means each Up press adds 10.
- **A** accepts the number and opens the next screen. **B** backs out.
- Leading zeroes are fine: **013 means 13** and **010 means 10**.

Starting from zero with +1 selected, follow this exact example:

1. **Group screen:** press Up **three times** to show 3. Press Right **once** to select +10. Press Up **once** to show 13. Press A.
2. **Map screen:** it starts at zero again. Press Right **once**, then Up **once**, to show 10. Press A.
3. **Warp screen:** leave the number at **0**. Press A.

You should now be inside Lilycove Harbor, near its exit. If you make a mistake, adjust the number with Up/Down before confirming, or press B and reopen the warp tool.

### 5. Collect your invitation and board

Walk up from the exit and find the **gentleman near the entrance**. Stand next to him, face him and press A. Tap A to read each page of dialogue. He should congratulate the Champion and give you an **Invite Ticket**.

Next, speak to the **sailor beside the main ferry attendant**. Use this sailor for Kanto travel; the original harbor attendant still offers Emerald's other destinations.

When asked to sail to Vermilion, choose **NO** with Up/Down and press A. You should stay in Lilycove. Talk to the sailor again, choose **YES**, and finish his dialogue. The game should fade and take you to Vermilion Port.

Read the first-arrival welcome with A. When it finishes, open **START → Bag → Key Items** and confirm the Invite Ticket is still there. Close the Bag with B. Walk **up/north along the gangway** to enter Vermilion City.

### 6. Explore, then try the optional battle

Visit the Pokémon Center, Mart, Fan Club and three open homes. Check that you can enter and leave, talk to people and heal your party. The Gym and northern road remain closed; the eastern road opens into the new foundation.

Find **Cooltrainer ALEX on the city waterfront**. Talk to him and choose NO first: declining should let you keep exploring. His six Pokémon are **Lv. 60–64**, so heal and bring a suitable team before accepting.

A new Quickstart save may have no usable team. You can skip this battle during your first travel test. To prepare Pokémon, use **Debug → Give X… → Pokémon (Basic)**, select a species and a level around 60–65 using the same number-selector controls, then confirm. Repeat for a team; if your party is full, check the PC. Heal before fighting.

On a normal win, finish the dialogue and talk to ALEX again; he should acknowledge the result instead of immediately battling again. On a separate loss attempt, you should recover at **Vermilion's Pokémon Center**. See the optional shortcuts below if you only want to check the victory event quickly.

### 7. Return to Hoenn and repeat the trip

Walk south back into the port. Speak to the **sailor at the end of the gangway**; stand above him and face down.

Choose NO first and confirm you remain in the port. Talk again, choose YES, and read the dialogue. You should return to Lilycove Harbor.

Speak to Lilycove's Kanto sailor again and sail back. **The same ticket should still work, the ship should remain available, and the first-arrival welcome should not repeat.**

Use **START → Save**, restart the game and choose **Continue**. Check that you return to the saved location and can still use the ferry. Try this once in Kanto and once in Hoenn.

### If something gets stuck

- **You updated the ROM but NPCs still appear in their old positions:** load your normal in-game save rather than an old emulator save state, then leave and re-enter the current map once. Emerald saves a snapshot of local NPCs; entering the map again refreshes their graphics, positions and movement from the new ROM. You do not need to start a new adventure.
- **The invitation is refused:** check that Game clear is ON, then speak to the gentleman again.
- **The sailor says you need a ticket:** obtain it from the gentleman; check the Bag's Key Items pocket.
- **The number rises by 10 instead of 1:** press Left until the indicator shows +1.
- **The ship is invisible on a fresh test save:** this can happen because Quickstart has not completed Emerald's ship setup. The new ferry sailor still handles travel. The optional ship-visibility fix is below.
- **You cannot move after arrival:** finish all welcome dialogue with A before trying to walk.

### What to send with a bug report

Include **Legends version and build (for example, v0.0.27 Debug), emulator name/version, fresh or existing save, the steps you took, what you expected, and what happened**. A screenshot of a visual problem helps. Say whether you used a direct warp or sailed normally.

The Release edition has the same Kanto content. An existing Champion save can test the normal invitation and ferry without using any Debug tools.

## Optional advanced shortcuts

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

**Show the native Lilycove ship on a fresh test save:** **Flags & Vars… → Set Flag XYZ… → 861** (`0x35D`). If TRUE, press A once to make it FALSE, exit the menu, then leave and re-enter the harbor. If already FALSE, leave it alone.

**Give the ticket directly:** **Give X… → Give item XYZ… → Item 874 → Quantity 1**. The normal invitation is the preferred progression test.

**Replay the welcome:** **Flags & Vars… → Set Flag XYZ… → 621** (`0x26D`, `FLAG_LEGENDS_KANTO_WELCOMED`). This menu toggles the selected flag when A is pressed. If TRUE, press A once to make it FALSE; if already FALSE, leave it alone. Exit and re-enter Vermilion Port.

**Check victory dialogue quickly:** During move selection in a Debug battle, press **SELECT** to open the native battle Debug menu. Scroll to **Instant Win** and press A. Finish the dialogue, then speak to ALEX again. This checks the victory event and trainer flag; it does not test battle balance. Use a separate attempt with a weak party to check the loss/blackout flow.

**Reset ALEX's victory:** use the same menu with **2135** (`0x857`, `TRAINER_FLAGS_START + TRAINER_LEGENDS_KANTO_ALEX`). Make it FALSE, then speak to him again. This resets only that optional trainer, not the rest of the game.

## Implementation

- Modular events: `data/scripts/legends_kanto.inc`; dedicated maps in appended **group 75**. Existing Hoenn and FRLG map IDs are unchanged. Map `region` is the build filter, so the imported maps use `REGION_HOENN` for Emerald inclusion; `region_map_section: MAPSEC_VERMILION_CITY` supplies the actual Kanto name/map geography.
- The four native FRLG object graphics used here (town woman, sailor, Cooltrainer and S.S. Anne), their palettes and picture tables are explicitly shared with Emerald. Upstream keeps the remaining FRLG-only objects gated.
- Two appended outdoor layouts reuse the original FRLG tiles/metatiles/palettes. Upstream FRLG attributes already use Emerald behavior semantics. `tileset_format: frlg` activates the engine's existing 640-primary tile/metatile counts, seven primary palettes, 32-bit attributes and explicit border dimensions while `layout_version: emerald` selects the build. Legacy layouts are unchanged. Selected door animations are registered against the new tileset pointers. Native FRLG water animations remain intact.
- Interior maps reuse compatible Emerald layouts, nurse animation, shops, PCs and link services. They do not run FireRed's early-game gifts, S.S. Anne departure, original trainer teams or story flags.
- Item 874, trainer 855 and the final heal location are appended. The welcome uses previously unused flag `0x26D`. Existing SaveBlock sizes, item IDs, map/layout IDs and trainer-flag allocation remain unchanged.
- Native S.S. Tidal route state and event-ticket handling are untouched. Ferry events use independent fades/ship sound and explicit safe arrival coordinates; the return restores the Lilycove heal point.
- `python3 test/legends-kanto.test.py` exercises actual script branching for invitation/ticket gates, declined journeys, retained-ticket round trips, welcome persistence and optional battle victory. It audits warp bounds/destinations, map sizes, spectator land placement and the blackout nurse destination. These checks do not replace emulator playtesting.

## Recorded validation (v0.0.26.1)

The compiled Debug ROM was checked in headless mGBA with a copy of the previous ordinary test save. Rendered frames confirmed Machop and the construction-site resident, the Gym attendant outside the door, Fan Club visitors standing clear of sofas, and idle looking/walking behavior. The relocated Lilycove sailor was approached and used for an actual outbound crossing; return passage reached Lilycove at the normal arrival point. The retained Invite Ticket displayed all three description lines without clipping in the Bag. Resetting welcome flag 621 through the native Debug menu replayed the first-arrival scene: both greeters faced the Champion, all dialogue completed and free movement resumed. Debug warps prepared isolated visual checks; the ferry checks used the actual boarding scripts. The new Debug ROM also saved, reset and continued in Vermilion. The locally compiled Release ROM loaded that normal save, showed the ordinary Start menu under R + START, returned to Lilycove and boarded again from the relocated sailor, without repeating the welcome. Eight Kanto checks pass, including every non-species NPC graphics registration, walk-route/furniture geometry and native-font ticket widths. Pizza Boy confirmation remains a player test; this record does not claim new full battle-balance coverage.

## Recorded validation (v0.0.26)

Debug was exercised in headless **mGBA 0.10.3** using the compiled ROM, rendered frames and normal controller inputs. Confirmed: R + START and documented warp selectors; Game clear toggle; invitation item award; outbound crossing and three-part first welcome; declined return and successful return to Lilycove; walking through the harbor/city boundary; Center door entry/exit, nurse interaction/healing, link-floor stair round trip; optional trainer battle startup with six opponents; deliberate loss and recovery at Vermilion's Center; normal in-game save, reset and Continue in Vermilion. A following Bulbasaur was present during city, Center and battle tests. Further checks confirmed all six open building entrances (Center, Mart, Fan Club and three homes), Mart inventory and an Ultra Ball purchase, normal Save/reset/Continue in the port, and ALEX's post-victory/repeat dialogue through the native Debug menu's Instant Win option. The victory shortcut verifies scripting, not battle balance. Visual testing caught and corrected FRLG-only sprite registrations; event testing caught and corrected native trainer comparison semantics.

Release also loaded the same ordinary save, showed the regular Start menu instead of Debug under R + START, and completed Vermilion → Lilycove → Vermilion with the retained ticket and no repeated welcome.

Automated checks cover additional ticket/progression and trainer-victory branches. The broader checklist below remains for full manual coverage, especially Pizza Boy, existing Champion saves, victory balance, every interior, both genders/costumes and native Hoenn destinations. Do not interpret this record as complete emulator coverage.

## Emulator checklist

- [ ] Release and Debug: normal Champion invitation, no invitation before Game clear; declined sailing; repeat-ticket use.
- [ ] Inspect first arrival, dialogue line widths, actor positions, ship layering, water animation and both costume/gender/follower states.
- [ ] Walk through every open door and back; inspect door animation, collisions/elevations and both harbor boundaries. Repair barriers must be visible and impassable.
- [ ] Center healing/PC/link-floor return, Mart purchases, optional battle decline/win/loss and correct regional blackout destination.
- [ ] Return/revisit, save/reload in each map, welcome persistence, ticket persistence, and ALEX's native victory flag.
- [ ] Native Hoenn sailings to Slateport/Frontier and event islands continue to work independently.
- [ ] Region map displays Kanto while visiting Vermilion; unsupported Kanto Fly destinations stay unavailable.
- [ ] Test on mGBA and Pizza Boy, including an existing Champion save.
