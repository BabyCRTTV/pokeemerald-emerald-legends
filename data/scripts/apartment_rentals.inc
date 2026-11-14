.set RENT_COVE_LILY, 2200
.set RENT_MAUVILLE_HILLS, 3100

Rental_Lily_Notice::
	lockall
	goto_if_set FLAG_RENTAL_COVE_LILY, Rental_Lily_AlreadyRented
	showmoneybox 0, 0
	buffernumberstring STR_VAR_1, RENT_COVE_LILY
	msgbox Rental_Text_LilyOffer, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, Rental_CloseOffer
	checkmoney RENT_COVE_LILY
	goto_if_eq VAR_RESULT, FALSE, Rental_NotEnoughMoney
	removemoney RENT_COVE_LILY
	setflag FLAG_RENTAL_COVE_LILY
	call Rental_UpdateMoney
	msgbox Rental_Text_LilyPaid, MSGBOX_DEFAULT
	goto Rental_CloseOffer

Rental_Mauville_Notice::
	lockall
	goto_if_set FLAG_RENTAL_MAUVILLE_HILLS, Rental_Mauville_AlreadyRented
	showmoneybox 0, 0
	buffernumberstring STR_VAR_1, RENT_MAUVILLE_HILLS
	msgbox Rental_Text_MauvilleOffer, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, Rental_CloseOffer
	checkmoney RENT_MAUVILLE_HILLS
	goto_if_eq VAR_RESULT, FALSE, Rental_NotEnoughMoney
	removemoney RENT_MAUVILLE_HILLS
	setflag FLAG_RENTAL_MAUVILLE_HILLS
	call Rental_UpdateMoney
	msgbox Rental_Text_MauvillePaid, MSGBOX_DEFAULT
	goto Rental_CloseOffer

Rental_UpdateMoney:
	playse SE_SHOP
	updatemoneybox
	return

Rental_NotEnoughMoney:
	msgbox Rental_Text_NotEnoughMoney, MSGBOX_DEFAULT
Rental_CloseOffer:
	hidemoneybox
	releaseall
	end

Rental_Lily_AlreadyRented:
	msgbox Rental_Text_LilyPaid, MSGBOX_DEFAULT
	releaseall
	end

Rental_Mauville_AlreadyRented:
	msgbox Rental_Text_MauvillePaid, MSGBOX_DEFAULT
	releaseall
	end

Rental_Mauville_ExteriorSign::
	msgbox Rental_Text_MauvilleExteriorSign, MSGBOX_SIGN
	end

Rental_Lily_Door::
	lockall
	goto_if_unset FLAG_RENTAL_COVE_LILY, Rental_Lily_Locked
	warp MAP_LILYCOVE_CITY_COVE_LILY_MOTEL_APARTMENT, 3, 6
	waitstate
	end

Rental_Mauville_Door::
	lockall
	goto_if_unset FLAG_RENTAL_MAUVILLE_HILLS, Rental_Mauville_Locked
	warp MAP_MAUVILLE_CITY_MAUVILLE_HILLS_APARTMENT, 3, 6
	waitstate
	end

Rental_Lily_Locked:
	msgbox Rental_Text_LilyLocked, MSGBOX_DEFAULT
	releaseall
	end

Rental_Mauville_Locked:
	msgbox Rental_Text_MauvilleLocked, MSGBOX_DEFAULT
	releaseall
	end

@ These step-out scripts are the only connections from the private rooms.
Rental_Lily_Exit::
	warp MAP_LILYCOVE_CITY_COVE_LILY_MOTEL_2F, 6, 2
	waitstate
	end

Rental_Mauville_Exit::
	warp MAP_MAUVILLE_CITY_MAUVILLE_HILLS_LOBBY, 6, 2
	waitstate
	end

Rental_Rest::
	lockall
	msgbox Rental_Text_Rest, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, Rental_Done
	fadescreen FADE_TO_BLACK
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	fadescreen FADE_FROM_BLACK
	msgbox Rental_Text_Rested, MSGBOX_DEFAULT
	goto Rental_Done

Rental_Lily_Decor::
	lockall
	msgbox Rental_Text_LilyDecor, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, Rental_Done
	goto_if_set FLAG_RENTAL_COVE_LILY_DECOR, Rental_Lily_PutAwayDecor
	setflag FLAG_RENTAL_COVE_LILY_DECOR
	call Rental_Lily_ShowDecor
	goto Rental_Redraw

Rental_Lily_PutAwayDecor:
	clearflag FLAG_RENTAL_COVE_LILY_DECOR
	setmetatile 1, 6, 0x223, FALSE
	setmetatile 1, 7, 0x223, FALSE
	goto Rental_Redraw

Rental_Mauville_Decor::
	lockall
	msgbox Rental_Text_MauvilleDecor, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, Rental_Done
	goto_if_set FLAG_RENTAL_MAUVILLE_HILLS_DECOR, Rental_Mauville_PutAwayDecor
	setflag FLAG_RENTAL_MAUVILLE_HILLS_DECOR
	call Rental_Mauville_ShowDecor
	goto Rental_Redraw

Rental_Mauville_PutAwayDecor:
	clearflag FLAG_RENTAL_MAUVILLE_HILLS_DECOR
	setmetatile 7, 6, 0x223, FALSE
	setmetatile 8, 6, 0x223, FALSE
	setmetatile 9, 6, 0x223, FALSE
	setmetatile 7, 7, 0x223, FALSE
	setmetatile 8, 7, 0x223, FALSE
	setmetatile 9, 7, 0x223, FALSE

Rental_Redraw:
	special DrawWholeMapView
	playse SE_SELECT
Rental_Done:
	releaseall
	end

Rental_Lily_OnLoad::
	call_if_set FLAG_RENTAL_COVE_LILY_DECOR, Rental_Lily_ShowDecor
	end

Rental_Mauville_OnLoad::
	call_if_set FLAG_RENTAL_MAUVILLE_HILLS_DECOR, Rental_Mauville_ShowDecor
	end

Rental_Lily_ShowDecor:
	setmetatile 1, 6, 0x291, TRUE
	setmetatile 1, 7, 0x299, TRUE
	return

Rental_Mauville_ShowDecor:
	setmetatile 7, 6, 0x235, FALSE
	setmetatile 8, 6, 0x236, FALSE
	setmetatile 9, 6, 0x237, FALSE
	setmetatile 7, 7, 0x245, FALSE
	setmetatile 8, 7, 0x246, FALSE
	setmetatile 9, 7, 0x247, FALSE
	return

Rental_Text_LilyOffer:
	.string "COVE LILY MOTEL\n"
	.string "Furnished studio upstairs.\p"
	.string "Rent it for ¥{STR_VAR_1}?\n"
	.string "One payment keeps the room yours.$"

Rental_Text_MauvilleOffer:
	.string "MAUVILLE HILLS\n"
	.string "Furnished apartment with a kitchen.\p"
	.string "Rent it for ¥{STR_VAR_1}?\n"
	.string "One payment keeps the room yours.$"

Rental_Text_NotEnoughMoney:
	.string "You don't have enough money\n"
	.string "to rent this apartment.$"

Rental_Text_LilyPaid:
	.string "The COVE LILY studio is yours.\n"
	.string "Your door is upstairs.$"

Rental_Text_MauvillePaid:
	.string "The MAUVILLE HILLS apartment\n"
	.string "is yours. Your door is at the back\l"
	.string "of the lobby.$"

Rental_Text_MauvilleExteriorSign:
	.string "MAUVILLE HILLS\n"
	.string "Furnished apartment for rent.\p"
	.string "See the notice at the front desk.$"

Rental_Text_LilyLocked:
	.string "The studio is locked.\n"
	.string "Check the rent notice downstairs.$"

Rental_Text_MauvilleLocked:
	.string "The apartment is locked.\n"
	.string "Check the rent notice at the desk.$"

Rental_Text_Rest:
	.string "Rest here with your POKéMON?$"

Rental_Text_Rested:
	.string "You and your POKéMON feel refreshed!$"

Rental_Text_LilyDecor:
	.string "A potted palm can go by the door.\n"
	.string "Change the display?$"

Rental_Text_MauvilleDecor:
	.string "Change the kitchen runner?$"
