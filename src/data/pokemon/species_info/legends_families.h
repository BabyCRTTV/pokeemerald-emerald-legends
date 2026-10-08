// Original Leafhopper Pokémon for Pokémon Emerald: Legends. No evolution.
    [SPECIES_DA_BUG] =
    {
        .baseHP = 65,
        .baseAttack = 70,
        .baseDefense = 75,
        .baseSpeed = 85,
        .baseSpAttack = 80,
        .baseSpDefense = 75,
        .types = MON_TYPES(TYPE_BUG, TYPE_GRASS),
        .catchRate = 45,
        .expYield = 165,
        .evYield_Speed = 1,
        .genderRatio = PERCENT_FEMALE(50),
        .eggCycles = 20,
        .friendship = STANDARD_FRIENDSHIP,
        .growthRate = GROWTH_MEDIUM_FAST,
        .eggGroups = MON_EGG_GROUPS(EGG_GROUP_BUG),
        .abilities = { ABILITY_SWARM, ABILITY_LEAF_GUARD, ABILITY_CHLOROPHYLL },
        .bodyColor = BODY_COLOR_GREEN,
        .speciesName = _("Da Bug"),
        .cryId = CRY_DA_BUG,
        .natDexNum = NATIONAL_DEX_DA_BUG,
        .categoryName = _("Leafhopper"),
        .height = 3,
        .weight = 12,
        .description = COMPOUND_STRING(
            "It sways in the breeze to mimic\n"
            "a fallen leaf. If its disguise\n"
            "fails, it flashes its red eyes\n"
            "and springs away."),
        .pokemonScale = 566,
        .pokemonOffset = 18,
        .trainerScale = 256,
        .trainerOffset = 0,
        .frontPic = gMonFrontPic_DaBug,
        .frontPicSize = MON_COORDS_SIZE(48, 40),
        .frontPicYOffset = 16,
        .frontAnimFrames = ANIM_FRAMES(
            ANIMCMD_FRAME(0, 12),
            ANIMCMD_FRAME(1, 8),
            ANIMCMD_FRAME(0, 8),
            ANIMCMD_FRAME(1, 8),
            ANIMCMD_FRAME(0, 12),
        ),
        .frontAnimId = ANIM_ROTATE_TO_SIDES,
        .backPic = gMonBackPic_DaBug,
        .backPicSize = MON_COORDS_SIZE(64, 56),
        .backPicYOffset = 16,
        .backAnimId = BACK_ANIM_LEGENDS_DA_BUG,
        .palette = gMonPalette_DaBug,
        .shinyPalette = gMonShinyPalette_DaBug,
        .iconSprite = gMonIcon_DaBug,
        .iconPalIndex = 1,
        .pokemonJumpType = PKMN_JUMP_TYPE_NORMAL,
        SHADOW(0, 0, SHADOW_SIZE_S)
        FOOTPRINT(DaBug)
        OVERWORLD(
            sPicTable_DaBug, SIZE_32x32, SHADOW_SIZE_S, TRACKS_FOOT,
            sAnimTable_Following, gOverworldPalette_DaBug, gShinyOverworldPalette_DaBug
        )
        .levelUpLearnset = sDaBugLevelUpLearnset,
        .teachableLearnset = sNoneTeachableLearnset,
        .eggMoveLearnset = sNoneEggMoveLearnset,
    },
