LegendsDayOff_PondProp::
	setvar VAR_0x8004, DAY_OFF_POND
	goto LegendsDayOff_OpenProp

LegendsDayOff_ShoreProp::
	setvar VAR_0x8004, DAY_OFF_SHORE
	goto LegendsDayOff_OpenProp

LegendsDayOff_WoodsProp::
	setvar VAR_0x8004, DAY_OFF_WOODS
	goto LegendsDayOff_OpenProp

LegendsDayOff_WorkshopProp::
	setvar VAR_0x8004, DAY_OFF_WORKSHOP

LegendsDayOff_OpenProp:
	lock
	specialvar VAR_RESULT, LegendsDayOffHasFollower
	goto_if_eq VAR_RESULT, FALSE, LegendsDayOff_NeedsFollower
	bufferlivemonnickname STR_VAR_1
	applymovement OBJ_EVENT_ID_FOLLOWER, LegendsDayOff_FacePlayer
	waitmovement OBJ_EVENT_ID_FOLLOWER
	goto_if_eq VAR_0x8004, DAY_OFF_WORKSHOP, LegendsDayOff_WashMenu
	goto_if_eq VAR_0x8004, DAY_OFF_WOODS, LegendsDayOff_HideMenu
	multichoice 0, 0, MULTI_LEGENDS_DAY_OFF_PLAY, FALSE
	goto LegendsDayOff_Choice

LegendsDayOff_HideMenu:
	multichoice 0, 0, MULTI_LEGENDS_DAY_OFF_HIDE, FALSE
	goto LegendsDayOff_Choice

LegendsDayOff_WashMenu:
	multichoice 0, 0, MULTI_LEGENDS_DAY_OFF_WASH, FALSE
LegendsDayOff_Choice:
	goto_if_ne VAR_RESULT, 0, LegendsDayOff_End
	specialvar VAR_0x8005, LegendsDayOffGetReaction
	goto_if_eq VAR_0x8004, DAY_OFF_WOODS, LegendsDayOff_Hide
	goto_if_eq VAR_0x8004, DAY_OFF_WORKSHOP, LegendsDayOff_Wash
	goto_if_eq VAR_0x8004, DAY_OFF_POND, LegendsDayOff_Pond
	msgbox LegendsDayOff_Text_Shore
	goto LegendsDayOff_Throw

LegendsDayOff_Pond::
	msgbox LegendsDayOff_Text_Pond
LegendsDayOff_Throw:
	closemessage
	setvar VAR_0x8007, 0
	special LegendsDayOffSkipStone
	playse SE_PUDDLE
	delay 10
	setvar VAR_0x8007, 1
	special LegendsDayOffSkipStone
	playse SE_PUDDLE
	delay 18
	goto_if_eq VAR_0x8005, DAY_OFF_SHY, LegendsDayOff_SkipShy
	goto_if_eq VAR_0x8005, DAY_OFF_WATER, LegendsDayOff_SkipWater
	loadword 0, LegendsDayOff_Text_SkipKeen
	goto LegendsDayOff_Celebrate

LegendsDayOff_SkipShy:
	applymovement OBJ_EVENT_ID_FOLLOWER, LegendsDayOff_Peek
	waitmovement OBJ_EVENT_ID_FOLLOWER
	loadword 0, LegendsDayOff_Text_SkipShy
	goto LegendsDayOff_Celebrate

LegendsDayOff_SkipWater:
	special LegendsDayOffSplashBack
	delay 5
	loadword 0, LegendsDayOff_Text_SkipWater
	goto LegendsDayOff_Celebrate

LegendsDayOff_Hide::
	msgbox LegendsDayOff_Text_Hide
	closemessage
	hideobjectat OBJ_EVENT_ID_FOLLOWER, MAP_PETALBURG_WOODS
	specialvar VAR_0x8006, LegendsDayOffPickHidingPlace
	delay 24
	playse SE_FU_ZAKU
	goto_if_eq VAR_0x8006, 0, LegendsDayOff_RootsClue
	message LegendsDayOff_Text_FernsClue
	goto LegendsDayOff_Seek

LegendsDayOff_RootsClue:
	message LegendsDayOff_Text_RootsClue
LegendsDayOff_Seek:
	waitmessage
	multichoice 0, 0, MULTI_LEGENDS_DAY_OFF_SEEK, FALSE
	closemessage
	goto_if_eq VAR_RESULT, MULTI_B_PRESSED, LegendsDayOff_StopSeeking
	showobjectat OBJ_EVENT_ID_FOLLOWER, MAP_PETALBURG_WOODS
	goto_if_ne VAR_RESULT, VAR_0x8006, LegendsDayOff_SeekMiss
	goto_if_eq VAR_0x8005, DAY_OFF_GRASS, LegendsDayOff_SeekGrass
	loadword 0, LegendsDayOff_Text_SeekFound
	goto LegendsDayOff_Celebrate

LegendsDayOff_StopSeeking:
	showobjectat OBJ_EVENT_ID_FOLLOWER, MAP_PETALBURG_WOODS
	msgbox LegendsDayOff_Text_SeekStop
	goto LegendsDayOff_End

LegendsDayOff_SeekMiss:
	loadword 0, LegendsDayOff_Text_SeekMiss
	goto LegendsDayOff_Celebrate

LegendsDayOff_SeekGrass:
	loadword 0, LegendsDayOff_Text_SeekGrass
	goto LegendsDayOff_Celebrate

LegendsDayOff_Wash::
	msgbox LegendsDayOff_Text_Wash
	closemessage
	goto_if_eq VAR_0x8005, DAY_OFF_SHY, LegendsDayOff_GentleWash
	goto_if_eq VAR_0x8005, DAY_OFF_FIRE, LegendsDayOff_DampCloth
	special LegendsDayOffWashEffect
	playse SE_PUDDLE
	delay 12
	special LegendsDayOffWashEffect
	goto_if_eq VAR_0x8005, DAY_OFF_WATER, LegendsDayOff_WashWater
	loadword 0, LegendsDayOff_Text_WashClean
	goto LegendsDayOff_Celebrate

LegendsDayOff_DampCloth:
	special LegendsDayOffWashEffect
	loadword 0, LegendsDayOff_Text_WashFire
	goto LegendsDayOff_Celebrate

LegendsDayOff_GentleWash:
	applymovement OBJ_EVENT_ID_FOLLOWER, LegendsDayOff_Peek
	waitmovement OBJ_EVENT_ID_FOLLOWER
	special LegendsDayOffWashEffect
	playse SE_PUDDLE
	loadword 0, LegendsDayOff_Text_WashShy
	goto LegendsDayOff_Celebrate

LegendsDayOff_WashWater:
	loadword 0, LegendsDayOff_Text_WashWater
LegendsDayOff_Celebrate:
	applymovement OBJ_EVENT_ID_FOLLOWER, LegendsDayOff_Hop
	delay 8
	special LegendsDayOffHeart
	playfirstmoncry
	message 0x0
	waitmessage
	waitmovement OBJ_EVENT_ID_FOLLOWER
	waitbuttonpress
LegendsDayOff_End:
	release
	end

LegendsDayOff_NeedsFollower:
	msgbox LegendsDayOff_Text_NeedsFollower
	goto LegendsDayOff_End

LegendsDayOff_Text_NeedsFollower::
	.string "Bring a walking POKéMON\n"
	.string "along to try this together.$"

LegendsDayOff_FacePlayer:
	face_player
	step_end

LegendsDayOff_Peek:
	face_away_player
	delay_16
	face_player
	step_end

LegendsDayOff_Hop:
	lock_facing_direction
	jump_in_place_down
	unlock_facing_direction
	face_player
	step_end

LegendsDayOff_Text_Pond::
	.string "You pick a flat stone from the pile\n"
	.string "beside ROUTE 102's pond.$"

LegendsDayOff_Text_Shore::
	.string "You choose a smooth, flat stone\n"
	.string "from the pile on DEWFORD's shore.$"

LegendsDayOff_Text_SkipKeen::
	.string "{STR_VAR_1} hops at each plip,\n"
	.string "then noses another stone your way.$"

LegendsDayOff_Text_SkipShy::
	.string "{STR_VAR_1} flinches at the splash,\n"
	.string "then leans in for the next one.$"

LegendsDayOff_Text_SkipWater::
	.string "{STR_VAR_1} splashes right back!\n"
	.string "You both end up a little wetter.$"

LegendsDayOff_Text_Hide::
	.string "You cover your eyes and count to\n"
	.string "three. Ready or not…$"

LegendsDayOff_Text_RootsClue::
	.string "Something rustles under the big\n"
	.string "tree roots. Where will you look?$"

LegendsDayOff_Text_FernsClue::
	.string "The ferns twitch. The air is still.\n"
	.string "Where will you look?$"

LegendsDayOff_Text_SeekFound::
	.string "Found you! {STR_VAR_1} pops out\n"
	.string "with a leaf stuck to its head.$"

LegendsDayOff_Text_SeekGrass::
	.string "Found you! {STR_VAR_1}'s colors\n"
	.string "almost passed for fallen leaves.$"

LegendsDayOff_Text_SeekMiss::
	.string "Nothing there! {STR_VAR_1} pops out\n"
	.string "behind you before you can turn.$"

LegendsDayOff_Text_SeekStop::
	.string "{STR_VAR_1} comes out of hiding\n"
	.string "and trots back to your side.$"

LegendsDayOff_Text_Wash::
	.string "There's a bucket of clean water\n"
	.string "beside the GLASS WORKSHOP.$"

LegendsDayOff_Text_WashClean::
	.string "Gray ash swirls into the bucket.\n"
	.string "{STR_VAR_1} shakes itself dry.$"

LegendsDayOff_Text_WashFire::
	.string "You wipe the ash off {STR_VAR_1}\n"
	.string "with a damp cloth. All clean!$"

LegendsDayOff_Text_WashShy::
	.string "{STR_VAR_1} hangs back at first,\n"
	.string "then lets you rinse the ash off.$"

LegendsDayOff_Text_WashWater::
	.string "{STR_VAR_1} gives a big shake.\n"
	.string "Now you need the towel, too!$"
