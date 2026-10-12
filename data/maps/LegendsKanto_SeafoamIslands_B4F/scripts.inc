

LegendsKanto_SeafoamIslands_B4F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LegendsSeafoam_B4F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, LegendsStory_Articuno_OnResume
	map_script MAP_SCRIPT_ON_LOAD, LegendsSeafoam_B4F_OnLoad
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, LegendsSeafoam_B4F_OnWarp
	map_script MAP_SCRIPT_ON_FRAME_TABLE, LegendsSeafoam_B4F_OnFrame
	.byte 0

LegendsSeafoam_B4F_OnTransition::
	call LegendsSeafoam_Init
	setrespawn HEAL_LOCATION_LEGENDS_KANTO_VERMILION
	call_if_unset FLAG_LEGENDS_STORY_SEAFOAM_B4F_CURRENT, LegendsSeafoam_B4F_EventScript_CheckStoppedCurrent
	call_if_set FLAG_LEGENDS_STORY_SEAFOAM_B4F_CURRENT, LegendsSeafoam_B4F_EventScript_SetNoCurrentLayout
	end

LegendsSeafoam_B4F_EventScript_CheckStoppedCurrent::
	setvar VAR_TEMP_2, 0
	call_if_unset FLAG_LEGENDS_STORY_SEAFOAM_B4F_BOULDER_1, LegendsSeafoam_B4F_EventScript_AddBoulderPresent
	call_if_unset FLAG_LEGENDS_STORY_SEAFOAM_B4F_BOULDER_2, LegendsSeafoam_B4F_EventScript_AddBoulderPresent
	call_if_eq VAR_TEMP_2, 2, LegendsSeafoam_B4F_EventScript_StoppedCurrent
	return

LegendsSeafoam_B4F_EventScript_StoppedCurrent::
	setflag FLAG_LEGENDS_STORY_SEAFOAM_B4F_CURRENT
	return

LegendsSeafoam_B4F_EventScript_SetNoCurrentLayout::
	setmaplayoutindex LAYOUT_LEGENDS_KANTO_SEAFOAM_ISLANDS_B4F_CURRENT_STOPPED
	return

LegendsSeafoam_B4F_OnLoad::
	setvar VAR_TEMP_2, 0
	call_if_unset FLAG_LEGENDS_STORY_SEAFOAM_B4F_BOULDER_1, LegendsSeafoam_B4F_EventScript_AddBoulderPresent
	call_if_unset FLAG_LEGENDS_STORY_SEAFOAM_B4F_BOULDER_2, LegendsSeafoam_B4F_EventScript_AddBoulderPresent
	goto_if_eq VAR_TEMP_2, 2, LegendsSeafoam_B4F_EventScript_SetCalmWaterNearStairs
	end

LegendsSeafoam_B4F_EventScript_SetCalmWaterNearStairs::
	setmetatile 12, 14, METATILE_GeneralFrlg_CalmWater, 0
	setmetatile 13, 14, METATILE_GeneralFrlg_CalmWater, 0
	end

LegendsSeafoam_B4F_OnWarp::
	map_script_2 VAR_LEGENDS_SEAFOAM_ENTRY, 1, LegendsSeafoam_B4F_EventScript_WarpInOnCurrent
	.2byte 0

LegendsSeafoam_B4F_EventScript_WarpInOnCurrent::
	turnobject LOCALID_PLAYER, DIR_NORTH
	special ForcePlayerToStartSurfing
	end

LegendsSeafoam_B4F_OnFrame::
	map_script_2 VAR_LEGENDS_SEAFOAM_ENTRY, 1, LegendsSeafoam_B4F_EventScript_EnterOnCurrent
	map_script_2 VAR_TEMP_1, 1, LegendsSeafoam_B4F_EventScript_EnterByFalling
	.2byte 0

@ The current the player is forced in on from B3F
LegendsSeafoam_B4F_EventScript_EnterOnCurrent::
	lockall
	applymovement LOCALID_PLAYER, LegendsSeafoam_B4F_Movement_EnterOnCurrent
	waitmovement 0
	setvar VAR_LEGENDS_SEAFOAM_ENTRY, 0
	releaseall
	end

LegendsSeafoam_B4F_Movement_EnterOnCurrent::
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

@ The current the player lands on when entering the map by falling
LegendsSeafoam_B4F_EventScript_EnterByFalling::
	lockall
	setvar VAR_TEMP_2, 0
	call_if_unset FLAG_LEGENDS_STORY_SEAFOAM_B4F_BOULDER_1, LegendsSeafoam_B4F_EventScript_AddBoulderPresent
	call_if_unset FLAG_LEGENDS_STORY_SEAFOAM_B4F_BOULDER_2, LegendsSeafoam_B4F_EventScript_AddBoulderPresent
	goto_if_eq VAR_TEMP_2, 2, LegendsSeafoam_B4F_EventScript_CurrentBlocked
	getplayerxy VAR_0x8008, VAR_0x8009
	call_if_lt VAR_0x8008, 9, LegendsSeafoam_B4F_EventScript_RideCurrentFar
	call_if_ge VAR_0x8008, 9, LegendsSeafoam_B4F_EventScript_RideCurrentClose
	special SeafoamIslandsB4F_CurrentDumpsPlayerOnLand
	setvar VAR_TEMP_1, 0
	releaseall
	end

LegendsSeafoam_B4F_EventScript_AddBoulderPresent::
	addvar VAR_TEMP_2, 1
	return

LegendsSeafoam_B4F_EventScript_RideCurrentFar::
	applymovement LOCALID_PLAYER, LegendsSeafoam_B4F_Movement_RideCurrentFar
	waitmovement 0
	return

LegendsSeafoam_B4F_EventScript_RideCurrentClose::
	applymovement LOCALID_PLAYER, LegendsSeafoam_B4F_Movement_RideCurrentClose
	waitmovement 0
	return

LegendsSeafoam_B4F_EventScript_CurrentBlocked::
	setvar VAR_TEMP_1, 0
	releaseall
	end

LegendsSeafoam_B4F_Movement_RideCurrentFar::
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	walk_up
	step_end

LegendsSeafoam_B4F_Movement_RideCurrentClose::
	walk_up
	walk_up
	walk_up
	walk_right
	walk_right
	walk_right
	walk_up
	step_end

@ Triggers blocking re-entry to B3F
LegendsSeafoam_B4F_EventScript_UpwardCurrent::
	lockall
	applymovement LOCALID_PLAYER, LegendsSeafoam_B4F_Movement_WalkUp
	waitmovement 0
	releaseall
	end

LegendsSeafoam_B4F_Movement_WalkUp::
	walk_up
	step_end
