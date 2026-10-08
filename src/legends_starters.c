#include "global.h"
#include "data.h"
#include "event_data.h"
#include "legends_starters.h"
#include "pokemon.h"
#include "random.h"
#include "constants/flags.h"
#include "constants/vars.h"

static const u16 sRandomVars[3] = {VAR_LEGENDS_STARTER_RANDOM_1, VAR_LEGENDS_STARTER_RANDOM_2, VAR_LEGENDS_STARTER_RANDOM_3};

static const u16 sStarterSets[LEGENDS_STARTERS_SPECIAL + 1][3] =
{
    [LEGENDS_STARTERS_GEN_1] = {SPECIES_BULBASAUR, SPECIES_CHARMANDER, SPECIES_SQUIRTLE},
    [LEGENDS_STARTERS_GEN_2] = {SPECIES_CHIKORITA, SPECIES_CYNDAQUIL, SPECIES_TOTODILE},
    [LEGENDS_STARTERS_GEN_3] = {SPECIES_TREECKO, SPECIES_TORCHIC, SPECIES_MUDKIP},
    [LEGENDS_STARTERS_GEN_4] = {SPECIES_TURTWIG, SPECIES_CHIMCHAR, SPECIES_PIPLUP},
    [LEGENDS_STARTERS_GEN_5] = {SPECIES_SNIVY, SPECIES_TEPIG, SPECIES_OSHAWOTT},
    [LEGENDS_STARTERS_GEN_6] = {SPECIES_CHESPIN, SPECIES_FENNEKIN, SPECIES_FROAKIE},
    [LEGENDS_STARTERS_GEN_7] = {SPECIES_ROWLET, SPECIES_LITTEN, SPECIES_POPPLIO},
    [LEGENDS_STARTERS_GEN_8] = {SPECIES_GROOKEY, SPECIES_SCORBUNNY, SPECIES_SOBBLE},
    [LEGENDS_STARTERS_GEN_9] = {SPECIES_SPRIGATITO, SPECIES_FUECOCO, SPECIES_QUAXLY},
    [LEGENDS_STARTERS_SPECIAL] = {SPECIES_HAPPINY, SPECIES_WATTREL, SPECIES_MANKEY},
};

u8 LegendsGetStarterSetting(void)
{
    u16 saved = VarGet(VAR_LEGENDS_STARTER_SETTING);
    return saved > 0 && saved <= LEGENDS_STARTERS_COUNT ? saved - 1 : LEGENDS_STARTERS_GEN_3;
}

void LegendsSetStarterSetting(u8 setting)
{
    if (setting >= LEGENDS_STARTERS_COUNT)
        setting = LEGENDS_STARTERS_GEN_3;
    VarSet(VAR_LEGENDS_STARTER_SETTING, setting + 1);
}

static u8 GetRescueSetting(void)
{
    u16 saved = VarGet(VAR_LEGENDS_STARTER_RESCUE);
    if (saved > 0 && saved <= LEGENDS_STARTERS_COUNT)
        return saved - 1;
    // A pre-feature save with a starter retains its original rival lineage.
    if (FlagGet(FLAG_RESCUED_BIRCH))
        return LEGENDS_STARTERS_GEN_3;
    return LegendsGetStarterSetting();
}

static bool32 IsRandomCandidate(u16 species, const u8 *evolved)
{
    const struct Evolution *evos;
    if (!IsSpeciesEnabled(species)
     || gSpeciesInfo[species].natDexNum == 0
     || GET_BASE_SPECIES_ID(species) != species
     || (evolved[species / 8] & (1 << (species % 8))))
        return FALSE;
    evos = GetSpeciesEvolutions(species);
    if (evos == NULL)
        return FALSE;
    for (u32 i = 0; evos[i].method != EVOLUTIONS_END; i++)
        if (IsSpeciesEnabled(evos[i].targetSpecies))
            return TRUE;
    return FALSE;
}

static void RollRandomStarters(void)
{
    u8 evolved[(NUM_SPECIES + 7) / 8] = {0};
    u16 choices[3] = {SPECIES_TREECKO, SPECIES_TORCHIC, SPECIES_MUDKIP};
    u32 seen = 0;
    // Mark incoming evolution edges once, instead of a full pre-evolution
    // search for every species. Keep forms from weighting a dex entry twice.
    for (u32 species = 1; species < NUM_SPECIES; species++)
    {
        const struct Evolution *evos;
        if (!IsSpeciesEnabled(species))
            continue;
        evos = GetSpeciesEvolutions(species);
        if (evos == NULL)
            continue;
        for (u32 i = 0; evos[i].method != EVOLUTIONS_END; i++)
        {
            u16 target = evos[i].targetSpecies;
            if (target > 0 && target < NUM_SPECIES)
                evolved[target / 8] |= 1 << (target % 8);
        }
    }
    // Reservoir sampling: three distinct entries with equal inclusion odds.
    for (u32 species = 1; species < NUM_SPECIES; species++)
    {
        u32 slot;
        if (!IsRandomCandidate(species, evolved))
            continue;
        seen++;
        slot = seen <= 3 ? seen - 1 : RandomUniform(RNG_NONE, 0, seen - 1);
        if (slot < 3)
            choices[slot] = species;
    }
    Shuffle16(choices, ARRAY_COUNT(choices));
    for (u32 i = 0; i < 3; i++)
        VarSet(sRandomVars[i], choices[i]);
}

void LegendsPrepareStarters(void)
{
    u16 saved = VarGet(VAR_LEGENDS_STARTER_RESCUE);
    if (saved > 0 && saved <= LEGENDS_STARTERS_COUNT)
        return;
    u8 setting = LegendsGetStarterSetting();
    if (setting == LEGENDS_STARTERS_RANDOM)
        RollRandomStarters();
    VarSet(VAR_LEGENDS_STARTER_RESCUE, setting + 1);
}

u16 LegendsGetStarterPokemon(u16 slot)
{
    u8 setting = GetRescueSetting();
    if (slot >= 3)
        slot = 0;
    if (setting == LEGENDS_STARTERS_RANDOM)
    {
        u16 species = VarGet(sRandomVars[slot]);
        return species > 0 && species < NUM_SPECIES && IsSpeciesEnabled(species)
             ? species : sStarterSets[LEGENDS_STARTERS_GEN_3][slot];
    }
    return sStarterSets[setting][slot];
}

static u16 EvolveRivalByLevel(u16 species, u8 level)
{
    // All generation starters and Zorua evolve by ordinary level thresholds.
    for (u32 stage = 0; stage < 2; stage++)
    {
        const struct Evolution *evos = GetSpeciesEvolutions(species);
        u16 next = species;
        if (evos == NULL)
            break;
        for (u32 i = 0; evos[i].method != EVOLUTIONS_END; i++)
            if (evos[i].method == EVO_LEVEL && evos[i].param <= level && IsSpeciesEnabled(evos[i].targetSpecies))
            {
                next = evos[i].targetSpecies;
                break;
            }
        if (next == species)
            break;
        species = next;
    }
    return species;
}

void LegendsCustomizeRivalMon(const struct Trainer *trainer, struct TrainerMon *mon)
{
    u8 setting = GetRescueSetting();
    u8 slot;
    if (IS_FRLG || setting == LEGENDS_STARTERS_GEN_3
     || trainer->trainerClass != TRAINER_CLASS_RIVAL
     || (trainer->trainerPic != TRAINER_PIC_BRENDAN && trainer->trainerPic != TRAINER_PIC_MAY))
        return;
    // The native scripts select the counter's team by grass/fire/water slot.
    // Substitute only that starter member, leaving the rest of the team intact.
    switch (mon->species)
    {
    case SPECIES_TREECKO: case SPECIES_GROVYLE: case SPECIES_SCEPTILE: slot = 0; break;
    case SPECIES_TORCHIC: case SPECIES_COMBUSKEN: case SPECIES_BLAZIKEN: slot = 1; break;
    case SPECIES_MUDKIP: case SPECIES_MARSHTOMP: case SPECIES_SWAMPERT: slot = 2; break;
    default: return;
    }
    mon->species = EvolveRivalByLevel(setting >= LEGENDS_STARTERS_SPECIAL ? SPECIES_ZORUA : sStarterSets[setting][slot], mon->lvl);
    // Native generation will assign this species' current-level moves/ability.
    memset(mon->moves, 0, sizeof(mon->moves));
    mon->ability = ABILITY_NONE;
    mon->teraType = 0;
}
