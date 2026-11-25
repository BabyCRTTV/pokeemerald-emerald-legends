#include "global.h"
#include "fieldmap.h"
#include "legends_johto.h"
#include "malloc.h"
#include "tilesets.h"
#include "constants/event_objects.h"

#if !IS_FRLG
// SaveMapView writes a 15x14 rectangle into a 256-word buffer. A marker
// just past that rectangle distinguishes the revised map collision on Continue.
#define JOHTO_VIEW_MARKER_INDEX (MAP_OFFSET_W * MAP_OFFSET_H)
#define JOHTO_VIEW_REVISION 0x4A01
STATIC_ASSERT(JOHTO_VIEW_MARKER_INDEX < ARRAY_COUNT(gSaveBlock1Ptr->mapView), JohtoViewMarkerFits);

// Each point belongs to the connected footpath on that specific map.
static const struct UCoords8 sTrailAnchors[] =
{
    [MAP_NUM(MAP_LEGENDS_JOHTO_ROUTE26)] = {16, 9},
    [MAP_NUM(MAP_LEGENDS_JOHTO_ROUTE27_EAST)] = {8, 11},
    [MAP_NUM(MAP_LEGENDS_JOHTO_ROUTE27_WEST)] = {23, 11},
    [MAP_NUM(MAP_LEGENDS_JOHTO_NEW_BARK_TOWN)] = {11, 10},
    [MAP_NUM(MAP_LEGENDS_JOHTO_ROUTE29)] = {18, 10},
    [MAP_NUM(MAP_LEGENDS_JOHTO_CHERRYGROVE_CITY)] = {10, 18},
    [MAP_NUM(MAP_LEGENDS_JOHTO_ROUTE30)] = {14, 31},
    [MAP_NUM(MAP_LEGENDS_JOHTO_ROUTE31)] = {17, 22},
    [MAP_NUM(MAP_LEGENDS_JOHTO_VIOLET_CITY)] = {20, 10},
    [MAP_NUM(MAP_LEGENDS_JOHTO_ROUTE32)] = {14, 50},
    [MAP_NUM(MAP_LEGENDS_JOHTO_ROUTE33)] = {19, 10},
    [MAP_NUM(MAP_LEGENDS_JOHTO_AZALEA_TOWN)] = {10, 10},
};

static s32 DistanceToSavedPlayer(s32 x, s32 y)
{
    s32 dx = x - gSaveBlock1Ptr->pos.x;
    s32 dy = y - gSaveBlock1Ptr->pos.y;
    return dx * dx + dy * dy;
}

static struct Coords16 FindResumeTile(const struct MapLayout *layout, const struct UCoords8 *anchor, bool32 surfing)
{
    struct Coords16 nearest = {anchor->x, anchor->y};
    s32 best = 0x7FFFFFFF;
    s32 stride = layout->width + 2;
    s32 cells = stride * (layout->height + 2);
    // A zero border makes every cardinal neighbor of an interior tile safe to inspect.
    u16 *queue = AllocZeroed(cells * (sizeof(u16) + sizeof(u8)));
    if (queue == NULL)
        return surfing ? gSaveBlock1Ptr->pos : nearest;
    u8 *available = (u8 *)(queue + cells);
    for (s32 y = 0; y < layout->height; y++)
    {
        for (s32 x = 0; x < layout->width; x++)
        {
            u16 block = layout->map[y * layout->width + x];
            if (UNPACK_COLLISION(block))
                continue;
            if (UNPACK_ELEVATION(block) == ELEVATION_SURF)
            {
                if (surfing && DistanceToSavedPlayer(x, y) < best)
                {
                    best = DistanceToSavedPlayer(x, y);
                    nearest = (struct Coords16){x, y};
                }
            }
            else
                available[(y + 1) * stride + x + 1] = TRUE;
        }
    }
    if (!surfing)
    {
        const struct MapEvents *events = gMapHeader.events;
        for (u32 i = 0; i < events->objectEventCount; i++)
        {
            const struct ObjectEventTemplate *actor = &events->objectEvents[i];
            if ((u32)actor->x < layout->width && (u32)actor->y < layout->height)
                available[(actor->y + 1) * stride + actor->x + 1] = FALSE;
        }
        s32 offsets[] = {-stride, -1, 1, stride};
        u32 head = 0, tail = 1;
        queue[0] = (anchor->y + 1) * stride + anchor->x + 1;
        available[queue[0]] = FALSE;
        while (head < tail)
        {
            s32 tile = queue[head++];
            s32 x = tile % stride - 1, y = tile / stride - 1;
            s32 distance = DistanceToSavedPlayer(x, y);
            if (distance < best)
            {
                best = distance;
                nearest = (struct Coords16){x, y};
                if (!distance)
                    break;
            }
            for (u32 i = 0; i < ARRAY_COUNT(offsets); i++)
            {
                s32 neighbor = tile + offsets[i];
                if (available[neighbor])
                {
                    available[neighbor] = FALSE;
                    queue[tail++] = neighbor;
                }
            }
        }
    }
    Free(queue);
    return nearest;
}

static void MoveResumedActor(struct ObjectEvent *actor, struct Coords16 pos, u8 elevation)
{
    if (!actor->isPlayer && actor->localId != LOCALID_FOLLOWING_POKEMON)
        return;
    pos.x += MAP_OFFSET;
    pos.y += MAP_OFFSET;
    actor->initialCoords = actor->currentCoords = actor->previousCoords = pos;
    actor->currentElevation = actor->previousElevation = elevation;
}
#endif

void LegendsJohtoMarkSavedScenery(void)
{
#if !IS_FRLG
    if (gMapHeader.mapLayout->secondaryTileset == &gTileset_LegendsJohto)
        gSaveBlock1Ptr->mapView[JOHTO_VIEW_MARKER_INDEX] = JOHTO_VIEW_REVISION;
#endif
}

bool32 LegendsJohtoRestoreLegacyScenery(void)
{
#if !IS_FRLG
    const struct MapLayout *layout = gMapHeader.mapLayout;
    u8 mapNum = gSaveBlock1Ptr->location.mapNum;
    if (layout->secondaryTileset != &gTileset_LegendsJohto
     || gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_LEGENDS_JOHTO_NEW_BARK_TOWN)
     || mapNum >= ARRAY_COUNT(sTrailAnchors)
     || (sTrailAnchors[mapNum].x == 0 && sTrailAnchors[mapNum].y == 0)
     || gSaveBlock1Ptr->mapView[JOHTO_VIEW_MARKER_INDEX] == JOHTO_VIEW_REVISION)
        return FALSE;
    bool32 surfing = FALSE;
    for (u32 i = 0; i < OBJECT_EVENTS_COUNT; i++)
        if (gSaveBlock1Ptr->objectEvents[i].isPlayer)
            surfing = gSaveBlock1Ptr->objectEvents[i].currentElevation == ELEVATION_SURF;
    struct Coords16 pos = FindResumeTile(layout, &sTrailAnchors[mapNum], surfing);
    if (pos.x != gSaveBlock1Ptr->pos.x || pos.y != gSaveBlock1Ptr->pos.y)
    {
        gSaveBlock1Ptr->pos = pos;
        u8 elevation = UNPACK_ELEVATION(layout->map[pos.y * layout->width + pos.x]);
        for (u32 i = 0; i < OBJECT_EVENTS_COUNT; i++)
        {
            MoveResumedActor(&gSaveBlock1Ptr->objectEvents[i], pos, elevation);
            MoveResumedActor(&gObjectEvents[i], pos, elevation);
        }
    }
    return TRUE;
#else
    return FALSE;
#endif
}
