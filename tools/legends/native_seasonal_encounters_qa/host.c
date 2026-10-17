#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <assert.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
static void quiet(struct mLogger *l,int c,enum mLogLevel v,const char *f,va_list a){}
static struct mLogger logger={.log=quiet};static struct mCore *c;static color_t *video;static unsigned mainAddr,qa,overworld,scene;static const char *out;
static unsigned box(int n){return c->busRead32(c,0x0203fc00+n*4);}
static void frames(int n){while(n--)c->runFrame(c);}
static void command(int n,int count){unsigned previous=c->busRead32(c,mainAddr+4);c->busWrite32(c,0x0203fc00,n);c->busWrite32(c,0x0203fc04,scene);c->busWrite32(c,0x0203fc78,0);c->busWrite32(c,0x0203fc7c,previous);c->busWrite32(c,mainAddr+4,qa);frames(count);for(int i=0;i<20000&&!box(30);i++)frames(1);assert(box(30));}
static void query(void){command(2,2);}
static void key(unsigned k){c->setKeys(c,k);frames(3);c->setKeys(c,0);frames(18);}
static void cap(const char *suffix){char p[4096];snprintf(p,sizeof(p),"%s/scene-%02u-%s.rgba",out,scene,suffix);FILE *f=fopen(p,"wb");assert(f&&fwrite(video,4,240*160,f)==240*160);fclose(f);}
static void verify(void){if(box(29)){cap("FAIL");fprintf(stderr,"scene %u diagnostic failure %u\n",scene,box(29));exit(2);}assert(!box(19));for(int i=8;i<=12;i++)assert(box(i)==box(i+6));}
int main(int argc,char **argv){
 assert(argc==7);setbuf(stdout,NULL);out=argv[2];mainAddr=strtoul(argv[3],0,0);qa=strtoul(argv[4],0,0)|1;overworld=strtoul(argv[5],0,0)|1;unsigned count=strtoul(argv[6],0,0);mLogSetDefaultLogger(&logger);
 c=mCoreFind(argv[1]);assert(c&&c->init(c));mCoreInitConfig(c,NULL);mCoreConfigSetDefaultIntValue(&c->config,"skipBios",1);c->loadConfig(c,&c->config);video=calloc(240*160,sizeof(color_t));c->setVideoBuffer(c,video,240);struct VFile *f=VFileOpen(argv[1],O_RDONLY);assert(f&&c->loadROM(c,f));
 for(scene=0;scene<count;scene++){
  c->reset(c);frames(650);c->busWrite32(c,mainAddr,0);c->busWrite32(c,0x0203fc74,0);command(0,400);
  for(int i=0;i<2000&&c->busRead32(c,mainAddr+4)!=overworld;i++)frames(1);assert(c->busRead32(c,mainAddr+4)==overworld);frames(200);
  command(1,1);frames(240);query();for(int i=0;i<400&&(!box(3)||box(4));i++){frames(1);query();}assert(box(3)&&!box(4));verify();cap("gui");
  if(box(6)){
   unsigned first=box(20),animated=box(21);assert(first);int changed=0;
   for(int i=0;i<12;i++){frames(5);query();verify();if(box(20)!=first){cap("animated");changed=1;break;}}
   assert(!animated||changed);
  }
  if(scene==16){assert(box(6)==box(5)&&!box(23));key(1);query();assert(box(3)&&!box(23));verify();cap("locked");}
  if(scene==17)assert(!box(6));
  key(2);frames(240);query();assert(!box(3));verify();
  printf("PASS scene %u: 256 real wild creations, active table, level lookup, native icons/animation/palettes, closed UI and protected state\n",scene);
 }
 c->deinit(c);free(video);return 0;
}
