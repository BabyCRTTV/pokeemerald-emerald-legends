// Seasonal land (101-104, 110-116) and Surf (105-109); native slot levels/rates/weights.
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

static const struct WildPokemon sRoute110SpringMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {12, 12, SPECIES_POOCHYENA},
    {12, 12, SPECIES_COMBEE},
    {12, 12, SPECIES_GULPIN},
    {13, 13, SPECIES_ELECTRIKE},
    {13, 13, SPECIES_MINUN},
    {13, 13, SPECIES_PETILIL},
    {13, 13, SPECIES_ODDISH},
    {13, 13, SPECIES_MINUN},
    {12, 12, SPECIES_WINGULL},
    {12, 12, SPECIES_WINGULL},
    {12, 12, SPECIES_PLUSLE},
    {13, 13, SPECIES_PLUSLE},
};

static const struct WildPokemon sRoute110SummerMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {12, 12, SPECIES_POOCHYENA},
    {12, 12, SPECIES_YAMPER},
    {12, 12, SPECIES_GULPIN},
    {13, 13, SPECIES_ELECTRIKE},
    {13, 13, SPECIES_MINUN},
    {13, 13, SPECIES_BLITZLE},
    {13, 13, SPECIES_ODDISH},
    {13, 13, SPECIES_MINUN},
    {12, 12, SPECIES_WINGULL},
    {12, 12, SPECIES_WINGULL},
    {12, 12, SPECIES_PLUSLE},
    {13, 13, SPECIES_PLUSLE},
};

static const struct WildPokemon sRoute110AutumnMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {12, 12, SPECIES_POOCHYENA},
    {12, 12, SPECIES_TRUBBISH},
    {12, 12, SPECIES_GULPIN},
    {13, 13, SPECIES_ELECTRIKE},
    {13, 13, SPECIES_MINUN},
    {13, 13, SPECIES_SHROODLE},
    {13, 13, SPECIES_ODDISH},
    {13, 13, SPECIES_MINUN},
    {12, 12, SPECIES_WINGULL},
    {12, 12, SPECIES_WINGULL},
    {12, 12, SPECIES_PLUSLE},
    {13, 13, SPECIES_PLUSLE},
};

static const struct WildPokemon sRoute110WinterMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {12, 12, SPECIES_POOCHYENA},
    {12, 12, SPECIES_PACHIRISU},
    {12, 12, SPECIES_GULPIN},
    {13, 13, SPECIES_ELECTRIKE},
    {13, 13, SPECIES_MINUN},
    {13, 13, SPECIES_EMOLGA},
    {13, 13, SPECIES_ODDISH},
    {13, 13, SPECIES_MINUN},
    {12, 12, SPECIES_WINGULL},
    {12, 12, SPECIES_WINGULL},
    {12, 12, SPECIES_PLUSLE},
    {13, 13, SPECIES_PLUSLE},
};

static const struct WildPokemon sRoute111SpringMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {20, 20, SPECIES_SANDSHREW},
    {20, 20, SPECIES_TRAPINCH},
    {21, 21, SPECIES_SANDSHREW},
    {21, 21, SPECIES_TRAPINCH},
    {19, 19, SPECIES_SANDILE},
    {21, 21, SPECIES_SANDILE},
    {19, 19, SPECIES_HELIOPTILE},
    {19, 19, SPECIES_HELIOPTILE},
    {20, 20, SPECIES_BALTOY},
    {20, 20, SPECIES_CACNEA},
    {22, 22, SPECIES_CACNEA},
    {22, 22, SPECIES_CACNEA},
};

static const struct WildPokemon sRoute111SummerMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {20, 20, SPECIES_SANDSHREW},
    {20, 20, SPECIES_TRAPINCH},
    {21, 21, SPECIES_SANDSHREW},
    {21, 21, SPECIES_TRAPINCH},
    {19, 19, SPECIES_SILICOBRA},
    {21, 21, SPECIES_SILICOBRA},
    {19, 19, SPECIES_HIPPOPOTAS},
    {19, 19, SPECIES_HIPPOPOTAS},
    {20, 20, SPECIES_BALTOY},
    {20, 20, SPECIES_CACNEA},
    {22, 22, SPECIES_CACNEA},
    {22, 22, SPECIES_CACNEA},
};

static const struct WildPokemon sRoute111AutumnMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {20, 20, SPECIES_SANDSHREW},
    {20, 20, SPECIES_TRAPINCH},
    {21, 21, SPECIES_SANDSHREW},
    {21, 21, SPECIES_TRAPINCH},
    {19, 19, SPECIES_DWEBBLE},
    {21, 21, SPECIES_DWEBBLE},
    {19, 19, SPECIES_SKORUPI},
    {19, 19, SPECIES_SKORUPI},
    {20, 20, SPECIES_BALTOY},
    {20, 20, SPECIES_CACNEA},
    {22, 22, SPECIES_CACNEA},
    {22, 22, SPECIES_CACNEA},
};

static const struct WildPokemon sRoute111WinterMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {20, 20, SPECIES_SANDSHREW},
    {20, 20, SPECIES_TRAPINCH},
    {21, 21, SPECIES_SANDSHREW},
    {21, 21, SPECIES_TRAPINCH},
    {19, 19, SPECIES_PHANPY},
    {21, 21, SPECIES_PHANPY},
    {19, 19, SPECIES_GIBLE},
    {19, 19, SPECIES_GIBLE},
    {20, 20, SPECIES_BALTOY},
    {20, 20, SPECIES_CACNEA},
    {22, 22, SPECIES_CACNEA},
    {22, 22, SPECIES_CACNEA},
};

static const struct WildPokemon sRoute112SpringMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {15, 15, SPECIES_NUMEL},
    {15, 15, SPECIES_NUMEL},
    {15, 15, SPECIES_MARILL},
    {14, 14, SPECIES_NUMEL},
    {14, 14, SPECIES_PONYTA},
    {14, 14, SPECIES_PONYTA},
    {16, 16, SPECIES_NUMEL},
    {16, 16, SPECIES_MARILL},
    {16, 16, SPECIES_DEERLING},
    {16, 16, SPECIES_DEERLING},
    {16, 16, SPECIES_DEERLING},
    {16, 16, SPECIES_DEERLING},
};

static const struct WildPokemon sRoute112SummerMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {15, 15, SPECIES_NUMEL},
    {15, 15, SPECIES_NUMEL},
    {15, 15, SPECIES_MARILL},
    {14, 14, SPECIES_NUMEL},
    {14, 14, SPECIES_LITLEO},
    {14, 14, SPECIES_LITLEO},
    {16, 16, SPECIES_NUMEL},
    {16, 16, SPECIES_MARILL},
    {16, 16, SPECIES_SIZZLIPEDE},
    {16, 16, SPECIES_SIZZLIPEDE},
    {16, 16, SPECIES_SIZZLIPEDE},
    {16, 16, SPECIES_SIZZLIPEDE},
};

static const struct WildPokemon sRoute112AutumnMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {15, 15, SPECIES_NUMEL},
    {15, 15, SPECIES_NUMEL},
    {15, 15, SPECIES_MARILL},
    {14, 14, SPECIES_NUMEL},
    {14, 14, SPECIES_HOUNDOUR},
    {14, 14, SPECIES_HOUNDOUR},
    {16, 16, SPECIES_NUMEL},
    {16, 16, SPECIES_MARILL},
    {16, 16, SPECIES_ROLYCOLY},
    {16, 16, SPECIES_ROLYCOLY},
    {16, 16, SPECIES_ROLYCOLY},
    {16, 16, SPECIES_ROLYCOLY},
};

static const struct WildPokemon sRoute112WinterMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {15, 15, SPECIES_NUMEL},
    {15, 15, SPECIES_NUMEL},
    {15, 15, SPECIES_MARILL},
    {14, 14, SPECIES_NUMEL},
    {14, 14, SPECIES_VULPIX},
    {14, 14, SPECIES_VULPIX},
    {16, 16, SPECIES_NUMEL},
    {16, 16, SPECIES_MARILL},
    {16, 16, SPECIES_ROCKRUFF},
    {16, 16, SPECIES_ROCKRUFF},
    {16, 16, SPECIES_ROCKRUFF},
    {16, 16, SPECIES_ROCKRUFF},
};

static const struct WildPokemon sRoute113SpringMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {15, 15, SPECIES_SPINDA},
    {15, 15, SPECIES_GROWLITHE},
    {15, 15, SPECIES_SLUGMA},
    {14, 14, SPECIES_SPINDA},
    {14, 14, SPECIES_RUFFLET},
    {14, 14, SPECIES_SLUGMA},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SLUGMA},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SKARMORY},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SKARMORY},
};

static const struct WildPokemon sRoute113SummerMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {15, 15, SPECIES_SPINDA},
    {15, 15, SPECIES_SALANDIT},
    {15, 15, SPECIES_SLUGMA},
    {14, 14, SPECIES_SPINDA},
    {14, 14, SPECIES_CHARCADET},
    {14, 14, SPECIES_SLUGMA},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SLUGMA},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SKARMORY},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SKARMORY},
};

static const struct WildPokemon sRoute113AutumnMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {15, 15, SPECIES_SPINDA},
    {15, 15, SPECIES_VULLABY},
    {15, 15, SPECIES_SLUGMA},
    {14, 14, SPECIES_SPINDA},
    {14, 14, SPECIES_KLINK},
    {14, 14, SPECIES_SLUGMA},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SLUGMA},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SKARMORY},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SKARMORY},
};

static const struct WildPokemon sRoute113WinterMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {15, 15, SPECIES_SPINDA},
    {15, 15, SPECIES_SNEASEL},
    {15, 15, SPECIES_SLUGMA},
    {14, 14, SPECIES_SPINDA},
    {14, 14, SPECIES_BRONZOR},
    {14, 14, SPECIES_SLUGMA},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SLUGMA},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SKARMORY},
    {16, 16, SPECIES_SPINDA},
    {16, 16, SPECIES_SKARMORY},
};

static const struct WildPokemon sRoute114SpringMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {16, 16, SPECIES_SWABLU},
    {16, 16, SPECIES_BOUNSWEET},
    {17, 17, SPECIES_SWABLU},
    {15, 15, SPECIES_LOTAD},
    {15, 15, SPECIES_APPLIN},
    {16, 16, SPECIES_LOMBRE},
    {16, 16, SPECIES_LOMBRE},
    {18, 18, SPECIES_LOMBRE},
    {17, 17, SPECIES_SEVIPER},
    {15, 15, SPECIES_SEVIPER},
    {17, 17, SPECIES_SEVIPER},
    {15, 15, SPECIES_NUZLEAF},
};

static const struct WildPokemon sRoute114SummerMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {16, 16, SPECIES_SWABLU},
    {16, 16, SPECIES_SKIDDO},
    {17, 17, SPECIES_SWABLU},
    {15, 15, SPECIES_LOTAD},
    {15, 15, SPECIES_PANCHAM},
    {16, 16, SPECIES_LOMBRE},
    {16, 16, SPECIES_LOMBRE},
    {18, 18, SPECIES_LOMBRE},
    {17, 17, SPECIES_SEVIPER},
    {15, 15, SPECIES_SEVIPER},
    {17, 17, SPECIES_SEVIPER},
    {15, 15, SPECIES_NUZLEAF},
};

static const struct WildPokemon sRoute114AutumnMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {16, 16, SPECIES_SWABLU},
    {16, 16, SPECIES_TEDDIURSA},
    {17, 17, SPECIES_SWABLU},
    {15, 15, SPECIES_LOTAD},
    {15, 15, SPECIES_MORELULL},
    {16, 16, SPECIES_LOMBRE},
    {16, 16, SPECIES_LOMBRE},
    {18, 18, SPECIES_LOMBRE},
    {17, 17, SPECIES_SEVIPER},
    {15, 15, SPECIES_SEVIPER},
    {17, 17, SPECIES_SEVIPER},
    {15, 15, SPECIES_NUZLEAF},
};

static const struct WildPokemon sRoute114WinterMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {16, 16, SPECIES_SWABLU},
    {16, 16, SPECIES_SNOVER},
    {17, 17, SPECIES_SWABLU},
    {15, 15, SPECIES_LOTAD},
    {15, 15, SPECIES_CETODDLE},
    {16, 16, SPECIES_LOMBRE},
    {16, 16, SPECIES_LOMBRE},
    {18, 18, SPECIES_LOMBRE},
    {17, 17, SPECIES_SEVIPER},
    {15, 15, SPECIES_SEVIPER},
    {17, 17, SPECIES_SEVIPER},
    {15, 15, SPECIES_NUZLEAF},
};

static const struct WildPokemon sRoute115SpringMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {23, 23, SPECIES_SWABLU},
    {23, 23, SPECIES_MIENFOO},
    {25, 25, SPECIES_SWABLU},
    {24, 24, SPECIES_TAILLOW},
    {25, 25, SPECIES_FARFETCHD},
    {25, 25, SPECIES_SWELLOW},
    {24, 24, SPECIES_JIGGLYPUFF},
    {25, 25, SPECIES_JIGGLYPUFF},
    {24, 24, SPECIES_WINGULL},
    {24, 24, SPECIES_WINGULL},
    {26, 26, SPECIES_WINGULL},
    {25, 25, SPECIES_WINGULL},
};

static const struct WildPokemon sRoute115SummerMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {23, 23, SPECIES_SWABLU},
    {23, 23, SPECIES_HAWLUCHA},
    {25, 25, SPECIES_SWABLU},
    {24, 24, SPECIES_TAILLOW},
    {25, 25, SPECIES_PASSIMIAN},
    {25, 25, SPECIES_SWELLOW},
    {24, 24, SPECIES_JIGGLYPUFF},
    {25, 25, SPECIES_JIGGLYPUFF},
    {24, 24, SPECIES_WINGULL},
    {24, 24, SPECIES_WINGULL},
    {26, 26, SPECIES_WINGULL},
    {25, 25, SPECIES_WINGULL},
};

static const struct WildPokemon sRoute115AutumnMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {23, 23, SPECIES_SWABLU},
    {23, 23, SPECIES_ZANGOOSE},
    {25, 25, SPECIES_SWABLU},
    {24, 24, SPECIES_TAILLOW},
    {25, 25, SPECIES_MURKROW},
    {25, 25, SPECIES_SWELLOW},
    {24, 24, SPECIES_JIGGLYPUFF},
    {25, 25, SPECIES_JIGGLYPUFF},
    {24, 24, SPECIES_WINGULL},
    {24, 24, SPECIES_WINGULL},
    {26, 26, SPECIES_WINGULL},
    {25, 25, SPECIES_WINGULL},
};

static const struct WildPokemon sRoute115WinterMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {23, 23, SPECIES_SWABLU},
    {23, 23, SPECIES_MINCCINO},
    {25, 25, SPECIES_SWABLU},
    {24, 24, SPECIES_TAILLOW},
    {25, 25, SPECIES_ABSOL},
    {25, 25, SPECIES_SWELLOW},
    {24, 24, SPECIES_JIGGLYPUFF},
    {25, 25, SPECIES_JIGGLYPUFF},
    {24, 24, SPECIES_WINGULL},
    {24, 24, SPECIES_WINGULL},
    {26, 26, SPECIES_WINGULL},
    {25, 25, SPECIES_WINGULL},
};

static const struct WildPokemon sRoute116SpringMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {6, 6, SPECIES_PICHU},
    {6, 6, SPECIES_WHISMUR},
    {6, 6, SPECIES_NINCADA},
    {7, 7, SPECIES_ABRA},
    {7, 7, SPECIES_BUNEARY},
    {6, 6, SPECIES_TAILLOW},
    {7, 7, SPECIES_TAILLOW},
    {8, 8, SPECIES_TAILLOW},
    {7, 7, SPECIES_POOCHYENA},
    {8, 8, SPECIES_POOCHYENA},
    {7, 7, SPECIES_SKITTY},
    {8, 8, SPECIES_SKITTY},
};

static const struct WildPokemon sRoute116SummerMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {6, 6, SPECIES_KRICKETOT},
    {6, 6, SPECIES_WHISMUR},
    {6, 6, SPECIES_NINCADA},
    {7, 7, SPECIES_ABRA},
    {7, 7, SPECIES_BLIPBUG},
    {6, 6, SPECIES_TAILLOW},
    {7, 7, SPECIES_TAILLOW},
    {8, 8, SPECIES_TAILLOW},
    {7, 7, SPECIES_POOCHYENA},
    {8, 8, SPECIES_POOCHYENA},
    {7, 7, SPECIES_SKITTY},
    {8, 8, SPECIES_SKITTY},
};

static const struct WildPokemon sRoute116AutumnMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {6, 6, SPECIES_NYMBLE},
    {6, 6, SPECIES_WHISMUR},
    {6, 6, SPECIES_NINCADA},
    {7, 7, SPECIES_ABRA},
    {7, 7, SPECIES_PATRAT},
    {6, 6, SPECIES_TAILLOW},
    {7, 7, SPECIES_TAILLOW},
    {8, 8, SPECIES_TAILLOW},
    {7, 7, SPECIES_POOCHYENA},
    {8, 8, SPECIES_POOCHYENA},
    {7, 7, SPECIES_SKITTY},
    {8, 8, SPECIES_SKITTY},
};

static const struct WildPokemon sRoute116WinterMons[NUM_LAND_MONS_ENCOUNTER_SLOTS] =
{
    {6, 6, SPECIES_WOOLOO},
    {6, 6, SPECIES_WHISMUR},
    {6, 6, SPECIES_NINCADA},
    {7, 7, SPECIES_ABRA},
    {7, 7, SPECIES_ESPURR},
    {6, 6, SPECIES_TAILLOW},
    {7, 7, SPECIES_TAILLOW},
    {8, 8, SPECIES_TAILLOW},
    {7, 7, SPECIES_POOCHYENA},
    {8, 8, SPECIES_POOCHYENA},
    {7, 7, SPECIES_SKITTY},
    {8, 8, SPECIES_SKITTY},
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
    {MAP_ROUTE110, {
        [LEGENDS_SPRING] = {20, sRoute110SpringMons},
        [LEGENDS_SUMMER] = {20, sRoute110SummerMons},
        [LEGENDS_AUTUMN] = {20, sRoute110AutumnMons},
        [LEGENDS_WINTER] = {20, sRoute110WinterMons},
    }},
    {MAP_ROUTE111, {
        [LEGENDS_SPRING] = {10, sRoute111SpringMons},
        [LEGENDS_SUMMER] = {10, sRoute111SummerMons},
        [LEGENDS_AUTUMN] = {10, sRoute111AutumnMons},
        [LEGENDS_WINTER] = {10, sRoute111WinterMons},
    }},
    {MAP_ROUTE112, {
        [LEGENDS_SPRING] = {20, sRoute112SpringMons},
        [LEGENDS_SUMMER] = {20, sRoute112SummerMons},
        [LEGENDS_AUTUMN] = {20, sRoute112AutumnMons},
        [LEGENDS_WINTER] = {20, sRoute112WinterMons},
    }},
    {MAP_ROUTE113, {
        [LEGENDS_SPRING] = {20, sRoute113SpringMons},
        [LEGENDS_SUMMER] = {20, sRoute113SummerMons},
        [LEGENDS_AUTUMN] = {20, sRoute113AutumnMons},
        [LEGENDS_WINTER] = {20, sRoute113WinterMons},
    }},
    {MAP_ROUTE114, {
        [LEGENDS_SPRING] = {20, sRoute114SpringMons},
        [LEGENDS_SUMMER] = {20, sRoute114SummerMons},
        [LEGENDS_AUTUMN] = {20, sRoute114AutumnMons},
        [LEGENDS_WINTER] = {20, sRoute114WinterMons},
    }},
    {MAP_ROUTE115, {
        [LEGENDS_SPRING] = {20, sRoute115SpringMons},
        [LEGENDS_SUMMER] = {20, sRoute115SummerMons},
        [LEGENDS_AUTUMN] = {20, sRoute115AutumnMons},
        [LEGENDS_WINTER] = {20, sRoute115WinterMons},
    }},
    {MAP_ROUTE116, {
        [LEGENDS_SPRING] = {20, sRoute116SpringMons},
        [LEGENDS_SUMMER] = {20, sRoute116SummerMons},
        [LEGENDS_AUTUMN] = {20, sRoute116AutumnMons},
        [LEGENDS_WINTER] = {20, sRoute116WinterMons},
    }},
};

// Native Surf weights: 60/30/5/4/1. Residents retain 65%; visitors 30%/5%.
struct LegendsSeasonalWaterTable
{
    u16 map;
    struct WildPokemonInfo seasons[LEGENDS_SEASON_COUNT];
};

static const struct WildPokemon sRoute105SpringWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_FINNEON},
    {15, 25, SPECIES_MANTYKE},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute105SummerWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_FINIZEN},
    {15, 25, SPECIES_ALOMOMOLA},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute105AutumnWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_REMORAID},
    {15, 25, SPECIES_FRILLISH},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute105WinterWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_CHINCHOU},
    {15, 25, SPECIES_SPHEAL},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute106SpringWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_KRABBY},
    {15, 25, SPECIES_BINACLE},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute106SummerWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_CLAUNCHER},
    {15, 25, SPECIES_CORSOLA},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute106AutumnWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_SKRELP},
    {15, 25, SPECIES_MAREANIE},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute106WinterWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_SHELLDER},
    {15, 25, SPECIES_PINCURCHIN},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute107SpringWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_BUIZEL},
    {15, 25, SPECIES_WISHIWASHI},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute107SummerWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_ARROKUDA},
    {15, 25, SPECIES_BRUXISH},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute107AutumnWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_BASCULIN},
    {15, 25, SPECIES_INKAY},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute107WinterWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_SEEL},
    {15, 25, SPECIES_QWILFISH},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute108SpringWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_HORSEA},
    {15, 25, SPECIES_SHELLOS},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute108SummerWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_WIGLETT},
    {15, 25, SPECIES_PYUKUMUKU},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute108AutumnWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_CORPHISH},
    {15, 25, SPECIES_CLAMPERL},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute108WinterWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_SLOWPOKE},
    {15, 25, SPECIES_RELICANTH},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute109SpringWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_STARYU},
    {15, 25, SPECIES_DEWPIDER},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute109SummerWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_LUVDISC},
    {15, 25, SPECIES_CHEWTLE},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute109AutumnWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_CRAMORANT},
    {15, 25, SPECIES_VELUZA},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct WildPokemon sRoute109WinterWaterMons[NUM_WATER_MONS_ENCOUNTER_SLOTS] =
{
    {5, 35, SPECIES_TENTACOOL},
    {10, 30, SPECIES_SEALEO},
    {15, 25, SPECIES_EISCUE},
    {25, 30, SPECIES_WINGULL},
    {25, 30, SPECIES_PELIPPER},
};

static const struct LegendsSeasonalWaterTable sLegendsSeasonalWater[] =
{
    {MAP_ROUTE105, {
        [LEGENDS_SPRING] = {4, sRoute105SpringWaterMons},
        [LEGENDS_SUMMER] = {4, sRoute105SummerWaterMons},
        [LEGENDS_AUTUMN] = {4, sRoute105AutumnWaterMons},
        [LEGENDS_WINTER] = {4, sRoute105WinterWaterMons},
    }},
    {MAP_ROUTE106, {
        [LEGENDS_SPRING] = {4, sRoute106SpringWaterMons},
        [LEGENDS_SUMMER] = {4, sRoute106SummerWaterMons},
        [LEGENDS_AUTUMN] = {4, sRoute106AutumnWaterMons},
        [LEGENDS_WINTER] = {4, sRoute106WinterWaterMons},
    }},
    {MAP_ROUTE107, {
        [LEGENDS_SPRING] = {4, sRoute107SpringWaterMons},
        [LEGENDS_SUMMER] = {4, sRoute107SummerWaterMons},
        [LEGENDS_AUTUMN] = {4, sRoute107AutumnWaterMons},
        [LEGENDS_WINTER] = {4, sRoute107WinterWaterMons},
    }},
    {MAP_ROUTE108, {
        [LEGENDS_SPRING] = {4, sRoute108SpringWaterMons},
        [LEGENDS_SUMMER] = {4, sRoute108SummerWaterMons},
        [LEGENDS_AUTUMN] = {4, sRoute108AutumnWaterMons},
        [LEGENDS_WINTER] = {4, sRoute108WinterWaterMons},
    }},
    {MAP_ROUTE109, {
        [LEGENDS_SPRING] = {4, sRoute109SpringWaterMons},
        [LEGENDS_SUMMER] = {4, sRoute109SummerWaterMons},
        [LEGENDS_AUTUMN] = {4, sRoute109AutumnWaterMons},
        [LEGENDS_WINTER] = {4, sRoute109WinterWaterMons},
    }},
};
