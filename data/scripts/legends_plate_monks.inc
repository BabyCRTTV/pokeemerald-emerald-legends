@ Each gift becomes permanent only after the normal Bag handoff succeeds.
    .macro plate_monk name, item, flag
    .global PlateMonk_\name
PlateMonk_\name:
    lock
    faceplayer
    goto_if_set \flag, PlateMonk_Revisit
    msgbox PlateTeaching_\name, MSGBOX_DEFAULT
    giveitem \item
    goto_if_eq VAR_RESULT, FALSE, PlateMonk_NoRoom
    setflag \flag
    setflag FLAG_PLATE_PILGRIMAGE_STARTED
    call PlateMonk_Count
    goto_if_ne VAR_RESULT, 19, PlateMonk_ShowCount
    setflag FLAG_ALL_MONK_PLATES
    msgbox PlateMonk_Text_ReturnHome, MSGBOX_DEFAULT
    release
    end
    .endm

    plate_monk Blank, ITEM_BLANK_PLATE, FLAG_MONK_BLANK_PLATE
    plate_monk Meadow, ITEM_MEADOW_PLATE, FLAG_MONK_MEADOW_PLATE
    plate_monk Insect, ITEM_INSECT_PLATE, FLAG_MONK_INSECT_PLATE
    plate_monk Fist, ITEM_FIST_PLATE, FLAG_MONK_FIST_PLATE
    plate_monk Stone, ITEM_STONE_PLATE, FLAG_MONK_STONE_PLATE
    plate_monk Iron, ITEM_IRON_PLATE, FLAG_MONK_IRON_PLATE
    plate_monk Splash, ITEM_SPLASH_PLATE, FLAG_MONK_SPLASH_PLATE
    plate_monk Zap, ITEM_ZAP_PLATE, FLAG_MONK_ZAP_PLATE
    plate_monk Flame, ITEM_FLAME_PLATE, FLAG_MONK_FLAME_PLATE
    plate_monk Earth, ITEM_EARTH_PLATE, FLAG_MONK_EARTH_PLATE
    plate_monk Toxic, ITEM_TOXIC_PLATE, FLAG_MONK_TOXIC_PLATE
    plate_monk Sky, ITEM_SKY_PLATE, FLAG_MONK_SKY_PLATE
    plate_monk Mind, ITEM_MIND_PLATE, FLAG_MONK_MIND_PLATE
    plate_monk Spooky, ITEM_SPOOKY_PLATE, FLAG_MONK_SPOOKY_PLATE
    plate_monk Dread, ITEM_DREAD_PLATE, FLAG_MONK_DREAD_PLATE
    plate_monk Icicle, ITEM_ICICLE_PLATE, FLAG_MONK_ICICLE_PLATE
    plate_monk Draco, ITEM_DRACO_PLATE, FLAG_MONK_DRACO_PLATE
    plate_monk Pixie, ITEM_PIXIE_PLATE, FLAG_MONK_PIXIE_PLATE
    plate_monk Legend, ITEM_LEGEND_PLATE, FLAG_MONK_LEGEND_PLATE

PlateMonk_Count:
    specialvar VAR_RESULT, CountMonkPlates
    buffernumberstring STR_VAR_1, VAR_RESULT
    return

PlateMonk_Revisit:
    goto_if_set FLAG_RECEIVED_AZURE_FLUTE, PlateMonk_Farewell
    goto_if_set FLAG_ALL_MONK_PLATES, PlateMonk_HomeHint
    call PlateMonk_Count
PlateMonk_ShowCount:
    msgbox PlateMonk_Text_Count, MSGBOX_DEFAULT
    release
    end

PlateMonk_NoRoom:
    msgbox PlateMonk_Text_NoRoom, MSGBOX_DEFAULT
    release
    end

PlateMonk_HomeHint:
    msgbox PlateMonk_Text_ReturnHome, MSGBOX_DEFAULT
    release
    end

PlateMonk_Elder::
    lock
    faceplayer
    goto_if_unset FLAG_ALL_MONK_PLATES, PlateMonk_Leave
    goto_if_set FLAG_RECEIVED_AZURE_FLUTE, PlateMonk_Farewell
    msgbox PlateMonk_Text_Flute, MSGBOX_DEFAULT
    giveitem ITEM_AZURE_FLUTE
    goto_if_eq VAR_RESULT, FALSE, PlateMonk_NoRoom
    setflag FLAG_RECEIVED_AZURE_FLUTE
PlateMonk_Farewell:
    msgbox PlateMonk_Text_Farewell, MSGBOX_DEFAULT
PlateMonk_Leave:
    release
    end

PlateTeaching_Blank:
    .string "Before a name is carved,\n"
    .string "the stone can be anything.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Blank Plate.$"

PlateTeaching_Meadow:
    .string "Even the smallest root can\n"
    .string "split a stone in its own time.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Meadow Plate.$"

PlateTeaching_Insect:
    .string "Hold still. Hear that hum?\n"
    .string "The whole wood is singing.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Insect Plate.$"

PlateTeaching_Fist:
    .string "An open hand can give what\n"
    .string "a closed fist cannot.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Fist Plate.$"

PlateTeaching_Stone:
    .string "This stone has outlasted\n"
    .string "every footstep in this cave.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Stone Plate.$"

PlateTeaching_Iron:
    .string "Two towns once dug toward each\n"
    .string "other. Iron joined their hands.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Iron Plate.$"

PlateTeaching_Splash:
    .string "They put the sea under glass.\n"
    .string "Still, you can hear the tide.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Splash Plate.$"

PlateTeaching_Zap:
    .string "Long after the lamps go dark,\n"
    .string "a spark sleeps in the stone.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Zap Plate.$"

PlateTeaching_Flame:
    .string "The mountain breathes out heat.\n"
    .string "This stone remembers the fire.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Flame Plate.$"

PlateTeaching_Earth:
    .string "Ash falls on these fields.\n"
    .string "In spring, the earth gives back.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Earth Plate.$"

PlateTeaching_Toxic:
    .string "One petal heals. Another stings.\n"
    .string "Both grow beside this path.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Toxic Plate.$"

PlateTeaching_Sky:
    .string "The wind needs no branches,\n"
    .string "yet it visits every tree.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Sky Plate.$"

PlateTeaching_Mind:
    .string "Before the telescope turns,\n"
    .string "someone must dream of a star.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Mind Plate.$"

PlateTeaching_Spooky:
    .string "Leave a space in the silence\n"
    .string "for the ones we remember.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Spooky Plate.$"

PlateTeaching_Dread:
    .string "Courage came through here once.\n"
    .string "I knew it by its shaking hands.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Dread Plate.$"

PlateTeaching_Icicle:
    .string "Step softly. Even sleeping ice\n"
    .string "speaks when it begins to thaw.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Icicle Plate.$"

PlateTeaching_Draco:
    .string "Look up where the water falls.\n"
    .string "Dragons once drank the stars.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Draco Plate.$"

PlateTeaching_Pixie:
    .string "A town grew inside a crater.\n"
    .string "Wonder takes root in odd places.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Pixie Plate.$"

PlateTeaching_Legend:
    .string "Some climb for a crown.\n"
    .string "You stopped to hear an old monk.\p"
    .string "Chosen one, I entrust you with"
    .string "\nthe Legend Plate.$"

PlateMonk_Text_Count:
    .string "{STR_VAR_1} of our 19 plates are yours.\p"
    .string "When all have been given, return\n"
    .string "to Littleroot, where you began.$"

PlateMonk_Text_ReturnHome:
    .string "All 19 plates, chosen one.\p"
    .string "Our elder awaits in Littleroot,\n"
    .string "beside the Pokémon Lab.$"

PlateMonk_Text_NoRoom:
    .string "Your Bag is full, chosen one.\n"
    .string "Make room. Your gift can wait.$"

PlateMonk_Text_Flute:
    .string "The others sent word, chosen one.\n"
    .string "You listened to all nineteen.\p"
    .string "I have carried this Azure Flute\n"
    .string "a long way. Now it is yours.$"

PlateMonk_Text_Farewell:
    .string "May the road home always be\n"
    .string "familiar to you, chosen one.$"


EventScript_AzureFlute::
    lockall
    playse SE_GLASS_FLUTE
    waitse
    msgbox PlateMonk_Text_FluteNote, MSGBOX_DEFAULT
    releaseall
    end

PlateMonk_Text_FluteNote:
    .string "A clear note rises, then fades\n"
    .string "into the distance.$"
