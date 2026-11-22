#ifndef GUARD_LEGENDS_GROTTO_REVIEW_H
#define GUARD_LEGENDS_GROTTO_REVIEW_H

bool32 LegendsGrottoIsEntrance(s16 x, s16 y);

void LegendsGrottoResetMotion(void);
void LegendsGrottoTickMotion(void);
const u16 *LegendsGrottoMotionTiles(s32 x, s32 y, u16 metatile, const u16 *tiles);

#endif
