@ Wing Survey chapter two: The Borrowed Voice.

LegendsKanto_Erika_Entry::
	lockall
	setvar VAR_TEMP_0, 1
	goto_if_set FLAG_LEGENDS_KANTO_ERIKA_WON, LegendsKanto_Erika_Completed
	msgbox LegendsKanto_Text_OneWin, MSGBOX_DEFAULT
	msgbox LegendsKanto_Erika_Text_Mode, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LegendsKanto_Erika_Champion
	setflag FLAG_LEGENDS_KANTO_ERIKA_MODE_SET
	clearflag FLAG_LEGENDS_KANTO_ERIKA_CHAMPION
	msgbox LegendsKanto_Text_StandardChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Erika_Champion::
	setflag FLAG_LEGENDS_KANTO_ERIKA_MODE_SET
	setflag FLAG_LEGENDS_KANTO_ERIKA_CHAMPION
	msgbox LegendsKanto_Text_ChampionChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Erika_Completed::
	msgbox LegendsKanto_Text_GymCompleted, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Erika_Leader::
	lockall
	faceplayer
	goto_if_set FLAG_LEGENDS_KANTO_ERIKA_WON, LegendsKanto_Erika_AfterWin
	goto_if_unset FLAG_LEGENDS_KANTO_ERIKA_MODE_SET, LegendsKanto_Erika_Entry
	msgbox LegendsKanto_Erika_Text_Confirm, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	goto_if_set FLAG_LEGENDS_KANTO_ERIKA_CHAMPION, LegendsKanto_Erika_BattleChampion
	trainerbattle_single TRAINER_LEGENDS_KANTO_ERIKA_STANDARD, LegendsKanto_Erika_Text_Intro, LegendsKanto_Erika_Text_Defeat
	goto LegendsKanto_Erika_Won

LegendsKanto_Erika_BattleChampion::
	trainerbattle_single TRAINER_LEGENDS_KANTO_ERIKA_CHAMPION, LegendsKanto_Erika_Text_Intro, LegendsKanto_Erika_Text_Defeat

LegendsKanto_Erika_Won::
	setflag FLAG_LEGENDS_KANTO_ERIKA_WON
	playfanfare MUS_OBTAIN_BADGE
	waitfanfare
	msgbox LegendsKanto_Text_VictoryRecorded, MSGBOX_DEFAULT
LegendsKanto_Erika_AfterWin::
	msgbox LegendsKanto_Erika_Text_Clue, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Sabrina_Entry::
	lockall
	setvar VAR_TEMP_0, 1
	goto_if_set FLAG_LEGENDS_KANTO_SABRINA_WON, LegendsKanto_Sabrina_Completed
	msgbox LegendsKanto_Text_OneWin, MSGBOX_DEFAULT
	msgbox LegendsKanto_Sabrina_Text_Mode, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LegendsKanto_Sabrina_Champion
	setflag FLAG_LEGENDS_KANTO_SABRINA_MODE_SET
	clearflag FLAG_LEGENDS_KANTO_SABRINA_CHAMPION
	msgbox LegendsKanto_Text_StandardChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Sabrina_Champion::
	setflag FLAG_LEGENDS_KANTO_SABRINA_MODE_SET
	setflag FLAG_LEGENDS_KANTO_SABRINA_CHAMPION
	msgbox LegendsKanto_Text_ChampionChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Sabrina_Completed::
	msgbox LegendsKanto_Text_GymCompleted, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Sabrina_Leader::
	lockall
	faceplayer
	goto_if_set FLAG_LEGENDS_KANTO_SABRINA_WON, LegendsKanto_Sabrina_AfterWin
	goto_if_unset FLAG_LEGENDS_KANTO_SABRINA_MODE_SET, LegendsKanto_Sabrina_Entry
	msgbox LegendsKanto_Sabrina_Text_Confirm, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	goto_if_set FLAG_LEGENDS_KANTO_SABRINA_CHAMPION, LegendsKanto_Sabrina_BattleChampion
	trainerbattle_single TRAINER_LEGENDS_KANTO_SABRINA_STANDARD, LegendsKanto_Sabrina_Text_Intro, LegendsKanto_Sabrina_Text_Defeat
	goto LegendsKanto_Sabrina_Won

LegendsKanto_Sabrina_BattleChampion::
	trainerbattle_single TRAINER_LEGENDS_KANTO_SABRINA_CHAMPION, LegendsKanto_Sabrina_Text_Intro, LegendsKanto_Sabrina_Text_Defeat

LegendsKanto_Sabrina_Won::
	setflag FLAG_LEGENDS_KANTO_SABRINA_WON
	playfanfare MUS_OBTAIN_BADGE
	waitfanfare
	msgbox LegendsKanto_Text_VictoryRecorded, MSGBOX_DEFAULT
LegendsKanto_Sabrina_AfterWin::
	msgbox LegendsKanto_Sabrina_Text_Clue, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Erika_Text_Mode:
	.string "Standard team: Lv. 54-58.\n"
	.string "Champion team: Lv. 74-78.\p"
	.string "Take the Champion challenge?\n"
	.string "YES: Champion. NO: Standard.$"
LegendsKanto_Erika_Text_Confirm:
	.string "ERIKA: Shall we begin?\n"
	.string "One victory completes my GYM.$"
LegendsKanto_Erika_Text_Intro:
	.string "ERIKA: A patient gardener\n"
	.string "knows when to take action.$"
LegendsKanto_Erika_Text_Defeat:
	.string "Your care shines through.$"
LegendsKanto_Erika_Text_Clue:
	.string "ERIKA: Leaves fell after the\n"
	.string "bright wing crossed ROUTE 16.\p"
	.string "But fallen leaves alone do\n"
	.string "not prove there was a fire.\p"
	.string "Our birdwatcher kept a sample.\n"
	.string "Find him beside the road.\p"
	.string "After OAK's first report,\n"
	.string "help him examine the leaves.$"
LegendsKanto_Erika_Staff::
	msgbox LegendsKanto_Erika_Text_Staff, MSGBOX_NPC
	end
LegendsKanto_Erika_Text_Staff:
	.string "ERIKA is beyond the garden.\n"
	.string "Use CUT on the small tree.\p"
	.string "The GYM GUIDE can change your\n"
	.string "team choice before you win.$"
LegendsKanto_Sabrina_Text_Mode:
	.string "Standard team: Lv. 58-62.\n"
	.string "Champion team: Lv. 78-82.\p"
	.string "Take the Champion challenge?\n"
	.string "YES: Champion. NO: Standard.$"
LegendsKanto_Sabrina_Text_Confirm:
	.string "SABRINA: Have you decided?\n"
	.string "One victory completes my GYM.$"
LegendsKanto_Sabrina_Text_Intro:
	.string "SABRINA: A clear mind sees\n"
	.string "beyond the first impression.$"
LegendsKanto_Sabrina_Text_Defeat:
	.string "You trusted your POKEMON.$"
LegendsKanto_Sabrina_Text_Clue:
	.string "SABRINA: Something curious\n"
	.string "is following the bird calls.\p"
	.string "Not angry. Not frightened.\n"
	.string "It seems to be learning.\p"
	.string "A researcher on ROUTE 8\n"
	.string "heard two calls from one bush.\p"
	.string "After OAK's first report,\n"
	.string "listen with the researcher.\p"
	.string "A feeling is not evidence.\n"
	.string "Record what you hear.$"
LegendsKanto_Sabrina_Staff::
	msgbox LegendsKanto_Sabrina_Text_Staff, MSGBOX_NPC
	end
LegendsKanto_Sabrina_Text_Staff:
	.string "The pads link nine rooms.\n"
	.string "SABRINA waits in the center.\p"
	.string "To reach her, use the pads:\n"
	.string "entry, top left, bottom left,\p"
	.string "then bottom left once more.\n"
	.string "Retrace those pads to return.\p"
	.string "The GUIDE can change your\n"
	.string "team choice before victory.$"

LegendsKanto_Chapter2_Journal::
	msgbox LegendsKanto_Text_Chapter2Intro, MSGBOX_DEFAULT
	goto_if_set FLAG_LEGENDS_KANTO_ERIKA_WON, LegendsKanto_Chapter2_CheckSabrina
	msgbox LegendsKanto_Text_NeedErika, MSGBOX_DEFAULT
LegendsKanto_Chapter2_CheckSabrina::
	goto_if_set FLAG_LEGENDS_KANTO_SABRINA_WON, LegendsKanto_Chapter2_CheckLeaves
	msgbox LegendsKanto_Text_NeedSabrina, MSGBOX_DEFAULT
LegendsKanto_Chapter2_CheckLeaves::
	goto_if_unset FLAG_LEGENDS_KANTO_ERIKA_WON, LegendsKanto_Chapter2_CheckEcho
	goto_if_set FLAG_LEGENDS_KANTO_SURVEY_LEAVES, LegendsKanto_Chapter2_CheckEcho
	msgbox LegendsKanto_Text_NeedLeaves, MSGBOX_DEFAULT
LegendsKanto_Chapter2_CheckEcho::
	goto_if_unset FLAG_LEGENDS_KANTO_SABRINA_WON, LegendsKanto_Chapter2_Finish
	goto_if_set FLAG_LEGENDS_KANTO_SURVEY_ECHO, LegendsKanto_Chapter2_Finish
	msgbox LegendsKanto_Text_NeedEcho, MSGBOX_DEFAULT
LegendsKanto_Chapter2_Finish::
	goto_if_unset FLAG_LEGENDS_KANTO_ERIKA_WON, LegendsKanto_Chapter2_Return
	goto_if_unset FLAG_LEGENDS_KANTO_SABRINA_WON, LegendsKanto_Chapter2_Return
	goto_if_unset FLAG_LEGENDS_KANTO_SURVEY_LEAVES, LegendsKanto_Chapter2_Return
	goto_if_unset FLAG_LEGENDS_KANTO_SURVEY_ECHO, LegendsKanto_Chapter2_Return
	goto_if_set FLAG_LEGENDS_KANTO_SURVEY_FIELD_REPORT, LegendsKanto_Chapter2_Filed
	msgbox LegendsKanto_Text_Chapter2Report, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_KANTO_SURVEY_FIELD_REPORT
LegendsKanto_Chapter2_Filed::
	msgbox LegendsKanto_Text_Chapter2Next, MSGBOX_DEFAULT
LegendsKanto_Chapter2_Return::
	releaseall
	end

LegendsKanto_Chapter2_Leaves::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_KANTO_SURVEY_REPORT, LegendsKanto_Chapter2_LeavesLocked
	goto_if_unset FLAG_LEGENDS_KANTO_ERIKA_WON, LegendsKanto_Chapter2_LeavesLocked
	goto_if_set FLAG_LEGENDS_KANTO_SURVEY_LEAVES, LegendsKanto_Chapter2_LeavesDone
	msgbox LegendsKanto_Text_LeavesOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	msgbox LegendsKanto_Text_LeavesScene, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_KANTO_SURVEY_LEAVES
LegendsKanto_Chapter2_LeavesDone::
	msgbox LegendsKanto_Text_LeavesRecorded, MSGBOX_DEFAULT
	releaseall
	end
LegendsKanto_Chapter2_LeavesLocked::
	msgbox LegendsKanto_Text_LeavesLocked, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Chapter2_Echo::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_KANTO_SURVEY_REPORT, LegendsKanto_Chapter2_EchoLocked
	goto_if_unset FLAG_LEGENDS_KANTO_SABRINA_WON, LegendsKanto_Chapter2_EchoLocked
	goto_if_set FLAG_LEGENDS_KANTO_SURVEY_ECHO, LegendsKanto_Chapter2_EchoDone
	msgbox LegendsKanto_Text_EchoOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	msgbox LegendsKanto_Text_EchoListen, MSGBOX_DEFAULT
	closemessage
	playcry SPECIES_PIDGEY, CRY_MODE_NORMAL
	waitcry
	delay 30
	playcry SPECIES_PIKACHU, CRY_MODE_NORMAL
	waitcry
	msgbox LegendsKanto_Text_EchoScene, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_KANTO_SURVEY_ECHO
LegendsKanto_Chapter2_EchoDone::
	msgbox LegendsKanto_Text_EchoRecorded, MSGBOX_DEFAULT
	releaseall
	end
LegendsKanto_Chapter2_EchoLocked::
	msgbox LegendsKanto_Text_EchoLocked, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Text_Chapter2Intro:
	.string "WING SURVEY: Borrowed Voice.\n"
	.string "Our next task is fieldwork.\p"
	.string "ERIKA and SABRINA are ready\n"
	.string "in CELADON and SAFFRON.\p"
	.string "Their challenges can be done\n"
	.string "in either mode, in any order.$"
LegendsKanto_Text_NeedErika:
	.string "ERIKA's record: Still needed.\n"
	.string "Visit CELADON's south GYM.$"
LegendsKanto_Text_NeedSabrina:
	.string "SABRINA's record: Needed.\n"
	.string "Visit SAFFRON's northeast GYM.$"
LegendsKanto_Text_NeedLeaves:
	.string "Leaf survey: Still needed.\n"
	.string "Talk to the ROUTE 16 watcher.\p"
	.string "Take CELADON's west road.\n"
	.string "He waits before the gate.$"
LegendsKanto_Text_NeedEcho:
	.string "Call survey: Still needed.\n"
	.string "Talk to the ROUTE 8 researcher.\p"
	.string "Take SAFFRON's east gate.\n"
	.string "Look beside the grass.$"
LegendsKanto_Text_LeavesLocked:
	.string "BIRDWATCHER: I'm keeping\n"
	.string "these leaves for ERIKA.\p"
	.string "Win her GYM challenge and\n"
	.string "file OAK's opening report\p"
	.string "at the VERMILION FAN CLUB.\n"
	.string "Then we can examine them.$"
LegendsKanto_Text_LeavesOffer:
	.string "ERIKA sent you? Help me\n"
	.string "examine the fallen leaves?$"
LegendsKanto_Text_LeavesScene:
	.string "You turn a leaf toward\n"
	.string "the light. Its edge is intact.\p"
	.string "BIRDWATCHER: No scorch marks.\n"
	.string "A warm gust shook them loose.\p"
	.string "I saw a bright wing high up,\n"
	.string "but no fire touched the trees.\p"
	.string "Then something small copied\n"
	.string "its cry from the branches.\p"
	.string "You record the wind and\n"
	.string "leave the habitat undisturbed.$"
LegendsKanto_Text_LeavesRecorded:
	.string "Leaf observation recorded.\n"
	.string "Bring it to OAK's field aide\p"
	.string "at the VERMILION FAN CLUB.\n"
	.string "The sample stays here.$"
LegendsKanto_Text_EchoLocked:
	.string "RESEARCHER: A strange call\n"
	.string "came from this patch of grass.\p"
	.string "Win SABRINA's GYM challenge\n"
	.string "and file the opening report\p"
	.string "at the VERMILION FAN CLUB.\n"
	.string "Then help me listen.$"
LegendsKanto_Text_EchoOffer:
	.string "SABRINA asked you to listen?\n"
	.string "Shall we stand quietly?$"
LegendsKanto_Text_EchoListen:
	.string "You and the researcher wait.\n"
	.string "The grass rustles...$"
LegendsKanto_Text_EchoScene:
	.string "Two different cries come\n"
	.string "from the same hiding place.\p"
	.string "RESEARCHER: A flock, perhaps?\n"
	.string "Or one very good imitator?\p"
	.string "Something brushes the leaves\n"
	.string "above you, then falls silent.\p"
	.string "You record both calls.\n"
	.string "You cannot identify the source.$"
LegendsKanto_Text_EchoRecorded:
	.string "Call observation recorded.\n"
	.string "Bring it to OAK's field aide\p"
	.string "at the VERMILION FAN CLUB.$"
LegendsKanto_Text_Chapter2Report:
	.string "FIELD AIDE: Four GYM records\n"
	.string "and two field observations!\p"
	.string "The trees were not burned.\n"
	.string "The bright bird passed above.\p"
	.string "The copied calls came from\n"
	.string "a different, smaller visitor.\p"
	.string "BIRCH agrees: We should not\n"
	.string "blame birds for every change.\p"
	.string "OAK will compare the calls\n"
	.string "with his rare POKEMON records.\p"
	.string "MEW is still only a theory.\n"
	.string "Your notes give us a lead.$"
LegendsKanto_Text_Chapter2Next:
	.string "Borrowed Voice report: Filed.\n"
	.string "All four current GYMS complete.\p"
	.string "The next survey heads north\n"
	.string "toward the POWER PLANT.\p"
	.string "That journey and the remaining\n"
	.string "GYMS open in a later chapter.\p"
	.string "Keep exploring KANTO or take\n"
	.string "the ferry home to HOENN.$"
LegendsKanto_Chapter2_CeladonLocal::
	msgbox LegendsKanto_Text_CeladonLocal, MSGBOX_NPC
	end
LegendsKanto_Text_CeladonLocal:
	.string "ERIKA's GYM is in the south.\n"
	.string "Her gardens are worth a visit.\p"
	.string "The west road leads to the\n"
	.string "ROUTE 16 birdwatcher.$"
LegendsKanto_Chapter2_SaffronLocal::
	msgbox LegendsKanto_Text_SaffronLocal, MSGBOX_NPC
	end
LegendsKanto_Text_SaffronLocal:
	.string "SABRINA's GYM is northeast.\n"
	.string "The pads can be confusing.\p"
	.string "Her staff explain a path.\n"
	.string "Ask them if you lose your way.$"
