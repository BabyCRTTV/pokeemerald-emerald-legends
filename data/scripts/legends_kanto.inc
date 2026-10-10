@ Legends Kanto chapter: self-contained events, independent of FRLG story flags
@ and Emerald's native S.S. Tidal cruise / event-island state machine.

LegendsKanto_EventScript_Invitation::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, LegendsKanto_EventScript_NotChampion
	checkitem ITEM_INVITE_TICKET
	goto_if_eq VAR_RESULT, TRUE, LegendsKanto_EventScript_InvitationReminder
	msgbox LegendsKanto_Text_Invitation, MSGBOX_DEFAULT
	giveitem ITEM_INVITE_TICKET
	goto_if_eq VAR_RESULT, FALSE, EventScript_BagIsFull
	msgbox LegendsKanto_Text_InvitationReminder, MSGBOX_DEFAULT
	release
	end

LegendsKanto_EventScript_InvitationReminder::
	msgbox LegendsKanto_Text_InvitationReminder, MSGBOX_DEFAULT
	release
	end

LegendsKanto_EventScript_NotChampion::
	msgbox LegendsKanto_Text_NotChampion, MSGBOX_DEFAULT
	release
	end

LegendsKanto_EventScript_OutboundFerry::
	lockall
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, LegendsKanto_EventScript_FerryClosed
	checkitem ITEM_INVITE_TICKET
	goto_if_eq VAR_RESULT, FALSE, LegendsKanto_EventScript_NeedInvitation
	msgbox LegendsKanto_Text_Outbound, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_EventScript_DeclineFerry
	msgbox LegendsKanto_Text_BonVoyage, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	playse SE_SHIP
	delay 60
	warp MAP_LEGENDS_KANTO_HARBOR, 32, 9
	waitstate
	releaseall
	end

LegendsKanto_EventScript_FerryClosed::
	msgbox LegendsKanto_Text_FerryClosed, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_EventScript_NeedInvitation::
	msgbox LegendsKanto_Text_NeedInvitation, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_EventScript_DeclineFerry::
	msgbox LegendsKanto_Text_DeclineFerry, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_EventScript_ReturnFerry::
	lockall
	faceplayer
	checkitem ITEM_INVITE_TICKET
	goto_if_eq VAR_RESULT, FALSE, LegendsKanto_EventScript_ReturnNoTicket
	msgbox LegendsKanto_Text_Return, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_EventScript_DeclineFerry
	msgbox LegendsKanto_Text_ReturnVoyage, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	playse SE_SHIP
	delay 60
	setrespawn HEAL_LOCATION_LILYCOVE_CITY
	warp MAP_LILYCOVE_CITY_HARBOR, 4, 13
	waitstate
	releaseall
	end

LegendsKanto_EventScript_ReturnNoTicket::
	msgbox LegendsKanto_Text_ReturnNoTicket, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_EventScript_FirstWelcome::
	setvar VAR_TEMP_0, 1
	goto_if_set FLAG_LEGENDS_KANTO_WELCOMED, LegendsKanto_EventScript_WelcomeDone
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, LegendsKanto_Movement_FaceUp
	waitmovement 0
	applymovement LOCALID_LEGENDS_KANTO_HOST, LegendsKanto_Movement_FaceDown
	waitmovement 0
	applymovement LOCALID_LEGENDS_KANTO_FAN, LegendsKanto_Movement_FaceDown
	waitmovement 0
	msgbox LegendsKanto_Text_FirstWelcome, MSGBOX_DEFAULT
	msgbox LegendsKanto_Text_FirstFan, MSGBOX_DEFAULT
	msgbox LegendsKanto_Text_FirstDirections, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_KANTO_WELCOMED
	releaseall
LegendsKanto_EventScript_WelcomeDone::
	end

LegendsKanto_Movement_FaceUp:
	face_up
	step_end

LegendsKanto_Movement_FaceDown:
	face_down
	step_end

LegendsKanto_EventScript_WelcomeHost::
	msgbox LegendsKanto_Text_Host, MSGBOX_NPC
	end

LegendsKanto_EventScript_WelcomeFan::
	msgbox LegendsKanto_Text_Fan, MSGBOX_NPC
	end

LegendsKanto_EventScript_Alex::
	lock
	faceplayer
	checktrainerflag TRAINER_LEGENDS_KANTO_ALEX
	goto_if TRUE, LegendsKanto_EventScript_AlexBeaten
	msgbox LegendsKanto_Text_AlexOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_EventScript_AlexDeclined
	trainerbattle_single TRAINER_LEGENDS_KANTO_ALEX, LegendsKanto_Text_AlexIntro, LegendsKanto_Text_AlexDefeat
	msgbox LegendsKanto_Text_AlexAfter, MSGBOX_DEFAULT
	release
	end

LegendsKanto_EventScript_AlexBeaten::
	msgbox LegendsKanto_Text_AlexAfter, MSGBOX_DEFAULT
	release
	end

LegendsKanto_EventScript_AlexDeclined::
	msgbox LegendsKanto_Text_AlexDeclined, MSGBOX_DEFAULT
	release
	end

LegendsKanto_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_LEGENDS_KANTO_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

LegendsKanto_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart LegendsKanto_MartStock
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
LegendsKanto_MartStock:
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_REVIVE
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_MAX_REPEL
	pokemartlistend

LegendsKanto_EventScript_Machop::
	lock
	faceplayer
	playmoncry SPECIES_MACHOP, CRY_MODE_NORMAL
	msgbox LegendsKanto_Text_Machop, MSGBOX_DEFAULT
	waitmoncry
	release
	end

LegendsKanto_EventScript_Pikachu::
	lock
	faceplayer
	playmoncry SPECIES_PIKACHU, CRY_MODE_NORMAL
	msgbox LegendsKanto_Text_Pikachu, MSGBOX_DEFAULT
	waitmoncry
	release
	end

LegendsKanto_Text_Invitation:
	.string "Congratulations, {PLAYER}!\n"
	.string "The news has reached KANTO.\p"
	.string "Its POKéMON LEAGUE has invited\n"
	.string "HOENN's new CHAMPION to visit.\p"
	.string "This is your INVITE TICKET.\n"
	.string "I hope you'll enjoy the journey!$"

LegendsKanto_Text_InvitationReminder:
	.string "Show your INVITE TICKET to the\n"
	.string "SAILOR by the harbor entrance.\p"
	.string "The KANTO service sails to\n"
	.string "VERMILION CITY. Keep your ticket!\p"
	.string "It is valid for return journeys\n"
	.string "whenever you wish to travel.$"

LegendsKanto_Text_NotChampion:
	.string "I'm here on POKéMON LEAGUE\n"
	.string "business. Some invitations are\l"
	.string "best delivered in person!$"

LegendsKanto_Text_FerryClosed:
	.string "We're preparing a special\n"
	.string "passenger service to KANTO.\p"
	.string "For now, please speak to the\n"
	.string "attendant about local sailings.$"

LegendsKanto_Text_NeedInvitation:
	.string "May I see your INVITE TICKET?\p"
	.string "The LEAGUE representative here\n"
	.string "has an invitation for you.$"

LegendsKanto_Text_Outbound:
	.string "An INVITE TICKET! Welcome aboard.\n"
	.string "Sail to VERMILION CITY in KANTO?$"

LegendsKanto_Text_BonVoyage:
	.string "All aboard for VERMILION CITY!\p"
	.string "We'll keep a berth ready for\n"
	.string "your return. Enjoy the crossing!$"

LegendsKanto_Text_DeclineFerry:
	.string "Take your time. We'll be here\n"
	.string "when you're ready to sail.$"

LegendsKanto_Text_Return:
	.string "Your INVITE TICKET is still valid.\n"
	.string "Sail back to LILYCOVE CITY?$"

LegendsKanto_Text_ReturnVoyage:
	.string "All aboard for LILYCOVE CITY!\p"
	.string "You're welcome to visit KANTO\n"
	.string "again on our next crossing.$"

LegendsKanto_Text_ReturnNoTicket:
	.string "You'll need an INVITE TICKET\n"
	.string "to board this passenger service.$"

LegendsKanto_Text_FirstWelcome:
	.string "Welcome to VERMILION CITY,\n"
	.string "{PLAYER}!\p"
	.string "The LEAGUE told our FAN CLUB\n"
	.string "that HOENN's CHAMPION was coming.\p"
	.string "A few of us came down to the\n"
	.string "port to welcome you to KANTO.$"

LegendsKanto_Text_FirstFan:
	.string "I saw your CHAMPIONSHIP match\n"
	.string "on TV! Your POKéMON were great!\p"
	.string "I hope they like it here, too!$"

LegendsKanto_Text_FirstDirections:
	.string "The POKéMON CENTER is at the\n"
	.string "north end of town.\p"
	.string "Please visit our FAN CLUB when\n"
	.string "you've had a chance to settle in.\p"
	.string "And your return ferry will be\n"
	.string "waiting right here at the port.$"

LegendsKanto_Text_Host:
	.string "It's lovely to meet a TRAINER\n"
	.string "from across the sea.\p"
	.string "Our FAN CLUB is open to everyone.\n"
	.string "Please stop by!$"

LegendsKanto_Text_Fan:
	.string "Being a CHAMPION must take a lot\n"
	.string "of practice. I'll keep training\l"
	.string "with my POKéMON, too!$"

LegendsKanto_Text_AlexOffer:
	.string "You're HOENN's CHAMPION!\n"
	.string "I was hoping to meet you.\p"
	.string "I've trained all around KANTO.\n"
	.string "Would you like a friendly match?\p"
	.string "I have six POKéMON, around\n"
	.string "Lv. 60 to 64. We won't hold back!\p"
	.string "Would you like to battle now?$"

LegendsKanto_Text_AlexIntro:
	.string "Let's see what our POKéMON\n"
	.string "have learned on their travels!$"

LegendsKanto_Text_AlexDefeat:
	.string "What a team! Now I see why\n"
	.string "you became the CHAMPION!$"

LegendsKanto_Text_AlexAfter:
	.string "That was a wonderful battle!\p"
	.string "You and your POKéMON really\n"
	.string "understand one another.\p"
	.string "There are always new things\n"
	.string "to learn from another TRAINER.\l"
	.string "I'm glad I came to the port!$"

LegendsKanto_Text_AlexDeclined:
	.string "Of course! Rest your POKéMON\n"
	.string "and have a look around.\p"
	.string "I'll be here if you feel\n"
	.string "like having a battle later.$"

LegendsKanto_Text_Machop:
	.string "MACHOP: Guoh! Guoh!$"

LegendsKanto_Text_Pikachu:
	.string "PIKACHU: Pika!$"

LegendsKanto_EventScript_TownWoman::
	msgbox LegendsKanto_Text_TownWoman, MSGBOX_NPC
	end

LegendsKanto_Text_TownWoman:
	.string "The LEAGUE has new challenges\n"
	.string "for visiting CHAMPIONS.\p"
	.string "OAK's aide is gathering\n"
	.string "reports at the FAN CLUB.$"

LegendsKanto_EventScript_OldMan::
	msgbox LegendsKanto_Text_OldMan, MSGBOX_NPC
	end

LegendsKanto_Text_OldMan:
	.string "Ships bring people and POKéMON\n"
	.string "here from all over the world.\p"
	.string "You never know who you might\n"
	.string "meet on a walk by the harbor!$"

LegendsKanto_EventScript_Builder::
	msgbox LegendsKanto_Text_Builder, MSGBOX_NPC
	end

LegendsKanto_Text_Builder:
	.string "I'm building a house here.\n"
	.string "MACHOP is a splendid helper.\p"
	.string "We have to be patient, though.\n"
	.string "Good work takes time!$"

LegendsKanto_EventScript_DockSailor::
	msgbox LegendsKanto_Text_DockSailor, MSGBOX_NPC
	end

LegendsKanto_Text_DockSailor:
	.string "That ship is on regular service\n"
	.string "between here and LILYCOVE.\p"
	.string "Your INVITE TICKET covers\n"
	.string "every crossing. Handy, eh?$"

LegendsKanto_EventScript_RoadCrew::
	msgbox LegendsKanto_Text_RoadCrew, MSGBOX_NPC
	end

LegendsKanto_Text_RoadCrew:
	.string "The north road is open!\n"
	.string "SAFFRON CITY lies ahead.$"

LegendsKanto_EventScript_GymClosed::
	msgbox LegendsKanto_Text_GymClosed, MSGBOX_NPC
	end

LegendsKanto_Text_GymClosed:
	.string "LT. SURGE is accepting\n"
	.string "visiting CHAMPIONS inside.$"

LegendsKanto_EventScript_CenterVisitor::
	msgbox LegendsKanto_Text_CenterVisitor, MSGBOX_NPC
	end

LegendsKanto_Text_CenterVisitor:
	.string "A CHAMPION needs a rest, too!\p"
	.string "This POKéMON CENTER can care\n"
	.string "for your whole team.$"

LegendsKanto_EventScript_CenterBoy::
	msgbox LegendsKanto_Text_CenterBoy, MSGBOX_NPC
	end

LegendsKanto_Text_CenterBoy:
	.string "There's a TRAINER at the port\n"
	.string "who was waiting for your ship.\p"
	.string "He says he's raised a whole\n"
	.string "team of POKéMON from KANTO!$"

LegendsKanto_EventScript_MartWoman::
	msgbox LegendsKanto_Text_MartWoman, MSGBOX_NPC
	end

LegendsKanto_Text_MartWoman:
	.string "I always stock up before\n"
	.string "taking a trip on the ferry.\p"
	.string "I don't want to run out of\n"
	.string "supplies far from home!$"

LegendsKanto_EventScript_MartBoy::
	msgbox LegendsKanto_Text_MartBoy, MSGBOX_NPC
	end

LegendsKanto_Text_MartBoy:
	.string "My POKéMON likes to watch\n"
	.string "the ships arrive at the port.\p"
	.string "I think it wants to travel!$"

LegendsKanto_EventScript_Chairman::
	msgbox LegendsKanto_Text_Chairman, MSGBOX_NPC
	end

LegendsKanto_Text_Chairman:
	.string "Welcome! I chair the POKéMON\n"
	.string "FAN CLUB here in VERMILION.\p"
	.string "What brings people together\n"
	.string "better than their POKéMON?\p"
	.string "I hear your team traveled all\n"
	.string "over HOENN with you.\p"
	.string "A title is a fine achievement.\n"
	.string "The friends you made on the\l"
	.string "way are just as precious!$"

LegendsKanto_EventScript_FanClubWoman::
	msgbox LegendsKanto_Text_FanClubWoman, MSGBOX_NPC
	end

LegendsKanto_Text_FanClubWoman:
	.string "The CHAMPION from HOENN!\p"
	.string "I wonder what POKéMON\n"
	.string "you met on your journey.\p"
	.string "I love hearing about POKéMON\n"
	.string "that live in faraway places.$"

LegendsKanto_EventScript_FanClubBoy::
	msgbox LegendsKanto_Text_FanClubBoy, MSGBOX_NPC
	end

LegendsKanto_Text_FanClubBoy:
	.string "PIKACHU and I came to see\n"
	.string "your ship arrive!\p"
	.string "Now it's showing off. I think\n"
	.string "it wants to impress you!$"

LegendsKanto_EventScript_House1::
	msgbox LegendsKanto_Text_House1, MSGBOX_NPC
	end

LegendsKanto_Text_House1:
	.string "Once, I sailed to HOENN.\n"
	.string "The sea was so blue!\p"
	.string "There was a town built right\n"
	.string "over the water. PACIFIDLOG,\l"
	.string "if I remember correctly.$"

LegendsKanto_EventScript_House2::
	msgbox LegendsKanto_Text_House2, MSGBOX_NPC
	end

LegendsKanto_Text_House2:
	.string "The sea connects VERMILION\n"
	.string "to places far beyond KANTO.\p"
	.string "As a fisherman, I like to\n"
	.string "think about the POKéMON\l"
	.string "living on the other shore.$"

LegendsKanto_EventScript_House3::
	msgbox LegendsKanto_Text_House3, MSGBOX_NPC
	end

LegendsKanto_Text_House3:
	.string "Some of our neighbors went\n"
	.string "to the port to greet you.\p"
	.string "It isn't every day that a\n"
	.string "CHAMPION comes across the sea!$"

LegendsKanto_EventScript_CitySign::
	msgbox LegendsKanto_Text_CitySign, MSGBOX_SIGN
	end

LegendsKanto_Text_CitySign:
	.string "VERMILION CITY\n"
	.string "The Port of Exquisite Sunsets$"

LegendsKanto_EventScript_FanClubSign::
	msgbox LegendsKanto_Text_FanClubSign, MSGBOX_SIGN
	end

LegendsKanto_Text_FanClubSign:
	.string "POKéMON FAN CLUB\n"
	.string "All POKéMON lovers welcome!$"

LegendsKanto_EventScript_GymSign::
	msgbox LegendsKanto_Text_GymSign, MSGBOX_SIGN
	end

LegendsKanto_Text_GymSign:
	.string "VERMILION GYM - LT. SURGE\n"
	.string "Choose your challenge inside.$"

LegendsKanto_EventScript_HarborSign::
	msgbox LegendsKanto_Text_HarborSign, MSGBOX_SIGN
	end

LegendsKanto_Text_HarborSign:
	.string "VERMILION PORT\p"
	.string "Passenger service to LILYCOVE\n"
	.string "INVITE TICKET required.$"

LegendsKanto_EventScript_RoadSign::
	msgbox LegendsKanto_Text_RoadSign, MSGBOX_SIGN
	end

LegendsKanto_Text_RoadSign:
	.string "ROUTE 11 - East\n"
	.string "ROUTE 6 - North$"

@ Transition shared by the original foundation and later populated chapters.
LegendsKanto_Foundation_OnTransition::
	setrespawn HEAL_LOCATION_LEGENDS_KANTO_VERMILION
	end

LegendsKanto_EventScript_SurfOutbound::
	lockall
	goto_if_unset FLAG_SYS_GAME_CLEAR, LegendsKanto_EventScript_SurfLocked
	checkitem ITEM_INVITE_TICKET
	goto_if_eq VAR_RESULT, FALSE, LegendsKanto_EventScript_SurfLocked
	msgbox LegendsKanto_Text_SurfOutbound, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_EventScript_DeclineFerry
	closemessage
	fadescreen FADE_TO_BLACK
	setrespawn HEAL_LOCATION_LEGENDS_KANTO_VERMILION
	warp MAP_LEGENDS_KANTO_ROUTE19, 12, 53
	waitstate
	releaseall
	end

LegendsKanto_EventScript_SurfReturn::
	lockall
	msgbox LegendsKanto_Text_SurfReturn, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsKanto_EventScript_DeclineFerry
	closemessage
	fadescreen FADE_TO_BLACK
	setrespawn HEAL_LOCATION_LILYCOVE_CITY
	warp MAP_ROUTE124, 20, 4
	waitstate
	releaseall
	end

LegendsKanto_EventScript_SurfLocked::
	msgbox LegendsKanto_Text_SurfLocked, MSGBOX_DEFAULT
	releaseall
	end

LegendsKanto_Text_SurfOutbound:
	.string "The northern passage leads\n"
	.string "to KANTO's ROUTE 19.\p"
	.string "Follow the passage?$"

LegendsKanto_Text_SurfReturn:
	.string "The southern passage leads\n"
	.string "to HOENN's ROUTE 124.\p"
	.string "Follow the passage?$"

LegendsKanto_Text_SurfLocked:
	.string "The distant passage is open\n"
	.string "to invited LEAGUE CHAMPIONS.$"

LegendsKanto_EventScript_FoundationClosed::
	msgbox LegendsKanto_Text_FoundationClosed, MSGBOX_SIGN
	end

LegendsKanto_Text_FoundationClosed:
	.string "This area is not available\n"
	.string "in this development build.$"
