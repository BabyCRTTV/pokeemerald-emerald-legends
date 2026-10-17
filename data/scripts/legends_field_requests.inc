@ Birch keeps native registration/gifts/story events ahead of optional work.
@ All menus close the dialogue first, so seven request rows cannot overlap it.
LegendsFieldRequests_Talk::
	special LegendsFieldRequestsBeginBirch
	goto LegendsFieldRequests_Root

LegendsDevonRequests_Talk::
	special LegendsFieldRequestsBeginDevon

LegendsFieldRequests_Root:
	special LegendsFieldRequestsGreeting
	msgbox gStringVar4, MSGBOX_DEFAULT
	closemessage
	special LegendsFieldRequestsGetPatron
	goto_if_eq VAR_RESULT, FIELD_PATRON_DEVON, LegendsFieldRequests_DevonMain
	multichoice 1, 1, MULTI_LEGENDS_BIRCH_MAIN, FALSE
	switch VAR_RESULT
	case 0, LegendsFieldRequests_Work
	case 1, ProfBirch_EventScript_NativeAskRatePokedex
	case 2, LegendsFieldRequests_ResearchNotes
	goto LegendsFieldRequests_Leave

LegendsFieldRequests_DevonMain:
	multichoice 1, 1, MULTI_LEGENDS_DEVON_MAIN, FALSE
	switch VAR_RESULT
	case 0, LegendsFieldRequests_Work
	case 1, RustboroCity_DevonCorp_3F_EventScript_NativeBusiness
	case 2, LegendsFieldRequests_ResearchNotes
	goto LegendsFieldRequests_Leave

@ Research notes reflect signed completion bits; never accept, claim or save.
LegendsFieldRequests_ResearchNotes:
	special LegendsFieldRequestsGetPatron
	goto_if_eq VAR_RESULT, FIELD_PATRON_DEVON, LegendsFieldRequests_DevonNotes
	special LegendsFieldRequestsResearchNotes
	goto_if_eq VAR_RESULT, 3, LegendsFieldRequests_BirchNotesFinal
	goto_if_eq VAR_RESULT, 2, LegendsFieldRequests_BirchNotesAdvanced
	goto_if_eq VAR_RESULT, 1, LegendsFieldRequests_BirchNotesEarly
	msgbox LegendsFieldRequests_Text_BirchNotesNone, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_BirchNotesEarly:
	msgbox LegendsFieldRequests_Text_BirchNotesEarly, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_BirchNotesAdvanced:
	msgbox LegendsFieldRequests_Text_BirchNotesAdvanced, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_BirchNotesFinal:
	msgbox LegendsFieldRequests_Text_BirchNotesFinal, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_DevonNotes:
	special LegendsFieldRequestsResearchNotes
	goto_if_eq VAR_RESULT, 3, LegendsFieldRequests_DevonNotesFinal
	goto_if_eq VAR_RESULT, 2, LegendsFieldRequests_DevonNotesAdvanced
	goto_if_eq VAR_RESULT, 1, LegendsFieldRequests_DevonNotesEarly
	msgbox LegendsFieldRequests_Text_DevonNotesNone, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_DevonNotesEarly:
	msgbox LegendsFieldRequests_Text_DevonNotesEarly, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_DevonNotesAdvanced:
	msgbox LegendsFieldRequests_Text_DevonNotesAdvanced, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_DevonNotesFinal:
	msgbox LegendsFieldRequests_Text_DevonNotesFinal, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_Work:
	special LegendsFieldRequestsGetActive
	goto_if_eq VAR_RESULT, FIELD_REQUEST_NONE, LegendsFieldRequests_Groups
	special LegendsFieldRequestsCanReview
	goto_if_eq VAR_RESULT, TRUE, LegendsFieldRequests_Review
	msgbox LegendsFieldRequests_Text_OtherPatron, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_Groups:
	closemessage
	special LegendsFieldRequestsGetPatron
	goto_if_eq VAR_RESULT, FIELD_PATRON_DEVON, LegendsFieldRequests_DevonGroups
	multichoice 1, 1, MULTI_LEGENDS_BIRCH_GROUPS, FALSE
	goto LegendsFieldRequests_GroupSelected

LegendsFieldRequests_DevonGroups:
	multichoice 1, 1, MULTI_LEGENDS_DEVON_GROUPS, FALSE

LegendsFieldRequests_GroupSelected:
	copyvar VAR_0x8004, VAR_RESULT
	special LegendsFieldRequestsSelectGroup
	goto_if_eq VAR_RESULT, FALSE, LegendsFieldRequests_Root

LegendsFieldRequests_List:
	special LegendsFieldRequestsPrepareMenu
	closemessage
	multichoice 1, 1, MULTI_LEGENDS_BIRCH_REQUESTS, FALSE
	goto_if_ge VAR_RESULT, LEGENDS_REQUEST_PAGE_SIZE, LegendsFieldRequests_Groups
	copyvar VAR_0x8004, VAR_RESULT
	special LegendsFieldRequestsSelectRow
	goto_if_eq VAR_RESULT, FALSE, LegendsFieldRequests_Groups
	special LegendsFieldRequestsDescribe
	goto_if_eq VAR_RESULT, TRUE, LegendsFieldRequests_AlreadyFinished
	msgbox gStringVar4, MSGBOX_DEFAULT
	msgbox LegendsFieldRequests_Text_Accept, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsFieldRequests_List
	special LegendsFieldRequestsAcceptSpecial
	goto_if_ne VAR_RESULT, FIELD_REQUEST_OK, LegendsFieldRequests_Work
	msgbox LegendsFieldRequests_Text_Accepted, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Leave

LegendsFieldRequests_AlreadyFinished:
	msgbox gStringVar4, MSGBOX_DEFAULT
	goto LegendsFieldRequests_List

LegendsFieldRequests_Review:
	special LegendsFieldRequestsReview
	msgbox gStringVar4, MSGBOX_DEFAULT
	closemessage
	multichoice 1, 1, MULTI_LEGENDS_BIRCH_ACTIVE, FALSE
	switch VAR_RESULT
	case 0, LegendsFieldRequests_Submit
	case 1, LegendsFieldRequests_AskAbandon
	goto LegendsFieldRequests_Root

LegendsFieldRequests_Submit:
	special LegendsFieldRequestsSubmitSpecial
	goto_if_eq VAR_RESULT, FIELD_REQUEST_NOT_READY, LegendsFieldRequests_NotReady
	goto_if_eq VAR_RESULT, FIELD_REQUEST_STORAGE_FULL, LegendsFieldRequests_Full
	goto_if_ne VAR_RESULT, FIELD_REQUEST_OK, LegendsFieldRequests_Work
	msgbox gStringVar4, MSGBOX_DEFAULT
	msgbox LegendsFieldRequests_Text_Reward, MSGBOX_DEFAULT
	msgbox LegendsFieldRequests_Text_Finished, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_NotReady:
	msgbox LegendsFieldRequests_Text_NotReady, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_Full:
	msgbox LegendsFieldRequests_Text_Full, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_AskAbandon:
	msgbox LegendsFieldRequests_Text_AskAbandon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsFieldRequests_Talk
	special LegendsFieldRequestsAbandonSpecial
	msgbox LegendsFieldRequests_Text_Abandoned, MSGBOX_DEFAULT
	goto LegendsFieldRequests_Root

LegendsFieldRequests_Leave:
	release
	end

LegendsFieldRequests_Text_BirchNotesNone:
	.string "BIRCH: A good field notebook\\n"
	.string "starts with an empty page.\\p"
	.string "The small things you notice\\n"
	.string "may answer the big questions.$"

LegendsFieldRequests_Text_BirchNotesEarly:
	.string "BIRCH: Those first reports tell\\n"
	.string "us something important.\\p"
	.string "POKéMON share their homes with\\n"
	.string "one another, and with people.\\p"
	.string "Even familiar paths are worth\\n"
	.string "another look.$"

LegendsFieldRequests_Text_BirchNotesAdvanced:
	.string "BIRCH: Your notes now span\\n"
	.string "forests, shores and highlands!\\p"
	.string "I can compare how POKéMON\\n"
	.string "adapt to very different places.\\p"
	.string "That's real field research.$"

LegendsFieldRequests_Text_BirchNotesFinal:
	.string "BIRCH: The HOENN FIELD ATLAS\\n"
	.string "is more than a list of species.\\p"
	.string "Your observations show how\\n"
	.string "every habitat fits together.\\p"
	.string "You should be proud of this.$"

LegendsFieldRequests_Text_DevonNotesNone:
	.string "MR. STONE: A good invention\\n"
	.string "begins with a good question.\\p"
	.string "Our engineers need honest\\n"
	.string "field reports, not guesses.$"

LegendsFieldRequests_Text_DevonNotesEarly:
	.string "MR. STONE: Your first contracts\\n"
	.string "helped us test real conditions.\\p"
	.string "A design on paper can look\\n"
	.string "perfect until it leaves the lab.$"

LegendsFieldRequests_Text_DevonNotesAdvanced:
	.string "MR. STONE: From tunnels to\\n"
	.string "stormy routes, your findings\\l"
	.string "have reached every department.\\p"
	.string "DEVON must build for the world\\n"
	.string "as it truly is.$"

LegendsFieldRequests_Text_DevonNotesFinal:
	.string "MR. STONE: Our master project\\n"
	.string "would not exist without you.\\p"
	.string "Different POKéMON working\\n"
	.string "together inspired its design.\\p"
	.string "No contract can measure\\n"
	.string "what that means to DEVON.$"

LegendsFieldRequests_Text_Invitation:
	.string "PROF. BIRCH: The GYM challenge isn't\n"
	.string "the only way to explore HOENN.\p"
	.string "If you'd like some other work,\n"
	.string "come and check in with me!\p"
	.string "You can choose a field request\n"
	.string "and help with my research.\p"
	.string "New studies open as you travel.\n"
	.string "Choose what interests you!$"

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
	.string "{STR_VAR_2}: I've added it to\n"
	.string "the SIDE page of your QUEST LOG.\p"
	.string "Come back when you're ready.\n"
	.string "There's no time limit!$"

LegendsFieldRequests_Text_NotReady:
	.string "{STR_VAR_2}: We need a little more\n"
	.string "information for this report.\p"
	.string "Check the request in your QUEST LOG,\n"
	.string "then come back when you're ready.$"

LegendsFieldRequests_Text_Full:
	.string "{STR_VAR_2}: Your PC ITEM STORAGE\n"
	.string "doesn't have room for the reward.\p"
	.string "I'll hold the report for you.\n"
	.string "No samples have been taken.$"

LegendsFieldRequests_Text_Reward:
	.string "Sent to PC ITEM STORAGE:\n"
	.string "{STR_VAR_1}!$"

LegendsFieldRequests_Text_Finished:
	.string "{STR_VAR_2}: Request complete!\p"
	.string "You're welcome to choose another\n"
	.string "whenever you're ready.$"

LegendsFieldRequests_Text_AskAbandon:
	.string "Abandon your current field request?\p"
	.string "It will be available to choose again.\n"
	.string "No reward or samples will change.$"

LegendsFieldRequests_Text_Abandoned:
	.string "{STR_VAR_2}: I've put it back\n"
	.string "on the list for another time.\p"
	.string "You can try it again later,\n"
	.string "or choose something different.$"

LegendsFieldRequests_Text_OtherPatron:
	.string "You're already helping with another\n"
	.string "BIRCH or DEVON research request.\p"
	.string "Please finish it, or speak to its\n"
	.string "researcher to abandon it first.$"

LegendsFieldRequests_EarlyBirchExplain:
	msgbox LegendsFieldRequests_Text_EarlyBirchExplain, MSGBOX_DEFAULT
	return

LegendsFieldRequests_Text_EarlyBirchOffer:
	.string "BIRCH: You have a good eye for\n"
	.string "POKéMON. I could use that help!\p"
	.string "Would you like to hear about\n"
	.string "my field research?$"

LegendsFieldRequests_Text_EarlyBirchExplain:
	.string "BIRCH: Once you have a POKéDEX,\n"
	.string "check in with me for field requests.\p"
	.string "There are things to learn beyond\n"
	.string "the GYM challenge. No rush, though!\p"
	.string "First, get to know your new partner.\n"
	.string "We'll study more as you explore.$"

LegendsFieldRequests_EarlyDevonExplain:
	msgbox LegendsFieldRequests_Text_EarlyDevonExplain, MSGBOX_DEFAULT
	return

LegendsFieldRequests_Text_EarlyDevonOffer:
	.string "MR. STONE: You know, reliable help\n"
	.string "like yours is hard to find.\p"
	.string "Would you like to hear about\n"
	.string "DEVON's research contracts?$"

LegendsFieldRequests_Text_EarlyDevonExplain:
	.string "MR. STONE: Our engineers need\n"
	.string "reports from traveling TRAINERS.\p"
	.string "Speak to me for optional contracts.\n"
	.string "New work opens as you travel.\p"
	.string "Your LETTER and parcel come first.\n"
	.string "The research can wait for you.$"
