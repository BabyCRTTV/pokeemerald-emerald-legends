@ Chapter 6: Ember's Passage. A small Sevii expedition, not the whole islands.
LegendsStory_Chapter6_Journal::
	goto_if_set FLAG_LEGENDS_STORY_EMBER_REPORT, LegendsStory_Chapter6_Filed
	msgbox LegendsStory_Text_EmberDirections, MSGBOX_DEFAULT
	goto_if_unset FLAG_LEGENDS_STORY_MOLTRES_SEEN, LegendsStory_Return
	msgbox LegendsStory_Text_EmberReport, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_EMBER_REPORT
LegendsStory_Chapter6_Filed::
	msgbox LegendsStory_Text_Endpoint, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_EmberFerry::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_NORTH_REPORT, LegendsStory_Locked
	goto_if_unset FLAG_LEGENDS_KANTO_BLAINE_WON, LegendsStory_NeedBlaine
	msgbox LegendsStory_Text_EmberSail, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	closemessage
	fadescreen FADE_TO_BLACK
	playse SE_SHIP
	delay 40
	warp MAP_LEGENDS_KANTO_MT_EMBER_EXTERIOR, 28, 47
	waitstate
	releaseall
	end
LegendsStory_EmberReturn::
	lockall
	faceplayer
	msgbox LegendsStory_Text_EmberReturn, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	closemessage
	fadescreen FADE_TO_BLACK
	playse SE_SHIP
	delay 40
	warp MAP_LEGENDS_KANTO_CINNABAR_ISLAND, 20, 9
	waitstate
	releaseall
	end
LegendsStory_NeedBlaine::
	msgbox LegendsStory_Text_NeedBlaine, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_EmberGuide::
	msgbox LegendsStory_Text_EmberGuide, MSGBOX_NPC
	end
LegendsStory_Text_EmberDirections:
	.string "WING SURVEY: Ember's Passage. SURF\n"
	.string "west along ROUTE 20 to CINNABAR.\p"
	.string "BLAINE has the volcanic observation.\p"
	.string "Win his visiting challenge, then speak\n"
	.string "to the expedition sailor by the\p"
	.string "eastern shore. The boat goes to MT.\n"
	.string "EMBER's southern landing.\p"
	.string "Follow the summit path. STRENGTH and\n"
	.string "ROCK SMASH keep their normal\p"
	.string "requirements. Observe the fiery roost\n"
	.string "and return here.$"

LegendsStory_Text_EmberSail:
	.string "BLAINE confirmed the feather's\n"
	.string "source. Our survey boat will take you\p"
	.string "to MT. EMBER in the SEVII ISLANDS.\p"
	.string "This is a summit expedition. The sailor\n"
	.string "stays at the landing for your return.\p"
	.string "Sail now?$"

LegendsStory_Text_EmberReturn:
	.string "The survey boat is ready. Return to\n"
	.string "CINNABAR's eastern shore?$"

LegendsStory_Text_NeedBlaine:
	.string "BLAINE can identify this volcanic\n"
	.string "feather. Complete his visiting\p"
	.string "challenge before our MT. EMBER\n"
	.string "expedition.$"

LegendsStory_Text_EmberGuide:
	.string "The summit trail begins at the western\n"
	.string "cave. It climbs through three rooms\p"
	.string "and returns outside near the peak.\p"
	.string "The RUBY tunnels are outside this\n"
	.string "expedition. Your boat stays at the\p"
	.string "southern landing. On the summit, use\n"
	.string "STRENGTH to shift the boulders.$"

LegendsStory_Text_EmberReport:
	.string "FIELD AIDE: MOLTRES shelters beside a\n"
	.string "warm updraft. Its migration explains\p"
	.string "the inland feather.\p"
	.string "Three birds, three habitats. None\n"
	.string "caused HOENN's fault. At every site,\p"
	.string "the smaller visitor passed quietly\n"
	.string "through.\p"
	.string "OAK is comparing the copied cries with\n"
	.string "an old maritime record. A missing\p"
	.string "eighth GYM record and one final voyage\n"
	.string "remain ahead.$"

LegendsStory_Text_Endpoint:
	.string "These three expeditions are complete.\n"
	.string "The next WING SURVEY chapter will\p"
	.string "follow the elusive visitor.\p"
	.string "VIRIDIAN's challenge and the final MEW\n"
	.string "voyage are not open yet. You may\p"
	.string "explore, revisit uncaught legends, or\n"
	.string "return to HOENN.$"

LegendsStory_Moltres::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_NORTH_REPORT, LegendsStory_Locked
	goto_if_unset FLAG_LEGENDS_KANTO_BLAINE_WON, LegendsStory_Locked
	goto_if_set FLAG_LEGENDS_STORY_MOLTRES_CAUGHT, LegendsStory_Return
	goto_if_set FLAG_LEGENDS_STORY_MOLTRES_SEEN, LegendsStory_Moltres_Offer
	playmoncry SPECIES_MOLTRES, CRY_MODE_NORMAL
	waitmoncry
	msgbox LegendsStory_Moltres_Text_Observe, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_MOLTRES_SEEN
LegendsStory_Moltres_Offer::
	msgbox LegendsStory_Moltres_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	closemessage
	waitse
	playmoncry SPECIES_MOLTRES, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_MOLTRES, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, LegendsStory_Moltres_Caught
	removeobject 1
	msgbox LegendsStory_Moltres_Text_Retry, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_Moltres_Caught::
	setflag FLAG_LEGENDS_STORY_MOLTRES_CAUGHT
	removeobject 1
	msgbox LegendsStory_Moltres_Text_Caught, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_Moltres_OnResume::
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, LegendsStory_Moltres_CheckCatch
	end
LegendsStory_Moltres_CheckCatch::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	setflag FLAG_LEGENDS_STORY_MOLTRES_CAUGHT
	removeobject 1
	return
LegendsStory_Moltres_Text_Observe:
	.string "Fire lights the crest above you.\n"
	.string "MOLTRES lifts its wings in the rising\p"
	.string "volcanic air.\p"
	.string "It turns toward the sea. A smaller\n"
	.string "shadow answers its cry from empty sky,\p"
	.string "then fades. You record the warm roost\n"
	.string "and the copied call.$"

LegendsStory_Moltres_Text_Offer:
	.string "Challenge MOLTRES at Lv. 50? Its\n"
	.string "survey is complete even if you leave it\p"
	.string "here.\p"
	.string "Fainting or fleeing allows a retry on\n"
	.string "reentry. Capture is permanent. GYM\p"
	.string "difficulty does not change this\n"
	.string "encounter.$"

LegendsStory_Moltres_Text_Retry:
	.string "MOLTRES retreats to shelter. It\n"
	.string "returns on your next visit. Your\p"
	.string "survey notes are safe.$"

LegendsStory_Moltres_Text_Caught:
	.string "MOLTRES joined your collection. Your\n"
	.string "observation remains recorded. Return\p"
	.string "to the FIELD AIDE.$"
