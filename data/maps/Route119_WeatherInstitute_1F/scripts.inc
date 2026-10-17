Route119_WeatherInstitute_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route119_WeatherInstitute_1F_OnTransition
	.byte 0

Route119_WeatherInstitute_1F_OnTransition:
	call_if_eq VAR_WEATHER_INSTITUTE_STATE, 0, Route119_WeatherInstitute_1F_EventScript_SetLittleBoyPos
	end

Route119_WeatherInstitute_1F_EventScript_SetLittleBoyPos::
	setobjectxyperm LOCALID_WEATHER_INSTITUTE_LITTLE_BOY, 0, 5
	setobjectmovementtype LOCALID_WEATHER_INSTITUTE_LITTLE_BOY, MOVEMENT_TYPE_FACE_RIGHT
	return

Route119_WeatherInstitute_1F_EventScript_LittleBoy::
	lock
	faceplayer
	special GetPlayerBigGuyGirlString
	goto_if_eq VAR_WEATHER_INSTITUTE_STATE, 0, Route119_WeatherInstitute_1F_EventScript_LittleBoyTeamAquaHere
	msgbox Route119_WeatherInstitute_1F_Text_WowYoureStrong, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_LittleBoyTeamAquaHere::
	msgbox Route119_WeatherInstitute_1F_Text_EveryoneWentUpstairs, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_InstituteWorker1::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, Route119_WeatherInstitute_1F_EventScript_StudyingRain
	setvar VAR_0x8004, 0
	call_if_set FLAG_DEFEATED_KYOGRE, Route119_WeatherInstitute_1F_EventScript_LegendaryDefeated
	call_if_set FLAG_DEFEATED_GROUDON, Route119_WeatherInstitute_1F_EventScript_LegendaryDefeated
	goto_if_eq VAR_0x8004, 2, Route119_WeatherInstitute_1F_EventScript_StudyingRain  @ Both defeated
	msgbox Route119_WeatherInstitute_1F_Text_NoticingAbnormalWeather, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_LegendaryDefeated::
	addvar VAR_0x8004, 1
	return

Route119_WeatherInstitute_1F_EventScript_StudyingRain::
	msgbox Route119_WeatherInstitute_1F_Text_ProfStudyingRain, MSGBOX_DEFAULT
	release
	end

Route119_WeatherInstitute_1F_EventScript_InstituteWorker2::
	lock
	faceplayer
	msgbox Route119_WeatherInstitute_1F_Text_WhatWereAquasUpTo, MSGBOX_DEFAULT
	goto_if_eq VAR_WEATHER_INSTITUTE_STATE, 0, Route119_WeatherInstitute_1F_EventScript_BulletinEnd
	msgbox Route119_WeatherInstitute_1F_Text_BulletinOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Route119_WeatherInstitute_1F_EventScript_BulletinEnd
	special LegendsSeasonBulletinSpecial
	goto_if_eq VAR_RESULT, 0, Route119_WeatherInstitute_1F_EventScript_BulletinSpring
	goto_if_eq VAR_RESULT, 1, Route119_WeatherInstitute_1F_EventScript_BulletinSummer
	goto_if_eq VAR_RESULT, 2, Route119_WeatherInstitute_1F_EventScript_BulletinAutumn
	msgbox Route119_WeatherInstitute_1F_Text_BulletinWinter, MSGBOX_DEFAULT
	goto Route119_WeatherInstitute_1F_EventScript_BulletinEnd

Route119_WeatherInstitute_1F_EventScript_BulletinSpring:
	msgbox Route119_WeatherInstitute_1F_Text_BulletinSpring, MSGBOX_DEFAULT
	goto Route119_WeatherInstitute_1F_EventScript_BulletinEnd

Route119_WeatherInstitute_1F_EventScript_BulletinSummer:
	msgbox Route119_WeatherInstitute_1F_Text_BulletinSummer, MSGBOX_DEFAULT
	goto Route119_WeatherInstitute_1F_EventScript_BulletinEnd

Route119_WeatherInstitute_1F_EventScript_BulletinAutumn:
	msgbox Route119_WeatherInstitute_1F_Text_BulletinAutumn, MSGBOX_DEFAULT

Route119_WeatherInstitute_1F_EventScript_BulletinEnd:
	release
	end

Route119_WeatherInstitute_1F_EventScript_Bed::
	lockall
	msgbox Route119_WeatherInstitute_1F_Text_TakeRestInBed, MSGBOX_DEFAULT
	closemessage
	call Common_EventScript_OutOfCenterPartyHeal
	releaseall
	end

Route119_WeatherInstitute_1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_GRUNT_WEATHER_INST_1, Route119_WeatherInstitute_1F_Text_Grunt1Intro, Route119_WeatherInstitute_1F_Text_Grunt1Defeat
	msgbox Route119_WeatherInstitute_1F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

Route119_WeatherInstitute_1F_EventScript_Grunt4::
	trainerbattle_single TRAINER_GRUNT_WEATHER_INST_4, Route119_WeatherInstitute_1F_Text_Grunt4Intro, Route119_WeatherInstitute_1F_Text_Grunt4Defeat
	msgbox Route119_WeatherInstitute_1F_Text_Grunt4PostBattle, MSGBOX_AUTOCLOSE
	end

Route119_WeatherInstitute_1F_Text_Grunt1Intro:
	.string "The BOSS got interested in\n"
	.string "the research they have going here,\l"
	.string "so he sent us out.\p"
	.string "You quit meddling!$"

Route119_WeatherInstitute_1F_Text_Grunt1Defeat:
	.string "Blast it…\n"
	.string "Blasted by a kid…$"

Route119_WeatherInstitute_1F_Text_Grunt1PostBattle:
	.string "Our BOSS knows everything.\p"
	.string "But I'm just a GRUNT. What would I know\n"
	.string "about what he's thinking?$"

Route119_WeatherInstitute_1F_Text_Grunt4Intro:
	.string "Huh?\n"
	.string "What's a kid doing here?$"

Route119_WeatherInstitute_1F_Text_Grunt4Defeat:
	.string "Huh?\n"
	.string "I lost?!$"

Route119_WeatherInstitute_1F_Text_Grunt4PostBattle:
	.string "Oh, no…\n"
	.string "I'll catch an earful for losing to a kid…\p"
	.string "I should just take a nap in the bed…$"

Route119_WeatherInstitute_1F_Text_EveryoneWentUpstairs:
	.string "While I was sleeping, everyone went\n"
	.string "upstairs!$"

Route119_WeatherInstitute_1F_Text_WowYoureStrong:
	.string "Wow, you're really strong!\p"
	.string "I wish I could be a POKéMON TRAINER\n"
	.string "like you!$"

Route119_WeatherInstitute_1F_Text_ProfStudyingRain:
	.string "The PROFESSOR loves rain.\n"
	.string "That's a fact.\p"
	.string "But if it keeps raining, people will be in\n"
	.string "trouble. That's another fact.\p"
	.string "And thus, the PROFESSOR is studying\n"
	.string "if the rain can be put to good use.$"

Route119_WeatherInstitute_1F_Text_NoticingAbnormalWeather:
	.string "On the 2nd floor of the INSTITUTE,\n"
	.string "we study the weather patterns over\l"
	.string "the HOENN region.\p"
	.string "We've been noticing temporary and\n"
	.string "isolated cases of droughts and\l"
	.string "heavy rain lately…$"

Route119_WeatherInstitute_1F_Text_WhatWereAquasUpTo:
	.string "Hello!\n"
	.string "We've been saved by your actions!\p"
	.string "What I don't understand is what on\n"
	.string "earth the AQUAS were up to.$"

Route119_WeatherInstitute_1F_Text_BulletinOffer:
	.string "Our field bulletin follows the\n"
	.string "region's changing seasons.\p"
	.string "Would you like today's notes?$"

Route119_WeatherInstitute_1F_Text_BulletinSpring:
	.string "FIELD BULLETIN: SPRING\p"
	.string "Fresh growth draws small BUG\n"
	.string "POKéMON out of hiding.\p"
	.string "Try watching the edges of\n"
	.string "PETALBURG WOODS and ROUTE 104.$"

Route119_WeatherInstitute_1F_Text_BulletinSummer:
	.string "FIELD BULLETIN: SUMMER\p"
	.string "Long, warm days make the\n"
	.string "riverbanks busy places.\p"
	.string "Watch the water along ROUTE 119.\n"
	.string "Bring a partner you trust.$"

Route119_WeatherInstitute_1F_Text_BulletinAutumn:
	.string "FIELD BULLETIN: AUTUMN\p"
	.string "Cooler air and mist change\n"
	.string "the look of HOENN's forests.\p"
	.string "Observe the treetops around\n"
	.string "FORTREE for subtle differences.$"

Route119_WeatherInstitute_1F_Text_BulletinWinter:
	.string "FIELD BULLETIN: WINTER\p"
	.string "Frost and flurries can hide\n"
	.string "tracks near grassy paths.\p"
	.string "Bring warm gear and watch\n"
	.string "where POKéMON take shelter.$"


Route119_WeatherInstitute_1F_Text_TakeRestInBed:
	.string "There's a bed…\n"
	.string "Let's take a rest.$"

