LegendsKanto_Harbor_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LegendsKanto_Harbor_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, LegendsKanto_Harbor_OnFrame
	.byte 0

LegendsKanto_Harbor_OnTransition:
	setrespawn HEAL_LOCATION_LEGENDS_KANTO_VERMILION
	setescapewarp MAP_LEGENDS_KANTO_VERMILION_CITY, 23, 33
	end

LegendsKanto_Harbor_OnFrame:
	map_script_2 VAR_TEMP_0, 0, LegendsKanto_EventScript_FirstWelcome
	.2byte 0
