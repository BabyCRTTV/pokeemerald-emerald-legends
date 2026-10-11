"""Exercise native first-item flags and compatible full/partial sector storage."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
def function(path, signature):
    text=(ROOT/path).read_text()
    start=text.index(signature+'\n{')
    return text[start:text.index('\n}',start)+2]
global_source=(ROOT/'include/global.h').read_text()
start=global_source.index('struct SaveBlock3\n{')
block=global_source[start:global_source.index('};',start)+2]
item_field='#if OW_SHOW_ITEM_DESCRIPTIONS == OW_ITEM_DESCRIPTIONS_FIRST_TIME\n    u8 itemFlags[ITEM_FLAGS_COUNT];\n#endif\n'
assert item_field in block
legacy=block.replace('struct SaveBlock3','struct LegacySaveBlock3').replace(item_field,'')
config=(ROOT/'include/config/overworld.h').read_text()
assert '#define OW_SHOW_ITEM_DESCRIPTIONS       OW_ITEM_DESCRIPTIONS_FIRST_TIME' in config
flags_enum=(ROOT/'include/overworld.h').read_text().split('enum ItemObtainFlags')[1].split('};')[0]
fixture=r'''
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32;
typedef int32_t s32; typedef uint8_t bool8; typedef int bool32;
#define TRUE 1
#define FALSE 0
#define OW_ITEM_DESCRIPTIONS_FIRST_TIME 1
#define OW_SHOW_ITEM_DESCRIPTIONS 1
#define OW_USE_FAKE_RTC 0
#define FNPC_ENABLE_NPC_FOLLOWERS 0
#define USE_DEXNAV_SEARCH_LEVELS 0
#define APRICORN_TREE_COUNT 0
#define EWRAM_DATA
#define max(a,b) ((a)>(b)?(a):(b))
#define min(a,b) ((a)<(b)?(a):(b))
#include "constants/items.h"
#include "legends_adventure.h"
#define ITEM_FLAGS_COUNT ((ITEMS_COUNT+7)/8)
#define GUARD_MAIN_H
typedef void (*MainCallback)(void);
#include "save.h"
'''
fixture+='enum ItemObtainFlags'+flags_enum+'};\n'+legacy+'\n'+block+r'''
static struct SaveBlock3 gSaveblock3,*gSaveBlock3Ptr=&gSaveblock3;
static struct SaveSector flash[NUM_SECTORS_PER_SLOT*NUM_SAVE_SLOTS], buffer;
static struct SaveSector *gReadWriteSector=&buffer;
struct SaveSectorLocation gRamSaveSectorLocations[NUM_SECTORS_PER_SLOT];
u16 gLastWrittenSector;u32 gSaveCounter;
static unsigned writes, damaged, failWrite;
CHECKSUM_FUNCTION
static bool8 ReadFlashSector(u8 sector,struct SaveSector *dest)
{ *dest=flash[sector];return TRUE; }
static void SetDamagedSectorBits(u8 action,u8 sector)
{ (void)action;(void)sector;damaged++; }
static u8 TryWriteSector(u8 sector,u8 *data)
{
    writes++;
    if(failWrite){damaged++;return SAVE_STATUS_ERROR;}
    memcpy(&flash[sector],data,sizeof(struct SaveSector));return SAVE_STATUS_OK;
}
'''
fixture=fixture.replace('CHECKSUM_FUNCTION',function('src/save.c','static u16 CalculateChecksum(void *data, u16 size)'))
code=function('src/overworld.c','bool8 GetSetItemObtained(enum Item item, enum ItemObtainFlags caseId)')
for signature in ['static u32 SaveBlock3Size(u32 sectorId)',
                  'static void CopyFromSaveBlock3(u32 sectorId, struct SaveSector *sector)',
                  'static void CopyToSaveBlock3(u32 sectorId, struct SaveSector *sector)',
                  'static void WriteSaveBlock3Tail(void)']:
    code+='\n'+function('src/save.c',signature)
tests=r'''
int main(void)
{
    assert(sizeof(struct LegacySaveBlock3)==0x21C);
    assert(offsetof(struct SaveBlock3, adventure)==offsetof(struct LegacySaveBlock3,adventure));
    assert(offsetof(struct SaveBlock3,itemFlags)==sizeof(struct LegacySaveBlock3));
    assert(sizeof(gSaveblock3)<=116*14);
    for(unsigned item=1;item<ITEMS_COUNT;item++)
    {
        memset(&gSaveblock3,0,sizeof(gSaveblock3));
        assert(!GetSetItemObtained(item,FLAG_GET_ITEM_OBTAINED));
        assert(GetSetItemObtained(item,FLAG_SET_ITEM_OBTAINED));
        assert(GetSetItemObtained(item,FLAG_GET_ITEM_OBTAINED));
        for(unsigned other=1;other<ITEMS_COUNT;other++)
            assert(!!GetSetItemObtained(other,FLAG_GET_ITEM_OBTAINED)==(other==item));
    }
    struct SaveBlock3 before=gSaveblock3;
    assert(!GetSetItemObtained(ITEM_NONE,FLAG_SET_ITEM_OBTAINED));
    assert(!GetSetItemObtained(ITEMS_COUNT,FLAG_SET_ITEM_OBTAINED));
    assert(!GetSetItemObtained(0xFFFF,FLAG_SET_ITEM_OBTAINED));
    assert(!memcmp(&before,&gSaveblock3,sizeof(before)));
    unsigned chunks=(sizeof(gSaveblock3)+115)/116;
    for(unsigned slot=0;slot<2;slot++)for(unsigned rotation=0;rotation<14;rotation++)
    {
        memset(flash,0,sizeof(flash));gSaveCounter=slot;gLastWrittenSector=rotation;
        memset(&gSaveblock3,0x45,sizeof(gSaveblock3));
        for(unsigned id=0;id<14;id++)
        {
            unsigned physical=(id+rotation)%14+slot*14;
            memset(flash[physical].data,id+3,sizeof(flash[physical].data));
            flash[physical].id=id;flash[physical].signature=SECTOR_SIGNATURE;
            flash[physical].counter=slot;gRamSaveSectorLocations[id].size=SECTOR_DATA_SIZE;
            flash[physical].checksum=CalculateChecksum(flash[physical].data,SECTOR_DATA_SIZE);
        }
        // Older Legends profiles leave unused chunk bytes zero. Legacy fields
        // survive loading; item history begins empty without shifting the log.
        struct LegacySaveBlock3 old={0};old.adventure.magic=0x12345678;
        for(unsigned id=0;id<14;id++)
        {
            unsigned physical=(id+rotation)%14+slot*14;
            unsigned begin=id*116;
            if(begin<sizeof(old))memcpy(flash[physical].saveBlock3Chunk,(u8*)&old+begin,min(116,sizeof(old)-begin));
            CopyToSaveBlock3(id,&flash[physical]);
        }
        assert(gSaveblock3.adventure.magic==old.adventure.magic);
        for(unsigned i=0;i<ITEM_FLAGS_COUNT;i++)assert(gSaveblock3.itemFlags[i]==0);
        memset(gSaveblock3.itemFlags,0xAB,ITEM_FLAGS_COUNT);
        struct SaveSector saved[28];memcpy(saved,flash,sizeof(flash));
        writes=damaged=failWrite=0;WriteSaveBlock3Tail();
        assert(writes==chunks-SECTOR_ID_PKMN_STORAGE_START && !damaged);
        for(unsigned id=0;id<14;id++)
        {
            unsigned physical=(id+rotation)%14+slot*14;
            assert(!memcmp(flash[physical].data,saved[physical].data,SECTOR_DATA_SIZE));
            assert(flash[physical].checksum==saved[physical].checksum);
            assert(flash[physical].signature==saved[physical].signature);
            assert(flash[physical].counter==saved[physical].counter);
            if(id<5 || id>=chunks)assert(!memcmp(&flash[physical],&saved[physical],sizeof(struct SaveSector)));
        }
        struct SaveBlock3 expected=gSaveblock3;
        // Full native chunk copy/load round trip preserves all fields.
        struct SaveSector full[14]={0};
        for(unsigned id=0;id<14;id++)CopyFromSaveBlock3(id,&full[id]);
        memset(&gSaveblock3,0,sizeof(gSaveblock3));
        for(unsigned id=0;id<14;id++)CopyToSaveBlock3(id,&full[id]);
        assert(!memcmp(&expected,&gSaveblock3,sizeof(expected)));
        // Reload all partial-save chunks, including the untouched old PC data.
        for(unsigned id=0;id<5;id++)CopyFromSaveBlock3(id,&flash[(id+rotation)%14+slot*14]);
        memset(&gSaveblock3,0,sizeof(gSaveblock3));
        for(unsigned id=0;id<14;id++)CopyToSaveBlock3(id,&flash[(id+rotation)%14+slot*14]);
        assert(!memcmp(&expected,&gSaveblock3,sizeof(expected)));
        unsigned priorWrites=writes;WriteSaveBlock3Tail();assert(writes==priorWrites);
        unsigned physical=(5+rotation)%14+slot*14;
        flash[physical].checksum++;WriteSaveBlock3Tail();assert(damaged==1 && writes==priorWrites);
        flash[physical].checksum--;gSaveblock3.itemFlags[ITEM_FLAGS_COUNT-1]^=1;
        failWrite=1;WriteSaveBlock3Tail();assert(damaged==2 && writes==priorWrites+1);
    }
    printf("%u item IDs; old-profile load; 28 slot/rotation layouts; partial PC preservation and write failures passed.\n",ITEMS_COUNT);
}
'''
# Both native partial-save paths must call the guarded tail write.
save=(ROOT/'src/save.c').read_text()
assert 'WriteSaveBlock3Tail();' in save.split('case SAVE_LINK:')[1].split('case SAVE_OVERWRITE_DIFFERENT_FILE:')[0]
assert 'WriteSaveBlock3Tail();' in function('src/save.c','bool8 WriteSaveBlock1Sector(void)')
assert 'sizeof(struct SaveBlock3) <= SAVE_BLOCK_3_CHUNK_SIZE * NUM_SECTORS_PER_SLOT' in save
assert 'offsetof(struct SaveBlock3, itemFlags) == 0x21C' in save
with tempfile.TemporaryDirectory() as directory:
    path=Path(directory);(path/'test.c').write_text(fixture+code+tests)
    subprocess.run(['cc','-std=gnu99','-Wall','-Wextra','-Werror','-iquote',str(ROOT/'include'),str(path/'test.c'),'-o',str(path/'check')],check=True)
    subprocess.run([str(path/'check')],check=True)
