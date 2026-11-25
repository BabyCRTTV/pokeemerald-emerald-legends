LegendsJohto_Route22_MapScripts::
LegendsJohto_IndigoGate_MapScripts::
LegendsJohto_Route26_MapScripts::
LegendsJohto_Route27East_MapScripts::
LegendsJohto_TohjoFalls_MapScripts::
LegendsJohto_Route27West_MapScripts::
LegendsJohto_Route29_MapScripts::
LegendsJohto_Route30_MapScripts::
LegendsJohto_Route31_MapScripts::
LegendsJohto_ElmsLab_MapScripts::
LegendsJohto_WindkeepersHouse_MapScripts::
LegendsJohto_GardenHouse_MapScripts::
LegendsJohto_GuidesHouse_MapScripts::
LegendsJohto_HarborHouse_MapScripts::
LegendsJohto_Academy_MapScripts::
LegendsJohto_KilnHouse_MapScripts::
LegendsJohto_SproutTower_MapScripts::
LegendsJohto_CherrygroveMart_MapScripts::
LegendsJohto_VioletMart_MapScripts::
LegendsJohto_VioletGym_MapScripts::
LegendsJohto_Route32_MapScripts::
LegendsJohto_UnionCave_MapScripts::
LegendsJohto_Route33_MapScripts::
LegendsJohto_SlowpokeWell_MapScripts::
LegendsJohto_AzaleaGym_MapScripts::
LegendsJohto_ApricornWorkshop_MapScripts::
LegendsJohto_AzaleaMart_MapScripts::
LegendsJohto_SproutTowerBelfry_MapScripts::
	.byte 0

LegendsJohto_NewBarkTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LegendsJohto_NewBarkTown_Arrival
	.byte 0
LegendsJohto_NewBarkTown_Arrival:
	setflag FLAG_VISITED_LEGENDS_NEW_BARK_TOWN
	end

LegendsJohto_CherrygroveCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LegendsJohto_CherrygroveCity_Arrival
	.byte 0
LegendsJohto_CherrygroveCity_Arrival:
	setflag FLAG_VISITED_LEGENDS_CHERRYGROVE_CITY
	end

LegendsJohto_VioletCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LegendsJohto_VioletCity_Arrival
	.byte 0
LegendsJohto_VioletCity_Arrival:
	setflag FLAG_VISITED_LEGENDS_VIOLET_CITY
	end

LegendsJohto_CherrygroveCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LegendsJohto_CherrygroveCenter_Arrival
	.byte 0
LegendsJohto_CherrygroveCenter_Arrival:
	setrespawn HEAL_LOCATION_LEGENDS_CHERRYGROVE_CITY
	end

LegendsJohto_VioletCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LegendsJohto_VioletCenter_Arrival
	.byte 0
LegendsJohto_VioletCenter_Arrival:
	setrespawn HEAL_LOCATION_LEGENDS_VIOLET_CITY
	end

LegendsJohto_AzaleaTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LegendsJohto_AzaleaTown_Arrival
	.byte 0
LegendsJohto_AzaleaTown_Arrival:
	setflag FLAG_VISITED_LEGENDS_AZALEA_TOWN
	end

LegendsJohto_AzaleaCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LegendsJohto_AzaleaCenter_Arrival
	.byte 0
LegendsJohto_AzaleaCenter_Arrival:
	setrespawn HEAL_LOCATION_LEGENDS_AZALEA_TOWN
	end

LegendsJohto_Route32Center_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LegendsJohto_Route32Center_Arrival
	.byte 0
LegendsJohto_Route32Center_Arrival:
	setrespawn HEAL_LOCATION_LEGENDS_ROUTE32
	end

Johto_Apricorn::
	msgbox Johto_Text_Apricorn, MSGBOX_NPC
	end

Johto_AzaleaSign::
	msgbox Johto_Text_AzaleaSign, MSGBOX_SIGN
	end

Johto_Belfry::
	msgbox Johto_Text_Belfry, MSGBOX_NPC
	end

Johto_Bells::
	msgbox Johto_Text_Bells, MSGBOX_NPC
	end

Johto_CaveSign::
	msgbox Johto_Text_CaveSign, MSGBOX_SIGN
	end

Johto_CherrySign::
	msgbox Johto_Text_CherrySign, MSGBOX_SIGN
	end

Johto_EastMouth::
	msgbox Johto_Text_EastMouth, MSGBOX_SIGN
	end

Johto_Fisher::
	msgbox Johto_Text_Fisher, MSGBOX_NPC
	end

Johto_Forest::
	msgbox Johto_Text_Forest, MSGBOX_NPC
	end

Johto_Gardener::
	msgbox Johto_Text_Gardener, MSGBOX_NPC
	end

Johto_Gate::
	msgbox Johto_Text_Gate, MSGBOX_NPC
	end

Johto_Guide::
	msgbox Johto_Text_Guide, MSGBOX_NPC
	end

Johto_GuideHouse::
	msgbox Johto_Text_GuideHouse, MSGBOX_NPC
	end

Johto_GymGuide::
	msgbox Johto_Text_GymGuide, MSGBOX_NPC
	end

Johto_Harbor::
	msgbox Johto_Text_Harbor, MSGBOX_NPC
	end

Johto_HiveSign::
	msgbox Johto_Text_HiveSign, MSGBOX_SIGN
	end

Johto_Kiln::
	msgbox Johto_Text_Kiln, MSGBOX_NPC
	end

Johto_LabSign::
	msgbox Johto_Text_LabSign, MSGBOX_SIGN
	end

Johto_Meadow::
	msgbox Johto_Text_Meadow, MSGBOX_NPC
	end

Johto_NewSign::
	msgbox Johto_Text_NewSign, MSGBOX_SIGN
	end

Johto_Orchard::
	msgbox Johto_Text_Orchard, MSGBOX_NPC
	end

Johto_Pond::
	msgbox Johto_Text_Pond, MSGBOX_NPC
	end

Johto_Rain::
	msgbox Johto_Text_Rain, MSGBOX_NPC
	end

Johto_River::
	msgbox Johto_Text_River, MSGBOX_NPC
	end

Johto_Sign29::
	msgbox Johto_Text_Sign29, MSGBOX_SIGN
	end

Johto_Sign30::
	msgbox Johto_Text_Sign30, MSGBOX_SIGN
	end

Johto_Sign31::
	msgbox Johto_Text_Sign31, MSGBOX_SIGN
	end

Johto_Sign32::
	msgbox Johto_Text_Sign32, MSGBOX_SIGN
	end

Johto_Sign33::
	msgbox Johto_Text_Sign33, MSGBOX_SIGN
	end

Johto_Teacher::
	msgbox Johto_Text_Teacher, MSGBOX_NPC
	end

Johto_TowerSign::
	msgbox Johto_Text_TowerSign, MSGBOX_SIGN
	end

Johto_Trail::
	msgbox Johto_Text_Trail, MSGBOX_SIGN
	end

Johto_Violet::
	msgbox Johto_Text_Violet, MSGBOX_NPC
	end

Johto_VioletSign::
	msgbox Johto_Text_VioletSign, MSGBOX_SIGN
	end

Johto_ViridianGuide::
	msgbox Johto_Text_ViridianGuide, MSGBOX_NPC
	end

Johto_Warden::
	msgbox Johto_Text_Warden, MSGBOX_NPC
	end

Johto_WellKeeper::
	msgbox Johto_Text_WellKeeper, MSGBOX_NPC
	end

Johto_WellSign::
	msgbox Johto_Text_WellSign, MSGBOX_SIGN
	end

Johto_WestMouth::
	msgbox Johto_Text_WestMouth, MSGBOX_SIGN
	end

Johto_Wind::
	msgbox Johto_Text_Wind, MSGBOX_NPC
	end

Johto_Windkeeper::
	msgbox Johto_Text_Windkeeper, MSGBOX_NPC
	end

Johto_Elm::
    lock
    faceplayer
    goto_if_set FLAG_JOHTO_SURVEY_RETURNED, Johto_ElmAfter
    goto_if_unset FLAG_JOHTO_ELM_SURVEY, Johto_Offer
    goto_if_unset FLAG_JOHTO_TIDE_READING, Johto_TideHint
    goto_if_unset FLAG_JOHTO_BELL_READING, Johto_BellHint
    msgbox Johto_Text_ElmDone, MSGBOX_DEFAULT
    setflag FLAG_JOHTO_SURVEY_RETURNED
    release
    end
Johto_Offer:
    msgbox Johto_Text_ElmIntro, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Johto_ElmNo
    setflag FLAG_JOHTO_ELM_SURVEY
    msgbox Johto_Text_ElmYes, MSGBOX_DEFAULT
    release
    end
Johto_ElmAfter:
	msgbox Johto_Text_ElmAfter, MSGBOX_DEFAULT
	release
	end
Johto_ElmNo:
	msgbox Johto_Text_ElmNo, MSGBOX_DEFAULT
	release
	end
Johto_TideHint:
	msgbox Johto_Text_TideHint, MSGBOX_DEFAULT
	release
	end
Johto_BellHint:
	msgbox Johto_Text_BellHint, MSGBOX_DEFAULT
	release
	end
Johto_TidePost::
	lockall
	goto_if_unset FLAG_JOHTO_ELM_SURVEY, Johto_TidePlain
	goto_if_set FLAG_JOHTO_TIDE_READING, Johto_TideAgain
	msgbox Johto_Text_TideRead, MSGBOX_DEFAULT
	setflag FLAG_JOHTO_TIDE_READING
	releaseall
	end
Johto_TidePlain:
	msgbox Johto_Text_TidePlain, MSGBOX_DEFAULT
	releaseall
	end
Johto_TideAgain:
	msgbox Johto_Text_TideAgain, MSGBOX_DEFAULT
	releaseall
	end
Johto_Keeper::
	lockall
	faceplayer
	goto_if_unset FLAG_JOHTO_ELM_SURVEY, Johto_BellPlain
	goto_if_set FLAG_JOHTO_BELL_READING, Johto_BellAgain
	msgbox Johto_Text_BellRead, MSGBOX_DEFAULT
	setflag FLAG_JOHTO_BELL_READING
	releaseall
	end
Johto_BellPlain:
	msgbox Johto_Text_BellPlain, MSGBOX_DEFAULT
	releaseall
	end
Johto_BellAgain:
	msgbox Johto_Text_BellAgain, MSGBOX_DEFAULT
	releaseall
	end
Johto_Wren::
	lockall
	faceplayer
	goto_if_set FLAG_JOHTO_ZEPHYR_BADGE, Johto_WrenAfter
	trainerbattle_single TRAINER_LEGENDS_JOHTO_WREN, Johto_Text_WrenIntro, Johto_Text_WrenDefeat
	setflag FLAG_JOHTO_ZEPHYR_BADGE
	playfanfare MUS_OBTAIN_BADGE
	msgbox Johto_Text_WrenWin, MSGBOX_DEFAULT
	waitfanfare
	releaseall
	end
Johto_WrenAfter:
	msgbox Johto_Text_WrenAfter, MSGBOX_DEFAULT
	releaseall
	end
Johto_Rue::
	lockall
	faceplayer
	goto_if_set FLAG_JOHTO_HIVE_BADGE, Johto_RueAfter
	goto_if_unset FLAG_JOHTO_ZEPHYR_BADGE, Johto_RueGate
	trainerbattle_single TRAINER_LEGENDS_JOHTO_RUE, Johto_Text_RueIntro, Johto_Text_RueDefeat
	setflag FLAG_JOHTO_HIVE_BADGE
	playfanfare MUS_OBTAIN_BADGE
	msgbox Johto_Text_RueWin, MSGBOX_DEFAULT
	waitfanfare
	releaseall
	end
Johto_RueAfter:
	msgbox Johto_Text_RueAfter, MSGBOX_DEFAULT
	releaseall
	end
Johto_RueGate:
	msgbox Johto_Text_RueGate, MSGBOX_DEFAULT
	releaseall
	end
Johto_Pidgeot::
	lock
	faceplayer
	playmoncry SPECIES_PIDGEOT, CRY_MODE_NORMAL
	waitmoncry
	msgbox Johto_Text_Pidgeot, MSGBOX_DEFAULT
	release
	end
Johto_Slowpoke::
	lock
	faceplayer
	playmoncry SPECIES_SLOWPOKE, CRY_MODE_NORMAL
	waitmoncry
	msgbox Johto_Text_Slowpoke, MSGBOX_DEFAULT
	release
	end
Johto_Nurse::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Johto_Text_ViridianGuide:
	.string "The west road leads to Route 22.\n"
	.string "Take the passage through the gate\l"
	.string "for Johto.$"

Johto_Text_Gate:
	.string "For Johto, follow Route 26 south\n"
	.string "after the gate. The lower path\l"
	.string "through Tohjo Falls is open in\l"
	.string "both directions.$"

Johto_Text_Trail:
	.string "BORDER FOOTPATH\p"
	.string "South to Tohjo Falls. North to\n"
	.string "Route 22 and Viridian.$"

Johto_Text_Warden:
	.string "I measure the river against that\n"
	.string "fence post after every storm. The\l"
	.string "footpath is dry today.$"

Johto_Text_EastMouth:
	.string "TOHJO FALLS\p"
	.string "Walk west along the lower shelf\n"
	.string "to reach New Bark Town.$"

Johto_Text_WestMouth:
	.string "ROUTE 27\p"
	.string "New Bark lies west. The caves\n"
	.string "lead back to Kanto.$"

Johto_Text_Fisher:
	.string "Some mornings my float drifts\n"
	.string "clear across the border. Nobody\l"
	.string "has asked it for papers yet.$"

Johto_Text_LabSign:
	.string "ELM POKéMON LAB\p"
	.string "Field observations and breeding\n"
	.string "records. Visitors welcome.$"

Johto_Text_NewSign:
	.string "NEW BARK TOWN\p"
	.string "East to Kanto. West to\n"
	.string "Cherrygrove.$"

Johto_Text_Wind:
	.string "Listen between the clicks of the\n"
	.string "wind vane. You can hear the sea\l"
	.string "from here.$"

Johto_Text_Windkeeper:
	.string "I keep a tin of spare washers for\n"
	.string "those vanes. Elm borrows one and\l"
	.string "brings back three.$"

Johto_Text_Gardener:
	.string "The gentlest afternoon wind is on\n"
	.string "this side of the lab. My flowers\l"
	.string "know it too.$"

Johto_Text_Sign29:
	.string "ROUTE 29\p"
	.string "Cherrygrove to the west. New Bark\n"
	.string "to the east.$"

Johto_Text_Meadow:
	.string "Ledyba bunch together at the edge\n"
	.string "of the trees before they take\l"
	.string "off.$"

Johto_Text_CherrySign:
	.string "CHERRYGROVE CITY\p"
	.string "The tide pier is southwest. Route\n"
	.string "30 leaves town to the north.$"

Johto_Text_Guide:
	.string "My knees retired from giving\n"
	.string "tours. My finger still works! The\l"
	.string "tide post is at the head of the\l"
	.string "pier.$"

Johto_Text_GuideHouse:
	.string "Our first town map was drawn on a\n"
	.string "napkin. I framed it before anyone\l"
	.string "could wipe jam on it.$"

Johto_Text_Harbor:
	.string "The pier piles each knock at a\n"
	.string "different pitch. Listen the next\l"
	.string "time the tide comes in.$"

Johto_Text_Sign30:
	.string "ROUTE 30\p"
	.string "North toward Violet. South to\n"
	.string "Cherrygrove.$"

Johto_Text_Pond:
	.string "You can tell a Poliwag from a\n"
	.string "raindrop. A Poliwag makes a\l"
	.string "second ring.$"

Johto_Text_Sign31:
	.string "ROUTE 31\p"
	.string "Violet City is west. Follow Route\n"
	.string "30 south for Cherrygrove.$"

Johto_Text_Bells:
	.string "On cold mornings, the low bell\n"
	.string "carries all the way to this pond.$"

Johto_Text_VioletSign:
	.string "VIOLET CITY\p"
	.string "Sprout Tower across the north\n"
	.string "bridge. Route 32 leaves town to\l"
	.string "the south.$"

Johto_Text_TowerSign:
	.string "SPROUT TOWER\p"
	.string "Cross quietly. The pillar carries\n"
	.string "every footfall.$"

Johto_Text_Violet:
	.string "I used to think somebody pulled\n"
	.string "the bells. The tower leans enough\l"
	.string "to ring them by itself.$"

Johto_Text_Teacher:
	.string "Draw the tower two days in a row\n"
	.string "and the roof will lean a\l"
	.string "different way on your page.$"

Johto_Text_Kiln:
	.string "Tap this clay bowl and it sings.\n"
	.string "Tap it twice and my neighbor\l"
	.string "comes over for lunch.$"

Johto_Text_Belfry:
	.string "The old bell has a thin spot\n"
	.string "where a thousand windy mornings\l"
	.string "struck it.$"

Johto_Text_GymGuide:
	.string "Rue lets her bugs hang their\n"
	.string "cocoons wherever they please.\l"
	.string "They like the far end of the\l"
	.string "hall.$"

Johto_Text_Sign32:
	.string "ROUTE 32\p"
	.string "Follow the river south. Union\n"
	.string "Cave is beyond the field station.$"

Johto_Text_CaveSign:
	.string "UNION CAVE\p"
	.string "Follow the dry ledges to the\n"
	.string "south mouth for Azalea. A Pokémon\l"
	.string "Center stands east of the trail.$"

Johto_Text_River:
	.string "The river planks are warm in the\n"
	.string "sun. Wooper like to hide in the\l"
	.string "shade beneath them.$"

Johto_Text_Sign33:
	.string "ROUTE 33\p"
	.string "West to Azalea Town. Union Cave\n"
	.string "leads north.$"

Johto_Text_Rain:
	.string "You can smell the wet bark a long\n"
	.string "way before you see the first\l"
	.string "house in Azalea.$"

Johto_Text_AzaleaSign:
	.string "AZALEA TOWN\p"
	.string "Apricorn workshop to the north.\n"
	.string "The Gym overlooks the southern\l"
	.string "orchard.$"

Johto_Text_WellSign:
	.string "SLOWPOKE WELL\p"
	.string "Walk down the well steps to the\n"
	.string "water table.$"

Johto_Text_HiveSign:
	.string "AZALEA GYM\p"
	.string "RUE, keeper of the Hive Badge.$"

Johto_Text_Orchard:
	.string "Leaving a few Apricorns on the\n"
	.string "high branches is a good way to\l"
	.string "invite the birds back.$"

Johto_Text_Forest:
	.string "Ilex Forest is beyond this grove.\n"
	.string "I walk the orchard rows to watch\l"
	.string "the cocoons open.$"

Johto_Text_Apricorn:
	.string "My grandfather cured green\n"
	.string "Apricorn shells over this kiln.\l"
	.string "If you rush the firing, the two\l"
	.string "halves never fit.$"

Johto_Text_WellKeeper:
	.string "The spring feeds the whole town.\n"
	.string "I scrub the steps while the\l"
	.string "Slowpoke supervise.$"

Johto_Text_Slowpoke:
	.string "SLOWPOKE blinks. A drop of water\n"
	.string "hangs from its nose.$"

Johto_Text_Pidgeot:
	.string "PIDGEOT stretches one wing. A\n"
	.string "loose feather skims across the\l"
	.string "floor.$"

Johto_Text_ElmIntro:
	.string "ELM: Come in! Mind the stacks. I\n"
	.string "set my glasses on a notebook and\l"
	.string "lost a whole afternoon.\p"
	.string "I used to chase the wind myself.\n"
	.string "Nowadays I send a second pair of\l"
	.string "eyes.\p"
	.string "Will you read the tide post at\n"
	.string "Cherrygrove pier and ask the\l"
	.string "Sprout Tower keeper about his\l"
	.string "bell?$"

Johto_Text_ElmYes:
	.string "ELM: Both readings, in any order.\n"
	.string "My notebooks can wait. The\l"
	.string "weather seldom does!$"

Johto_Text_ElmNo:
	.string "ELM: Another day, then. I should\n"
	.string "label that notebook before it\l"
	.string "vanishes again.$"

Johto_Text_TideHint:
	.string "ELM: Look beside the pier at\n"
	.string "Cherrygrove. Someone cut a notch\l"
	.string "in the post at the highest tide.$"

Johto_Text_BellHint:
	.string "ELM: The keeper is on the ground\n"
	.string "floor of Sprout Tower. The north\l"
	.string "bridge in Violet leads to him.$"

Johto_Text_ElmDone:
	.string "ELM: A rising tide, then a bell\n"
	.string "from the east. The wind arrived\l"
	.string "here just after your reading.\p"
	.string "Three towns and one gust! Your\n"
	.string "name belongs beside mine in this\l"
	.string "notebook.$"

Johto_Text_ElmAfter:
	.string "ELM: I found my glasses. They\n"
	.string "were marking the page with your\l"
	.string "readings.$"

Johto_Text_TidePlain:
	.string "Old notches climb the tide post.\n"
	.string "The newest is still wet.$"

Johto_Text_TideRead:
	.string "The tide is rising toward the\n"
	.string "third notch. You record the\l"
	.string "waterline for Elm.$"

Johto_Text_TideAgain:
	.string "Your mark is here, just below the\n"
	.string "third notch.$"

Johto_Text_BellPlain:
	.string "We never straighten the pillar.\n"
	.string "The give in the timber keeps our\l"
	.string "tower standing.$"

Johto_Text_BellRead:
	.string "The bell swung east at first\n"
	.string "light. Here, feel the rope. It\l"
	.string "still hums.\p"
	.string "You record the direction for Elm.$"

Johto_Text_BellAgain:
	.string "East at first light. That was a\n"
	.string "wind worth writing down.$"

Johto_Text_WrenIntro:
	.string "WREN: A good wing can read the\n"
	.string "current. Let me see how your team\l"
	.string "handles a change in the wind.$"

Johto_Text_WrenDefeat:
	.string "You waited for the wind to turn.\n"
	.string "Well flown!$"

Johto_Text_WrenWin:
	.string "WREN: The ZEPHYR BADGE is yours.\n"
	.string "Your Adventure Log carries the\l"
	.string "mark of Violet Gym.$"

Johto_Text_WrenAfter:
	.string "WREN: Follow Route 32 south.\n"
	.string "Azalea grows quiet when Rue takes\l"
	.string "her team out.$"

Johto_Text_RueGate:
	.string "RUE: Wren in Violet certifies\n"
	.string "visiting trainers first. Bring\l"
	.string "the Zephyr Badge for our official\l"
	.string "match.$"

Johto_Text_RueIntro:
	.string "RUE: The whole grove is\n"
	.string "listening. Let us give them a\l"
	.string "good match!$"

Johto_Text_RueDefeat:
	.string "You read my swarm perfectly.$"

Johto_Text_RueWin:
	.string "RUE: The HIVE BADGE is yours. Two\n"
	.string "Johto badges in your Adventure\l"
	.string "Log!$"

Johto_Text_RueAfter:
	.string "RUE: My Scyther taps the hive\n"
	.string "mark with one claw when he\l"
	.string "approves of a trainer. He tapped\l"
	.string "yours.$"
