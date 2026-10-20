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
static struct mCore *c; static color_t *video; static unsigned mainAddr, callback;
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned n){c->setKeys(c,n);frames(2);c->setKeys(c,0);frames(24);}
static void command(unsigned n,int count){c->busWrite32(c,0x0203fc00,n);c->busWrite32(c,mainAddr+4,callback);frames(count);}
static void capture(const char *folder,const char *name){char p[4096];snprintf(p,sizeof(p),"%s/%s.rgba",folder,name);FILE *f=fopen(p,"wb");assert(f);assert(fwrite(video,4,240*160,f)==240*160);fclose(f);puts(name);}
static void battery(const char *dir,const char *name){void *data=NULL;size_t n=c->savedataClone(c,&data);assert(n==131072&&data);char path[4096];snprintf(path,sizeof(path),"%s/%s.sav",dir,name);FILE *f=fopen(path,"wb");assert(f&&fwrite(data,1,n,f)==n);fclose(f);free(data);}
static void checkPalette(void){command(7,2);assert(c->busRead32(c,0x0203fc08)==0);}
int main(int argc,char **argv){
 setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);assert(argc==5);mainAddr=strtoul(argv[3],NULL,0);callback=strtoul(argv[4],NULL,0);
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);
 mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);mCoreConfigSetDefaultIntValue(&c->config,"logLevel",0);c->loadConfig(c,&c->config);
 video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);
 struct VFile *f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));c->reset(c);frames(300);
 c->busWrite32(c,mainAddr,0);command(0,400);capture(argv[2],"male-room");
 command(2,300);capture(argv[2],"hoenn-card");key(256);capture(argv[2],"kanto-card");key(2);frames(300);
 command(3,140);capture(argv[2],"wardrobe");key(2);frames(300);capture(argv[2],"wardrobe-cancel-room");
 command(5,400);capture(argv[2],"center-day");command(9,1200);battery(argv[2],"private-day");
 command(6,400);capture(argv[2],"center-night");command(9,1200);battery(argv[2],"private-night");
 key(8);capture(argv[2],"pause-page1");key(16);capture(argv[2],"pause-page2");key(2);frames(120);
 for (int gender=0;gender<2;gender++){
  command(gender,400);capture(argv[2],gender?"female-room-initial":"male-room-initial");command(9,1200);battery(argv[2],gender?"private-female":"private-male");
  for (int repeat=0;repeat<4;repeat++)for(int state=0;state<9;state++){
   c->busWrite32(c,0x0203fc28,state);command(8,30);command(7,2);
   unsigned errors=c->busRead32(c,0x0203fc08);
   printf("palette gender=%d repeat=%d state=%d slot=%u tag=%x errors=%u\n",gender,repeat,state,c->busRead32(c,0x0203fc0c),c->busRead32(c,0x0203fc10),errors);assert(errors==0);
  }
  command(4,350);c->busWrite32(c,0x0203fc28,0);
  for(int repeat=0;repeat<8;repeat++){
   command(3,140);key(16);key(64);key(64);key(1);frames(300);checkPalette();
   command(2,300);key(2);frames(300);checkPalette();
   command(3,140);key(16);key(2);frames(300);checkPalette();
  }
  command(9,1200);assert(c->busRead32(c,0x0203fc14)==1&&c->busRead32(c,0x0203fc1c)==1&&c->busRead32(c,0x0203fc18)==c->busRead32(c,0x0203fc20)&&c->busRead32(c,0x0203fc24)==0);
  command(4,350);checkPalette();puts("Wardrobe Apply/Cancel, Trainer Card returns and real flash roundtrip: passed");
  capture(argv[2],gender?"female-room":"male-room-return");
 }
 c->deinit(c);free(video);return 0;
}
