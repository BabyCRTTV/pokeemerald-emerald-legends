#include "global.h"
#include "legends_storage.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "item.h"
#include "malloc.h"
#include "string_util.h"
#include "strings.h"
#include "constants/characters.h"

struct LegacyPokemonStorage
{
    u8 currentBox;
    struct BoxPokemon boxes[14][IN_BOX_COUNT];
    u8 boxNames[14][BOX_NAME_LENGTH + 1];
    u8 boxWallpapers[14];
    struct Pokemon fusions[MAX_FUSION_STORAGE];
};
// Exact v0.0.43-v0.0.77 expanded inventory; never use mutable runtime limits.
struct LegacyExpandedBag
{
    struct ItemSlot items[150], keyItems[60], pokeBalls[32], TMsHMs[128], berries[80];
};
STATIC_ASSERT(sizeof(struct PokemonStorage) < 65536, StorageHashPositionsFitU16);
STATIC_ASSERT(LEGENDS_BAG_SLOTS >= 450, BagCanMigratePublishedInventory);

static bool32 BagLayoutValid(void)
{
    u32 i, used = 0;
    for (i = 0; i < POCKETS_COUNT; i++) used += LegendsStorageBag()->pocketSizes[i];
    return used <= LEGENDS_BAG_SLOTS;
}

// Copy encrypted quantities verbatim; preserve pocket order and every stack.
static void ImportPocket(enum Pocket pocket, const struct ItemSlot *source, u32 count)
{
    struct Bag *bag = LegendsStorageBag();
    u32 i, offset = 0;
    while (count && source[count - 1].itemId == ITEM_NONE) count--;
    for (i = 0; i < pocket; i++) offset += bag->pocketSizes[i];
    memcpy(bag->slots + offset, source, count * sizeof(*source));
    bag->pocketSizes[pocket] = count;
}

static void ImportExpandedBag(const struct LegacyExpandedBag *old)
{
    memset(LegendsStorageBag(), 0, sizeof(struct Bag));
    ImportPocket(POCKET_ITEMS, old->items, ARRAY_COUNT(old->items));
    ImportPocket(POCKET_POKE_BALLS, old->pokeBalls, ARRAY_COUNT(old->pokeBalls));
    ImportPocket(POCKET_TM_HM, old->TMsHMs, ARRAY_COUNT(old->TMsHMs));
    ImportPocket(POCKET_BERRIES, old->berries, ARRAY_COUNT(old->berries));
    ImportPocket(POCKET_KEY_ITEMS, old->keyItems, ARRAY_COUNT(old->keyItems));
}

EWRAM_DATA static u8 *sPacked = NULL;

struct Bag *LegendsStorageBag(void) { return &gPokemonStoragePtr->inventory; }
struct ItemSlot *LegendsStoragePCItems(void) { return gPokemonStoragePtr->pcItems; }
u8 *LegendsStorageBuffer(void) { return sPacked; }
u32 LegendsStorageLegacyBytes(void) { return sizeof(struct LegacyPokemonStorage); }
static u32 Hash(const u8 *src, u32 size)
{
    u32 i, h = 2166136261u;
    for (i = 0; i < size; i++) h = (h ^ src[i]) * 16777619u;
    return h;
}
// Bounded LZ tokens, with a 4096-byte history and 3..18-byte matches.
// Unlike BIOS decompression, the reader validates every source/destination bound.
u32 LegendsStoragePack(const u8 *src, u32 size, u8 *dst, u32 capacity, u16 *hash)
{
    u32 in = 0, out = 0, group, bit, key, prev, len, k;
    memset(hash, 0xFF, 4096 * sizeof(*hash));
    while (in < size)
    {
        if (out >= capacity) return 0;
        group = out++; dst[group] = 0;
        for (bit = 0; bit < 8 && in < size; bit++)
        {
            len = 0;
            if (in + 2 < size)
            {
                key = (src[in] * 251u + src[in + 1] * 17u + src[in + 2]) & 4095;
                prev = hash[key];
                if (prev < in && in - prev <= 4096)
                    while (len < 18 && in + len < size && src[prev + len] == src[in + len]) len++;
            }
            if (len >= 3)
            {
                u32 distance = in - prev - 1;
                if (out + 2 > capacity) return 0;
                dst[group] |= 0x80 >> bit;
                dst[out++] = ((len - 3) << 4) | (distance >> 8);
                dst[out++] = distance;
            }
            else
            {
                len = 1;
                if (out >= capacity) return 0;
                dst[out++] = src[in];
            }
            for (k = 0; k < len && in + k + 2 < size; k++)
            {
                key = (src[in + k] * 251u + src[in + k + 1] * 17u + src[in + k + 2]) & 4095;
                hash[key] = in + k;
            }
            in += len;
        }
    }
    return out;
}
bool32 LegendsStorageUnpack(const u8 *src, u32 size, u8 *dst, u32 capacity)
{
    u32 in = 0, out = 0, bit, flags, len, distance;
    while (out < capacity)
    {
        if (in >= size) return FALSE;
        flags = src[in++];
        for (bit = 0; bit < 8 && out < capacity; bit++)
        {
            if (flags & (0x80 >> bit))
            {
                if (in + 2 > size) return FALSE;
                len = (src[in] >> 4) + 3;
                distance = ((src[in] & 15) << 8) + src[in + 1] + 1;
                in += 2;
                if (distance > out || len > capacity - out) return FALSE;
                while (len--) { dst[out] = dst[out - distance]; out++; }
            }
            else
            {
                if (in >= size) return FALSE;
                dst[out++] = src[in++];
            }
        }
    }
    return in == size;
}
static void ToggleEncryption(void)
{
    u32 box, slot, word;
    // The reversible XOR does not change ordering, checksum, or any mon field.
    for (box = 0; box < TOTAL_BOXES_COUNT; box++)
        for (slot = 0; slot < IN_BOX_COUNT; slot++)
        {
            struct BoxPokemon *mon = &gPokemonStoragePtr->boxes[box][slot];
            u32 key = mon->personality ^ mon->otId;
            for (word = 0; word < ARRAY_COUNT(mon->secure.raw); word++) mon->secure.raw[word] ^= key;
        }
}
bool32 LegendsStorageAllocate(void)
{
    if (!sPacked) sPacked = AllocZeroed(LEGENDS_STORAGE_FLASH_BYTES);
    return sPacked != NULL;
}
void LegendsStorageRelease(void)
{
    if (sPacked) Free(sPacked);
    sPacked = NULL;
}
bool32 LegendsStoragePrepare(void)
{
    struct LegendsPackedHeader *header;
    u16 *hash;
    u32 size;
    if (!BagLayoutValid()) return FALSE;
    LegendsStorageRelease();
    if (!LegendsStorageAllocate()) return FALSE;
    hash = Alloc(4096 * sizeof(*hash));
    if (!hash) { LegendsStorageRelease(); return FALSE; }
    ToggleEncryption();
    header = (struct LegendsPackedHeader *)sPacked;
    header->magic = LEGENDS_STORAGE_MAGIC;
    header->rawSize = sizeof(*gPokemonStoragePtr);
    header->checksum = Hash((u8 *)gPokemonStoragePtr, sizeof(*gPokemonStoragePtr));
    size = LegendsStoragePack((u8 *)gPokemonStoragePtr, sizeof(*gPokemonStoragePtr),
        sPacked + sizeof(*header), LEGENDS_STORAGE_FLASH_BYTES - sizeof(*header), hash);
    ToggleEncryption();
    Free(hash);
    header->payloadSize = size;
    if (!size) { LegendsStorageRelease(); return FALSE; }
    return TRUE;
}
static void InitExtraBox(u8 box)
{
    u8 *end = StringCopy(gPokemonStoragePtr->boxNames[box], COMPOUND_STRING("BOX"));
    ConvertIntToDecimalStringN(end, box + 1, STR_CONV_MODE_LEFT_ALIGN, 2);
    gPokemonStoragePtr->boxWallpapers[box] = box % 16;
}
void LegendsStorageNewGame(void)
{
    memset(&gPokemonStoragePtr->inventory, 0, sizeof(gPokemonStoragePtr->inventory));
    memset(gPokemonStoragePtr->pcItems, 0, sizeof(gPokemonStoragePtr->pcItems));
}
bool32 LegendsStorageDecode(void)
{
    struct LegendsPackedHeader *header = (struct LegendsPackedHeader *)sPacked;
    if (!sPacked) return FALSE;
    if (header->magic == LEGENDS_STORAGE_MAGIC || header->magic == LEGENDS_STORAGE_LEGACY_MAGIC)
    {
        const u32 inventoryOffset = offsetof(struct PokemonStorage, inventory);
        const u32 oldSize = inventoryOffset + sizeof(struct LegacyExpandedBag) + PC_ITEMS_COUNT * sizeof(struct ItemSlot);
        bool32 oldFormat = header->magic == LEGENDS_STORAGE_LEGACY_MAGIC;
        u32 rawSize = oldFormat ? oldSize : sizeof(*gPokemonStoragePtr);
        struct LegacyExpandedBag *oldBag = NULL;
        if (header->rawSize != rawSize || !header->payloadSize
            || header->payloadSize > LEGENDS_STORAGE_FLASH_BYTES - sizeof(*header)) return FALSE;
        // Acquire migration scratch before changing the loaded destination.
        if (oldFormat && !(oldBag = Alloc(sizeof(*oldBag)))) return FALSE;
        if (!LegendsStorageUnpack(sPacked + sizeof(*header), header->payloadSize,
            (u8 *)gPokemonStoragePtr, rawSize)
            || Hash((u8 *)gPokemonStoragePtr, rawSize) != header->checksum)
        {
            if (oldBag) Free(oldBag);
            return FALSE;
        }
        if (oldFormat)
        {
            u8 *raw = (u8 *)gPokemonStoragePtr;
            memcpy(oldBag, raw + inventoryOffset, sizeof(*oldBag));
            memmove(gPokemonStoragePtr->pcItems, raw + inventoryOffset + sizeof(*oldBag),
                sizeof(gPokemonStoragePtr->pcItems));
            ImportExpandedBag(oldBag);
            Free(oldBag);
        }
        if (!BagLayoutValid()) return FALSE;
        ToggleEncryption();
        if (gPokemonStoragePtr->currentBox >= TOTAL_BOXES_COUNT) return FALSE;
    }
    else
    {
        const struct LegacyPokemonStorage *old = (const void *)sPacked;
        u8 i;
        memset(gPokemonStoragePtr, 0, sizeof(*gPokemonStoragePtr));
        gPokemonStoragePtr->currentBox = old->currentBox < 14 ? old->currentBox : 0;
        memcpy(gPokemonStoragePtr->boxes, old->boxes, sizeof(old->boxes));
        memcpy(gPokemonStoragePtr->boxNames, old->boxNames, sizeof(old->boxNames));
        memcpy(gPokemonStoragePtr->boxWallpapers, old->boxWallpapers, sizeof(old->boxWallpapers));
        memcpy(gPokemonStoragePtr->fusions, old->fusions, sizeof(old->fusions));
        for (i = 14; i < TOTAL_BOXES_COUNT; i++) InitExtraBox(i);
        // Original fourteen-box saves retain their native pocket widths.
        memset(LegendsStorageBag(), 0, sizeof(struct Bag));
        ImportPocket(POCKET_ITEMS, gSaveBlock1Ptr->bag.items, ARRAY_COUNT(gSaveBlock1Ptr->bag.items));
        ImportPocket(POCKET_POKE_BALLS, gSaveBlock1Ptr->bag.pokeBalls, ARRAY_COUNT(gSaveBlock1Ptr->bag.pokeBalls));
        ImportPocket(POCKET_TM_HM, gSaveBlock1Ptr->bag.TMsHMs, ARRAY_COUNT(gSaveBlock1Ptr->bag.TMsHMs));
        ImportPocket(POCKET_BERRIES, gSaveBlock1Ptr->bag.berries, ARRAY_COUNT(gSaveBlock1Ptr->bag.berries));
        ImportPocket(POCKET_KEY_ITEMS, gSaveBlock1Ptr->bag.keyItems, ARRAY_COUNT(gSaveBlock1Ptr->bag.keyItems));
        memcpy(gPokemonStoragePtr->pcItems, gSaveBlock1Ptr->pcItems, sizeof(gSaveBlock1Ptr->pcItems));
    }
    SetBagItemsPointers();
    return TRUE;
}
