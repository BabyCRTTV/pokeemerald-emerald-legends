LegendsWyrmtide_Isle_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Wyrmtide_Landing
	map_script MAP_SCRIPT_ON_LOAD, LegendsWyrmtide_Isle_OnLoad
	.byte 0
LegendsWyrmtide_Isle_OnLoad:
	call Wyrmtide_SealOnLoad
	end
