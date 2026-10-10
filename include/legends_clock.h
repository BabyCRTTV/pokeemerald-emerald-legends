#ifndef GUARD_LEGENDS_CLOCK_H
#define GUARD_LEGENDS_CLOCK_H
void LegendsClockTick(void);
void LegendsClockCalcLocalTime(void);
void LegendsClockSetManual(u8 hour, u8 minute);
void LegendsClockBufferTime(void);
void LegendsClockUseRealTime(void);
#endif
