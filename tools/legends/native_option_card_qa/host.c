// Native compositor capture. Controlled RAM setup only; ROM bytes stay intact.
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
static void key(unsigned mask){c->setKeys(c,mask);frames(2);c->setKeys(c,0);frames(24);}
static unsigned arg(char **argv,int i){return strtoul(argv[i],NULL,0);}
static void capture(const char *dir,const char *name){char p[4096];snprintf(p,sizeof(p),"%s/%s.rgba",dir,name);FILE *f=fopen(p,"wb");assert(f);assert(fwrite(video,4,240*160,f)==240*160);fclose(f);puts(name);}
int main(int argc,char **argv){
 assert(argc==10);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);
 mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);mCoreConfigSetDefaultIntValue(&c->config,"logLevel",0);c->loadConfig(c,&c->config);
 video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);
 struct VFile *file=VFileOpen(argv[1],O_RDONLY);assert(file&&c->loadROM(c,file));
 for(unsigned layout=0;layout<4;layout++){
  c->reset(c);frames(300);
  unsigned sb2=c->busRead32(c,arg(argv,7));assert(sb2>=0x02000000&&sb2<0x02040000);
  c->busWrite8(c,sb2,0xbb);c->busWrite8(c,sb2+1,0xff);
  c->busWrite16(c,arg(argv,8),layout?1:0); // SAVE_STATUS_OK / EMPTY
  c->busWrite32(c,arg(argv,3)+4,arg(argv,4)|1); // CB2_InitMainMenu
  unsigned task=0;
  for(unsigned frame=0;frame<300&&!task;frame++){
   frames(1);
   for(unsigned i=0;i<16;i++){
    unsigned at=arg(argv,5)+40*i;
    if((c->busRead32(c,at)&~1u)==(arg(argv,6)&~1u)){
     task=at;break;
    }
   }
  }
  assert(task);c->busWrite16(c,task+8,layout);c->busWrite16(c,task+10,0);c->busWrite16(c,task+32,layout+2);
  frames(100);char name[80];snprintf(name,sizeof(name),"layout-%u-unselected",layout);capture(argv[2],name);
  for(unsigned i=0;i<layout+1;i++)key(128);
  snprintf(name,sizeof(name),"layout-%u-selected",layout);capture(argv[2],name);
  assert((c->busRead32(c,task)&~1u)==(arg(argv,9)&~1u));
  assert(c->busRead16(c,task+10)==layout+1);
  if(layout<2){key(1);frames(100);snprintf(name,sizeof(name),"layout-%u-options-open",layout);capture(argv[2],name);key(2);frames(180);snprintf(name,sizeof(name),"layout-%u-options-return",layout);capture(argv[2],name);}
 }
 c->deinit(c);free(video);puts("All four layout selections and native Options open/return paths captured.");return 0;
}
