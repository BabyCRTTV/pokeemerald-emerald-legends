@ Northern and volcanic visiting Gyms. Native one-win contract.


LegendsKanto_Brock_Entry::
	lockall
	setvar VAR_TEMP_0, 1
	goto_if_set FLAG_LEGENDS_KANTO_BROCK_WON, LegendsKanto_Brock_Completed
	msgbox LegendsKanto_Text_OneWin, MSGBOX_DEFAULT
	msgbox LegendsKanto_Brock_Text_Mode, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LegendsKanto_Brock_Champion
	setflag FLAG_LEGENDS_STORY_BROCK_MODE_SET
	clearflag FLAG_LEGENDS_STORY_BROCK_CHAMPION
	msgbox LegendsKanto_Text_StandardChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Brock_Champion::
	setflag FLAG_LEGENDS_STORY_BROCK_MODE_SET
	setflag FLAG_LEGENDS_STORY_BROCK_CHAMPION
	msgbox LegendsKanto_Text_ChampionChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Brock_Completed::
	msgbox LegendsKanto_Text_GymCompleted, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Brock_Leader::
	lockall
	faceplayer
	goto_if_set FLAG_LEGENDS_KANTO_BROCK_WON, LegendsKanto_Brock_AfterWin
	goto_if_unset FLAG_LEGENDS_STORY_BROCK_MODE_SET, LegendsKanto_Brock_Entry
	msgbox LegendsKanto_Brock_Text_Confirm, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	goto_if_set FLAG_LEGENDS_STORY_BROCK_CHAMPION, LegendsKanto_Brock_BattleChampion
	trainerbattle_single TRAINER_LEGENDS_KANTO_BROCK_STANDARD, LegendsKanto_Brock_Text_Intro, LegendsKanto_Brock_Text_Defeat
	goto LegendsKanto_Brock_Won

LegendsKanto_Brock_BattleChampion::
	trainerbattle_single TRAINER_LEGENDS_KANTO_BROCK_CHAMPION, LegendsKanto_Brock_Text_Intro, LegendsKanto_Brock_Text_Defeat

LegendsKanto_Brock_Won::
	setflag FLAG_LEGENDS_KANTO_BROCK_WON
	playfanfare MUS_OBTAIN_BADGE
	waitfanfare
	msgbox LegendsKanto_Text_VictoryRecorded, MSGBOX_DEFAULT
LegendsKanto_Brock_AfterWin::
	msgbox LegendsKanto_Brock_Text_Clue, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Brock_Text_Mode:
	.string "BROCK: Champion challenge? YES: Lv.\n"
	.string "70-74, six POKEMON. NO: Standard Lv.\p"
	.string "50-54, four POKEMON.$"

LegendsKanto_Brock_Text_Confirm:
	.string "Challenge BROCK? You may change\n"
	.string "difficulty with the entrance guide\p"
	.string "until your one victory is recorded.$"

LegendsKanto_Brock_Text_Intro:
	.string "I study what holds a landscape\n"
	.string "together. Show me what your HOENN\p"
	.string "journey has taught you!$"

LegendsKanto_Brock_Text_Defeat:
	.string "Solid judgment. You have earned this\n"
	.string "visiting record.$"

LegendsKanto_Brock_Text_Clue:
	.string "The rockfalls near MT. MOON are old. A\n"
	.string "smaller visitor crossed fresh dust\p"
	.string "without shifting the stones. Compare\n"
	.string "them with our researcher outside the\p"
	.string "western entrance.$"



LegendsKanto_Misty_Entry::
	lockall
	setvar VAR_TEMP_0, 1
	goto_if_set FLAG_LEGENDS_KANTO_MISTY_WON, LegendsKanto_Misty_Completed
	msgbox LegendsKanto_Text_OneWin, MSGBOX_DEFAULT
	msgbox LegendsKanto_Misty_Text_Mode, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LegendsKanto_Misty_Champion
	setflag FLAG_LEGENDS_STORY_MISTY_MODE_SET
	clearflag FLAG_LEGENDS_STORY_MISTY_CHAMPION
	msgbox LegendsKanto_Text_StandardChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Misty_Champion::
	setflag FLAG_LEGENDS_STORY_MISTY_MODE_SET
	setflag FLAG_LEGENDS_STORY_MISTY_CHAMPION
	msgbox LegendsKanto_Text_ChampionChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Misty_Completed::
	msgbox LegendsKanto_Text_GymCompleted, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Misty_Leader::
	lockall
	faceplayer
	goto_if_set FLAG_LEGENDS_KANTO_MISTY_WON, LegendsKanto_Misty_AfterWin
	goto_if_unset FLAG_LEGENDS_STORY_MISTY_MODE_SET, LegendsKanto_Misty_Entry
	msgbox LegendsKanto_Misty_Text_Confirm, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	goto_if_set FLAG_LEGENDS_STORY_MISTY_CHAMPION, LegendsKanto_Misty_BattleChampion
	trainerbattle_single TRAINER_LEGENDS_KANTO_MISTY_STANDARD, LegendsKanto_Misty_Text_Intro, LegendsKanto_Misty_Text_Defeat
	goto LegendsKanto_Misty_Won

LegendsKanto_Misty_BattleChampion::
	trainerbattle_single TRAINER_LEGENDS_KANTO_MISTY_CHAMPION, LegendsKanto_Misty_Text_Intro, LegendsKanto_Misty_Text_Defeat

LegendsKanto_Misty_Won::
	setflag FLAG_LEGENDS_KANTO_MISTY_WON
	playfanfare MUS_OBTAIN_BADGE
	waitfanfare
	msgbox LegendsKanto_Text_VictoryRecorded, MSGBOX_DEFAULT
LegendsKanto_Misty_AfterWin::
	msgbox LegendsKanto_Misty_Text_Clue, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Misty_Text_Mode:
	.string "MISTY: Champion challenge? YES: Lv.\n"
	.string "72-76, six POKEMON. NO: Standard Lv.\p"
	.string "52-56, four POKEMON.$"

LegendsKanto_Misty_Text_Confirm:
	.string "Challenge MISTY? You may change\n"
	.string "difficulty with the entrance guide\p"
	.string "until your one victory is recorded.$"

LegendsKanto_Misty_Text_Intro:
	.string "Every current has its own rhythm.\n"
	.string "Let's see how your team handles mine!$"

LegendsKanto_Misty_Text_Defeat:
	.string "You kept your footing. That was a\n"
	.string "wonderful battle!$"

LegendsKanto_Misty_Text_Clue:
	.string "SEAFOAM's current changed, but this\n"
	.string "river did not. Our researcher is by the\p"
	.string "northwest water in CERULEAN. A copied\n"
	.string "cry alone does not mean the weather\p"
	.string "changed.$"



LegendsKanto_Blaine_Entry::
	lockall
	setvar VAR_TEMP_0, 1
	goto_if_set FLAG_LEGENDS_KANTO_BLAINE_WON, LegendsKanto_Blaine_Completed
	msgbox LegendsKanto_Text_OneWin, MSGBOX_DEFAULT
	msgbox LegendsKanto_Blaine_Text_Mode, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LegendsKanto_Blaine_Champion
	setflag FLAG_LEGENDS_STORY_BLAINE_MODE_SET
	clearflag FLAG_LEGENDS_STORY_BLAINE_CHAMPION
	msgbox LegendsKanto_Text_StandardChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Blaine_Champion::
	setflag FLAG_LEGENDS_STORY_BLAINE_MODE_SET
	setflag FLAG_LEGENDS_STORY_BLAINE_CHAMPION
	msgbox LegendsKanto_Text_ChampionChosen, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Blaine_Completed::
	msgbox LegendsKanto_Text_GymCompleted, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Blaine_Leader::
	lockall
	faceplayer
	goto_if_set FLAG_LEGENDS_KANTO_BLAINE_WON, LegendsKanto_Blaine_AfterWin
	goto_if_unset FLAG_LEGENDS_STORY_BLAINE_MODE_SET, LegendsKanto_Blaine_Entry
	msgbox LegendsKanto_Blaine_Text_Confirm, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_Challenge_Decline
	goto_if_set FLAG_LEGENDS_STORY_BLAINE_CHAMPION, LegendsKanto_Blaine_BattleChampion
	trainerbattle_single TRAINER_LEGENDS_KANTO_BLAINE_STANDARD, LegendsKanto_Blaine_Text_Intro, LegendsKanto_Blaine_Text_Defeat
	goto LegendsKanto_Blaine_Won

LegendsKanto_Blaine_BattleChampion::
	trainerbattle_single TRAINER_LEGENDS_KANTO_BLAINE_CHAMPION, LegendsKanto_Blaine_Text_Intro, LegendsKanto_Blaine_Text_Defeat

LegendsKanto_Blaine_Won::
	setflag FLAG_LEGENDS_KANTO_BLAINE_WON
	playfanfare MUS_OBTAIN_BADGE
	waitfanfare
	msgbox LegendsKanto_Text_VictoryRecorded, MSGBOX_DEFAULT
LegendsKanto_Blaine_AfterWin::
	msgbox LegendsKanto_Blaine_Text_Clue, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Blaine_Text_Mode:
	.string "BLAINE: Champion challenge? YES: Lv.\n"
	.string "80-84, six POKEMON. NO: Standard Lv.\p"
	.string "60-64, four POKEMON.$"

LegendsKanto_Blaine_Text_Confirm:
	.string "Challenge BLAINE? You may change\n"
	.string "difficulty with the entrance guide\p"
	.string "until your one victory is recorded.$"

LegendsKanto_Blaine_Text_Intro:
	.string "A feather can travel farther than a\n"
	.string "flame! First, let me test the heat of\p"
	.string "your team!$"

LegendsKanto_Blaine_Text_Defeat:
	.string "A splendid answer! Your team burns\n"
	.string "brightly.$"

LegendsKanto_Blaine_Text_Clue:
	.string "That feather rode a volcanic updraft.\n"
	.string "MOLTRES has a roost on MT. EMBER. Our\p"
	.string "expedition sailor waits on CINNABAR's\n"
	.string "eastern shore. File the northern\p"
	.string "report first.$"
