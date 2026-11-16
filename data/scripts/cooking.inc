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
	message Text_ChooseKitchenRecipe
	waitmessage
	dynmultichoice 0, 0, FALSE, 6, 0, DYN_MULTICHOICE_CB_NONE, Text_CookingMenuOmelet, Text_CookingMenuPancakes, Text_CookingMenuFlatbread, Text_CookingMenuSoup, Text_CookingMenuCrackers, Text_CookingMenuHotCocoa, Text_CookingMenuCustard, Text_CookingMenuTomatoFlatbread, Text_CookingMenuButteredPotatoes, Text_CookingMenuCarrotSoup, Text_CookingMenuOnionTart, Text_CookingMenuApplePancakes, Text_CookingMenuPotatoHash, Text_CookingMenuEggnog, Text_CookingMenuSpicedCider, Text_CookingMenuIcedCinnamonCoffee, Text_CookingMenuGarlicRicePilaf, Text_CookingMenuTomatoRice, Text_CookingMenuLemonShortbread, Text_CookingMenuVanillaPudding, Text_CookingMenuIcedLemonade, Text_CookingMenuVanillaLatte, Text_CancelCooking
	switch VAR_RESULT
	case 0, EventScript_MealOmelet
	case 1, EventScript_MealPancakes
	case 2, EventScript_MealFlatbread
	case 3, EventScript_MealSoup
	case 4, EventScript_MealCrackers
	case 5, EventScript_MealHotCocoa
	case 6, EventScript_MealEggCustard
	case 7, EventScript_MealTomatoFlatbread
	case 8, EventScript_MealButteredPotatoes
	case 9, EventScript_MealCarrotSoup
	case 10, EventScript_MealOnionTart
	case 11, EventScript_MealApplePancakes
	case 12, EventScript_MealPotatoHash
	case 13, EventScript_MealEggnog
	case 14, EventScript_MealSpicedCider
	case 15, EventScript_MealIcedCinnamonCoffee
	case 16, EventScript_MealGarlicRicePilaf
	case 17, EventScript_MealTomatoRice
	case 18, EventScript_MealLemonShortbread
	case 19, EventScript_MealVanillaPudding
	case 20, EventScript_MealIcedLemonade
	case 21, EventScript_MealVanillaLatte
	goto EventScript_FinishMealInteraction

EventScript_ChooseCanteenDrink::
	message Text_ChooseDrink
	waitmessage
	multichoice 0, 0, MULTI_LEGENDS_CANTEEN, FALSE
	switch VAR_RESULT
	case 0, EventScript_MealHotCocoa
	case 1, EventScript_MealEggnog
	case 2, EventScript_MealSpicedCider
	case 3, EventScript_MealIcedLemonade
	goto EventScript_FinishMealInteraction

EventScript_ChooseMessKitMeal::
	message Text_ChooseMeal
	waitmessage
	dynmultichoice 0, 0, FALSE, 6, 0, DYN_MULTICHOICE_CB_NONE, Text_CookingMenuOmelet, Text_CookingMenuPancakes, Text_CookingMenuFlatbread, Text_CookingMenuSoup, Text_CookingMenuCrackers, Text_CookingMenuCustard, Text_CookingMenuTomatoFlatbread, Text_CookingMenuButteredPotatoes, Text_CookingMenuCarrotSoup, Text_CookingMenuOnionTart, Text_CookingMenuApplePancakes, Text_CookingMenuPotatoHash, Text_CookingMenuGarlicRicePilaf, Text_CookingMenuTomatoRice, Text_CookingMenuLemonShortbread, Text_CookingMenuVanillaPudding, Text_CancelCooking
	switch VAR_RESULT
	case 0, EventScript_MealOmelet
	case 1, EventScript_MealPancakes
	case 2, EventScript_MealFlatbread
	case 3, EventScript_MealSoup
	case 4, EventScript_MealCrackers
	case 5, EventScript_MealEggCustard
	case 6, EventScript_MealTomatoFlatbread
	case 7, EventScript_MealButteredPotatoes
	case 8, EventScript_MealCarrotSoup
	case 9, EventScript_MealOnionTart
	case 10, EventScript_MealApplePancakes
	case 11, EventScript_MealPotatoHash
	case 12, EventScript_MealGarlicRicePilaf
	case 13, EventScript_MealTomatoRice
	case 14, EventScript_MealLemonShortbread
	case 15, EventScript_MealVanillaPudding
	goto EventScript_FinishMealInteraction

EventScript_ChoosePercolatorDrink::
	message Text_ChooseBrew
	waitmessage
	dynmultichoice 0, 0, FALSE, 6, 0, DYN_MULTICHOICE_CB_NONE, Text_BrewMenuMilkCoffee, Text_BrewMenuSweetTea, Text_BrewMenuMatchaLatte, Text_BrewMenuBrewedOolong, Text_BrewMenuBrewedBlackTea, Text_BrewMenuBlackCoffee, Text_BrewMenuHojichaLatte, Text_BrewMenuHojichaTea, Text_CookingMenuIcedCinnamonCoffee, Text_CookingMenuVanillaLatte, Text_CancelCooking
	switch VAR_RESULT
	case 0, EventScript_MealMilkCoffee
	case 1, EventScript_MealSweetTea
	case 2, EventScript_MealMatchaLatte
	case 3, EventScript_MealBrewedOolong
	case 4, EventScript_MealBrewedBlackTea
	case 5, EventScript_MealBlackCoffee
	case 6, EventScript_MealHojichaLatte
	case 7, EventScript_MealHojichaTea
	case 8, EventScript_MealIcedCinnamonCoffee
	case 9, EventScript_MealVanillaLatte
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

EventScript_MealMatchaLatte::
	setvar VAR_0x8004, 9
	msgbox Text_MealMatchaLatte
	goto EventScript_ConfirmPrepareDrink

EventScript_MealBrewedOolong::
	setvar VAR_0x8004, 10
	msgbox Text_MealBrewedOolong
	goto EventScript_ConfirmPrepareDrink

EventScript_MealBrewedBlackTea::
	setvar VAR_0x8004, 11
	msgbox Text_MealBrewedBlackTea
	goto EventScript_ConfirmPrepareDrink

EventScript_MealBlackCoffee::
	setvar VAR_0x8004, 12
	msgbox Text_MealBlackCoffee
	goto EventScript_ConfirmPrepareDrink

EventScript_MealHojichaLatte::
	setvar VAR_0x8004, 13
	msgbox Text_MealHojichaLatte
	goto EventScript_ConfirmPrepareDrink

EventScript_MealHojichaTea::
	setvar VAR_0x8004, 14
	msgbox Text_MealHojichaTea
	goto EventScript_ConfirmPrepareDrink

EventScript_MealTomatoFlatbread::
	setvar VAR_0x8004, 15
	msgbox Text_MealTomatoFlatbread
	goto EventScript_ConfirmCookMeal

EventScript_MealButteredPotatoes::
	setvar VAR_0x8004, 16
	msgbox Text_MealButteredPotatoes
	goto EventScript_ConfirmCookMeal

EventScript_MealCarrotSoup::
	setvar VAR_0x8004, 17
	msgbox Text_MealCarrotSoup
	goto EventScript_ConfirmCookMeal

EventScript_MealOnionTart::
	setvar VAR_0x8004, 18
	msgbox Text_MealOnionTart
	goto EventScript_ConfirmCookMeal

EventScript_MealApplePancakes::
	setvar VAR_0x8004, 19
	msgbox Text_MealApplePancakes
	goto EventScript_ConfirmCookMeal

EventScript_MealPotatoHash::
	setvar VAR_0x8004, 20
	msgbox Text_MealPotatoHash
	goto EventScript_ConfirmCookMeal

EventScript_MealEggnog::
	setvar VAR_0x8004, 21
	msgbox Text_MealEggnog
	goto EventScript_ConfirmPrepareDrink

EventScript_MealSpicedCider::
	setvar VAR_0x8004, 22
	msgbox Text_MealSpicedCider
	goto EventScript_ConfirmPrepareDrink

EventScript_MealIcedCinnamonCoffee::
	setvar VAR_0x8004, 23
	msgbox Text_MealIcedCinnamonCoffee
	goto EventScript_ConfirmPrepareDrink

EventScript_MealGarlicRicePilaf::
	setvar VAR_0x8004, 24
	msgbox Text_MealGarlicRicePilaf
	goto EventScript_ConfirmCookMeal

EventScript_MealTomatoRice::
	setvar VAR_0x8004, 25
	msgbox Text_MealTomatoRice
	goto EventScript_ConfirmCookMeal

EventScript_MealLemonShortbread::
	setvar VAR_0x8004, 26
	msgbox Text_MealLemonShortbread
	goto EventScript_ConfirmCookMeal

EventScript_MealVanillaPudding::
	setvar VAR_0x8004, 27
	msgbox Text_MealVanillaPudding
	goto EventScript_ConfirmCookMeal

EventScript_MealIcedLemonade::
	setvar VAR_0x8004, 28
	msgbox Text_MealIcedLemonade
	goto EventScript_ConfirmPrepareDrink

EventScript_MealVanillaLatte::
	setvar VAR_0x8004, 29
	msgbox Text_MealVanillaLatte
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

Text_CookingMenuOmelet:
	.string "Butter Omelet$"

Text_CookingMenuPancakes:
	.string "Pancakes$"

Text_CookingMenuFlatbread:
	.string "Flatbread$"

Text_CookingMenuSoup:
	.string "Egg Drop Soup$"

Text_CookingMenuCrackers:
	.string "Crackers$"

Text_CookingMenuCustard:
	.string "Egg Custard$"

Text_CookingMenuTomatoFlatbread:
	.string "Tomato Flatbread$"

Text_CookingMenuButteredPotatoes:
	.string "Buttered Potatoes$"

Text_CookingMenuHotCocoa:
	.string "Hot Cocoa$"

Text_CookingMenuCarrotSoup:
	.string "Carrot Soup$"

Text_CookingMenuOnionTart:
	.string "Onion Tart$"

Text_CookingMenuApplePancakes:
	.string "Apple Pancakes$"

Text_CookingMenuPotatoHash:
	.string "Potato Hash$"

Text_CookingMenuEggnog:
	.string "Eggnog$"

Text_CookingMenuSpicedCider:
	.string "Spiced Cider$"

Text_CookingMenuIcedCinnamonCoffee:
	.string "Iced Cinnamon Brew$"

Text_CookingMenuGarlicRicePilaf:
	.string "Garlic Rice Pilaf$"

Text_CookingMenuTomatoRice:
	.string "Tomato Rice$"

Text_CookingMenuLemonShortbread:
	.string "Lemon Shortbread$"

Text_CookingMenuVanillaPudding:
	.string "Vanilla Pudding$"

Text_CookingMenuIcedLemonade:
	.string "Iced Lemonade$"

Text_CookingMenuVanillaLatte:
	.string "Vanilla Latte$"

Text_CancelCooking:
	.string "CANCEL$"

Text_BrewMenuMilkCoffee:
	.string "Milk Coffee$"

Text_BrewMenuSweetTea:
	.string "Sweet Tea$"

Text_BrewMenuMatchaLatte:
	.string "Matcha Latte$"

Text_BrewMenuBrewedOolong:
	.string "Brewed Oolong$"

Text_BrewMenuBrewedBlackTea:
	.string "Brewed Black Tea$"

Text_BrewMenuBlackCoffee:
	.string "Black Coffee$"

Text_BrewMenuHojichaLatte:
	.string "Hojicha Latte$"

Text_BrewMenuHojichaTea:
	.string "Hojicha Tea$"

Text_Kitchen::
	.string "It smells delicious!\n"
	.string "Somebody's been cooking here.$"

Text_KitchenSink::
	.string "It's a kitchen sink.$"

Text_KitchenFridge::
	.string "It's a refrigerator.$"

Text_PrepareMeal::
	.string "Prepare a meal?$"

Text_ChooseKitchenRecipe::
	.string "What will you prepare?$"

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

Text_MealMatchaLatte::
	.string "Matcha Latte: Matcha Powder,\nWater, and Milk (1 each).\p"
	.string "Walking friendship gains +2\nfor 10 minutes.$"

Text_MealBrewedOolong::
	.string "Brewed Oolong: Oolong Tea and\nWater (1 each).\p"
	.string "Wild encounters -10%\nfor 10 minutes.$"

Text_MealBrewedBlackTea::
	.string "Brewed Black Tea: Black Tea and\nWater (1 each).\p"
	.string "Trainer prize money +10%\nfor 10 minutes.$"

Text_MealBlackCoffee::
	.string "Black Coffee: Coffee and\nWater (1 each).\p"
	.string "Battle Exp. +10% for 10 minutes.$"

Text_MealHojichaLatte::
	.string "Hojicha Latte: Hojicha Powder,\nWater, and Milk (1 each).\p"
	.string "Walking friendship gains +2\nfor 10 minutes.$"

Text_MealHojichaTea::
	.string "Hojicha Tea: Hojicha Leaves\nand Water (1 each).\p"
	.string "Walking friendship gains +1\nfor 10 minutes.$"

Text_MealTomatoFlatbread::
	.string "Tomato Flatbread: Flour, Water,\n"
	.string "Tomato, and Cheese (1 each).\p"
	.string "Trainer prize money +15%\n"
	.string "for 10 minutes.$"

Text_MealButteredPotatoes::
	.string "Buttered Potatoes: Potato,\n"
	.string "Butter, and Salt (1 each).\p"
	.string "Wild encounters -10%\n"
	.string "for 10 minutes.$"

Text_MealCarrotSoup::
	.string "Carrot Soup\p"
	.string "Carrot, Onion,\n"
	.string "Water, and Salt (1 each).\p"
	.string "Wild encounters -15%\n"
	.string "for 10 minutes.$"

Text_MealOnionTart::
	.string "Onion Tart\p"
	.string "Onion, Cheese,\n"
	.string "Flour, and Butter (1 each).\p"
	.string "Trainer prize money +15%\n"
	.string "for 10 minutes.$"

Text_MealApplePancakes::
	.string "Apple Pancakes\p"
	.string "Apple, Flour,\n"
	.string "Egg, and Butter (1 each).\p"
	.string "Battle Exp. +15%\n"
	.string "for 10 minutes.$"

Text_MealPotatoHash::
	.string "Potato Hash\p"
	.string "Potato, Onion,\n"
	.string "Butter, and Pepper (1 each).\p"
	.string "Catch odds +5%\n"
	.string "for 10 minutes.$"

Text_MealEggnog::
	.string "Eggnog\p"
	.string "Egg, Milk, Sugar,\n"
	.string "and Cinnamon (1 each).\p"
	.string "Walking friendship gains +2\n"
	.string "for 10 minutes.$"

Text_MealSpicedCider::
	.string "Spiced Cider\p"
	.string "Apple, Water,\n"
	.string "Cinnamon, and Sugar (1 each).\p"
	.string "Trainer prize money +10%\n"
	.string "for 10 minutes.$"

Text_MealIcedCinnamonCoffee::
	.string "Iced Cinnamon Brew\p"
	.string "Coffee Grounds, Water,\n"
	.string "Cinnamon, and Ice Cubes (1 each).\p"
	.string "Battle Exp. +10%\n"
	.string "for 10 minutes.$"

Text_MealGarlicRicePilaf::
	.string "Garlic Rice Pilaf\p"
	.string "Rice, Garlic, Butter,\n"
	.string "and Onion (1 each).\p"
	.string "Wild encounters -15%\n"
	.string "for 10 minutes.$"

Text_MealTomatoRice::
	.string "Tomato Rice\p"
	.string "Rice, Tomato, Onion,\n"
	.string "and Salt (1 each).\p"
	.string "Trainer prize money +10%\n"
	.string "for 10 minutes.$"

Text_MealLemonShortbread::
	.string "Lemon Shortbread\p"
	.string "Lemon, Flour, Butter,\n"
	.string "and Sugar (1 each).\p"
	.string "Catch odds +5%\n"
	.string "for 10 minutes.$"

Text_MealVanillaPudding::
	.string "Vanilla Pudding\p"
	.string "Rice, Milk, Vanilla,\n"
	.string "and Sugar (1 each).\p"
	.string "Walking friendship gains +2\n"
	.string "for 10 minutes.$"

Text_MealIcedLemonade::
	.string "Iced Lemonade\p"
	.string "Lemon, Water, Sugar,\n"
	.string "and Ice Cubes (1 each).\p"
	.string "Walking friendship gains +1\n"
	.string "for 10 minutes.$"

Text_MealVanillaLatte::
	.string "Vanilla Latte\p"
	.string "Coffee Grounds, Water,\n"
	.string "Milk, and Vanilla (1 each).\p"
	.string "Battle Exp. +15%\n"
	.string "for 10 minutes.$"

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
