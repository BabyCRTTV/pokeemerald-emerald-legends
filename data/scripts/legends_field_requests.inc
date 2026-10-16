@ Birch keeps native registration/gifts/story events ahead of optional work.
@ All menus close the dialogue first, so seven request rows cannot overlap it.
LegendsFieldRequests_Talk::
	msgbox LegendsFieldRequests_Text_Greeting, MSGBOX_DEFAULT
	closemessage
	multichoice 1, 1, MULTI_LEGENDS_BIRCH_MAIN, FALSE
	switch VAR_RESULT
	case 0, LegendsFieldRequests_Work
	case 1, ProfBirch_EventScript_NativeAskRatePokedex
	goto LegendsFieldRequests_Leave

LegendsFieldRequests_Work:
	special LegendsFieldRequestsGetActive
	goto_if_ne VAR_RESULT, FIELD_REQUEST_NONE, LegendsFieldRequests_Review
	special LegendsFieldRequestsPrepareMenu
	closemessage
	multichoice 1, 1, MULTI_LEGENDS_BIRCH_REQUESTS, FALSE
	goto_if_ge VAR_RESULT, LEGENDS_FIELD_REQUEST_COUNT, LegendsFieldRequests_Talk
	copyvar VAR_0x8004, VAR_RESULT
	special LegendsFieldRequestsDescribe
	goto_if_eq VAR_RESULT, TRUE, LegendsFieldRequests_AlreadyFinished
	msgbox gStringVar4, MSGBOX_DEFAULT
	msgbox LegendsFieldRequests_Text_Accept, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsFieldRequests_Work
	special LegendsFieldRequestsAcceptSpecial
	goto_if_ne VAR_RESULT, FIELD_REQUEST_OK, LegendsFieldRequests_Work
	msgbox LegendsFieldRequests_Text_Accepted, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Leave

LegendsFieldRequests_AlreadyFinished:
	msgbox gStringVar4, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Work

LegendsFieldRequests_Review:
	special LegendsFieldRequestsReview
	msgbox gStringVar4, MSGBOX_DEFAULT
	closemessage
	multichoice 1, 1, MULTI_LEGENDS_BIRCH_ACTIVE, FALSE
	switch VAR_RESULT
	case 0, LegendsFieldRequests_Submit
	case 1, LegendsFieldRequests_AskAbandon
	goto LegendsFieldRequests_Talk

LegendsFieldRequests_Submit:
	special LegendsFieldRequestsSubmitSpecial
	goto_if_eq VAR_RESULT, FIELD_REQUEST_NOT_READY, LegendsFieldRequests_NotReady
	goto_if_eq VAR_RESULT, FIELD_REQUEST_STORAGE_FULL, LegendsFieldRequests_Full
	goto_if_ne VAR_RESULT, FIELD_REQUEST_OK, LegendsFieldRequests_Work
	msgbox gStringVar4, MSGBOX_DEFAULT
	msgbox LegendsFieldRequests_Text_Reward, MSGBOX_DEFAULT
	msgbox LegendsFieldRequests_Text_Finished, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Talk

LegendsFieldRequests_NotReady:
	msgbox LegendsFieldRequests_Text_NotReady, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Talk

LegendsFieldRequests_Full:
	msgbox LegendsFieldRequests_Text_Full, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Talk

LegendsFieldRequests_AskAbandon:
	msgbox LegendsFieldRequests_Text_AskAbandon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsFieldRequests_Talk
	special LegendsFieldRequestsAbandonSpecial
	msgbox LegendsFieldRequests_Text_Abandoned, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Talk

LegendsFieldRequests_Leave:
	release
	end

LegendsFieldRequests_Text_Invitation:
	.string "PROF. BIRCH: The GYM challenge isn't\n"
	.string "the only way to explore HOENN.\p"
	.string "If you'd like some other work,\n"
	.string "come and check in with me!\p"
	.string "You can choose a field request\n"
	.string "and help with my research.$"

LegendsFieldRequests_Text_Greeting:
	.string "BIRCH: Good to see you!\n"
	.string "What would you like to work on?\p"
	.string "I have field requests if you'd like\n"
	.string "a change from the GYM challenge.$"

LegendsFieldRequests_Text_Accept:
	.string "Take this field request?\p"
	.string "You can work on one at a time,\n"
	.string "or speak to me to abandon it.$"

LegendsFieldRequests_Text_Accepted:
	.string "BIRCH: Wonderful! I've added it to\n"
	.string "the SIDE page of your QUEST LOG.\p"
	.string "Come back when you're ready.\n"
	.string "There's no time limit!$"

LegendsFieldRequests_Text_NotReady:
	.string "BIRCH: We still need a little more\n"
	.string "information for this report.\p"
	.string "Check the request in your QUEST LOG,\n"
	.string "then come back when you're ready.$"

LegendsFieldRequests_Text_Full:
	.string "BIRCH: Your PC's ITEM STORAGE\n"
	.string "doesn't have room for the reward.\p"
	.string "I'll hold the report for you.\n"
	.string "No samples have been taken.$"

LegendsFieldRequests_Text_Reward:
	.string "Sent to PC ITEM STORAGE:\n"
	.string "{STR_VAR_1}!$"

LegendsFieldRequests_Text_Finished:
	.string "BIRCH: That request is complete!\p"
	.string "You're welcome to choose another\n"
	.string "whenever you're ready.$"

LegendsFieldRequests_Text_AskAbandon:
	.string "Abandon your current field request?\p"
	.string "It will be available to choose again.\n"
	.string "No reward or samples will change.$"

LegendsFieldRequests_Text_Abandoned:
	.string "BIRCH: All right. I've put it back\n"
	.string "on the list for another time.\p"
	.string "You can try it again later,\n"
	.string "or choose something different.$"
