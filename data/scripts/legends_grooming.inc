EventScript_GroomingGift::
	lockall
	msgbox Grooming_Welcome, MSGBOX_DEFAULT
	giveitem ITEM_GROOMING_KIT
	goto_if_eq VAR_RESULT, FALSE, Grooming_NoRoom
	msgbox Grooming_KitHint, MSGBOX_DEFAULT
	releaseall
	end
Grooming_NoRoom:
	msgbox Grooming_Full, MSGBOX_DEFAULT
	releaseall
	end

EventScript_GroomingKit::
	lockall
	getpartysize
	goto_if_eq VAR_RESULT, 0, Grooming_End
	special ChoosePartyMon
	goto_if_ge VAR_0x8004, PARTY_SIZE, Grooming_End
	special GroomingValidateMon
	goto_if_eq VAR_RESULT, FALSE, Grooming_Egg
	special GroomingStart
	waitstate
Grooming_End:
	releaseall
	end
Grooming_Egg:
	msgbox Grooming_Wait, MSGBOX_DEFAULT
	releaseall
	end

Grooming_Welcome:
	.string "NURSE: Welcome! Here, take this.\p"
	.string "After a dusty trip, a warm bath\n"
	.string "feels good on paws and scales alike.$"
Grooming_KitHint:
	.string "Open the Grooming Kit in KEY ITEMS\n"
	.string "and choose a partner for bath time!$"
Grooming_Full:
	.string "Make room in your BAG and stop\n"
	.string "by again. I'll keep it for you!$"
Grooming_Wait:
	.string "Let's wait until this EGG hatches.$"
