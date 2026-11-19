# Town notice boards

The first three boards stand outside the Poké Marts in Oldale, Petalburg and Rustboro. They are independent of Birch's and Devon's requests. A player can take multiple notices, track them in the Quest Log and put unfinished notices back on their board. Each local sighting reads a species category from the nearby route's current wild land table.

| Board | Posting | Recipient and objective | PC reward |
| --- | --- | --- | --- |
| Oldale | First-Aid Tin | Deliver 1 Potion to Finn, the boy in the Mart | 3 Poké Balls |
| Oldale | Crooked Tracks | Show Zigzagoon to Nell, the girl outdoors | 2 Potions |
| Petalburg | Woods Medicine | Deliver 2 Antidotes to Reed, the man in the Mart | 2 Great Balls |
| Petalburg | Pond Portrait | Show Wingull to Pip, the boy by the pond | 2 Net Balls |
| Rustboro | Tunnel Lifeline | Deliver 1 Escape Rope to Len, the Bug Catcher in the Mart | 3 Dusk Balls |
| Rustboro | Echo Lesson | Show Whismur to Kit, the boy at the left desk in the school | 2 Super Potions |

![First-Aid Tin in Debug mGBA](first-aid-tin.png)

![Wooden notice boards in Debug mGBA at noon and 23:00](wooden-notice-boards.png)

## Verification

- Debug mGBA used ordinary directional input and A to interact with all three placed boards. At Oldale the player browsed a sighting, read Finn's notice, accepted it, spoke directly to him at the Mart, declined once and then delivered the Potion. Native flash save, clear and reload preserved the pending and completed states.
- Controlled Debug fixtures exercised all six transactions, including missing items, Eggs presented as proof, full PC storage, retry, one-time payment and returning a notice. The other five NPC interactions were checked for script and map wiring.
- The journal, field request and missive regression checks passed. The feature appends journal IDs 65–70 and uses twelve audited native flag bits. The save layout stays compatible.
- Built both ROM variants on the v0.0.91 feature branch. The Debug SHA-256 was `29b3815fe327ae6fb24c7adbb05a48d1b03761a1ebbcec542cbe01ed8b27f6a0`. The Release SHA-256 was `c629c6f9362769f3b50359bb2de7081d50eea2ba3a61d96f8aa61b1878288332`. Gameplay captures are from the Debug build.
- The visual revision appends one board metatile to each of the Petalburg and Rustboro tilesets. All three map edits retain their original collision and elevation bits. Frame differences at the previous camera positions fell entirely within each 16×16 sign.
