LegendsBedroom_OnLoad:
	special LegendsBedroomApply
	end

LegendsBedroom_Notebook:
	special LegendsBedroomIsHomeSpecial
	goto_if_eq VAR_RESULT, FALSE, LegendsBedroom_NotebookOriginal
	lockall
	msgbox PlayersHouse_2F_Text_Notebook, MSGBOX_DEFAULT
	goto_if_unset FLAG_BADGE01_GET, LegendsBedroom_NotebookEnd
	msgbox LegendsBedroom_Text_ReadMemories, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LegendsBedroom_NotebookEnd
	call_if_set FLAG_BADGE01_GET, LegendsBedroom_MemoryFirst
	call_if_set FLAG_BADGE05_GET, LegendsBedroom_MemoryNorman
	call_if_set FLAG_SYS_GAME_CLEAR, LegendsBedroom_MemoryChampion
	call_if_set FLAG_LEGENDS_KANTO_WELCOMED, LegendsBedroom_MemoryKanto
	call_if_set FLAG_LEGENDS_KANTO_SURVEY_REPORT, LegendsBedroom_MemorySurvey
	call_if_set FLAG_LEGENDS_KANTO_SURVEY_POWER_REPORT, LegendsBedroom_MemoryPower
	call_if_set FLAG_LEGENDS_STORY_SEAFOAM_REPORT, LegendsBedroom_MemorySeafoam
	call_if_set FLAG_LEGENDS_STORY_WEATHER_REPORT, LegendsBedroom_MemoryContinent
	call_if_set FLAG_LEGENDS_STORY_NORTH_REPORT, LegendsBedroom_MemoryNorth
	call_if_set FLAG_LEGENDS_STORY_EMBER_REPORT, LegendsBedroom_MemoryEmber
	call_if_set FLAG_LEGENDS_FINAL_EIGHT_RECORDS, LegendsBedroom_MemoryRecords
	call_if_set FLAG_LEGENDS_FINAL_ISLAND_VISITED, LegendsBedroom_MemoryIsland
	call_if_set FLAG_LEGENDS_FINAL_HOENN_EPILOGUE, LegendsBedroom_MemoryHome
LegendsBedroom_NotebookEnd:
	releaseall
	end
LegendsBedroom_NotebookOriginal:
	msgbox PlayersHouse_2F_Text_Notebook, MSGBOX_SIGN
	end
LegendsBedroom_Text_ReadMemories:
	.string "Read the pages of home memories?$"

LegendsBedroom_MemoryFirst:
	msgbox LegendsBedroom_Text_First, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_First:
	.string "FIRST STEPS\nMom left flowers after my first BADGE.$"

LegendsBedroom_MemoryNorman:
	msgbox LegendsBedroom_Text_Norman, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_Norman:
	.string "A PROUD FAMILY\nDad's BADGE. A silver gift from home.$"

LegendsBedroom_MemoryChampion:
	msgbox LegendsBedroom_Text_Champion, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_Champion:
	.string "HOME OF A CHAMPION\nA gold display, and a warm welcome.$"

LegendsBedroom_MemoryKanto:
	msgbox LegendsBedroom_Text_Kanto, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_Kanto:
	.string "LETTERS FROM KANTO\nA new region. The same place to return.$"

LegendsBedroom_MemorySurvey:
	msgbox LegendsBedroom_Text_Survey, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_Survey:
	.string "THE WING SURVEY\nMy first report. A BALL POSTER at home.$"

LegendsBedroom_MemoryPower:
	msgbox LegendsBedroom_Text_Power, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_Power:
	.string "THE QUIET CURRENT\nZAPDOS observed. A habitat understood.$"

LegendsBedroom_MemorySeafoam:
	msgbox LegendsBedroom_Text_Seafoam, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_Seafoam:
	.string "STILLWATER WINGS\nARTICUNO's refuge. The report is filed.$"

LegendsBedroom_MemoryContinent:
	msgbox LegendsBedroom_Text_Continent, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_Continent:
	.string "THE SLEEPING CONTINENT\nWith STEVEN and BIRCH, HOENN is safe.$"

LegendsBedroom_MemoryNorth:
	msgbox LegendsBedroom_Text_North, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_North:
	.string "STONE AND TIDE\nNorthern rivers and old mountain paths.$"

LegendsBedroom_MemoryEmber:
	msgbox LegendsBedroom_Text_Ember, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_Ember:
	.string "EMBER'S PASSAGE\nMOLTRES's summit. Three bird reports.$"

LegendsBedroom_MemoryRecords:
	msgbox LegendsBedroom_Text_Records, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_Records:
	.string "EIGHT VISITING RECORDS\nKANTO's Leaders recognized my journey.$"

LegendsBedroom_MemoryIsland:
	msgbox LegendsBedroom_Text_Island, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_Island:
	.string "BEYOND THE HORIZON\nThe voyage to FARAWAY ISLAND.$"

LegendsBedroom_MemoryHome:
	msgbox LegendsBedroom_Text_Home, MSGBOX_DEFAULT
	return
LegendsBedroom_Text_Home:
	.string "HOMEWARD BOUND\nBIRCH's letter. A room of memories.$"
