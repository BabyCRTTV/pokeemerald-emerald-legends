"""Exercise the native follower selection/spawn logic with the Legends config."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'src/event_object_movement.c').read_text()
def function(signature):
    start = source.index(signature + '\n{')
    pos = source.index('{', start) + 1
    depth = 1
    while depth:
        depth += (source[pos] == '{') - (source[pos] == '}')
        pos += 1
    return source[start:pos]
selection = function('struct Pokemon *GetFirstLiveMon(void)')
info = function('bool8 GetFollowerInfo(enum Species *species, bool32 *shiny, bool32 *female)')
update = function('void UpdateFollowingPokemon(void)')
program = r'''
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8;
typedef uint32_t u32;
typedef uint8_t bool8;
typedef uint32_t bool32;
#define TRUE 1
#define FALSE 0
#define FLAG_LEGENDS_FOLLOWERS_DISABLED 1
#define FLAG_TEMP_HIDE_FOLLOWER 2
#include "config/overworld.h"
#define PARTY_SIZE 6
#define B_TRAINER_PLAYER 0
#define OBJECT_EVENTS_COUNT 4
#define OBJ_EVENT_ID_FOLLOWER 99
#define MAP_TYPE_INDOOR 1
#define ST_OAM_SIZE_2 2
#define MOVEMENT_TYPE_FOLLOW_PLAYER 1
#define MON_DATA_SPECIES_OR_EGG 0
#define MON_DATA_MET_LEVEL 1
#define MON_DATA_MET_LOCATION 2
enum Species {SPECIES_NONE, SPECIES_BULBASAUR, SPECIES_WAILORD};
struct Pokemon {enum Species species; u32 hp; struct {bool8 isEgg, isBadEgg;} box;};
struct ObjectEvent {u32 graphicsId, spriteId, currentElevation; bool32 active, invisible; struct {int x,y;} currentCoords;};
struct Sprite {int data[8];};
struct ObjectEventTemplate {u32 localId,graphicsId,flagId; int x,y; u32 elevation,movementType;};
struct Oam {u32 size;};
struct ObjectEventGraphicsInfo {struct Oam *oam;};
struct Pokemon gParties[1][PARTY_SIZE];
struct ObjectEvent gObjectEvents[OBJECT_EVENTS_COUNT];
struct Sprite gSprites[OBJECT_EVENTS_COUNT];
struct {u32 objectEventId;} gPlayerAvatar;
struct {u32 mapType;} gMapHeader;
struct Save {struct {int x,y;} pos;} save;
struct Save *gSaveBlock1Ptr = &save;
struct Oam oam;
struct ObjectEventGraphicsInfo graphics = {&oam};
bool32 flags[3], npc, full, noGraphics;
u32 removed, spawned, changed;
#define OW_SPECIES(o) ((o)->graphicsId)
#define OW_SHINY(o) FALSE
#define OW_FEMALE(o) FALSE
u32 GetMonData(struct Pokemon *mon,u32 field) {return field == MON_DATA_SPECIES_OR_EGG ? mon->species : 0;}
u32 VarGet(u32 id) {(void)id; return 0;}
bool32 FlagGet(u32 id) {return flags[id];}
bool32 PlayerHasFollowerNPC(void) {return npc;}
struct ObjectEvent *GetFollowerObject(void) {return gObjectEvents[1].active ? &gObjectEvents[1] : NULL;}
void RemoveFollowingPokemon(void) {if(gObjectEvents[1].active) removed++; gObjectEvents[1].active=FALSE;}
bool8 GetMonInfo(struct Pokemon *mon,enum Species *species,bool32 *shiny,bool32 *female)
{if(!mon)return FALSE; *species=mon->species; *shiny=FALSE; *female=FALSE; return TRUE;}
const struct ObjectEventGraphicsInfo *SpeciesToGraphicsInfo(enum Species s,bool32 shiny,bool32 female)
{(void)s; (void)shiny; (void)female; return noGraphics ? NULL : &graphics;}
u32 GetGraphicsIdForMon(enum Species s,bool32 shiny,bool32 female) {(void)shiny; (void)female; return s;}
u32 SpawnSpecialObjectEvent(const struct ObjectEventTemplate *t)
{if(full)return OBJECT_EVENTS_COUNT; spawned++;gObjectEvents[1].active=TRUE;gObjectEvents[1].graphicsId=t->graphicsId;gObjectEvents[1].spriteId=1;return 1;}
void MoveObjectEventToMapCoords(struct ObjectEvent *o,int x,int y) {o->currentCoords.x=x; o->currentCoords.y=y;}
void FollowerSetGraphics(struct ObjectEvent *o,enum Species s,bool32 shiny,bool32 female)
{(void)shiny; (void)female; o->graphicsId=s;changed++;}
'''+selection+'\n'+info+'\n'+update+r'''
int main(void)
{
    assert(OW_FOLLOWERS_ENABLED == TRUE);
    assert(B_FLAG_FOLLOWERS_DISABLED == FLAG_LEGENDS_FOLLOWERS_DISABLED);
    UpdateFollowingPokemon(); assert(!GetFollowerObject());
    gParties[0][0].species=SPECIES_WAILORD; gParties[0][0].hp=0;
    gParties[0][1].species=SPECIES_WAILORD; gParties[0][1].hp=20;gParties[0][1].box.isEgg=TRUE;
    gParties[0][2].species=SPECIES_BULBASAUR;gParties[0][2].hp=20;
    assert(GetFirstLiveMon()==&gParties[0][2]);
    UpdateFollowingPokemon();assert(GetFollowerObject());assert(spawned==1);
    assert(GetFollowerObject()->graphicsId==SPECIES_BULBASAUR);
    flags[FLAG_LEGENDS_FOLLOWERS_DISABLED]=TRUE;
    UpdateFollowingPokemon();assert(!GetFollowerObject());assert(removed==1);
    UpdateFollowingPokemon();assert(!GetFollowerObject());assert(removed==1);
    flags[FLAG_LEGENDS_FOLLOWERS_DISABLED]=FALSE;
    UpdateFollowingPokemon();assert(GetFollowerObject());
    flags[FLAG_TEMP_HIDE_FOLLOWER]=TRUE;
    UpdateFollowingPokemon();assert(!GetFollowerObject());
    flags[FLAG_TEMP_HIDE_FOLLOWER]=FALSE; npc=TRUE;
    UpdateFollowingPokemon();assert(!GetFollowerObject());
    npc=FALSE;gMapHeader.mapType=MAP_TYPE_INDOOR;oam.size=3;
    UpdateFollowingPokemon();assert(!GetFollowerObject());
    oam.size=2;UpdateFollowingPokemon();assert(GetFollowerObject());
    gParties[0][0].hp=20;UpdateFollowingPokemon();assert(changed==1);
    assert(GetFollowerObject()->graphicsId==SPECIES_WAILORD);
    noGraphics=TRUE;UpdateFollowingPokemon();assert(!GetFollowerObject());
    noGraphics=FALSE;full=TRUE;UpdateFollowingPokemon();assert(!GetFollowerObject());
    full=FALSE;UpdateFollowingPokemon();assert(GetFollowerObject());
    gParties[0][0].hp=0;gParties[0][2].hp=0;
    UpdateFollowingPokemon();assert(!GetFollowerObject());
    puts("Native follower selection, toggle removal/re-enable, script/NPC hiding, indoor size, party changes and full object slots passed.");
}
'''
options = (ROOT / 'src/option_menu.c').read_text()
assert '[OPTION_PAGE_LEGENDS] = 7' in options
assert 'LegendsSetFollowersEnabled(gTasks[taskId].tFollowers == 0);' in options
assert 'tFollowers = LegendsAreFollowersEnabled() ? 0 : 1;' in options
assert '.height = 14' in options and '.height = 15' not in options
# ReloadMap uses the native refresh after respawning field sprites on menu exit.
overworld = (ROOT / 'src/overworld.c').read_text()
assert 'UpdateFollowingPokemon();' in overworld.split('InitObjectEventsReturnToField();')[1].split('case 1:')[0]
with tempfile.TemporaryDirectory() as directory:
    tmp=Path(directory);(tmp/'check.c').write_text(program)
    subprocess.run(['cc','-std=c99','-Wall','-Wextra','-Werror','-I',str(ROOT/'include'),str(tmp/'check.c'),'-o',str(tmp/'check')],check=True)
    subprocess.run([str(tmp/'check')],check=True)
