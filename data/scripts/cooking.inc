EventScript_Kitchen::
	setflag FLAG_SAFE_FOLLOWER_MOVEMENT
	lockall
	msgbox Text_Kitchen
	goto EventScript_PrepareMeal

EventScript_KitchenSink::
	setflag FLAG_SAFE_FOLLOWER_MOVEMENT
	lockall
	msgbox Text_KitchenSink
	goto EventScript_PrepareMeal

EventScript_KitchenFridge::
	setflag FLAG_SAFE_FOLLOWER_MOVEMENT
	lockall
	msgbox Text_KitchenFridge
	goto EventScript_PrepareMeal

EventScript_PrepareMeal::
	setvar VAR_0x8005, 0
	msgbox Text_PrepareMeal, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, EventScript_FinishMealInteraction
	goto EventScript_ChooseMeal

EventScript_UseSteelCanteen::
	setvar VAR_0x8005, 1
	goto EventScript_OpenPortableCooking

EventScript_UseMessKit::
	setvar VAR_0x8005, 2
	goto EventScript_OpenPortableCooking

EventScript_UsePercolator::
	setvar VAR_0x8005, 3
	goto EventScript_OpenPortableCooking

EventScript_OpenPortableCooking::
	setflag FLAG_SAFE_FOLLOWER_MOVEMENT
	lockall
	goto EventScript_ChooseMeal

EventScript_ChooseMeal::
	goto_if_eq VAR_0x8005, 1, EventScript_ChooseCanteenDrink
	goto_if_eq VAR_0x8005, 2, EventScript_ChooseMessKitMeal
	goto_if_eq VAR_0x8005, 3, EventScript_ChoosePercolatorDrink
	message Text_ChooseMeal
	waitmessage
	multichoicegrid 0, 0, MULTI_LEGENDS_MEALS, 2, FALSE
	switch VAR_RESULT
	case 0, EventScript_MealOmelet
	case 1, EventScript_MealPancakes
	case 2, EventScript_MealFlatbread
	case 3, EventScript_MealSoup
	case 4, EventScript_MealCrackers
	case 5, EventScript_MealHotCocoa
	case 6, EventScript_MealEggCustard
	goto EventScript_FinishMealInteraction

EventScript_ChooseCanteenDrink::
	message Text_ChooseDrink
	waitmessage
	multichoice 0, 0, MULTI_LEGENDS_CANTEEN, FALSE
	goto_if_eq VAR_RESULT, 0, EventScript_MealHotCocoa
	goto EventScript_FinishMealInteraction

EventScript_ChooseMessKitMeal::
	message Text_ChooseMeal
	waitmessage
	dynmultichoice 0, 0, FALSE, 6, 0, DYN_MULTICHOICE_CB_NONE, Text_MessKitOmelet, Text_MessKitPancakes, Text_MessKitFlatbread, Text_MessKitSoup, Text_MessKitCrackers, Text_MessKitCustard, Text_MessKitCancel
	switch VAR_RESULT
	case 0, EventScript_MealOmelet
	case 1, EventScript_MealPancakes
	case 2, EventScript_MealFlatbread
	case 3, EventScript_MealSoup
	case 4, EventScript_MealCrackers
	case 5, EventScript_MealEggCustard
	goto EventScript_FinishMealInteraction

EventScript_ChoosePercolatorDrink::
	message Text_ChooseBrew
	waitmessage
	multichoice 0, 0, MULTI_LEGENDS_PERCOLATOR, FALSE
	switch VAR_RESULT
	case 0, EventScript_MealMilkCoffee
	case 1, EventScript_MealSweetTea
	goto EventScript_FinishMealInteraction

EventScript_MealOmelet::
	setvar VAR_0x8004, 0
	msgbox Text_MealOmelet
	goto EventScript_ConfirmCookMeal

EventScript_MealPancakes::
	setvar VAR_0x8004, 1
	msgbox Text_MealPancakes
	goto EventScript_ConfirmCookMeal

EventScript_MealFlatbread::
	setvar VAR_0x8004, 2
	msgbox Text_MealFlatbread
	goto EventScript_ConfirmCookMeal

EventScript_MealSoup::
	setvar VAR_0x8004, 3
	msgbox Text_MealSoup
	goto EventScript_ConfirmCookMeal

EventScript_MealCrackers::
	setvar VAR_0x8004, 4
	msgbox Text_MealCrackers
	goto EventScript_ConfirmCookMeal

EventScript_MealHotCocoa::
	setvar VAR_0x8004, 5
	msgbox Text_MealHotCocoa
	goto EventScript_ConfirmPrepareDrink

EventScript_MealEggCustard::
	setvar VAR_0x8004, 6
	msgbox Text_MealEggCustard
	goto EventScript_ConfirmCookMeal

EventScript_MealMilkCoffee::
	setvar VAR_0x8004, 7
	msgbox Text_MealMilkCoffee
	goto EventScript_ConfirmPrepareDrink

EventScript_MealSweetTea::
	setvar VAR_0x8004, 8
	msgbox Text_MealSweetTea
	goto EventScript_ConfirmPrepareDrink

EventScript_ConfirmCookMeal::
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

Text_MessKitOmelet:
	.string "Butter Omelet$"

Text_MessKitPancakes:
	.string "Pancakes$"

Text_MessKitFlatbread:
	.string "Flatbread$"

Text_MessKitSoup:
	.string "Egg Drop Soup$"

Text_MessKitCrackers:
	.string "Crackers$"

Text_MessKitCustard:
	.string "Egg Custard$"

Text_MessKitCancel:
	.string "CANCEL$"

Text_Kitchen::
	.string "It smells delicious!\n"
	.string "Somebody's been cooking here.$"

Text_KitchenSink::
	.string "It's a kitchen sink.$"

Text_KitchenFridge::
	.string "It's a refrigerator.$"

Text_PrepareMeal::
	.string "Prepare a meal?$"

Text_ChooseMeal::
	.string "What would you like to cook?$"

Text_ChooseDrink::
	.string "What would you like to prepare?$"

Text_ChooseBrew::
	.string "What would you like to brew?$"

Text_MealOmelet::
	.string "Butter Omelet: Butter, Egg, Salt,\n"
	.string "and Pepper (1 each).\p"
	.string "Catch odds +5% for 10 minutes.$"

Text_MealPancakes::
	.string "Pancakes: Flour, Egg, Water,\n"
	.string "and Butter (1 each).\p"
	.string "Battle Exp. +10% for 10 minutes.$"

Text_MealFlatbread::
	.string "Flatbread: Flour, Water, Salt,\n"
	.string "and Butter (1 each).\p"
	.string "Trainer prize money +10%\n"
	.string "for 10 minutes.$"

Text_MealSoup::
	.string "Egg Drop Soup: Egg, Water, Salt,\n"
	.string "and Pepper (1 each).\p"
	.string "Wild encounters -15%\n"
	.string "for 10 minutes.$"

Text_MealCrackers::
	.string "Crackers: Flour, Water, Salt,\n"
	.string "and Pepper (1 each).\p"
	.string "Walking friendship gains +1\n"
	.string "for 10 minutes.$"

Text_MealHotCocoa::
	.string "Hot Cocoa: Milk, Sugar, and\n"
	.string "Cocoa Powder (1 each).\p"
	.string "Walking friendship gains +2\n"
	.string "for 10 minutes.$"

Text_MealEggCustard::
	.string "Egg Custard: Egg, Milk, and\n"
	.string "Sugar (1 each).\p"
	.string "Battle Exp. +15% for 10 minutes.$"

Text_MealMilkCoffee::
	.string "Milk Coffee: Coffee Grounds,\n"
	.string "Water, and Milk (1 each).\p"
	.string "Battle Exp. +10% for 10 minutes.$"

Text_MealSweetTea::
	.string "Sweet Tea: Tea Leaves, Water,\n"
	.string "and Sugar (1 each).\p"
	.string "Catch odds +5% for 10 minutes.$"

Text_CookSelectedMeal::
	.string "Cook this meal?$"

Text_PrepareSelectedDrink::
	.string "Prepare this drink?$"

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
