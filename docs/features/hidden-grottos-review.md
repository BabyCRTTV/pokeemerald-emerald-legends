# Hidden grottos — first review

Status: **unshipped exploration prototype**, based on v0.0.68. Owner requested implementation and previews before publication on 20 October 2026. Layouts, names, roster and renewal rules are proposals pending that review.

Three small, optional shelters reward inspecting the edges of familiar routes. A root gap, a cool draft and footprints provide discoverable clues. Each entrance asks before entering; walking back through the mouth returns to the original approach. Native Hoenn art and species sprites supply every pixel. Existing route artwork and story scripts are unchanged.

| Shelter | Entrance | Character | Environmental clue |
| --- | --- | --- | --- |
| Leafshade Hollow | Southern Petalburg Woods | Shaded clearing, flowers and close tree cover | Nibbled berries and small prints beneath roots |
| Stillwater Nook | Route 114, below the bridge | Compact rocky chamber and clear spring | A stone worn smooth on only one side |
| Rainroot Hollow | Lower Route 119 | Wet foliage, small pool and long grass | Curled leaves shelter a dry sleeping place |

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

- Three appended maps and layouts; three background entrance interactions added to the existing routes.
- Native yes/no entry, walking exits, seasonal overworld visitors with cry/dialogue, environmental clue text and an inspectable item placeholder.
- No battle, capture, item award, cooldown, save-state allocation, version bump, BPS replacement or public-site change in this review.
- Published v0.0.68 and its bedroom-only approval remain the baseline. The rejected badge, sign, pause-menu and outfit proposals remain untouched.

Actual preview frames and verification are in `docs/designs/hidden-grottos/`. Captures use the compiled Legends Debug review ROM under native mGBA 0.10.2, with private controlled scene setup. They are not map-editor compositions. ROMs and private fixtures must not be committed or distributed.
