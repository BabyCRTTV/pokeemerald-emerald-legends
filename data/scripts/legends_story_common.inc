@ Explicit, saved gates. No capture trophies or altered Hoenn badges.
LegendsStory_Return::
	releaseall
	end
LegendsStory_Locked::
	msgbox LegendsStory_Text_Locked, MSGBOX_DEFAULT
	releaseall
	end
LegendsStory_Journal::
	goto_if_unset FLAG_LEGENDS_STORY_SEAFOAM_REPORT, LegendsStory_Chapter4_Journal
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_REPORT, LegendsHoenn_Journal
	goto_if_unset FLAG_LEGENDS_STORY_NORTH_REPORT, LegendsStory_Chapter5_Journal
	goto_if_unset FLAG_LEGENDS_STORY_EMBER_REPORT, LegendsStory_Chapter6_Journal
	goto LegendsFinal_Journal
LegendsStory_Text_Locked:
	.string "Finish the previous WING SURVEY\n"
	.string "report first. OAK's aide keeps your\p"
	.string "notes at VERMILION FAN CLUB.$"

LegendsStory_CityGuide::
	msgbox LegendsStory_Text_CityGuide, MSGBOX_NPC
	end
LegendsStory_Text_CityGuide:
	.string "The local GYM, POKEMON CENTER and\n"
	.string "MART welcome visitors. OAK's aide in\p"
	.string "VERMILION keeps your WING SURVEY\n"
	.string "notes.\p"
	.string "Some roads and buildings remain\n"
	.string "closed. Signs mark those approaches.$"
