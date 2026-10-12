@ Chapter 5: Stone and Tide. Either difficulty and either order count.
LegendsStory_Chapter5_Journal::
	msgbox LegendsStory_Text_NorthDirections, MSGBOX_DEFAULT
	goto_if_unset FLAG_LEGENDS_STORY_NORTH_WATER, LegendsStory_Return
	goto_if_unset FLAG_LEGENDS_STORY_NORTH_STONE, LegendsStory_Return
	msgbox LegendsStory_Text_NorthReport, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_NORTH_REPORT
	msgbox LegendsStory_Text_EmberDirections, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_NorthWater::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_REPORT, LegendsStory_Locked
	goto_if_unset FLAG_LEGENDS_KANTO_MISTY_WON, LegendsStory_NeedMisty
	goto_if_set FLAG_LEGENDS_STORY_NORTH_WATER, LegendsStory_NorthWaterDone
	msgbox LegendsStory_Text_WaterOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	msgbox LegendsStory_Text_WaterScene, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_NORTH_WATER
LegendsStory_NorthWaterDone::
	msgbox LegendsStory_Text_WaterDone, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_NeedMisty::
	msgbox LegendsStory_Text_NeedMisty, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_NorthStone::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_REPORT, LegendsStory_Locked
	goto_if_unset FLAG_LEGENDS_KANTO_BROCK_WON, LegendsStory_NeedBrock
	goto_if_set FLAG_LEGENDS_STORY_NORTH_STONE, LegendsStory_NorthStoneDone
	msgbox LegendsStory_Text_StoneOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	msgbox LegendsStory_Text_StoneScene, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_NORTH_STONE
LegendsStory_NorthStoneDone::
	msgbox LegendsStory_Text_StoneDone, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_NeedBrock::
	msgbox LegendsStory_Text_NeedBrock, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_Route4ReturnTrail::
	lockall
	faceplayer
	msgbox LegendsStory_Text_ReturnTrail, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	closemessage
	fadescreen FADE_TO_BLACK
	warp MAP_LEGENDS_KANTO_ROUTE4, 15, 14
	waitstate
	releaseall
	end
LegendsStory_Text_NorthDirections:
	.string "WING SURVEY: Stone and Tide. Go west\n"
	.string "from ROUTE 10 along ROUTE 9 to\p"
	.string "CERULEAN. MISTY studies the current.\p"
	.string "Go west along ROUTE 4. The survey\n"
	.string "guide by MT. MOON's eastern exit\p"
	.string "offers a return trail around the\n"
	.string "one-way ledges.\p"
	.string "ROUTE 3 leads west to PEWTER. Meet\n"
	.string "BROCK, then compare a river reading in\p"
	.string "CERULEAN with the stone survey at MT.\n"
	.string "MOON's western entrance.\p"
	.string "Win both visiting challenges in either\n"
	.string "difficulty and either order. Return\p"
	.string "here with both field readings.$"

LegendsStory_Text_WaterOffer:
	.string "RIVER RESEARCHER: MISTY's notes\n"
	.string "match the old gauge. Compare its\p"
	.string "calm-water reading with SEAFOAM's\n"
	.string "current?$"

LegendsStory_Text_WaterScene:
	.string "The river moves normally. A small\n"
	.string "reflection flickers above it, then\p"
	.string "vanishes against the sky.\p"
	.string "It copied ARTICUNO's call, but the\n"
	.string "gauge did not change. The visitor\p"
	.string "follows the birds. It does not control\n"
	.string "their habitats.$"

LegendsStory_Text_WaterDone:
	.string "The river comparison is recorded. The\n"
	.string "copied call left no change in the\p"
	.string "current.$"

LegendsStory_Text_NeedMisty:
	.string "MISTY has the matching gauge record.\n"
	.string "Complete her visiting GYM challenge\p"
	.string "before comparing these readings.$"

LegendsStory_Text_StoneOffer:
	.string "STONE RESEARCHER: BROCK found old\n"
	.string "rockfalls, not a fresh quake. Compare\p"
	.string "his notes with the marks near MT.\n"
	.string "MOON?$"

LegendsStory_Text_StoneScene:
	.string "You compare the weathered rocks.\n"
	.string "These cracks are old. Tiny prints\p"
	.string "cross fresh dust without disturbing a\n"
	.string "single stone.\p"
	.string "A bright feather caught in the rock\n"
	.string "faces south. A warmer trail continues\p"
	.string "beyond the cold and electric roosts.$"

LegendsStory_Text_StoneDone:
	.string "The stone reading is recorded. No new\n"
	.string "quake connects these prints to\p"
	.string "HOENN's buried vault.$"

LegendsStory_Text_NeedBrock:
	.string "BROCK can date these rockfalls.\n"
	.string "Complete his PEWTER visiting challenge\p"
	.string "before comparing the stone marks.$"

LegendsStory_Text_NorthReport:
	.string "FIELD AIDE: HOENN's fault was local.\n"
	.string "KANTO's currents and rocks are stable\p"
	.string "too.\p"
	.string "The smaller visitor copies calls and\n"
	.string "follows the birds without changing\p"
	.string "their habitats. Our remaining feather\n"
	.string "points toward volcanic air.$"

LegendsStory_Text_ReturnTrail:
	.string "SURVEY GUIDE: MT. MOON's ledges run\n"
	.string "east. Our marked return trail skirts\p"
	.string "the cliffs to its western entrance.\p"
	.string "Take the return trail? From there,\n"
	.string "ROUTE 3 leads west to PEWTER. The cave\p"
	.string "itself retains its original passages.$"
