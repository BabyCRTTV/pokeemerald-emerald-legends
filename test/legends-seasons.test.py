"""Host regression tests compile the actual season module against engine mocks."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
COMMON = r'''
#ifndef TEST_GLOBAL_H
#define TEST_GLOBAL_H
#include <stdint.h>
#include <stddef.h>
#include <string.h>
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef int8_t s8;
typedef u32 bool32;
#define TRUE 1
#define FALSE 0
#define COMPOUND_STRING(s) ((const u8 *)(s))
#include "constants/vars.h"
#include "constants/map_types.h"
#include "constants/weather.h"
#include "constants/field_weather.h"
#define RTC_ERR_FLAG_MASK 0x0FF0
#define RTC_INIT_ERROR 1
struct SiiRtcInfo {u8 year, month, day;};
struct SaveBlock2 {u16 playTimeHours; u8 playTimeMinutes, playTimeSeconds, playTimeVBlanks;};
extern struct SaveBlock2 *gSaveBlock2Ptr;
struct MapHeader {u8 mapType; u16 regionMapSectionId; u8 weather; void *mapLayout;};
extern struct MapHeader gMapHeader;
struct Weather {u8 palProcessingState; s8 colorMapIndex;};
extern struct Weather *gWeatherPtr;
struct PaletteFade {u8 active;};
extern struct PaletteFade gPaletteFade;
extern u16 gPlttBufferUnfaded[512];
u16 VarGet(u16);
void VarSet(u16, u16);
void RtcGetInfo(struct SiiRtcInfo *);
u32 ConvertBcdToBinary(u8);
u16 RtcGetErrorStatus(void);
u16 RtcGetDayCount(struct SiiRtcInfo *);
u32 RtcGetLocalDayCount(void);
u8 GetSavedWeather(void);
void SetSavedWeather(enum OverworldWeather);
void DoCurrentWeather(void);
void ApplyWeatherColorMapIfIdle(s8);
void LoadMapTilesetPalettes(const void *);
u8 ScriptContext_IsEnabled(void);
#endif
'''
HARNESS = r'''
#include "global.h"
#include "legends_seasons.h"
#include "constants/region_map_sections.h"
#include "constants/rgb.h"
#include <assert.h>
#include <stdio.h>
struct SaveBlock2 save;
struct SaveBlock2 *gSaveBlock2Ptr = &save;
struct MapHeader gMapHeader;
struct Weather weather;
struct Weather *gWeatherPtr = &weather;
struct PaletteFade gPaletteFade;
u16 gPlttBufferUnfaded[512];
u16 vars[256], rtcError, savedWeather, reloads;
u8 month = 3, scriptActive;
u32 day = 100;
u16 VarGet(u16 v) {return vars[v - 0x4000];}
void VarSet(u16 v, u16 n) {vars[v - 0x4000] = n;}
void RtcGetInfo(struct SiiRtcInfo *r) {r->month = (month / 10) * 16 + month % 10;}
u32 ConvertBcdToBinary(u8 v) {return (v >> 4) * 10 + (v & 15);}
u16 RtcGetErrorStatus(void) {return rtcError;}
u16 RtcGetDayCount(struct SiiRtcInfo *r) {(void)r; return day;}
u32 RtcGetLocalDayCount(void) {return day;}
u8 GetSavedWeather(void) {return savedWeather;}
void SetSavedWeather(enum OverworldWeather w) {VarSet(VAR_LEGENDS_BASE_WEATHER, 0x100 + w); savedWeather = LegendsSeasonWeather(w);}
void DoCurrentWeather(void) {}
void ApplyWeatherColorMapIfIdle(s8 i) {(void)i;}
void LoadMapTilesetPalettes(const void *p) {(void)p; reloads++;}
u8 ScriptContext_IsEnabled(void) {return scriptActive;}
void setSeconds(u32 n) {VarSet(VAR_LEGENDS_SEASON_SECONDS_LO, n); VarSet(VAR_LEGENDS_SEASON_SECONDS_HI, n >> 16); VarSet(VAR_LEGENDS_SEASON_CLOCK_INIT, 1); VarSet(VAR_LEGENDS_SEASON_FRAMES, 0);}
int main(void)
{
    const u8 expected[] = {3,3,0,0,0,1,1,1,2,2,2,3};
    for (month = 1; month <= 12; month++) assert(LegendsGetSeason() == expected[month - 1]);
    // Read-only Options preview must not commit mode.
    assert(LegendsGetSeasonForMode(1) == LEGENDS_SPRING);
    assert(LegendsGetSeasonMode() == LEGENDS_SEASONS_RTC);
    LegendsSetSeasonMode(1);
    for (u32 i = 0; i < 4; i++) {
        setSeconds(i * LEGENDS_SEASON_SECONDS);
        assert(LegendsGetSeason() == i);
        setSeconds((i + 1) * LEGENDS_SEASON_SECONDS - 1);
        for (u32 frame = 0; frame < 59; frame++) LegendsSeasonTick();
        assert(LegendsGetSeason() == i);
        LegendsSeasonTick(); assert(LegendsGetSeason() == (i + 1) % 4);
    }
    // Migrate recorded playtime, then continue past the native 999-hour cap.
    memset(vars, 0, sizeof(vars)); save.playTimeHours = 999; save.playTimeMinutes = 59; save.playTimeSeconds = 59;
    LegendsSetSeasonMode(1);
    assert(LegendsGetSeason() == (999 / 28) % 4);
    setSeconds(LEGENDS_SEASON_SECONDS - 1);
    VarSet(VAR_LEGENDS_SEASON_FRAMES, 59); LegendsSeasonTick();
    assert(LegendsGetSeason() == LEGENDS_SUMMER);
    // Every persisted sub-second frame survives save/load (vars are the save).
    setSeconds(0); for (u32 i = 0; i < 31; i++) LegendsSeasonTick();
    assert(VarGet(VAR_LEGENDS_SEASON_FRAMES) == 31);
    for (u32 i = 31; i < 60; i++) LegendsSeasonTick();
    assert(VarGet(VAR_LEGENDS_SEASON_SECONDS_LO) == 1);
    LegendsSetSeasonMode(0); rtcError = RTC_INIT_ERROR;
    setSeconds(2 * LEGENDS_SEASON_SECONDS); assert(LegendsGetSeason() == LEGENDS_AUTUMN);
    rtcError = 0; month = 0; assert(LegendsGetSeason() == LEGENDS_AUTUMN); month = 10;
    gMapHeader.mapType = MAP_TYPE_ROUTE; gMapHeader.weather = WEATHER_SUNNY;
    gMapHeader.regionMapSectionId = MAPSEC_TEST_ROUTE;
    assert(LegendsMapHasSeasons());
    const u16 excluded[] = {MAPSEC_MT_CHIMNEY, MAPSEC_JAGGED_PASS, MAPSEC_FIERY_PATH, MAPSEC_LAVARIDGE_TOWN, MAPSEC_FALLARBOR_TOWN, MAPSEC_ROUTE_111, MAPSEC_ROUTE_112, MAPSEC_ROUTE_113};
    for (u32 i = 0; i < sizeof(excluded)/sizeof(*excluded); i++) {
        gMapHeader.regionMapSectionId = excluded[i]; assert(!LegendsMapHasSeasons());
        assert(LegendsSeasonWeather(WEATHER_SUNNY) == WEATHER_SUNNY);
    }
    gMapHeader.regionMapSectionId = MAPSEC_TEST_ROUTE;
    const u8 indoor[] = {MAP_TYPE_INDOOR, MAP_TYPE_UNDERGROUND, MAP_TYPE_UNDERWATER, MAP_TYPE_SECRET_BASE};
    for (u32 i = 0; i < sizeof(indoor); i++) {gMapHeader.mapType = indoor[i]; assert(!LegendsMapHasSeasons());}
    gMapHeader.mapType = MAP_TYPE_ROUTE;
    // Native special/story effects always win.
    const u8 special[] = {WEATHER_ABNORMAL, WEATHER_DROUGHT, WEATHER_DOWNPOUR, WEATHER_SANDSTORM, WEATHER_VOLCANIC_ASH, WEATHER_UNDERWATER_BUBBLES, WEATHER_NONE, WEATHER_SHADE};
    for (u32 i = 0; i < sizeof(special); i++) assert(LegendsSeasonWeather(special[i]) == special[i]);
    month = 1;
    u32 snowDays = 0;
    for (day = 1; day <= 100; day++) {
        u8 w = LegendsSeasonWeather(WEATHER_SUNNY);
        assert(w == LegendsSeasonWeather(WEATHER_SUNNY));
        snowDays += w == WEATHER_SNOW;
    }
    assert(snowDays == 60);
    gMapHeader.mapType = MAP_TYPE_OCEAN_ROUTE;
    for (day = 1; day < 20; day++) assert(LegendsSeasonWeather(WEATHER_SUNNY) != WEATHER_SNOW);
    gMapHeader.mapType = MAP_TYPE_ROUTE;
    LegendsSetSeasonMode(1);
    const u16 green = RGB(7, 22, 6), blue = RGB(8, 15, 28), gray = RGB(15, 15, 15);
    for (u32 season = 0; season < 4; season++) {
        setSeconds(season * LEGENDS_SEASON_SECONDS);
        for (u32 i = 0; i < 512; i++) gPlttBufferUnfaded[i] = green;
        gPlttBufferUnfaded[33] = blue; gPlttBufferUnfaded[34] = gray;
        LegendsApplySeasonPalette(0, 512);
        assert(gPlttBufferUnfaded[0] == green && gPlttBufferUnfaded[16] == green);
        assert(gPlttBufferUnfaded[33] == blue && gPlttBufferUnfaded[34] == gray);
        assert(gPlttBufferUnfaded[13*16] == green && gPlttBufferUnfaded[256] == green);
        assert(gPlttBufferUnfaded[35] != green && gPlttBufferUnfaded[35] < 0x8000);
    }
    // Full RGB555 domain always stays in range.
    for (u32 color = 0; color < 32768; color++) {gPlttBufferUnfaded[35] = color; LegendsApplySeasonPalette(35, 1); assert(gPlttBufferUnfaded[35] < 32768);}
    VarSet(VAR_LEGENDS_BASE_WEATHER, 0x100 + WEATHER_ABNORMAL);
    LegendsRestoreSeasonWeather(); assert(savedWeather == WEATHER_ABNORMAL);
    // Refresh waits until palette fades/scripts/weather transitions finish.
    gPaletteFade.active = 1;
    for (u32 i = 0; i < 60; i++) LegendsRefreshSeasons(); assert(reloads == 0);
    gPaletteFade.active = 0; scriptActive = 1; LegendsRefreshSeasons(); assert(reloads == 0);
    scriptActive = 0; weather.palProcessingState = WEATHER_PAL_STATE_IDLE;
    LegendsRefreshSeasons(); assert(reloads == 1);
    puts("Season calendar, timing, migration, exclusions, weather, RGB555 and refresh checks passed.");
}
'''

with tempfile.TemporaryDirectory() as directory:
    tmp = Path(directory)
    (tmp / 'global.h').write_text(COMMON)
    for header in ['event_data.h', 'field_weather.h', 'fieldmap.h', 'overworld.h', 'palette.h', 'rtc.h', 'script.h']:
        (tmp / header).write_text('#include "global.h"\n')
    (tmp / 'constants').mkdir()
    names = ['MT_CHIMNEY', 'JAGGED_PASS', 'FIERY_PATH', 'LAVARIDGE_TOWN', 'FALLARBOR_TOWN', 'ROUTE_111', 'ROUTE_112', 'ROUTE_113', 'DEWFORD_TOWN', 'PACIFIDLOG_TOWN', 'SOOTOPOLIS_CITY', 'TEST_ROUTE']
    (tmp / 'constants/region_map_sections.h').write_text('\n'.join(f'#define MAPSEC_{name} {i}' for i, name in enumerate(names)))
    (tmp / 'harness.c').write_text(HARNESS)
    subprocess.run(['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', '-Wno-misleading-indentation', '-I', str(tmp), '-I', str(ROOT / 'include'), str(ROOT / 'src/legends_seasons.c'), str(tmp / 'harness.c'), '-o', str(tmp / 'check')], check=True)
    subprocess.run([str(tmp / 'check')], check=True)
