# Birch's original field requests (v0.0.58)

Published in v0.0.58 after owner approval on 16 October 2026. v0.0.59 extended this system; see the [current Birch/Devon guide](research-requests.md). [Publication verification](../qa/birch-v0.0.58-public.json).

After giving the National Pokédex, Birch invites the player to check in for work beyond the Gym challenge. Talk to him at his lab or during his native field visits and choose **Field Requests**. Native registration, gifts and story events retain priority. Pokédex rating remains a separate choice.

| Request | Objective | One-time PC reward |
| --- | --- | --- |
| Grassland Neighbors | Record Poochyena and Zigzagoon as caught in the Pokédex. Earlier catches count. | 5 Poké Balls |
| Beneath the Canopy | Visit Petalburg Woods with a non-Egg Bug-type in the party. | 3 Great Balls |
| Berry Samples | Bring three Oran Berries in the Bag for the lab. | 2 Super Potions |
| Coastal Wings | Visit Route 104 with Wingull or Pelipper in the party. | 2 Net Balls |
| Nature's Recovery | Show a non-Egg party Pokémon that knows Absorb, Mega Drain or Giga Drain. | 3 Heal Balls |
| A Balanced Team | Show at least three distinct types across the non-Egg party. Both types of dual-type Pokémon count. | 1 Rare Candy |

All six are available after the Pokédex without badges, time limits or Gym prerequisites. Read the objective, hint and reward before accepting. Only one Birch request can be active; other main/side quests continue normally. The accepted request appears on the Quest Log's SIDE page. If nothing is already tracked, it is pinned automatically; an existing pin is preserved.

Speak to Birch to review progress, turn in a report or abandon the current request. Abandonment requires confirmation, makes the request selectable again and consumes no items. New habitat observations must be recorded again on a retry. Caught Pokédex records remain valid, and completed requests remain permanently complete with a `Done:` marker on Birch's list.

Pokémon are never taken. The berry study removes exactly three Oran Berries only when its reward fits in PC Item Storage. Full storage leaves the request, samples and reward pending for retry. Report rewards are granted once and cannot be farmed by abandonment or repeated conversation.

## Continuity and expansion

Request IDs 0–5 and corresponding journal IDs 33–38 are append-only. The original 33 quests and all 95 achievements retain their IDs. Request definitions and hints live in `src/legends_field_requests.c`; native dialogue/menu flow is in `data/scripts/legends_field_requests.inc`.

The feature reuses previously unreferenced native vars 0x406B–0x406D: signed active selection, completion bits and current habitat-note bits. A valid 0xB7 signature and bounded fields are required; invalid legacy data reads as no request without mutation and initializes only on accepting work. No native save structure, sector, packed-storage header or 36-byte version-1 journal layout changes. The current bit words support 16 stable requests; expanding beyond that requires an explicit additional-word migration, not renumbering existing IDs.

No map geometry, collision, NPC artwork, wardrobe asset or season rules were changed. The habitat observer only writes a note once for the matching active request, location and party sample, and is suppressed during link activity.
