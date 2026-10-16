// Load a controlled Debug-produced battery fixture through normal Release Continue.
// This host never changes the Release ROM or writes RAM/callbacks.
#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
static void quiet(struct mLogger *l,int category,enum mLogLevel level,const char *format,va_list args) {}
static struct mLogger logger={.log=quiet};static struct mCore *c;static color_t *video;static unsigned reminder;
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned k){c->setKeys(c,k);frames(2);c->setKeys(c,0);frames(120);}
static unsigned card(void){return c->busRead8(c,reminder);}
static void capture(const char *dir,const char *name){char p[4096];snprintf(p,sizeof(p),"%s/%s.rgba",dir,name);FILE *f=fopen(p,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);printf("%s card=%u\n",name,card());}
int main(int argc,char **argv){
 assert(argc==11);setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);reminder=strtoul(argv[4],NULL,0);unsigned main=strtoul(argv[5],NULL,0),overworld=strtoul(argv[6],NULL,0)|1;
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);
 video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);
 struct VFile *rom=VFileOpen(argv[1],O_RDONLY),*save=VFileOpen(argv[2],O_RDWR);assert(rom&&save&&c->loadROM(c,rom)&&c->loadSave(c,save));c->reset(c);frames(300);
 for(int n=0;n<10&&c->busRead32(c,main+4)!=overworld;n++){key(1);frames(240);}
 assert(c->busRead32(c,main+4)==overworld);capture(argv[3],"release-continued");
 unsigned sb1=c->busRead32(c,strtoul(argv[7],NULL,0)), vars=sb1+strtoul(argv[8],NULL,0);
 unsigned state=c->busRead16(c,vars+0x6b*2),done=c->busRead16(c,vars+0x6c*2),notes=c->busRead16(c,vars+0x6d*2);
 assert(state==strtoul(argv[9],NULL,0)&&done==strtoul(argv[10],NULL,0)&&notes==(state==0xffff?0xffff:0));
 printf("Continued request state=%04x done=%04x notes=%04x\n",state,done,notes);
 if(state!=0xb703){c->deinit(c);free(video);return 0;}
 key(8);assert(card());capture(argv[3],"release-pause-tracked");
 key(16);assert(card());capture(argv[3],"release-journal-page");
 key(1);assert(!card());key(16);key(128);key(1);capture(argv[3],"release-detail-tracked");
 key(1);key(2);key(8);assert(!card());capture(argv[3],"release-stopped");
 puts("Normal Release Continue loaded the battery fixture; native pause/journal/Details and stop tracking passed.");
 c->deinit(c);free(video);return 0;
}
