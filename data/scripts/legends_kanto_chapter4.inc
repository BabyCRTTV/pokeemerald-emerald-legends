@ Chapter 4: Stillwater Wings. Native boulder/current rooms.
LegendsStory_Chapter4_Journal::
	msgbox LegendsStory_Text_SeafoamDirections, MSGBOX_DEFAULT
	goto_if_unset FLAG_LEGENDS_STORY_ARTICUNO_SEEN, LegendsStory_Return
	msgbox LegendsStory_Text_SeafoamReport, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_SEAFOAM_REPORT
	setflag FLAG_LEGENDS_STORY_WEATHER_SUMMONED
	msgbox LegendsStory_Text_HoennCall, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_SeafoamGuide::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_KANTO_SURVEY_POWER_REPORT, LegendsStory_Locked
	msgbox LegendsStory_Text_SeafoamGuide, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_Text_SeafoamDirections:
	.string "WING SURVEY: Stillwater Wings. SURF\n"
	.string "south from FUCHSIA, then west on\p"
	.string "ROUTE 20 to SEAFOAM ISLANDS.\p"
	.string "Our boat is sheltering outside the\n"
	.string "east cave. Use STRENGTH to drop the\p"
	.string "boulders down the shafts and stop\n"
	.string "both currents.\p"
	.string "Find the cold roost on B4F. Observe\n"
	.string "the bird, then bring your notes here.\p"
	.string "Capture is optional.$"

LegendsStory_Text_SeafoamGuide:
	.string "SURVEY SAILOR: We sheltered here when\n"
	.string "the channels changed. The boat is\p"
	.string "safe, but we cannot take a reading in\n"
	.string "that current.\p"
	.string "Follow both boulder shafts from 1F\n"
	.string "down to B3F. Then push the loose B3F\p"
	.string "boulders into its two southern holes.\p"
	.string "Both channels must settle. The upper\n"
	.string "western island on B4F holds the cold\p"
	.string "roost. Your HOENN SURF and STRENGTH\n"
	.string "rules still apply.$"

LegendsStory_Text_SeafoamReport:
	.string "FIELD AIDE: ARTICUNO's frost follows a\n"
	.string "cold updraft. The shifted stones\p"
	.string "redirected the current beneath its\n"
	.string "roost.\p"
	.string "You made the channel safe without\n"
	.string "driving the bird away. The tiny prints\p"
	.string "stop at open water. Our smaller visitor\n"
	.string "can travel without a boat.$"

LegendsStory_Text_HoennCall:
	.string "A message arrives from HOENN's\n"
	.string "WEATHER INSTITUTE.\p"
	.string "Rainfall and ground pressure are\n"
	.string "repeating a pattern long after\p"
	.string "RAYQUAZA ended the crisis. These\n"
	.string "readings differ from the birds'\p"
	.string "habitats.\p"
	.string "Return on the VERMILION ferry to\n"
	.string "LILYCOVE. Meet the new field scientist\p"
	.string "upstairs at the WEATHER INSTITUTE on\n"
	.string "ROUTE 119.\p"
	.string "KANTO will wait. Bring us the\n"
	.string "explanation when HOENN is safe.$"

LegendsStory_Articuno::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_KANTO_SURVEY_POWER_REPORT, LegendsStory_Locked
	goto_if_unset FLAG_LEGENDS_STORY_SEAFOAM_B3F_CURRENT, LegendsStory_Locked
	goto_if_unset FLAG_LEGENDS_STORY_SEAFOAM_B4F_CURRENT, LegendsStory_Locked
	goto_if_set FLAG_LEGENDS_STORY_ARTICUNO_CAUGHT, LegendsStory_Return
	goto_if_set FLAG_LEGENDS_STORY_ARTICUNO_SEEN, LegendsStory_Articuno_Offer
	playmoncry SPECIES_ARTICUNO, CRY_MODE_NORMAL
	waitmoncry
	msgbox LegendsStory_Articuno_Text_Observe, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_ARTICUNO_SEEN
LegendsStory_Articuno_Offer::
	msgbox LegendsStory_Articuno_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	closemessage
	waitse
	playmoncry SPECIES_ARTICUNO, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_ARTICUNO, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, LegendsStory_Articuno_Caught
	removeobject 1
	msgbox LegendsStory_Articuno_Text_Retry, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_Articuno_Caught::
	setflag FLAG_LEGENDS_STORY_ARTICUNO_CAUGHT
	removeobject 1
	msgbox LegendsStory_Articuno_Text_Caught, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_Articuno_OnResume::
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, LegendsStory_Articuno_CheckCatch
	end
LegendsStory_Articuno_CheckCatch::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	setflag FLAG_LEGENDS_STORY_ARTICUNO_CAUGHT
	removeobject 1
	return
LegendsStory_Articuno_Text_Observe:
	.string "Pale wings open above the calm water.\n"
	.string "Frost glitters in the cave's cold\p"
	.string "updraft. ARTICUNO!\p"
	.string "It watches the cleared channel. A tiny\n"
	.string "print marks the rim of a dry ledge, far\p"
	.string "above the water. You record both clues\n"
	.string "without disturbing the roost.$"

LegendsStory_Articuno_Text_Offer:
	.string "Challenge ARTICUNO at Lv. 50? Its\n"
	.string "survey is complete even if you leave it\p"
	.string "here.\p"
	.string "Fainting or fleeing allows a retry on\n"
	.string "reentry. Capture is permanent. GYM\p"
	.string "difficulty does not change this\n"
	.string "encounter.$"

LegendsStory_Articuno_Text_Retry:
	.string "ARTICUNO retreats to shelter. It\n"
	.string "returns on your next visit. Your\p"
	.string "survey notes are safe.$"

LegendsStory_Articuno_Text_Caught:
	.string "ARTICUNO joined your collection. Your\n"
	.string "observation remains recorded. Return\p"
	.string "to the FIELD AIDE.$"
