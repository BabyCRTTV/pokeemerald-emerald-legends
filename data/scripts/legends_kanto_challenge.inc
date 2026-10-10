@ Legends Kanto: independent gym records and the Wing Survey journal.

LegendsKanto_Surge_Entry::
	lockall
	setvar VAR_TEMP_0, 1
	goto_if_set FLAG_LEGENDS_KANTO_SURGE_WON, LegendsKanto_Surge_Completed
	msgbox LegendsKanto_Text_OneWin, MSGBOX_DEFAULT
	msgbox LegendsKanto_Surge_Text_Mode, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LegendsKanto_Surge_Champion
	setvar VAR_LEGENDS_KANTO_SURGE_MODE, 1
	msgbox LegendsKanto_Text_StandardChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Surge_Champion::
	setvar VAR_LEGENDS_KANTO_SURGE_MODE, 2
	msgbox LegendsKanto_Text_ChampionChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Surge_Completed::
	msgbox LegendsKanto_Text_GymCompleted, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Surge_Leader::
	lockall
	faceplayer
	goto_if_set FLAG_LEGENDS_KANTO_SURGE_WON, LegendsKanto_Surge_AfterWin
	goto_if_eq VAR_LEGENDS_KANTO_SURGE_MODE, 0, LegendsKanto_Surge_Entry
	msgbox LegendsKanto_Surge_Text_Confirm, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	goto_if_eq VAR_LEGENDS_KANTO_SURGE_MODE, 2, LegendsKanto_Surge_BattleChampion
	trainerbattle_single TRAINER_LEGENDS_KANTO_SURGE_STANDARD, LegendsKanto_Surge_Text_Intro, LegendsKanto_Surge_Text_Defeat
	goto LegendsKanto_Surge_Won

LegendsKanto_Surge_BattleChampion::
	trainerbattle_single TRAINER_LEGENDS_KANTO_SURGE_CHAMPION, LegendsKanto_Surge_Text_Intro, LegendsKanto_Surge_Text_Defeat

LegendsKanto_Surge_Won::
	setflag FLAG_LEGENDS_KANTO_SURGE_WON
	msgbox LegendsKanto_Text_VictoryRecorded, MSGBOX_DEFAULT
LegendsKanto_Surge_AfterWin::
	msgbox LegendsKanto_Surge_Text_Clue, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Surge_Text_Mode:
	.string "Standard team: Lv. 52-56.\n"
	.string "Champion team: Lv. 72-76.\p"
	.string "Take the Champion challenge?\n"
	.string "YES: Champion. NO: Standard.$"

LegendsKanto_Surge_Text_Confirm:
	.string "Your chosen team is ready.\n"
	.string "One victory ends this GYM.\p"
	.string "Ready to battle?$"

LegendsKanto_Surge_Text_Intro:
	.string "LT. SURGE: HOENN's CHAMPION!\n"
	.string "Show me your fighting spirit!$"

LegendsKanto_Surge_Text_Defeat:
	.string "Now that's real power!$"

LegendsKanto_Surge_Text_Clue:
	.string "LT. SURGE: My instruments\n"
	.string "picked up an odd surge.\p"
	.string "It came from the old POWER\n"
	.string "PLANT, before a storm.\p"
	.string "A huge bird flew above it.\n"
	.string "Could it have been ZAPDOS?\p"
	.string "OAK's field aide is at the\n"
	.string "VERMILION FAN CLUB.\p"
	.string "Share what you've learned.\n"
	.string "This needs a careful survey.$"

LegendsKanto_Koga_Entry::
	lockall
	setvar VAR_TEMP_0, 1
	goto_if_set FLAG_LEGENDS_KANTO_KOGA_WON, LegendsKanto_Koga_Completed
	msgbox LegendsKanto_Text_OneWin, MSGBOX_DEFAULT
	msgbox LegendsKanto_Koga_Text_Mode, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LegendsKanto_Koga_Champion
	setvar VAR_LEGENDS_KANTO_KOGA_MODE, 1
	msgbox LegendsKanto_Text_StandardChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Koga_Champion::
	setvar VAR_LEGENDS_KANTO_KOGA_MODE, 2
	msgbox LegendsKanto_Text_ChampionChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Koga_Completed::
	msgbox LegendsKanto_Text_GymCompleted, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Koga_Leader::
	lockall
	faceplayer
	goto_if_set FLAG_LEGENDS_KANTO_KOGA_WON, LegendsKanto_Koga_AfterWin
	goto_if_eq VAR_LEGENDS_KANTO_KOGA_MODE, 0, LegendsKanto_Koga_Entry
	msgbox LegendsKanto_Koga_Text_Confirm, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	goto_if_eq VAR_LEGENDS_KANTO_KOGA_MODE, 2, LegendsKanto_Koga_BattleChampion
	trainerbattle_single TRAINER_LEGENDS_KANTO_KOGA_STANDARD, LegendsKanto_Koga_Text_Intro, LegendsKanto_Koga_Text_Defeat
	goto LegendsKanto_Koga_Won

LegendsKanto_Koga_BattleChampion::
	trainerbattle_single TRAINER_LEGENDS_KANTO_KOGA_CHAMPION, LegendsKanto_Koga_Text_Intro, LegendsKanto_Koga_Text_Defeat

LegendsKanto_Koga_Won::
	setflag FLAG_LEGENDS_KANTO_KOGA_WON
	msgbox LegendsKanto_Text_VictoryRecorded, MSGBOX_DEFAULT
LegendsKanto_Koga_AfterWin::
	msgbox LegendsKanto_Koga_Text_Clue, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Koga_Text_Mode:
	.string "Standard team: Lv. 56-60.\n"
	.string "Champion team: Lv. 76-80.\p"
	.string "Take the Champion challenge?\n"
	.string "YES: Champion. NO: Standard.$"

LegendsKanto_Koga_Text_Confirm:
	.string "Your chosen team is ready.\n"
	.string "One victory ends this GYM.\p"
	.string "Ready to battle?$"

LegendsKanto_Koga_Text_Intro:
	.string "KOGA: Strength alone is not\n"
	.string "enough. Observe, then act!$"

LegendsKanto_Koga_Text_Defeat:
	.string "Your judgment is excellent!$"

LegendsKanto_Koga_Text_Clue:
	.string "KOGA: Sailors report a cold\n"
	.string "wind near SEAFOAM ISLANDS.\p"
	.string "A pale bird passed above\n"
	.string "the sea. ARTICUNO, perhaps.\p"
	.string "I also heard of a bright\n"
	.string "wing over the western hills.\p"
	.string "OAK's aide needs both reports.\n"
	.string "Find them at the FAN CLUB.\p"
	.string "Treat these birds as living\n"
	.string "POKEMON, not prizes.$"

LegendsKanto_Text_OneWin:
	.string "GYM GUIDE: Choose a team\n"
	.string "for this GYM's challenge.\p"
	.string "Each LEADER can be defeated\n"
	.string "only ONCE on this save.\p"
	.string "Winning either mode closes\n"
	.string "BOTH challenges here.\p"
	.string "If you lose, you may retry\n"
	.string "or change your preference.\p"
	.string "Talk to me before battling\n"
	.string "to change your selection.$"

LegendsKanto_Text_StandardChosen:
	.string "Standard challenge selected.\n"
	.string "Your party is not rescaled.$"

LegendsKanto_Text_ChampionChosen:
	.string "Champion challenge selected.\n"
	.string "Your party is not rescaled.$"

LegendsKanto_Text_GymCompleted:
	.string "Your victory is recorded.\n"
	.string "This GYM is complete.\p"
	.string "The other difficulty cannot\n"
	.string "be challenged on this save.$"

LegendsKanto_Text_VictoryRecorded:
	.string "KANTO GYM victory recorded!\n"
	.string "Both modes are now complete.$"

LegendsKanto_Challenge_Decline::
	releaseall
	end

LegendsKanto_Survey_Aide::
	lockall
	faceplayer
	goto_if_set FLAG_LEGENDS_KANTO_SURVEY_STARTED, LegendsKanto_Survey_CheckProgress
	msgbox LegendsKanto_Text_SurveyIntro, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_KANTO_SURVEY_STARTED
LegendsKanto_Survey_CheckProgress::
	goto_if_unset FLAG_LEGENDS_KANTO_SURGE_WON, LegendsKanto_Survey_NoSurge
	goto_if_unset FLAG_LEGENDS_KANTO_KOGA_WON, LegendsKanto_Survey_OnlySurge
	goto_if_set FLAG_LEGENDS_KANTO_SURVEY_REPORT, LegendsKanto_Survey_Later
	msgbox LegendsKanto_Text_SurveyReport, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_KANTO_SURVEY_REPORT
LegendsKanto_Survey_Later::
	msgbox LegendsKanto_Text_JournalComplete, MSGBOX_DEFAULT
	msgbox LegendsKanto_Text_ReviewRecords, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Survey_Next
	msgbox LegendsKanto_Surge_Text_Clue, MSGBOX_DEFAULT
	msgbox LegendsKanto_Koga_Text_Clue, MSGBOX_DEFAULT
	msgbox LegendsKanto_Text_JournalEvidence, MSGBOX_DEFAULT
LegendsKanto_Survey_Next::
	msgbox LegendsKanto_Text_SurveyNext, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Survey_NoSurge::
	goto_if_set FLAG_LEGENDS_KANTO_KOGA_WON, LegendsKanto_Survey_OnlyKoga
	msgbox LegendsKanto_Text_SurveyReminder, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Survey_OnlySurge::
	msgbox LegendsKanto_Text_JournalOnlySurge, MSGBOX_DEFAULT
	msgbox LegendsKanto_Text_ReviewRecords, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	msgbox LegendsKanto_Surge_Text_Clue, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Survey_OnlyKoga::
	msgbox LegendsKanto_Text_JournalOnlyKoga, MSGBOX_DEFAULT
	msgbox LegendsKanto_Text_ReviewRecords, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	msgbox LegendsKanto_Koga_Text_Clue, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Text_SurveyIntro:
	.string "FIELD AIDE: PROF. OAK asked\n"
	.string "me to meet HOENN's CHAMPION.\p"
	.string "You helped stop KYOGRE and\n"
	.string "GROUDON's weather crisis.\p"
	.string "KANTO has odd reports too:\n"
	.string "storms, frost and fiery wings.\p"
	.string "We need to learn whether\n"
	.string "the birds are being disturbed.\p"
	.string "OAK calls this the WING SURVEY.\n"
	.string "The LEAGUE is helping us.\p"
	.string "Train with the GYM LEADERS.\n"
	.string "Listen to their observations.\p"
	.string "You choose the challenge.\n"
	.string "Either victory earns trust.$"

LegendsKanto_Text_SurveyReminder:
	.string "WING SURVEY: 0 of 2 records.\n"
	.string "No GYM reports collected yet.\p"
	.string "LT. SURGE: VERMILION GYM.\n"
	.string "KOGA: FUCHSIA GYM.\p"
	.string "Win their challenges in\n"
	.string "either mode, in any order.\p"
	.string "Return here to check progress\n"
	.string "and review collected clues.$"

LegendsKanto_Text_JournalOnlySurge:
	.string "WING SURVEY: 1 of 2 records.\n"
	.string "LT. SURGE: Report collected.\p"
	.string "KOGA: Report still needed.\n"
	.string "Visit his GYM in FUCHSIA.\p"
	.string "Win in either mode, then\n"
	.string "bring his observations here.$"

LegendsKanto_Text_JournalOnlyKoga:
	.string "WING SURVEY: 1 of 2 records.\n"
	.string "KOGA: Report collected.\p"
	.string "LT. SURGE: Report needed.\n"
	.string "Visit his GYM in VERMILION.\p"
	.string "Win in either mode, then\n"
	.string "bring his observations here.$"

LegendsKanto_Text_JournalComplete:
	.string "WING SURVEY: 2 of 2 records.\n"
	.string "LT. SURGE and KOGA: Filed.\p"
	.string "The first report is complete.\n"
	.string "Their GYMS remain completed.$"

LegendsKanto_Text_ReviewRecords:
	.string "Review the observations\n"
	.string "you've collected so far?$"

LegendsKanto_Text_JournalEvidence:
	.string "FIELD AIDE: These are clues,\n"
	.string "not confirmed identifications.\p"
	.string "BIRCH and OAK are comparing\n"
	.string "the weather and habitat notes.\p"
	.string "The mimic cry and pink hair\n"
	.string "may belong to another visitor.\p"
	.string "MEW is only a possibility.\n"
	.string "We need direct observations.$"

LegendsKanto_Text_SurveyReport:
	.string "FIELD AIDE: Lightning near\n"
	.string "the plant. Frost at SEAFOAM.\p"
	.string "A third sighting inland...\n"
	.string "Three different habitats.\p"
	.string "OAK thinks ZAPDOS, ARTICUNO\n"
	.string "and MOLTRES may be involved.\p"
	.string "We'll compare KANTO's records\n"
	.string "with BIRCH's weather notes.\p"
	.string "The records mention another\n"
	.string "POKEMON imitating bird cries.\p"
	.string "OAK found a tiny pink hair.\n"
	.string "Could it be the elusive MEW?\p"
	.string "First, we must protect the\n"
	.string "birds' homes and learn more.$"

LegendsKanto_Text_SurveyNext:
	.string "WING SURVEY: First report\n"
	.string "complete. Thank you!\p"
	.string "The next expedition and other\n"
	.string "GYMS are still being prepared.\p"
	.string "Bird and MEW encounters come\n"
	.string "in a later development chapter.$"

LegendsKanto_ROUTE6_Trainer::
	lock
	faceplayer
	checktrainerflag TRAINER_LEGENDS_KANTO_ROUTE6
	goto_if TRUE, LegendsKanto_RouteTrainer_After
	msgbox LegendsKanto_Text_RouteOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_RouteTrainer_Decline
	trainerbattle_single TRAINER_LEGENDS_KANTO_ROUTE6, LegendsKanto_Text_RouteIntro, LegendsKanto_Text_RouteDefeat
	goto LegendsKanto_RouteTrainer_After

LegendsKanto_ROUTE7_Trainer::
	lock
	faceplayer
	checktrainerflag TRAINER_LEGENDS_KANTO_ROUTE7
	goto_if TRUE, LegendsKanto_RouteTrainer_After
	msgbox LegendsKanto_Text_RouteOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_RouteTrainer_Decline
	trainerbattle_single TRAINER_LEGENDS_KANTO_ROUTE7, LegendsKanto_Text_RouteIntro, LegendsKanto_Text_RouteDefeat
	goto LegendsKanto_RouteTrainer_After

LegendsKanto_ROUTE8_Trainer::
	lock
	faceplayer
	checktrainerflag TRAINER_LEGENDS_KANTO_ROUTE8
	goto_if TRUE, LegendsKanto_RouteTrainer_After
	msgbox LegendsKanto_Text_RouteOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_RouteTrainer_Decline
	trainerbattle_single TRAINER_LEGENDS_KANTO_ROUTE8, LegendsKanto_Text_RouteIntro, LegendsKanto_Text_RouteDefeat
	goto LegendsKanto_RouteTrainer_After

LegendsKanto_ROUTE16_Birdwatcher::
	msgbox LegendsKanto_Text_Birdwatcher, MSGBOX_NPC
	end

LegendsKanto_ROUTE17_Trainer::
	lock
	faceplayer
	checktrainerflag TRAINER_LEGENDS_KANTO_ROUTE17
	goto_if TRUE, LegendsKanto_RouteTrainer_After
	msgbox LegendsKanto_Text_RouteOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_RouteTrainer_Decline
	trainerbattle_single TRAINER_LEGENDS_KANTO_ROUTE17, LegendsKanto_Text_RouteIntro, LegendsKanto_Text_RouteDefeat
	goto LegendsKanto_RouteTrainer_After

LegendsKanto_ROUTE18_Birdwatcher::
	msgbox LegendsKanto_Text_Birdwatcher, MSGBOX_NPC
	end

LegendsKanto_RouteTrainer_After::
	msgbox LegendsKanto_Text_RouteAfter, MSGBOX_DEFAULT
LegendsKanto_RouteTrainer_Decline::
	release
	end

LegendsKanto_Text_RouteOffer:
	.string "Training for the KANTO GYMS?\n"
	.string "Let's have a practice battle!$"
LegendsKanto_Text_RouteIntro:
	.string "There's always more to learn!$"
LegendsKanto_Text_RouteDefeat:
	.string "That's a CHAMPION's skill!$"
LegendsKanto_Text_RouteAfter:
	.string "Pick the GYM team that suits\n"
	.string "you. Both choices count.$"

LegendsKanto_Text_Birdwatcher:
	.string "A bright wing crossed these\n"
	.string "hills. It was gone in a flash.\p"
	.string "KOGA has heard the reports.\n"
	.string "Could it be a migrating bird?$"
