#ifndef GUARD_LEGENDS_WEATHER_H
#define GUARD_LEGENDS_WEATHER_H

#define LEGENDS_WEATHER_PERIOD_SECONDS (20 * 60)
#define LEGENDS_WEATHER_CYCLE_SECONDS (18 * 60 * 60)

u8 LegendsChooseAmbientWeather(u8 weather);
void LegendsAdvanceWeatherClock(void);
void LegendsWeatherTick(void);

#endif
