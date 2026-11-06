"""Production-C shared bag and all published inventory-format migrations."""
from pathlib import Path
import re,subprocess,tempfile
R=Path(__file__).resolve().parents[1]
item=(R/'src/item.c').read_text();storage=(R/'src/legends_storage.c').read_text();menu=(R/'src/item_menu.c').read_text()
def function(source,name):
 m=re.search(r'^[^\n;]*\b'+name+r'\([^;]*?\)\n\{',source,re.M);assert m,name
 start=m.start();a=source.index('{',m.start());depth=1;b=a+1
 while depth:depth+=(source[b]=='{')-(source[b]=='}');b+=1
 return source[start:b]
names=['BagPoolUsed','BagPocket_GetSlotDataGeneric','BagPocket_GetSlotDataPC','BagPocket_SetSlotDataGeneric','BagPocket_SetSlotDataPC','BagPocket_GetSlotData','BagPocket_SetSlotData','SetBagItemsPointers','CheckSlotAndUpdateCount','BagPocket_AddItem','BagPocket_RemoveItem','BagPocket_CompactItems','BagPocket_MoveItemSlot','BagPocket_CountTotalItemQuantity']
funcs=[function(item,n) for n in names]+[function(menu,n) for n in ['Merge','MergeSort']]
code=r'''
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int32_t s32;typedef int8_t s8;typedef int bool32;
#define TRUE 1
#define FALSE 0
#define EWRAM_DATA
#define NONNULL
#define STATIC_ASSERT(x,n) _Static_assert(x,#n)
#define LEGENDS_BAG_SLOTS 1152
#define MAX_BAG_ITEM_CAPACITY 999
#define PC_ITEMS_COUNT 150
#define TOTAL_BOXES_COUNT 20
#define IN_BOX_COUNT 30
#define BOX_NAME_LENGTH 8
#define MAX_FUSION_STORAGE 4
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define COMPOUND_STRING(s) ((const u8 *)(s))
#define STR_CONV_MODE_LEFT_ALIGN 0
#define min(a,b) ((a)<(b)?(a):(b))
#define max(a,b) ((a)>(b)?(a):(b))
#define CurMapIsSecretBase() FALSE
#define VarSet(a,b) ((void)0)
#define VarGet(a) 0
#define VAR_SECRET_BASE_LOW_TV_FLAGS 0
#define VAR_SECRET_BASE_LAST_ITEM_USED 0
#define SECRET_BASE_USED_BAG 0
#include "constants/item.h"
enum Item {ITEM_NONE=0};
struct ItemSlot {u16 itemId,quantity;};
struct Bag {u16 pocketSizes[POCKETS_COUNT];struct ItemSlot slots[LEGENDS_BAG_SLOTS];};
struct LegacyBag {struct ItemSlot items[30],keyItems[30],pokeBalls[16],TMsHMs[64],berries[46];};
struct BoxPokemon {u32 personality,otId;u8 other[24];struct {u32 raw[12];} secure;};
struct Pokemon {u8 bytes[100];};
struct PokemonStorage {u8 currentBox;struct BoxPokemon boxes[20][30];u8 boxNames[20][9],boxWallpapers[20];struct Pokemon fusions[4];struct Bag inventory;struct ItemSlot pcItems[150];};
struct BagPocket {struct ItemSlot *itemSlots;u16 capacity;enum Pocket id;};
struct PokemonStorage data,*gPokemonStoragePtr=&data;
struct {struct LegacyBag bag;struct ItemSlot pcItems[50];} nativeSave,*gSaveBlock1Ptr=&nativeSave;
struct {u32 encryptionKey;} save2={0x1234abcd},*gSaveBlock2Ptr=&save2;
struct BagPocket gBagPockets[POCKETS_COUNT];
static int failAlloc;
static void *Alloc(u32 n){return failAlloc?NULL:malloc(n);}
static void *AllocZeroed(u32 n){return failAlloc?NULL:calloc(1,n);}
#define Free free
static u8 *StringCopy(u8 *dst,const u8 *src){strcpy((char *)dst,(const char *)src);return dst+strlen((const char *)dst);}
static void ConvertIntToDecimalStringN(u8 *dst,u32 n,u32 mode,u32 digits){(void)mode;(void)digits;sprintf((char *)dst,"%u",n);}
#include "legends_storage.h"
void SetBagItemsPointers(void);
static void BagPocket_SetSlotItemIdAndCount(struct BagPocket *p,u32 pos,enum Item id,u16 q);
'''
code+='\n'.join(f[:f.index('{')].strip()+';' for f in funcs)+'\n'
code+='\n'.join(l for l in storage.splitlines() if not l.startswith('#include'))+'\n'+'\n'.join(funcs)
code+=r'''
static void BagPocket_SetSlotItemIdAndCount(struct BagPocket *p,u32 pos,enum Item id,u16 q){BagPocket_SetSlotData(p,pos,(struct ItemSlot){id,q});}
static s32 cmp(enum Pocket id,struct ItemSlot a,struct ItemSlot b){(void)id;return !a.itemId?1:!b.itemId?-1:(s32)a.itemId-b.itemId;}
static void fresh(void){memset(&data,0,sizeof(data));SetBagItemsPointers();}
static void invariant(void){u32 offset=0,used=BagPoolUsed();assert(used<=1152);for(u32 p=0;p<5;p++){assert(gBagPockets[p].itemSlots==data.inventory.slots+offset);assert(gBagPockets[p].capacity==data.inventory.pocketSizes[p]+1152-used);offset+=data.inventory.pocketSizes[p];}}
int main(void)
{
 for(unsigned pocket=0;pocket<5;pocket++){
  fresh();for(unsigned i=1;i<=1152;i++){assert(BagPocket_AddItem(&gBagPockets[pocket],i,999));invariant();}
  assert(data.inventory.pocketSizes[pocket]==1152);
  for(unsigned i=0;i<1152;i++){struct ItemSlot v=BagPocket_GetSlotData(&gBagPockets[pocket],i);assert(v.itemId==i+1&&v.quantity==999);}
  struct Bag before=data.inventory;assert(!BagPocket_AddItem(&gBagPockets[(pocket+1)%5],5000,1));assert(!memcmp(&before,&data.inventory,sizeof(before)));
  assert(BagPocket_RemoveItem(&gBagPockets[pocket],600,999));invariant();assert(BagPocket_AddItem(&gBagPockets[(pocket+1)%5],5000,1));invariant();
 }
 fresh();for(unsigned i=0;i<600;i++)assert(BagPocket_AddItem(&gBagPockets[0],1,999));assert(BagPocket_CountTotalItemQuantity(&gBagPockets[0],1)==599400);assert(BagPocket_RemoveItem(&gBagPockets[0],1,1500));assert(BagPocket_CountTotalItemQuantity(&gBagPockets[0],1)==597900);
 fresh();for(unsigned p=0;p<5;p++)for(unsigned i=0;i<110;i++)assert(BagPocket_AddItem(&gBagPockets[p],1000*p+110-i,7));
 for(unsigned p=0;p<5;p++){MergeSort(&gBagPockets[p],cmp);invariant();for(unsigned i=0;i<110;i++)assert(BagPocket_GetSlotData(&gBagPockets[p],i).itemId==1000*p+i+1);}
 BagPocket_MoveItemSlot(&gBagPockets[0],0,110);assert(BagPocket_GetSlotData(&gBagPockets[0],109).itemId==1);invariant();
 struct PokemonStorage before=data;assert(LegendsStoragePrepare());memset(&data,0,sizeof(data));assert(LegendsStorageDecode());assert(!memcmp(&before,&data,sizeof(data)));LegendsStorageRelease();
 // Published compressed twenty-box inventory: all450 entries, quantities, PC,
 // Pokemon/fusions and names survive; next save uses the new magic exactly once.
 fresh();memset(&data,0x36,offsetof(struct PokemonStorage,inventory));data.currentBox=17;struct PokemonStorage expected=data;
 struct LegacyExpandedBag old;struct ItemSlot *entries=(void *)&old;
 for(unsigned i=0;i<450;i++)entries[i]=(struct ItemSlot){i+1,(i%999+1)^save2.encryptionKey};
 for(unsigned i=0;i<150;i++)data.pcItems[i]=(struct ItemSlot){i+50,i+100};
 struct ItemSlot pc[150];memcpy(pc,data.pcItems,sizeof(pc));
 const u32 prefix=offsetof(struct PokemonStorage,inventory),oldSize=prefix+sizeof(old)+sizeof(pc);
 u8 *raw=malloc(oldSize);ToggleEncryption();memcpy(raw,&data,prefix);ToggleEncryption();memcpy(raw+prefix,&old,sizeof(old));memcpy(raw+prefix+sizeof(old),pc,sizeof(pc));
 assert(LegendsStorageAllocate());struct LegendsPackedHeader *h=(void *)sPacked;h->magic=LEGENDS_STORAGE_LEGACY_MAGIC;h->rawSize=oldSize;h->checksum=Hash(raw,oldSize);u16 hash[4096];h->payloadSize=LegendsStoragePack(raw,oldSize,sPacked+sizeof(*h),LEGENDS_STORAGE_FLASH_BYTES-sizeof(*h),hash);assert(h->payloadSize);
 memset(&data,0,sizeof(data));assert(LegendsStorageDecode());invariant();assert(!memcmp(&expected,&data,prefix));assert(!memcmp(pc,data.pcItems,sizeof(pc)));
 const struct ItemSlot *sources[]={old.items,old.pokeBalls,old.TMsHMs,old.berries,old.keyItems};unsigned counts[]={150,32,128,80,60};
 for(unsigned p=0;p<5;p++)for(unsigned i=0;i<counts[p];i++){struct ItemSlot actual=BagPocket_GetSlotData(&gBagPockets[p],i);assert(actual.itemId==sources[p][i].itemId&&actual.quantity==(u16)(sources[p][i].quantity^save2.encryptionKey));}
 before=data;assert(LegendsStoragePrepare());assert(((struct LegendsPackedHeader *)sPacked)->magic==LEGENDS_STORAGE_MAGIC);memset(&data,0,sizeof(data));assert(LegendsStorageDecode());assert(!memcmp(&before,&data,sizeof(data)));
 ((struct LegendsPackedHeader *)sPacked)->rawSize--;assert(!LegendsStorageDecode());LegendsStorageRelease();free(raw);
 // Original native fourteen-box format still imports every original pocket.
 fresh();memset(&nativeSave,0,sizeof(nativeSave));nativeSave.bag.keyItems[29]=(struct ItemSlot){875,1^save2.encryptionKey};nativeSave.bag.items[29]=(struct ItemSlot){23,77^save2.encryptionKey};nativeSave.pcItems[49]=(struct ItemSlot){88,99};
 assert(LegendsStorageAllocate());memset(sPacked,0,LEGENDS_STORAGE_FLASH_BYTES);assert(LegendsStorageDecode());invariant();assert(BagPocket_GetSlotData(&gBagPockets[4],29).itemId==875);assert(BagPocket_GetSlotData(&gBagPockets[0],29).quantity==77);assert(data.pcItems[49].quantity==99);assert(data.boxNames[19][0]=='B');LegendsStorageRelease();
 fresh();failAlloc=1;assert(!BagPocket_AddItem(&gBagPockets[0],1,1));assert(!LegendsStoragePrepare());failAlloc=0;
 puts("PASS: each pocket1152 stacks; shared reuse/full refusal; >255 indices; cross-pocket preservation; sorting/swapping; old14-box and v43-v77 packed migration; new save/reload; malformed-size and allocation refusal");
}
'''
with tempfile.TemporaryDirectory() as folder:
 p=Path(folder);(p/'test.c').write_text(code)
 subprocess.run(['cc','-iquote',str(R/'include'),'-std=gnu11','-O1','-g','-Wall','-Wextra','-Werror','-Wno-unused-function','-Wno-enum-conversion','-fsanitize=address,undefined',str(p/'test.c'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True)
