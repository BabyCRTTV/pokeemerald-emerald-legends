LegendsPoffin_Machine::
	lockall
	msgbox Poffin_Intro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Poffin_View
	special LegendsPoffinHasRoom
	goto_if_eq VAR_RESULT, 0, Poffin_Full
	msgbox Poffin_First, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	closemessage
	special Bag_ChooseBerry
	goto_if_eq VAR_ITEM_ID, 0, Poffin_End
	copyvar VAR_0x8004, VAR_ITEM_ID
	setvar VAR_0x8005, 0
	msgbox Poffin_Second, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Poffin_Cook
	fadescreen FADE_TO_BLACK
	closemessage
	special Bag_ChooseBerry
	goto_if_eq VAR_ITEM_ID, 0, Poffin_End
	copyvar VAR_0x8005, VAR_ITEM_ID
Poffin_Cook:
	closemessage
	special LegendsCookPoffin
	goto_if_eq VAR_RESULT, 0, Poffin_Short
	goto Poffin_End
Poffin_Full:
	msgbox Poffin_FullText, MSGBOX_DEFAULT
Poffin_View:
	msgbox Poffin_ViewText, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Poffin_End
	fadescreen FADE_TO_BLACK
	closemessage
	special LegendsOpenTreatCase
	goto Poffin_End
Poffin_Short:
	msgbox Poffin_ShortText, MSGBOX_DEFAULT
Poffin_End:
	releaseall
	end
Poffin_Intro:
	.string "It's a POFFIN MAKER!\nCook a batch of POFFINS?$"
Poffin_First:
	.string "Pick a BERRY for the batter.$"
Poffin_Second:
	.string "Mix in a second BERRY?$"
Poffin_ViewText:
	.string "Open the treat case?$"
Poffin_FullText:
	.string "The treat case is full.$"
Poffin_ShortText:
	.string "There aren't enough BERRIES or\nspace for this batch.$"
