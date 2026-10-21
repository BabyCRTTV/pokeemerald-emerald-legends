@ Review build: exploration, seasonal visitors and clues only.
@ Capture, reward and replenishment rules await owner review.
LegendsGrotto_OnTransition::
	special LegendsGrottoPrepareVisitor
	end

LegendsGrotto_EnterLeafshade::
	lockall
	msgbox LegendsGrotto_Text_LeafshadeEntry, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsGrotto_Decline
	closemessage
	warp MAP_LEGENDS_GROTTO_LEAFSHADE, 9, 11
	waitstate
	releaseall
	end
LegendsGrotto_EnterStillwater::
	lockall
	msgbox LegendsGrotto_Text_StillwaterEntry, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsGrotto_Decline
	closemessage
	warp MAP_LEGENDS_GROTTO_STILLWATER, 9, 11
	waitstate
	releaseall
	end
LegendsGrotto_EnterRainroot::
	lockall
	msgbox LegendsGrotto_Text_RainrootEntry, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsGrotto_Decline
	closemessage
	warp MAP_LEGENDS_GROTTO_RAINROOT, 9, 11
	waitstate
	releaseall
	end
LegendsGrotto_Decline::
	closemessage
	releaseall
	end

LegendsGrotto_ExitLeafshade::
	lockall
	warp MAP_PETALBURG_WOODS, 13, 32
	waitstate
	releaseall
	end
LegendsGrotto_ExitStillwater::
	lockall
	warp MAP_ROUTE114, 14, 40
	waitstate
	releaseall
	end
LegendsGrotto_ExitRainroot::
	lockall
	warp MAP_ROUTE119, 27, 106
	waitstate
	releaseall
	end

LegendsGrotto_Visitor::
	lock
	faceplayer
	special LegendsGrottoPrepareVisitor
	playmoncry VAR_0x8004, CRY_MODE_NORMAL
	msgbox LegendsGrotto_Text_Visitor, MSGBOX_DEFAULT
	waitmoncry
	release
	end
LegendsGrotto_Find::
	lock
	msgbox LegendsGrotto_Text_Find, MSGBOX_DEFAULT
	release
	end
LegendsGrotto_ClueLeafshade::
	msgbox LegendsGrotto_Text_LeafshadeClue, MSGBOX_SIGN
	end
LegendsGrotto_ClueStillwater::
	msgbox LegendsGrotto_Text_StillwaterClue, MSGBOX_SIGN
	end
LegendsGrotto_ClueRainroot::
	msgbox LegendsGrotto_Text_RainrootClue, MSGBOX_SIGN
	end

LegendsGrotto_Text_LeafshadeEntry:
	.string "Vines frame a gap in the trunk.\n"
	.string "A narrow trail leads out of sight.\p"
	.string "Explore LEAFSHADE HOLLOW?$"
LegendsGrotto_Text_StillwaterEntry:
	.string "A cool draft rises from the crack.\n"
	.string "You can hear water dripping inside.\p"
	.string "Explore STILLWATER NOOK?$"
LegendsGrotto_Text_RainrootEntry:
	.string "The rain has parted the undergrowth.\n"
	.string "Small footprints lead beneath it.\p"
	.string "Explore RAINROOT HOLLOW?$"
LegendsGrotto_Text_Visitor:
	.string "{STR_VAR_1} watches you quietly.\n"
	.string "It seems at home in this shelter.$"
LegendsGrotto_Text_Find:
	.string "Something has been tucked away here.\n"
	.string "You leave it undisturbed for now.$"
LegendsGrotto_Text_LeafshadeClue:
	.string "Nibbled berries lie under the leaves.\n"
	.string "The smallest prints end at the roots.$"
LegendsGrotto_Text_StillwaterClue:
	.string "The stone is worn smooth on one side.\n"
	.string "The water beneath it is still clear.$"
LegendsGrotto_Text_RainrootClue:
	.string "Rain gathers in the curled leaves.\n"
	.string "Something has made a dry bed below.$"
