"""Compile actual appearance settings; exhaustively check saves and palettes."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
# Saved object templates retain native dynamic IDs across updates.
constants=(root/"include/constants/event_objects.h").read_text()
native_enum=constants.split("NUM_OBJ_EVENT_GFX,")[0]
assert "OBJ_EVENT_GFX_LEGENDS_PLAYER_START" not in native_enum
assert "#define OBJ_EVENT_GFX_LEGENDS_PLAYER_START 0x0F00" in constants
source=(root/"src/legends_appearance.c").read_text()
source="\n".join(l for l in source.splitlines() if not l.startswith("#include"))
source=(root/"src/data/legends/appearance_palettes.h").read_text()+"\n"+source
graphics=(root/"src/legends_appearance_graphics.c").read_text()
graphics="\n".join(l for l in graphics.splitlines() if not l.startswith("#include"))
import re
base_ids=list(dict.fromkeys(re.findall(r"OBJ_EVENT_GFX_(?:BRENDAN|MAY)_\w+",graphics)))
graphics_constants="\n".join(f"#define {name} {i+100}" for i,name in enumerate(base_ids))
source += '\n'+graphics_constants+r'''
#define ALIGNED(x) __attribute__((aligned(x)))
#define LEGENDS_APPEARANCE_STATES 9
#define OBJ_EVENT_GFX_LEGENDS_PLAYER_START 1000
#define OBJ_EVENT_PAL_TAG_LEGENDS_PLAYER_MALE 2000
#define OBJ_EVENT_PAL_TAG_LEGENDS_UNDERWATER_MALE 2002
struct SpriteFrameImage {const u8 *data;u16 size;};
struct ObjectEventGraphicsInfo {u16 paletteTag;u16 size;const struct SpriteFrameImage *images;};
'''+(root/"src/data/legends/overworld_outfits.h").read_text()+'\n'+graphics
pre=r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int bool8;
enum Gender {MALE,FEMALE};
enum TrainerPicID {TRAINER_PIC_LEGENDS_BRENDAN_EMERALD=200};
#define EWRAM_DATA
#define TRUE 1
#define FALSE 0
#define LEGENDS_SKIN_TONE_COUNT 5
#define LEGENDS_OUTFIT_COUNT 5
#define VAR_LEGENDS_APPEARANCE 0
static u16 value;
u16 VarGet(u16 id){return value;}
void VarSet(u16 id,u16 v){value=v;}
void LegendsClearAppearanceSelection(void);
void LegendsUpdateAppearancePalettes(void);
'''
main=r'''
int main(void){
value=0;LegendsClearAppearanceSelection();LegendsUpdateAppearancePalettes();
assert(LegendsGetSkinTone()==0&&LegendsGetOutfit()==0);
assert(!memcmp(gLegendsOverworldPalettes,sBaseOverworldPalettes,sizeof(gLegendsOverworldPalettes)));
assert(!memcmp(gLegendsTrainerPalettes,sBaseTrainerPalettes,sizeof(gLegendsTrainerPalettes)));
for(int outfit=0;outfit<5;outfit++)for(int skin=0;skin<5;skin++){
    value=0;LegendsBeginAppearanceSelection();LegendsSetAppearanceSelection(skin,outfit);
    assert(LegendsGetSkinTone()==skin&&LegendsGetOutfit()==outfit);
    assert(value==0);
    // The real New Game clears permanent vars before applying pending choices.
    value=0;LegendsApplyAppearanceToNewGame();
    assert(value==1+skin+5*outfit&&!sSelection.valid);
    LegendsUpdateAppearancePalettes();
    for(int g=0;g<2;g++){
        assert(LegendsGetPlayerTrainerPic(g)==200+g*5+outfit);
        struct SpriteFrameImage nativeImage={0};
        struct ObjectEventGraphicsInfo native={99,512,&nativeImage};
        for(int state=0;state<9;state++){
            u16 id=LegendsGetPlayerGraphicsId(state,g);
            assert(id==1000+g*9+state);
            assert(LegendsGetBasePlayerGraphicsId(id)==sBaseGraphicsIds[g][state]);
            const struct ObjectEventGraphicsInfo *info=LegendsGetPlayerGraphicsInfo(id,&native);
            assert(info!=&native&&info->size==512);
            assert(info->paletteTag==(state==4?2002:2000)+g);
            assert(info->images==(outfit?sLegendsOutfitImages[g][outfit-1][state==8?5:state]:&nativeImage));
            assert(native.paletteTag==99&&native.images==&nativeImage);
        }
        assert(LegendsGetPlayerGraphicsId(255,g)==1000+g*9);
        assert(LegendsGetBasePlayerGraphicsId(35)==35);
        assert(LegendsGetPlayerGraphicsInfo(35,&native)==&native); // NPC passthrough.
        for(int i=0;i<16;i++){
            if(i>=1&&i<=3){
                assert(gLegendsOverworldPalettes[g][i]==sSkinPalettes[skin][i-1]);
                assert(gLegendsTrainerPalettes[g][i]==sSkinPalettes[skin][i-1]);
                assert(gLegendsUnderwaterPalettes[g][i]==sSkinPalettes[skin][i-1]);
            }else if(outfit&&i>=10&&i<=11){
                assert(gLegendsOverworldPalettes[g][i]==sOutfitPalettes[outfit-1][i-10]);
            }else{
                assert(gLegendsOverworldPalettes[g][i]==sBaseOverworldPalettes[g][i]);
                assert(gLegendsTrainerPalettes[g][i]==sBaseTrainerPalettes[g][i]);
            }
        }
    }
    // A fresh title discards uncommitted choices and displays the saved appearance.
    LegendsBeginAppearanceSelection();LegendsClearAppearanceSelection();
    assert(LegendsGetSkinTone()==skin&&LegendsGetOutfit()==outfit);
}
value=65535;LegendsClearAppearanceSelection();LegendsUpdateAppearancePalettes();
assert(LegendsGetSkinTone()==0&&LegendsGetOutfit()==0);
assert(!memcmp(gLegendsTrainerPalettes,sBaseTrainerPalettes,sizeof(gLegendsTrainerPalettes)));
LegendsSetAppearanceSelection(255,255);assert(LegendsGetSkinTone()==0&&LegendsGetOutfit()==0);
LegendsApplyAppearanceToNewGame();assert(value==1);
LegendsApplyAppearanceToNewGame();assert(value==0); // Pending selection is consumed once.
puts("All 50 gender/skin/outfit appearances, save handoff, legacy defaults and palette isolation passed.");
}
'''
with tempfile.TemporaryDirectory() as d:
    p=Path(d)/"appearance.c";p.write_text(pre+source+main)
    subprocess.run(["cc","-std=gnu11","-Werror=implicit-function-declaration",str(p),"-o",d+"/appearance"],check=True)
    subprocess.run([d+"/appearance"],check=True)
