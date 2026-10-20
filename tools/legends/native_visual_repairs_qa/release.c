// Normal Release Continue and controller input; no ROM, RAM or callback writes.
#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
static void quiet(struct mLogger *l,int category,enum mLogLevel level,const char *format,va_list args) {}
static struct mLogger logger={.log=quiet};
static struct mCore *c;static color_t *video;
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned mask){c->setKeys(c,mask);frames(2);c->setKeys(c,0);frames(60);}
static void walkTo(unsigned savePtr,int x,int y){
 unsigned at=c->busRead32(c,savePtr);int steps=0;
 while((c->busRead16(c,at)!=x||c->busRead16(c,at+2)!=y)&&steps++<500){
  int px=c->busRead16(c,at),py=c->busRead16(c,at+2);
  c->setKeys(c,py<y?128:py>y?64:px<x?16:32);frames(1);
 }
 c->setKeys(c,0);frames(30);assert(c->busRead16(c,at)==x&&c->busRead16(c,at+2)==y);
}
static void capture(const char *dir,const char *name){char p[4096];snprintf(p,sizeof(p),"%s/%s.rgba",dir,name);FILE *f=fopen(p,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);puts(name);}
int main(int argc,char **argv){
 assert(argc==11);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);
 unsigned main=strtoul(argv[4],NULL,0),overworld=strtoul(argv[5],NULL,0)|1;
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);
 video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);
 struct VFile *rom=VFileOpen(argv[1],O_RDONLY),*save=VFileOpen(argv[2],O_RDWR);assert(rom&&save&&c->loadROM(c,rom)&&c->loadSave(c,save));c->reset(c);frames(300);
 for(int n=0;n<12&&c->busRead32(c,main+4)!=overworld;n++){key(1);frames(240);}
 assert(c->busRead32(c,main+4)==overworld);capture(argv[3],"continued");
 key(8);capture(argv[3],"pause-page1");
 key(16);capture(argv[3],"pause-page2");key(32);
 unsigned actions=strtoul(argv[7],NULL,0),cursor=strtoul(argv[8],NULL,0);
 for(int n=0;n<10&&c->busRead8(c,actions+c->busRead8(c,cursor))!=4;n++)key(128);
 assert(c->busRead8(c,actions+c->busRead8(c,cursor))==4);
 key(1);frames(240);assert(c->busRead32(c,main+4)==(strtoul(argv[9],NULL,0)|1));capture(argv[3],"hoenn-card");
 key(256);capture(argv[3],"kanto-card");key(2);frames(240);key(2);frames(240);
 if(strtoul(argv[6],NULL,0)){
  walkTo(strtoul(argv[10],NULL,0),4,6);
  walkTo(strtoul(argv[10],NULL,0),strtoul(argv[6],NULL,0)==1?2:6,6);
  key(1);frames(240);capture(argv[3],"wardrobe");assert(c->busRead32(c,main+4)!=overworld);key(2);frames(300);assert(c->busRead32(c,main+4)==overworld);capture(argv[3],"wardrobe-return");
 }
 puts("Release normal Continue, pause page navigation and Trainer Card inputs completed.");
 c->deinit(c);free(video);return 0;
}
