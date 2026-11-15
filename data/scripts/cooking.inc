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
	msgbox Text_PrepareMeal, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, EventScript_FinishMealInteraction
EventScript_ChooseMeal::
	message Text_ChooseMeal
	waitmessage
	multichoice 0, 0, MULTI_LEGENDS_MEALS, FALSE
	copyvar VAR_0x8004, VAR_RESULT
	switch VAR_RESULT
	case 0, EventScript_MealOmelet
	case 1, EventScript_MealPancakes
	case 2, EventScript_MealFlatbread
	case 3, EventScript_MealSoup
	case 4, EventScript_MealCrackers
	goto EventScript_FinishMealInteraction

EventScript_MealOmelet::
	msgbox Text_MealOmelet
	goto EventScript_ConfirmCookMeal

EventScript_MealPancakes::
	msgbox Text_MealPancakes
	goto EventScript_ConfirmCookMeal

EventScript_MealFlatbread::
	msgbox Text_MealFlatbread
	goto EventScript_ConfirmCookMeal

EventScript_MealSoup::
	msgbox Text_MealSoup
	goto EventScript_ConfirmCookMeal

EventScript_MealCrackers::
	msgbox Text_MealCrackers
	goto EventScript_ConfirmCookMeal

EventScript_ConfirmCookMeal::
	msgbox Text_CookSelectedMeal, MSGBOX_YESNO
	goto_if_ne VAR_RESULT, YES, EventScript_ChooseMeal
	callnative Script_LegendsCookMeal
	goto_if_eq VAR_RESULT, 0, EventScript_CookMissingSupplies
	goto_if_eq VAR_RESULT, 2, EventScript_CookBagFull
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	msgbox Text_CookSuccess
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

Text_CookSelectedMeal::
	.string "Cook this meal?$"

Text_CookSuccess::
	.string "You cooked {STR_VAR_1}!\n"
	.string "It's in the FOOD pocket.$"

Text_CookMissingSupplies::
	.string "You're missing some ingredients.\n"
	.string "Try a POKé MART's COOKING SUPPLIES.$"

Text_CookBagFull::
	.string "There's no room in your BAG.$"
