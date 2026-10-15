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
static struct mCore *c; static color_t *video; static unsigned mainAddr,callback;
static void frames(int n){while(n--)c->runFrame(c);}
static void key(unsigned k){c->setKeys(c,k);frames(2);c->setKeys(c,0);frames(60);}
static void command(unsigned n,int count){c->busWrite32(c,0x0203fc00,n);c->busWrite32(c,mainAddr+4,callback);frames(count);}
static unsigned box(int n){return c->busRead32(c,0x0203fc00+4*n);}
static void capture(const char *dir,int gender,int page){char p[4096];snprintf(p,sizeof(p),"%s/%s-%02d.rgba",dir,gender==0?"male":gender==1?"female":gender==2?"mom":"norman",page);FILE *f=fopen(p,"wb");assert(f);assert(fwrite(video,4,240*160,f)==240*160);fclose(f);}
static void profile(void){command(2,2);assert(box(5)==0xb423&&box(6)==0xca03&&box(7)==3&&box(8)==2&&box(9)==3&&box(10)==1&&box(11)==3);}
int main(int argc,char **argv){
 setbuf(stdout,NULL);mLogSetDefaultLogger(&logger);assert(argc==5);mainAddr=strtoul(argv[3],NULL,0);callback=strtoul(argv[4],NULL,0);
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);
 mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);mCoreConfigSetDefaultIntValue(&c->config,"logLevel",0);c->loadConfig(c,&c->config);
 video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);
 struct VFile *f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));c->reset(c);frames(300);
 c->busWrite32(c,mainAddr,0);
 for(int gender=0;gender<2;gender++){
  command(gender,400);profile();assert(box(1)==0xffff&&!box(2));
  unsigned appearance=box(4);
  command(3,1200);profile();assert(box(12)==1&&box(13)==1&&box(1)==0xffff&&box(4)==appearance);
  key(gender?16:32);key(1);capture(argv[2],gender,0);
  int presses=0;unsigned last=0;
  for(;presses<65;presses++){
   profile();last=box(1);if(!box(2))break;
   key(1);capture(argv[2],gender,presses+1);
  }
  profile();printf("gender=%d presses=%d memory=%x script=%u dad=%u\n",gender,presses,box(1),box(2),box(3));
  assert(presses<65&&box(1)==0xd666&&!box(2)&&box(3)==16);
  command(3,1200);profile();assert(box(12)==1&&box(13)==1&&box(1)==0xd666&&box(4)==appearance);
  // Talk again after the flash round trip: existing reassurance only; no family spawn.
  key(1);
  for(int n=0;n<14;n++){profile();assert(box(3)==16);if(!box(2))break;key(1);}
  profile();assert(!box(2)&&box(1)==0xd666);
  printf("gender=%d flash roundtrip and no-repeat passed\n",gender);
 }
 command(4,2);key(1);
 for(int n=0;n<25;n++){profile();if(!box(2))break;capture(argv[2],2,n);key(1);}
 profile();assert(!box(2)&&box(1)==0xd604);
 command(5,400);key(64);key(1);
 for(int n=0;n<25;n++){profile();if(!box(2))break;capture(argv[2],3,n);key(1);}
 profile();printf("personal Mom/Norman memory=%x script=%u\n",box(1),box(2));assert(!box(2)&&box(1)==0xd614);
 c->deinit(c);free(video);return 0;
}
