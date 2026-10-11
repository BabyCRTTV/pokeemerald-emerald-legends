#define LOCALID_LEGENDS_KANTO_ZAPDOS 1

@ Wing Survey chapter three: The Quiet Current.
@ Observations advance the story. Zapdos capture is optional and never required.

LegendsKanto_Chapter3_Journal::
	goto_if_unset FLAG_LEGENDS_KANTO_SURVEY_FIELD_REPORT, LegendsKanto_Chapter3_Locked
	goto_if_set FLAG_LEGENDS_KANTO_SURVEY_POWER_REPORT, LegendsKanto_Chapter3_Filed
	msgbox LegendsKanto_Chapter3_Text_Journal, MSGBOX_DEFAULT
	goto_if_set FLAG_LEGENDS_KANTO_WEST_RELAY, LegendsKanto_Chapter3_CheckEast
	msgbox LegendsKanto_Chapter3_Text_NeedWest, MSGBOX_DEFAULT
LegendsKanto_Chapter3_CheckEast::
	goto_if_set FLAG_LEGENDS_KANTO_EAST_RELAY, LegendsKanto_Chapter3_CheckBird
	msgbox LegendsKanto_Chapter3_Text_NeedEast, MSGBOX_DEFAULT
LegendsKanto_Chapter3_CheckBird::
	goto_if_unset FLAG_LEGENDS_KANTO_WEST_RELAY, LegendsKanto_Chapter3_Return
	goto_if_unset FLAG_LEGENDS_KANTO_EAST_RELAY, LegendsKanto_Chapter3_Return
	goto_if_set FLAG_LEGENDS_KANTO_ZAPDOS_SEEN, LegendsKanto_Chapter3_Report
	msgbox LegendsKanto_Chapter3_Text_NeedBird, MSGBOX_DEFAULT
	goto LegendsKanto_Chapter3_Return
LegendsKanto_Chapter3_Report::
	msgbox LegendsKanto_Chapter3_Text_Report, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_KANTO_SURVEY_POWER_REPORT
LegendsKanto_Chapter3_Filed::
	msgbox LegendsKanto_Chapter3_Text_Next, MSGBOX_DEFAULT
LegendsKanto_Chapter3_Return::
	releaseall
	end

LegendsKanto_Chapter3_Locked::
	msgbox LegendsKanto_Chapter3_Text_Locked, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Chapter3_WestRelay::
	lockall
	goto_if_unset FLAG_LEGENDS_KANTO_SURVEY_FIELD_REPORT, LegendsKanto_Chapter3_Locked
	goto_if_set FLAG_LEGENDS_KANTO_WEST_RELAY, LegendsKanto_Chapter3_WestDone
	msgbox LegendsKanto_Chapter3_Text_WestOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	msgbox LegendsKanto_Chapter3_Text_WestScene, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_KANTO_WEST_RELAY
LegendsKanto_Chapter3_WestDone::
	msgbox LegendsKanto_Chapter3_Text_WestDone, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Chapter3_EastRelay::
	lockall
	goto_if_unset FLAG_LEGENDS_KANTO_SURVEY_FIELD_REPORT, LegendsKanto_Chapter3_Locked
	goto_if_set FLAG_LEGENDS_KANTO_EAST_RELAY, LegendsKanto_Chapter3_EastDone
	msgbox LegendsKanto_Chapter3_Text_EastOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	msgbox LegendsKanto_Chapter3_Text_EastScene, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_KANTO_EAST_RELAY
LegendsKanto_Chapter3_EastDone::
	msgbox LegendsKanto_Chapter3_Text_EastDone, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Chapter3_Zapdos::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_KANTO_SURVEY_FIELD_REPORT, LegendsKanto_Chapter3_Locked
	goto_if_unset FLAG_LEGENDS_KANTO_WEST_RELAY, LegendsKanto_Chapter3_RoostUnsafe
	goto_if_unset FLAG_LEGENDS_KANTO_EAST_RELAY, LegendsKanto_Chapter3_RoostUnsafe
	goto_if_set FLAG_LEGENDS_KANTO_ZAPDOS_CAUGHT, LegendsKanto_Chapter3_Return
	goto_if_set FLAG_LEGENDS_KANTO_ZAPDOS_SEEN, LegendsKanto_Chapter3_Challenge
	playmoncry SPECIES_ZAPDOS, CRY_MODE_NORMAL
	waitmoncry
	msgbox LegendsKanto_Chapter3_Text_Observe, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_KANTO_ZAPDOS_SEEN
LegendsKanto_Chapter3_Challenge::
	msgbox LegendsKanto_Chapter3_Text_Challenge, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Chapter3_LeaveBird
	closemessage
	waitse
	playmoncry SPECIES_ZAPDOS, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_ZAPDOS, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, LegendsKanto_Chapter3_Caught
	removeobject LOCALID_LEGENDS_KANTO_ZAPDOS
	msgbox LegendsKanto_Chapter3_Text_Rest, MSGBOX_DEFAULT
	releaseall
	end
LegendsKanto_Chapter3_Caught::
	setflag FLAG_LEGENDS_KANTO_ZAPDOS_CAUGHT
	removeobject LOCALID_LEGENDS_KANTO_ZAPDOS
	msgbox LegendsKanto_Chapter3_Text_Caught, MSGBOX_DEFAULT
	releaseall
	end
LegendsKanto_Chapter3_LeaveBird::
	msgbox LegendsKanto_Chapter3_Text_LeaveBird, MSGBOX_DEFAULT
	releaseall
	end
LegendsKanto_Chapter3_RoostUnsafe::
	msgbox LegendsKanto_Chapter3_Text_Unsafe, MSGBOX_DEFAULT
	releaseall
	end

@ Native legendary return reconstructs field objects before continuing the script.
LegendsKanto_Chapter3_OnResume::
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, LegendsKanto_Chapter3_CheckCatch
	end
LegendsKanto_Chapter3_CheckCatch::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	setflag FLAG_LEGENDS_KANTO_ZAPDOS_CAUGHT
	removeobject LOCALID_LEGENDS_KANTO_ZAPDOS
	return

LegendsKanto_Chapter3_TunnelGuide::
	msgbox LegendsKanto_Chapter3_Text_TunnelGuide, MSGBOX_NPC
	end
LegendsKanto_Chapter3_RiverGuide::
	msgbox LegendsKanto_Chapter3_Text_RiverGuide, MSGBOX_NPC
	end
LegendsKanto_Chapter3_CaveGuide::
	msgbox LegendsKanto_Chapter3_Text_CaveGuide, MSGBOX_NPC
	end
LegendsKanto_Chapter3_PlantGuide::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_KANTO_SURVEY_FIELD_REPORT, LegendsKanto_Chapter3_Locked
	msgbox LegendsKanto_Chapter3_Text_PlantGuide, MSGBOX_DEFAULT
	releaseall
	end
LegendsKanto_Chapter3_TunnelSign::
	msgbox LegendsKanto_Chapter3_Text_TunnelSign, MSGBOX_SIGN
	end
LegendsKanto_Chapter3_PlantSign::
	msgbox LegendsKanto_Chapter3_Text_PlantSign, MSGBOX_SIGN
	end
LegendsKanto_Chapter3_RoadClosed::
	msgbox LegendsKanto_Chapter3_Text_RoadClosed, MSGBOX_SIGN
	end

LegendsKanto_Chapter3_Text_Journal:
	.string "WING SURVEY: Quiet Current.\n"
	.string "The northern road is open.\p"
	.string "Go north from LAVENDER,\n"
	.string "through ROCK TUNNEL.\p"
	.string "Past the north POKEMON CENTER,\n"
	.string "SURF down the east river\p"
	.string "to the POWER PLANT.\n"
	.string "Our technician is inside.$"
LegendsKanto_Chapter3_Text_NeedWest:
	.string "West feed: Still active.\n"
	.string "Check the left-wall terminal\p"
	.string "in the first room north\n"
	.string "of the POWER PLANT entrance.$"
LegendsKanto_Chapter3_Text_NeedEast:
	.string "East feed: Still active.\n"
	.string "Check the center terminal\p"
	.string "on the long southern wall,\n"
	.string "beyond the entrance corridor.$"
LegendsKanto_Chapter3_Text_NeedBird:
	.string "Both feeds are safe.\n"
	.string "Follow the winding halls\p"
	.string "to the northwest roost.\n"
	.string "Observe the bird quietly.$"
LegendsKanto_Chapter3_Text_Locked:
	.string "File the Borrowed Voice\n"
	.string "report before the site survey.\p"
	.string "OAK's aide is in the\n"
	.string "VERMILION FAN CLUB.$"
LegendsKanto_Chapter3_Text_WestOffer:
	.string "WEST FEED: A cracked cable\n"
	.string "still carries a small charge.\p"
	.string "Isolate this unused feed?$"
LegendsKanto_Chapter3_Text_WestScene:
	.string "You switch the old feed off\n"
	.string "and record the meter reading.\p"
	.string "The cable falls quiet, but\n"
	.string "a steady pulse remains nearby.\p"
	.string "Something is storing charge.\n"
	.string "The storm is not the whole story.$"
LegendsKanto_Chapter3_Text_WestDone:
	.string "WEST FEED: Safely isolated.\n"
	.string "Its reading is in your notes.$"
LegendsKanto_Chapter3_Text_EastOffer:
	.string "EAST FEED: Old contacts hum\n"
	.string "beneath a layer of dust.\p"
	.string "Isolate this unused feed?$"
LegendsKanto_Chapter3_Text_EastScene:
	.string "You turn off the unused feed.\n"
	.string "The meter slowly settles.\p"
	.string "Tiny prints cross the dust.\n"
	.string "They are too small for the bird.\p"
	.string "A copied call echoes once.\n"
	.string "You record it without guessing.$"
LegendsKanto_Chapter3_Text_EastDone:
	.string "EAST FEED: Safely isolated.\n"
	.string "The small prints remain intact.$"
LegendsKanto_Chapter3_Text_Unsafe:
	.string "A huge bird watches you.\n"
	.string "Loose contacts crackle nearby.\p"
	.string "Make both old feeds safe\n"
	.string "before approaching its roost.$"
LegendsKanto_Chapter3_Text_Observe:
	.string "The bird spreads golden wings.\n"
	.string "Electric light crosses its crest.\p"
	.string "ZAPDOS! The pulse follows\n"
	.string "its breathing, even in calm air.\p"
	.string "It is guarding an old roost,\n"
	.string "not attacking the town.\p"
	.string "You record the observation.\n"
	.string "OAK needs notes, not a capture.$"
LegendsKanto_Chapter3_Text_Challenge:
	.string "Challenge ZAPDOS at Lv. 50?\n"
	.string "You may leave it undisturbed.\p"
	.string "Its level is the same for\n"
	.string "both GYM difficulty choices.$"
LegendsKanto_Chapter3_Text_LeaveBird:
	.string "You leave ZAPDOS at its roost.\n"
	.string "Your survey is still complete.\p"
	.string "Return to OAK's field aide\n"
	.string "in the VERMILION FAN CLUB.$"
LegendsKanto_Chapter3_Text_Rest:
	.string "ZAPDOS flies above the plant.\n"
	.string "It returns on your next visit.\p"
	.string "Your notes remain complete.\n"
	.string "Return to OAK's field aide.$"
LegendsKanto_Chapter3_Text_Caught:
	.string "ZAPDOS joined your collection.\n"
	.string "The observation is recorded.\p"
	.string "Return to OAK's field aide\n"
	.string "in the VERMILION FAN CLUB.$"
LegendsKanto_Chapter3_Text_Report:
	.string "FIELD AIDE: A confirmed ZAPDOS\n"
	.string "roost, and safe equipment!\p"
	.string "The old contacts carried\n"
	.string "the bird's charge into the meter.\p"
	.string "BIRCH's HOENN records do not\n"
	.string "show the same pattern.\p"
	.string "These are local habitat clues,\n"
	.string "not another weather crisis.\p"
	.string "The smaller prints and copied\n"
	.string "call remain a separate mystery.\p"
	.string "OAK will compare them with\n"
	.string "the notes from ROUTES 8 and 16.$"
LegendsKanto_Chapter3_Text_Next:
	.string "Quiet Current report: Filed.\n"
	.string "Next lead: SEAFOAM's cold water.\p"
	.string "KOGA will help plan that survey.\n"
	.string "The island journey opens later.\p"
	.string "Four visiting GYMS are ready.\n"
	.string "The other four are still ahead.$"
LegendsKanto_Chapter3_Text_TunnelGuide:
	.string "The north road is open again!\n"
	.string "ROCK TUNNEL links both halves.\p"
	.string "Use FIELD's FLASH in the cave.\n"
	.string "No POKEMON needs the move.\p"
	.string "For the POWER PLANT survey,\n"
	.string "first file OAK's field report.$"
LegendsKanto_Chapter3_Text_RiverGuide:
	.string "Follow the bank east from\n"
	.string "the POKEMON CENTER.\p"
	.string "SURF downriver to the plant.\n"
	.string "That small west path returns\p"
	.string "from the roost's side exit.\n"
	.string "The main door works both ways.$"
LegendsKanto_Chapter3_Text_CaveGuide:
	.string "The ladders join two floors.\n"
	.string "FLASH makes the path clearer.\p"
	.string "The north exit leads to a\n"
	.string "POKEMON CENTER and the river.$"
LegendsKanto_Chapter3_Text_PlantGuide:
	.string "SURGE asked us to make the\n"
	.string "old feeds safe, not restart them.\p"
	.string "West terminal: Left wall,\n"
	.string "first room north of this door.\p"
	.string "East terminal: Center of the\n"
	.string "long wall along the south side.\p"
	.string "Inspect them in either order.\n"
	.string "Keep clear of the roost until\p"
	.string "both are isolated. ZAPDOS is\n"
	.string "a Lv. 50 optional encounter.\p"
	.string "You can finish the survey\n"
	.string "without catching or fighting it.$"
LegendsKanto_Chapter3_Text_TunnelSign:
	.string "ROCK TUNNEL\n"
	.string "Two floors. Bring a light.$"
LegendsKanto_Chapter3_Text_PlantSign:
	.string "POWER PLANT\n"
	.string "WING SURVEY research site.$"
LegendsKanto_Chapter3_Text_RoadClosed:
	.string "ROUTE 9 roadworks\n"
	.string "CERULEAN access opens later.$"
