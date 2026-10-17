// Normal Continue with an unmodified Debug or Release ROM; host reads RAM and sends keys only.
#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include "constants/items.h"
static void quiet(struct mLogger *l,int c,enum mLogLevel v,const char *f,va_list a){}
static struct mLogger logger={.log=quiet};static struct mCore *c;static color_t *video;
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned k){c->setKeys(c,k);frames(2);c->setKeys(c,0);frames(120);}
int main(int argc,char **argv){
 assert(argc==12);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);
 unsigned main=strtoul(argv[4],NULL,0),overworld=strtoul(argv[5],NULL,0)|1;
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);
 struct VFile *rom=VFileOpen(argv[1],O_RDONLY),*save=VFileOpen(argv[2],O_RDWR);assert(rom&&save&&c->loadROM(c,rom)&&c->loadSave(c,save));c->reset(c);frames(300);
 for(int n=0;n<12&&c->busRead32(c,main+4)!=overworld;n++){key(1);frames(240);}assert(c->busRead32(c,main+4)==overworld);
 unsigned sb3=c->busRead32(c,strtoul(argv[6],NULL,0)),pc=c->busRead32(c,strtoul(argv[7],NULL,0))+strtoul(argv[8],NULL,0),vars=c->busRead32(c,strtoul(argv[9],NULL,0))+strtoul(argv[10],NULL,0),claimed=strtoul(argv[11],NULL,0);
 assert(c->busRead32(c,sb3+652)==0x4C514143&&c->busRead16(c,sb3+660)==1&&c->busRead16(c,sb3+662)==0xA702);
 assert(c->busRead8(c,sb3+664)&1);assert(c->busRead8(c,sb3+676)&1);assert(c->busRead8(c,sb3+675)&0x40);assert(c->busRead8(c,sb3+687)&0x40);
 assert(c->busRead32(c,sb3+688)==0x41434832);assert(c->busRead8(c,sb3+700)&0xFF);assert(c->busRead8(c,sb3+701)&1);
 assert(!!(c->busRead8(c,sb3+704)&2)==claimed);assert(!!(c->busRead8(c,sb3+712)&2)==claimed);
 assert(c->busRead16(c,vars+0x7A*2)==0x3FFF&&c->busRead16(c,vars+0x5C*2)==0xB423);
 unsigned berry=0,potion=0;for(int n=0;n<150;n++){unsigned item=c->busRead16(c,pc+n*4),q=c->busRead16(c,pc+n*4+2);if(item==ITEM_CHARTI_BERRY)berry+=q;if(item==ITEM_POTION)potion+=q;}assert(berry==(claimed?3:0)&&potion==7);
 char path[4096];snprintf(path,sizeof(path),"%s/continued.rgba",argv[3]);FILE *f=fopen(path,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);
 puts("Normal Continue retained original claims/pin, extra earned/claimed high bits, research, bedroom colors and exact PC reward quantities; ROM/RAM unmodified by host.");c->deinit(c);free(video);return 0;
}
