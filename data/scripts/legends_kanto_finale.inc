@ Wing Survey chapters 7-9. Existing Mew, native ferry, one eighth Gym record.
LegendsFinal_Journal::
	goto_if_set FLAG_LEGENDS_FINAL_REPORT, LegendsFinal_CompleteJournal
	goto_if_set FLAG_LEGENDS_FINAL_VOYAGE_READY, LegendsFinal_VoyageJournal
	goto_if_set FLAG_LEGENDS_FINAL_EIGHT_RECORDS, LegendsFinal_OakJournal
	msgbox LegendsFinal_Text_Viridian, MSGBOX_DEFAULT
	call LegendsFinal_CheckEight
	goto_if_eq VAR_RESULT, FALSE, LegendsStory_Return
	msgbox LegendsFinal_Text_Eight, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_FINAL_EIGHT_RECORDS
LegendsFinal_OakJournal::
	msgbox LegendsFinal_Text_OakDirections, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_VoyageJournal::
	msgbox LegendsFinal_Text_Voyage, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_CompleteJournal::
	msgbox LegendsFinal_Text_Complete, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_CheckEight::
	setvar VAR_RESULT, FALSE
	goto_if_unset FLAG_LEGENDS_STORY_EMBER_REPORT, Common_EventScript_NopReturn
	goto_if_unset FLAG_LEGENDS_KANTO_SURGE_WON, Common_EventScript_NopReturn
	goto_if_unset FLAG_LEGENDS_KANTO_KOGA_WON, Common_EventScript_NopReturn
	goto_if_unset FLAG_LEGENDS_KANTO_ERIKA_WON, Common_EventScript_NopReturn
	goto_if_unset FLAG_LEGENDS_KANTO_SABRINA_WON, Common_EventScript_NopReturn
	goto_if_unset FLAG_LEGENDS_KANTO_MISTY_WON, Common_EventScript_NopReturn
	goto_if_unset FLAG_LEGENDS_KANTO_BROCK_WON, Common_EventScript_NopReturn
	goto_if_unset FLAG_LEGENDS_KANTO_BLAINE_WON, Common_EventScript_NopReturn
	goto_if_unset FLAG_LEGENDS_KANTO_VIRIDIAN_WON, Common_EventScript_NopReturn
	setvar VAR_RESULT, TRUE
	return
LegendsFinal_ViridianDirections::
	msgbox LegendsFinal_Text_Viridian, MSGBOX_NPC
	end
LegendsFinal_LeagueClosed::
	msgbox LegendsFinal_Text_LeagueClosed, MSGBOX_NPC
	end
LegendsFinal_PalletGuide::
	msgbox LegendsFinal_Text_Pallet, MSGBOX_NPC
	end
LegendsFinal_ForestGuide::
	msgbox LegendsFinal_Text_Forest, MSGBOX_NPC
	end
LegendsFinal_LabNotes::
	msgbox LegendsFinal_Text_OakDirections, MSGBOX_SIGN
	end
LegendsFinal_GymEntry::
	lockall
	setvar VAR_TEMP_0, 1
	goto_if_unset FLAG_LEGENDS_STORY_EMBER_REPORT, LegendsFinal_GymNotReady
	goto_if_set FLAG_LEGENDS_KANTO_VIRIDIAN_WON, LegendsFinal_GymComplete
	msgbox LegendsKanto_Text_OneWin, MSGBOX_DEFAULT
	msgbox LegendsFinal_Text_Mode, MSGBOX_YESNO
	setflag FLAG_LEGENDS_FINAL_VIRIDIAN_MODE_SET
	goto_if_eq VAR_RESULT, YES, LegendsFinal_Champion
	clearflag FLAG_LEGENDS_FINAL_VIRIDIAN_CHAMPION
	msgbox LegendsKanto_Text_StandardChosen, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_Champion::
	setflag FLAG_LEGENDS_FINAL_VIRIDIAN_CHAMPION
	msgbox LegendsKanto_Text_ChampionChosen, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_GymNotReady::
	msgbox LegendsFinal_Text_GymNotReady, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_GymComplete::
	msgbox LegendsKanto_Text_GymCompleted, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_Blue::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_EMBER_REPORT, LegendsFinal_GymNotReady
	goto_if_set FLAG_LEGENDS_KANTO_VIRIDIAN_WON, LegendsFinal_BlueAfter
	goto_if_unset FLAG_LEGENDS_FINAL_VIRIDIAN_MODE_SET, LegendsFinal_GymEntry
	msgbox LegendsFinal_Text_BlueConfirm, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	goto_if_set FLAG_LEGENDS_FINAL_VIRIDIAN_CHAMPION, LegendsFinal_BlueChampion
	trainerbattle_single TRAINER_LEGENDS_KANTO_BLUE_STANDARD, LegendsFinal_Text_BlueIntro, LegendsFinal_Text_BlueDefeat
	goto LegendsFinal_BlueWon
LegendsFinal_BlueChampion::
	trainerbattle_single TRAINER_LEGENDS_KANTO_BLUE_CHAMPION, LegendsFinal_Text_BlueIntro, LegendsFinal_Text_BlueDefeat
LegendsFinal_BlueWon::
	setflag FLAG_LEGENDS_KANTO_VIRIDIAN_WON
	playfanfare MUS_OBTAIN_BADGE
	waitfanfare
	msgbox LegendsKanto_Text_VictoryRecorded, MSGBOX_DEFAULT
LegendsFinal_BlueAfter::
	msgbox LegendsFinal_Text_BlueClue, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_Oak::
	lockall
	faceplayer
	call LegendsFinal_CheckEight
	goto_if_eq VAR_RESULT, FALSE, LegendsFinal_OakNeedRecords
	setflag FLAG_LEGENDS_FINAL_EIGHT_RECORDS
	goto_if_set FLAG_LEGENDS_FINAL_REPORT, LegendsFinal_OakReward
	goto_if_unset FLAG_LEGENDS_FINAL_OAK_ANALYSIS, LegendsFinal_OakAnalysis
	goto_if_unset FLAG_LEGENDS_FINAL_VOYAGE_READY, LegendsFinal_OakMap
	goto_if_unset FLAG_LEGENDS_FINAL_ISLAND_VISITED, LegendsFinal_VoyageJournal
	goto_if_set FLAG_LEGENDS_FINAL_MEW_OBSERVED, LegendsFinal_OakReport
	goto_if_set FLAG_CAUGHT_MEW, LegendsFinal_OakReport
	goto LegendsFinal_VoyageJournal
LegendsFinal_OakNeedRecords::
	msgbox LegendsFinal_Text_NeedRecords, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_OakAnalysis::
	msgbox LegendsFinal_Text_OakAnalysis, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_FINAL_OAK_ANALYSIS
LegendsFinal_OakMap::
	checkitem ITEM_OLD_SEA_MAP
	goto_if_eq VAR_RESULT, TRUE, LegendsFinal_OakMapReady
	goto_if_set FLAG_RECEIVED_OLD_SEA_MAP, LegendsFinal_MapMissing
	msgbox LegendsFinal_Text_MapGift, MSGBOX_DEFAULT
	giveitem ITEM_OLD_SEA_MAP, 1
	goto_if_eq VAR_RESULT, FALSE, LegendsFinal_MapFull
LegendsFinal_OakMapReady::
	setflag FLAG_RECEIVED_OLD_SEA_MAP
	setflag FLAG_ENABLE_SHIP_FARAWAY_ISLAND
	setflag FLAG_LEGENDS_FINAL_VOYAGE_READY
	msgbox LegendsFinal_Text_Voyage, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_MapFull::
	msgbox LegendsFinal_Text_MapFull, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_MapMissing::
	msgbox LegendsFinal_Text_MapMissing, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_OakReport::
	msgbox LegendsFinal_Text_FinalReport, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_FINAL_REPORT
LegendsFinal_OakReward::
	goto_if_set FLAG_LEGENDS_FINAL_REWARD, LegendsFinal_OakAfter
	msgbox LegendsFinal_Text_Reward, MSGBOX_DEFAULT
	giveitem ITEM_MASTER_BALL, 1
	goto_if_eq VAR_RESULT, TRUE, LegendsFinal_RewardReceived
	addpcitem ITEM_MASTER_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, LegendsFinal_RewardFull
	msgbox LegendsFinal_Text_RewardPC, MSGBOX_DEFAULT
LegendsFinal_RewardReceived::
	setflag FLAG_LEGENDS_FINAL_REWARD
LegendsFinal_OakAfter::
	msgbox LegendsFinal_Text_Complete, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_RewardFull::
	msgbox LegendsFinal_Text_RewardFull, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_LabHeal::
	lockall
	faceplayer
	msgbox LegendsFinal_Text_Heal, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	closemessage
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox LegendsFinal_Text_Healed, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_IslandArrival::
	goto_if_unset FLAG_LEGENDS_FINAL_VOYAGE_READY, Common_EventScript_NopReturn
	setflag FLAG_LEGENDS_FINAL_ISLAND_VISITED
	setrespawn HEAL_LOCATION_LILYCOVE_CITY
	return
LegendsFinal_MewReentry::
	goto_if_unset FLAG_LEGENDS_FINAL_VOYAGE_READY, Common_EventScript_NopReturn
	goto_if_set FLAG_CAUGHT_MEW, Common_EventScript_NopReturn
	clearflag FLAG_DEFEATED_MEW
	return
LegendsFinal_MewObserve::
	goto_if_set FLAG_LEGENDS_FINAL_MEW_OBSERVED, LegendsFinal_MewChallenge
	playmoncry SPECIES_MEW, CRY_MODE_NORMAL
	waitmoncry
	msgbox LegendsFinal_Text_MewObserve, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_FINAL_MEW_OBSERVED
LegendsFinal_MewChallenge::
	msgbox LegendsFinal_Text_MewChallenge, MSGBOX_YESNO
	return
LegendsFinal_AlreadyCaught::
	goto_if_unset FLAG_LEGENDS_FINAL_VOYAGE_READY, Common_EventScript_NopReturn
	goto_if_unset FLAG_CAUGHT_MEW, Common_EventScript_NopReturn
	goto_if_set FLAG_LEGENDS_FINAL_MEW_OBSERVED, Common_EventScript_NopReturn
	msgbox LegendsFinal_Text_AlreadyCaught, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_FINAL_MEW_OBSERVED
	return
LegendsFinal_HoennEpilogue::
	goto_if_set FLAG_LEGENDS_FINAL_HOENN_EPILOGUE, LegendsFinal_HoennAfter
	msgbox LegendsFinal_Text_HoennEpilogue, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_FINAL_HOENN_EPILOGUE
LegendsFinal_HoennAfter::
	msgbox LegendsFinal_Text_HoennAfter, MSGBOX_DEFAULT
	releaseall
	end
LegendsFinal_Text_Viridian:
	.string "WING SURVEY: The Last Record. From\n"
	.string "PEWTER, follow ROUTE 2 south through\p"
	.string "VIRIDIAN FOREST to VIRIDIAN CITY.\p"
	.string "BLUE is serving as the visiting GYM's\n"
	.string "acting LEADER. Finish Ember's Passage\p"
	.string "first, then choose your challenge at\n"
	.string "the entrance.\p"
	.string "After all eight records, meet OAK at\n"
	.string "his PALLET lab. ROUTE 1 runs south\p"
	.string "from VIRIDIAN. You can also SURF\n"
	.string "north from CINNABAR along ROUTE 21.$"

LegendsFinal_Text_Eight:
	.string "FIELD AIDE: Eight visiting records,\n"
	.string "three bird habitats, and a fault\p"
	.string "restored in HOENN. You have followed\n"
	.string "every lead.\p"
	.string "OAK wants to compare the copied calls\n"
	.string "with an old voyage record. He is\p"
	.string "waiting in his PALLET lab.$"

LegendsFinal_Text_OakDirections:
	.string "WING SURVEY: A Familiar Shadow. OAK's\n"
	.string "lab is the large building in southeast\p"
	.string "PALLET TOWN.\p"
	.string "Go south from VIRIDIAN along ROUTE 1,\n"
	.string "or SURF north from CINNABAR on ROUTE\p"
	.string "21. His assistant can heal your party.$"

LegendsFinal_Text_LeagueClosed:
	.string "The INDIGO LEAGUE approach remains\n"
	.string "closed to this visiting circuit. BLUE\p"
	.string "handles the eighth GYM record here in\n"
	.string "VIRIDIAN.$"

LegendsFinal_Text_Pallet:
	.string "OAK has been listening to those copied\n"
	.string "cries all morning. His lab is the large\p"
	.string "building to the southeast.\p"
	.string "ROUTE 1 leads north to VIRIDIAN. SURF\n"
	.string "south along ROUTE 21 to CINNABAR.$"

LegendsFinal_Text_Forest:
	.string "The two gatehouses link ROUTE 2\n"
	.string "through this forest. PEWTER is north;\p"
	.string "VIRIDIAN is south.\p"
	.string "The forest still has its ordinary wild\n"
	.string "POKEMON. Follow the clear paths around\p"
	.string "the long grass.$"

LegendsFinal_Text_Mode:
	.string "BLUE's Champion challenge? YES: six\n"
	.string "POKEMON at Lv. 84-88. NO: four POKEMON\p"
	.string "at Lv. 64-68.$"

LegendsFinal_Text_GymNotReady:
	.string "The acting LEADER is reviewing the\n"
	.string "volcanic report. File Ember's Passage\p"
	.string "with OAK's aide in VERMILION FAN CLUB\n"
	.string "first.$"

LegendsFinal_Text_BlueConfirm:
	.string "BLUE: Ready for your final visiting\n"
	.string "challenge? You can change modes at\p"
	.string "the entrance until your one victory.$"

LegendsFinal_Text_BlueIntro:
	.string "BLUE: I agreed to keep this GYM open\n"
	.string "for OAK's survey. That doesn't mean\p"
	.string "I'll make your last record easy!\p"
	.string "Let's see what a HOENN CHAMPION can\n"
	.string "do!$"

LegendsFinal_Text_BlueDefeat:
	.string "You earned it. No excuses from me!$"

LegendsFinal_Text_BlueClue:
	.string "BLUE: Those tiny tracks passed right\n"
	.string "through this old GYM. No damage. Just a\p"
	.string "curious visitor following strong\n"
	.string "POKEMON.\p"
	.string "My grandfather says the copied calls\n"
	.string "match a voyage record from long ago.\p"
	.string "Take all eight records to his PALLET\n"
	.string "lab.$"

LegendsFinal_Text_NeedRecords:
	.string "OAK: The copied cries may belong to\n"
	.string "one POKEMON. I need the complete\p"
	.string "survey before I can be certain.\p"
	.string "File Ember's Passage and collect all\n"
	.string "eight visiting GYM records. BLUE is in\p"
	.string "VIRIDIAN; my aide in VERMILION keeps\n"
	.string "your directions.$"

LegendsFinal_Text_OakAnalysis:
	.string "OAK: Listen. ZAPDOS at the old plant.\n"
	.string "ARTICUNO above the still water.\p"
	.string "MOLTRES riding a warm updraft.\p"
	.string "Now hear the smaller visitor. Three\n"
	.string "calls, copied perfectly. The tiny\p"
	.string "prints and pink hair never belonged to\n"
	.string "any of those birds.\p"
	.string "BIRCH's readings separated HOENN's\n"
	.string "fault from the visitor's trail. It was\p"
	.string "curious about the roosts, not causing\n"
	.string "the crisis.\p"
	.string "An old sailor's record describes a pink\n"
	.string "POKEMON playing among deep grass on a\p"
	.string "distant island. The drawings match\n"
	.string "your tracks.\p"
	.string "MEW. I believe it crossed the sea to\n"
	.string "watch the birds and returned to its\p"
	.string "quiet home.\p"
	.string "Let us follow the voyage record\n"
	.string "carefully. Find it, observe it, and\p"
	.string "decide for yourself whether to\n"
	.string "challenge it.$"

LegendsFinal_Text_MapGift:
	.string "OAK: This OLD SEA MAP marks the\n"
	.string "recorded shore. Take it to LILYCOVE's\p"
	.string "ferry attendant. The captain knows\n"
	.string "those distant waters.$"

LegendsFinal_Text_MapFull:
	.string "There is no room for the OLD SEA MAP.\n"
	.string "Make room in KEY ITEMS, then speak to\p"
	.string "OAK again. Your analysis is recorded.$"

LegendsFinal_Text_MapMissing:
	.string "Your OLD SEA MAP was already issued,\n"
	.string "but it is not in your BAG. Retrieve it\p"
	.string "from storage and speak to OAK again. A\n"
	.string "second map will not be issued.$"

LegendsFinal_Text_Voyage:
	.string "Chapter 9: Beyond the Horizon. Sail\n"
	.string "from LILYCOVE with the OLD SEA MAP.\p"
	.string "Follow the island trail into the\n"
	.string "forest.\p"
	.string "Find MEW to hear the visitor's call.\n"
	.string "Capturing it is your choice. If MEW\p"
	.string "already travels with you, read the\n"
	.string "weathered shore sign or speak with\p"
	.string "the sailor.\p"
	.string "Return to OAK in PALLET TOWN with your\n"
	.string "field notes.$"


LegendsFinal_Text_MewObserve:
	.string "A small pink POKEMON rises from the\n"
	.string "grass. It turns its head, listening to\p"
	.string "your partner.\p"
	.string "For an instant, its playful cry echoes\n"
	.string "all three distant roosts. Then its own\p"
	.string "clear voice rings through the trees.\n"
	.string "MEW!\p"
	.string "You record the tracks, the copied\n"
	.string "calls, and the island habitat. OAK's\p"
	.string "final question is answered. Your\n"
	.string "survey does not require a capture.$"

LegendsFinal_Text_MewChallenge:
	.string "Challenge MEW at Lv. 30? NO leaves\n"
	.string "your observation complete. If\p"
	.string "uncaught, it remains available on\n"
	.string "forest reentry. A capture is\p"
	.string "permanent.$"

LegendsFinal_Text_AlreadyCaught:
	.string "The island record matches your earlier\n"
	.string "encounter with MEW. Its tracks and\p"
	.string "the copied calls fit the same playful\n"
	.string "visitor.\p"
	.string "You record the habitat alongside your\n"
	.string "existing capture. OAK has the missing\p"
	.string "piece. No second MEW waits in this\n"
	.string "forest.$"

LegendsFinal_Text_FinalReport:
	.string "OAK: A curious traveler, not a threat.\n"
	.string "The copied calls belonged to MEW, and\p"
	.string "the birds kept their own habitats.\p"
	.string "You crossed two regions, settled\n"
	.string "HOENN's buried fault, and let your\p"
	.string "observations speak before drawing\n"
	.string "conclusions.\p"
	.string "BIRCH and the WEATHER INSTITUTE have\n"
	.string "your island notes. BLUE has entered\p"
	.string "your eighth visiting record with the\n"
	.string "others.\p"
	.string "The WING SURVEY is complete. Thank\n"
	.string "you for showing us how much there is\p"
	.string "still to learn.$"

LegendsFinal_Text_Reward:
	.string "OAK: Please accept one MASTER BALL as\n"
	.string "our thanks for this journey. Your\p"
	.string "choice to observe or capture did not\n"
	.string "change the value of your work.$"

LegendsFinal_Text_RewardPC:
	.string "Your BAG was full. The MASTER BALL has\n"
	.string "been placed in your item storage PC.$"

LegendsFinal_Text_RewardFull:
	.string "Your BAG and item storage are full. The\n"
	.string "survey is complete, but your reward is\p"
	.string "still waiting. Make room and speak to\n"
	.string "OAK again.$"

LegendsFinal_Text_Complete:
	.string "The WING SURVEY is complete. You may\n"
	.string "revisit uncaught legends, sail between\p"
	.string "regions, or continue exploring HOENN.\p"
	.string "The WEATHER INSTITUTE scientist has\n"
	.string "one final letter from BIRCH. Your\p"
	.string "ordinary postgame remains open.$"

LegendsFinal_Text_Heal:
	.string "OAK's assistant can rest your team\n"
	.string "before the voyage. Heal your POKEMON?$"

LegendsFinal_Text_Healed:
	.string "Your team is refreshed. Safe travels!$"

LegendsFinal_Text_HoennEpilogue:
	.string "FIELD SCIENTIST: OAK sent the island\n"
	.string "report. BIRCH asked me to pass on his\p"
	.string "thanks.\p"
	.string "The gauges are steady. REGIGIGAS is\n"
	.string "quiet. We now know which signs\p"
	.string "belonged to the local fault and which\n"
	.string "to a curious traveler.\p"
	.string "Two regions shared their\n"
	.string "observations, and you found the\p"
	.string "connection. The work of a POKEMON\n"
	.string "researcher never really ends.$"

LegendsFinal_Text_HoennAfter:
	.string "Your WING SURVEY report is safely\n"
	.string "filed. Normal HOENN weather research\p"
	.string "continues, and the ferries remain\n"
	.string "available.$"
