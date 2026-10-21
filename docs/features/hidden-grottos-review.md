# Hidden grottos — exploration review

Status: **unshipped exploration prototype, third, compact interior review**, based on v0.0.68. Owner requested another cleanup and smaller grotto interiors after the discovery review. Layouts, names, roster and renewal rules remain proposals pending review.

Three small, optional shelters reward inspecting the edges of familiar routes. A vine-framed trunk, a rock crevice and a gap in the undergrowth provide visible clues. Each entrance asks before entering; walking back through the mouth returns to the original approach. Native Hoenn art and species sprites supply every pixel. Ten bounded route cells show the openings; existing route events, warps and story scripts retain their meanings.

| Shelter | Entrance | Character | Environmental clue |
| --- | --- | --- | --- |
| Leafshade Hollow | Southern Petalburg Woods, beside the lower Trainer Tips sign | Shaded clearing, flowers and close tree cover | Nibbled berries and small prints beneath roots |
| Stillwater Nook | Route 114, southwest of Lanette's house | Compact rocky chamber and clear spring | A stone worn smooth on only one side |
| Rainroot Hollow | Lower Route 119, northwest of the small house | Wet foliage, small reflective pool and long grass | Curled leaves shelter a dry sleeping place |

The compact revision reduces each map from **22×20 to 18×16 tiles** (35% less map area), draws the canopy/walls closer around the visitor and keeps a clear central approach. Stillwater uses a simpler continuous chamber wall and a narrower spring; the outdoor shelters use smaller, grouped planting and complete native trees. Route entrances and return points are unchanged. [Current native preview](../designs/hidden-grottos/Emerald-Legends-Grottos-Compact-Preview.png).

## Finding and entering

These use the existing area's access conditions. Leafshade is an early discovery in the southern woods; Stillwater and Rainroot become reachable as the player reaches their routes. Once at an opening, no special move or item is required.

Walk up to the visible opening and press **A**. A short description mentions the draft, trail or footprints, followed by an **Explore [name]?** Yes/No choice. Yes fades into the separate grotto map. No leaves the player outside. Walking back through the mouth returns to a passable tile beside the same opening. Both halves of Leafshade's vine-framed trunk accept examination.

The borrowed native entrance graphics carry Secret Base behavior. A coordinate-specific door-warp guard isolates exactly these four interaction cells from the native auto-warp; all other Secret Base positions retain the original path. The route 119 return is now `(27,106)`, directly below its complete undergrowth opening.

The [discovery clip](../designs/hidden-grottos/Emerald-Legends-Grotto-Discovery.gif) records a real native walk from three tiles away, then examination, confirmation, fade and arrival. Private QA setup places the player at the start of that short approach; it does not depict a complete new-game journey.

## Proposed visitor rotation

| Shelter | Spring | Summer | Autumn | Winter | Proposed level |
| --- | --- | --- | --- | --- | --- |
| Leafshade | Buneary | Fomantis | Shroomish | Minccino | 8 |
| Stillwater | Marill | Barboach | Wooper | Snorunt | 18 |
| Rainroot | Morelull | Tropius | Goomy | Swablu | 25 |

The prototype selects the displayed species from the existing **committed visible season**, matching seasonal scenery. Visitors can be approached and heard. Interior grass is scenery, without a random encounter table.

## Proposed finished loop — not implemented in this review

1. Inspect a discreet entrance and choose to enter.
2. Find one optional visible Pokémon encounter and one small item cache. Choose whether to approach the Pokémon; use ordinary capture mechanics and the player's existing shiny setting.
3. Read the environmental clue for a short sense of who lives there. No mandatory story interruption.
4. After clearing the shelter, travel another **1,024 overworld steps** to refresh it. This proposal works with either clock mode. Contents remain stable across leaving, Continue and clock/season-option changes until the refresh is earned. The next visit uses the committed season for the new visitor.

Suggested item themes are berries in Leafshade, ordinary healing items or Great Balls in Stillwater, and berries or Net Balls in Rainroot. Quantities and renewal balance remain review decisions.

Before shipping that loop, add signed persistent state, audit shared Hoenn/FireRed variable aliases, preserve old saves and map IDs, cover full-Bag retries, capture/storage outcomes, defeat/flee/whiteout handling and repeated Continue. Trace related capture/research/achievement hooks through native battle entry. Synchronize the final wiki/LegendsDex after a verified release.

## Implemented review scope

- Three appended maps and layouts; four background interaction cells at three entrances added to the existing routes.
- Native yes/no entry, walking exits, seasonal overworld visitors with cry/dialogue, environmental clue text and an inspectable item placeholder.
- No battle, capture, item award, cooldown, save-state allocation, version bump, BPS replacement or public-site change in this review.
- Published v0.0.68 and its bedroom-only approval remain the baseline. The rejected badge, sign, pause-menu and outfit proposals remain untouched.

Actual preview frames and verification are in `docs/designs/hidden-grottos/`. Captures use the compiled Legends Debug review ROM under native mGBA 0.10.2, with private controlled scene setup. They are not map-editor compositions. ROMs and private fixtures must not be committed or distributed.
