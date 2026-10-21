@ Optional post-Regigigas voyage. Existing Briney routes/ship state remain native.
Wyrmtide_UnknownCall::
	lockall
	pokenavcall Wyrmtide_Text_Call
	waitmessage
	setflag FLAG_LEGENDS_WYRMTIDE_CALL
	special LegendsWyrmtideRefreshDewford
	releaseall
	end

@ Local visibility only: never rewrite Briney's original persistent travel flags.
Wyrmtide_PrepareDewford::
	setflag FLAG_TEMP_6
	setflag FLAG_TEMP_7
	goto_if_unset FLAG_LEGENDS_WYRMTIDE_CALL, Common_EventScript_NopReturn
	call_if_set FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN, Wyrmtide_ShowExpeditionBriney
	call_if_set FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN, Wyrmtide_ShowExpeditionBoat
	return
Wyrmtide_ShowExpeditionBriney::
	clearflag FLAG_TEMP_6
	return
Wyrmtide_ShowExpeditionBoat::
	clearflag FLAG_TEMP_7
	return
Wyrmtide_ExpeditionBriney::
	lock
	faceplayer
	msgbox Wyrmtide_Text_Departure, MSGBOX_DEFAULT
	multichoice 10, 5, MULTI_LEGENDS_WYRMTIDE_EXPEDITION, FALSE
	goto_if_eq VAR_RESULT, 0, Wyrmtide_Depart
	releaseall
	end
Wyrmtide_DewfordChoice::
	msgbox Wyrmtide_Text_Departure, MSGBOX_DEFAULT
	multichoice 10, 5, MULTI_LEGENDS_WYRMTIDE, FALSE
	goto_if_eq VAR_RESULT, 0, Wyrmtide_Depart
	goto_if_eq VAR_RESULT, 1, Wyrmtide_NormalRoutes
	releaseall
	end
Wyrmtide_NormalRoutes::
	goto_if_set FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN, Wyrmtide_LaterRoutes
	goto DewfordTown_EventScript_BrineyNormal
Wyrmtide_LaterRoutes::
	msgbox Wyrmtide_Text_LaterRoutes, MSGBOX_DEFAULT
	releaseall
	end
Wyrmtide_ShipReminder::
	msgbox Wyrmtide_Text_ShipReminder, MSGBOX_NPC
	end
Wyrmtide_Depart::
	msgbox Wyrmtide_Text_SetSail, MSGBOX_DEFAULT
	closemessage
	playbgm MUS_SAILING, TRUE
	fadescreen FADE_TO_BLACK
	playse SE_SHIP
	delay 90
	warp MAP_LEGENDS_WYRMTIDE_ISLE, 14, 21
	waitstate
	releaseall
	end
Wyrmtide_Landing::
	setflag FLAG_LEGENDS_WYRMTIDE_LANDED
	end
Wyrmtide_ShoreBriney::
	lock
	faceplayer
	goto_if_unset FLAG_LEGENDS_WYRMTIDE_CALMED, Wyrmtide_ShoreOffer
	goto_if_set FLAG_LEGENDS_WYRMTIDE_REPORT, Wyrmtide_ShoreOffer
	msgbox Wyrmtide_Text_Report, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_WYRMTIDE_REPORT
Wyrmtide_ShoreOffer::
	msgbox Wyrmtide_Text_ReturnOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, Wyrmtide_Return
	msgbox Wyrmtide_Text_Wait, MSGBOX_DEFAULT
	releaseall
	end
Wyrmtide_Return::
	closemessage
	playbgm MUS_SAILING, TRUE
	fadescreen FADE_TO_BLACK
	delay 60
	warp MAP_DEWFORD_TOWN, 11, 10
	waitstate
	releaseall
	end
Wyrmtide_ShoreTablet::
	msgbox Wyrmtide_Text_ShoreTablet, MSGBOX_SIGN
	end
Wyrmtide_MakerTablet::
	msgbox Wyrmtide_Text_MakerTablet, MSGBOX_SIGN
	end
Wyrmtide_SeaTablet::
	msgbox Wyrmtide_Text_SeaTablet, MSGBOX_SIGN
	end
Wyrmtide_SealOnLoad::
	goto_if_unset FLAG_LEGENDS_WYRMTIDE_SEAL_OPEN, Common_EventScript_NopReturn
	call Wyrmtide_RemoveSeal
	return
Wyrmtide_Seal::
	lockall
	goto_if_set FLAG_LEGENDS_WYRMTIDE_SEAL_OPEN, Wyrmtide_Enter
	specialvar VAR_RESULT, LegendsWyrmtideHasMaker
	goto_if_eq VAR_RESULT, FALSE, Wyrmtide_Sealed
	msgbox Wyrmtide_Text_SealAnswers, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_REGIGIGAS, CRY_MODE_NORMAL
	waitmoncry
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 1
	setvar VAR_0x8006, 24
	setvar VAR_0x8007, 3
	special ShakeScreen
	waitstate
	playse SE_DOOR
	setflag FLAG_LEGENDS_WYRMTIDE_SEAL_OPEN
	call Wyrmtide_RemoveSeal
	special DrawWholeMapView
	msgbox Wyrmtide_Text_SealOpen, MSGBOX_DEFAULT
Wyrmtide_Enter::
	msgbox Wyrmtide_Text_Enter, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	closemessage
	fadescreen FADE_TO_BLACK
	warp MAP_LEGENDS_WYRMTIDE_DESCENT1, 8, 4
	waitstate
	releaseall
	end
Wyrmtide_Sealed::
	msgbox Wyrmtide_Text_Sealed, MSGBOX_DEFAULT
	releaseall
	end
Wyrmtide_RemoveSeal::
	setmetatile 15, 10, METATILE_Cave_SealedChamberEntrance_BottomLeft, TRUE
	setmetatile 16, 10, METATILE_Cave_SealedChamberEntrance_BottomMid, FALSE
	setmetatile 17, 10, METATILE_Cave_SealedChamberEntrance_BottomRight, TRUE
	return
Wyrmtide_DepthTablet::
	msgbox Wyrmtide_Text_DepthTablet, MSGBOX_SIGN
	end
Wyrmtide_ChamberOnTransition::
	setvar VAR_OBJ_GFX_ID_F, OBJ_EVENT_MON + SPECIES_REGIDRAGO
	end
Wyrmtide_ChamberOnResume::
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, Wyrmtide_CheckCatch
	end
Wyrmtide_CheckCatch::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	setflag FLAG_LEGENDS_WYRMTIDE_CAUGHT
	setflag FLAG_LEGENDS_WYRMTIDE_CALMED
	removeobject 1
	return
Wyrmtide_Regidrago::
	lockall
	faceplayer
	goto_if_set FLAG_LEGENDS_WYRMTIDE_CAUGHT, LegendsStory_Return
	goto_if_set FLAG_LEGENDS_WYRMTIDE_AWAKENED, Wyrmtide_Challenge
	msgbox Wyrmtide_Text_Sleeping, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	msgbox Wyrmtide_Text_Awakening, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_REGIDRAGO, CRY_MODE_ENCOUNTER
	waitmoncry
	setflag FLAG_LEGENDS_WYRMTIDE_AWAKENED
	goto Wyrmtide_Battle
Wyrmtide_Challenge::
	msgbox Wyrmtide_Text_Challenge, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
Wyrmtide_Battle::
	closemessage
	setwildbattle SPECIES_REGIDRAGO, 75
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special StartRegiBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Wyrmtide_Caught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, Wyrmtide_Calmed
	msgbox Wyrmtide_Text_Retry, MSGBOX_DEFAULT
	releaseall
	end
Wyrmtide_Caught::
	setflag FLAG_LEGENDS_WYRMTIDE_CAUGHT
	removeobject 1
Wyrmtide_Calmed::
	setflag FLAG_LEGENDS_WYRMTIDE_CALMED
	msgbox Wyrmtide_Text_Calmed, MSGBOX_DEFAULT
	releaseall
	end

Wyrmtide_Text_Call:
	.string "UNKNOWN NUMBER: ...Ahoy?\n"
	.string "Can you hear me, {PLAYER}?\p"
	.string "MR. BRINEY here! PEEKO spotted\n"
	.string "something after those tremors.\p"
	.string "A little isle, just west of DEWFORD!\n"
	.string "There's old stonework on its shore.\p"
	.string "The currents have settled now.\n"
	.string "I'll take you there, if you're game!\p"
	.string "Meet me by the boat in DEWFORD.\n"
	.string "And keep this between us, eh?$"
Wyrmtide_Text_Departure:
	.string "MR. BRINEY: Ahoy, {PLAYER}!\n"
	.string "Ready to visit my little discovery?$"
Wyrmtide_Text_LaterRoutes:
	.string "MR. BRINEY: I've chartered this boat\n"
	.string "for our island expedition.\p"
	.string "I left my old coastal rounds\n"
	.string "to other captains. I'll wait here!$"
Wyrmtide_Text_ShipReminder:
	.string "MR. BRINEY: That rocky little isle\n"
	.string "is still on my mind!\p"
	.string "Meet me at DEWFORD's boat when\n"
	.string "you're ready for our expedition.$"
Wyrmtide_Text_SetSail:
	.string "MR. BRINEY: Westward, then!\n"
	.string "PEEKO, keep an eye on the reefs!$"
Wyrmtide_Text_ReturnOffer:
	.string "MR. BRINEY: Shall we head back\n"
	.string "to DEWFORD?$"
Wyrmtide_Text_Wait:
	.string "MR. BRINEY: Take your time.\n"
	.string "PEEKO and I aren't going anywhere.$"
Wyrmtide_Text_Report:
	.string "MR. BRINEY: A dragon sleeping\n"
	.string "beneath that little isle?\p"
	.string "The sea's still got secrets, eh?\n"
	.string "I'm glad I brought you along.\p"
	.string "This passage stays open to you.\n"
	.string "Just say the word, {PLAYER}!$"
Wyrmtide_Text_ShoreTablet:
	.string "The salt-worn tablet reads:\p"
	.string "THREE KEPT THE DOOR.\n"
	.string "ONE GAVE THE THREE THEIR FORM.\p"
	.string "SEEK NOT THE SERVANTS,\n"
	.string "BUT THE HAND THAT SHAPED THEM.$"
Wyrmtide_Text_MakerTablet:
	.string "Beneath a worn six-pointed mark:\p"
	.string "NOT STONE, NOR ICE, NOR STEEL\n"
	.string "ALONE SHALL BREAK THIS SILENCE.\p"
	.string "LET THE CONTINENT'S MOVER\n"
	.string "STAND AMONG YOUR SIX.$"
Wyrmtide_Text_SeaTablet:
	.string "An inscription faces the sea:\p"
	.string "WE HID THE LAST HEART\n"
	.string "WHERE NO SUN COULD FIND IT.\p"
	.string "ITS MAKER ALONE\n"
	.string "MAY CALL IT FROM ITS DREAM.$"
Wyrmtide_Text_Sealed:
	.string "An unbroken stone seal bars\n"
	.string "the entrance.\p"
	.string "Six worn hollows surround a larger\n"
	.string "mark. Something is missing...$"
Wyrmtide_Text_SealAnswers:
	.string "REGIGIGAS turns toward the seal.\n"
	.string "The hollows begin to hum...$"
Wyrmtide_Text_SealOpen:
	.string "The ancient stone parts.\n"
	.string "Cold air rises from far below.$"
Wyrmtide_Text_Enter:
	.string "A stairway descends into darkness.\n"
	.string "Go inside?$"
Wyrmtide_Text_DepthTablet:
	.string "The letters here are untouched\n"
	.string "by wind or salt.\p"
	.string "THE MAKER GAVE ALL IT COULD.\n"
	.string "THE LAST HEART STILL DREAMS.\p"
	.string "DOWN, BEYOND THE REACH OF TIDES,\n"
	.string "LET ITS REST BE UNDISTURBED.$"
Wyrmtide_Text_Sleeping:
	.string "A crimson shape lies motionless.\n"
	.string "A faint pulse stirs within it...\p"
	.string "REGIDRAGO is sleeping deeply.\n"
	.string "Call out to it?$"
Wyrmtide_Text_Awakening:
	.string "The pulse quickens.\n"
	.string "Stone trembles beneath your feet.\p"
	.string "Two vast jaws lift from the dust.\n"
	.string "The dragon opens its eyes!$"
Wyrmtide_Text_Challenge:
	.string "REGIDRAGO watches you in silence.\n"
	.string "Challenge it again?$"
Wyrmtide_Text_Retry:
	.string "REGIDRAGO remains in the chamber.\n"
	.string "Its long vigil is not yet over.$"
Wyrmtide_Text_Calmed:
	.string "The chamber falls quiet.\n"
	.string "The pulse beneath the isle settles.\p"
	.string "MR. BRINEY is waiting on the shore.$"

Wyrmtide_Peeko::
	msgbox Wyrmtide_Text_Peeko, MSGBOX_NPC
	end
Wyrmtide_Text_Peeko:
	.string "PEEKO: Pihyoh!$"
Wyrmtide_ExitCavern::
	lockall
	fadescreen FADE_TO_BLACK
	warp MAP_LEGENDS_WYRMTIDE_ISLE, 16, 11
	waitstate
	releaseall
	end

Wyrmtide_FinalTablet::
	msgbox Wyrmtide_Text_FinalTablet, MSGBOX_SIGN
	end
Wyrmtide_Text_FinalTablet:
	.string "The final inscription reads:\p"
	.string "A HEART OF DRAGON POWER.\n"
	.string "A BODY LEFT UNFINISHED.\p"
	.string "WE GAVE IT STONE AND SILENCE,\n"
	.string "UNTIL ITS MAKER COULD RETURN.$"

Wyrmtide_DewfordResume::
	call Wyrmtide_PrepareDewford
	special LegendsWyrmtideRefreshDewford
	end
