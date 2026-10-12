#ifndef GUARD_LEGENDS_STORAGE_H
#define GUARD_LEGENDS_STORAGE_H
#define LEGENDS_STORAGE_MAGIC 0x4C504332
#define LEGENDS_STORAGE_FLASH_BYTES (3968 * 9)
struct LegendsPackedHeader { u32 magic, rawSize, checksum, payloadSize; };
struct Bag *LegendsStorageBag(void);
struct ItemSlot *LegendsStoragePCItems(void);
void LegendsStorageNewGame(void);
bool32 LegendsStoragePrepare(void);
bool32 LegendsStorageAllocate(void);
void LegendsStorageRelease(void);
u8 *LegendsStorageBuffer(void);
bool32 LegendsStorageDecode(void);
u32 LegendsStorageLegacyBytes(void);
u32 LegendsStoragePack(const u8 *src, u32 size, u8 *dst, u32 capacity, u16 *hash);
bool32 LegendsStorageUnpack(const u8 *src, u32 size, u8 *dst, u32 capacity);
#endif
