// Unmodified Release ROM: normal Continue and buttons; observations are read-only.
#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
static void quiet(struct mLogger*l,int c,enum mLogLevel v,const char*f,va_list a){}
static struct mLogger logger={.log=quiet};
static struct mCore*c;static color_t*video;static unsigned mainAddr,overworld,savePtr,resultAddr,lockAddr,flagsOffset,flagIds[3];
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned k){c->setKeys(c,k);frames(3);c->setKeys(c,0);frames(42);}
static void walk(unsigned k){c->setKeys(c,k);frames(12);c->setKeys(c,0);frames(42);}
static unsigned base(void){return c->busRead32(c,savePtr);}
static unsigned flags(void){unsigned bits=0,p=base()+flagsOffset;for(int i=0;i<3;i++)if(c->busRead8(c,p+(flagIds[i]>>3))&(1u<<(flagIds[i]&7)))bits|=1u<<i;return bits;}
static int idle(void){return c->busRead32(c,mainAddr+4)==overworld&&!c->busRead8(c,lockAddr);}
static void waitIdle(void){for(int i=0;i<120;i++){frames(30);if(idle()){frames(120);if(idle())return;}}assert(!"Field controls did not return");}
static void location(unsigned group,unsigned map,unsigned x,unsigned y,unsigned bits){unsigned p=base();printf("map=%u,%u xy=%u,%u flags=%u lock=%u result=%u\n",c->busRead8(c,p+4),c->busRead8(c,p+5),c->busRead16(c,p),c->busRead16(c,p+2),flags(),c->busRead8(c,lockAddr),c->busRead16(c,resultAddr));assert(idle()&&c->busRead8(c,p+4)==group&&c->busRead8(c,p+5)==map&&c->busRead16(c,p)==x&&c->busRead16(c,p+2)==y&&flags()==bits);}
static void choice(void){for(int i=0;i<50;i++){if(c->busRead16(c,resultAddr)==255){frames(12);assert(c->busRead16(c,resultAddr)==255);return;}key(1);}assert(!"Native Yes/No menu did not appear");}
static void capture(const char*out,const char*name){char path[4096];snprintf(path,sizeof(path),"%s/%s.rgba",out,name);FILE*f=fopen(path,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);}
int main(int argc,char**argv){
 assert(argc==18);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);
 mainAddr=strtoul(argv[4],0,0);overworld=strtoul(argv[5],0,0)|1;savePtr=strtoul(argv[6],0,0);resultAddr=strtoul(argv[7],0,0);flagsOffset=strtoul(argv[8],0,0);for(int i=0;i<3;i++)flagIds[i]=strtoul(argv[9+i],0,0);
 unsigned eg=strtoul(argv[12],0,0),em=strtoul(argv[13],0,0),tg=strtoul(argv[14],0,0),tm=strtoul(argv[15],0,0),ready=strtoul(argv[16],0,0),bits=ready?3:0;lockAddr=strtoul(argv[17],0,0);
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);
 struct VFile*rom=VFileOpen(argv[1],O_RDONLY),*save=VFileOpen(argv[2],O_RDWR);assert(rom&&save&&c->loadROM(c,rom)&&c->loadSave(c,save));c->reset(c);frames(300);
 for(int i=0;i<12&&c->busRead32(c,mainAddr+4)!=overworld;i++){key(1);frames(240);}waitIdle();location(eg,em,28,47,bits);
 walk(64);location(eg,em,28,46,bits);key(16);location(eg,em,28,46,bits);key(1);choice();key(2);waitIdle();location(eg,em,28,46,bits);assert(c->busRead16(c,resultAddr)==0);puts("PASS Release declined return without movement or flag changes");
 key(1);choice();key(1);waitIdle();location(tg,tm,21,8,bits);capture(argv[3],"return");
 walk(64);location(tg,tm,21,7,bits);walk(128);location(tg,tm,21,8,bits);puts("PASS Release actual return and collision-enabled walking");
 key(32);location(tg,tm,21,8,bits);key(1);
 if(ready){choice();key(2);waitIdle();location(tg,tm,21,8,bits);key(1);choice();key(1);waitIdle();location(eg,em,28,47,bits);capture(argv[3],"reboarded");puts("PASS Release declined then reboarded production boat");}
 else{for(int i=0;i<50&&!idle();i++){assert(c->busRead16(c,resultAddr)!=255);key(1);}waitIdle();location(tg,tm,21,8,bits);puts("PASS Release outbound gates retained after unrestricted return");}
 c->deinit(c);free(video);return 0;
}
