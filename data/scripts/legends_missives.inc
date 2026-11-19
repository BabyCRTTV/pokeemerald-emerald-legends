Missive_Board::
	lockall
	msgbox Missive_Text_Header, MSGBOX_DEFAULT
Missive_List:
	closemessage
	special MissiveList
	goto_if_eq VAR_RESULT, FALSE, Missive_Leave
	multichoice 1, 1, MULTI_LEGENDS_MISSIVES, FALSE
	goto_if_eq VAR_RESULT, 2, Missive_Sighting
	goto_if_ge VAR_RESULT, 3, Missive_Leave
	copyvar VAR_0x8004, VAR_RESULT
	special MissiveRead
	copyvar VAR_0x8005, VAR_RESULT
	msgbox gStringVar4, MSGBOX_DEFAULT
	goto_if_eq VAR_0x8005, 2, Missive_Filled
	goto_if_eq VAR_0x8005, 1, Missive_Taken
	msgbox Missive_Text_Accept, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Missive_List
	special MissiveAccept
	msgbox Missive_Text_Recorded, MSGBOX_DEFAULT
	goto Missive_List
Missive_Taken:
	msgbox Missive_Text_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Missive_List
	special MissiveReturn
	msgbox Missive_Text_Returned, MSGBOX_DEFAULT
	goto Missive_List
Missive_Filled:
	msgbox Missive_Text_Filled, MSGBOX_DEFAULT
	goto Missive_List
Missive_Sighting:
	special MissiveRumor
	msgbox gStringVar4, MSGBOX_DEFAULT
	goto Missive_List
Missive_Leave:
	releaseall
	end

Missive_Recipient::
	lock
	faceplayer
	special MissivePrepareDelivery
	copyvar VAR_0x8005, VAR_RESULT
	msgbox gStringVar4, MSGBOX_DEFAULT
	goto_if_eq VAR_0x8005, FALSE, Missive_EndTalk
	msgbox Missive_Text_TurnIn, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Missive_EndTalk
	special MissiveSettle
	goto_if_eq VAR_RESULT, FALSE, Missive_NoRoom
	msgbox gStringVar4, MSGBOX_DEFAULT
	playfanfare MUS_OBTAIN_ITEM
	msgbox Missive_Text_Paid, MSGBOX_DEFAULT
	waitfanfare
	goto Missive_EndTalk
Missive_NoRoom:
	msgbox Missive_Text_NoRoom, MSGBOX_DEFAULT
Missive_EndTalk:
	release
	end

Missive_Text_Header:
	.string "Local notices are pinned here.$"
Missive_Text_Accept:
	.string "Take this job?$"
Missive_Text_Recorded:
	.string "You copied the notice into your\nQUEST LOG.$"
Missive_Text_Return:
	.string "You've taken this job.\nPut it back on the board?$"
Missive_Text_Returned:
	.string "The notice is open again.$"
Missive_Text_Filled:
	.string "Someone stamped it: PAID IN FULL.$"
Missive_Text_TurnIn:
	.string "Turn in this request?$"
Missive_Text_Paid:
	.string "Reward sent to your PC:\n{STR_VAR_1} {STR_VAR_2}.$"
Missive_Text_NoRoom:
	.string "Your PC item storage is full.\nMake room and come back.$"
