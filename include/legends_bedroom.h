#ifndef GUARD_LEGENDS_BEDROOM_H
#define GUARD_LEGENDS_BEDROOM_H
#define BEDROOM_COLOR_COUNT 7
#define BEDROOM_MATERIAL_RUG 0
#define BEDROOM_MATERIAL_BED 1
#define BEDROOM_MATERIAL_CHAIR 2
bool32 LegendsBedroomIsHome(void);
bool32 LegendsBedroomIsMap(void);
u8 LegendsBedroomColor(u8 material);
void LegendsBedroomSetColor(u8 material, u8 color);
void LegendsBedroomLoadPalette(bool8 skipFaded);
void LegendsBedroomApply(void);
bool32 LegendsBedroomCanPlace(s16 x, s16 y, u8 width, u8 height);
bool32 LegendsBedroomSavedPosition(s16 x, s16 y);
void LegendsBedroomIsHomeSpecial(void);
void LegendsBedroomMomMessage(void);
#endif
