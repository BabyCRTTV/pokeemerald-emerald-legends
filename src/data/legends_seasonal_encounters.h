// Four-route grass encounter trial. Levels, rates and native slot weights are unchanged.
// See docs/features/seasonal-encounters.md for the full distribution and approval state.
struct LegendsSeasonalLandTable
{
    u16 map;
    struct WildPokemonInfo seasons[LEGENDS_SEASON_COUNT];
};

static const struct WildPokemon sRoute101SpringMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {2, 2, SPECIES_WURMPLE},
    {2, 2, SPECIES_POOCHYENA},
    {2, 2, SPECIES_WURMPLE},
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_SCATTERBUG},
    {3, 3, SPECIES_SCATTERBUG},
    {3, 3, SPECIES_FLETCHLING},
    {2, 2, SPECIES_SCATTERBUG},
    {2, 2, SPECIES_FLETCHLING},
    {3, 3, SPECIES_SCATTERBUG},
    {3, 3, SPECIES_FLETCHLING},
};

static const struct WildPokemon sRoute101SummerMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {2, 2, SPECIES_WURMPLE},
    {2, 2, SPECIES_POOCHYENA},
    {2, 2, SPECIES_WURMPLE},
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_SUNKERN},
    {3, 3, SPECIES_SUNKERN},
    {3, 3, SPECIES_HOPPIP},
    {2, 2, SPECIES_SUNKERN},
    {2, 2, SPECIES_HOPPIP},
    {3, 3, SPECIES_SUNKERN},
    {3, 3, SPECIES_HOPPIP},
};

static const struct WildPokemon sRoute101AutumnMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {2, 2, SPECIES_WURMPLE},
    {2, 2, SPECIES_POOCHYENA},
    {2, 2, SPECIES_WURMPLE},
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_SENTRET},
    {3, 3, SPECIES_SENTRET},
    {3, 3, SPECIES_TAROUNTULA},
    {2, 2, SPECIES_SENTRET},
    {2, 2, SPECIES_TAROUNTULA},
    {3, 3, SPECIES_SENTRET},
    {3, 3, SPECIES_TAROUNTULA},
};

static const struct WildPokemon sRoute101WinterMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {2, 2, SPECIES_WURMPLE},
    {2, 2, SPECIES_POOCHYENA},
    {2, 2, SPECIES_WURMPLE},
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_SKWOVET},
    {3, 3, SPECIES_SKWOVET},
    {3, 3, SPECIES_ROOKIDEE},
    {2, 2, SPECIES_SKWOVET},
    {2, 2, SPECIES_ROOKIDEE},
    {3, 3, SPECIES_SKWOVET},
    {3, 3, SPECIES_ROOKIDEE},
};

static const struct WildPokemon sRoute102SpringMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_WURMPLE},
    {4, 4, SPECIES_LOTAD},
    {4, 4, SPECIES_LOTAD},
    {3, 3, SPECIES_BUDEW},
    {4, 4, SPECIES_BUDEW},
    {3, 3, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_AZURILL},
    {4, 4, SPECIES_RALTS},
    {4, 4, SPECIES_AZURILL},
    {4, 4, SPECIES_SEEDOT},
    {3, 3, SPECIES_AZURILL},
};

static const struct WildPokemon sRoute102SummerMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_WURMPLE},
    {4, 4, SPECIES_LOTAD},
    {4, 4, SPECIES_LOTAD},
    {3, 3, SPECIES_SURSKIT},
    {4, 4, SPECIES_SURSKIT},
    {3, 3, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_TYMPOLE},
    {4, 4, SPECIES_RALTS},
    {4, 4, SPECIES_TYMPOLE},
    {4, 4, SPECIES_SEEDOT},
    {3, 3, SPECIES_TYMPOLE},
};

static const struct WildPokemon sRoute102AutumnMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_WURMPLE},
    {4, 4, SPECIES_LOTAD},
    {4, 4, SPECIES_LOTAD},
    {3, 3, SPECIES_SEWADDLE},
    {4, 4, SPECIES_SEWADDLE},
    {3, 3, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_SMOLIV},
    {4, 4, SPECIES_RALTS},
    {4, 4, SPECIES_SMOLIV},
    {4, 4, SPECIES_SEEDOT},
    {3, 3, SPECIES_SMOLIV},
};

static const struct WildPokemon sRoute102WinterMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_WURMPLE},
    {4, 4, SPECIES_LOTAD},
    {4, 4, SPECIES_LOTAD},
    {3, 3, SPECIES_WOOPER},
    {4, 4, SPECIES_WOOPER},
    {3, 3, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_DUCKLETT},
    {4, 4, SPECIES_RALTS},
    {4, 4, SPECIES_DUCKLETT},
    {4, 4, SPECIES_SEEDOT},
    {3, 3, SPECIES_DUCKLETT},
};

static const struct WildPokemon sRoute103SpringMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {2, 2, SPECIES_POOCHYENA},
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_ZIGZAGOON},
    {4, 4, SPECIES_WINGULL},
    {2, 2, SPECIES_PIDOVE},
    {3, 3, SPECIES_PIDOVE},
    {3, 3, SPECIES_ZIGZAGOON},
    {4, 4, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_BUNNELBY},
    {3, 3, SPECIES_BUNNELBY},
    {2, 2, SPECIES_BUNNELBY},
    {4, 4, SPECIES_BUNNELBY},
};

static const struct WildPokemon sRoute103SummerMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {2, 2, SPECIES_POOCHYENA},
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_ZIGZAGOON},
    {4, 4, SPECIES_WINGULL},
    {2, 2, SPECIES_BUIZEL},
    {3, 3, SPECIES_BUIZEL},
    {3, 3, SPECIES_ZIGZAGOON},
    {4, 4, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_WATTREL},
    {3, 3, SPECIES_WATTREL},
    {2, 2, SPECIES_WATTREL},
    {4, 4, SPECIES_WATTREL},
};

static const struct WildPokemon sRoute103AutumnMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {2, 2, SPECIES_POOCHYENA},
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_ZIGZAGOON},
    {4, 4, SPECIES_WINGULL},
    {2, 2, SPECIES_NIDORAN_F},
    {3, 3, SPECIES_NIDORAN_F},
    {3, 3, SPECIES_ZIGZAGOON},
    {4, 4, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_NICKIT},
    {3, 3, SPECIES_NICKIT},
    {2, 2, SPECIES_NICKIT},
    {4, 4, SPECIES_NICKIT},
};

static const struct WildPokemon sRoute103WinterMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {2, 2, SPECIES_POOCHYENA},
    {3, 3, SPECIES_POOCHYENA},
    {3, 3, SPECIES_ZIGZAGOON},
    {4, 4, SPECIES_WINGULL},
    {2, 2, SPECIES_SPHEAL},
    {3, 3, SPECIES_SPHEAL},
    {3, 3, SPECIES_ZIGZAGOON},
    {4, 4, SPECIES_ZIGZAGOON},
    {3, 3, SPECIES_LILLIPUP},
    {3, 3, SPECIES_LILLIPUP},
    {2, 2, SPECIES_LILLIPUP},
    {4, 4, SPECIES_LILLIPUP},
};

static const struct WildPokemon sRoute104SpringMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {4, 4, SPECIES_POOCHYENA},
    {4, 4, SPECIES_WURMPLE},
    {5, 5, SPECIES_POOCHYENA},
    {5, 5, SPECIES_MARILL},
    {4, 4, SPECIES_CATERPIE},
    {5, 5, SPECIES_CATERPIE},
    {4, 4, SPECIES_TAILLOW},
    {5, 5, SPECIES_WINGULL},
    {4, 4, SPECIES_CUTIEFLY},
    {4, 4, SPECIES_CUTIEFLY},
    {3, 3, SPECIES_CUTIEFLY},
    {5, 5, SPECIES_CUTIEFLY},
};

static const struct WildPokemon sRoute104SummerMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {4, 4, SPECIES_POOCHYENA},
    {4, 4, SPECIES_WURMPLE},
    {5, 5, SPECIES_POOCHYENA},
    {5, 5, SPECIES_MARILL},
    {4, 4, SPECIES_FOMANTIS},
    {5, 5, SPECIES_FOMANTIS},
    {4, 4, SPECIES_TAILLOW},
    {5, 5, SPECIES_WINGULL},
    {4, 4, SPECIES_LEDYBA},
    {4, 4, SPECIES_LEDYBA},
    {3, 3, SPECIES_LEDYBA},
    {5, 5, SPECIES_LEDYBA},
};

static const struct WildPokemon sRoute104AutumnMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {4, 4, SPECIES_POOCHYENA},
    {4, 4, SPECIES_WURMPLE},
    {5, 5, SPECIES_POOCHYENA},
    {5, 5, SPECIES_MARILL},
    {4, 4, SPECIES_DEERLING_AUTUMN},
    {5, 5, SPECIES_DEERLING_AUTUMN},
    {4, 4, SPECIES_TAILLOW},
    {5, 5, SPECIES_WINGULL},
    {4, 4, SPECIES_SHROOMISH},
    {4, 4, SPECIES_SHROOMISH},
    {3, 3, SPECIES_SHROOMISH},
    {5, 5, SPECIES_SHROOMISH},
};

static const struct WildPokemon sRoute104WinterMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {4, 4, SPECIES_POOCHYENA},
    {4, 4, SPECIES_WURMPLE},
    {5, 5, SPECIES_POOCHYENA},
    {5, 5, SPECIES_MARILL},
    {4, 4, SPECIES_SNORUNT},
    {5, 5, SPECIES_SNORUNT},
    {4, 4, SPECIES_TAILLOW},
    {5, 5, SPECIES_WINGULL},
    {4, 4, SPECIES_SANDSHREW_ALOLA},
    {4, 4, SPECIES_SANDSHREW_ALOLA},
    {3, 3, SPECIES_SANDSHREW_ALOLA},
    {5, 5, SPECIES_SANDSHREW_ALOLA},
};

static const struct LegendsSeasonalLandTable sLegendsSeasonalLand[] =
{
    {MAP_ROUTE101, {
        [LEGENDS_SPRING] = {20, sRoute101SpringMons},
        [LEGENDS_SUMMER] = {20, sRoute101SummerMons},
        [LEGENDS_AUTUMN] = {20, sRoute101AutumnMons},
        [LEGENDS_WINTER] = {20, sRoute101WinterMons},
    }},
    {MAP_ROUTE102, {
        [LEGENDS_SPRING] = {20, sRoute102SpringMons},
        [LEGENDS_SUMMER] = {20, sRoute102SummerMons},
        [LEGENDS_AUTUMN] = {20, sRoute102AutumnMons},
        [LEGENDS_WINTER] = {20, sRoute102WinterMons},
    }},
    {MAP_ROUTE103, {
        [LEGENDS_SPRING] = {20, sRoute103SpringMons},
        [LEGENDS_SUMMER] = {20, sRoute103SummerMons},
        [LEGENDS_AUTUMN] = {20, sRoute103AutumnMons},
        [LEGENDS_WINTER] = {20, sRoute103WinterMons},
    }},
    {MAP_ROUTE104, {
        [LEGENDS_SPRING] = {20, sRoute104SpringMons},
        [LEGENDS_SUMMER] = {20, sRoute104SummerMons},
        [LEGENDS_AUTUMN] = {20, sRoute104AutumnMons},
        [LEGENDS_WINTER] = {20, sRoute104WinterMons},
    }},
};
