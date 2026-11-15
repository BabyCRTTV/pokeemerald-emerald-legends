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
	msgbox Text_NoMealIngredients
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

Text_NoMealIngredients::
	.string "There aren't any cooking ingredients\n"
	.string "available yet.$"
