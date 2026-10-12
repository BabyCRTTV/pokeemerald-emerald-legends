#!/usr/bin/env python3
"""Append the native western Kanto circuit using the shared import contract."""
from build_story_maps import main
SOURCES=['Route2','Route2_ViridianForest_NorthEntrance','Route2_ViridianForest_SouthEntrance',
 'ViridianForest','ViridianCity','ViridianCity_Gym','ViridianCity_PokemonCenter_1F','ViridianCity_Mart',
 'Route1','PalletTown','PalletTown_ProfessorOaksLab','Route21_North','Route21_South']
if __name__=='__main__':
 main(SOURCES,'data/legends_kanto_finale.json','\t.include "data/scripts/legends_kanto_chapter6.inc"')
