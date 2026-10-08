# Selectable Wild Shiny Rate

**Introduced:** 0.0.10

Legends Options (L/R -> Legends 2/2) adds SHINY RATE, controlled by Left/Right.

| Selection | Base shiny chance |
| --- | --- |
| 1/8192 | Default for new and older saves |
| 1/5680 | Moderately increased chance |
| 1/1226 | Increased chance |

The index lives in `VAR_LEGENDS_SHINY_RATE` (formerly unused 0x40E5), where zero means 1/8192. No save block structure changes. Selecting a new rate is saved on exit from Options.

## Scope

The rate is applied only while `CreateWildMon` calls the standard player-OT shiny generation path. This covers wild grass, water, fishing, and DexNav wild opponents. The temporary context is reset immediately after generating each opponent. Eggs, gift Pokémon, scripted and roaming Pokémon generated via other functions, trainer Pokémon, and existing PC/party entries remain unchanged.

The base 1/N probability uses unbiased 16-bit rejection sampling: random values outside the largest complete multiple of N in 65,536 are discarded, then the accepted value is compared modulo N. Existing extra shiny rolls (Shiny Charm, chain fishing, DexNav and other configured bonuses) continue to apply; they can raise the *effective* odds beyond the displayed base setting. Force-shiny and force-nonshiny flags take priority.

The original expansion shiny calculation for nonwild Pokémon is left untouched. The shiny result remains stored via the existing mon shiny modifier and is not recalculated when players change their Options later.
