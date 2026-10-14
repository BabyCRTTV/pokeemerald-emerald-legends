#include "global.h"
#include "legends_bedroom.h"
#include "legends_bedroom_tiles.h"
#include "decoration.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "fieldmap.h"
#include "field_player_avatar.h"
#include "palette.h"
#include "string_util.h"
#include "constants/maps.h"
#include "constants/rgb.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/decorations.h"

// No serialized structures or published identifiers change. An invalid/old
// reserved variable is read as Default; only an explicit menu choice writes it.
#define COLOR_SIGNATURE 0xB400
#define ROOM_W 9
#define ROOM_H 8
static const u16 sRoomPalette[] = INCGFX_U16("data/tilesets/secondary/brendans_mays_house/palettes/06.pal", ".gbapal");
static const u16 sMaleBedPalette[] = INCGFX_U16("data/tilesets/secondary/brendans_mays_house/palettes/07.pal", ".gbapal");
static const u16 sFemaleBedPalette[] = INCGFX_U16("data/tilesets/secondary/brendans_mays_house/palettes/10.pal", ".gbapal");
static const u16 sDecorPalettes[][16] = {
    INCGFX_U16("data/tilesets/primary/secret_base/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/secret_base/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/secret_base/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/secret_base/palettes/03.pal", ".gbapal"),
};
static const u16 sColors[][4] = {
    {RGB(8,13,21), RGB(13,18,24), RGB(17,23,30), RGB(23,27,31)}, // Blue
    {RGB(17,7,11), RGB(23,12,17), RGB(28,18,23), RGB(31,25,29)}, // Rose
    {RGB(7,16,12), RGB(12,22,17), RGB(18,27,22), RGB(25,31,28)}, // Mint
    {RGB(19,12,4), RGB(25,17,6), RGB(30,23,10), RGB(31,29,18)}, // Gold
    {RGB(12,8,19), RGB(18,13,25), RGB(23,19,29), RGB(28,25,31)}, // Plum
    {RGB(19,8,7), RGB(25,13,11), RGB(30,19,16), RGB(31,26,22)}, // Coral
};

static bool32 MaleRoom(void)
{
    return gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F)
        && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F);
}
bool32 LegendsBedroomIsMap(void)
{
    return MaleRoom() || (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_LITTLEROOT_TOWN_MAYS_HOUSE_2F)
        && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_LITTLEROOT_TOWN_MAYS_HOUSE_2F));
}
bool32 LegendsBedroomIsHome(void)
{
    return LegendsBedroomIsMap() && (MaleRoom() == (gSaveBlock2Ptr->playerGender == MALE));
}
void LegendsBedroomIsHomeSpecial(void) { gSpecialVar_Result = LegendsBedroomIsHome(); }
u8 LegendsBedroomColor(bool32 bed)
{
    u16 value = VarGet(VAR_LEGENDS_BEDROOM_COLORS);
    if ((value & 0xFF00) != COLOR_SIGNATURE || (value & 15) >= BEDROOM_COLOR_COUNT || ((value >> 4) & 15) >= BEDROOM_COLOR_COUNT)
        return 0;
    return (value >> (bed ? 0 : 4)) & 15;
}
void LegendsBedroomSetColor(bool32 bed, u8 color)
{
    u8 rug, blanket;
    if (!LegendsBedroomIsHome() || color >= BEDROOM_COLOR_COUNT)
        return;
    rug = LegendsBedroomColor(FALSE); blanket = LegendsBedroomColor(TRUE);
    if (bed) blanket = color; else rug = color;
    VarSet(VAR_LEGENDS_BEDROOM_COLORS, COLOR_SIGNATURE | (rug << 4) | blanket);
    LegendsBedroomLoadPalette(FALSE);
}
static void RoomPalette(const u16 *colors, u8 slot, bool8 skipFaded)
{
    if (skipFaded) CpuCopy16(colors, &gPlttBufferUnfaded[slot * 16], 32);
    else LoadPalette(colors, slot * 16, 32);
}
void LegendsBedroomLoadPalette(bool8 skipFaded)
{
    u16 colors[16]; u8 i, selected;
    if (!LegendsBedroomIsMap()) return;
    CpuCopy16(sRoomPalette, colors, sizeof(colors));
    selected = LegendsBedroomIsHome() ? LegendsBedroomColor(FALSE) : 0;
    if (selected)
        for (i = 0; i < 3; i++) colors[10 + i] = colors[13 + i] = sColors[selected - 1][i + 1];
    RoomPalette(colors, 1, skipFaded);
    CpuCopy16(MaleRoom() ? sMaleBedPalette : sFemaleBedPalette, colors, sizeof(colors));
    selected = LegendsBedroomIsHome() ? LegendsBedroomColor(TRUE) : 0;
    if (selected)
    {
        if (MaleRoom()) for (i = 0; i < 4; i++) colors[8 + i] = sColors[selected - 1][i];
        else { colors[10] = sColors[selected - 1][1]; colors[11] = sColors[selected - 1][2]; }
    }
    RoomPalette(colors, 2, skipFaded);
    RoomPalette(sDecorPalettes[0], 5, skipFaded);
    RoomPalette(sDecorPalettes[1], 11, skipFaded);
    RoomPalette(sDecorPalettes[2], 4, skipFaded);
    RoomPalette(sDecorPalettes[3], 3, skipFaded);
}
static bool32 Floor(u16 tile)
{
    return tile == 0x201 || (tile >= 0x204 && tile <= 0x207) || tile == 0x278
        || (tile >= 0x298 && tile <= 0x2AD);
}
bool32 LegendsBedroomSavedPosition(s16 x, s16 y)
{
    return LegendsBedroomIsHome() && x >= 0 && x < ROOM_W && y >= 0 && y < ROOM_H
        && Floor(gMapHeader.mapLayout->map[y * ROOM_W + x] & 0x3FF);
}
static bool32 DecorOverlaps(u8 x, u8 y, u8 w, u8 h)
{
    u8 i, dw, dh; s16 dx, dy;
    for (i = 0; i < DECOR_MAX_PLAYERS_HOUSE; i++)
    {
        u8 decor = gSaveBlock1Ptr->playerRoomDecorations[i];
        if (!decor || decor > NUM_DECORATIONS) continue;
        GetDecorationDimensions(decor, &dw, &dh);
        dx = gSaveBlock1Ptr->playerRoomDecorationPositions[i] >> 4;
        dy = (gSaveBlock1Ptr->playerRoomDecorationPositions[i] & 15) - dh + 1;
        if (x < dx + dw && dx < x + w && y < dy + dh && dy < y + h) return TRUE;
    }
    return FALSE;
}
static void Keepsake(u8 x, u8 y, u16 tile)
{
    if (DecorOverlaps(x, y, 1, 2)) return;
    MapGridSetMetatileEntryAt(x + MAP_OFFSET, y + MAP_OFFSET, tile | MAPGRID_IMPASSABLE | 0x3000);
    MapGridSetMetatileEntryAt(x + MAP_OFFSET, y + 1 + MAP_OFFSET, (tile + 1) | MAPGRID_IMPASSABLE | 0x3000);
}
void LegendsBedroomApply(void)
{
    u8 x, y, left, right, edge; u16 base;
    if (!LegendsBedroomIsHome() || !FlagGet(FLAG_RESCUED_BIRCH)) return;
    // Reset only this room's ROM map; saved doll records are never touched.
    for (y = 0; y < ROOM_H; y++) for (x = 0; x < ROOM_W; x++)
        MapGridSetMetatileEntryAt(x + MAP_OFFSET, y + MAP_OFFSET, gMapHeader.mapLayout->map[y * ROOM_W + x]);
    left = MaleRoom() ? 3 : 1; right = MaleRoom() ? 7 : 5;
    for (y = 3; y <= 6; y++) for (x = left; x <= right; x++)
    {
        base = (MaleRoom() ? 0x298 : 0x29B) + (y == 3 ? 0 : y == 6 ? 16 : 8);
        MapGridSetMetatileEntryAt(x + MAP_OFFSET, y + MAP_OFFSET, (base + (x == left ? 0 : x == right ? 2 : 1)) | 0x3000);
    }
    edge = MaleRoom() ? 8 : 0;
    if (FlagGet(FLAG_BADGE01_GET)) Keepsake(edge, 6, BEDROOM_FLOWERS);
    if (FlagGet(FLAG_BADGE05_GET)) Keepsake(edge, 4, BEDROOM_SILVER);
    if (FlagGet(FLAG_SYS_GAME_CLEAR)) Keepsake(edge, 2, BEDROOM_GOLD);
    if (FlagGet(FLAG_LEGENDS_KANTO_SURVEY_REPORT))
    {
        x = MaleRoom() ? 3 : 7;
        MapGridSetMetatileIdAt(x + MAP_OFFSET, MAP_OFFSET, BEDROOM_POSTER);
        MapGridSetMetatileIdAt(x + MAP_OFFSET, 1 + MAP_OFFSET, BEDROOM_POSTER + 1);
    }
}
// Flood-fill the actual passable map before/after placement. Functional
// approaches must remain reachable; empty corners may become display space.
static void Reachable(u8 *seen, s16 px, s16 py, u8 width, u8 height)
{
    u8 queue[ROOM_W * ROOM_H], head = 0, tail = 0, x, y, n, id;
    static const s8 steps[4][2] = {{1,0},{-1,0},{0,1},{0,-1}};
    memset(seen, 0, ROOM_W * ROOM_H);
    id = MaleRoom() ? 1 * ROOM_W + 7 : 1 * ROOM_W + 1;
    seen[id] = 1; queue[tail++] = id;
    while (head < tail)
    {
        id = queue[head++];
        for (n = 0; n < 4; n++)
        {
            s16 nx = id % ROOM_W + steps[n][0], ny = id / ROOM_W + steps[n][1];
            u8 obj;
            if (nx < 0 || nx >= ROOM_W || ny < 0 || ny >= ROOM_H) continue;
            x = nx; y = ny; id = queue[head - 1];
            if (seen[y * ROOM_W + x] || (x >= px && x < px + width && y >= py && y < py + height)) continue;
            if (MapGridGetCollisionAt(x + MAP_OFFSET, y + MAP_OFFSET)) continue;
            // Room floor is elevation 3; elevation 0 is the native wildcard.
            // Raised bed edges are not a valid alternate path around a doll.
            if (MapGridGetElevationAt(x + MAP_OFFSET, y + MAP_OFFSET) != 0
                && MapGridGetElevationAt(x + MAP_OFFSET, y + MAP_OFFSET) != 3) continue;
            obj = GetObjectEventIdByPosition(x + MAP_OFFSET, y + MAP_OFFSET, 0);
            if (obj != OBJECT_EVENTS_COUNT && obj != gPlayerAvatar.objectEventId) continue;
            seen[y * ROOM_W + x] = 1; queue[tail++] = y * ROOM_W + x;
        }
    }
}
bool32 LegendsBedroomCanPlace(s16 x, s16 y, u8 width, u8 height)
{
    static const u8 accessX[2][6] = {{0,1,3,5,1,7}, {8,7,5,3,7,1}};
    static const u8 accessY[6] = {2,2,2,2,7,2};
    u8 before[ROOM_W * ROOM_H], after[ROOM_W * ROOM_H]; s16 px, py, dx, dy; u8 i, layout = MaleRoom() ? 0 : 1;
    if (!LegendsBedroomIsHome() || !width || !height) return FALSE;
    px = x - MAP_OFFSET; py = y - MAP_OFFSET - height + 1;
    if (px < 0 || py < 0 || px + width > ROOM_W || py + height > ROOM_H
        || DecorOverlaps(px, py, width, height)) return FALSE;
    for (dy = 0; dy < height; dy++) for (dx = 0; dx < width; dx++)
    {
        s16 xx = px + dx, yy = py + dy;
        for (i = 0; i < 6; i++)
            if (xx == accessX[layout][i] && yy == accessY[i]) return FALSE;
        if (!LegendsBedroomSavedPosition(xx, yy) || MapGridGetCollisionAt(xx + MAP_OFFSET, yy + MAP_OFFSET)
            || GetObjectEventIdByPosition(xx + MAP_OFFSET, yy + MAP_OFFSET, 0) != OBJECT_EVENTS_COUNT) return FALSE;
    }
    Reachable(before, -1, -1, 0, 0); Reachable(after, px, py, width, height);
    for (i = 0; i < 6; i++)
    {
        u8 cell = accessY[i] * ROOM_W + accessX[layout][i];
        if (before[cell] && !after[cell]) return FALSE;
    }
    return TRUE;
}
void LegendsBedroomMomMessage(void)
{
    const u8 *text = NULL;
    if (FlagGet(FLAG_LEGENDS_FINAL_HOENN_EPILOGUE)) text = COMPOUND_STRING("MOM: Even after all those voyages,\nthis will always be your home.");
    else if (FlagGet(FLAG_LEGENDS_FINAL_ISLAND_VISITED)) text = COMPOUND_STRING("MOM: An island beyond the horizon!\nI can't wait to hear about it.");
    else if (FlagGet(FLAG_LEGENDS_FINAL_EIGHT_RECORDS)) text = COMPOUND_STRING("MOM: Eight visiting GYM records!\nYour dad is so proud of you.");
    else if (FlagGet(FLAG_LEGENDS_STORY_WEATHER_REPORT)) text = COMPOUND_STRING("MOM: BIRCH told us about your work.\nThank you for keeping HOENN safe.");
    else if (FlagGet(FLAG_LEGENDS_KANTO_SURVEY_REPORT)) text = COMPOUND_STRING("MOM: Your reports arrived safely.\nI put a BALL POSTER in your room.");
    else if (FlagGet(FLAG_LEGENDS_KANTO_WELCOMED)) text = COMPOUND_STRING("MOM: Letters from KANTO already!\nRemember to come home sometimes.");
    else if (FlagGet(FLAG_SYS_GAME_CLEAR)) text = COMPOUND_STRING("MOM: Our own CHAMPION! I found\na gold display for your room.");
    else if (FlagGet(FLAG_BADGE05_GET)) text = COMPOUND_STRING("MOM: Your dad kept smiling all day.\nThe silver display is from us both.");
    else if (FlagGet(FLAG_BADGE01_GET)) text = COMPOUND_STRING("MOM: I left flowers in your room.\nYou've come such a long way!");
    gSpecialVar_Result = text != NULL;
    if (text) StringCopy(gStringVar4, text);
}
