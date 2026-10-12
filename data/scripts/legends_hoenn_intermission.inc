@ Intermission: The Sleeping Continent. Separate from Emerald's weather crisis.
LegendsHoenn_Journal::
	msgbox LegendsHoenn_Text_Directions, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_Scientist::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_SUMMONED, LegendsHoenn_BeforeCall
	goto_if_set FLAG_LEGENDS_STORY_WEATHER_REPORT, LegendsHoenn_AfterReport
	goto_if_set FLAG_LEGENDS_STORY_REGIGIGAS_CALMED, LegendsHoenn_FileReport
	goto_if_set FLAG_LEGENDS_STORY_WEATHER_STARTED, LegendsHoenn_Reminder
	msgbox LegendsHoenn_Text_Intro, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_WEATHER_STARTED
LegendsHoenn_Reminder::
	msgbox LegendsHoenn_Text_Directions, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_BeforeCall::
	msgbox LegendsHoenn_Text_Before, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_FileReport::
	msgbox LegendsHoenn_Text_Report, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_WEATHER_REPORT
LegendsHoenn_AfterReport::
	msgbox LegendsHoenn_Text_After, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_RainReading::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_STARTED, LegendsStory_Locked
	goto_if_set FLAG_LEGENDS_STORY_WEATHER_RAIN_READING, LegendsHoenn_RainDone
	msgbox LegendsHoenn_Text_RainOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	msgbox LegendsHoenn_Text_Rain, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_WEATHER_RAIN_READING
LegendsHoenn_RainDone::
	msgbox LegendsHoenn_Text_RainDone, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_HeatReading::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_STARTED, LegendsStory_Locked
	goto_if_set FLAG_LEGENDS_STORY_WEATHER_HEAT_READING, LegendsHoenn_HeatDone
	msgbox LegendsHoenn_Text_HeatOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	msgbox LegendsHoenn_Text_Heat, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_WEATHER_HEAT_READING
LegendsHoenn_HeatDone::
	msgbox LegendsHoenn_Text_HeatDone, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_FaultEntrance::
	lockall
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_STARTED, LegendsHoenn_EntranceClosed
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_RAIN_READING, LegendsHoenn_NeedReadings
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_HEAT_READING, LegendsHoenn_NeedReadings
	msgbox LegendsHoenn_Text_Enter, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	closemessage
	fadescreen FADE_TO_BLACK
	warp MAP_LEGENDS_HOENN_CONTINENTAL_VAULT, 8, 27
	waitstate
	releaseall
	end
LegendsHoenn_EntranceClosed::
	msgbox LegendsHoenn_Text_Closed, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_NeedReadings::
	msgbox LegendsHoenn_Text_NeedReadings, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_Vault_OnLoad::
	call_if_unset FLAG_LEGENDS_STORY_VAULT_ROCK, LegendsHoenn_CloseVault
	call_if_unset FLAG_LEGENDS_STORY_VAULT_ICE, LegendsHoenn_CloseVault
	call_if_unset FLAG_LEGENDS_STORY_VAULT_STEEL, LegendsHoenn_CloseVault
	end
LegendsHoenn_CloseVault::
	setmetatile 7, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 8, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 9, 19, METATILE_Cave_EntranceCover, TRUE
	setmetatile 7, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 8, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	setmetatile 9, 20, METATILE_Cave_SealedChamberBraille_Mid, TRUE
	return
LegendsHoenn_VaultHint::
	lockall
	msgbox LegendsHoenn_Text_VaultHint, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_OpenVault::
	goto_if_unset FLAG_LEGENDS_STORY_VAULT_ROCK, LegendsStory_Return
	goto_if_unset FLAG_LEGENDS_STORY_VAULT_ICE, LegendsStory_Return
	goto_if_unset FLAG_LEGENDS_STORY_VAULT_STEEL, LegendsStory_Return
	msgbox LegendsHoenn_Text_Door, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 2
	setvar VAR_0x8005, 1
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 3
	special ShakeScreen
	waitstate
	setmetatile 7, 19, METATILE_Cave_SealedChamberEntrance_TopLeft, FALSE
	setmetatile 8, 19, METATILE_Cave_SealedChamberEntrance_TopMid, FALSE
	setmetatile 9, 19, METATILE_Cave_SealedChamberEntrance_TopRight, FALSE
	setmetatile 7, 20, METATILE_Cave_SealedChamberEntrance_BottomLeft, FALSE
	setmetatile 8, 20, METATILE_Cave_SealedChamberEntrance_BottomMid, FALSE
	setmetatile 9, 20, METATILE_Cave_SealedChamberEntrance_BottomRight, FALSE
	special DrawWholeMapView
	releaseall
	end
LegendsHoenn_Regigigas::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_VAULT_ROCK, LegendsHoenn_NeedReadings
	goto_if_unset FLAG_LEGENDS_STORY_VAULT_ICE, LegendsHoenn_NeedReadings
	goto_if_unset FLAG_LEGENDS_STORY_VAULT_STEEL, LegendsHoenn_NeedReadings
	goto_if_set FLAG_LEGENDS_STORY_REGIGIGAS_CAUGHT, LegendsStory_Return
	msgbox LegendsHoenn_Text_Ready, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	goto_if_set FLAG_LEGENDS_STORY_REGIGIGAS_AWAKENED, LegendsHoenn_RegigigasBattle
	msgbox LegendsHoenn_Text_Awakening, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 3
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 24
	setvar VAR_0x8007, 3
	special ShakeScreen
	waitstate
	fadescreen FADE_TO_WHITE
	delay 24
	fadescreen FADE_FROM_WHITE
	playmoncry SPECIES_REGIGIGAS, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox LegendsHoenn_Text_Titan, MSGBOX_DEFAULT
	setflag FLAG_LEGENDS_STORY_REGIGIGAS_AWAKENED
LegendsHoenn_RegigigasBattle::
	closemessage
	setwildbattle SPECIES_REGIGIGAS, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special StartRegiBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, LegendsHoenn_RegigigasCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, LegendsHoenn_RegigigasCalmed
	removeobject 1
	msgbox LegendsHoenn_Text_Retry, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_RegigigasCaught::
	setflag FLAG_LEGENDS_STORY_REGIGIGAS_CAUGHT
	removeobject 1
LegendsHoenn_RegigigasCalmed::
	setflag FLAG_LEGENDS_STORY_REGIGIGAS_CALMED
	msgbox LegendsHoenn_Text_Calmed, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_Vault_OnResume::
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, LegendsHoenn_CheckCatch
	end
LegendsHoenn_CheckCatch::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	setflag FLAG_LEGENDS_STORY_REGIGIGAS_CAUGHT
	setflag FLAG_LEGENDS_STORY_REGIGIGAS_CALMED
	removeobject 1
	return
LegendsHoenn_AnchorRock::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_RAIN_READING, LegendsHoenn_NeedReadings
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_HEAT_READING, LegendsHoenn_NeedReadings
	goto_if_set FLAG_LEGENDS_STORY_VAULT_ROCK, LegendsHoenn_AnchorRockDone
	msgbox LegendsHoenn_Text_AnchorRock, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	playse SE_PIN
	setflag FLAG_LEGENDS_STORY_VAULT_ROCK
	msgbox LegendsHoenn_Text_AnchorRockDone, MSGBOX_DEFAULT
	goto LegendsHoenn_OpenVault
LegendsHoenn_AnchorRockDone::
	msgbox LegendsHoenn_Text_AnchorRockDone, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_Text_AnchorRock:
	.string "The stone regulator vibrates in time\n"
	.string "with the ground reading. Release its\p"
	.string "trapped pressure?$"

LegendsHoenn_Text_AnchorRockDone:
	.string "The stone pulse steadies. The floor\n"
	.string "carries the pressure away from the old\p"
	.string "seal.$"

LegendsHoenn_AnchorIce::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_RAIN_READING, LegendsHoenn_NeedReadings
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_HEAT_READING, LegendsHoenn_NeedReadings
	goto_if_set FLAG_LEGENDS_STORY_VAULT_ICE, LegendsHoenn_AnchorIceDone
	msgbox LegendsHoenn_Text_AnchorIce, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	playse SE_PIN
	setflag FLAG_LEGENDS_STORY_VAULT_ICE
	msgbox LegendsHoenn_Text_AnchorIceDone, MSGBOX_DEFAULT
	goto LegendsHoenn_OpenVault
LegendsHoenn_AnchorIceDone::
	msgbox LegendsHoenn_Text_AnchorIceDone, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_Text_AnchorIce:
	.string "The frost regulator repeats the\n"
	.string "river's cold pulse. Open its blocked\p"
	.string "channel?$"

LegendsHoenn_Text_AnchorIceDone:
	.string "Cold air moves through the open vent.\n"
	.string "Frost retreats from the inscription.$"

LegendsHoenn_AnchorSteel::
	lockall
	faceplayer
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_RAIN_READING, LegendsHoenn_NeedReadings
	goto_if_unset FLAG_LEGENDS_STORY_WEATHER_HEAT_READING, LegendsHoenn_NeedReadings
	goto_if_set FLAG_LEGENDS_STORY_VAULT_STEEL, LegendsHoenn_AnchorSteelDone
	msgbox LegendsHoenn_Text_AnchorSteel, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsStory_Return
	playse SE_PIN
	setflag FLAG_LEGENDS_STORY_VAULT_STEEL
	msgbox LegendsHoenn_Text_AnchorSteelDone, MSGBOX_DEFAULT
	goto LegendsHoenn_OpenVault
LegendsHoenn_AnchorSteelDone::
	msgbox LegendsHoenn_Text_AnchorSteelDone, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_Text_AnchorSteel:
	.string "The metal regulator rings like the\n"
	.string "Institute's gauge. Ground the\p"
	.string "repeated signal?$"

LegendsHoenn_Text_AnchorSteelDone:
	.string "The metallic echo fades. Three steady\n"
	.string "notes answer from behind the wall.$"

LegendsHoenn_Text_Before:
	.string "I compare distant habitat reports\n"
	.string "with HOENN's weather readings. The\p"
	.string "WEATHER INSTITUTE's ordinary\n"
	.string "research continues upstairs.$"

LegendsHoenn_Text_Intro:
	.string "FIELD SCIENTIST: BIRCH sent your\n"
	.string "KANTO notes. These new HOENN pulses\p"
	.string "began deep beneath the central\n"
	.string "volcanic belt.\p"
	.string "RAYQUAZA ended the old crisis.\n"
	.string "GROUDON and KYOGRE remain quiet. The\p"
	.string "instruments point to trapped\n"
	.string "pressure, not another battle between\p"
	.string "them.\p"
	.string "Rain surges along ROUTE 119. The\n"
	.string "desert's ground temperature on ROUTE\p"
	.string "111 drops at the same moment. Collect\n"
	.string "both readings before entering the\p"
	.string "fault.$"

LegendsHoenn_Text_Directions:
	.string "The Sleeping Continent. Find our river\n"
	.string "scientist just south of the WEATHER\p"
	.string "INSTITUTE on ROUTE 119.\p"
	.string "Find our desert scientist by ROUTE\n"
	.string "111's northern desert entrance. Both\p"
	.string "readings can be collected in either\n"
	.string "order.\p"
	.string "Enter FIERY PATH from ROUTE 112.\n"
	.string "Examine the marked eastern rock face\p"
	.string "at the south end of the main passage.\n"
	.string "The fault entrance lies beside the\p"
	.string "southern doorway.\p"
	.string "Deep inside, restore the stone, frost\n"
	.string "and metal regulators. Return here\p"
	.string "after calming the source. Your normal\n"
	.string "field-move permissions remain intact.$"

LegendsHoenn_Text_RainOffer:
	.string "The river gauge leaps, then falls\n"
	.string "silent. Record a full pressure cycle?$"

LegendsHoenn_Text_Rain:
	.string "Thunder breaks over an empty sky. The\n"
	.string "gauge repeats the same three pulses,\p"
	.string "even when the rain eases.\p"
	.string "The pulse arrives through the ground\n"
	.string "before it reaches the river. You\p"
	.string "record its timing for the buried\n"
	.string "regulators.$"

LegendsHoenn_Text_RainDone:
	.string "ROUTE 119's rain cycle is recorded. The\n"
	.string "ground pulse precedes the river surge.$"

LegendsHoenn_Text_HeatOffer:
	.string "The desert's buried probe chills while\n"
	.string "the surface stays hot. Record the\p"
	.string "ground-temperature cycle?$"

LegendsHoenn_Text_Heat:
	.string "A cool breath escapes between the\n"
	.string "stones. The probe repeats the river\p"
	.string "gauge's three pulses.\p"
	.string "The two readings converge beneath\n"
	.string "FIERY PATH. An old chamber is\p"
	.string "releasing pressure through the\n"
	.string "central rock, not through the sea.$"

LegendsHoenn_Text_HeatDone:
	.string "ROUTE 111's ground cycle is recorded.\n"
	.string "The FIERY PATH fault lies between\p"
	.string "both readings.$"

LegendsHoenn_Text_Closed:
	.string "A deep seam crosses this wall. A faint\n"
	.string "three-note echo rises from the rock.\p"
	.string "The WEATHER INSTITUTE may recognize\n"
	.string "it.$"

LegendsHoenn_Text_NeedReadings:
	.string "Compare both field readings and\n"
	.string "restore all three regulators before\p"
	.string "approaching the source. The Institute\n"
	.string "scientist keeps your directions.$"

LegendsHoenn_Text_Enter:
	.string "The readings match this marked seam. A\n"
	.string "narrow passage opens behind the rock.\p"
	.string "Enter the CONTINENTAL VAULT?$"

LegendsHoenn_Text_VaultHint:
	.string "STONE, FROST, METAL. Three regulators\n"
	.string "ring around the sealed passage.\p"
	.string "Examine each after collecting both\n"
	.string "field readings.$"

LegendsHoenn_Text_Door:
	.string "Three notes become one. The old seal\n"
	.string "slides aside. A slow, heavy heartbeat\p"
	.string "answers from the chamber above.$"

LegendsHoenn_Text_Ready:
	.string "A colossal figure waits beyond the\n"
	.string "seal. Prepare for REGIGIGAS at Lv. 70?\p"
	.string "Win or capture it to settle the fault.\p"
	.string "If you flee or lose, you can return and\n"
	.string "retry. You may capture it later if you\p"
	.string "first defeat it. This encounter uses\n"
	.string "its normal ability.$"

LegendsHoenn_Text_Awakening:
	.string "The floor heaves. Dust rises in three\n"
	.string "spirals. The stone, frost and metal\p"
	.string "lights flare together.\p"
	.string "A vast hand presses against the wall.\n"
	.string "Moss shakes loose from an ancient\p"
	.string "body. Its lights open in the dark.$"

LegendsHoenn_Text_Titan:
	.string "REGIGIGAS rises! The three pulses\n"
	.string "become a single deep roar.\p"
	.string "The regulators were repeating its\n"
	.string "restless movements through the fault.\p"
	.string "Face the awakened titan and give the\n"
	.string "chamber a chance to settle!$"

LegendsHoenn_Text_Retry:
	.string "REGIGIGAS withdraws into the deep\n"
	.string "chamber. The fault is still unsettled.\p"
	.string "Reenter the vault to face it again.$"

LegendsHoenn_Text_Calmed:
	.string "The giant lowers its arms. The\n"
	.string "chamber's pulse settles into the\p"
	.string "rhythm of the earth.\p"
	.string "Far above, the storm breaks. The\n"
	.string "unnatural pressure has eased. Return\p"
	.string "to the WEATHER INSTITUTE with your\n"
	.string "findings.$"

LegendsHoenn_Text_Report:
	.string "FIELD SCIENTIST: The gauges are\n"
	.string "steady. You traced the echo to\p"
	.string "REGIGIGAS and freed the blocked\n"
	.string "regulators.\p"
	.string "The old crisis left these buried\n"
	.string "channels unstable. We found a local\p"
	.string "aftereffect, not a return of GROUDON\n"
	.string "and KYOGRE.\p"
	.string "BIRCH will monitor the fault. OAK has\n"
	.string "your report. Your KANTO survey can\p"
	.string "continue with MISTY and BROCK.$"

LegendsHoenn_Text_After:
	.string "HOENN's abnormal readings have\n"
	.string "settled. Ordinary seasons and weather\p"
	.string "continue. Return to OAK's aide in\n"
	.string "VERMILION FAN CLUB for Stone and\p"
	.string "Tide.$"


LegendsHoenn_StevenVisibility::
	setflag FLAG_LEGENDS_STORY_HIDE_STEVEN
	call_if_set FLAG_LEGENDS_STORY_WEATHER_STARTED, LegendsHoenn_ShowSteven
	return
LegendsHoenn_ShowSteven::
	clearflag FLAG_LEGENDS_STORY_HIDE_STEVEN
	return
LegendsHoenn_Steven::
	lockall
	faceplayer
	goto_if_set FLAG_LEGENDS_STORY_REGIGIGAS_CALMED, LegendsHoenn_StevenAfter
	msgbox LegendsHoenn_Text_Steven, MSGBOX_DEFAULT
	goto LegendsHoenn_FaultEntrance
LegendsHoenn_StevenAfter::
	msgbox LegendsHoenn_Text_StevenAfter, MSGBOX_DEFAULT
	releaseall
	end
LegendsHoenn_Text_Steven:
	.string "STEVEN: I followed the pulse through\n"
	.string "this rock. The seam beside the south\p"
	.string "exit leads beneath the central fault.\p"
	.string "Those carvings resemble the ancient\n"
	.string "REGI chambers. We should restore the\p"
	.string "regulators before disturbing whatever\n"
	.string "sleeps beyond the seal.$"

LegendsHoenn_Text_StevenAfter:
	.string "STEVEN: The stone has stopped\n"
	.string "trembling. You gave an ancient\p"
	.string "POKEMON room to rest.\p"
	.string "The WEATHER INSTITUTE needs your\n"
	.string "findings. I will watch this seam while\p"
	.string "you continue the KANTO survey.$"
