@ Called only from Mom's ordinary conversation branches, after native gifts.
LegendsHomecoming_Mom:
	special LegendsHomecomingReady
	call_if_eq VAR_RESULT, TRUE, LegendsHomecoming_Family
	special LegendsHomecomingMomMessage
	call_if_eq VAR_RESULT, TRUE, LegendsHomecoming_MomWords
	return

LegendsHomecoming_MomWords:
	msgbox gStringVar4, MSGBOX_DEFAULT
	special LegendsHomecomingRememberMom
	return

LegendsHomecoming_Dad:
	special LegendsHomecomingDadMessage
	call_if_eq VAR_RESULT, TRUE, LegendsHomecoming_DadWords
	return

LegendsHomecoming_DadWords:
	msgbox gStringVar4, MSGBOX_DEFAULT
	special LegendsHomecomingRememberDad
	return

@ Reuse the original Norman object at the family table in either house.
@ Keep the player in place; no forced paths can collide with their follower.
LegendsHomecoming_Family:
	closemessage
	fadescreen FADE_TO_BLACK
	setvar VAR_0x8004, LOCALID_PLAYERS_HOUSE_1F_DAD
	special LegendsHomecomingShowDad
	goto_if_eq VAR_RESULT, FALSE, LegendsHomecoming_NoDad
	applymovement LOCALID_PLAYERS_HOUSE_1F_DAD, Common_Movement_FacePlayer
	waitmovement 0
	fadescreen FADE_FROM_BLACK
	msgbox LegendsHomecoming_Text_MomWelcome, MSGBOX_DEFAULT
	msgbox LegendsHomecoming_Text_DadWelcome, MSGBOX_DEFAULT
	msgbox LegendsHomecoming_Text_MomTea, MSGBOX_DEFAULT
	msgbox LegendsHomecoming_Text_DadStay, MSGBOX_DEFAULT
	msgbox LegendsHomecoming_Text_MomHome, MSGBOX_DEFAULT
	closemessage
	special LegendsHomecomingFinish
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_PLAYERS_HOUSE_1F_DAD
	fadescreen FADE_FROM_BLACK
	return

@ If the native object/sprite pool is full, keep the welcome pending.
LegendsHomecoming_NoDad:
	fadescreen FADE_FROM_BLACK
	return

LegendsHomecoming_Text_MomWelcome:
	.string "MOM: Look who's home!\n"
	.string "Your dad managed to get away too.\p"
	.string "I thought we could have a little\n"
	.string "time together.$"

LegendsHomecoming_Text_DadWelcome:
	.string "DAD: BIRCH told us you'd finished\n"
	.string "your work. Congratulations.\p"
	.string "I've been trying to follow it all\n"
	.string "on the map at the GYM.$"

LegendsHomecoming_Text_MomTea:
	.string "MOM: He brought it home last night.\n"
	.string "It covered half the table!\p"
	.string "Now, tell us about that island.\n"
	.string "What was it like?$"

LegendsHomecoming_Text_DadStay:
	.string "DAD: …An island that quiet…\n"
	.string "I'd like to see it someday.\p"
	.string "I should get back to the GYM soon.\n"
	.string "I'm glad I caught you at home.$"

LegendsHomecoming_Text_MomHome:
	.string "MOM: We'll have plenty to talk about\n"
	.string "the next time you're here.\p"
	.string "For now, take a little rest.\n"
	.string "It's good to have you home.$"
