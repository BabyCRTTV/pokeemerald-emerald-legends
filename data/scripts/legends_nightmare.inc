@ When Morning Never Comes. Audited native flags; no saved structure changes.
Nightmare_UnknownCall::
	lockall
	setflag FLAG_LEGENDS_NIGHTMARE_CALL
	pokenavcall Nightmare_Text_Call
	waitmessage
	releaseall
	end
Nightmare_HomeLoad::
	setflag FLAG_TEMP_8
	setflag FLAG_TEMP_9
	goto_if_unset FLAG_LEGENDS_NIGHTMARE_CALL, Nightmare_HomeAwake
	goto_if_set FLAG_LEGENDS_NIGHTMARE_RESOLVED, Nightmare_HomeAwake
	clearflag FLAG_TEMP_9
	end
Nightmare_HomeAwake::
	clearflag FLAG_TEMP_8
Nightmare_HomeLoadEnd::
	end
Nightmare_Father::
	lock
	faceplayer
	goto_if_unset FLAG_LEGENDS_NIGHTMARE_CALL, Nightmare_FatherBefore
	goto_if_set FLAG_LEGENDS_NIGHTMARE_REPORTED, Nightmare_FatherAfter
	goto_if_set FLAG_LEGENDS_NIGHTMARE_RESOLVED, Nightmare_FatherThanks
	goto_if_set FLAG_LEGENDS_NIGHTMARE_VISITED, Nightmare_FatherHint
	msgbox Nightmare_Text_Father, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_NIGHTMARE_VISITED
Nightmare_FatherHint::
	goto_if_set FLAG_LEGENDS_NIGHTMARE_WING, Nightmare_FatherWing
	msgbox Nightmare_Text_PyreHint, MSGBOX_DEFAULT
	release
	end
Nightmare_FatherWing::
	msgbox Nightmare_Text_FatherWing, MSGBOX_DEFAULT
	release
	end
Nightmare_FatherBefore::
	msgbox Nightmare_Text_Before, MSGBOX_DEFAULT
	release
	end
Nightmare_FatherThanks::
	msgbox Nightmare_Text_Thanks, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_NIGHTMARE_REPORTED
	release
	end
Nightmare_FatherAfter::
	msgbox Nightmare_Text_FatherAfter, MSGBOX_DEFAULT
	release
	end
@ Called within the native caretaker's locked interaction. Her Cleanse Tag
@ and repeat dialogue continue after this; no original reward is suppressed.
Nightmare_Keeper::
	goto_if_unset FLAG_LEGENDS_NIGHTMARE_VISITED, Common_EventScript_NopReturn
	goto_if_set FLAG_LEGENDS_NIGHTMARE_WING, Common_EventScript_NopReturn
	msgbox Nightmare_Text_Keeper, MSGBOX_DEFAULT
	checkitem ITEM_LUNAR_WING
	goto_if_eq VAR_RESULT, TRUE, Nightmare_WingReceived
	giveitem ITEM_LUNAR_WING
	goto_if_eq VAR_RESULT, FALSE, Nightmare_WingBagFull
Nightmare_WingReceived::
	setflag FLAG_LEGENDS_NIGHTMARE_WING
	msgbox Nightmare_Text_Wing, MSGBOX_DEFAULT
	return
Nightmare_WingBagFull::
	msgbox Nightmare_Text_WingBagFull, MSGBOX_DEFAULT
	return
Nightmare_Bed::
	lockall
	goto_if_unset FLAG_LEGENDS_NIGHTMARE_CALL, Nightmare_BedBefore
	goto_if_set FLAG_LEGENDS_NIGHTMARE_RESOLVED, Nightmare_BedAfter
	msgbox Nightmare_Text_Sleeping, MSGBOX_DEFAULT
	goto_if_unset FLAG_LEGENDS_NIGHTMARE_WING, Nightmare_End
	msgbox Nightmare_Text_Enter, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Nightmare_End
	goto Nightmare_IntoDream
Nightmare_BedBefore::
	msgbox Nightmare_Text_BedBefore, MSGBOX_DEFAULT
	releaseall
	end
Nightmare_BedAfter::
	msgbox Nightmare_Text_Revisit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Nightmare_End
Nightmare_IntoDream::
	closemessage
	fadescreen FADE_TO_BLACK
	warp MAP_LEGENDS_NIGHTMARE_BEDROOM, 6, 6
	waitstate
	releaseall
	end
Nightmare_EnterDream::
	setflag FLAG_LEGENDS_NIGHTMARE_ENTERED
	end
Nightmare_Chair::
	msgbox Nightmare_Text_Chair, MSGBOX_SIGN
	end
Nightmare_DreamChair::
	lockall
	playse SE_DOOR
	msgbox Nightmare_Text_DreamChair, MSGBOX_DEFAULT
	releaseall
	end
Nightmare_DreamBed::
	lockall
	msgbox Nightmare_Text_LeaveDream, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Nightmare_End
	goto Nightmare_Wake
Nightmare_Echo::
	lock
	faceplayer
	goto_if_set FLAG_LEGENDS_NIGHTMARE_RESOLVED, Nightmare_EchoAfter
	msgbox Nightmare_Text_Echo, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_NIGHTMARE_VOICE
	release
	end
Nightmare_EchoAfter::
	msgbox Nightmare_Text_EchoAfter, MSGBOX_DEFAULT
	release
	end
Nightmare_WrongDoor::
	msgbox Nightmare_Text_WrongDoor, MSGBOX_SIGN
	end
Nightmare_ShoreResume::
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, Nightmare_CheckCapture
	end
Nightmare_CheckCapture::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	setflag FLAG_LEGENDS_NIGHTMARE_CAUGHT
	setflag FLAG_LEGENDS_NIGHTMARE_RESOLVED
	removeobject 1
	return
Nightmare_Darkrai::
	lockall
	faceplayer
	goto_if_set FLAG_LEGENDS_NIGHTMARE_CAUGHT, Nightmare_End
	msgbox Nightmare_Text_Darkrai, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Nightmare_End
	closemessage
	playmoncry SPECIES_DARKRAI, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_DARKRAI, 80
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Nightmare_Caught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, Nightmare_Resolved
	msgbox Nightmare_Text_Retry, MSGBOX_DEFAULT
	releaseall
	end
Nightmare_Caught::
	setflag FLAG_LEGENDS_NIGHTMARE_CAUGHT
	removeobject 1
Nightmare_Resolved::
	setflag FLAG_LEGENDS_NIGHTMARE_RESOLVED
	msgbox Nightmare_Text_DreamEnds, MSGBOX_DEFAULT
Nightmare_Wake::
	closemessage
	fadescreen FADE_TO_BLACK
	warp MAP_LEGENDS_NIGHTMARE_HOME, 7, 5
	waitstate
	releaseall
	end
Nightmare_End::
	releaseall
	end
Nightmare_Mira::
	goto_if_unset FLAG_LEGENDS_NIGHTMARE_CALL, Nightmare_MiraBefore
	msgbox Nightmare_Text_Awake, MSGBOX_NPC
	end

Nightmare_Text_Call:
	.string "UNKNOWN NUMBER: ...Hello?\nIs this {PLAYER}?\pMy name is ELIAS. MR. BRINEY\nsaid you might be able to help.\pMy daughter won't wake up.\nNot for days. Nothing helps.\pShe keeps whispering about a house\nbeside a sea with no moon.\pWe're in LILYCOVE, in the little\nhouse beside the MOVE DELETER.\pPlease... I don't know who else\nto ask.$"

Nightmare_Text_Before:
	.string "ELIAS: My daughter loves the sea.\nShe says it follows her into dreams.$"

Nightmare_Text_Father:
	.string "ELIAS: You came. Thank you.\nHer name is MIRA.\pI thought she was just tired.\nThen morning came... and went.\pSometimes she says she's cold.\nSometimes she asks me to find her.\pI'm right here. I've been right\nhere the whole time.$"

Nightmare_Text_PyreHint:
	.string "ELIAS: The caretaker at MT. PYRE\nonce helped MIRA with bad dreams.\pThe old woman on the first floor.\nCould you speak to her?$"

Nightmare_Text_FatherWing:
	.string "ELIAS: That feather...\nMIRA stopped shivering.\pPlease, try it beside her bed.\nI'll stay here with her.$"

Nightmare_Text_Keeper:
	.string "A child who cannot leave her dream?\nAnd a sea without a moon...\pDARKRAI's dreams can spill over\ninto the sleep of those nearby.\pThat does not mean it wishes harm.\nSometimes even it cannot stop them.\pThis LUNAR WING carries a little\nof CRESSELIA's light.\pIt may not wake her. But it can\ngive you a way to reach her.\pHold it beside her bed. If you\nmust return, seek that bed again.$"

Nightmare_Text_Wing:
	.string "You carefully took the LUNAR WING.\pIts light feels warm in your hand.\nYou'll keep it safe for MIRA.$"

Nightmare_Text_Sleeping:
	.string "MIRA lies very still.\nHer breathing is shallow.\pMIRA: ...The door is wrong...\n...I can hear the sea...$"

Nightmare_Text_Enter:
	.string "The LUNAR WING begins to glow.\nFollow its light into MIRA's dream?$"

Nightmare_Text_Chair:
	.string "An empty chair beside the bed.\nIts cushion is worn.$"

Nightmare_Text_DreamChair:
	.string "The empty chair creaks.\pYou hear someone stand up.\nThere is nobody there.$"

Nightmare_Text_LeaveDream:
	.string "The bed is empty. The LUNAR WING\ncasts a warm light over its pillow.\pFollow that light and wake up?$"

Nightmare_Text_Echo:
	.string "MIRA: I opened our door...\nBut it wasn't our street.\pThe other house. I could hear\nthe sea behind its door.\pThere's someone waiting there.\nI think it's frightened, too.$"

Nightmare_Text_WrongDoor:
	.string "There is no sound from inside.\pThen, very faintly...\nWaves breaking against wood.$"

Nightmare_Text_Darkrai:
	.string "A dark shape drifts over the pier.\nThe water beneath it is still.\pThe LUNAR WING glows. DARKRAI\nturns toward you. Approach it?$"

Nightmare_Text_Retry:
	.string "The shore has not changed.\nDARKRAI waits beside the black sea.\pThe LUNAR WING is still warm.\nYou can try again.$"

Nightmare_Text_DreamEnds:
	.string "A ripple crosses the black water.\nFor a moment, you can see the sky.\pMIRA: ...Dad?\pThe LUNAR WING fills your vision\nwith a soft, white light.$"

Nightmare_Text_Awake:
	.string "MIRA: You found me.\nI knew somebody would.\pI don't think it meant to scare me.\nIt looked so lonely out there.\pCould we open the window?\nI'd like to hear the real sea.$"

Nightmare_Text_Thanks:
	.string "ELIAS: She asked for breakfast.\nSuch a small thing...\pI'd forgotten how much I missed\nhearing her say it.\pThank you for bringing my little\ngirl home, {PLAYER}.$"

Nightmare_Text_FatherAfter:
	.string "ELIAS: MIRA slept well last night.\nSo did I, for the first time in days.$"

Nightmare_Text_Revisit:
	.string "MIRA is safe. The LUNAR WING still\nanswers something beyond this room.\pVisit the quiet shore again?$"

Nightmare_Text_EchoAfter:
	.string "The street is quiet.\nThis memory no longer feels afraid.$"

Nightmare_MiraBefore::
	msgbox Nightmare_Text_MiraBefore, MSGBOX_NPC
	end
Nightmare_Text_WingBagFull:
	.string "Keep a little room for the wing.\nCome back when you can carry it.$"
Nightmare_Text_BedBefore:
	.string "MIRA's bed is neatly made.\nSea air drifts through the window.$"
Nightmare_Text_MiraBefore:
	.string "MIRA: I like listening to the waves.\nThey help me fall asleep.$"
