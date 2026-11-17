EventScript_Kitchen::
EventScript_KitchenSink::
EventScript_KitchenFridge::
	setvar VAR_0x8005, 0
	goto EventScript_OpenCooking

EventScript_UseSteelCanteen::
	setvar VAR_0x8005, 1
	goto EventScript_OpenCooking

EventScript_UseMessKit::
	setvar VAR_0x8005, 2
	goto EventScript_OpenCooking

EventScript_UsePercolator::
	setvar VAR_0x8005, 3

EventScript_OpenCooking::
	setflag FLAG_SAFE_FOLLOWER_MOVEMENT
	lockall
	setvar VAR_0x8004, MULTI_B_PRESSED

EventScript_ChooseMeal::
	closemessage
	callnative Script_LegendsChooseRecipe
	goto_if_eq VAR_RESULT, MULTI_B_PRESSED, EventScript_FinishMealInteraction
	copyvar VAR_0x8004, VAR_RESULT
	goto_if_eq VAR_0x8006, TRUE, EventScript_ConfirmPrepareDrink
	msgbox Text_CookSelectedMeal, MSGBOX_YESNO
	goto EventScript_TryCookSelectedRecipe

EventScript_ConfirmPrepareDrink::
	msgbox Text_PrepareSelectedDrink, MSGBOX_YESNO

EventScript_TryCookSelectedRecipe::
	goto_if_ne VAR_RESULT, YES, EventScript_ChooseMeal
	callnative Script_LegendsCookMeal
	goto_if_eq VAR_RESULT, 0, EventScript_CookMissingSupplies
	goto_if_eq VAR_RESULT, 2, EventScript_CookBagFull
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	goto_if_eq VAR_0x8006, TRUE, EventScript_PrepareDrinkSuccess
	msgbox Text_CookSuccess
	goto EventScript_ChooseMeal

EventScript_PrepareDrinkSuccess::
	msgbox Text_DrinkPrepared
	goto EventScript_ChooseMeal

EventScript_CookMissingSupplies::
	msgbox Text_CookMissingSupplies
	goto EventScript_ChooseMeal

EventScript_CookBagFull::
	msgbox Text_CookBagFull
	goto EventScript_ChooseMeal

EventScript_FinishMealInteraction::
	releaseall
	clearflag FLAG_SAFE_FOLLOWER_MOVEMENT
	end

EventScript_MomPortableCookingGear::
	checkitem ITEM_STEEL_CANTEEN
	goto_if_eq VAR_RESULT, FALSE, EventScript_MomGivePortableCookingGear
	checkitem ITEM_MESS_KIT
	goto_if_eq VAR_RESULT, FALSE, EventScript_MomGivePortableCookingGear
	checkitem ITEM_PERCOLATOR
	goto_if_eq VAR_RESULT, FALSE, EventScript_MomGivePortableCookingGear
	return

EventScript_MomGivePortableCookingGear::
	msgbox Text_MomPackedCookingGear
	checkitem ITEM_STEEL_CANTEEN
	call_if_eq VAR_RESULT, FALSE, EventScript_GiveSteelCanteen
	goto_if_eq VAR_RESULT, FALSE, EventScript_MomFinishPortableCookingGift
	checkitem ITEM_MESS_KIT
	call_if_eq VAR_RESULT, FALSE, EventScript_GiveMessKit
	goto_if_eq VAR_RESULT, FALSE, EventScript_MomFinishPortableCookingGift
	checkitem ITEM_PERCOLATOR
	call_if_eq VAR_RESULT, FALSE, EventScript_GivePercolator
EventScript_MomFinishPortableCookingGift::
	return

EventScript_GiveSteelCanteen::
	giveitem ITEM_STEEL_CANTEEN
	return

EventScript_GiveMessKit::
	giveitem ITEM_MESS_KIT
	return

EventScript_GivePercolator::
	giveitem ITEM_PERCOLATOR
	return

Text_MomPackedCookingGear::
	.string "MOM: I packed some cooking gear\n"
	.string "for your trip, honey.\p"
	.string "With a meal and a warm drink,\n"
	.string "you can make anywhere feel like home.$"

Text_CookSelectedMeal::
	.string "Craft this meal?$"

Text_PrepareSelectedDrink::
	.string "Craft this drink?$"

Text_CookSuccess::
	.string "You cooked {STR_VAR_1}!\n"
	.string "It's in the FOOD pocket.$"

Text_DrinkPrepared::
	.string "You prepared {STR_VAR_1}!\n"
	.string "It's in the FOOD pocket.$"

Text_CookMissingSupplies::
	.string "You're missing some ingredients.\n"
	.string "Try INGREDIENTS at the POKé MART.$"

Text_CookBagFull::
	.string "There's no room in your BAG.$"
