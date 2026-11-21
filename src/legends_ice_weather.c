// Seasonal field precipitation. Each blizzard object carries several flakes,
// leaving OAM slots for trainers, grass effects and the player on busy routes.
#include "global.h"
#include "field_weather.h"
#include "sprite.h"
#include "trig.h"

static const u32 sFlurryTiles[] = INCGFX_U32("graphics/weather/flurries.png", ".4bpp");
static const u32 sHailTiles[] = INCGFX_U32("graphics/weather/hail.png", ".4bpp");
static const u32 sBlizzardTiles[] = INCGFX_U32("graphics/weather/blizzard.png", ".4bpp");

static const struct OamData sGrainOam = {
    .shape = SPRITE_SHAPE(8x8), .size = SPRITE_SIZE(8x8), .priority = 1,
};
static const struct OamData sGustOam = {
    .shape = SPRITE_SHAPE(64x32), .size = SPRITE_SIZE(64x32), .priority = 1,
};

#define x16          data[0]
#define y16          data[1]
#define fallSpeed    data[2]
#define phase        data[3]
#define windSpeed    data[4]
#define impactY      data[5]
#define bounceFrames data[6]
#define localSeed    data[7]

static void WrapParticle(struct Sprite *s, s16 xMargin, s16 yMargin)
{
    if (s->x16 < -xMargin * 16)
        s->x16 += (DISPLAY_WIDTH + 2 * xMargin) * 16;
    if (s->x16 >= (DISPLAY_WIDTH + xMargin) * 16)
        s->x16 -= (DISPLAY_WIDTH + 2 * xMargin) * 16;
    if (s->y16 >= (DISPLAY_HEIGHT + yMargin) * 16)
        s->y16 -= (DISPLAY_HEIGHT + 2 * yMargin) * 16;
    s->x = s->x16 >> 4;
    s->y = s->y16 >> 4;
}

static void DriftFlurry(struct Sprite *s)
{
    s->phase = (s->phase + 1) & 255;
    s->x16 += s->windSpeed;
    s->y16 += s->fallSpeed;
    WrapParticle(s, 8, 4);
    s->x2 = Sin(s->phase, 4);
}

static void BlowSnow(struct Sprite *s)
{
    s->phase = (s->phase + 2) & 255;
    s->x16 -= s->windSpeed + Sin(s->phase, 7);
    s->y16 += s->fallSpeed;
    WrapParticle(s, 32, 16);
}

static void FallHail(struct Sprite *s)
{
    s->x16 -= s->windSpeed;
    if (s->bounceFrames)
    {
        // Brief upward kick, then land and start another stone above the field.
        s->y16 += (6 - s->bounceFrames) * 5;
        if (--s->bounceFrames == 0)
        {
            u16 seed = s->localSeed * 109u + 89;
            s->localSeed = seed;
            s->x16 = (seed % DISPLAY_WIDTH) * 16;
            s->y16 = -4 * 16;
            s->impactY = 18 + (seed >> 8) % (DISPLAY_HEIGHT - 18);
        }
    }
    else
    {
        s->y16 += s->fallSpeed;
        if (s->y16 >= s->impactY * 16)
        {
            s->y16 = s->impactY * 16;
            s->bounceFrames = 11;
        }
    }
    WrapParticle(s, 4, 4);
}

struct IceEffect
{
    struct SpriteSheet sheet;
    struct SpriteTemplate sprite;
    u8 count, tilesPerFrame, fall, wind;
};
static const struct IceEffect sFlurries = {
    {sFlurryTiles, sizeof(sFlurryTiles), GFXTAG_ICE_PARTICLES},
    {.tileTag = GFXTAG_ICE_PARTICLES, .paletteTag = PALTAG_WEATHER, .oam = &sGrainOam, .callback = DriftFlurry},
    7, 1, 5, 2,
};
static const struct IceEffect sHail = {
    {sHailTiles, sizeof(sHailTiles), GFXTAG_ICE_PARTICLES},
    {.tileTag = GFXTAG_ICE_PARTICLES, .paletteTag = PALTAG_WEATHER, .oam = &sGrainOam, .callback = FallHail},
    18, 1, 49, 7,
};
static const struct IceEffect sBlizzard = {
    {sBlizzardTiles, sizeof(sBlizzardTiles), GFXTAG_ICE_PARTICLES},
    {.tileTag = GFXTAG_ICE_PARTICLES, .paletteTag = PALTAG_WEATHER, .oam = &sGustOam, .callback = BlowSnow},
    24, 32, 20, 42,
};

static void InitIceEffect(const struct IceEffect *effect)
{
    Shade_InitVars();
    // SetNextWeather may cancel a transition and reinitialize the active effect.
    if (gWeatherPtr->snowflakeSpriteCount)
        return;
    if (GetSpriteTileStartByTag(GFXTAG_ICE_PARTICLES) == TAG_NONE)
        LoadSpriteSheet(&effect->sheet);
    if (GetSpriteTileStartByTag(GFXTAG_ICE_PARTICLES) == TAG_NONE)
        return;
    // Keep eight free OBJ slots for walking effects and newly visible map objects.
    u32 available = 0;
    for (u32 i = 0; i < MAX_SPRITES; i++)
        if (!gSprites[i].inUse)
            available++;
    for (u32 i = 0; i < effect->count && i + 8 < available; i++)
    {
        u32 id = CreateSpriteAtEndUnchecked(&effect->sprite, 0, 0, 78);
        if (id == MAX_SPRITES)
            break;
        struct Sprite *s = &gSprites[id];
        u16 seed = 0x467B + i * 7919;
        s->localSeed = seed;
        s->phase = (i * 71) & 255;
        s->fallSpeed = effect->fall + (i % 5);
        s->windSpeed = effect->wind + (i % 7);
        s->impactY = 18 + (seed >> 8) % (DISPLAY_HEIGHT - 18);
        s->x = (i * 89 + 17) % DISPLAY_WIDTH;
        s->y = (i * 57 + 31) % (effect == &sHail ? s->impactY : DISPLAY_HEIGHT);
        if (effect == &sBlizzard && i < 20)
        {
            // Stagger the broad banks so a gust fills the viewport even on a
            // bright winter route. Four independent foreground groups cross them.
            u32 row = i / 5, col = i % 5;
            s->x = -28 + 60 * col + (row * 19 % 43);
            s->y = -14 + 48 * row + (col * 13 % 26);
            s->phase = row * 63;
            s->windSpeed = 38 + 3 * row;
            s->fallSpeed = 20;
        }
        s->x16 = s->x * 16;
        s->y16 = s->y * 16;
        s->oam.tileNum = s->sheetTileStart + (i % 3) * effect->tilesPerFrame;
        s->animBeginning = FALSE;
        s->animPaused = TRUE;
        gWeatherPtr->sprites.s1.snowflakeSprites[gWeatherPtr->snowflakeSpriteCount++] = s;
    }
}

void Flurries_Init(void) { InitIceEffect(&sFlurries); }
void Hail_Init(void) { InitIceEffect(&sHail); }
void Blizzard_Init(void) { InitIceEffect(&sBlizzard); }

bool8 IceParticles_Finish(void)
{
    while (gWeatherPtr->snowflakeSpriteCount)
        DestroySprite(gWeatherPtr->sprites.s1.snowflakeSprites[--gWeatherPtr->snowflakeSpriteCount]);
    FreeSpriteTilesByTag(GFXTAG_ICE_PARTICLES);
    return FALSE;
}
