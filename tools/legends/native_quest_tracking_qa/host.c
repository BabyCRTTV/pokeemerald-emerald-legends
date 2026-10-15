#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static void quiet(struct mLogger *l,int category,enum mLogLevel level,const char *format,va_list args) {}
static struct mLogger logger={.log=quiet};
static struct mCore *c; static color_t *video; static unsigned mainAddr,callback,reminder;
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned k){c->setKeys(c,k);frames(2);c->setKeys(c,0);frames(100);}
static void command(unsigned n,int count){unsigned prev=c->busRead32(c,mainAddr+4);c->busWrite32(c,0x0203fc78,0);c->busWrite32(c,0x0203fc7c,prev);c->busWrite32(c,0x0203fc00,n);c->busWrite32(c,mainAddr+4,callback);frames(count);for(int n=0;n<200&&!c->busRead32(c,0x0203fc78);n++)frames(1);assert(c->busRead32(c,0x0203fc78));frames(2);}
static unsigned box(int n){return c->busRead32(c,0x0203fc00+4*n);}
static unsigned card(void){return c->busRead8(c,reminder);}
static void capture(const char *dir,const char *name){char p[4096];snprintf(p,sizeof(p),"%s/%s.rgba",dir,name);FILE *f=fopen(p,"wb");assert(f);assert(fwrite(video,4,240*160,f)==240*160);fclose(f);printf("capture %s card=%u\n",name,card());}
static void battery(const char *dir){void *data=NULL;size_t size=c->savedataClone(c,&data);assert(size==131072&&data);char p[4096];snprintf(p,sizeof(p),"%s/private-tracked.sav",dir);FILE *f=fopen(p,"wb");assert(f&&fwrite(data,1,size,f)==size);fclose(f);free(data);}
static void profile(void){command(2,2);assert(box(6)==0xb423&&box(7)==0xca03&&box(8)==3&&box(9)==2&&box(10)==3&&box(11)==1&&box(12)==3);assert(box(15)==1&&box(16)==7&&box(17)==0);}
int main(int argc,char **argv){
 setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);assert(argc==6);mainAddr=strtoul(argv[3],NULL,0);callback=strtoul(argv[4],NULL,0);reminder=strtoul(argv[5],NULL,0);
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);
 video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);struct VFile *f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));c->reset(c);frames(300);c->busWrite32(c,mainAddr,0);
 command(0,400);profile();unsigned appearance=box(5);assert(box(3)==0&&box(1)==0xffff&&box(2)==1);
 command(3,1200);profile();assert(box(13)==1&&box(14)==1&&box(3)==0&&box(5)==appearance);
 // Real pause -> journal page -> Quest Log -> Devon Delivery -> Track.
 key(8);assert(!card());capture(argv[2],"pause-off");
 key(16);key(1);key(128);key(128);key(1);capture(argv[2],"quest-detail-before");
 key(1);profile();assert(box(1)==9);capture(argv[2],"quest-detail-tracked");
 key(2);capture(argv[2],"quest-list-tracked");key(8);assert(card());capture(argv[2],"pause-journal");
 key(32);assert(card());capture(argv[2],"pause-tracked");
 // Existing DexNav help temporarily owns the same left-side card region.
 key(128);key(128);key(1);assert(!card());capture(argv[2],"dexnav-help");
 key(2);assert(card());capture(argv[2],"dexnav-return");
 // Save dialog and submenus must not retain the reminder.
 for(int i=0;i<4;i++)key(128);key(1);assert(!card());capture(argv[2],"save-dialog");
 for(int n=0;n<3&&!card();n++)key(2);assert(card());capture(argv[2],"save-return");key(2);assert(!card());
 command(3,1200);profile();assert(box(13)==1&&box(14)==1&&box(1)==9&&box(5)==appearance);
 battery(argv[2]);
 key(8);assert(card());capture(argv[2],"pause-after-flash");key(2);assert(!card());
 command(4,2);profile();assert(box(1)==9&&box(2)==2);
 key(8);capture(argv[2],"pause-next-step");assert(card());key(2);
 command(6,2);key(8);assert(!card());capture(argv[2],"safari-counter");key(2);command(7,2);
 command(5,2);profile();assert(box(1)==0xffff&&box(3)==0xa700&&box(4));
 key(8);assert(!card());capture(argv[2],"pause-completed");key(2);
 command(3,1200);profile();assert(box(13)==1&&box(14)==1&&box(1)==0xffff&&box(5)==appearance);
 printf("Native track, menu exclusion, next-step update, completion, real flash and retained profile checks passed.\n");
 c->deinit(c);free(video);return 0;
}
